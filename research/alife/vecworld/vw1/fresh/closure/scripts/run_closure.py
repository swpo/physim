"""Closure ceilings for one view from the fresh VW-1 data.

usage: python -B run_closure.py coarse|objects [--quick]
  -> results/closure_<phi>.json, results/closure_<phi>_items.npz

1. analyze.closure (VW-0 code, unchanged, MLP off) and closure_ext (copy, MLP off, no extra)
   must agree exactly: checks the copy.
2. closure_ext with the VW-0 MLP on and the JAX residual MLP ('rmlp') in the best-of set;
   bootstrap SE over trajectories (400, as analyze); selection check (best predictor chosen on
   half the trajectories, scored on the other half, 200 random splits).
3. Learning curve: the learned predictors refitted on 1/4, 1/2 and all fit trajectories of each
   fold (fit = training minus the validation trajectories, as integrate/learning_curve.py), scored
   against the replicate futures; bootstrap SE of V(1/2) - V(all) over trajectories.
"""
import json
import sys
import time

import numpy as np

sys.path.insert(0, "/home/user/evalwork/vecworld/vw1/fresh/closure/scripts")
import closure_lib as CL  # noqa: E402

AN = CL.AN
PHI = sys.argv[1]
QUICK = "--quick" in sys.argv
K = 12 if PHI == "objects" else None
T0 = time.time()


def log(*a):
    print(f"[{time.time() - T0:8.1f}s]", *a, flush=True)


SCR = "/tmp/claude-0/-home-user/a7c2ec48-e3a6-5436-88da-a7523dbbe428/scratchpad/closure_quick"
if QUICK:   # code-path test only: old port data (horizons <= 8), few epochs
    AN.HORIZONS = [1, 2, 4, 8]
    AN.MLP.__init__.__defaults__ = (128, 1e-3, 1e-4, 3, 128, 0)
    D, cat, metas = CL.load_data(("qA", "qB"), res=SCR)
else:
    AN.HORIZONS = [1, 2, 4, 8, 16, 32]
    D, cat, metas = CL.load_data()
J = len(D["Yc"])
log(PHI, "J", J, "T", len(D["Yc"][0]) - 1, "test ticks", D["st_tick"][0].tolist())
nH = len(AN.HORIZONS)
RK = dict(epochs=8, seeds=(0,)) if QUICK else dict(epochs=300, seeds=(0, 1))

# ---- 1. copy check
ref = AN.closure(D, PHI, K=K, mlp=False)[0]
chk, _ = CL.closure_ext(D, PHI, K=K, mlp=False)
common = [nm for nm in chk["V"] if nm in ref["V"]]
copy_diff = max(float(np.abs(np.asarray(ref["V"][nm]) - np.asarray(chk["V"][nm])).max()) for nm in common)
copy_diff = max(copy_diff, float(np.abs(np.asarray(ref["V_oracle"]) - np.asarray(chk["V_oracle"])).max()))
log("copy check: max |V_analyze - V_copy| =", copy_diff, "over", common)
assert copy_diff == 0.0, copy_diff
del chk

# ---- 2. main estimate
rinfo, sinfo = [], []
hook = CL.make_rmlp_extra(log=log, info_store=rinfo, **RK)
if PHI == "objects":
    hook = CL.combine(hook, CL.make_slot_extra(D, log=log, info_store=sinfo, **RK))
else:
    hook = CL.combine(hook, CL.make_patch_extra(D, log=log, info_store=sinfo, **RK))
out, det = CL.closure_ext(D, PHI, K=K, mlp=True, extra=hook, log=log)
log("ceiling", np.round(out["ceiling"], 4).tolist(), "+-", np.round(out["ceiling_se"], 4).tolist())
log("best", out["best_name"])
for nm, v in out["V"].items():
    log(f"   {nm:14s}", np.round(v, 4).tolist())
err, orac, item_j = det["err"], det["orac"], det["item_j"]
V0, Vu = np.asarray(out["V0_mean_predictor"]), np.asarray(out["V_oracle"])
names = list(err)


def best_of(idx, use=None):
    use = names if use is None else use
    V = np.stack([err[nm][idx].mean(0) for nm in use])
    return V.min(0), [use[k] for k in V.argmin(0)]


# ceiling without the new predictor (VW-0 best-of set, MLP on) for comparison
NEW = ("rmlp", "slotnet", "patchnet")
old_set = [nm for nm in names if nm not in NEW]
all_idx = np.arange(len(item_j))
b_old, n_old = best_of(all_idx, old_set)
rng = np.random.default_rng(0)
uj = np.unique(item_j)
bs_old = []
for b in range(400):
    pick = rng.choice(uj, uj.size, replace=True)
    idx = np.concatenate([np.flatnonzero(item_j == q) for q in pick])
    bb, _ = best_of(idx, old_set)
    bs_old.append((err["mean"][idx].mean(0) - bb) / (err["mean"][idx].mean(0) - orac[idx].mean(0)))
out["vw0_set_only"] = {"best_level1": b_old, "best_name": n_old, "ceiling": (V0 - b_old) / (V0 - Vu),
                       "ceiling_se": np.std(bs_old, 0)}
