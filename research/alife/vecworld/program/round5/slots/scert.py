"""scert -- CPU certification worker of the round-5 study `slots` (see s5.py). Several run in parallel.

usage: python -B scert.py WORKER_ID
Claims latent files $S5_WORK/lat/<phi>__cert<h>.npz (atomic rename of the .ready marker; references first) and
judges each Phi on its own coordinates with one fixed predictor family (per-coordinate standardisation, 4 folds by
trajectory, branch futures at h = 1, 2, 4, 8, 16; closure_lib.closure_ext, the VW-0 estimator):
  G   mean, persistence, AR(1), ridge on 1 / 2 / 4 / 8 lags, kNN                         (every Phi)
  S   G + 'sridge' + 'setnet': the family for slot sets, permutation-equivariant, the same for every slot Phi:
      sridge  one linear rule shared by the slots (own 2 lags + the mean of the other slots' 2 lags)
      setnet  one residual network shared by the slots: own 4 lags, one attention layer over the other slots,
              zero-initialised output on top of the better of AR(1) / ridge_p2 per horizon, early stopping on
              held-out trajectories, 2 seeds averaged
  O   S + 'kinematic', 'kin+ridge_p4', 'slotnet' (closure_lib; they read the tracker's 12-number layout)
                                                                                         (moment-layout Phi only)
  GL  G + 'lridge' (local ridge on the 8 x 8 grid; block views only)
Predictable content: Gaussian log-det measures as round4/bias (I_avail, I_capt per family) and per-coordinate error
tables (for the diagonal version, pooled in scombine).
Agreement with the tracker (base trajectories of the certification half; slot Phi with masks): slots are matched to
the tracker's present objects per frame by assignment on shared matter (soft masks); mass / position / velocity R^2
of the matched slot's mask moments ("direct") and of cross-validated probes from the matched slot's certified
numbers at 2 lags (linear ridge; ridge on random Fourier features); recall, precision, matter-weighted ARI of the
hard segmentation, slots per object, identity persistence, and recall / precision by ticks since the object's last
fusion / fission.
-> $S5_WORK/cert/<stem>.npz, <stem>.json; JSON also in $S5_OUT/cert/, per-item errors in $S5_OUT/items/.
"""
import glob
import json
import math
import os
import sys
import time
import traceback

import numpy as np
from scipy.optimize import linear_sum_assignment

import s5

CL, LP = s5.setup_paths(closure=True)
AN = CL.AN
WID = sys.argv[1] if len(sys.argv) > 1 else "0"
DATA = s5.work_dir("data")
LAT = s5.work_dir("lat")
CERT = s5.work_dir("cert")
OUTC = s5.out_dir("cert")
OUTI = s5.out_dir("items")
T0 = time.time()
K, NPIX = s5.K, s5.NPIX
E = NPIX / (2 * np.pi)
LAMS = (1e-4, 1e-2, 1.0, 1e2)
FAM_G = list(LP.FAM_G)
TINY = s5.SIZE in ("tiny", "dev")
NET_KW = dict(epochs=3, seeds=(0,), batch=32) if TINY else dict(epochs=300, seeds=(0, 1), batch=256)


def log(*a):
    s5.progress(f"[scert {WID} {time.time() - T0:7.1f}s] " + " ".join(str(x) for x in a))


def mi(d):
    return (d + NPIX / 2) % NPIX - NPIX / 2


# ----------------------------------------------------------------------------- the slot-set family
def _full(eff, d):
    idx = np.flatnonzero(eff)

    def full(Y):
        out = np.zeros(Y.shape[:-1] + (K * d,))
        out[..., idx] = Y
        return out.reshape(Y.shape[:-1] + (K, d))
    return full


