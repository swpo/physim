"""closure_lib -- fresh closure estimates on VW-1 level-1 data.

closure_ext  integrate/analyze.closure (the VW-0 estimator), copied line for line, with two hooks:
             (1) `extra`: extra level-1 predictors fitted on the same folds and added to the
             best-of set; (2) it also returns the per-item errors, the oracle and the futures,
             so the bootstrap, the selection check and the gap split can use them. With extra=None
             it reproduces analyze.closure exactly (checked in run_closure.py against the
             unmodified analyze.closure, MLP off).
rmlp         a residual MLP in JAX on 4 lags: predicts the residual of a linear baseline
             (per horizon the better of AR(1) and ridge on 2 lags on the validation set), with a
             zero-initialised output layer, per-horizon early stopping on held-out trajectories
             (epoch 0 = the baseline itself) and an average over seeds.
load_data    merges the per-process sim_*.npz files.
"""
import math
import os
import sys
import time

sys.path.insert(0, "/home/user/evalwork/vecworld/vw1/port")
import _paths  # noqa: E402,F401   (puts integrate/ on the path, read only, no bytecode)
import numpy as np  # noqa: E402

import analyze as AN  # noqa: E402   VW-0 estimator code (read only); imports lenia_world for constants only

assert AN.__file__.startswith(_paths.INT_DIR), AN.__file__
LW = AN.LW
RES = "/home/user/evalwork/vecworld/vw1/fresh/closure/results"
N_COARSE = 192


def jsonable(o):
    if isinstance(o, dict):
        return {str(k): jsonable(v) for k, v in o.items()}
    if isinstance(o, (list, tuple)):
        return [jsonable(v) for v in o]
    if isinstance(o, np.ndarray):
        return jsonable(o.tolist())
    if isinstance(o, (np.floating,)):
        return float(o)
    if isinstance(o, (np.integer,)):
        return int(o)
    if isinstance(o, np.bool_):
        return bool(o)
    if isinstance(o, float) and not math.isfinite(o):
        return None
    return o


def load_data(tags=("A", "B"), res=RES):
    parts = [np.load(f"{res}/sim_{t}.npz") for t in tags]
    import json
    metas = [json.load(open(f"{res}/sim_{t}.json")) for t in tags]
    cat = {k: np.concatenate([p[k] for p in parts], 0) for k in ("Y", "TAB", "B", "BTAB", "X")}
    J = cat["Y"].shape[0]
    TEST = metas[0]["test_ticks"]
    assert all(m["test_ticks"] == TEST for m in metas)
    D = {"Yc": [cat["Y"][j, :, :N_COARSE].astype(float) for j in range(J)],
         "Yo": [cat["Y"][j, :, N_COARSE:].astype(float) for j in range(J)],
         "Bc": [cat["B"][j, ..., :N_COARSE].astype(float) for j in range(J)],
         "Bo": [cat["B"][j, ..., N_COARSE:].astype(float) for j in range(J)],
         "st_tick": [np.array(TEST) for _ in range(J)], "j": list(range(J))}
    return D, cat, metas


# ----------------------------------------------------------------------------- residual MLP (JAX)
def _jax():
    import jax
    import jax.numpy as jnp
    return jax, jnp


