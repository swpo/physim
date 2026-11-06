"""Item 5, second estimator: the mean response dE[o]/dtheta by the likelihood-ratio identity.

usage: python -B fisher_lr.py N [TICKS]  -> results/fisher_lr.json (TICKS = 1) or fisher_lr_T<TICKS>_N<N>.json

Same world, parameters, members and keys as fisher_demo.py (one tick = 20 substeps from x*). The
flow noise is additive Gaussian on the flow field, Phi_s = F_theta(x_s) + std * xi_s, and the next
state is a deterministic function of (x_s, Phi_s). So the path density is prod_s N(Phi_s;
F_theta(x_s), std^2 I) and
    d E[o] / d theta = E[(o - E o) * score],   score = sum_s <xi_s, d_theta F_theta(x_s)> / std,
where d_theta F is taken at the FIXED realised state x_s: no derivative is propagated through the
chaotic dynamics, so the estimator's variance grows with the number of substeps, not
exponentially. Compared on the same paths with the pathwise (autodiff) mean derivative, and both
plugged into the moment bound Jbar^T S^-1 Jbar (debiased for the estimator noise).
"""
import json
import math
import sys
import time

import _paths
import jax
import jax.numpy as jnp
import numpy as np

import vw
from vw.world import _NS_CERT, _ST_DYN, _ST_OBS, _ST_PROC, make_key, member_keys
import aworld as AW
import flowlenia_jax as FJ

N = int(sys.argv[1]) if len(sys.argv) > 1 else 2048
TICKS = int(sys.argv[2]) if len(sys.argv) > 2 else 1
CHUNK = min(64, N)
t_start = time.time()
specs, parts = AW.build(with_objects=False)
lev, cfg, pc = parts["level"], parts["cfg"], parts["phi_coarse"]
p0 = lev.params
xstar = AW.MapWorld(specs["coarse"], world_seed=0).designer.ensemble(1, seed=(301,)).carry.x[0]
sig = AW.OBS.quantum / math.sqrt(12.0)
std = AW.NOISE_STD
shape = (cfg.C, cfg.H, cfg.W)
theta0 = jnp.array([float(p0["m"][0]), float(p0["R"])])


def embed(theta):
    p = dict(p0)
    p["m"] = p0["m"].at[0].set(theta[0])
    p["R"] = theta[1]
    return p


ki_all = member_keys(make_key(_NS_CERT, 0, 81, 0), N)
kd_all = jax.vmap(lambda k: jax.random.fold_in(k, _ST_DYN))(ki_all)


