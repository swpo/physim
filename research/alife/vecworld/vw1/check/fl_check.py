"""Independent re-run: JAX Flow-Lenia (port/flowlenia_jax.py) vs numpy (level0/flowlenia.py,
integrate/lenia_world.Level0) on A_gliders, and mass conservation. Writes check/fl_check.json.
Run: ../.venv/bin/python -B fl_check.py  (from vw1/check)."""
import json
import os
import sys
import time

sys.dont_write_bytecode = True
HERE = os.path.dirname(os.path.abspath(__file__))
VW1 = os.path.dirname(HERE)
VEC = os.path.dirname(VW1)
sys.path.insert(0, VW1)
sys.path.insert(0, os.path.join(VW1, "port"))
for p in (os.path.join(VEC, "integrate"), os.path.join(VEC, "spec"), os.path.join(VEC, "level0")):
    sys.path.append(p)

import jax  # noqa: E402
import jax.numpy as jnp  # noqa: E402
import numpy as np  # noqa: E402

import flowlenia as fl  # noqa: E402
import flowlenia_jax as FJ  # noqa: E402
import lenia_world as LW  # noqa: E402
import vw  # noqa: E402

out = {}
cfg, params, meta = FJ.load_world("A_gliders")
pnp = FJ.numpy_params(cfg, params)
A0 = np.load(os.path.join(VEC, "level0", "worlds", "A_gliders", "init.npz"))["A0"]
fK = FJ.kernel_fft(cfg, params)
jstep = jax.jit(lambda A: FJ.substep(cfg, params, A, fK=fK))
jnoisy = jax.jit(lambda A, xi: FJ.substep(cfg, params, A, xi, 0.5, fK=fK))
jkick = jax.jit(lambda A, u: FJ.kick(cfg, A, u))
l0 = LW.Level0("A_gliders", 20, 0.5)
rng = np.random.default_rng(20261106)

# (1) numpy reference trajectory to step 1200 (deterministic); one JAX substep from sampled states
t0 = time.time()
A = A0.copy()
states = {}
for t in range(1200):
    if t % 12 == 0:
        states[t] = A.copy()
    A = fl.step(A, pnp)
states[1200] = A
one = []
for t in sorted(states)[:-1]:
    ref = fl.step(states[t], pnp)
    one.append(float(np.abs(np.asarray(jstep(jnp.asarray(states[t]))) - ref).max()))
out["one_substep_det"] = {"n_states": len(one), "max_abs": max(one), "median_abs": float(np.median(one)),
                          "state_max": float(max(s.max() for s in states.values()))}

# (2) one noisy substep with the SAME flow noise (numpy Level0.substep vs JAX substep)
noisy = []
for t in list(sorted(states))[::10]:
    z = rng.standard_normal((2,) + A0.shape)
    ref = l0.substep(states[t], z)
    noisy.append(float(np.abs(np.asarray(jnoisy(jnp.asarray(states[t]), jnp.asarray(z))) - ref).max()))
out["one_substep_noisy_same_xi"] = {"n": len(noisy), "max_abs": max(noisy)}

# (3) the zero-sum kick, numpy vs JAX, including sources on empty and dense cells; channel masses
kick = []
HW = cfg.H * cfg.W
for t in list(sorted(states))[::20]:
    S = states[t].sum(0).ravel()
    for trial in range(3):
        u = np.zeros(HW)
        dense, empty = np.argsort(-S)[:3], np.argsort(S)[:3]
        rnd = rng.choice(HW, 10, replace=False)
        idx = np.unique(np.concatenate([dense, empty, rnd]))[:16]
        v = rng.uniform(-1, 1, idx.size)
        v -= v.mean()
        u[idx] = v
        u[idx[np.argmax(np.abs(v))]] -= u.sum()
        kn = l0.kick(states[t].ravel()[None], u[None])[0].reshape(A0.shape)
        kj = np.asarray(jkick(jnp.asarray(states[t]), jnp.asarray(u)))
        m0 = states[t].sum((1, 2))
        kick.append((float(np.abs(kj - kn).max()), float(np.abs(kj.sum((1, 2)) / m0 - 1).max()),
                     float(kj.min())))