def make_sridge(d, eff, p=2):
    """'sridge': each slot's change at every horizon from its own p lags and the mean of the other slots' p lags,
    one ridge shared by all slots (penalty chosen on the validation trajectories, refitted on all training ones)."""
    HZ = list(s5.HZ)
    tmax, nH = max(HZ), len(HZ)
    full = _full(eff, d)

    def feats(Yf, ts):
        own = np.concatenate([Yf[ts - l] for l in range(p)], -1)
        oth = (own.sum(1, keepdims=True) - own) / (K - 1)
        return np.concatenate([own, oth], -1)

    def extra(f, Ys, tr_j, fit_j, va_j, te_items):
        def mk(js):
            X, T = [], []
            for jj in js:
                Yf = full(Ys[jj])
                ts = np.arange(p - 1, len(Yf) - tmax)
                X.append(feats(Yf, ts).reshape(-1, 2 * p * d))
                T.append(np.stack([(Yf[ts + h] - Yf[ts]).reshape(-1, d) for h in HZ], 0))
            return np.concatenate(X), np.concatenate(T, 1)
        Xf, Tf = mk(fit_j)
        Xv, Tv = mk(va_j)
        rg = AN.Ridge().fit(Xf, list(Tf), Xv, list(Tv))
        X, T = mk(tr_j)
        rg = AN.Ridge().fit(X, list(T), lams=rg.lams)
        out = []
        for jj, i, t in te_items:
            Yf = full(Ys[jj])
            x = feats(Yf, np.array([t]))[0]
            out.append(np.stack([(Yf[t] + rg.predict(x, hi)).reshape(-1)[eff] for hi in range(nH)]))
        return {"sridge": np.stack(out)}
    return extra


