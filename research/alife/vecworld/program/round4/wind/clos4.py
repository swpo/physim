"""clos4 -- closure ceilings of the full-size wind certification (one set and one view per process).

usage: python -B clos4.py F|M|F2|M2|P coarse|objects [--quick] [--nolc]
  F, M  (vw1/fresh/closure/scripts/run_closure.py on this study's data, horizons 1..32)
        1. copy check: unmodified analyze.closure (MLP off) == closure_lib.closure_ext (MLP off)
        2. closure_ext, VW-0 MLP on, plus the JAX rmlp and patchnet (coarse) / slotnet (objects);
           bootstrap SE over trajectories; the VW-0 set alone; selection check
        3. learning curve: the learned predictors refitted on 1/4, 1/2 and all fit trajectories per fold
        4. common scale: V_oracle and V_best in units of M's level-1 SD
        5. M only: every predictor scored against MW (M's test states, wind on, M's keys): the paired
           oracle cost of the wind and the ceiling of the wind-free predictors under wind
  P     the program mix (horizons 1..16): closure_ext with the VW-0 MLP plus blind rmlp, patchnet/slotnet,
        the '+u2' predictors, patchnet+u / slotnet+u (p4lib); exam effect, twin (true) effect, the share
        of the true effect a learned level-1 predictor recovers, energy scores of ensemble forecasts
  F2, M2  the second F/M pair (FM2.npz), same analysis (--nolc skips the learning curve)
  --quick  code-path test: few epochs, one seed
-> $W4_WORK/closure_<S>_<view>.json, closure_<S>_<view>_items.npz (with predictions);
   $W4_OUT/closure_<S>_<view>.json (same JSON), $W4_OUT/items/closure_<S>_<view>_items.npz (errors only)
"""
import json
import math
import os
import sys
import time

import numpy as np

import w4

CL = w4.setup_paths(closure=True)     # closure_lib (integrate/analyze) before actuation/ joins the path
import wr  # noqa: E402
import feats as FT  # noqa: E402
import p4lib  # noqa: E402

p4lib.setup(CL, FT, wr)
AN = CL.AN
SET, VIEW = sys.argv[1], sys.argv[2]
QUICK = "--quick" in sys.argv
K = 12 if VIEW == "objects" else None
NC = wr.WD.NC
WORK, OUT = w4.work_dir(), w4.out_dir()
os.makedirs(f"{OUT}/items", exist_ok=True)
T0 = time.time()
TAG = f"{SET}_{VIEW}"


def log(*a):
    msg = " ".join(str(x) for x in a)
    print(f"[{time.time() - T0:8.1f}s] {msg}", flush=True)
    if any(k in msg for k in ("ceiling", "saved", "FAILED", "fold 3 done", "LC best")):
        w4.progress(f"[clos4 {TAG} {time.time() - T0:7.1f}s] {msg[:300]}")


RK = dict(epochs=4, seeds=(0,)) if QUICK else dict(epochs=300, seeds=(0, 1))


def make_D(Y, B, test):
    J = len(Y)
    return {"Yc": [Y[j][:, :NC].astype(float) for j in range(J)], "Yo": [Y[j][:, NC:].astype(float) for j in range(J)],
            "Bc": [B[j][..., :NC].astype(float) for j in range(J)], "Bo": [B[j][..., NC:].astype(float) for j in range(J)],
            "st_tick": [np.array(test) for _ in range(J)], "j": list(range(J))}


def load():
    if SET[0] in ("F", "M"):
        tag = "FM" + SET[1:]
        meta = json.load(open(f"{WORK}/{tag}.json"))
        z = np.load(f"{WORK}/{tag}.npz")
        J = meta["J"]
        rows = slice(0, J) if SET[0] == "F" else slice(J, 2 * J)
        D = make_D(z["Y"][rows], z["B"][rows], meta["test_ticks"])
        return D, meta, z
    meta = json.load(open(f"{WORK}/P.json"))
    z = np.load(f"{WORK}/P.npz")
    D = make_D(z["Y"], z["B"], meta["test_ticks"])
    return D, meta, z