def rmlp_fit_predict(Xf, Rf, Xv, Rv, Xte, hidden=128, nblocks=2, lr=1e-3, wd=1e-4, epochs=300,
                     patience=25, batch=256, seeds=(0, 1), log=None, steps_per_epoch=None, max_val=None):
    """Fit residual MLPs. X (N, [S...,] d) inputs; R (N, [S...,] nH, q) residual targets (future - baseline);
    optional middle axes S (e.g. object slots) share the weights. Returns predicted residuals for Xte
    (n, [S...,] nH, q) (seed average; per-horizon early stopping on Xv) and a dict of training info."""
    jax, jnp = _jax()
    if max_val is not None and len(Xv) > max_val:                    # fixed random subset for early stopping
        iv = np.random.default_rng(7).choice(len(Xv), max_val, replace=False)
        Xv, Rv = Xv[iv], Rv[iv]
    N, nH, q = Rf.shape[0], Rf.shape[-2], Rf.shape[-1]
    S = Rf.shape[1:-2]
    d = Xf.shape[-1]
    mx, sx = Xf.reshape(-1, d).mean(0), np.maximum(Xf.reshape(-1, d).std(0), 0.1)
    w_h = 1.0 / np.maximum((Rf ** 2).reshape(-1, nH, q).mean((0, 2)), 1e-6)   # equalise horizons in the loss
    f32 = lambda a: jnp.asarray(a, jnp.float32)
    Zf, Zv, Zt = f32((Xf - mx) / sx), f32((Xv - mx) / sx), f32((Xte - mx) / sx)
    Tf, Tv = f32(Rf.reshape(Rf.shape[:-2] + (-1,))), f32(Rv.reshape(Rv.shape[:-2] + (-1,)))
    wq = f32(np.repeat(w_h, q))

    def init(key):
        ks = jax.random.split(key, 2 + 2 * nblocks)
        P = {"W0": jax.random.normal(ks[0], (d, hidden), jnp.float32) * math.sqrt(2.0 / d), "b0": jnp.zeros(hidden, jnp.float32),
             "Wo": jnp.zeros((hidden, nH * q), jnp.float32), "bo": jnp.zeros(nH * q, jnp.float32)}
        for b in range(nblocks):
            P[f"W{b}a"] = jax.random.normal(ks[2 + 2 * b], (hidden, hidden), jnp.float32) * math.sqrt(2.0 / hidden)
            P[f"b{b}a"] = jnp.zeros(hidden, jnp.float32)
            P[f"W{b}b"] = jax.random.normal(ks[3 + 2 * b], (hidden, hidden), jnp.float32) * math.sqrt(0.5 / hidden)
            P[f"b{b}b"] = jnp.zeros(hidden, jnp.float32)
        return P

    def fwd(P, z):
        h = jax.nn.gelu(z @ P["W0"] + P["b0"])
        for b in range(nblocks):
            u = (h - h.mean(-1, keepdims=True)) / (h.std(-1, keepdims=True) + 1e-5)
            h = h + jax.nn.gelu(u @ P[f"W{b}a"] + P[f"b{b}a"]) @ P[f"W{b}b"] + P[f"b{b}b"]
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
        e = ((fwd(P, z) - t) ** 2).reshape(-1, nH, q).mean((0, 2))
        return e

    pred_sum = np.zeros((len(Xte),) + S + (nH * q,))
    info = {"best_epoch": [], "val_gain": []}
    for s in seeds:
        rng = np.random.default_rng(1000 + s)
        P = init(jax.random.PRNGKey(s))
        M = jax.tree_util.tree_map(jnp.zeros_like, P)
        V = jax.tree_util.tree_map(jnp.zeros_like, P)
        v0 = np.asarray(val_by_h(P, Zv, Tv))
        best = v0.copy()
        snap = [P] * nH
        best_ep = np.zeros(nH, int)
        bad, it = 0, 0
        for ep in range(1, epochs + 1):
            perm = rng.permutation(N)
            starts = range(0, N - batch + 1, batch)
            if steps_per_epoch is not None:
                starts = list(starts)[:steps_per_epoch]
            for b0 in starts:
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
        out = np.zeros((len(Xte),) + S + (nH * q,))
        cache = {}
        for h in range(nH):
            k = id(snap[h])
            if k not in cache:
                cache[k] = np.asarray(fwd(snap[h], Zt))
            out[..., h * q:(h + 1) * q] = cache[k][..., h * q:(h + 1) * q]
        pred_sum += out
        info["best_epoch"].append(best_ep.tolist())
        info["val_gain"].append((1 - best / v0).tolist())
        if log:
            log(f"    rmlp seed {s}: epochs {ep}, best epoch per h {best_ep.tolist()}, val gain {np.round(1 - best / v0, 3).tolist()}")
    return (pred_sum / len(seeds)).reshape((len(Xte),) + S + (nH, q)), info