def noise_of(kd, j):
    """The world's draw for substep j (tick j // 20, substep j % 20): Noise(fold(kd, PROC), t).substep(20, i)."""
    return vw.Noise(jax.random.fold_in(kd, _ST_PROC), j // AW.STRIDE).substep(AW.STRIDE, j % AW.STRIDE).normal((2,) + shape)


def obs_of(x, kd):
    y = pc.phi(x, ())
    return y + sig * jax.random.normal(jax.random.fold_in(jax.random.fold_in(kd, _ST_OBS), TICKS), y.shape)


def path(theta, kd, with_score=True):
    """One tick from x*: (o, score) with the LR score at fixed realised states."""
    p = embed(theta)
    fK = FJ.kernel_fft(cfg, p)
    u0 = jnp.zeros(cfg.H * cfg.W)

    def flow_th(th, x):
        pp = embed(th)
        return FJ.flow(cfg, pp, x, FJ.kernel_fft(cfg, pp))

    def body(carry, i):
        x, score = carry
        x = FJ.kick(cfg, x, u0)
        xi = noise_of(kd, i)
        Fy, Fx = FJ.flow(cfg, p, x, fK)
        if with_score:
            dFy, dFx = jax.jacfwd(lambda th: flow_th(th, jax.lax.stop_gradient(x)))(theta)    # (C,H,W,2)
            score = score + (jnp.einsum("chw,chwk->k", xi[0], dFy) + jnp.einsum("chw,chwk->k", xi[1], dFx)) / std
        Fy, Fx = jax.lax.optimization_barrier((Fy + std * xi[0], Fx + std * xi[1]))
        return (FJ.reintegrate(cfg, x, Fy, Fx), score), None

    (x, score), _ = jax.lax.scan(body, (xstar, jnp.zeros(2)), jnp.arange(TICKS * AW.STRIDE))
    return obs_of(x, kd), score


def path_o(theta, kd):
    return path(theta, kd, with_score=False)[0]


def chunk_fn(kds):
    def one(kd):
        o, sc = path(theta0, kd)
        J = jax.jacfwd(path_o)(theta0, kd)
        return o, sc, J
    return jax.lax.map(one, kds)


cf = jax.jit(chunk_fn)
O, SC, JJ = [], [], []
for s in range(0, N, CHUNK):
    o, sc, J = cf(kd_all[s:s + CHUNK])
    O.append(np.asarray(o))
    SC.append(np.asarray(sc))
    JJ.append(np.asarray(J))
    if (s // CHUNK) % 8 == 7:
        print("members", s + CHUNK, round(time.time() - t_start, 1), "s", flush=True)
O, SC, JJ = np.concatenate(O), np.concatenate(SC), np.concatenate(JJ)       # (N, m), (N, 2), (N, m, 2)
Nn, m = O.shape
ob = O.mean(0)
S = np.cov(O.T, ddof=1)
Si = np.linalg.inv(S)
wish = (Nn - m - 2) / (Nn - 1)
est = {"pathwise_AD": JJ, "likelihood_ratio": (O - ob)[:, :, None] * SC[:, None, :]}
out = {"N": Nn, "m": int(m), "ticks": TICKS, "theta_names": ["m_0", "R"], "score_mean": SC.mean(0), "score_sd": SC.std(0, ddof=1)}
for k, E in est.items():
    Jbar = E.mean(0)
    D = E - Jbar
    noise = np.einsum("nmi,mk,nkj->ij", D, Si, D) / (Nn - 1) / Nn
    raw = Jbar.T @ Si @ Jbar
    out[k] = {"Jbar_norm": np.linalg.norm(Jbar, axis=0), "per_sample_rms": np.sqrt((D ** 2).sum(1).mean(0)),
              "Jbar_snr": np.linalg.norm(Jbar, axis=0) / np.sqrt((D ** 2).sum((0, 1)) / (Nn - 1) / Nn),
              "lower_raw": raw, "estimator_noise_term": noise, "lower_debiased": wish * raw - noise,
              "lower_debiased_se_diag": np.sqrt(2 * np.diag(noise) ** 2 + 4 * np.diag(noise) * np.maximum(np.diag(wish * raw - noise), 0))}
    print(k, json.dumps(vw.jsonable(out[k])), flush=True)
Ja, Jl = est["pathwise_AD"].mean(0), est["likelihood_ratio"].mean(0)
Da, Dl = est["pathwise_AD"] - Ja, est["likelihood_ratio"] - Jl
se_diff = np.sqrt(((Da - Dl) ** 2).sum(0) / (Nn - 1) / Nn)            # per coordinate, paired
out["agreement"] = {"z_rms_over_coords": np.sqrt((((Ja - Jl) / np.maximum(se_diff, 1e-300)) ** 2).mean(0)),
                    "corr_Jbar_AD_LR": [float(np.corrcoef(Ja[:, i], Jl[:, i])[0, 1]) for i in range(2)]}
out["seconds"] = time.time() - t_start
print(json.dumps(vw.jsonable(out["agreement"])), flush=True)
fn = "fisher_lr.json" if TICKS == 1 and N == 2048 else f"fisher_lr_T{TICKS}_N{N}.json"
json.dump(vw.jsonable(out), open(f"{_paths.RESULTS}/{fn}", "w"), indent=1)
