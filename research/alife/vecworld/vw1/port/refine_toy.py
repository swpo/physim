"""Item 4 (refine): a level -1 under the library's nonlinear mass ring, exact and leaky.

usage: python -B refine_toy.py   -> results/refine_toy.json

Coarse world: vw.toys.mass_ring (16 cells, pooling kick, diffusion, mass-conserving random
fluxes; Phi = 4 block sums; zero-sum k = 4 inputs; observation noise 0.05).
Level -1: every cell split into two sub-cells, z (16, 2), psi(z) = z.sum(1); the hidden split
q = z[:, 0] / c relaxes to 1/2 with its own noise (stream 1).
  exact   the cell totals follow the coarse law with the SAME noise draws: psi o F_-1 = F_0 o psi
          pathwise (strong lumpability); the kick acts on psi(z), so (R1) holds by construction
  leaky_mean  diffusion between cells i and i+1 reads the facing sub-cells (weight eta = 0.5):
          the conditional MEAN of the cell totals depends on the hidden split
  leaky_var   the random flux amplitude is modulated by the facing sub-cells,
          f_i -> f_i (1 + eta (q_(i+1) - q_i)): only the conditional VARIANCE depends on the split
Checks: vw.commutation_error (pathwise and distributional, with and without an input), vw.refine
with check/tol, pathwise invisibility of the exact refinement (same keys -> identical observations,
identical exam scores), and vw.closure on the three worlds (the gap moves only under the leaky one).
"""
import json
import time

import _paths
import jax
import jax.numpy as jnp
import numpy as np

import vw
from vw import toys

t_start = time.time()
n, G = 16, 4
coarse_spec = toys.mass_ring(n=n, G=G)
Lc = coarse_spec.base
D, SIG = 0.15, 1.0


def ring_step(x, nz, u, factor=None, q=None, eta_d=0.0):
    """vw.toys.mass_ring_level's law; optional leaks: a flux factor (noise amplitude) and, with the
    split q, diffusion through the facing sub-cells (weight eta_d). Neither: the library law."""
    x = toys.pool_kick(x, u)
    if eta_d == 0.0:
        x = x + D * (jnp.roll(x, 1) + jnp.roll(x, -1) - 2 * x)
    else:                                   # J_i: net flow from cell i+1 into cell i
        left, right = 2 * x * q, 2 * x * (1 - q)
        J = D * ((1 - eta_d) * (jnp.roll(x, -1) - x) + eta_d * (jnp.roll(left, -1) - right))
        x = x + J - jnp.roll(J, 1)
    f = 0.25 * jnp.tanh(SIG * nz.normal((n,))) * jnp.minimum(x, jnp.roll(x, -1))
    if factor is not None:
        f = f * factor
    return x - f + jnp.roll(f, 1)


def fine_level(kind: str, eta: float = 0.5, kappa: float = 0.3, s_int: float = 0.1) -> vw.Level:
    def init(p, key):
        c = Lc.init(p, key)
        q = jax.random.uniform(jax.random.fold_in(key, 7), (n,), minval=0.2, maxval=0.8)
        return jnp.stack([c * q, c * (1 - q)], 1)

    def step(p, z, nz, u):
        c = z.sum(1)
        q = jnp.where(c > 0, z[:, 0] / jnp.where(c > 0, c, 1.0), 0.5)
        if kind == "exact":
            c2 = Lc.step(p, c, nz, u)                       # the library's coarse law, same draws
        elif kind == "leaky_mean":                          # diffusion reads the facing sub-cells
            c2 = ring_step(c, nz, u, q=q, eta_d=eta)
        else:                                               # the split modulates the flux amplitude
            c2 = ring_step(c, nz, u, factor=1.0 + eta * (jnp.roll(q, -1) - q))
        q2 = jnp.clip(q + kappa * (0.5 - q) + s_int * nz.stream(1).normal((n,)), 0.0, 1.0)
        return jnp.stack([c2 * q2, c2 * (1 - q2)], 1)

    return vw.Level(init=init, step=step, input_dim=n, conserved={"mass": jnp.sum}, name=f"ring-split({kind})")


psi = vw.CoarseGrain.of(lambda z: z.sum(1), name="pair-sum")
out = {"n_cells": n, "blocks": G}
# the reimplemented law equals the library's
x0 = Lc.init(None, jax.random.key(1))
key = jax.random.key(2)
out["ring_step_equals_library"] = float(jnp.abs(ring_step(x0, vw.Noise(key, 0), jnp.zeros(n)) -
                                                Lc.step(None, x0, vw.Noise(key, 0), jnp.zeros(n))).max())
u_test = jnp.zeros(n).at[jnp.array([1, 5, 9, 13])].set(jnp.array([-0.6, 0.6, -0.3, 0.3]))   # admissible: k=4, sum 0, total 1.8
fines = {k: fine_level(k) for k in ("exact", "leaky_mean", "leaky_var")}
ce = {}
for nm, Lf in fines.items():
    r0 = vw.commutation_error(Lf, psi, Lc, T=(1, 2, 4), n=2000, n_rep=16, seed=0)
    r1 = vw.commutation_error(Lf, psi, Lc, T=(1, 2, 4), n=2000, n_rep=16, seed=1, u=u_test)
    ce[nm] = {"free": {k: r0[k] for k in ("T", "delta2_pathwise", "delta2", "mc_bias")},
              "with_input_at_t0": {k: r1[k] for k in ("delta2_pathwise", "delta2")}}