def linear_baselines(Ys, fit_j, va_j, tmax, mu):
    """AR(1) and ridge_p2 fitted on fit_j (ridge lambda on va_j); returns predictor functions
    (Y, ts) -> (len(ts), nH, q) and their validation errors per horizon."""
    nH = len(AN.HORIZONS)
    X1, F1, _ = AN.multi_pairs([Ys[jj] for jj in fit_j], 1, tmax)
    rho = []
    for hi in range(nH):
        a, b = X1 - mu, F1[hi] - mu
        rho.append((a * b).sum(0) / np.maximum((a * a).sum(0), 1e-12))
    rho = np.stack(rho)                                                        # (nH, q)
    Xf, Ff, Y0f = AN.multi_pairs([Ys[jj] for jj in fit_j], 2, tmax)
    Xv, Fv, Y0v = AN.multi_pairs([Ys[jj] for jj in va_j], 2, tmax)
    rg = AN.Ridge().fit(Xf, [Ff[hi] - Y0f for hi in range(nH)], Xv, [Fv[hi] - Y0v for hi in range(nH)])

    def ar1(Y, ts):
        return mu[None, None] + rho[None] * (Y[ts] - mu)[:, None]

    def ridge2(Y, ts):
        x = AN.lag_matrix(Y, ts, 2)
        return np.stack([Y[ts] + rg.predict(x, hi) for hi in range(nH)], 1)
    # validation errors (against the single realised future, same pairs as the ridge's)
    ts_all = [(Y, np.arange(1, len(Y) - tmax)) for Y in (Ys[jj] for jj in va_j)]
    Fv_ = np.concatenate([np.stack([Y[ts + h] for h in AN.HORIZONS], 1) for Y, ts in ts_all])
    ev = {nm: ((np.concatenate([fn(Y, ts) for Y, ts in ts_all]) - Fv_) ** 2).mean((0, 2))
          for nm, fn in (("ar1", ar1), ("ridge_p2", ridge2))}
    return {"ar1": ar1, "ridge_p2": ridge2}, ev


def make_rmlp_extra(p=4, log=None, frac=1.0, info_store=None, **kw):
    """`extra` hook for closure_ext: the residual MLP on p lags, trained on fit_j[:frac]."""
    tmax = max(AN.HORIZONS)
    nH = len(AN.HORIZONS)

    def extra(f, Ys, tr_j, fit_j, va_j, te_items):
        t0 = time.time()
        if frac < 1.0:
            fit_j = fit_j[:max(1, int(round(frac * len(fit_j))))]
        mu = np.concatenate([Ys[jj] for jj in fit_j]).mean(0)
        fns, ev = linear_baselines(Ys, fit_j, va_j, tmax, mu)
        choose = np.where(ev["ar1"] <= ev["ridge_p2"], 0, 1)                  # per horizon

        def base(Y, ts):
            A, Rr = fns["ar1"](Y, ts), fns["ridge_p2"](Y, ts)
            return np.where(choose[None, :, None] == 0, A, Rr)

        def mk(js):
            X, Rs = [], []
            for jj in js:
                Y = Ys[jj]
                ts = np.arange(p - 1, len(Y) - tmax)
                X.append(AN.lag_matrix(Y, ts, p))
                F = np.stack([Y[ts + h] for h in AN.HORIZONS], 1)
                Rs.append(F - base(Y, ts))
            return np.concatenate(X), np.concatenate(Rs)
        Xf, Rf = mk(fit_j)
        Xv, Rv = mk(va_j)
        Xte = np.concatenate([AN.lag_matrix(Ys[jj], np.array([t]), p) for jj, i, t in te_items])
        Bte = np.concatenate([base(Ys[jj], np.array([t])) for jj, i, t in te_items])
        res, info = rmlp_fit_predict(Xf, Rf, Xv, Rv, Xte, log=log, **kw)
        info.update(fold=f, baseline=["ar1" if c == 0 else "ridge_p2" for c in choose], n_fit=len(Xf),
                    n_val=len(Xv), seconds=time.time() - t0, n_fit_traj=len(fit_j))
        if info_store is not None:
            info_store.append(info)
        if log:
            log(f"  rmlp fold {f}: {len(fit_j)} fit traj, {time.time() - t0:.1f} s, baseline {info['baseline']}")
        return {"rmlp": Bte + res}
    return extra