k = np.array(kick)
out["kick"] = {"n": len(kick), "max_abs_jax_vs_numpy": float(k[:, 0].max()),
               "max_rel_channel_mass_change": float(k[:, 1].max()), "min_value": float(k[:, 2].min())}

# (4) one full VW-0 tick (kick + 20 noisy substeps, same xi) numpy vs JAX
tick = []
for t in (300, 600, 1200):
    h = states[t].ravel()[None]
    u = np.zeros(HW)
    idx = rng.choice(HW, 8, replace=False)
    v = rng.uniform(-0.5, 0.5, 8)
    v -= v.mean()
    u[idx] = v
    xi = rng.standard_normal((1, l0.noise_dim))
    ref = l0.law(l0.kick(h, u[None]), xi)[0].reshape(A0.shape)
    Aj = jkick(jnp.asarray(states[t]), jnp.asarray(u))
    m = 2 * l0.n0
    for s in range(20):
        Aj = jnoisy(Aj, jnp.asarray(xi[0, s * m:(s + 1) * m].reshape((2,) + A0.shape)))
    tick.append(float(np.abs(np.asarray(Aj) - ref).max()))
out["one_vw0_tick_same_xi_max_abs"] = tick

# (5) free running from step 600 for 150 deterministic substeps: JAX vs numpy, numpy vs numpy+1ulp
An = states[600].copy()
Ap = An * (1.0 + 2.0 ** -52 * rng.choice([-1.0, 1.0], An.shape))
Aj = jnp.asarray(An)
free, floor = [], []
for t in range(150):
    An = fl.step(An, pnp)
    Ap = fl.step(Ap, pnp)
    Aj = jstep(Aj)
    free.append(float(np.abs(np.asarray(Aj) - An).max()))
    floor.append(float(np.abs(Ap - An).max()))
free, floor = np.array(free), np.array(floor)
cross = lambda e, thr: int(np.argmax(e > thr)) + 1 if (e > thr).any() else None  # noqa: E731
out["free_running_from_600"] = {"jax_vs_numpy_first_step_above_1e-6": cross(free, 1e-6),
                                "numpy_1ulp_first_step_above_1e-6": cross(floor, 1e-6),
                                "jax_vs_numpy_at": {str(s): float(free[s - 1]) for s in (1, 10, 20, 40, 80, 150)},
                                "numpy_1ulp_at": {str(s): float(floor[s - 1]) for s in (1, 10, 20, 40, 80, 150)},
                                "growth_rate_per_step_jax": float(np.polyfit(np.arange(10, 60), np.log(free[10:60]), 1)[0])}

# (6) mass: the VW-1 level, stride 20, noise 0.5, a random zero-sum kick every tick, 25 ticks
lev, _, _ = FJ.make_level("A_gliders", 0.5)
L20 = vw.stride_level(lev, 20)
tickj = jax.jit(lambda x, t, u: L20.step(params, x, vw.Noise(jax.random.key(7), t), u))
x = jnp.asarray(states[600])
m0 = np.asarray(x.sum((1, 2)))
drift = []
for t in range(25):
    u = np.zeros(HW)
    idx = rng.choice(HW, 16, replace=False)
    v = rng.uniform(-1, 1, 16)
    v -= v.mean()
    u[idx] = v
    u[idx[0]] -= u.sum()
    x = tickj(x, t, jnp.asarray(u))
    drift.append(float(np.abs(np.asarray(x.sum((1, 2))) / m0 - 1).max()))
out["mass_25_ticks_500_noisy_substeps_with_kicks"] = {"max_rel_drift_per_channel": max(drift),
                                                      "min_value": float(np.asarray(x).min())}
out["seconds"] = round(time.time() - t0, 1)
print(json.dumps(out, indent=1))
json.dump(out, open(os.path.join(HERE, "fl_check.json"), "w"), indent=1)
