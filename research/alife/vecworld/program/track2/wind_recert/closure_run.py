"""closure_run -- closure ceilings in the wind world (sets F and P) and the matched wind-free reference.

usage: python -B closure_run.py F|M|P coarse|objects [--nomlp] [--jax]
  F  free runs at sigma_w = 0.05 (results/raw/free_b*.npz)
  M  the wind-free closure data (vw1/fresh/closure sim_A, sim_B) cut to F's size: 8 + 8 trajectories,
     ticks 0..236, test ticks 40/100/160/220, branches cut to 16 ticks
  P  program-mix runs (results/raw/prog_b*.npz): the input-blind closure_ext set, plus input-aware
     ridge predictors (feats.py) through closure_ext's 'extra' hook on the same folds and items; then the
     exam effect (loss of the best input-blind predictor), its detectability, and the true program
     effect from the no-input twins.
Estimator: closure_lib.closure_ext with AN.HORIZONS = [1, 2, 4, 8, 16] (VW-0 MLP on unless --nomlp);
check: unmodified analyze.closure (MLP off) equals closure_ext (MLP off) exactly on the same data.
-> results/closure_<SET>_<view>.json and results/raw/closure_<SET>_<view>_items.npz
"""
import glob
import json
import math
import sys
import time

import numpy as np

sys.dont_write_bytecode = True
sys.path.insert(0, "/home/user/evalwork/vecworld/vw1/fresh/closure/scripts")
import closure_lib as CL  # noqa: E402   (first: caches integrate/analyze before actuation/ joins the path)
import wr  # noqa: E402
import feats as FT  # noqa: E402

AN = CL.AN
AN.HORIZONS = list(wr.HORIZONS)
HZ = AN.HORIZONS
nH, TMAX = len(HZ), max(HZ)
NC = wr.WD.NC
SET, VIEW = sys.argv[1], sys.argv[2]
MLP = "--nomlp" not in sys.argv
JAXP = "--jax" in sys.argv          # add closure_lib's JAX predictors (rmlp + patchnet/slotnet), F and M only
SFX = "_jax" if JAXP else ""
DEBUG = "--debug" in sys.argv
K = 12 if VIEW == "objects" else None
T0 = time.time()


def log(*a):
    print(f"[{time.time() - T0:8.1f}s]", *a, flush=True)


def make_D(Y, B, test):
    J = len(Y)
    return {"Yc": [Y[j][:, :NC].astype(float) for j in range(J)], "Yo": [Y[j][:, NC:].astype(float) for j in range(J)],
            "Bc": [B[j][..., :NC].astype(float) for j in range(J)], "Bo": [B[j][..., NC:].astype(float) for j in range(J)],
            "st_tick": [np.array(test) for _ in range(J)], "j": list(range(J))}


def load(set_):
    extra = {}
    if set_ == "F":
        fs = sorted(glob.glob(f"{wr.RAW}/free_b*.npz"))
        Z = [np.load(f) for f in fs]
        Y = np.concatenate([z["Y"] for z in Z])
        B = np.concatenate([z["B"] for z in Z])
        D = make_D(Y, B, wr.F_TEST)
        extra["source"] = fs
    elif set_ == "M":
        Ys, Bs = [], []
        for tg in "AB":
            z = np.load(f"/home/user/evalwork/vecworld/vw1/fresh/closure/results/sim_{tg}.npz")
            Ys.append(z["Y"][:8, :wr.F_T + 1])
            Bs.append(z["B"][:8, :, :, :wr.TB])
        D = make_D(np.concatenate(Ys), np.concatenate(Bs), wr.F_TEST)
        extra["source"] = ["vw1/fresh/closure/results/sim_A.npz[:8]", "sim_B.npz[:8]"]
    else:
        fs = sorted(glob.glob(f"{wr.RAW}/prog_b*.npz"))
        Z = [np.load(f) for f in fs]
        meta = [json.load(open(f.replace(".npz", ".json"))) for f in fs]
        Y = np.concatenate([z["Y"] for z in Z])
        D = make_D(Y, np.concatenate([z["B"] for z in Z]), wr.P_TEST)
        extra["U"] = np.concatenate([z["U"] for z in Z]).astype(float)
        extra["Bnone"] = np.concatenate([z["Bnone"] for z in Z]).astype(float)
        extra["items"] = {(it["j"], it["test_index"]): it for m in meta for it in m["items"]}
        extra["episodes"] = [e for m in meta for e in m["episodes"]]
        extra["source"] = fs
    return D, extra