# ----------------------------------------------------------------------------- the estimator
def closure_ext(D, phi, K=None, mlp=True, extra=None, log=None):
    """analyze.closure (VW-0) with the `extra` hook and per-item outputs (see module doc)."""
    HORIZONS, PASTS, NFOLD, Ridge, MLP = AN.HORIZONS, AN.PASTS, AN.NFOLD, AN.Ridge, AN.MLP
    multi_pairs, lag_matrix, knn_predict, kinematic = AN.multi_pairs, AN.lag_matrix, AN.knn_predict, AN.kinematic
    Ys = D["Yo"] if phi == "objects" else D["Yc"]
    Bs = D["Bo"] if phi == "objects" else D["Bc"]
    J = len(Ys)
    allY = np.concatenate(Ys)
    sd = allY.std(0)
    eff = sd > 1e-6 * max(sd.max(), 1e-12)
    sd = np.where(eff, sd, 1.0)
    neff = int(eff.sum())
    Ys = [Y[:, eff] / sd[eff] for Y in Ys]      # standardised, constant coords dropped
    Bs = [None if B is None else B[..., eff] / sd[eff] for B in Bs]
    items = []
    for jj in range(J):
        if Bs[jj] is None:
            continue
        for i, t in enumerate(D["st_tick"][jj]):
            items.append((jj, i, int(t)))
    nH = len(HORIZONS)
    tmax = max(HORIZONS)

    def futures(jj, i, t):
        F = [np.stack([Ys[jj][t + h] for h in HORIZONS])]
        for r in range(Bs[jj].shape[1]):
            F.append(np.stack([Bs[jj][i, r, h - 1] for h in HORIZONS]))
        return np.stack(F)       # (R, nH, q)

    FUT = np.stack([futures(*it) for it in items])                     # (n, R, nH, q)
    R = FUT.shape[1]
    orac = ((FUT - FUT.mean(1, keepdims=True)) ** 2).sum((1, 3)) / (R - 1) / neff   # (n, nH)
    preds = {}
    fold_of = {jj: (D["j"][jj] % NFOLD) for jj in range(J)}
    names = ["mean", "persistence", "ar1"] + [f"ridge_p{p}" for p in PASTS] + ["knn"] + (["mlp"] if mlp else [])
    if phi == "objects":
        names += ["kinematic", "kin+ridge_p4"]
    for nm in names:
        preds[nm] = np.zeros((len(items), nH, FUT.shape[3]))
    lam_log = {}
    for f in range(NFOLD):
        tf0 = time.time()
        tr_j = [jj for jj in range(J) if fold_of[jj] != f]
        va_j = [jj for jj in tr_j if fold_of[jj] == (f + 1) % NFOLD]
        fit_j = [jj for jj in tr_j if jj not in va_j]
        te = [n for n, it in enumerate(items) if fold_of[it[0]] == f]
        if not te:
            continue
        mu = np.concatenate([Ys[jj] for jj in tr_j]).mean(0)
        for n in te:
            jj, i, t = items[n]
            preds["mean"][n] = mu
            preds["persistence"][n] = Ys[jj][t]
        X1, F1, _ = multi_pairs([Ys[jj] for jj in tr_j], 1, tmax)
        for hi in range(nH):
            a, b = X1 - mu, F1[hi] - mu
            rho = (a * b).sum(0) / np.maximum((a * a).sum(0), 1e-12)
            for n in te:
                jj, i, t = items[n]
                preds["ar1"][n, hi] = mu + rho * (Ys[jj][t] - mu)
        for p in PASTS:
            Xf, Ff, Y0f = multi_pairs([Ys[jj] for jj in fit_j], p, tmax)
            Xv, Fv, Y0v = multi_pairs([Ys[jj] for jj in va_j], p, tmax)
            rg = Ridge().fit(Xf, [Ff[hi] - Y0f for hi in range(nH)], Xv, [Fv[hi] - Y0v for hi in range(nH)])
            X, F, Y0 = multi_pairs([Ys[jj] for jj in tr_j], p, tmax)
            rg = Ridge().fit(X, [F[hi] - Y0 for hi in range(nH)], lams=rg.lams)
            for hi, h in enumerate(HORIZONS):
                lam_log[(f, p, h)] = rg.lams[hi]
            for n in te:
                jj, i, t = items[n]
                x = lag_matrix(Ys[jj], np.array([t]), p)
                for hi in range(nH):
                    preds[f"ridge_p{p}"][n, hi] = Ys[jj][t] + rg.predict(x, hi)[0]
        Xtr = np.concatenate([np.concatenate([Y[1:-tmax], Y[1:-tmax] - Y[:-tmax - 1]], 1) for Y in (Ys[jj] for jj in tr_j)])
        mX = Xtr.mean(0)
        U, s, Vt = np.linalg.svd(Xtr - mX, full_matrices=False)
        Pc = Vt[:24].T
        Ztr = (Xtr - mX) @ Pc
        Dtr = np.concatenate([np.stack([Y[1 + h:len(Y) - tmax + h] - Y[1:-tmax] for h in HORIZONS], 1)
                              for Y in (Ys[jj] for jj in tr_j)])                     # (N, nH, q)
        Xte = np.stack([np.concatenate([Ys[items[n][0]][items[n][2]],
                                        Ys[items[n][0]][items[n][2]] - Ys[items[n][0]][items[n][2] - 1]]) for n in te])
        Zte = (Xte - mX) @ Pc
        dk = knn_predict(Ztr, Dtr.reshape(len(Dtr), -1), Zte, 20).reshape(len(te), nH, -1)
        for a, n in enumerate(te):
            preds["knn"][n] = Ys[items[n][0]][items[n][2]] + dk[a]
        if mlp:
            def mk(js):
                X, T = [], []
                for jj in js:
                    Y = Ys[jj]
                    ts = np.arange(1, len(Y) - tmax)
                    X.append(lag_matrix(Y, ts, 2))
                    T.append(np.concatenate([Y[ts + h] - Y[ts] for h in HORIZONS], 1))
                return np.concatenate(X), np.concatenate(T)
            Xf, Tf = mk(fit_j)
            Xv, Tv = mk(va_j)
            net = MLP(seed=f).fit(Xf, Tf, Xv, Tv)
            for n in te:
                jj, i, t = items[n]
                dlt = net.predict(lag_matrix(Ys[jj], np.array([t]), 2))[0].reshape(nH, -1)
                preds["mlp"][n] = Ys[jj][t] + dlt
        if phi == "objects":
            sdq = sd[eff]
            full_idx = np.flatnonzero(eff)

            def kin_std(Ystd_rows, h):
                Yr = np.zeros((len(Ystd_rows), len(sd)))
                Yr[:, full_idx] = Ystd_rows * sdq
                return kinematic(Yr, h, K)[:, full_idx] / sdq
            p = 4
            Xf, Ff, Y0f = multi_pairs([Ys[jj] for jj in fit_j], p, tmax)
            Xv, Fv, Y0v = multi_pairs([Ys[jj] for jj in va_j], p, tmax)
            X, F, Y0 = multi_pairs([Ys[jj] for jj in tr_j], p, tmax)
            rg = Ridge().fit(Xf, [Ff[hi] - kin_std(Y0f, h) for hi, h in enumerate(HORIZONS)],
                             Xv, [Fv[hi] - kin_std(Y0v, h) for hi, h in enumerate(HORIZONS)])
            rg = Ridge().fit(X, [F[hi] - kin_std(Y0, h) for hi, h in enumerate(HORIZONS)], lams=rg.lams)
            for n in te:
                jj, i, t = items[n]
                x = lag_matrix(Ys[jj], np.array([t]), p)
                for hi, h in enumerate(HORIZONS):
                    k0 = kin_std(Ys[jj][t][None], h)[0]
                    preds["kinematic"][n, hi] = k0
                    preds["kin+ridge_p4"][n, hi] = k0 + rg.predict(x, hi)[0]
        if extra is not None:                                              # hook (1)
            ex = extra(f, Ys, tr_j, fit_j, va_j, [items[n] for n in te])
            for nm, P in ex.items():
                if nm not in preds:
                    preds[nm] = np.zeros((len(items), nH, FUT.shape[3]))
                preds[nm][te] = P
        if log:
            log(f"  fold {f} done in {time.time() - tf0:.1f} s")
    err = {nm: ((FUT - P[:, None]) ** 2).sum(3).mean(1) / neff for nm, P in preds.items()}   # (n, nH)
    item_j = np.array([it[0] for it in items])

    def summarise(e_by_name, orac_):
        V = {nm: e.mean(0) for nm, e in e_by_name.items()}
        Vu = orac_.mean(0)
        V0 = V["mean"]
        best = np.min(np.stack([V[nm] for nm in V]), 0)
        return V, Vu, V0, best

    V, Vu, V0, best = summarise(err, orac)
    bestname = [min(V, key=lambda nm: V[nm][hi]) for hi in range(nH)]
    groups = {}
    if phi == "objects":
        feat = np.array([LW.OBJ_FEATURES[q % LW.NF] for q in np.flatnonzero(eff)])
        G = {"identity(present,mass,frac_c1)": ("present", "mass", "frac_c1"),
             "position(4)": ("x_cos", "x_sin", "y_cos", "y_sin"), "shape(rg,q1,q2)": ("rg", "q1", "q2"),
             "velocity(2)": ("vx", "vy")}
        for g, fs in G.items():
            sel = np.isin(feat, fs)
            og = ((FUT[..., sel] - FUT[..., sel].mean(1, keepdims=True)) ** 2).sum((1, 3)) / (R - 1) / sel.sum()
            groups[g] = {"oracle": og.mean(0), "n_coords": int(sel.sum())}
            for nm in ("mean", "persistence", "ar1", "ridge_p1", "kinematic", "kin+ridge_p4") + \
                    (("rmlp",) if "rmlp" in preds else ()):
                groups[g][nm] = (((FUT[..., sel] - preds[nm][:, None][..., sel]) ** 2).sum(3).mean(1) / sel.sum()).mean(0)
    ceiling = (V0 - best) / (V0 - Vu)
    depth = (best - Vu) / V0
    rng = np.random.default_rng(0)
    uj = np.unique(item_j)
    bc, bd = [], []
    for b in range(400):
        pick = rng.choice(uj, uj.size, replace=True)
        idx = np.concatenate([np.flatnonzero(item_j == q) for q in pick])
        Vb, Vub, V0b, bestb = summarise({nm: e[idx] for nm, e in err.items()}, orac[idx])
        bc.append((V0b - bestb) / (V0b - Vub))
        bd.append((bestb - Vub) / V0b)
    out = {
        "phi": phi, "n_eff_coords": neff, "n1": int(len(eff)), "n_test_states": len(items), "replicates": int(R),
        "horizons_ticks": HORIZONS, "V0_mean_predictor": V0, "V_oracle": Vu,
        "V": {nm: v for nm, v in V.items()}, "best_level1": best, "best_name": bestname,
        "ceiling": ceiling, "ceiling_se": np.std(bc, 0), "depth_gain": depth, "depth_gain_se": np.std(bd, 0),
        "half_log_ratio_nats_per_coord": 0.5 * np.log(best / Vu),
        "ceiling_well_defined(V0-Vu>=0.1)": (V0 - Vu) >= 0.1,
        "error_by_feature_group": groups,
        "ridge_memory": {f"p{p}": V[f"ridge_p{p}"] for p in PASTS},
        "ridge_lambdas": {f"{k[0]}_{k[1]}_{k[2]}": v for k, v in lam_log.items()},
    }
    det = {"err": err, "orac": orac, "items": np.array(items), "item_j": item_j, "FUT": FUT, "preds": preds,
           "eff": eff, "sd": sd, "Ys": Ys}
    return out, det


