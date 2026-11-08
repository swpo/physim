"""p4lib -- input-aware level-1 predictors, the exam effect and energy scores for the program-mix set P.

Copied from track2/wind_recert/closure_run.py with the view, horizons and data passed in (that script
reads them from sys.argv): local_hook ('+u2', the structured linear input response), exam_effect,
twin_effect. New here:
  wind channels   the declared future commands as level-1 input channels, in windows relative to the
                  forecast time t: single ticks [t, t+1) .. [t+3, t+4), then [t+4, t+8), [t+8, t+16)
                  (and [t+16, t+32) when the longest horizon is 32).
                  coarse: the block-averaged displacement field 4 * Ebar(sum u) (2 x 8 x 8 px, wind_recert
                  feats.dblk_of) per window, in each block's 3 x 3 periodic neighbourhood (18 per window);
                  objects: per slot the wind displacement at its kinematically extrapolated centroid summed
                  over each window (feats.slot_disp_cum; 2 per window).
  aware baseline  per horizon the better (on the validation trajectories) of AR(1)+u2 and ridge_p2+u2, both
                  fitted on the fit trajectories only (closure_lib.linear_baselines plus the '+u2' least
                  squares input response on their fit residuals).
  patchnet+u /    closure_lib's patchnet / slotnet (same architecture, training, early stopping, seeds)
  slotnet+u       with the wind channels appended to every block's / slot's inputs and the aware
                  baseline in place of the blind one (zero-initialised output: epoch 0 is the baseline).
  energy scores   ensemble forecasts from every point predictor: the point forecast plus m = 32 residual
                  vectors drawn from out-of-fold items of the other folds (all replicate truths), the
                  same draws for every predictor (paired); fair energy score (vw.scoring convention: RMS
                  norm on the closure's standardised coordinates) per replicate truth; the oracle
                  reference is the leave-one-out score of the replicate truths; the ideal 'actions
                  matter' contrast scores the no-input twins (blind) and the other program replicates
                  (aware) on the replicates whose keys no twin shares (0, 4, 5).
"""
from __future__ import annotations

import math
import time

import numpy as np


def setup(CL_, FT_, wr_):
    global CL, AN, FT, wr
    CL, AN, FT, wr = CL_, CL_.AN, FT_, wr_


def windows(tmax):
    w = [(0, 1), (1, 2), (2, 3), (3, 4), (4, 8), (8, 16)]
    if tmax >= 32:
        w.append((16, 32))
    return [x for x in w if x[1] <= tmax]


# ----------------------------------------------------------------------------- local input features
class Local:
    """Raw level-1 rows and commands per trajectory; caches the '+u2' local features (raw units, effective
    coordinates) and the wind channels for all rows t in [0, T - tmax)."""

    def __init__(self, view, raw, U, eff, HZ):
        self.view, self.raw, self.U, self.eff, self.HZ = view, raw, U, eff, list(HZ)
        self.tmax = max(HZ)
        self.wins = windows(self.tmax)
        self._loc, self._wc = {}, {}
        G = FT.G
        self.G = G

    def ts(self, jj):
        return np.arange(0, len(self.raw[jj]) - self.tmax)

    def loc(self, jj):
        if jj not in self._loc:
            ts, raw, U, eff = self.ts(jj), self.raw[jj], self.U[jj], self.eff
            if self.view == "coarse":
                Dd = FT.dblk_of(FT.ucum_all(U, ts, self.HZ))
                self._loc[jj] = {h: FT.coarse_local(raw[ts], Dd[i])[:, eff].astype(np.float32) for i, h in enumerate(self.HZ)}
            else:
                cum = FT.slot_disp_cum(raw[ts], U, ts, self.tmax)
                self._loc[jj] = {h: FT.objects_local(raw[ts], cum, h)[:, eff].astype(np.float32) for h in self.HZ}
        return self._loc[jj]

    def wind(self, jj):
        """coarse -> (n_t, 64, 18 * n_win); objects -> (n_t, K, 2 * n_win) (raw px)."""
        if jj not in self._wc:
            ts, U = self.ts(jj), self.U[jj]
            G = self.G
            if self.view == "coarse":
                cs = np.concatenate([np.zeros((1, U.shape[1])), np.cumsum(U, 0)])
                F = []
                for a, b in self.wins:
                    D = FT.dblk_of(cs[ts + b] - cs[ts + a]).reshape(len(ts), 2, G, G)
                    for dy in (-1, 0, 1):
                        for dx in (-1, 0, 1):
                            F.append(np.roll(D, (-dy, -dx), (2, 3)))
                X = np.concatenate(F, 1).reshape(len(ts), -1, G * G).transpose(0, 2, 1)
            else:
                cum = FT.slot_disp_cum(self.raw[jj][ts], U, ts, self.tmax)
                X = np.concatenate([cum[b] - cum[a] for a, b in self.wins], -1)
            self._wc[jj] = X.astype(np.float32)
        return self._wc[jj]