def setnet_fit_predict(Xf, Rf, Xv, Rv, Xte, hidden=96, lr=1e-3, wd=1e-4, epochs=300, patience=25, batch=256,
                       seeds=(0, 1), max_val=4000):
    """Residual set network. X (N, K, d_in) own-lag inputs; R (N, K, nH, q) residual targets. One attention layer
    over the other slots; zero-initialised output; per-horizon early stopping on (Xv, Rv); seed average.
    The training loop is closure_lib.rmlp_fit_predict's."""
    import jax
    import jax.numpy as jnp
    if len(Xv) > max_val:
        iv = np.random.default_rng(7).choice(len(Xv), max_val, replace=False)
        Xv, Rv = Xv[iv], Rv[iv]
    N, Kk, din = Xf.shape
    nH, q = Rf.shape[-2:]
    mx, sx = Xf.reshape(-1, din).mean(0), np.maximum(Xf.reshape(-1, din).std(0), 0.1)
    w_h = 1.0 / np.maximum((Rf ** 2).reshape(-1, nH, q).mean((0, 2)), 1e-6)
    f32 = lambda a: jnp.asarray(a, jnp.float32)
    Zf, Zv, Zt = f32((Xf - mx) / sx), f32((Xv - mx) / sx), f32((Xte - mx) / sx)
    Tf, Tv = f32(Rf.reshape(Rf.shape[:-2] + (-1,))), f32(Rv.reshape(Rv.shape[:-2] + (-1,)))
    wq = f32(np.repeat(w_h, q))
    H = hidden
    eye = jnp.eye(Kk, dtype=jnp.float32)

    def init(key):
        ks = jax.random.split(key, 8)
        nrm = lambda k, a, b, g: jax.random.normal(k, (a, b), jnp.float32) * math.sqrt(g / a)
        return {"W0": nrm(ks[0], din, H, 2.0), "b0": jnp.zeros(H, jnp.float32),
                "Wq": nrm(ks[1], H, H, 1.0), "Wk": nrm(ks[2], H, H, 1.0), "Wv": nrm(ks[3], H, H, 1.0),
                "W1": nrm(ks[4], 2 * H, H, 2.0), "b1": jnp.zeros(H, jnp.float32),
                "W2": nrm(ks[5], H, H, 0.5), "b2": jnp.zeros(H, jnp.float32),
                "Wo": jnp.zeros((H, nH * q), jnp.float32), "bo": jnp.zeros(nH * q, jnp.float32)}

    def fwd(P, z):
        e = jax.nn.gelu(z @ P["W0"] + P["b0"])
        u = (e - e.mean(-1, keepdims=True)) / (e.std(-1, keepdims=True) + 1e-5)
        a = jnp.einsum("...kh,...jh->...kj", u @ P["Wq"], u @ P["Wk"]) / math.sqrt(H) - 1e9 * eye
        m = jax.nn.softmax(a, -1) @ (u @ P["Wv"])
        h = e + jax.nn.gelu(jnp.concatenate([u, m], -1) @ P["W1"] + P["b1"]) @ P["W2"] + P["b2"]
        return h @ P["Wo"] + P["bo"]

    def loss(P, z, t):
        return (((fwd(P, z) - t) ** 2) * wq).mean()

    @jax.jit
    def step(P, M, V, it, z, t):
        g = jax.grad(loss)(P, z, t)
        M = jax.tree_util.tree_map(lambda m, gg: 0.9 * m + 0.1 * gg, M, g)
        V = jax.tree_util.tree_map(lambda v, gg: 0.999 * v + 0.001 * gg * gg, V, g)
        c1, c2 = 1 - 0.9 ** it, 1 - 0.999 ** it
        P = jax.tree_util.tree_map(lambda p, m, v: p - lr * ((m / c1) / (jnp.sqrt(v / c2) + 1e-8) +
                                                             (wd * p if p.ndim == 2 else 0.0)), P, M, V)
        return P, M, V

    @jax.jit
    def val_by_h(P, z, t):
        return ((fwd(P, z) - t) ** 2).reshape(-1, nH, q).mean((0, 2))

    fwd_j = jax.jit(fwd)
    pred_sum = np.zeros((len(Xte), Kk, nH * q))
    info = {"best_epoch": [], "val_gain": []}
    for s in seeds:
        rng = np.random.default_rng(2000 + s)
        P = init(jax.random.PRNGKey(100 + s))
        M = jax.tree_util.tree_map(jnp.zeros_like, P)
        V = jax.tree_util.tree_map(jnp.zeros_like, P)
        v0 = np.asarray(val_by_h(P, Zv, Tv))
        best = v0.copy()
        snap = [P] * nH
        best_ep = np.zeros(nH, int)
        bad, it = 0, 0
        for ep in range(1, epochs + 1):
            perm = rng.permutation(N)
            for b0 in range(0, N - batch + 1, batch):
                ib = perm[b0:b0 + batch]
                it += 1
                P, M, V = step(P, M, V, float(it), Zf[ib], Tf[ib])
            vh = np.asarray(val_by_h(P, Zv, Tv))
            imp = vh < best * (1 - 1e-4)
            for h in np.flatnonzero(imp):
                best[h], snap[h], best_ep[h] = vh[h], P, ep
            bad = 0 if imp.any() else bad + 1
            if bad >= patience:
                break
        out = np.zeros((len(Xte), Kk, nH * q))
        cache = {}
        for h in range(nH):
            k = id(snap[h])
            if k not in cache:
                cache[k] = np.asarray(fwd_j(snap[h], Zt))
            out[..., h * q:(h + 1) * q] = cache[k][..., h * q:(h + 1) * q]
        pred_sum += out
        info["best_epoch"].append(best_ep.tolist())
        info["val_gain"].append((1 - best / np.maximum(v0, 1e-30)).tolist())
    return (pred_sum / len(seeds)).reshape(len(Xte), Kk, nH, q), info