# ----------------------------------------------------------------------------- slot network (JAX)
def slot_features(Zs, raw, ts, p=4, nnb=3, H=128, W=128):
    """Per-slot inputs at times ts for the objects view. Zs (T, K, NF) standardised (all coordinates),
    raw (T, K, NF) raw features. Per slot: its own features at p lags; its nnb nearest present
    neighbours (torus offset, distance, gap between bodies, neighbour mass and size, relative
    velocity, approach rate over the last tick); slot one-hot, the presence vector, a lowest-free-slot
    flag and the object count. Returns (len(ts), K, d)."""
    Kk = raw.shape[1]
    n = len(ts)
    own = np.concatenate([Zs[ts - l] for l in range(p)], -1)

    def geom(ti):
        S = raw[ti]
        pres = S[..., 0] > 0.5
        cx = (np.arctan2(S[..., 4], S[..., 3]) * W / (2 * np.pi)) % W
        cy = (np.arctan2(S[..., 6], S[..., 5]) * H / (2 * np.pi)) % H
        dy = (cy[:, None, :] - cy[:, :, None] + H / 2) % H - H / 2          # [t, self, other]
        dx = (cx[:, None, :] - cx[:, :, None] + W / 2) % W - W / 2
        d = np.hypot(dy, dx)
        valid = pres[:, None, :] & pres[:, :, None] & ~np.eye(Kk, dtype=bool)[None]
        return S, pres, dy, dx, d, valid
    S0, p0, dy0, dx0, d0, v0 = geom(ts)
    _, _, _, _, d1, v1 = geom(ts - 1)
    dist = np.where(v0, d0, np.inf)
    order = np.argsort(dist, -1)[..., :nnb]
    take = lambda A: np.take_along_axis(A, order, -1)
    ok = np.isfinite(take(dist))
    bc = lambda col: np.broadcast_to(S0[:, None, :, col], d0.shape)
    rg = S0[..., 7]
    nb_rg = take(bc(7))
    feats = [take(dy0), take(dx0), take(d0), take(d0) - rg[..., None] - nb_rg, take(bc(1)), nb_rg,
             take(bc(10)) - S0[..., 10:11], take(bc(11)) - S0[..., 11:12], take(np.where(v0 & v1, d0 - d1, 0.0))]
    nb = np.stack([np.where(ok, f, 0.0) for f in feats] + [ok.astype(float)], -1).reshape(n, Kk, -1)
    onehot = np.broadcast_to(np.eye(Kk)[None], (n, Kk, Kk))
    presv = np.broadcast_to(p0[:, None, :].astype(float), (n, Kk, Kk))
    free = ~p0
    lowest = np.zeros((n, Kk))
    has = free.any(1)
    lowest[np.flatnonzero(has), np.argmax(free, 1)[has]] = 1.0
    cnt = np.broadcast_to(p0.sum(1, keepdims=True).astype(float), (n, Kk))
    return np.concatenate([own, nb, onehot, presv, lowest[..., None], cnt[..., None]], -1)


