"""Item 1: the JAX Flow-Lenia level against level0/flowlenia.py on A_gliders; mass; timing.

usage: python -B check_level0.py [N_STEPS]          -> results/level0_check.json, level0_divergence.png

(a) one-step agreement: from every numpy state A_np(t), t < N, one JAX substep vs numpy's A_np(t+1);
(b) free-running agreement: JAX and numpy trajectories from init.npz for N steps;
(c) the rounding floor: numpy against numpy started from init.npz perturbed by one ulp (relative
    2^-52 noise), i.e. how much the dynamics itself amplifies a rounding-sized difference;
(d) the stored level0/worlds/A_gliders/state_t4000.npz (numpy, original environment);
(e) mass: deterministic run, noisy level (flow noise 0.5) and the zero-sum kick;
(f) time per substep and per tick (20 substeps): single member, vmap over 8 and 32, lax.map.
"""
import json
import sys
import time

import _paths
import jax
import jax.numpy as jnp
import numpy as np

import flowlenia as fl
import flowlenia_jax as FJ
import vw

N = int(sys.argv[1]) if len(sys.argv) > 1 else 4000
cfg, params, meta = FJ.load_world("A_gliders")
pnp = FJ.numpy_params(cfg, params)
A0 = np.load(f"{_paths.L0_DIR}/worlds/A_gliders/init.npz")["A0"]
fK = FJ.kernel_fft(cfg, params)
jstep = jax.jit(lambda A: FJ.substep(cfg, params, A, fK=fK))
out = {"world": "A_gliders", "steps": N, "shape": list(A0.shape), "dtype": "float64",
       "jax": jax.__version__, "numpy": np.__version__}

# kernels
out["kernel_maxabs_diff"] = float(np.abs(np.asarray(jnp.fft.irfft2(fK, s=(cfg.H, cfg.W))) - fl.kernels(pnp, cfg.H, cfg.W)).max())

# (a)-(c)
rng = np.random.default_rng(0)
A_np = A0.copy()
A_pert = A0 * (1.0 + 2.0 ** -52 * rng.choice([-1.0, 1.0], A0.shape))
A_j = jnp.asarray(A0)
one, free, floor, scale = [], [], [], []
mass_j, mass_n = [], []
t0 = time.time()
for t in range(N):
    A_next = fl.step(A_np, pnp)
    one.append(float(np.abs(np.asarray(jstep(jnp.asarray(A_np))) - A_next).max()))
    A_j = jstep(A_j)
    A_pert = fl.step(A_pert, pnp)
    A_np = A_next
    Aj = np.asarray(A_j)
    free.append(float(np.abs(Aj - A_np).max()))
    floor.append(float(np.abs(A_pert - A_np).max()))
    scale.append(float(A_np.max()))
    mass_j.append(Aj.sum((1, 2)))
    mass_n.append(A_np.sum((1, 2)))
    if (t + 1) % 500 == 0:
        print(t + 1, one[-1], free[-1], floor[-1], round(time.time() - t0, 1), flush=True)
mass_j, mass_n = np.array(mass_j), np.array(mass_n)
m0 = A0.sum((1, 2))
one, free, floor = np.array(one), np.array(free), np.array(floor)
out["one_step"] = {"max_abs": float(one.max()), "median_abs": float(np.median(one)),
                   "max_rel_to_state_max": float((one / np.array(scale)).max())}
marks = [m for m in (1, 10, 100, 500, 1000, 2000, 3000, 4000, N) if m <= N]
out["free_running"] = {"max_abs_at": {str(m): float(free[m - 1]) for m in sorted(set(marks))},
                       "max_abs_over_first_2000": float(free[:2000].max()),
                       "max_abs_over_all": float(free.max())}
out["rounding_floor_numpy_vs_numpy_1ulp"] = {"max_abs_at": {str(m): float(floor[m - 1]) for m in sorted(set(marks))},
                                             "max_abs_over_all": float(floor.max())}
out["state_max"] = float(np.max(scale))
out["mass"] = {"jax_max_rel_drift": float(np.abs(mass_j / m0 - 1).max()),
               "numpy_max_rel_drift": float(np.abs(mass_n / m0 - 1).max()), "mass0": m0.tolist()}
if N >= 4000:
    ref = np.load(f"{_paths.L0_DIR}/worlds/A_gliders/state_t4000.npz")["A"]
    Aj4000 = np.asarray(A_j) if N == 4000 else None
    out["stored_state_t4000"] = {"numpy_here_vs_stored_max_abs": float(np.abs(A_np - ref).max()) if N == 4000 else None,
                                 "jax_vs_stored_max_abs": float(np.abs(Aj4000 - ref).max()) if N == 4000 else None}
np.savez_compressed(f"{_paths.RESULTS}/level0_divergence.npz", one=one, free=free, floor=floor)