def make_setnet(d, eff, p=4, info_store=None, **kw):
    """'setnet' hook for closure_ext: the residual of the per-horizon better of AR(1) / ridge_p2 (fit trajectories
    only, as closure_lib's slotnet), predicted slot by slot by setnet_fit_predict."""
    HZ = list(s5.HZ)
    tmax, nH = max(HZ), len(HZ)
    full = _full(eff, d)

    def extra(f, Ys, tr_j, fit_j, va_j, te_items):
        t0 = time.time()
        mu = np.concatenate([Ys[jj] for jj in fit_j]).mean(0)
        fns, ev = CL.linear_baselines(Ys, fit_j, va_j, tmax, mu)
        choose = np.where(ev["ar1"] <= ev["ridge_p2"], 0, 1)

        def base(Y, ts):
            A, Rr = fns["ar1"](Y, ts), fns["ridge_p2"](Y, ts)
            return np.where(choose[None, :, None] == 0, A, Rr)

        def own(Yf, ts):
            return np.concatenate([Yf[ts - l] for l in range(p)], -1)                       # (n, K, p d)

        def mk(js):
            X, Rs = [], []
            for jj in js:
                Yf = full(Ys[jj])
                ts = np.arange(p - 1, len(Yf) - tmax)
                X.append(own(Yf, ts))
                Fu = np.stack([Ys[jj][ts + h] for h in HZ], 1)                              # (n, nH, q_eff)
                Rs.append(full(Fu - base(Ys[jj], ts)).transpose(0, 2, 1, 3))                # (n, K, nH, d)
            return np.concatenate(X), np.concatenate(Rs)
        Xf, Rf = mk(fit_j)
        Xv, Rv = mk(va_j)
        Xte = np.concatenate([own(full(Ys[jj]), np.array([t])) for jj, i, t in te_items])
        Bte = np.concatenate([base(Ys[jj], np.array([t])) for jj, i, t in te_items])
        res, info = setnet_fit_predict(Xf, Rf, Xv, Rv, Xte, **kw)                           # (n, K, nH, d)
        res = res.transpose(0, 2, 1, 3).reshape(len(te_items), nH, K * d)[..., eff]
        info.update(fold=f, baseline=["ar1" if c == 0 else "ridge_p2" for c in choose], n_fit=len(Xf), seconds=time.time() - t0)
        if info_store is not None:
            info_store.append(info)
        return {"setnet": Bte + res}
    return extra


FAMILIES = {"trk": {"G": FAM_G, "S": FAM_G + ["sridge", "setnet"],
                    "O": FAM_G + ["sridge", "setnet", "kinematic", "kin+ridge_p4", "slotnet"]},
            "sub": {"G": FAM_G, "S": FAM_G + ["sridge", "setnet"]},
            "code": {"G": FAM_G, "S": FAM_G + ["sridge", "setnet"]},
            "grid": {"G": FAM_G, "GL": FAM_G + ["lridge"]}}


def _logdet(S, dof):
    """Wishart-corrected log det (vw.certificates.logdet); None when the scatter is singular or dof <= q."""
    q = S.shape[0]
    if dof <= q + 1:
        return None
    v = LP.logdet(S, dof)
    return v if np.isfinite(v) else None


def certify(Zt, ZB, layout, d, gshape=None):
    """One certification half: Zt (JC, T+1, q), ZB (JC, nT, R, TB, q). Per-item errors of every predictor, the
    oracle, per-coordinate error tables and the Gaussian log-det measures per family."""
    AN.HORIZONS = list(s5.HZ)
    J = Zt.shape[0]
    Ys, Bs = [Zt[j] for j in range(J)], [ZB[j] for j in range(J)]
    D = {"Yc": Ys, "Bc": Bs, "Yo": Ys, "Bo": Bs, "st_tick": [np.array(s5.TEST) for _ in range(J)], "j": list(range(J))}
    sd = np.concatenate(Ys).std(0)
    eff = sd > 1e-6 * max(sd.max(), 1e-12)
    hooks, store = [], {"setnet": [], "slotnet": []}
    if layout in ("trk", "sub", "code"):
        hooks += [make_sridge(d, eff), make_setnet(d, eff, info_store=store["setnet"], **NET_KW)]
    if layout == "trk":
        hooks.append(CL.make_slot_extra(D, info_store=store["slotnet"], **NET_KW))
    if layout == "grid" and bool(eff.all()):
        hooks.append(LP.make_lridge(gshape))
    out, det = CL.closure_ext(D, "objects" if layout == "trk" else "coarse", K=K, mlp=False,
                              extra=CL.combine(*hooks) if hooks else None)
    err, orac, FUT, preds = det["err"], det["orac"], det["FUT"], det["preds"]
    n, R, nH, q = FUT.shape
    Do = FUT - FUT.mean(1, keepdims=True)
    Vc = {nm: ((FUT - P[:, None]) ** 2).mean((0, 1)) for nm, P in preds.items()}          # (nH, q) per coordinate
    Vc_or = (Do ** 2).sum((0, 1)) / (n * (R - 1))
    ld = {}
    So = np.einsum("nrhi,nrhj->hij", Do, Do) / (n * (R - 1))
    S_of = lambda P: np.einsum("nrhi,nrhj->hij", FUT - P[:, None], FUT - P[:, None]) / (n * R)
    Sm = S_of(preds["mean"])
    l_or = [_logdet(So[hi], n * (R - 1)) for hi in range(nH)]
    l_mean = [_logdet(Sm[hi], n * R) for hi in range(nH)]
    half = lambda a, b: None if (a is None or b is None) else 0.5 * (a - b)
    ld["I_avail"] = [half(l_mean[hi], l_or[hi]) for hi in range(nH)]
    V = {nm: e.mean(0) for nm, e in err.items()}
    for fam, names in FAMILIES[layout].items():
        names = [nm for nm in names if nm in V]
        bn = [min(names, key=lambda nm: V[nm][hi]) for hi in range(nH)]
        Sb = {nm: S_of(preds[nm]) for nm in set(bn)}
        l_best = [_logdet(Sb[bn[hi]][hi], n * R) for hi in range(nH)]
        ld[f"I_capt_{fam}"] = [half(l_mean[hi], l_best[hi]) for hi in range(nH)]
        ld[f"best_{fam}"] = bn
    names = sorted(err)
    return {"names": names, "err": np.stack([err[nm] for nm in names]), "orac": orac, "item_j": det["item_j"],
            "Vc": np.stack([Vc[nm] for nm in names]), "Vc_orac": Vc_or, "eff": eff, "ld": ld,
            "n_eff": int(out["n_eff_coords"]), "q": int(Zt.shape[-1]),
            "net_info": {k: [{kk: i[kk] for kk in ("best_epoch", "val_gain", "seconds") if kk in i} for i in v]
                         for k, v in store.items() if v}}