def make_slot_extra(D, p=4, log=None, frac=1.0, info_store=None, **kw):
    """`extra` hook for closure_ext (objects only): 'slotnet', one residual MLP shared by all slots
    on slot_features, predicting each slot's own features at every horizon (residual of the same
    linear baseline as rmlp), trained on fit_j[:frac] with per-horizon early stopping on va_j."""
    Kk, NF = 12, LW.NF
    allY = np.concatenate(D["Yo"])
    sd = allY.std(0)
    eff = sd > 1e-6 * max(sd.max(), 1e-12)
    sd = np.where(eff, sd, 1.0)
    tmax = max(AN.HORIZONS)
    nH = len(AN.HORIZONS)

    def full(Y_eff):                                   # (..., q_eff) -> (..., K*NF) standardised
        out = np.zeros(Y_eff.shape[:-1] + (Kk * NF,))
        out[..., eff] = Y_eff
        return out

    def extra(f, Ys, tr_j, fit_j, va_j, te_items):
        t0 = time.time()
        if frac < 1.0:
            fit_j = fit_j[:max(1, int(round(frac * len(fit_j))))]
        mu = np.concatenate([Ys[jj] for jj in fit_j]).mean(0)
        fns, ev = linear_baselines(Ys, fit_j, va_j, tmax, mu)
        choose = np.where(ev["ar1"] <= ev["ridge_p2"], 0, 1)

        def base(Y, ts):
            A, Rr = fns["ar1"](Y, ts), fns["ridge_p2"](Y, ts)
            return np.where(choose[None, :, None] == 0, A, Rr)
        Zc, Rc = {}, {}

        def views(jj):
            if jj not in Zc:
                Zf = full(Ys[jj])
                Zc[jj] = Zf.reshape(len(Zf), Kk, NF)
                Rc[jj] = (Zf * sd).reshape(len(Zf), Kk, NF)
            return Zc[jj], Rc[jj]

        def mk(js):
            X, Rs = [], []
            for jj in js:
                Zs, raw = views(jj)
                ts = np.arange(p - 1, len(Zs) - tmax)
                X.append(slot_features(Zs, raw, ts, p))
                F = np.stack([full(Ys[jj][ts + h]) for h in AN.HORIZONS], 1)        # (n, nH, K*NF)
                Rs.append((F - full(base(Ys[jj], ts))).reshape(len(ts), nH, Kk, NF).transpose(0, 2, 1, 3))
            return np.concatenate(X), np.concatenate(Rs)
        Xf, Rf = mk(fit_j)
        Xv, Rv = mk(va_j)
        Xte = np.concatenate([slot_features(*views(jj), np.array([t]), p) for jj, i, t in te_items])
        Bte = np.concatenate([base(Ys[jj], np.array([t])) for jj, i, t in te_items])          # (n, nH, q_eff)
        res, info = rmlp_fit_predict(Xf, Rf, Xv, Rv, Xte, log=log, **kw)                     # (n, K, nH, NF)
        res = res.transpose(0, 2, 1, 3).reshape(len(te_items), nH, Kk * NF)[..., eff]
        info.update(fold=f, baseline=["ar1" if c == 0 else "ridge_p2" for c in choose], n_fit=len(Xf),
                    n_val=len(Xv), seconds=time.time() - t0, n_fit_traj=len(fit_j), d_in=int(Xf.shape[-1]))
        if info_store is not None:
            info_store.append(info)
        if log:
            log(f"  slotnet fold {f}: {len(fit_j)} fit traj, {time.time() - t0:.1f} s")
        return {"slotnet": Bte + res}
    return extra


