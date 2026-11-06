"""Item 5: Fisher information of the coarse observation about two Flow-Lenia parameters, by autodiff.

usage: python -B fisher_demo.py N NFD NGROW     -> results/fisher.json

theta = (m_0, R): the growth centre of kernel 0 (channel 0 -> 0) and the global kernel radius R
(all kernel widths scale with R + 15). World: A_gliders level 0 prepared in one post-burn-in state
x* (a lab's "identical samples": mu = delta_x*, so derivatives run only through the horizon),
Phi_coarse observed after one tick (192 numbers, 20 noisy substeps). The port's quantum 1e-3 is
replaced by its Gaussian stand-in, noise q / sqrt(12) (Fisher needs sigma_o > 0; note, Sec. 9).

Per member n (keys as vw.certificates.fisher): o_n and the pathwise Jacobian J_n = do_n/dtheta
(jax.jacfwd through the World's rollout: lax.map over members, lax.scan over substeps, FFTs, the
scatter of the reintegration tracking). Reported, 2 x 2:
  lower     Jbar^T S^-1 Jbar (S = Cov o): the moment bound, <= I_o for any law of o (as vw.fisher);
            raw, and debiased (Wishart factor (N-m-2)/(N-1), minus tr(S^-1 Cov J_n)/N for the noise in Jbar)
  gaussian  raw lower + 1/2 tr(S^-1 dS_i S^-1 dS_j): exact if o were Gaussian (as vw.fisher)
  upper     E[J_n^T J_n] / sigma_o^2: the complete-data information of (process noise, o), an upper
            bound on I_o (note, open question 5)
Cross-checks: vw.fisher(world, wrt=['R']) on the first 256 members against this code (same keys);
central finite differences with common random numbers on NFD members at two step sizes; and, on
NGROW members, the growth of the pathwise derivative from tick 1 to tick 2 (chaos).
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
from vw.world import _NS_CERT, _ST_DYN, make_key, member_keys
import aworld as AW

N = int(sys.argv[1]) if len(sys.argv) > 1 else 2048
NFD = int(sys.argv[2]) if len(sys.argv) > 2 else 128
NGROW = int(sys.argv[3]) if len(sys.argv) > 3 else 64
CHUNK, SEED = 64, 0
NLIB = min(256, N)
t_start = time.time()
specs, parts = AW.build(with_objects=False)
lev, cfg, pc = parts["level"], parts["cfg"], parts["phi_coarse"]
p0 = lev.params
xstar = AW.MapWorld(specs["coarse"], world_seed=0).designer.ensemble(1, seed=(301,)).carry.x[0]
sig = AW.OBS.quantum / math.sqrt(12.0)
Lx = vw.Level(init=lambda p, k: xstar, step=lev.step, input_dim=lev.input_dim, params=p0, conserved=dict(lev.conserved),
              name="FlowLenia from x*")
spec = vw.stride(vw.WorldSpec(base=Lx, chain=(pc,), inport=vw.InputPort(admissible=AW.INPUTS),
                              outport=vw.ObservePort(noise=sig), burn_in=0, name="A_gliders/coarse from x*"), AW.STRIDE)
wf = AW.MapWorld(spec, world_seed=0)
names = ["m_0", "R"]
theta0 = jnp.array([float(p0["m"][0]), float(p0["R"])])


def embed(theta):
    p = dict(p0)
    p["m"] = p0["m"].at[0].set(theta[0])
    p["R"] = theta[1]
    return p


ki_all = member_keys(make_key(_NS_CERT, wf.world_seed, 81, SEED), N)
kd_all = jax.vmap(lambda k: jax.random.fold_in(k, _ST_DYN))(ki_all)


def make_g(times):
    Hm, tsel = max(times), jnp.asarray(times)

    def g(theta, ki, kd):
        p = embed(theta)
        c = jax.vmap(wf._init_member, in_axes=(None, 0, 0))(p, ki, kd)
        A = jnp.zeros((Hm, ki.shape[0], wf.n_in))
        _, rec = wf._rollout_fn(p, c, A, ("obs_continuous",))
        o = rec["obs_continuous"][tsel]
        return jnp.swapaxes(o, 0, 1).reshape(ki.shape[0], -1)

    def f(theta, ki, kd):
        y = g(theta, ki, kd)
        return y, y
    return jax.jit(g), jax.jit(jax.jacfwd(f, has_aux=True))


def run_ad(gj, n):
    Ys, Js = [], []
    for s in range(0, n, CHUNK):
        J, Y = gj(theta0, ki_all[s:s + CHUNK], kd_all[s:s + CHUNK])
        Ys.append(np.asarray(Y))
        Js.append(np.asarray(J))
        if (s // CHUNK) % 8 == 7:
            print("members", s + CHUNK, round(time.time() - t_start, 1), "s", flush=True)
    return np.concatenate(Ys), np.concatenate(Js)


def bounds(Y, Jn, S=None):
    Nn, m = Y.shape
    ybar, Jbar = Y.mean(0), Jn.mean(0)
    if S is None:
        S = np.cov(Y.T, ddof=1)
    Si = np.linalg.inv(S)
    lin = Jbar.T @ Si @ Jbar
    Dj = Jn - Jbar
    noise_bias = np.einsum("nmi,mk,nkj->ij", Dj, Si, Dj) / (Nn - 1) / Nn
    wish = (Nn - m - 2) / (Nn - 1)
    dS = np.stack([(np.einsum("nm,nk->mk", Dj[..., i], Y - ybar) + np.einsum("nm,nk->mk", Y - ybar, Dj[..., i])) / (Nn - 1)
                   for i in range(Jn.shape[2])])
    A_ = np.einsum("mk,dkl->dml", Si, dS)
    cov = 0.5 * np.einsum("iml,jlm->ij", A_, A_)
    upper = np.einsum("nmi,nmj->ij", Jn, Jn) / Nn / sig ** 2
    return {"lower_raw": lin, "lower_debiased": wish * lin - noise_bias, "gaussian_raw": lin + cov,
            "covariance_term": cov, "upper_complete_data": upper, "Jbar": Jbar, "S": S,
            "jbar_snr": np.linalg.norm(Jbar, axis=0) / (np.sqrt((Dj ** 2).sum((0, 1)) / (Nn - 1)) / math.sqrt(Nn))}


# ---- main: one tick
g1, gj1 = make_g((1,))
Y, Jn = run_ad(gj1, N)
t_ad = time.time() - t_start
B = bounds(Y, Jn)
m = Y.shape[1]
out = {"theta_names": names, "theta": np.asarray(theta0), "horizon_ticks": 1, "substeps": AW.STRIDE, "N": N, "m": int(m),
       "sigma_o": sig, "ad_seconds": t_ad, "ad_ms_per_member": 1e3 * t_ad / N}
for k in ("lower_raw", "lower_debiased", "gaussian_raw", "covariance_term", "upper_complete_data", "jbar_snr"):
    out[k] = B[k]
for k in ("lower_debiased", "upper_complete_data"):
    try:
        out[f"crb_from_{k}"] = np.sqrt(np.diag(np.linalg.inv(B[k])))
    except np.linalg.LinAlgError:
        out[f"crb_from_{k}"] = None
out["upper_over_lower_debiased_diag"] = np.diag(B["upper_complete_data"]) / np.diag(B["lower_debiased"])
print(json.dumps(vw.jsonable({k: out[k] for k in ("lower_raw", "lower_debiased", "gaussian_raw", "upper_complete_data", "jbar_snr")}), indent=1), flush=True)

# ---- library cross-check (R only, first NLIB members, same keys)
t0 = time.time()
lib = vw.fisher(wf, wrt=["R"], times=(1,), n=NLIB, chunk=CHUNK, seed=SEED)
mine = bounds(Y[:NLIB], Jn[:NLIB, :, 1:2])
out["library_check"] = {"n": NLIB, "vw.fisher_linear_R": float(lib["linear"][0, 0]), "this_code_lower_raw_R": float(mine["lower_raw"][0, 0]),
                        "vw.fisher_gaussian_R": float(lib["gaussian"][0, 0]), "this_code_gaussian_raw_R": float(mine["gaussian_raw"][0, 0]),
                        "dmean_max_abs_diff": float(np.abs(lib["dmean"][:, 0] - mine["Jbar"][:, 0]).max()), "seconds": time.time() - t0}
print(json.dumps(out["library_check"]), flush=True)

# ---- finite differences, common random numbers
t0 = time.time()
fd = {}
ki, kd = ki_all[:NFD], kd_all[:NFD]
Jad = Jn[:NFD]
for hrel in (1e-6, 1e-8):
    Jfd = np.zeros_like(Jad)
    for i in range(2):
        h = hrel * abs(float(theta0[i]))
        e = jnp.zeros(2).at[i].set(h)
        yp = np.concatenate([np.asarray(g1(theta0 + e, ki[s:s + CHUNK], kd[s:s + CHUNK])) for s in range(0, NFD, CHUNK)])
        ym = np.concatenate([np.asarray(g1(theta0 - e, ki[s:s + CHUNK], kd[s:s + CHUNK])) for s in range(0, NFD, CHUNK)])
        Jfd[..., i] = (yp - ym) / (2 * h)
    rel = np.linalg.norm(Jfd - Jad, axis=1) / np.maximum(np.linalg.norm(Jad, axis=1), 1e-300)     # (NFD, 2)
    bfd, bad = bounds(Y[:NFD], Jfd, S=B["S"]), bounds(Y[:NFD], Jad, S=B["S"])
    fd[f"h_rel={hrel:g}"] = {"per_member_rel_err_median": np.median(rel, 0), "per_member_rel_err_p90": np.quantile(rel, 0.9, 0),
                             "per_member_rel_err_max": rel.max(0),
                             "Jbar_rel_err": np.linalg.norm(bfd["Jbar"] - bad["Jbar"], axis=0) / np.linalg.norm(bad["Jbar"], axis=0),
                             "lower_raw_fd": bfd["lower_raw"], "lower_raw_ad": bad["lower_raw"]}
    print(hrel, json.dumps(vw.jsonable(fd[f"h_rel={hrel:g}"])), flush=True)
out["finite_differences"] = {"NFD": NFD, "S_from": "all N members", **fd, "seconds": time.time() - t0}

# ---- growth of the pathwise derivative over a second tick
t0 = time.time()
_, gj2 = make_g((1, 2))
Y2, J2 = run_ad(gj2, NGROW)
n1 = Y2.shape[1] // 2
nrm1 = np.linalg.norm(J2[:, :n1], axis=1)                 # (NGROW, 2)
nrm2 = np.linalg.norm(J2[:, n1:], axis=1)
D2 = J2[:, n1:] - J2[:, n1:].mean(0)
out["two_ticks"] = {"NGROW": NGROW, "median_norm_dobs_dtheta_tick1": np.median(nrm1, 0), "median_norm_dobs_dtheta_tick2": np.median(nrm2, 0),
                    "median_growth_factor": np.median(nrm2 / nrm1, 0),
                    "jbar_snr_tick1": np.linalg.norm(J2[:, :n1].mean(0), axis=0) / (np.sqrt(((J2[:, :n1] - J2[:, :n1].mean(0)) ** 2).sum((0, 1)) / (NGROW - 1)) / math.sqrt(NGROW)),
                    "jbar_snr_tick2": np.linalg.norm(J2[:, n1:].mean(0), axis=0) / (np.sqrt((D2 ** 2).sum((0, 1)) / (NGROW - 1)) / math.sqrt(NGROW)),
                    "seconds": time.time() - t0}
print(json.dumps(vw.jsonable(out["two_ticks"])), flush=True)
out["total_seconds"] = time.time() - t_start
json.dump(vw.jsonable(out), open(f"{_paths.RESULTS}/fisher.json", "w"), indent=1)