# ----------------------------------------------------------------------------- agreement with the tracker
def cv_ridge(X, Y, groups, lams=LAMS):
    """Cross-validated ridge of Y on X (X standardised, folds = groups); per-column R^2 at the pooled-best penalty."""
    s = X.std(0)
    keep = s > 1e-9 * max(float(s.max()), 1e-30)
    if not keep.any():
        return np.zeros(Y.shape[1]), None
    X = (X[:, keep] - X[:, keep].mean(0)) / s[keep]
    sse = np.zeros((len(lams), Y.shape[1]))
    sst = np.zeros(Y.shape[1])
    for f in np.unique(groups):
        tr, te = groups != f, groups == f
        if not tr.any() or not te.any():
            continue
        mx, my = X[tr].mean(0), Y[tr].mean(0)
        Xc = X[tr] - mx
        ev, U = np.linalg.eigh(Xc.T @ Xc)
        UB = U.T @ (Xc.T @ (Y[tr] - my))
        Xt = (X[te] - mx) @ U
        for i, lam in enumerate(lams):
            Pd = Xt @ (UB / (ev + lam * tr.sum())[:, None]) + my
            sse[i] += ((Y[te] - Pd) ** 2).sum(0)
        sst += ((Y[te] - my) ** 2).sum(0)
    i = int(np.argmin(sse.sum(1)))
    return 1 - sse[i] / np.maximum(sst, 1e-30), lams[i]


def rff(X, n=300, seed=0):
    """Random Fourier features of standardised X (RBF kernel, bandwidth = sqrt(dim))."""
    s = X.std(0)
    keep = s > 1e-9 * max(float(s.max()), 1e-30)
    Xs = (X[:, keep] - X[:, keep].mean(0)) / s[keep]
    rng = np.random.default_rng(seed)
    W = rng.standard_normal((Xs.shape[1], n)) / math.sqrt(max(Xs.shape[1], 1))
    b = rng.uniform(0, 2 * np.pi, n)
    return np.concatenate([Xs, np.cos(Xs @ W + b)], 1)


BINS = ((0, 0), (1, 1), (2, 3), (4, 7), (8, 15), (16, 10 ** 6))