def std_of(D):
    Ys = D["Yo"] if VIEW == "objects" else D["Yc"]
    sd = np.concatenate(Ys).std(0)
    eff = sd > 1e-6 * max(sd.max(), 1e-12)
    return eff, np.where(eff, sd, 1.0)


# ----------------------------------------------------------------------------- input-aware hook
def aware_hook(D, U, ps=(1, 2, 4), info=None):
    raw = D["Yo"] if VIEW == "objects" else D["Yc"]
    eff, sd = std_of(D)
    J = len(raw)
    cache = {}

    def feats_of(jj):
        if jj not in cache:
            ts = np.arange(0, len(raw[jj]) - TMAX)
            F, disp = FT.input_features(VIEW, raw[jj], U[jj], ts, HZ)
            kw = None
            if VIEW == "objects":
                kw = {h: FT.kin_wind(raw[jj][ts], h, disp[i])[:, eff] / sd[eff] for i, h in enumerate(HZ)}
            cache[jj] = (F, kw)
        return cache[jj]

    def extra(f, Ys, tr_j, fit_j, va_j, te_items):
        out = {}
        t1 = time.time()
        variants = [(p, "ridge") for p in ps] + ([(4, "kinw")] if VIEW == "objects" else [])
        for p, kind in variants:
            nm = f"ridge_p{p}+u" if kind == "ridge" else "kinw+ridge_p4+u"
            P = np.zeros((len(te_items), nH, Ys[0].shape[1]))

            def rows(js, hi, h):
                X, T = [], []
                for jj in js:
                    ts = np.arange(p - 1, len(Ys[jj]) - TMAX)
                    Fu, kw = feats_of(jj)
                    X.append(np.concatenate([AN.lag_matrix(Ys[jj], ts, p), Fu[h][ts]], 1))
                    base = kw[h][ts] if kind == "kinw" else Ys[jj][ts]
                    T.append(Ys[jj][ts + h] - base)
                return np.concatenate(X), np.concatenate(T)
            lam = []
            for hi, h in enumerate(HZ):
                Xf, Tf = rows(fit_j, hi, h)
                Xv, Tv = rows(va_j, hi, h)
                Xa, Ta = rows(tr_j, hi, h)
                nl = p * Ys[0].shape[1]                       # lag columns (already standardised)
                s = Xf[:, nl:].std(0)
                keep = np.concatenate([np.ones(nl, bool), s > 1e-12])
                scale = np.concatenate([np.ones(nl), np.where(s > 1e-12, s, 1.0)])
                Xf, Xv, Xa = (x[:, keep] / scale[keep] for x in (Xf, Xv, Xa))
                rg = AN.Ridge().fit(Xf, [Tf], Xv, [Tv])
                lam.append(rg.lams[0])
                rg = AN.Ridge().fit(Xa, [Ta], lams=rg.lams)
                for a, (jj, i, t) in enumerate(te_items):
                    Fu, kw = feats_of(jj)
                    x = np.concatenate([AN.lag_matrix(Ys[jj], np.array([t]), p), Fu[h][[t]]], 1)[:, keep] / scale[keep]
                    base = kw[h][t] if kind == "kinw" else Ys[jj][t]
                    P[a, hi] = base + rg.predict(x, 0)[0]
                if kind == "kinw":                            # the kinematic+wind map alone (no fit)
                    out.setdefault("kinw_only", np.zeros_like(P))
                    for a, (jj, i, t) in enumerate(te_items):
                        out["kinw_only"][a, hi] = feats_of(jj)[1][h][t]
            out[nm] = P
            if info is not None:
                info.append({"fold": f, "name": nm, "lambda_by_h": lam})
        log(f"  aware fold {f}: {time.time() - t1:.1f} s")
        return out
    return extra