def view_types(view, eff):
    eidx = np.flatnonzero(eff)
    if view == "objects":
        return eidx % FT.NF, FT.NF
    return eidx // 64, 3


def fit_u2(view, Ys, fn, js, L, tye, ntype, sde, HZ, P0=3):
    """Least-squares input response of the base fn on its residuals over trajectories js (raw units):
    coefs (nH, ntype, nloc)."""
    tmax = max(HZ)
    nloc = L.loc(js[0])[HZ[0]].shape[-1]
    coefs = np.zeros((len(HZ), ntype, nloc))
    Btr = {jj: fn(Ys[jj], np.arange(P0, len(Ys[jj]) - tmax)) for jj in js}
    for hi, h in enumerate(HZ):
        Xs, ys = [], []
        for jj in js:
            ts = np.arange(P0, len(Ys[jj]) - tmax)
            Xs.append(L.loc(jj)[h][ts])
            ys.append((Ys[jj][ts + h] - Btr[jj][:, hi]) * sde)
        Xs, ys = np.concatenate(Xs), np.concatenate(ys)
        for c in range(ntype):
            sel = tye == c
            if not sel.any():
                continue
            A = Xs[:, sel].reshape(-1, nloc).astype(float)
            b = ys[:, sel].reshape(-1)
            G_ = A.T @ A
            coefs[hi, c] = np.linalg.solve(G_ + (1e-8 * np.trace(G_) / nloc + 1e-300) * np.eye(nloc), A.T @ b)
    return coefs


def u2_corr(L, jj, ts, coefs, tye, sde, HZ):
    """(len(ts), nH, q) correction in standardised units."""
    return np.stack([np.einsum("nqk,qk->nq", L.loc(jj)[h][ts].astype(float), coefs[hi, tye]) / sde
                     for hi, h in enumerate(HZ)], 1)


def local_hook(view, D, L, K=None, info=None, log=print):
    """'+u2' predictors (wind_recert closure_run.local_hook): a blind base refitted on the fold exactly as
    closure_ext fits it plus the input response linear in the local features, coefficients shared across
    blocks or slots, one set per horizon and coordinate type, fitted on the base's in-sample residuals."""
    HZ = list(AN.HORIZONS)
    nH, TMAX = len(HZ), max(HZ)
    raw = D["Yo"] if view == "objects" else D["Yc"]
    sd_all = np.concatenate(raw).std(0)
    eff = sd_all > 1e-6 * max(sd_all.max(), 1e-12)
    sd = np.where(eff, sd_all, 1.0)
    eidx = np.flatnonzero(eff)
    tye, ntype = view_types(view, eff)
    sde = sd[eff]
    P0 = 3

    def bases(Ys, tr_j, fit_j, va_j):
        fns = {}
        mu = np.concatenate([Ys[jj] for jj in tr_j]).mean(0)
        X1, F1, _ = AN.multi_pairs([Ys[jj] for jj in tr_j], 1, TMAX)
        rho = np.stack([((X1 - mu) * (F1[hi] - mu)).sum(0) / np.maximum(((X1 - mu) ** 2).sum(0), 1e-12)
                        for hi in range(nH)])
        fns["ar1"] = lambda Y, ts: mu[None, None] + rho[None] * (Y[ts] - mu)[:, None]

        def ridge_fn(p, kin=False):
            if kin:
                n1 = len(sd)

                def ks(rows_, h):
                    Yr = np.zeros((len(rows_), n1))
                    Yr[:, eidx] = rows_ * sde
                    return AN.kinematic(Yr, h, K)[:, eidx] / sde
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
        for p in ((1, 2) if view == "objects" else (1, 2, 4)):
            fns[f"ridge_p{p}"] = ridge_fn(p)
        if view == "objects":
            fns["kin+ridge_p4"] = ridge_fn(4, kin=True)
        return fns

    def extra(f, Ys, tr_j, fit_j, va_j, te_items):
        t1 = time.time()
        out = {}
        fns = bases(Ys, tr_j, fit_j, va_j)
        out["ar1_rep"] = np.stack([fns["ar1"](Ys[jj], np.array([t]))[0] for jj, i, t in te_items])
        for bn, fn in fns.items():
            coefs = fit_u2(view, Ys, fn, tr_j, L, tye, ntype, sde, HZ, P0)
            Pte = np.stack([fn(Ys[jj], np.array([t]))[0] + u2_corr(L, jj, np.array([t]), coefs, tye, sde, HZ)[0]
                            for jj, i, t in te_items])
            out[f"{bn}+u2"] = Pte
            if info is not None:
                info.append({"fold": f, "name": f"{bn}+u2", "coef_by_h_type": coefs})
        log(f"  local (+u2) fold {f}: {time.time() - t1:.1f} s")
        return out
    return extra