def sd_ref(view, z, meta):
    """M's level-1 SD (the common scale), from the FM file (or this set's own data when absent)."""
    if os.path.exists(f"{WORK}/FM.npz"):
        zz = z if SET in ("F", "M") else np.load(f"{WORK}/FM.npz")
        J = (meta if SET in ("F", "M") else json.load(open(f"{WORK}/FM.json")))["J"]       # M of the first pair
        Y = zz["Y"][J:2 * J]
    else:
        Y = z["Y"]
    sl = slice(0, NC) if view == "coarse" else slice(NC, None)
    s = Y[..., sl].reshape(-1, Y[..., sl].shape[-1]).astype(float).std(0)
    eff = s > 1e-6 * max(s.max(), 1e-12)
    return np.where(eff, s, 1.0), eff


def common_scale(det, out, z, meta):
    eff, sd = det["eff"], det["sd"]
    sdc, effc = sd_ref(VIEW, z, meta)
    rescale = (sd[eff] / sdc[eff]) ** 2
    FUT = det["FUT"]
    nH = FUT.shape[2]
    orac_c = ((FUT - FUT.mean(1, keepdims=True)) ** 2 * rescale).sum((1, 3)) / (FUT.shape[1] - 1) / eff.sum()
    bn = out["best_name"]
    vb_items = np.stack([(((FUT[:, :, hi] - det["preds"][bn[hi]][:, None, hi]) ** 2 * rescale).sum(-1).mean(1)
                          / eff.sum()) for hi in range(nH)], 1)
    v0_items = np.stack([(((FUT[:, :, hi] - det["preds"]["mean"][:, None, hi]) ** 2 * rescale).sum(-1).mean(1)
                          / eff.sum()) for hi in range(nH)], 1)
    out["common_scale"] = {"note": "errors in units of M's level-1 SD (the wind-free set of this job)",
                           "V_oracle": orac_c.mean(0), "V_oracle_se": orac_c.std(0, ddof=1) / math.sqrt(len(orac_c)),
                           "V_best": vb_items.mean(0), "V0": v0_items.mean(0)}
    return orac_c, vb_items, v0_items


def copy_check(D):
    ref = AN.closure(D, VIEW, K=K, mlp=False)[0]
    chk, _ = CL.closure_ext(D, VIEW, K=K, mlp=False)
    common = [nm for nm in chk["V"] if nm in ref["V"]]
    diff = max(float(np.abs(np.asarray(ref["V"][nm]) - np.asarray(chk["V"][nm])).max()) for nm in common)
    diff = max(diff, float(np.abs(np.asarray(ref["V_oracle"]) - np.asarray(chk["V_oracle"])).max()))
    log("copy check: max |V_analyze - V_copy| =", diff)
    assert diff == 0.0, diff
    return diff


def best_of(err, names, idx):
    V = np.stack([err[nm][idx].mean(0) for nm in names])
    return V.min(0), [names[k] for k in V.argmin(0)]