out["commutation_error"] = ce
# refine with a tolerance
refined = {}
s_exact = vw.refine(coarse_spec, fines["exact"], psi, check=dict(T=(1,), n=1000, n_rep=8), tol=1e-20)
refined["exact"] = s_exact
for k in ("leaky_mean", "leaky_var"):
    try:
        vw.refine(coarse_spec, fines[k], psi, check=dict(T=(1,), n=1000, n_rep=8), tol=1e-3)
        out[f"refine_{k}_with_tol_1e-3"] = "accepted"
    except ValueError as e:
        out[f"refine_{k}_with_tol_1e-3"] = f"ValueError: {str(e)[:100]}"
for k in ("leaky_mean", "leaky_var"):
    refined[k] = vw.refine(coarse_spec, fines[k], psi, check=dict(T=(1,), n=1000, n_rep=8))
out["refine_check_stored"] = {k: {kk: vv for kk, vv in s.meta["refine_check"].items() if kk in ("delta2_pathwise", "delta2")}
                              for k, s in refined.items()}

# pathwise invisibility: same world seed, coupled initial states, shared member keys
wc = vw.World(coarse_spec, world_seed=4)
inv = {}
for nm, s in refined.items():
    wf = vw.World(s, world_seed=4)
    assert np.array_equal(wf.in_map, wc.in_map) and np.array_equal(wf.out_map, wc.out_map)
    ens_f = wf.designer.ensemble(256, seed=(3,))
    z = ens_f.carry.x
    keys = ens_f.carry.key
    ef = wf.designer.from_states(z, keys=keys)
    ec = wc.designer.from_states(jax.vmap(lambda zz: zz.sum(1))(z), keys=keys)
    rng = np.random.default_rng(0)
    progs = [wc.designer.random_program(rng, 20, 0.5) for _ in range(256)]
    P = np.stack([wc.designer.program_dense(p, 20) for p in progs])
    _, rf = wf.designer.rollout(ef, P, T=20, rec=("obs_continuous",))
    _, rc = wc.designer.rollout(ec, P, T=20, rec=("obs_continuous",))
    dif = np.abs(rf["obs_continuous"] - rc["obs_continuous"])
    inv[nm] = {"max_abs_obs_diff_tick1": float(dif[:, 1].max()), "max_abs_obs_diff_20_ticks": float(dif.max()),
               "rms_obs_diff_tick20": float(np.sqrt((dif[:, 20] ** 2).mean()))}
    # exam: same exam seed and world seed
    ex_c = vw.Exam(wc, n_items=64, prefix=8, horizon=8, queries=(1, 2, 4, 8), exam_seed=2)
    ex_f = vw.Exam(wf, n_items=64, prefix=8, horizon=8, queries=(1, 2, 4, 8), exam_seed=2)
    pub_same = all(np.array_equal(a["past_obs"], b["past_obs"]) for a, b in zip(ex_c.public(), ex_f.public()))
    sc_c, sc_f = ex_c.score(n_rep=16), ex_f.score(n_rep=16)
    inv[nm]["exam_public_items_identical"] = bool(pub_same)
    inv[nm]["exam_past_obs_max_abs_diff"] = float(max(np.abs(a["past_obs"] - b["past_obs"]).max()
                                                      for a, b in zip(ex_c.public(), ex_f.public())))
    inv[nm]["exam_persistence_mse_coarse"] = sc_c["mse"]["persistence"]
    inv[nm]["exam_persistence_mse_refined"] = sc_f["mse"]["persistence"]
    inv[nm]["exam_oracle_coarse"] = sc_c["oracle"]
    inv[nm]["exam_oracle_refined"] = sc_f["oracle"]
out["invisibility"] = inv

# closure on the three worlds (library certificate, cheap toy)
cl = {}
for nm, s in (("coarse", coarse_spec), *((f"refined_{k}", v) for k, v in refined.items())):
    c = vw.closure(vw.World(s, world_seed=4), horizons=(1, 2, 4), pasts=(0, 1, 2, 4, 8), n_traj=20000, n_oracle=4000,
                   n_rep=16, seed=0)
    cl[nm] = {"gap_nats_tau1": c["gap_nats"][0], "ceiling_tau1": c["ceiling"][0], "Vu": c["Vu"], "se_gap_tau1": c["se"]["gap_nats"][0],
              "pasts": c["pasts"]}
    print(nm, json.dumps(vw.jsonable(cl[nm])), flush=True)
out["closure"] = cl
out["seconds"] = time.time() - t_start
print(json.dumps(vw.jsonable({k: v for k, v in out.items() if k != "closure"}), indent=1)[:4000])
json.dump(vw.jsonable(out), open(f"{_paths.RESULTS}/refine_toy.json", "w"), indent=1)