def agreement(MM, OS, OH, TAB, Zt, d):
    """Base trajectories of one certification half. MM (J, T+1, K, 14), OS / OH (J, T+1, K, 13), TAB (J, T+1, K, 17)
    tracker table, Zt (J, T+1, K * d) certified readout."""
    J, T1 = MM.shape[:2]
    Zs = Zt.reshape(J, T1, K, d)
    pres = TAB[..., 0] > 0.5
    ev, uid = TAB[..., 15], TAB[..., 16]
    # ticks since the slot's last event and that event's type
    since = np.zeros((J, T1, K), int)
    last = np.zeros((J, T1, K), int)
    for t in range(T1):
        e = ev[:, t] != 0
        if t == 0:
            since[:, 0], last[:, 0] = np.where(e, 0, 99), np.where(e, ev[:, 0], 0)
        else:
            same = pres[:, t] & pres[:, t - 1] & (uid[:, t] == uid[:, t - 1])
            since[:, t] = np.where(e, 0, np.where(same, since[:, t - 1] + 1, 0))
            last[:, t] = np.where(e, ev[:, t], np.where(same, last[:, t - 1], 0))
    rows = []          # per matched pair: j, t, s, k, recall, precision
    match = -np.ones((J, T1, K), int)
    ari, spo, ops = [], [], []
    for j in range(J):
        for t in range(T1):
            cols = np.flatnonzero(pres[j, t])
            O = OS[j, t]
            if cols.size:
                r, c = linear_sum_assignment(-O[:, 1:][:, cols])
                for rr, cc in zip(r, c):
                    s = cols[cc]
                    tot_s = O[:, 1 + s].sum()
                    rows.append((j, t, s, rr, O[rr, 1 + s] / max(tot_s, 1e-9), O[rr, 1 + s] / max(O[rr].sum(), 1e-9)))
                    match[j, t, s] = rr
                Oc = O[:, 1:][:, cols]
                w = Oc.sum(0)
                spo.append(float((w * (w ** 2 / np.maximum((Oc ** 2).sum(0), 1e-12))).sum() / max(w.sum(), 1e-9)))
                wk = Oc.sum(1)
                big = wk > s5.M_MIN
                if big.any():
                    ops.append(float((wk[big] * (wk[big] ** 2 / np.maximum((Oc[big] ** 2).sum(1), 1e-12))).sum() / wk[big].sum()))
            n = OH[j, t][:, 1:]
            a, b, N = n.sum(1), n.sum(0), n.sum()
            if N > 0:
                ex = (a ** 2).sum() * (b ** 2).sum() / N ** 2
                den = 0.5 * ((a ** 2).sum() + (b ** 2).sum()) - ex
                ari.append(float(((n ** 2).sum() - ex) / den) if den > 1e-9 else 1.0)
    rows = np.array(rows)
    jj, tt, ss, kk = (rows[:, i].astype(int) for i in range(4))
    rec, prec = rows[:, 4], rows[:, 5]
    out = {"n_pairs": int(len(rows)), "recall": float(rec.mean()), "precision": float(prec.mean()),
           "clean_match_rate(recall,precision>=0.9)": float(((rec >= 0.9) & (prec >= 0.9)).mean()),
           "ari_hard_matter_weighted": float(np.mean(ari)), "slots_per_object": float(np.mean(spo)),
           "objects_per_slot": float(np.mean(ops)) if ops else None}
    # direct agreement of the matched slot's mask moments
    m_s, m_k = TAB[jj, tt, ss, 1], MM[jj, tt, kk, 1]
    cy_s, cx_s = TAB[jj, tt, ss, 12], TAB[jj, tt, ss, 13]
    cy_k, cx_k = MM[jj, tt, kk, 12], MM[jj, tt, kk, 13]
    dist = np.hypot(mi(cy_k - cy_s), mi(cx_k - cx_s))
    r2 = lambda a, b: float(1 - ((a - b) ** 2).sum() / max(((b - b.mean(0)) ** 2).sum(), 1e-30))
    out["direct"] = {"mass_R2": r2(m_k, m_s), "mass_corr2": float(np.corrcoef(m_k, m_s)[0, 1] ** 2),
                     "pos_err_px_median": float(np.median(dist)), "pos_err_px_mean": float(dist.mean()),
                     "pos_R2": float(1 - (dist ** 2).mean() / (2 * NPIX ** 2 / 12))}
    okv = (tt >= 1) & (ev[jj, tt, ss] == 0) & (since[jj, tt, ss] >= 1)
    tp = np.maximum(tt - 1, 0)
    v_k = np.stack([mi(MM[jj, tt, kk, 13] - MM[jj, tp, kk, 13]), mi(MM[jj, tt, kk, 12] - MM[jj, tp, kk, 12])], 1)
    v_s = TAB[jj, tt, ss, 10:12]
    out["direct"]["vel_R2"] = r2(v_k[okv], v_s[okv])
    out["direct"]["n_vel"] = int(okv.sum())
    # identity persistence: the matched slot of a continuing, event-free object stays the same
    cont = (tt >= 1) & (ev[jj, tt, ss] == 0) & (uid[jj, tt, ss] == uid[jj, tp, ss]) & pres[jj, tp, ss]
    out["identity_persistence"] = float((match[jj, tt, ss] == match[jj, tp, ss])[cont].mean()) if cont.any() else None
    # probes from the matched slot's certified numbers (2 lags)
    X = np.concatenate([Zs[jj, tt, kk], Zs[jj, tp, kk]], 1)[okv]
    tgt = np.column_stack([m_s, TAB[jj, tt, ss, 3], TAB[jj, tt, ss, 4], TAB[jj, tt, ss, 5], TAB[jj, tt, ss, 6], v_s])[okv]
    g = (jj % 4)[okv]
    if len(X) > 50:
        sub = np.random.default_rng(0).choice(len(X), min(len(X), 40000), replace=False)
        for nm, F in (("probe_linear", X[sub]), ("probe_rff", rff(X[sub]))):
            R2, lam = cv_ridge(F, tgt[sub], g[sub])
            out[nm] = {"mass_R2": float(R2[0]), "pos_R2": float(R2[1:5].mean()), "vel_R2": float(R2[5:7].mean()), "lam": lam,
                       "n": int(len(sub))}
    # recall / precision by ticks since the last fusion (3) / fission (2) of the object
    by = {}
    sn, lt = since[jj, tt, ss], last[jj, tt, ss]
    for nm, code in (("fusion", 3), ("fission", 2)):
        by[nm] = []
        for lo, hi in BINS:
            sel = (lt == code) & (sn >= lo) & (sn <= hi)
            by[nm].append({"ticks": [lo, hi], "n": int(sel.sum()), "recall": float(rec[sel].mean()) if sel.any() else None,
                           "precision": float(prec[sel].mean()) if sel.any() else None})
    out["by_ticks_since_event"] = by
    return out


