"""(c) autodiff input sensitivity: how strongly each of the 16384 input coordinates moves the coarse
level, by reverse-mode autodiff through the strided Flow-Lenia level and the differentiable
Phi_coarse (the VW-1 coarse world aworld.build()['coarse'], its pure tick MapWorld._tick).

usage: python -B sensitivity.py "S0,S1,.." -> results/sensitivity.json, results/sensitivity_maps.npz

Per state x0 (results/states.npz) and member key k (make_key(6161, s)):
  f_N(x) = Phi_coarse(tick^N(x)) with zero input, standardised by the coarse SD (results/vis_sd.npz);
  G_N = df_N/dx (n_eff x 2 x 128 x 128) from n_eff VJPs (one forward with residuals, lax.map over
  the cotangents), N = 1, 2, 4. The kick acts before the first substep, so per input coordinate i:
    deposit  u_i = +eps (designer probe, non-zero sum: eps/2 per channel)  dx = eps e_i (x) (1/2, 1/2)
    move     source i (-eps), sink r (+eps), r = the cell farthest from matter; zero sum, admissible;
             dx = eps (e_r - e_i) (x) c_i with c_i = A_i / A_sum,i (valid while eps <= A_sum,i)
  sensitivity s(i) = |G_N dx| / eps (norm over the standardised outputs); for admissible amplitude
  b = 0.5 the move is clipped to the matter present: s_eff(i) = min(b, A_sum,i) * s_move(i).
Validation: finite-difference pushes through the world's own input path (Designer.from_states with
the same key, all members in one call per tick; null member must equal the base exactly), at 50
deposit cells (25 in the matter footprint, 25 uniform) and 50 move sources (A_sum >= 0.01), eps in
EPS, against G_N dx (N = 1, 2, 4) and forward-mode JVPs (jax.jvp) at N = 8."""
import json
import sys
import time

import common as CM
import jax
import jax.numpy as jnp
import numpy as np
import scipy.ndimage as ndi

from vw.world import Carry, make_key, member_keys
import aworld as AW

STATES = [int(s) for s in (sys.argv[1] if len(sys.argv) > 1 else "0,1,2").split(",")]
import os
TEST = os.environ.get("SENS_TEST") == "1"
MAP_H = (1,) if TEST else (1, 2, 4)
VAL_H = (1, 2) if TEST else (1, 2, 4, 8)
EPS = (1e-5,) if TEST else (1e-3, 1e-5, 1e-7)
NCELL, BAMP = (4 if TEST else 50), 0.5
TAG = "_test" if TEST else ""
t_all = time.time()
wc, parts, _ = CM.build_world("coarse")
d = wc.designer
C = wc.inport.admissible
inv = AW.inverse_in_map(wc)
pc = parts["phi_coarse"]
params = wc.params
st = np.load(f"{CM.RES}/states.npz")
X = st["x"]
sdz = np.load(f"{CM.RES}/vis_sd.npz")
sd = sdz["sd"][:CM.NC]
eff = sdz["eff_coarse"]
ne = int(eff.sum())
cts = jnp.asarray(np.eye(CM.NC)[eff] / sd[eff][:, None])            # (ne, 192): standardised rows
z = jnp.zeros(wc.n_in)


def make_f(N, key):
    def f(x):
        c = Carry(x, ((),), jnp.zeros((), jnp.int64), key)
        for _ in range(N):
            c = wc._tick(params, c, z)
        return pc.phi(c.x, ())
    return f


vjp_map = jax.jit(lambda vf, cts: jax.lax.map(lambda c: vf(c)[0], cts))


def jvp_dirs(f, x, V):
    """forward-mode JVPs of f at x along each direction in V (no stored linearisation: O(1) memory in N)"""
    return jax.jit(lambda x, V: jax.lax.map(lambda v: jax.jvp(f, (x,), (v,))[1], V))(x, V)


def shares(v, foot, foot_dil):
    v = np.asarray(v, float).ravel()
    o = np.argsort(-v)
    out = {}
    for nm, w_ in (("s", v), ("s2", v ** 2)):
        cum = np.cumsum(w_[o]) / w_.sum()
        n90 = int(np.searchsorted(cum, 0.9) + 1)
        top = o[:n90]
        out[nm] = {"share_cells_for_90pct": n90 / v.size, "n_cells_for_90pct": n90,
                   "frac_of_those_in_footprint": float(foot[top].mean()),
                   "frac_of_those_within_4px_of_footprint": float(foot_dil[top].mean()),
                   "share_of_total_in_footprint": float(w_[foot].sum() / w_.sum())}
    return out