# ----------------------------------------------------------------------------- input-aware nets
def aware_baseline(view, Ys, fit_j, va_j, L, eff, sd, HZ):
    """Per horizon the better of AR(1)+u2 and ridge_p2+u2 on va_j (both fitted on fit_j only).
    Returns base(jj, ts) -> (len(ts), nH, q) and the choice."""
    tmax = max(HZ)
    tye, ntype = view_types(view, eff)
    sde = sd[eff]
    mu = np.concatenate([Ys[jj] for jj in fit_j]).mean(0)
    fns, _ = CL.linear_baselines(Ys, fit_j, va_j, tmax, mu)
    co = {bn: fit_u2(view, Ys, fn, fit_j, L, tye, ntype, sde, HZ) for bn, fn in fns.items()}

    def pred(bn, jj, ts):
        return fns[bn](Ys[jj], ts) + u2_corr(L, jj, ts, co[bn], tye, sde, HZ)
    ev = {}
    for bn in fns:
        e = []
        for jj in va_j:
            ts = np.arange(3, len(Ys[jj]) - tmax)
            F = np.stack([Ys[jj][ts + h] for h in HZ], 1)
            e.append(((pred(bn, jj, ts) - F) ** 2).mean(2))
        ev[bn] = np.concatenate(e).mean(0)
    names = list(fns)
    choose = np.argmin(np.stack([ev[bn] for bn in names]), 0)

    def base(jj, ts):
        Pz = np.stack([pred(bn, jj, ts) for bn in names])
        return np.take_along_axis(Pz, choose[None, None, :, None], 0)[0]
    return base, [names[c] + "+u2" for c in choose], ev