def selection_and_vw0(out, det, nH):
    err, orac, item_j = det["err"], det["orac"], det["item_j"]
    names = list(err)
    V0, Vu = np.asarray(out["V0_mean_predictor"]), np.asarray(out["V_oracle"])
    NEW = ("rmlp", "slotnet", "patchnet")
    old_set = [nm for nm in names if nm not in NEW]
    b_old, n_old = best_of(err, old_set, np.arange(len(item_j)))
    rng = np.random.default_rng(0)
    uj = np.unique(item_j)
    bs_old = []
    for b in range(400):
        pick = rng.choice(uj, uj.size, replace=True)
        idx = np.concatenate([np.flatnonzero(item_j == q) for q in pick])
        bb, _ = best_of(err, old_set, idx)
        bs_old.append((err["mean"][idx].mean(0) - bb) / (err["mean"][idx].mean(0) - orac[idx].mean(0)))
    out["vw0_set_only"] = {"best_level1": b_old, "best_name": n_old, "ceiling": (V0 - b_old) / (V0 - Vu),
                           "ceiling_se": np.std(bs_old, 0)}
    rng = np.random.default_rng(1)
    sel_c = []
    for s in range(200):
        half = rng.permutation(uj)[: uj.size // 2]
        A = np.isin(item_j, half)
        cs = []
        for (tr_m, te_m) in ((A, ~A), (~A, A)):
            _, nm_h = best_of(err, names, np.flatnonzero(tr_m))
            e = np.array([err[nm_h[hi]][te_m, hi].mean() for hi in range(nH)])
            v0, vu = err["mean"][te_m].mean(0), orac[te_m].mean(0)
            cs.append((v0 - e) / (v0 - vu))
        sel_c.append(np.mean(cs, 0))
    sel_c = np.array(sel_c)
    out["selection_check"] = {"ceiling_mean": sel_c.mean(0), "ceiling_sd_over_splits": sel_c.std(0),
                              "note": "best predictor per horizon chosen on half the trajectories, ceiling on the "
                                      "other half; 200 random splits"}
    log("selection-checked ceiling", np.round(sel_c.mean(0), 4).tolist())


def learning_curve(D, out, det, nH):
    """run_closure.py section 3 (unchanged logic)."""
    J = len(D["Yc"])
    Ys, FUT, items, item_j = det["Ys"], det["FUT"], det["items"], det["item_j"]
    err, orac = det["err"], det["orac"]
    V0, Vu = np.asarray(out["V0_mean_predictor"]), np.asarray(out["V_oracle"])
    tmax = max(AN.HORIZONS)
    fold_of = {jj: D["j"][jj] % AN.NFOLD for jj in range(J)}
    lc_names = sorted(set(out["best_name"]) | {"ar1", "ridge_p2"})
    lc_names = [nm for nm in lc_names if nm not in ("mean", "persistence", "knn", "kinematic")]
    log("learning curve for", lc_names)
    fracs = (0.25, 0.5, 1.0)
    LC = {fr: {nm: np.zeros((len(items), nH, FUT.shape[3])) for nm in lc_names} for fr in fracs}
    n_fit_traj = {fr: [] for fr in fracs}
    eff, sd = det["eff"], det["sd"]
    for fr in fracs:
        for f in range(AN.NFOLD):
            tr_j = [jj for jj in range(J) if fold_of[jj] != f]
            va_j = [jj for jj in tr_j if fold_of[jj] == (f + 1) % AN.NFOLD]
            fit_all = [jj for jj in tr_j if jj not in va_j]
            fit_j = fit_all[:max(1, int(round(fr * len(fit_all))))]
            n_fit_traj[fr].append(len(fit_j))
            te = [n for n, it in enumerate(items) if fold_of[it[0]] == f]
            te_items = [tuple(items[n]) for n in te]
            mu = np.concatenate([Ys[jj] for jj in fit_j]).mean(0)
            if "ar1" in lc_names:
                X1, F1, _ = AN.multi_pairs([Ys[jj] for jj in fit_j], 1, tmax)
                for hi in range(nH):
                    a, b = X1 - mu, F1[hi] - mu
                    rho = (a * b).sum(0) / np.maximum((a * a).sum(0), 1e-12)
                    for n in te:
                        jj, i, t = items[n]
                        LC[fr]["ar1"][n, hi] = mu + rho * (Ys[jj][t] - mu)
            for p in AN.PASTS:
                nm = f"ridge_p{p}"
                if nm not in lc_names:
                    continue
                Xf, Ff, Y0f = AN.multi_pairs([Ys[jj] for jj in fit_j], p, tmax)
                Xv, Fv, Y0v = AN.multi_pairs([Ys[jj] for jj in va_j], p, tmax)
                rg = AN.Ridge().fit(Xf, [Ff[hi] - Y0f for hi in range(nH)], Xv, [Fv[hi] - Y0v for hi in range(nH)])
                for n in te:
                    jj, i, t = items[n]
                    x = AN.lag_matrix(Ys[jj], np.array([t]), p)
                    for hi in range(nH):
                        LC[fr][nm][n, hi] = Ys[jj][t] + rg.predict(x, hi)[0]
            if "mlp" in lc_names:
                def mk(js):
                    X, T = [], []
                    for jj in js:
                        Y = Ys[jj]
                        ts = np.arange(1, len(Y) - tmax)
                        X.append(AN.lag_matrix(Y, ts, 2))
                        T.append(np.concatenate([Y[ts + h] - Y[ts] for h in AN.HORIZONS], 1))
                    return np.concatenate(X), np.concatenate(T)
                Xf, Tf = mk(fit_j)
                Xv, Tv = mk(va_j)
                net = AN.MLP(seed=f).fit(Xf, Tf, Xv, Tv)
                for n in te:
                    jj, i, t = items[n]
                    LC[fr]["mlp"][n] = Ys[jj][t] + net.predict(AN.lag_matrix(Ys[jj], np.array([t]), 2))[0].reshape(nH, -1)
            if "kin+ridge_p4" in lc_names:
                sdq, full_idx = sd[eff], np.flatnonzero(eff)

                def kin_std(Ystd_rows, h):
                    Yr = np.zeros((len(Ystd_rows), len(sd)))
                    Yr[:, full_idx] = Ystd_rows * sdq
                    return AN.kinematic(Yr, h, K)[:, full_idx] / sdq
                Xf, Ff, Y0f = AN.multi_pairs([Ys[jj] for jj in fit_j], 4, tmax)
                Xv, Fv, Y0v = AN.multi_pairs([Ys[jj] for jj in va_j], 4, tmax)
                rg = AN.Ridge().fit(Xf, [Ff[hi] - kin_std(Y0f, h) for hi, h in enumerate(AN.HORIZONS)],
                                    Xv, [Fv[hi] - kin_std(Y0v, h) for hi, h in enumerate(AN.HORIZONS)])
                for n in te:
                    jj, i, t = items[n]
                    x = AN.lag_matrix(Ys[jj], np.array([t]), 4)
                    for hi, h in enumerate(AN.HORIZONS):
                        LC[fr]["kin+ridge_p4"][n, hi] = kin_std(Ys[jj][t][None], h)[0] + rg.predict(x, hi)[0]
            if "rmlp" in lc_names:
                LC[fr]["rmlp"][te] = CL.make_rmlp_extra(frac=1.0, **RK)(f, Ys, tr_j, fit_j, va_j, te_items)["rmlp"]
            if "slotnet" in lc_names:
                LC[fr]["slotnet"][te] = CL.make_slot_extra(D, frac=1.0, **RK)(f, Ys, tr_j, fit_j, va_j, te_items)["slotnet"]
            if "patchnet" in lc_names:
                LC[fr]["patchnet"][te] = CL.make_patch_extra(D, frac=1.0, **RK)(f, Ys, tr_j, fit_j, va_j, te_items)["patchnet"]
            log(f"  LC frac {fr} fold {f}: {len(fit_j)} fit trajectories")
    neff = FUT.shape[3]
    LCerr = {fr: {nm: ((FUT - P[:, None]) ** 2).sum(3).mean(1) / neff for nm, P in LC[fr].items()} for fr in fracs}
    lc = {"fit_trajectories_per_fold": {str(fr): n_fit_traj[fr] for fr in fracs}, "names": lc_names,
          "note": "all fits on the fit trajectories of each fold only (training minus validation); the main closure "
                  "refits ridge and AR(1) on all training trajectories (fit + validation)", "V": {}, "best": {}, "ceiling": {}}
    for fr in fracs:
        lc["V"][str(fr)] = {nm: e.mean(0) for nm, e in LCerr[fr].items()}
        Vb = np.min(np.stack([e.mean(0) for e in LCerr[fr].values()]), 0)
        lc["best"][str(fr)] = Vb
        lc["ceiling"][str(fr)] = (V0 - Vb) / (V0 - Vu)
    rng = np.random.default_rng(2)
    uj = np.unique(item_j)
    dd = []
    for b in range(400):
        pick = rng.choice(uj, uj.size, replace=True)
        idx = np.concatenate([np.flatnonzero(item_j == q) for q in pick])
        vh = np.min(np.stack([e[idx].mean(0) for e in LCerr[0.5].values()]), 0)
        va = np.min(np.stack([e[idx].mean(0) for e in LCerr[1.0].values()]), 0)
        dd.append(vh - va)
    dd = np.array(dd)
    dV = np.asarray(lc["best"]["0.5"]) - np.asarray(lc["best"]["1.0"])
    lc["dV_half_minus_all"] = dV
    lc["dV_half_minus_all_se"] = dd.std(0)
    lc["rel_drop_half_to_all"] = dV / np.asarray(lc["best"]["0.5"])
    lc["rel_drop_quarter_to_half"] = (np.asarray(lc["best"]["0.25"]) - np.asarray(lc["best"]["0.5"])) / np.asarray(lc["best"]["0.25"])
    lc["saturated"] = [bool(abs(d) < 2 * s or abs(r) < 0.02) for d, s, r in zip(dV, dd.std(0), lc["rel_drop_half_to_all"])]
    lc["saturation_rule"] = "saturated if V(1/2) - V(all) < 2 SE (bootstrap over trajectories) or the relative drop < 2%"
    out["learning_curve"] = lc
    log("LC best", {k: np.round(v, 4).tolist() for k, v in lc["best"].items()})
    return LCerr


def mw_scoring(out, det, z, meta):
    """M only: every M predictor against MW futures (M's test states, wind on, M's keys)."""
    eff, sd = det["eff"], det["sd"]
    sl = slice(0, NC) if VIEW == "coarse" else slice(NC, None)
    MW = z["MW"][..., sl]                                                      # (J, nT, 6, TB, n)
    items = det["items"]
    HZ = AN.HORIZONS
    FW = np.stack([np.stack([MW[jj, i][:, h - 1] for h in HZ], 1) for jj, i, t in items])     # (n, 6, nH, n1)
    FW = FW[..., eff].astype(float) / sd[eff]
    neff = int(eff.sum())
    errW = {nm: ((FW - P[:, None]) ** 2).sum(3).mean(1) / neff for nm, P in det["preds"].items()}
    oracW = ((FW - FW.mean(1, keepdims=True)) ** 2).sum((1, 3)) / (FW.shape[1] - 1) / neff
    V = {nm: e.mean(0) for nm, e in errW.items()}
    best = np.min(np.stack(list(V.values())), 0)
    V0, Vu = V["mean"], oracW.mean(0)
    orac = det["orac"]
    dV = oracW - orac                                                          # paired per item
    item_j = det["item_j"]
    uj = np.unique(item_j)
    rng = np.random.default_rng(3)
    bs = []
    for b in range(400):
        pick = rng.choice(uj, uj.size, replace=True)
        idx = np.concatenate([np.flatnonzero(item_j == q) for q in pick])
        bs.append(dV[idx].mean(0))
    Vb_M = np.asarray(out["best_level1"])
    out["MW"] = {"note": "M's test states branched with wind (sigma_w = 0.05), 6 replicates on M's keys; predictors "
                         "fitted on M (wind-free) scored against the wind futures",
                 "V_oracle": Vu, "V0": V0, "V_best": best, "best_name": [min(V, key=lambda nm: V[nm][hi]) for hi in range(len(HZ))],
                 "ceiling_wind_free_predictors": (V0 - best) / (V0 - Vu),
                 "oracle_cost_dV": dV.mean(0), "oracle_cost_dV_se_traj_boot": np.std(bs, 0),
                 "oracle_cost_dV_over_Vbest_M": dV.mean(0) / Vb_M,
                 "oracle_cost_dV_over_Vbest_M_se": np.std(bs, 0) / Vb_M,
                 "oracle_cost_dV_median_item": np.median(dV, 0),
                 "best_M_predictor_error_increase": np.array([errW[out["best_name"][hi]][:, hi].mean() - det["err"][out["best_name"][hi]][:, hi].mean()
                                                              for hi in range(len(HZ))])}
    log("MW oracle cost dV/Vbest", np.round(out["MW"]["oracle_cost_dV_over_Vbest_M"], 4).tolist(),
        "+-", np.round(out["MW"]["oracle_cost_dV_over_Vbest_M_se"], 4).tolist())
    return errW, oracW


# ----------------------------------------------------------------------------- F / M
def main_fm():
    AN.HORIZONS = list(w4.HZ_FM)
    D, meta, z = load()
    J = len(D["Yc"])
    nH = len(AN.HORIZONS)
    log(SET, VIEW, "J", J, "T", len(D["Yc"][0]) - 1, "test", D["st_tick"][0].tolist(), "quick", QUICK)
    diff = copy_check(D)
    rinfo, sinfo = [], []
    hook = CL.make_rmlp_extra(log=log, info_store=rinfo, **RK)
    hook = CL.combine(hook, CL.make_slot_extra(D, log=log, info_store=sinfo, **RK) if VIEW == "objects"
                      else CL.make_patch_extra(D, log=log, info_store=sinfo, **RK))
    out, det = CL.closure_ext(D, VIEW, K=K, mlp=True, extra=hook, log=log)
    log("ceiling", np.round(out["ceiling"], 4).tolist(), "+-", np.round(out["ceiling_se"], 4).tolist())
    log("best", out["best_name"], "Vbest", np.round(out["best_level1"], 4).tolist(),
        "Voracle", np.round(out["V_oracle"], 4).tolist())
    out["copy_check_max_abs_diff"] = diff
    selection_and_vw0(out, det, nH)
    orac_c, vb_c, v0_c = common_scale(det, out, z, meta)
    sv_extra = {}
    if SET[0] == "M" and "MW" in z.files:
        errW, oracW = mw_scoring(out, det, z, meta)
        sv_extra = {"errW": np.stack([errW[nm] for nm in errW]).astype(np.float32), "oracW": oracW.astype(np.float32)}
    out["rmlp_info"] = rinfo
    out["net_info"] = sinfo
    _save_partial(out, det, orac_c, vb_c, v0_c, sv_extra, meta, J)        # main results first (LC can fail)
    if "--nolc" in sys.argv:
        return
    LCerr = learning_curve(D, out, det, nH)
    sv_extra.update({f"lc_err_{fr}": np.stack([LCerr[fr][nm] for nm in LCerr[fr]]).astype(np.float32) for fr in LCerr})
    sv_extra["lc_names"] = np.array(list(LCerr[1.0]))
    _save_partial(out, det, orac_c, vb_c, v0_c, sv_extra, meta, J)


def _save_partial(out, det, orac_c, vb_c, v0_c, sv_extra, meta, J):
    names = list(det["err"])
    out["data"] = {"set": SET, "J": J, "T": len(det["Ys"][0]) - 1, "test_ticks": meta["test_ticks"],
                   "replicates": int(det["FUT"].shape[1]), "platform": meta["platform"], "quick": QUICK,
                   "seed": meta["seed"]}
    out["seconds"] = time.time() - T0
    js = CL.jsonable(out)
    for d in (WORK, OUT):
        json.dump(js, open(f"{d}/closure_{TAG}.json", "w"), indent=1)
    base = {"err": np.stack([det["err"][nm] for nm in names]).astype(np.float32), "names": np.array(names),
            "orac": det["orac"].astype(np.float32), "items": det["items"], "item_j": det["item_j"],
            "eff": det["eff"], "sd": det["sd"], "orac_common": orac_c.astype(np.float32),
            "vbest_common": vb_c.astype(np.float32), "v0_common": v0_c.astype(np.float32)}
    base.update(sv_extra)
    np.savez_compressed(f"{OUT}/items/closure_{TAG}_items.npz", **base)
    np.savez(f"{WORK}/closure_{TAG}_items.npz", preds=np.stack([det["preds"][nm] for nm in names]).astype(np.float32),
             FUT=det["FUT"].astype(np.float32), **base)
    log("saved", f"{OUT}/closure_{TAG}.json")


# ----------------------------------------------------------------------------- P
def main_p():
    AN.HORIZONS = list(w4.HZ_P)
    HZ = AN.HORIZONS
    nH = len(HZ)
    D, meta, z = load()
    J = len(D["Yc"])
    log(SET, VIEW, "J", J, "T", len(D["Yc"][0]) - 1, "test", D["st_tick"][0].tolist(), "quick", QUICK)
    diff = copy_check(D)
    U = [z["U"][j].astype(float) for j in range(J)]
    raw = D["Yo"] if VIEW == "objects" else D["Yc"]
    sd_all = np.concatenate(raw).std(0)
    eff = sd_all > 1e-6 * max(sd_all.max(), 1e-12)
    L = p4lib.Local(VIEW, raw, U, eff, HZ)
    ainfo, rinfo, sinfo, uinfo = [], [], [], []
    hooks = [p4lib.local_hook(VIEW, D, L, K=K, info=ainfo, log=log), CL.make_rmlp_extra(log=log, info_store=rinfo, **RK)]
    if VIEW == "objects":
        hooks += [CL.make_slot_extra(D, log=log, info_store=sinfo, **RK),
                  p4lib.make_slot_aware_extra(D, L, log=log, info_store=uinfo, **RK)]
    else:
        hooks += [CL.make_patch_extra(D, log=log, info_store=sinfo, **RK),
                  p4lib.make_patch_aware_extra(D, L, log=log, info_store=uinfo, **RK)]
    out, det = CL.closure_ext(D, VIEW, K=K, mlp=True, extra=CL.combine(*hooks), log=log)
    aware = [nm for nm in det["err"] if nm.endswith("+u2") or nm.endswith("+u") or nm == "aware_base"]
    out["ar1_rep_check_max_abs_V_diff"] = float(np.abs(det["err"]["ar1_rep"] - det["err"]["ar1"]).max())
    log("ar1 refit check (max |err diff|)", out["ar1_rep_check_max_abs_V_diff"])
    for dct in (det["err"], det["preds"], out["V"]):
        dct.pop("ar1_rep")
    # the best-of over all predictors (the closure ceiling) recomputed after dropping the check copy
    log("ceiling", np.round(out["ceiling"], 4).tolist(), "+-", np.round(out["ceiling_se"], 4).tolist())
    log("best", out["best_name"])
    out["copy_check_max_abs_diff"] = diff
    orac_c, vb_c, v0_c = common_scale(det, out, z, meta)
    items_meta = {(it["j"], it["test_index"]): it for it in meta["items"]}
    klass = np.array([items_meta[(int(jj), int(i))]["klass"] for jj, i, t in det["items"]])
    Cn = np.array([items_meta[(int(jj), int(i))]["charged_nats"] for jj, i, t in det["items"]])
    out["aware_names"] = aware
    out["aware_info"] = ainfo
    out["net_info"] = {"rmlp": rinfo, "blind_net": sinfo, "aware_net": uinfo}
    ee = p4lib.exam_effect(det, klass, aware, nH)
    out["exam_effect"] = ee
    sl = slice(NC, None) if VIEW == "objects" else slice(0, NC)
    Bn = np.stack([z["Bnone"][jj, i] for jj, i, t in det["items"]])[..., sl]
    Bn_std = np.stack([Bn[:, :, h - 1] for h in HZ], 2)[..., det["eff"]].astype(float) / det["sd"][det["eff"]]
    Vbest = ee["V_best_all"]
    tw, crn, unp = p4lib.twin_effect(det, Bn_std, klass, Vbest)
    out["twin_effect"] = tw
    out["items_meta"] = {"klass_counts": {k: int((klass == k).sum()) for k in wr.CLASSES},
                         "charged_nats_by_class": {k: [float(Cn[klass == k].min()), float(Cn[klass == k].mean()),
                                                       float(Cn[klass == k].max())] for k in wr.CLASSES if (klass == k).any()}}
    # ---- the share of the true effect recovered (squared error): achieved loss / ideal loss
    err = det["err"]
    item_j = det["item_j"]
    uj = np.unique(item_j)
    pairs = {"best_blind -> best_all": (ee["best_blind"], ee["best_all"])}
    net, netu = ("slotnet", "slotnet+u") if VIEW == "objects" else ("patchnet", "patchnet+u")
    pairs[f"{net} -> {netu}"] = ([net] * nH, [netu] * nH)
    pairs["ridge_p2 -> ridge_p2+u2"] = (["ridge_p2"] * nH, ["ridge_p2+u2"] * nH)
    pairs[f"{net} -> aware_base"] = ([net] * nH, ["aware_base"] * nH)
    rec = {}
    masks = {"all": np.ones(len(klass), bool), "programs": klass != "none",
             "aimed_regional": (klass == "aimed") | (klass == "regional")}
    for pn, (a, b) in pairs.items():
        d = np.stack([err[a[hi]][:, hi] - err[b[hi]][:, hi] for hi in range(nH)], 1)
        rec[pn] = {}
        for mk_, sel in masks.items():
            num, den = d[sel].mean(0), crn[sel].mean(0)
            rng = np.random.default_rng(5)
            bs = []
            for b_ in range(400):
                pick = rng.choice(uj, uj.size, replace=True)
                idx = np.concatenate([np.flatnonzero((item_j == q) & sel) for q in pick])
                bs.append(d[idx].mean(0) / crn[idx].mean(0))
            rec[pn][mk_] = {"achieved_loss_over_Vbest": num / Vbest, "ideal_loss_over_Vbest": den / Vbest,
                            "share_recovered": num / den, "share_recovered_se_traj_boot": np.std(bs, 0)}
    out["recovered"] = rec
    for pn in rec:
        log(f"  recovered share {pn:28s}", np.round(rec[pn]["all"]["share_recovered"], 3).tolist())
    # ---- energy scores of ensemble forecasts
    t1 = time.time()
    fold_of_item = det["item_j"] % AN.NFOLD
    S, draws = p4lib.es_all(det, fold_of_item, m=32, seed=0)
    names = [nm for nm in det["preds"]]
    blind = [nm for nm in names if nm not in aware]
    ESm = {nm: S[nm].mean((0, 1)) for nm in names}
    S_or = S["oracle_loo"]
    clim = ESm["mean"]
    best_es_all = [min(names, key=lambda nm: ESm[nm][hi]) for hi in range(nH)]
    best_es_blind = [min(blind, key=lambda nm: ESm[nm][hi]) for hi in range(nH)]
    pick = lambda nms: np.stack([S[nms[hi]][:, :, hi] for hi in range(nH)], 2)
    es = {"note": "fair energy score (RMS norm, standardised level-1 coordinates) of residual-pool ensembles "
                  "(m = 32 out-of-fold residual vectors, same draws for every predictor), mean over the 6 replicate "
                  "truths; OES = (S_clim - S) / (S_clim - S_oracle) with S_clim the 'mean' predictor's ensemble and "
                  "S_oracle the leave-one-out score of the replicate truths",
          "mean_score": ESm, "oracle_loo": S_or.mean((0, 1)),
          "oes": {nm: (clim - ESm[nm]) / (clim - S_or.mean((0, 1))) for nm in names},
          "best_by_es_all": best_es_all, "best_by_es_blind": best_es_blind,
          "pairs": {}, "ideal": {}}
    Sref = clim - S_or.mean((0, 1))
    cmp = {"best_blind_se -> best_all_se (chosen by squared error)": (pick(ee["best_blind"]), pick(ee["best_all"])),
           "best_blind_es -> best_all_es (chosen by ES)": (pick(best_es_blind), pick(best_es_all)),
           f"{net} -> {netu}": (S[net], S[netu]), "ridge_p2 -> ridge_p2+u2": (S["ridge_p2"], S["ridge_p2+u2"])}
    for pn, (Sa, Sb) in cmp.items():
        es["pairs"][pn] = {mk_: p4lib.es_pair(Sa, Sb, sel, Vref=Sref) for mk_, sel in masks.items()}
    idl = p4lib.ideal_es(det["FUT"], Bn_std, klass)
    for mk_, sel in masks.items():
        es["ideal"][mk_] = p4lib.es_pair(idl, np.zeros_like(idl), sel, Vref=Sref)
    # recovered share in ES: achieved (best blind -> best aware by ES) / ideal ES contrast
    for pn in ("best_blind_es -> best_all_es (chosen by ES)", f"{net} -> {netu}"):
        es["pairs"][pn]["share_of_ideal_all"] = (np.asarray(es["pairs"][pn]["all"]["loss_mean"]) /
                                                 np.asarray(es["ideal"]["all"]["loss_mean"]))
    es["seconds"] = time.time() - t1
    out["energy_score"] = es
    log("ES oes best aware", np.round([es["oes"][best_es_all[hi]][hi] for hi in range(nH)], 3).tolist(),
        "ES loss blind->aware (all)", np.round(es["pairs"]["best_blind_es -> best_all_es (chosen by ES)"]["all"]["loss_mean"], 5).tolist(),
        "z64 R1", np.round(es["pairs"]["best_blind_es -> best_all_es (chosen by ES)"]["all"]["z_n64_R1"], 2).tolist())
    for kl in ("all", "programs_only") + wr.CLASSES:
        log(f"  loss/Vbest {kl:9s}", np.round(ee["best_vs_best"][kl]["loss_over_Vbest"], 3).tolist(),
            "z64 R1", np.round(ee["best_vs_best"][kl]["z_n64_R1"], 1).tolist())
    sv = {"klass": klass, "nats": Cn, "crn": crn.astype(np.float32), "unp": unp.astype(np.float32),
          "es_names": np.array(names), "es": np.stack([S[nm] for nm in names]).astype(np.float32),
          "es_oracle": S_or.astype(np.float32), "es_ideal": idl.astype(np.float32)}
    _save_partial(out, det, orac_c, vb_c, v0_c, sv, meta, J)


if __name__ == "__main__":
    try:
        (main_p if SET == "P" else main_fm)()
    except Exception:
        import traceback
        tb = traceback.format_exc()
        print(tb, flush=True)
        log(f"FAILED {TAG}: {tb[-400:]}")
        sys.exit(1)