def local_hook(D, U, info=None):
    """'+u2' (added after the declared dense '+u' features overfit): a blind base predictor, refitted on the
    fold exactly as closure_ext fits it, plus an input response linear in N_LOC local features per output
    coordinate (feats.coarse_local / feats.objects_local) with coefficients shared across blocks or slots,
    one set per horizon and coordinate type (3 coarse types, 12 object features), fitted by least squares
    on the base's in-sample residuals over the training trajectories (raw units)."""
    raw = D["Yo"] if VIEW == "objects" else D["Yc"]
    eff, sd = std_of(D)
    eidx = np.flatnonzero(eff)
    ntype = wr.WD.NF if VIEW == "objects" else 3
    tye = (eidx % wr.WD.NF) if VIEW == "objects" else (eidx // 64)
    sde = sd[eff]
    cache = {}
    P0 = 3                                                   # first row usable by every base (4 lags)

    def loc(jj):
        if jj not in cache:
            ts = np.arange(0, len(raw[jj]) - TMAX)
            if VIEW == "coarse":
                Dd = FT.dblk_of(FT.ucum_all(U[jj], ts, HZ))
                cache[jj] = {h: FT.coarse_local(raw[jj][ts], Dd[i])[:, eff].astype(np.float32) for i, h in enumerate(HZ)}
            else:
                cum = FT.slot_disp_cum(raw[jj][ts], U[jj], ts, TMAX)
                cache[jj] = {h: FT.objects_local(raw[jj][ts], cum, h)[:, eff].astype(np.float32) for h in HZ}
        return cache[jj]

    def bases(Ys, tr_j, fit_j, va_j):
        fns = {}
        mu = np.concatenate([Ys[jj] for jj in tr_j]).mean(0)
        X1, F1, _ = AN.multi_pairs([Ys[jj] for jj in tr_j], 1, TMAX)
        rho = np.stack([((X1 - mu) * (F1[hi] - mu)).sum(0) / np.maximum(((X1 - mu) ** 2).sum(0), 1e-12)
                        for hi in range(nH)])
        fns["ar1"] = lambda Y, ts: mu[None, None] + rho[None] * (Y[ts] - mu)[:, None]

        def ridge_fn(p, kin=False):
            if kin:
                sdq, full_idx, n1 = sde, eidx, len(sd)

                def ks(rows_, h):
                    Yr = np.zeros((len(rows_), n1))
                    Yr[:, full_idx] = rows_ * sdq
                    return AN.kinematic(Yr, h, K)[:, full_idx] / sdq
            base = (lambda Y0, h: ks(Y0, h)) if kin else (lambda Y0, h: Y0)
            Xf, Ff, Y0f = AN.multi_pairs([Ys[jj] for jj in fit_j], p, TMAX)
            Xv, Fv, Y0v = AN.multi_pairs([Ys[jj] for jj in va_j], p, TMAX)
            rg = AN.Ridge().fit(Xf, [Ff[hi] - base(Y0f, h) for hi, h in enumerate(HZ)],
                                Xv, [Fv[hi] - base(Y0v, h) for hi, h in enumerate(HZ)])
            X, F, Y0 = AN.multi_pairs([Ys[jj] for jj in tr_j], p, TMAX)
            rg = AN.Ridge().fit(X, [F[hi] - base(Y0, h) for hi, h in enumerate(HZ)], lams=rg.lams)

            def fn(Y, ts):
                x = AN.lag_matrix(Y, ts, p)
                return np.stack([base(Y[ts], h) + rg.predict(x, hi) for hi, h in enumerate(HZ)], 1)
            return fn
        for p in ((1, 2) if VIEW == "objects" else (1, 2, 4)):
            fns[f"ridge_p{p}"] = ridge_fn(p)
        if VIEW == "objects":
            fns["kin+ridge_p4"] = ridge_fn(4, kin=True)
        return fns

    def extra(f, Ys, tr_j, fit_j, va_j, te_items):
        t1 = time.time()
        out = {}
        fns = bases(Ys, tr_j, fit_j, va_j)
        out["ar1_rep"] = np.stack([fns["ar1"](Ys[jj], np.array([t]))[0] for jj, i, t in te_items])
        for bn, fn in fns.items():
            Btr = {jj: fn(Ys[jj], np.arange(P0, len(Ys[jj]) - TMAX)) for jj in tr_j}
            Pte = np.stack([fn(Ys[jj], np.array([t]))[0] for jj, i, t in te_items])      # (n_te, nH, q)
            nloc = loc(tr_j[0])[HZ[0]].shape[-1]
            coefs = np.zeros((nH, ntype, nloc))
            for hi, h in enumerate(HZ):
                Xs, ys = [], []
                for jj in tr_j:
                    ts = np.arange(P0, len(Ys[jj]) - TMAX)
                    Xs.append(loc(jj)[h][ts])                                          # (n, q, 9)
                    ys.append((Ys[jj][ts + h] - Btr[jj][:, hi]) * sde)                 # raw residual (n, q)
                Xs, ys = np.concatenate(Xs), np.concatenate(ys)
                for c in range(ntype):
                    sel = tye == c
                    if not sel.any():
                        continue
                    A = Xs[:, sel].reshape(-1, nloc).astype(float)
                    b = ys[:, sel].reshape(-1)
                    G_ = A.T @ A
                    coefs[hi, c] = np.linalg.solve(G_ + (1e-8 * np.trace(G_) / nloc + 1e-300) * np.eye(nloc), A.T @ b)
                for a, (jj, i, t) in enumerate(te_items):
                    corr = np.einsum("qk,qk->q", loc(jj)[h][t].astype(float), coefs[hi, tye])
                    Pte[a, hi] = Pte[a, hi] + corr / sde
            out[f"{bn}+u2"] = Pte
            if DEBUG:
                out[f"{bn}_base"] = np.stack([fn(Ys[jj], np.array([t]))[0] for jj, i, t in te_items])
            if info is not None:
                info.append({"fold": f, "name": f"{bn}+u2", "coef_by_h_type": coefs})
        log(f"  local fold {f}: {time.time() - t1:.1f} s")
        return out
    return extra


# ----------------------------------------------------------------------------- exam effect
def exam_effect(det, out, klass, aware_names):
    err, FUT, preds = det["err"], det["FUT"], det["preds"]
    names = list(err)
    blind = [nm for nm in names if nm not in aware_names]
    V = {nm: e.mean(0) for nm, e in err.items()}
    best_all = [min(names, key=lambda nm: V[nm][hi]) for hi in range(nH)]
    best_blind = [min(blind, key=lambda nm: V[nm][hi]) for hi in range(nH)]
    Vbest = np.array([V[best_all[hi]][hi] for hi in range(nH)])
    q = FUT.shape[3]
    res = {"best_all": best_all, "best_blind": best_blind, "V_best_all": Vbest,
           "V_best_blind": np.array([V[best_blind[hi]][hi] for hi in range(nH)])}

    def pair(a_by_h, b_by_h, sel):
        """loss of a (blind) vs b (aware): per item, R = 6 and single truth; detectability."""
        d6 = np.stack([err[a_by_h[hi]][sel, hi] - err[b_by_h[hi]][sel, hi] for hi in range(nH)], 1)
        dl = []
        for hi in range(nH):
            ya, yb = preds[a_by_h[hi]][sel, hi], preds[b_by_h[hi]][sel, hi]
            F = FUT[sel, :, hi]
            dl.append((((F - ya[:, None]) ** 2).sum(-1) - ((F - yb[:, None]) ** 2).sum(-1)) / q)   # (n, R)
        dl = np.stack(dl, 2)                                                                     # (n, R, nH)
        R = dl.shape[1]
        sn2 = dl.var(1, ddof=1).mean(0)
        sb2 = np.maximum(d6.var(0, ddof=1) - sn2 / R, 0.0)
        r = {"n_items": int(sel.sum()), "loss_mean": d6.mean(0), "loss_se": d6.std(0, ddof=1) / math.sqrt(sel.sum()),
             "loss_over_Vbest": d6.mean(0) / Vbest, "loss_single_truth_mean": dl[:, 0].mean(0),
             "var_between_items": sb2, "var_truth_noise_single": sn2}
        for n in (16, 32, 64, 128):
            for Rr in (1, 6, 16):
                se = np.sqrt((sb2 + sn2 / Rr) / n)
                r[f"z_n{n}_R{Rr}"] = d6.mean(0) / se
                r[f"mde80_over_Vbest_n{n}_R{Rr}"] = 2.486 * se / Vbest
        return r
    allm = np.ones(len(klass), bool)
    res["best_vs_best"] = {"all": pair(best_blind, best_all, allm)}
    for kl in wr.CLASSES:
        res["best_vs_best"][kl] = pair(best_blind, best_all, klass == kl)
    progs = klass != "none"
    res["best_vs_best"]["programs_only"] = pair(best_blind, best_all, progs)
    res["best_vs_best"]["aimed_regional"] = pair(best_blind, best_all, (klass == "aimed") | (klass == "regional"))
    fixed = {}
    for nm in aware_names:
        if nm.endswith("+u2"):
            b = nm[:-3]
        elif nm.startswith("ridge_p") and nm.endswith("+u"):
            b = nm[:-2]
        elif nm == "kinw+ridge_p4+u":
            b = "kin+ridge_p4"
        else:
            continue
        masks = {"all": allm, "aimed_regional": (klass == "aimed") | (klass == "regional"), "programs": progs}
        fixed[f"{b} vs {nm}"] = {kl: pair([b] * nH, [nm] * nH, masks.get(kl, klass == kl))
                                 for kl in ("all", "programs", "aimed_regional") + wr.CLASSES}
    res["fixed_pairs"] = fixed
    # ceilings by class (best-of over all; and blind only)
    orac = det["orac"]
    res["by_class"] = {}
    for kl in ("all",) + wr.CLASSES:
        sel = allm if kl == "all" else klass == kl
        Vk = {nm: err[nm][sel].mean(0) for nm in names}
        V0, Vu = Vk["mean"], orac[sel].mean(0)
        ba = np.min(np.stack([Vk[nm] for nm in names]), 0)
        bb = np.min(np.stack([Vk[nm] for nm in blind]), 0)
        res["by_class"][kl] = {"n": int(sel.sum()), "V_oracle": Vu, "V0": V0, "V_best_all": ba, "V_best_blind": bb,
                               "ceiling_all": (V0 - ba) / (V0 - Vu), "ceiling_blind": (V0 - bb) / (V0 - Vu)}
    return res


def twin_effect(det, Bn_std, klass, Vbest):
    """True mean program effect per item from the no-input twins (branch keys 0..2 = FUT replicates 1..3)."""
    FUT = det["FUT"]
    q = FUT.shape[3]
    sel = klass != "none"
    out = {}
    Pm = FUT[:, 1:1 + wr.R_TWIN]                  # program branches with twin keys (n, 3, nH, q)
    Dl = Pm - Bn_std                              # paired differences
    crn = ((Dl.mean(1) ** 2).sum(-1) - Dl.var(1, ddof=1).sum(-1) / wr.R_TWIN) / q        # (n, nH) unbiased
    unp = ((((FUT.mean(1) - Bn_std.mean(1)) ** 2).sum(-1) - FUT.var(1, ddof=1).sum(-1) / FUT.shape[1]
            - Bn_std.var(1, ddof=1).sum(-1) / wr.R_TWIN) / q)
    for kl in wr.CLASSES[1:] + ("programs",):
        s = sel if kl == "programs" else klass == kl
        out[kl] = {"n": int(s.sum()), "crn_effect_over_Vbest": np.nanmean(crn[s], 0) / Vbest,
                   "crn_effect_se_over_Vbest": np.nanstd(crn[s], 0, ddof=1) / math.sqrt(s.sum()) / Vbest,
                   "unpaired_effect_over_Vbest": np.nanmean(unp[s], 0) / Vbest,
                   "unpaired_effect_se_over_Vbest": np.nanstd(unp[s], 0, ddof=1) / math.sqrt(s.sum()) / Vbest,
                   "share_items_crn_ge_0.1Vbest": (crn[s] >= 0.1 * Vbest).mean(0)}
    # ideal loss: a blind predictor of the no-input mean vs an aware predictor of the program mean. Per item
    # d = e + 2 (ybar_R - mu_P).(mu_P - mu_0) / q; noise variance for one truth 4 Delta' Sigma Delta / q^2,
    # Sigma from the 6 program replicates, Delta the CRN mean shift. None items: d = 0.
    Dm = Dl.mean(1)                                                                        # (n, nH, q)
    proj = np.einsum("nrhq,nhq->nrh", FUT - FUT.mean(1, keepdims=True), np.nan_to_num(Dm))
    noise1 = 4.0 * (proj ** 2).sum(1) / (FUT.shape[1] - 1) / q ** 2                        # (n, nH)
    e = np.nan_to_num(crn)
    ideal = {}
    for kl, s in (("all", np.ones(len(klass), bool)), ("programs", sel),
                  ("aimed_regional", (klass == "aimed") | (klass == "regional"))):
        m, vb, vn = e[s].mean(0), e[s].var(0, ddof=1), noise1[s].mean(0)
        r = {"n": int(s.sum()), "loss_over_Vbest": m / Vbest}
        for n_ in (16, 32, 64, 128):
            for R in (1, 6, 16):
                r[f"z_n{n_}_R{R}"] = m / np.sqrt((vb + vn / R) / n_)
        ideal[kl] = r
    out["ideal_loss_detectability"] = ideal
    return out, crn, unp


# ----------------------------------------------------------------------------- main
def main():
    D, ex = load(SET)
    J = len(D["Yc"])
    log(SET, VIEW, "J", J, "T", len(D["Yc"][0]) - 1, "test", D["st_tick"][0].tolist(), "mlp", MLP)
    # copy check against the unmodified analyze.closure (MLP off)
    ref = AN.closure(D, VIEW, K=K, mlp=False)[0]
    chk, _ = CL.closure_ext(D, VIEW, K=K, mlp=False)
    common = [nm for nm in chk["V"] if nm in ref["V"]]
    diff = max(float(np.abs(np.asarray(ref["V"][nm]) - np.asarray(chk["V"][nm])).max()) for nm in common)
    diff = max(diff, float(np.abs(np.asarray(ref["V_oracle"]) - np.asarray(chk["V_oracle"])).max()))
    log("copy check max |V_analyze - V_copy| =", diff)
    assert diff == 0.0
    hook, ainfo, aware = None, [], []
    jinfo, sinfo = [], []
    if SET == "P":
        hook = CL.combine(aware_hook(D, list(ex["U"]), info=ainfo), local_hook(D, list(ex["U"]), info=ainfo))
    elif JAXP:
        RK = dict(epochs=300, seeds=(0, 1))
        hook = CL.make_rmlp_extra(log=log, info_store=jinfo, **RK)
        hook = CL.combine(hook, CL.make_slot_extra(D, log=log, info_store=sinfo, **RK) if VIEW == "objects"
                          else CL.make_patch_extra(D, log=log, info_store=sinfo, **RK))
    out, det = CL.closure_ext(D, VIEW, K=K, mlp=MLP, extra=hook, log=log)
    if SET == "P":
        aware = [nm for nm in det["err"] if nm.endswith("+u") or nm.endswith("+u2") or nm == "kinw_only"]
        out["ar1_rep_check_max_abs_V_diff"] = float(np.abs(det["err"]["ar1_rep"] - det["err"]["ar1"]).max())
        log("ar1 refit check (max |err diff|)", out["ar1_rep_check_max_abs_V_diff"])
        for dct in (det["err"], det["preds"], out["V"]):
            dct.pop("ar1_rep")
    log("ceiling", np.round(out["ceiling"], 4).tolist(), "+-", np.round(out["ceiling_se"], 4).tolist())
    log("best", out["best_name"], "Vbest", np.round(out["best_level1"], 4).tolist(),
        "Voracle", np.round(out["V_oracle"], 4).tolist())
    eff, sd = det["eff"], det["sd"]
    # common scale: the fresh closure SD (wind.closure_sd) for oracle / best comparisons across sets
    sdc, effc = wr.WD.closure_sd()[VIEW]
    rescale = (sd[eff] / sdc[eff]) ** 2                       # per effective coordinate
    FUT = det["FUT"]
    orac_c = ((FUT - FUT.mean(1, keepdims=True)) ** 2 * rescale).sum((1, 3)) / (FUT.shape[1] - 1) / eff.sum()
    bn = out["best_name"]
    vb_c = np.array([(((FUT[:, :, hi] - det["preds"][bn[hi]][:, None, hi]) ** 2 * rescale).sum(-1).mean(1)
                      / eff.sum()).mean() for hi in range(nH)])
    out["common_scale"] = {"note": "errors in units of the fresh closure SD (36 wind-free trajectories)",
                           "V_oracle": orac_c.mean(0), "V_oracle_se": orac_c.std(0, ddof=1) / math.sqrt(len(orac_c)),
                           "V_best": vb_c}
    out["copy_check_max_abs_diff"] = diff
    if JAXP:
        out["rmlp_info"], out["net_info"] = jinfo, sinfo
    out["data"] = {"set": SET, "J": J, "T": len(D["Yc"][0]) - 1, "test_ticks": D["st_tick"][0].tolist(),
                   "replicates": int(FUT.shape[1]), "source": ex["source"], "mlp": MLP}
    sv = {"err": np.stack([det["err"][nm] for nm in det["err"]]).astype(np.float32),
          "names": np.array(list(det["err"])), "orac": det["orac"].astype(np.float32), "items": det["items"],
          "item_j": det["item_j"], "orac_common": orac_c.astype(np.float32)}
    if SET == "P":
        klass = np.array([ex["items"][(int(jj), int(i))]["klass"] for jj, i, t in det["items"]])
        Cn = np.array([ex["items"][(int(jj), int(i))]["charged_nats"] for jj, i, t in det["items"]])
        out["aware_names"] = aware
        out["aware_info"] = ainfo
        out["exam_effect"] = exam_effect(det, out, klass, aware)
        Bn = np.stack([ex["Bnone"][jj, i] for jj, i, t in det["items"]])            # (n, 3, TB, 336)
        Bn = Bn[..., NC:] if VIEW == "objects" else Bn[..., :NC]
        Bn_std = np.stack([Bn[:, :, h - 1] for h in HZ], 2)[..., eff] / sd[eff]      # (n, 3, nH, q)
        tw, crn, unp = twin_effect(det, Bn_std, klass, out["exam_effect"]["V_best_all"])
        out["twin_effect"] = tw
        out["items_meta"] = {"klass_counts": {k: int((klass == k).sum()) for k in wr.CLASSES},
                             "charged_nats_by_class": {k: [float(Cn[klass == k].min()), float(Cn[klass == k].mean()),
                                                           float(Cn[klass == k].max())] for k in wr.CLASSES}}
        sv.update(klass=klass, nats=Cn, crn=crn.astype(np.float32), unp=unp.astype(np.float32))
        ee = out["exam_effect"]["best_vs_best"]
        for kl in ("all", "programs_only") + wr.CLASSES:
            log(f"  loss/Vbest {kl:9s}", np.round(ee[kl]["loss_over_Vbest"], 3).tolist(),
                "z64 R16", np.round(ee[kl]["z_n64_R16"], 1).tolist())
        for kl, v in tw.items():
            if "crn_effect_over_Vbest" in v:
                log(f"  twin effect/Vbest {kl:9s}", np.round(v["crn_effect_over_Vbest"], 3).tolist())
    out["seconds"] = time.time() - T0
    json.dump(CL.jsonable(out), open(f"{wr.RES}/closure_{SET}_{VIEW}{SFX}.json", "w"), indent=1)
    np.savez_compressed(f"{wr.RAW}/closure_{SET}_{VIEW}{SFX}_items.npz", **sv)
    log("saved", f"{wr.RES}/closure_{SET}_{VIEW}{SFX}.json")


if __name__ == "__main__":
    main()