def make_patch_aware_extra(D, L, p=3, rad=2, log=None, info_store=None, **kw):
    """'patchnet+u': closure_lib.make_patch_extra with the wind channels and the aware baseline."""
    G, C3 = 8, 3
    sd_all = np.concatenate(D["Yc"]).std(0)
    eff = sd_all > 1e-6 * max(sd_all.max(), 1e-12)
    assert eff.all()
    sd = np.where(eff, sd_all, 1.0)
    HZ = list(AN.HORIZONS)
    tmax, nH = max(HZ), len(HZ)
    to_grid = lambda Y: Y.reshape(Y.shape[:-1] + (C3, G, G))

    def extra(f, Ys, tr_j, fit_j, va_j, te_items):
        t0 = time.time()
        base, choice, ev = aware_baseline("coarse", Ys, fit_j, va_j, L, eff, sd, HZ)

        def mk(js):
            X, Rs = [], []
            for jj in js:
                Y = Ys[jj]
                ts = np.arange(p - 1, len(Y) - tmax)
                X.append(np.concatenate([CL.patch_features(to_grid(Y), ts, p, rad), L.wind(jj)[ts]], -1).astype(np.float32))
                F = np.stack([Y[ts + h] for h in HZ], 1)
                Rr = to_grid(F - base(jj, ts)).reshape(len(ts), nH, C3, G * G).transpose(0, 3, 1, 2)
                Rs.append(Rr.astype(np.float32))
            return np.concatenate(X), np.concatenate(Rs)
        Xf, Rf = mk(fit_j)
        Xv, Rv = mk(va_j)
        Xte = np.concatenate([np.concatenate([CL.patch_features(to_grid(Ys[jj]), np.array([t]), p, rad),
                                              L.wind(jj)[[t]]], -1) for jj, i, t in te_items])
        Bte = np.concatenate([base(jj, np.array([t])) for jj, i, t in te_items])
        d = Xf.shape[-1]
        kw2 = dict(hidden=64, nblocks=2, batch=1024, steps_per_epoch=60, max_val=40000)
        kw2.update(kw)
        res, info = CL.rmlp_fit_predict(Xf.reshape(-1, d), Rf.reshape(-1, nH, C3), Xv.reshape(-1, d),
                                        Rv.reshape(-1, nH, C3), Xte.reshape(-1, d), log=log, **kw2)
        res = res.reshape(len(te_items), G * G, nH, C3).transpose(0, 2, 3, 1).reshape(len(te_items), nH, C3 * G * G)
        info.update(fold=f, baseline=choice, baseline_val=ev, n_fit_rows=int(len(Xf)), d_in=int(d),
                    seconds=time.time() - t0, n_fit_traj=len(fit_j))
        if info_store is not None:
            info_store.append(info)
        if log:
            log(f"  patchnet+u fold {f}: {time.time() - t0:.1f} s, baseline {choice}")
        return {"patchnet+u": Bte + res, "aware_base": Bte}
    return extra


def make_slot_aware_extra(D, L, p=4, log=None, info_store=None, **kw):
    """'slotnet+u': closure_lib.make_slot_extra with the wind channels and the aware baseline."""
    Kk, NF = 12, CL.LW.NF
    sd_all = np.concatenate(D["Yo"]).std(0)
    eff = sd_all > 1e-6 * max(sd_all.max(), 1e-12)
    sd = np.where(eff, sd_all, 1.0)
    HZ = list(AN.HORIZONS)
    tmax, nH = max(HZ), len(HZ)

    def full(Y_eff):
        out = np.zeros(Y_eff.shape[:-1] + (Kk * NF,))
        out[..., eff] = Y_eff
        return out

    def extra(f, Ys, tr_j, fit_j, va_j, te_items):
        t0 = time.time()
        base, choice, ev = aware_baseline("objects", Ys, fit_j, va_j, L, eff, sd, HZ)
        Zc, Rc = {}, {}

        def views(jj):
            if jj not in Zc:
                Zf = full(Ys[jj])
                Zc[jj] = Zf.reshape(len(Zf), Kk, NF)
                Rc[jj] = (Zf * sd).reshape(len(Zf), Kk, NF)
            return Zc[jj], Rc[jj]

        def feats(jj, ts):
            return np.concatenate([CL.slot_features(*views(jj), ts, p), L.wind(jj)[ts]], -1)

        def mk(js):
            X, Rs = [], []
            for jj in js:
                ts = np.arange(p - 1, len(Ys[jj]) - tmax)
                X.append(feats(jj, ts))
                F = np.stack([full(Ys[jj][ts + h]) for h in HZ], 1)
                Rs.append((F - full(base(jj, ts))).reshape(len(ts), nH, Kk, NF).transpose(0, 2, 1, 3))
            return np.concatenate(X), np.concatenate(Rs)
        Xf, Rf = mk(fit_j)
        Xv, Rv = mk(va_j)
        Xte = np.concatenate([feats(jj, np.array([t])) for jj, i, t in te_items])
        Bte = np.concatenate([base(jj, np.array([t])) for jj, i, t in te_items])
        res, info = CL.rmlp_fit_predict(Xf, Rf, Xv, Rv, Xte, log=log, **kw)
        res = res.transpose(0, 2, 1, 3).reshape(len(te_items), nH, Kk * NF)[..., eff]
        info.update(fold=f, baseline=choice, baseline_val=ev, n_fit=int(len(Xf)), d_in=int(Xf.shape[-1]),
                    seconds=time.time() - t0, n_fit_traj=len(fit_j))
        if info_store is not None:
            info_store.append(info)
        if log:
            log(f"  slotnet+u fold {f}: {time.time() - t0:.1f} s, baseline {choice}")
        return {"slotnet+u": Bte + res, "aware_base": Bte}
    return extra