res = {"states": STATES, "map_horizons": MAP_H, "validation_horizons": VAL_H, "eps": EPS, "n_eff_outputs": ne,
       "amplitude_b": BAMP, "per_state": {}}
maps_out = {}
for s in STATES:
    t0 = time.time()
    x0 = jnp.asarray(X[s])
    A = X[s].reshape(2, -1)
    Sm = A.sum(0)
    foot = Sm > 1e-3
    foot_dil = ndi.binary_dilation(np.tile(foot.reshape(CM.H, CM.W), (3, 3)), iterations=4)[CM.H:2 * CM.H, CM.W:2 * CM.W].ravel()
    dist = ndi.distance_transform_edt(np.tile(~foot.reshape(CM.H, CM.W), (3, 3)))[CM.H:2 * CM.H, CM.W:2 * CM.W]
    r = int(np.argmax(dist.ravel()))
    cmp_ = A / Sm[None]                                               # (2, HW) composition
    key = member_keys(make_key(6161, s), 1)[0]
    rec = {"far_sink_cell": r, "far_sink_distance_px": float(dist.ravel()[r]),
           "footprint_frac_A_sum_gt_1e-3": float(foot.mean()), "footprint_frac_A_sum_gt_1e-2": float((Sm > 1e-2).mean())}
    G = {}
    for N in MAP_H:
        t1 = time.time()
        f = make_f(N, key)
        y, vf = jax.jit(lambda x: jax.vjp(f, x))(x0)
        G[N] = np.asarray(vjp_map(vf, cts)).reshape(ne, 2, CM.HW)
        del vf
        dep = np.linalg.norm(0.5 * (G[N][:, 0] + G[N][:, 1]), axis=0)          # (HW,)
        gi = (G[N] * cmp_[None]).sum(1)                                          # (ne, HW)
        gr = G[N][:, :, r] @ cmp_                                                # (ne, HW)
        mv = np.linalg.norm(gr - gi, axis=0)
        mv_eff = np.minimum(BAMP, Sm) * mv
        rec[f"N{N}"] = {"seconds": time.time() - t1,
                        "deposit": {"max": float(dep.max()), "median_all": float(np.median(dep)),
                                    "median_footprint": float(np.median(dep[foot])),
                                    "median_empty": float(np.median(dep[~foot])),
                                    "direct_block_mean_floor": float(np.linalg.norm(
                                        0.5 * (G[N][:, 0, r] + G[N][:, 1, r]))),
                                    "shares": shares(dep, foot, foot_dil),
                                    "shares_excess_over_direct_floor": shares(np.maximum(dep - np.linalg.norm(
                                        0.5 * (G[N][:, 0, r] + G[N][:, 1, r])), 0.0), foot, foot_dil),
                                    "top10_cells": [int(c) for c in np.argsort(-dep)[:10]],
                                    "top10_values": [float(v) for v in np.sort(dep)[::-1][:10]],
                                    "p99_9": float(np.percentile(dep, 99.9)), "p99": float(np.percentile(dep, 99))},
                        "move_eff_b0.5": {"max": float(mv_eff.max()), "median_footprint": float(np.median(mv_eff[foot])),
                                          "p99_9": float(np.percentile(mv_eff, 99.9)),
                                          "shares": shares(mv_eff, foot, foot_dil)},
                        "move_per_unit": {"median_footprint": float(np.median(mv[foot]))}}
        if N == 1:
            maps_out[f"s{s}_matter"] = Sm.astype(np.float32)
        maps_out[f"s{s}_dep_N{N}"] = dep.astype(np.float32)
        maps_out[f"s{s}_move_eff_N{N}"] = mv_eff.astype(np.float32)
        print(f"state {s} N={N}: VJPs {time.time() - t1:.0f}s dep max {dep.max():.3g} 90%-share "
              f"{rec[f'N{N}']['deposit']['shares']['s']['share_cells_for_90pct']:.3f}", flush=True)
    # oracle spread at this state (8 fresh-noise replicates), for linear responses in oracle units
    ens = d.from_states(jnp.asarray(np.repeat(X[s][None], 8, 0)), keys=member_keys(make_key(6162, s), 8))
    _, ro = d.rollout(ens, None, T=max(VAL_H), rec=("L1",))
    Zo = ro["L1"][..., eff] / sd[eff]
    Vu = Zo.var(0, ddof=1).mean(1)
    rec["oracle_Vu"] = {N: float(Vu[N]) for N in VAL_H}
    for N in MAP_H:
        dep = maps_out[f"s{s}_dep_N{N}"].astype(float)
        mve = maps_out[f"s{s}_move_eff_N{N}"].astype(float)
        rec[f"N{N}"]["linear_snr_deposit_b0.5_max_cell"] = float((BAMP * dep.max()) ** 2 / ne / Vu[N])
        rec[f"N{N}"]["linear_snr_deposit_b0.5_median_footprint_cell"] = float((BAMP * np.median(dep[foot])) ** 2 / ne / Vu[N])
        rec[f"N{N}"]["linear_snr_move_b0.5_max_cell"] = float(mve.max() ** 2 / ne / Vu[N])
    # finite-difference validation through the world's input path
    rng = np.random.default_rng([6163, s])
    ntop = max(1, NCELL // 5)
    dep1 = maps_out[f"s{s}_dep_N1"].astype(float)
    top_d = np.argsort(-dep1)[:ntop]
    pool_f = np.setdiff1d(np.flatnonzero(foot), top_d)
    pool_u = np.setdiff1d(np.arange(CM.HW), top_d)
    nf_ = (NCELL - ntop) // 2
    dep_cells = np.r_[top_d, rng.choice(pool_f, nf_, replace=False), rng.choice(pool_u, NCELL - ntop - nf_, replace=False)]
    dep_grp = ["top"] * ntop + ["footprint"] * nf_ + ["uniform"] * (NCELL - ntop - nf_)
    mve1 = maps_out[f"s{s}_move_eff_N1"].astype(float)
    okc = np.flatnonzero(Sm >= 0.01)
    top_m = okc[np.argsort(-mve1[okc])[:ntop]]
    src_cells = np.r_[top_m, rng.choice(np.setdiff1d(okc, top_m), NCELL - ntop, replace=False)]
    src_grp = ["top"] * ntop + ["random"] * (NCELL - ntop)
    dirs, labels, groups = [], [], []
    for i, g in zip(dep_cells, dep_grp):
        v = np.zeros((2, CM.HW))
        v[:, i] = 0.5
        dirs.append(v)
        labels.append(("deposit", int(i)))
        groups.append(g)
    for i, g in zip(src_cells, src_grp):
        v = np.zeros((2, CM.HW))
        v[:, r] += cmp_[:, i]
        v[:, i] -= cmp_[:, i]
        dirs.append(v)
        labels.append(("move", int(i)))
        groups.append(g)
    dirs = np.array(dirs)                                             # (100, 2, HW), per unit of eps
    groups = np.array(groups)
    nd = len(dirs)
    AMPS = tuple(EPS) + (BAMP,)                                       # last: the admissible amplitude 0.5
    B = 2 + nd * len(AMPS)
    P = np.zeros((B, 1, wc.n_in))
    adm_move = True
    for e_i, eps in enumerate(AMPS):
        for j, (kind, i) in enumerate(labels):
            b = 2 + e_i * nd + j
            if kind == "deposit":
                P[b, 0, inv[i]] = eps                                  # designer probe (not zero-sum)
            else:
                a = {int(inv[i]): -eps, int(inv[r]): eps}
                adm_move &= not C.violations(a)
                P[b, 0] = d.program_dense([(0, a)], 1, validate=True)[0]
    # matter actually moved by the amplitude-0.5 move (clipped to the source's matter)
    amp_scale = np.array([BAMP if k == "deposit" else min(BAMP, Sm[i]) for k, i in labels])
    t1 = time.time()
    ens = d.from_states(jnp.asarray(np.repeat(X[s][None], B, 0)), keys=member_keys(make_key(6161, s), 1)[jnp.zeros(B, int)])
    ens, r1 = d.rollout(ens, P, T=1, rec=("L1",))
    Ys = [r1["L1"][:, 0], r1["L1"][:, 1]]
    for t in range(2, max(VAL_H) + 1):
        ens = ens.step(None)
        Ys.append(ens.level(1))
    Y = np.stack(Ys, 1)                                               # (B, 9, 192)
    rec["fd_seconds"] = time.time() - t1
    rec["fd_null_check_max_abs"] = float(np.abs(Y[1] - Y[0]).max())
    rec["move_inputs_admissible"] = bool(adm_move)
    # AD predictions
    AD = {}
    for N in MAP_H:
        AD[N] = np.einsum("ock,dck->do", G[N], dirs)                    # (nd, ne)
        rec[f"N{N}"]["primal_vs_rollout_max_abs"] = float(np.abs(
            np.asarray(jax.jit(make_f(N, key))(x0)) - Y[0, N]).max())
    t1 = time.time()
    Vd = jnp.asarray(dirs.reshape(nd, 2, CM.H, CM.W))
    for N in VAL_H:
        if N not in AD:
            AD[N] = np.asarray(jvp_dirs(make_f(N, key), x0, Vd))[:, eff] / sd[eff]
    Nm = max(MAP_H)
    jm = np.asarray(jvp_dirs(make_f(Nm, key), x0, Vd[:4]))[:, eff] / sd[eff]
    rec[f"jvp_vs_vjp_N{Nm}_max_rel"] = float((np.linalg.norm(jm - AD[Nm][:4], axis=1) / np.linalg.norm(AD[Nm][:4], axis=1)).max())
    rec["jvp_seconds"] = time.time() - t1
    val, amp = {}, {}
    for N in VAL_H:
        for kind in ("deposit", "move"):
            sel = np.array([k == kind for k, _ in labels])
            for e_i, eps in enumerate(EPS):
                fd = (Y[2 + e_i * nd: 2 + (e_i + 1) * nd, N][:, eff] - Y[0, N][eff]) / sd[eff] / eps
                re = np.linalg.norm(fd[sel] - AD[N][sel], axis=1) / np.linalg.norm(AD[N][sel], axis=1)
                gq = groups[sel]
                val[f"N{N}_{kind}_eps{eps:g}"] = {"rel_err_median": float(np.median(re)),
                                                  "rel_err_p90": float(np.percentile(re, 90)),
                                                  "frac_rel_err_lt_0.01": float((re < 0.01).mean()),
                                                  "frac_rel_err_lt_0.1": float((re < 0.1).mean()),
                                                  "rel_err_median_by_group": {g: float(np.median(re[gq == g])) for g in np.unique(gq)}}
            rec.setdefault("ad_norm_median", {})[f"N{N}_{kind}"] = float(np.median(np.linalg.norm(AD[N][sel], axis=1)))
            # the admissible amplitude: actual response vs the linear (autodiff) prediction
            e_i = len(AMPS) - 1
            act = (Y[2 + e_i * nd: 2 + (e_i + 1) * nd, N][:, eff] - Y[0, N][eff]) / sd[eff]
            lin = AD[N] * amp_scale[:, None]
            na, nl = np.linalg.norm(act[sel], axis=1), np.linalg.norm(lin[sel], axis=1)
            gq = groups[sel]
            amp[f"N{N}_{kind}"] = {
                "actual_over_linear_norm_median": float(np.median(na / nl)),
                "rel_err_vs_linear_median": float(np.median(np.linalg.norm(act[sel] - lin[sel], axis=1) / nl)),
                "actual_snr_median": float(np.median(na ** 2 / ne / Vu[N])),
                "linear_snr_median": float(np.median(nl ** 2 / ne / Vu[N])),
                "by_group": {g: {"actual_snr_median": float(np.median(na[gq == g] ** 2 / ne / Vu[N])),
                                 "linear_snr_median": float(np.median(nl[gq == g] ** 2 / ne / Vu[N])),
                                 "actual_over_linear_norm_median": float(np.median(na[gq == g] / nl[gq == g]))}
                             for g in np.unique(gq)}}
    rec["validation"] = val
    rec["amplitude_0.5"] = amp
    rec["moved_by_amplitude_0.5_move_median"] = float(np.median(amp_scale[len(dep_cells):]))
    rec["seconds"] = time.time() - t0
    res["per_state"][s] = rec
    print(f"state {s} done {time.time() - t0:.0f}s; null {rec['fd_null_check_max_abs']:.3g}; " +
          " ".join(f"N{N}:{min(val[f'N{N}_deposit_eps{e:g}']['rel_err_median'] for e in EPS):.2g}/"
                   f"{min(val[f'N{N}_move_eps{e:g}']['rel_err_median'] for e in EPS):.2g}" for N in VAL_H), flush=True)
    json.dump(res, open(f"{CM.RES}/sensitivity{TAG}.json", "w"), indent=1)
    np.savez_compressed(f"{CM.RES}/sensitivity_maps{TAG}.npz", **maps_out)
res["seconds_total"] = time.time() - t_all
json.dump(res, open(f"{CM.RES}/sensitivity{TAG}.json", "w"), indent=1)
print("total", round(time.time() - t_all), "s", flush=True)