# (e) noisy level and kick: mass
lev, _, _ = FJ.make_level("A_gliders", 0.5)
L20 = vw.stride_level(lev, 20)
key = jax.random.key(3)
traj_end = jax.jit(lambda x: jax.lax.fori_loop(0, 50, lambda t, xx: L20.step(params, xx, vw.Noise(key, t), jnp.zeros(cfg.H * cfg.W)), x))
An = np.asarray(traj_end(jnp.asarray(A0)))
u = np.zeros(cfg.H * cfg.W)
S = A0.sum(0).ravel()
src, snk = np.argsort(-S)[:4], np.argsort(S)[:4]
u[src], u[snk] = -0.9, 0.9
Ak = np.asarray(jax.jit(lambda A, u: FJ.kick(cfg, A, u))(jnp.asarray(A0), jnp.asarray(u)))
Ak_np = Ak  # VW-0 kick for comparison
import lenia_world as LW  # noqa: E402
l0 = LW.Level0("A_gliders", 20, 0.0)
Ak_vw0 = l0.kick(A0.ravel()[None], u[None])[0].reshape(A0.shape)
out["mass_noisy_level"] = {"substeps": 1000, "flow_noise_std": 0.5,
                           "max_rel_drift": float(np.abs(An.sum((1, 2)) / m0 - 1).max())}
out["kick"] = {"max_abs_diff_vs_vw0_kick": float(np.abs(Ak - Ak_vw0).max()),
               "rel_mass_change": float(np.abs(Ak.sum((1, 2)) / m0 - 1).max()), "min_value": float(Ak.min())}
print(json.dumps({k: out[k] for k in ("one_step", "free_running", "mass", "mass_noisy_level", "kick")}, indent=1))


# (f) timing
def tm(f, *a, n=10):
    jax.block_until_ready(f(*a))
    t = time.time()
    for _ in range(n):
        r = f(*a)
    jax.block_until_ready(r)
    return (time.time() - t) / n


sub = lambda A: FJ.substep(cfg, params, A, fK=fK)   # noqa: E731
lev_step = lambda A, k: lev.step(params, A, vw.Noise(k, 0), jnp.zeros(cfg.H * cfg.W))  # noqa: E731
tick = lambda A, k: L20.step(params, A, vw.Noise(k, 0), jnp.zeros(cfg.H * cfg.W))  # noqa: E731
A0j = jnp.asarray(A0)
_t = time.time()
for _ in range(20):
    fl.step(A0, pnp)
T = {"numpy_substep_ms": 1e3 * (time.time() - _t) / 20}
T["jax_substep_deterministic_ms"] = 1e3 * tm(jax.jit(sub), A0j, n=40)
T["jax_substep_level_ms"] = 1e3 * tm(jax.jit(lev_step), A0j, key, n=40)
T["jax_tick20_ms"] = 1e3 * tm(jax.jit(tick), A0j, key, n=5)
for B in (8, 32):
    AB = jnp.broadcast_to(A0j, (B,) + A0j.shape) + 0.0
    kB = jax.random.split(key, B)
    T[f"vmap{B}_substep_ms_per_member"] = 1e3 * tm(jax.jit(jax.vmap(lev_step)), AB, kB) / B
    T[f"laxmap{B}_substep_ms_per_member"] = 1e3 * tm(jax.jit(lambda X, K: jax.lax.map(lambda a: lev_step(*a), (X, K))), AB, kB) / B
    T[f"vmap{B}_tick20_ms_per_member"] = 1e3 * tm(jax.jit(jax.vmap(tick)), AB, kB, n=2) / B
    T[f"laxmap{B}_tick20_ms_per_member"] = 1e3 * tm(jax.jit(lambda X, K: jax.lax.map(lambda a: tick(*a), (X, K))), AB, kB, n=2) / B
out["timing"] = T
out["timing_note"] = "CPU, 2 cores (taskset), float64; per substep unless 'tick20' (20 substeps + kick each)"
print(json.dumps(T, indent=1))
json.dump(out, open(f"{_paths.RESULTS}/level0_check.json", "w"), indent=1)

# plot
import matplotlib  # noqa: E402
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
fig, ax = plt.subplots(figsize=(7, 3.6))
ts = np.arange(1, N + 1)
ax.semilogy(ts, np.maximum(one, 1e-18), lw=0.6, label="one step from the numpy state")
ax.semilogy(ts, np.maximum(free, 1e-18), lw=1.0, label="free running, JAX vs numpy")
ax.semilogy(ts, np.maximum(floor, 1e-18), lw=1.0, ls="--", label="numpy vs numpy, 1-ulp start")
ax.set_xlabel("Flow-Lenia step")
ax.set_ylabel("max |difference| (state max ~1.2)")
ax.legend(fontsize=8)
ax.set_title("A_gliders: JAX level vs level0/flowlenia.py", fontsize=10)
fig.tight_layout()
fig.savefig(f"{_paths.RESULTS}/level0_divergence.png", dpi=120)