def nontriv(Zt):
    Jn, T, q = Zt.shape
    Z = Zt.reshape(-1, q)
    s = Z.std(0)
    keep = s > 1e-9 * max(float(s.max()), 1e-30)
    r_dyn = float(np.mean(Zt[..., keep].var(1).mean(0) / Z[:, keep].var(0)))
    C = np.corrcoef(Z[:, keep].T) if keep.sum() > 1 else np.ones((1, 1))
    evs = np.clip(np.linalg.eigvalsh(np.atleast_2d(C)), 0, None)
    return {"r_dyn": r_dyn, "participation_ratio": float(evs.sum() ** 2 / (evs ** 2).sum()), "n_nonconst": int(keep.sum())}


def territory(MM):
    """How territorial the slots are: mean resultant length of each slot's mask centroid over all frames (1 = the
    slot never leaves one place, 0 = it roams the whole torus), mass-gated; and the mean slot speed in px / tick."""
    g = MM[..., 0] > 0.5
    cy, cx = MM[..., 12], MM[..., 13]
    Rl = []
    for k in range(K):
        if g[..., k].sum() < 10:
            continue
        ry = np.abs(np.exp(1j * cy[..., k][g[..., k]] / E).mean())
        rx = np.abs(np.exp(1j * cx[..., k][g[..., k]] / E).mean())
        Rl.append(0.5 * (ry + rx))
    sp = np.hypot(mi(cy[:, 1:] - cy[:, :-1]), mi(cx[:, 1:] - cx[:, :-1]))[g[:, 1:] & g[:, :-1]]
    return {"resultant_length": float(np.mean(Rl)) if Rl else None, "slot_speed_px": float(sp.mean()) if sp.size else None,
            "slots_present_mean": float(g.sum(-1).mean()), "mass_in_present_slots": float(np.where(g, MM[..., 1], 0).sum(-1).mean())}