# ----------------------------------------------------------------------------- exam effect (copied)
def exam_effect(det, klass, aware_names, nH):
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
        d6 = np.stack([err[a_by_h[hi]][sel, hi] - err[b_by_h[hi]][sel, hi] for hi in range(nH)], 1)
        dl = []
        for hi in range(nH):
            ya, yb = preds[a_by_h[hi]][sel, hi], preds[b_by_h[hi]][sel, hi]
            F = FUT[sel, :, hi]
            dl.append((((F - ya[:, None]) ** 2).sum(-1) - ((F - yb[:, None]) ** 2).sum(-1)) / q)
        dl = np.stack(dl, 2)
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
    progs = klass != "none"
    ar = (klass == "aimed") | (klass == "regional")
    res["best_vs_best"] = {"all": pair(best_blind, best_all, allm)}
    for kl in wr.CLASSES:
        res["best_vs_best"][kl] = pair(best_blind, best_all, klass == kl)
    res["best_vs_best"]["programs_only"] = pair(best_blind, best_all, progs)
    res["best_vs_best"]["aimed_regional"] = pair(best_blind, best_all, ar)
    fixed = {}
    for nm in aware_names:
        if nm.endswith("+u2"):
            b = nm[:-3]
        elif nm in ("patchnet+u", "slotnet+u"):
            b = nm[:-2]
        else:
            continue
        if b not in err:
            continue
        masks = {"all": allm, "aimed_regional": ar, "programs": progs}
        fixed[f"{b} vs {nm}"] = {kl: pair([b] * nH, [nm] * nH, masks.get(kl, klass == kl))
                                 for kl in ("all", "programs", "aimed_regional") + wr.CLASSES}
    res["fixed_pairs"] = fixed
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


def twin_effect(det, Bn_std, klass, Vbest, R_TWIN=3):
    """True mean program effect per item from the no-input twins (branch keys 0..2 = FUT replicates 1..3)."""
    FUT = det["FUT"]
    q = FUT.shape[3]
    sel = klass != "none"
    out = {}
    Pm = FUT[:, 1:1 + R_TWIN]
    Dl = Pm - Bn_std
    crn = ((Dl.mean(1) ** 2).sum(-1) - Dl.var(1, ddof=1).sum(-1) / R_TWIN) / q
    unp = ((((FUT.mean(1) - Bn_std.mean(1)) ** 2).sum(-1) - FUT.var(1, ddof=1).sum(-1) / FUT.shape[1]
            - Bn_std.var(1, ddof=1).sum(-1) / R_TWIN) / q)
    crn = np.where(sel[:, None], crn, 0.0)               # 'none' twins duplicate branches 1..3: effect 0
    for kl in wr.CLASSES[1:] + ("programs",):
        s = sel if kl == "programs" else klass == kl
        out[kl] = {"n": int(s.sum()), "crn_effect_over_Vbest": np.nanmean(crn[s], 0) / Vbest,
                   "crn_effect_se_over_Vbest": np.nanstd(crn[s], 0, ddof=1) / math.sqrt(s.sum()) / Vbest,
                   "unpaired_effect_over_Vbest": np.nanmean(unp[s], 0) / Vbest,
                   "unpaired_effect_se_over_Vbest": np.nanstd(unp[s], 0, ddof=1) / math.sqrt(s.sum()) / Vbest,
                   "share_items_crn_ge_0.1Vbest": (crn[s] >= 0.1 * Vbest).mean(0)}
    Dm = np.where(sel[:, None, None], Dl.mean(1), 0.0)
    proj = np.einsum("nrhq,nhq->nrh", FUT - FUT.mean(1, keepdims=True), Dm)
    noise1 = 4.0 * (proj ** 2).sum(1) / (FUT.shape[1] - 1) / q ** 2
    e = crn
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