# selection check: choose the best predictor per horizon on a random half of the trajectories,
# score it on the other half
rng = np.random.default_rng(1)
sel_c, sel_names = [], []
for s in range(200):
    half = rng.permutation(uj)[: uj.size // 2]
    A = np.isin(item_j, half)
    Bm = ~A
    cs = []
    for (tr_m, te_m) in ((A, Bm), (Bm, A)):
        _, nm_h = best_of(np.flatnonzero(tr_m))
        e = np.array([err[nm_h[hi]][te_m, hi].mean() for hi in range(nH)])
        v0, vu = err["mean"][te_m].mean(0), orac[te_m].mean(0)
        cs.append((v0 - e) / (v0 - vu))
        sel_names.append(nm_h)
    sel_c.append(np.mean(cs, 0))
sel_c = np.array(sel_c)
out["selection_check"] = {"ceiling_mean": sel_c.mean(0), "ceiling_sd_over_splits": sel_c.std(0),
                          "note": "best predictor per horizon chosen on half the trajectories, ceiling on the other half; "
                                  "200 random splits",
                          "chosen_names_freq": [{nm: int(sum(1 for x in sel_names if x[hi] == nm)) for nm in names}
                                                for hi in range(nH)]}
log("selection-checked ceiling", np.round(sel_c.mean(0), 4).tolist())
out["rmlp_info"] = rinfo
out["slotnet_info" if PHI == "objects" else "patchnet_info"] = sinfo

# ---- 3. learning curve
Ys, FUT, items = det["Ys"], det["FUT"], det["items"]
tmax = max(AN.HORIZONS)
fold_of = {jj: D["j"][jj] % AN.NFOLD for jj in range(J)}
lc_names = sorted(set(out["best_name"]) | {"ar1", "ridge_p2"})       # the best predictors, plus the cheap linear ones
lc_names = [nm for nm in lc_names if nm not in ("mean", "persistence", "knn", "kinematic")]
log("learning curve for", lc_names)
fracs = (0.25, 0.5, 1.0)
LC = {fr: {nm: np.zeros((len(items), nH, FUT.shape[3])) for nm in lc_names} for fr in fracs}
n_fit_traj = {fr: [] for fr in fracs}
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
            eff, sd = det["eff"], det["sd"]
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
            ex = CL.make_rmlp_extra(frac=1.0, **RK)(f, Ys, tr_j, fit_j, va_j, te_items)
            LC[fr]["rmlp"][te] = ex["rmlp"]
        if "slotnet" in lc_names:
            ex = CL.make_slot_extra(D, frac=1.0, **RK)(f, Ys, tr_j, fit_j, va_j, te_items)
            LC[fr]["slotnet"][te] = ex["slotnet"]
        if "patchnet" in lc_names:
            ex = CL.make_patch_extra(D, frac=1.0, **RK)(f, Ys, tr_j, fit_j, va_j, te_items)
            LC[fr]["patchnet"][te] = ex["patchnet"]
        log(f"  LC frac {fr} fold {f}: {len(fit_j)} fit trajectories")
neff = FUT.shape[3]
LCerr = {fr: {nm: ((FUT - P[:, None]) ** 2).sum(3).mean(1) / neff for nm, P in LC[fr].items()} for fr in fracs}
lc = {"fit_trajectories_per_fold": {str(fr): n_fit_traj[fr] for fr in fracs}, "names": lc_names,
      "note": "all fits on the fit trajectories of each fold only (training minus validation); the main closure refits "
              "ridge and AR(1) on all training trajectories (fit + validation)", "V": {}, "best": {}, "ceiling": {}}
for fr in fracs:
    lc["V"][str(fr)] = {nm: e.mean(0) for nm, e in LCerr[fr].items()}
    Vb = np.min(np.stack([e.mean(0) for e in LCerr[fr].values()]), 0)
    lc["best"][str(fr)] = Vb
    lc["ceiling"][str(fr)] = (V0 - Vb) / (V0 - Vu)
# saturation: bootstrap over trajectories of the best-of envelope at 1/2 vs all
rng = np.random.default_rng(2)
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
lc["saturated"] = [bool(abs(d) < 2 * s or abs(r) < 0.02) for d, s, r in
                   zip(dV, dd.std(0), lc["rel_drop_half_to_all"])]
lc["saturation_rule"] = "saturated if V(1/2) - V(all) < 2 SE (bootstrap over trajectories) or the relative drop < 2%"
out["learning_curve"] = lc
log("LC best", {k: np.round(v, 4).tolist() for k, v in lc["best"].items()})
log("LC saturated", lc["saturated"], "rel drop", np.round(lc["rel_drop_half_to_all"], 3).tolist())

out["data"] = {"J": J, "T": len(D["Yc"][0]) - 1, "test_ticks": D["st_tick"][0].tolist(),
               "designer_seeds": [m["designer_seed"] for m in metas], "world_seed": 0,
               "replicates": int(FUT.shape[1]), "copy_check_max_abs_diff": copy_diff,
               "source": [f"{CL.RES}/sim_{m['tag']}.npz" for m in metas]}
out["seconds"] = time.time() - T0
sfx = "_quick" if QUICK else ""
json.dump(CL.jsonable(out), open(f"{SCR if QUICK else CL.RES}/closure_{PHI}{sfx}.json", "w"), indent=1)
np.savez_compressed(f"{SCR if QUICK else CL.RES}/closure_{PHI}{sfx}_items.npz",
                    err=np.stack([err[nm] for nm in names]).astype(np.float32), names=np.array(names),
                    orac=orac.astype(np.float32), items=items, item_j=item_j, eff=det["eff"], sd=det["sd"],
                    FUT1=FUT[:, :, 0].astype(np.float32),
                    P1=np.stack([det["preds"][nm][:, 0] for nm in names]).astype(np.float32))
log("saved", f"{SCR if QUICK else CL.RES}/closure_{PHI}{sfx}.json")