def combine(*hooks):
    def extra(*a):
        out = {}
        for h in hooks:
            out.update(h(*a))
        return out
    return extra


# ----------------------------------------------------------------------------- patch network (JAX), coarse view
def patch_features(Zc, ts, p=3, rad=2, G=8):
    """Per-block inputs for the coarse view. Zc (T, 3, G, G) standardised [mean_c0, mean_c1, m2]
    blocks. Per block: the (2 rad + 1)^2 periodic neighbourhood of all 3 channels at p lags, plus
    the view-wide channel means at lag 0. Returns (len(ts), G*G, d)."""
    n = len(ts)
    feats = []
    for l in range(p):
        Z = Zc[ts - l]                                                       # (n, 3, G, G)
        for dy in range(-rad, rad + 1):
            for dx in range(-rad, rad + 1):
                feats.append(np.roll(Z, (-dy, -dx), (2, 3)))                 # value at (i+dy, j+dx)
    X = np.stack(feats, 1).reshape(n, -1, G * G).transpose(0, 2, 1)         # (n, G*G, p*25*3)
    gm = np.broadcast_to(Zc[ts].mean((2, 3))[:, None, :], (n, G * G, Zc.shape[1]))
    return np.concatenate([X, gm], -1)


def make_patch_extra(D, p=3, rad=2, log=None, frac=1.0, info_store=None, **kw):
    """`extra` hook for closure_ext (coarse only): 'patchnet', one residual MLP shared by all 64
    blocks (translation-equivariant on the 8 x 8 torus) on patch_features, predicting each block's 3
    numbers at every horizon (residual of the same linear baseline as rmlp)."""
    G, C3 = 8, 3
    allY = np.concatenate(D["Yc"])
    sd = allY.std(0)
    eff = sd > 1e-6 * max(sd.max(), 1e-12)
    assert eff.all(), "coarse: every block coordinate effective expected"
    tmax = max(AN.HORIZONS)
    nH = len(AN.HORIZONS)
    to_grid = lambda Y: Y.reshape(Y.shape[:-1] + (C3, G, G))

    def extra(f, Ys, tr_j, fit_j, va_j, te_items):
        t0 = time.time()
        if frac < 1.0:
            fit_j = fit_j[:max(1, int(round(frac * len(fit_j))))]
        mu = np.concatenate([Ys[jj] for jj in fit_j]).mean(0)
        fns, ev = linear_baselines(Ys, fit_j, va_j, tmax, mu)
        choose = np.where(ev["ar1"] <= ev["ridge_p2"], 0, 1)

        def base(Y, ts):
            A, Rr = fns["ar1"](Y, ts), fns["ridge_p2"](Y, ts)
            return np.where(choose[None, :, None] == 0, A, Rr)

        def mk(js):
            X, Rs = [], []
            for jj in js:
                Y = Ys[jj]
                ts = np.arange(p - 1, len(Y) - tmax)
                X.append(patch_features(to_grid(Y), ts, p, rad).astype(np.float32))
                F = np.stack([Y[ts + h] for h in AN.HORIZONS], 1)                       # (n, nH, 192)
                Rr = to_grid(F - base(Y, ts)).reshape(len(ts), nH, C3, G * G).transpose(0, 3, 1, 2)
                Rs.append(Rr.astype(np.float32))                                         # (n, 64, nH, 3)
            return np.concatenate(X), np.concatenate(Rs)
        Xf, Rf = mk(fit_j)
        Xv, Rv = mk(va_j)
        Xte = np.concatenate([patch_features(to_grid(Ys[jj]), np.array([t]), p, rad) for jj, i, t in te_items])
        Bte = np.concatenate([base(Ys[jj], np.array([t])) for jj, i, t in te_items])
        d = Xf.shape[-1]
        nf_, nv_ = len(Xf), len(Xv)
        # every (sample, block) is a row of one shared network: flatten the block axis
        kw2 = dict(hidden=64, nblocks=2, batch=1024, steps_per_epoch=60, max_val=40000)
        kw2.update(kw)
        res, info = rmlp_fit_predict(Xf.reshape(-1, d), Rf.reshape(-1, nH, C3), Xv.reshape(-1, d), Rv.reshape(-1, nH, C3),
                                     Xte.reshape(-1, d), log=log, **kw2)
        res = res.reshape(len(te_items), G * G, nH, C3).transpose(0, 2, 3, 1).reshape(len(te_items), nH, C3 * G * G)
        Xf = np.zeros((nf_, 1, d)); Xv = np.zeros((nv_, 1, d))                            # (for the info below)
        info.update(fold=f, baseline=["ar1" if c == 0 else "ridge_p2" for c in choose], n_fit=len(Xf),
                    n_val=len(Xv), seconds=time.time() - t0, n_fit_traj=len(fit_j), d_in=int(Xf.shape[-1]))
        if info_store is not None:
            info_store.append(info)
        if log:
            log(f"  patchnet fold {f}: {len(fit_j)} fit traj, {time.time() - t0:.1f} s")
        return {"patchnet": Bte + res}
    return extra