# ----------------------------------------------------------------------------- energy scores
def es_per_truth(X, Y, chunk=64):
    """Fair energy score (RMS norm) of ensembles X (n, m, d) at truths Y (n, R, d) -> (n, R)."""
    n, m, d = X.shape
    out = np.zeros((n, Y.shape[1]))
    for a in range(0, n, chunk):
        x, y = X[a:a + chunk], Y[a:a + chunk]
        xx = (x ** 2).sum(-1)
        yy = (y ** 2).sum(-1)
        dxy = np.sqrt(np.maximum(xx[:, :, None] + yy[:, None, :] - 2 * np.einsum("nmd,nrd->nmr", x, y), 0.0))
        dxx = np.sqrt(np.maximum(xx[:, :, None] + xx[:, None, :] - 2 * np.einsum("nmd,nkd->nmk", x, x), 0.0))
        out[a:a + chunk] = (dxy.mean(1) - (dxx.sum((1, 2)) / (2.0 * m * (m - 1)))[:, None]) / math.sqrt(d)
    return out


def es_loo(Y):
    """Leave-one-out fair energy score of the replicate truths Y (n, R, d) -> (n, R) (vw.scoring.energy_loo
    per truth)."""
    n, R, d = Y.shape
    out = np.zeros((n, R))
    for r in range(R):
        others = np.delete(Y, r, 1)
        out[:, r] = es_per_truth(others, Y[:, r:r + 1])[:, 0]
    return out


def residual_draws(item_fold, R, m=32, seed=0):
    """For each item, m (item, replicate) residual indices from items of other folds (fixed seed)."""
    rng = np.random.default_rng(seed)
    n = len(item_fold)
    draws = np.zeros((n, m, 2), int)
    for a in range(n):
        pool = np.flatnonzero(item_fold != item_fold[a])
        draws[a, :, 0] = rng.choice(pool, m, replace=True)
        draws[a, :, 1] = rng.integers(0, R, m)
    return draws


def es_all(det, item_fold, names=None, m=32, seed=0):
    """ES per (predictor, item, truth, horizon) for residual-pool ensembles; plus the LOO oracle."""
    FUT, preds = det["FUT"], det["preds"]
    n, R, nH, q = FUT.shape
    draws = residual_draws(item_fold, R, m, seed)
    names = list(preds) if names is None else names
    S = {}
    for nm in names:
        P = preds[nm]
        s = np.zeros((n, R, nH))
        for hi in range(nH):
            E = FUT[:, :, hi] - P[:, None, hi]                       # (n, R, q)
            Xe = P[:, None, hi] + E[draws[..., 0], draws[..., 1]]    # (n, m, q)
            s[:, :, hi] = es_per_truth(Xe, FUT[:, :, hi])
        S[nm] = s
    S["oracle_loo"] = np.stack([es_loo(FUT[:, :, hi]) for hi in range(nH)], 2)
    return S, draws


def es_pair(Sa, Sb, sel, Vref=None):
    """Loss of a vs b in ES per item (mean over truths) and per truth; z at n items and R truths."""
    dl = (Sa - Sb)[sel]                                           # (n, R, nH)
    d = dl.mean(1)
    R = dl.shape[1]
    sn2 = dl.var(1, ddof=1).mean(0)
    sb2 = np.maximum(d.var(0, ddof=1) - sn2 / R, 0.0)
    r = {"n_items": int(sel.sum()), "loss_mean": d.mean(0), "loss_se": d.std(0, ddof=1) / math.sqrt(sel.sum()),
         "var_between_items": sb2, "var_truth_noise_single": sn2}
    if Vref is not None:
        r["loss_over_ref"] = d.mean(0) / Vref
    for n_ in (32, 64, 128):
        for Rr in (1, 6, 16):
            r[f"z_n{n_}_R{Rr}"] = d.mean(0) / np.sqrt((sb2 + sn2 / Rr) / n_)
    return r


def ideal_es(FUT, Bn_std, klass, truths=(0, 4, 5)):
    """Ideal contrast in ES: blind = the no-input twins as the ensemble, aware = the other program replicates;
    scored on the replicates whose keys no twin shares. -> (n, len(truths), nH) per-truth differences."""
    n, R, nH, q = FUT.shape
    out = np.zeros((n, len(truths), nH))
    for hi in range(nH):
        for k, r in enumerate(truths):
            others = np.delete(FUT[:, :, hi], r, 1)
            sa = es_per_truth(others, FUT[:, r:r + 1, hi])[:, 0]
            sb = es_per_truth(Bn_std[:, :, hi], FUT[:, r:r + 1, hi])[:, 0]
            out[:, k, hi] = sb - sa
    out[klass == "none"] = 0.0
    return out