_TAB = {}


def tracker_table(ch):
    if ch not in _TAB:
        _TAB[ch] = np.load(f"{DATA}/TAB_{ch}.npy")[:s5.J_CERT].astype(np.float64)
    return _TAB[ch]


def process(path):
    t1 = time.time()
    stem = os.path.basename(path)[:-4]
    d = np.load(path)
    meta = json.loads(str(d["meta"]))
    Zt, ZB = d["Zt"].astype(np.float64), d["ZB"].astype(np.float64)
    ch = stem.rsplit("__cert", 1)[1]
    layout = meta["layout"]
    res = {"stem": stem, "meta": meta, "q": int(Zt.shape[-1]), "layout": layout}
    cert = certify(Zt, ZB, layout, int(meta.get("d", 0)), gshape=tuple(meta["gshape"]) if "gshape" in meta else None)
    np.savez_compressed(f"{CERT}/{stem}.npz", names=np.array(cert["names"]), err=cert["err"], orac=cert["orac"],
                        item_j=cert["item_j"], Vc=cert["Vc"], Vc_orac=cert["Vc_orac"], eff=cert["eff"])
    np.savez_compressed(f"{OUTI}/{stem}.npz", names=np.array(cert["names"]), err=cert["err"].astype(np.float32),
                        orac=cert["orac"].astype(np.float32), item_j=cert["item_j"], Vc=cert["Vc"].astype(np.float32),
                        Vc_orac=cert["Vc_orac"].astype(np.float32), eff=cert["eff"])
    res.update(ld=cert["ld"], n_eff=cert["n_eff"], net_info=cert["net_info"])
    t_cert = time.time() - t1
    res["nontriv"] = nontriv(Zt)
    if "MM" in d.files:
        MM, OS, OH = d["MM"].astype(np.float64), d["OS"].astype(np.float64), d["OH"].astype(np.float64)
        res["agreement"] = agreement(MM, OS, OH, tracker_table(ch), Zt, int(meta["d"]))
        res["territory"] = territory(MM)
    elif stem.startswith("trk__"):
        TAB = tracker_table(ch)
        MMt = np.concatenate([TAB[..., :12], TAB[..., 12:14]], -1)
        res["territory"] = territory(MMt)
    res["seconds"] = {"certify": t_cert, "total": time.time() - t1}
    s5.jdump(res, f"{CERT}/{stem}.json")
    s5.jdump(res, f"{OUTC}/{stem}.json")
    return res


def claim():
    """Oldest .ready file, references first; atomic rename to .claimed.<WID>."""
    rd = glob.glob(f"{LAT}/*.npz.ready")
    ref = lambda p: 0 if os.path.basename(p).startswith(("trk", "hand_", "km_", "grid")) else 1
    rd.sort(key=lambda p: (ref(p), os.path.getmtime(p) if os.path.exists(p) else 0))
    for r in rd:
        tgt = r[:-6] + f".claimed.{WID}"
        try:
            os.rename(r, tgt)
            return r[:-6]
        except OSError:
            continue
    return None


def main():
    n = 0
    dl = s5.deadline("cert")
    while True:
        if time.time() > dl:
            log("certification deadline reached; stopping")
            break
        p = claim()
        if p is None:
            if os.path.exists(f"{LAT}/DONE") and not glob.glob(f"{LAT}/*.npz.ready"):
                break
            time.sleep(3)
            continue
        try:
            res = process(p)
            n += 1
            log(f"{res['stem']} q={res['q']} certified in {res['seconds']['total']:.1f}s")
        except Exception as exc:
            log(f"{os.path.basename(p)} FAILED: {exc!r}")
            with open(os.path.join(s5.out_dir(), f"cert_errors_{WID}.txt"), "a") as f:
                f.write(f"{p}\n{traceback.format_exc()}\n")
    log(f"worker exits after {n} items")


if __name__ == "__main__":
    main()
