"""Certificates for each (world, Phi) pair from the base / branch / input / steer runs.

usage: python analyze.py WORLD      -> results/WORLD_certificates.json

Closure ceiling at this scale (the spec's estimators need ~1e4 trajectories per program and full
log-determinants; here n1 = 144-288 and we have ~70 test states, so):
  - all errors are in standardised units: squared error of coordinate j divided by its stationary
    variance, averaged over the n_eff non-constant coordinates (1.0 = the unconditional mean);
  - the oracle is the true simulator from the true (h0, m): V_u(tau) is the unbiased within-
    replicate variance over R fresh-noise replicates (base continuation + R-1 branches);
  - level-1-only predictors are trained on whole held-out-by-trajectory folds and scored against
    the same replicate futures (expected squared error over replicates);
  - ceiling c = (V0 - V_best)/(V0 - V_u); depth gain g = (V_best - V_u)/V0: the share of
    variance that only level-0 access predicts (an upper bound: better level-1 predictors shrink it).
"""
import glob
import json
import math
import os
import sys

import numpy as np

import lenia_world as LW
vw = LW.vw

HORIZONS = [1, 2, 4, 8, 16, 32]
PASTS = [1, 2, 4, 8]
NFOLD = 4


# ----------------------------------------------------------------------------- data
def load(name):
    base = sorted(glob.glob(f"data/{name}/base_*.npz"))
    D = {"Yo": [], "Yc": [], "tab": [], "glob": [], "mass": [], "st_tick": [], "burn": None, "j": []}
    Bo, Bc = [], []
    for f in base:
        j = int(os.path.basename(f)[5:8])
        bf = f"data/{name}/branch_{j:03d}.npz"
        d = np.load(f)
        D["j"].append(j)
        for k in ("Yo", "Yc", "tab", "glob", "mass"):
            D[k].append(d[k])
        D["burn"] = int(d["burn_in"])
        D["st_tick"].append(d["st_tick"] - D["burn"])
        if os.path.exists(bf):
            b = np.load(bf)
            Bo.append(b["Yo"])
            Bc.append(b["Yc"])
        else:
            Bo.append(None)
            Bc.append(None)
    D["Bo"], D["Bc"] = Bo, Bc
    return D


# ----------------------------------------------------------------------------- predictors
def lag_matrix(Y, ts, p):
    return np.concatenate([Y[ts - l] for l in range(p)], 1)


def train_pairs(Ys, p, tau):
    X, Yt, Y0 = [], [], []
    for Y in Ys:
        ts = np.arange(p - 1, len(Y) - tau)
        X.append(lag_matrix(Y, ts, p))
        Yt.append(Y[ts + tau])
        Y0.append(Y[ts])
    return np.concatenate(X), np.concatenate(Yt), np.concatenate(Y0)


class Ridge:
    """Ridge regression of several target blocks on one design matrix (one SVD); the penalty is
    chosen per block on a validation set."""
    LAMS = [1e-1, 1, 10, 100, 1e3, 1e4, 1e5]

    def fit(self, X, Ys, Xv=None, Yvs=None, lams=None):
        self.mx, self.sx = X.mean(0), np.maximum(X.std(0), 0.1)     # inputs are globally standardised
        Z = (X - self.mx) / self.sx
        U, s, Vt = np.linalg.svd(Z, full_matrices=False)
        self.my = [Y.mean(0) for Y in Ys]
        UtY = [U.T @ (Y - m) for Y, m in zip(Ys, self.my)]
        if Xv is not None:
            Zv = (Xv - self.mx) / self.sx
            self.lams = []
            for b, Yv in enumerate(Yvs):
                errs = [((Zv @ (Vt.T @ ((s / (s ** 2 + lam))[:, None] * UtY[b])) + self.my[b] - Yv) ** 2).mean()
                        for lam in self.LAMS]
                self.lams.append(self.LAMS[int(np.argmin(errs))])
        elif lams is not None:
            self.lams = list(lams)
        self.W = [Vt.T @ ((s / (s ** 2 + lam))[:, None] * u) for lam, u in zip(self.lams, UtY)]
        return self

    def predict(self, X, b):
        return ((X - self.mx) / self.sx) @ self.W[b] + self.my[b]


def multi_pairs(Ys, p, tmax):
    """Design matrix of p lags and the futures at every horizon, on a common time range."""
    X, F, Y0 = [], [], []
    for Y in Ys:
        ts = np.arange(p - 1, len(Y) - tmax)
        X.append(lag_matrix(Y, ts, p))
        F.append(np.stack([Y[ts + h] for h in HORIZONS], 0))
        Y0.append(Y[ts])
    return np.concatenate(X), np.concatenate(F, 1), np.concatenate(Y0)


def knn_predict(Xtr, Dtr, Xte, k):
    # Xtr (N,d) already reduced; Dtr (N,q) target deltas
    d2 = (Xte ** 2).sum(1)[:, None] - 2 * Xte @ Xtr.T + (Xtr ** 2).sum(1)[None]
    idx = np.argpartition(d2, k, axis=1)[:, :k]
    return Dtr[idx].mean(1)


class MLP:
    """One hidden layer (ReLU), Adam, early stopping on a validation set."""

    def __init__(self, hidden=128, lr=1e-3, wd=1e-4, epochs=150, batch=128, seed=0):
        self.h, self.lr, self.wd, self.epochs, self.batch = hidden, lr, wd, epochs, batch
        self.rng = np.random.default_rng(seed)

    def fit(self, X, Y, Xv, Yv):
        self.mx, self.sx = X.mean(0), np.maximum(X.std(0), 0.1)     # inputs are globally standardised
        self.my, self.sy = Y.mean(0), np.maximum(Y.std(0), 0.1)
        Z, T = (X - self.mx) / self.sx, (Y - self.my) / self.sy
        Zv, Tv = (Xv - self.mx) / self.sx, (Yv - self.my) / self.sy
        d, q = Z.shape[1], T.shape[1]
        P = {"W1": self.rng.standard_normal((d, self.h)) * math.sqrt(2.0 / d), "b1": np.zeros(self.h),
             "W2": self.rng.standard_normal((self.h, q)) * math.sqrt(1.0 / self.h), "b2": np.zeros(q)}
        M = {k: np.zeros_like(v) for k, v in P.items()}
        V = {k: np.zeros_like(v) for k, v in P.items()}
        best, bestP, bad, it = np.inf, None, 0, 0
        for ep in range(self.epochs):
            perm = self.rng.permutation(len(Z))
            for b0 in range(0, len(Z), self.batch):
                ib = perm[b0:b0 + self.batch]
                x, t = Z[ib], T[ib]
                a1 = x @ P["W1"] + P["b1"]
                h1 = np.maximum(a1, 0)
                out = h1 @ P["W2"] + P["b2"]
                g = 2 * (out - t) / t.size
                G = {"W2": h1.T @ g, "b2": g.sum(0)}
                gh = (g @ P["W2"].T) * (a1 > 0)
                G["W1"], G["b1"] = x.T @ gh, gh.sum(0)
                it += 1
                for k in P:
                    G[k] = G[k] + self.wd * P[k] if k[0] == "W" else G[k]
                    M[k] = 0.9 * M[k] + 0.1 * G[k]
                    V[k] = 0.999 * V[k] + 0.001 * G[k] ** 2
                    P[k] -= self.lr * (M[k] / (1 - 0.9 ** it)) / (np.sqrt(V[k] / (1 - 0.999 ** it)) + 1e-8)
            vl = ((np.maximum(Zv @ P["W1"] + P["b1"], 0) @ P["W2"] + P["b2"] - Tv) ** 2).mean()
            if vl < best - 1e-5:
                best, bestP, bad = vl, {k: v.copy() for k, v in P.items()}, 0
            else:
                bad += 1
                if bad >= 12:
                    break
        self.P = bestP
        return self

    def predict(self, X):
        Z = (X - self.mx) / self.sx
        P = self.P
        return (np.maximum(Z @ P["W1"] + P["b1"], 0) @ P["W2"] + P["b2"]) * self.sy + self.my


def kinematic(Y0, tau, K, H=128, W=128):
    """Objects: move each present slot's embedded centroid by tau * velocity, keep the rest."""
    out = Y0.copy()
    S = out.reshape(len(Y0), K, LW.NF)
    E = H / (2 * np.pi)
    cx = np.arctan2(S[:, :, 4], S[:, :, 3]) * W / (2 * np.pi) + tau * S[:, :, 10]
    cy = np.arctan2(S[:, :, 6], S[:, :, 5]) * H / (2 * np.pi) + tau * S[:, :, 11]
    pres = S[:, :, 0] > 0.5
    S[:, :, 3] = np.where(pres, E * np.cos(2 * np.pi * cx / W), 0)
    S[:, :, 4] = np.where(pres, E * np.sin(2 * np.pi * cx / W), 0)
    S[:, :, 5] = np.where(pres, E * np.cos(2 * np.pi * cy / H), 0)
    S[:, :, 6] = np.where(pres, E * np.sin(2 * np.pi * cy / H), 0)
    return S.reshape(len(Y0), -1)


# ----------------------------------------------------------------------------- closure
def closure(D, phi, K=None, mlp=True):
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
    # test items
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
    names = ["mean", "persistence", "ar1"] + [f"ridge_p{p}" for p in PASTS] + ["knn", "mlp"]
    if phi == "objects":
        names += ["kinematic", "kin+ridge_p4"]
    for nm in names:
        preds[nm] = np.zeros((len(items), nH, FUT.shape[3]))
    lam_log = {}
    for f in range(NFOLD):
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
        # ar1: per-coordinate damped persistence toward the training mean, rho_j(tau) by least squares
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
        # kNN on PCA of [y(t), y(t)-y(t-1)]
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
        # MLP: p = 2 lags -> deltas at all horizons
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
    # errors against replicate futures
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
            for nm in ("mean", "persistence", "ar1", "ridge_p1", "kinematic", "kin+ridge_p4"):
                groups[g][nm] = (((FUT[..., sel] - preds[nm][:, None][..., sel]) ** 2).sum(3).mean(1) / sel.sum()).mean(0)
    ceiling = (V0 - best) / (V0 - Vu)
    depth = (best - Vu) / V0
    # bootstrap over trajectories
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
    return out, eff, sd


# ----------------------------------------------------------------------------- interestingness
def mi(d, L):
    return (d + L / 2) % L - L / 2


def objects_stats(D, K, stride, H=128, W=128):
    n_present, speeds, rgs, masses = [], [], [], []
    tracks = {}          # (j, uid) -> dict
    inter_event = []
    enc_total, enc_fused = 0, 0
    ev_counts = np.zeros(4)
    T_all = 0
    for jj, (Yo, tab, gl) in enumerate(zip(D["Yo"], D["tab"], D["glob"])):
        S = Yo.reshape(len(Yo), K, LW.NF)
        pres = S[:, :, 0] > 0.5
        n_present.append(pres.sum(1))
        ev = tab[:, :, 3]
        uid = tab[:, :, 4]
        cont = pres & (ev == 0)
        speeds.append(np.hypot(S[:, :, 10], S[:, :, 11])[cont])
        rgs.append(S[:, :, 7][pres])
        masses.append(S[:, :, 1][pres])
        ev_counts += gl[-1, 1:] - gl[0, 1:]
        T_all += len(Yo) - 1
        last_ev = {}
        for t in range(len(Yo)):
            for s in range(K):
                if not pres[t, s]:
                    continue
                key = (jj, int(uid[t, s]))
                tk = tracks.setdefault(key, {"first": t, "last": t, "start_ev": int(ev[t, s]), "path": 0.0,
                                              "pos": [], "rg": []})
                tk["last"] = t
                tk["pos"].append((tab[t, s, 0], tab[t, s, 1]))
                tk["rg"].append(S[t, s, 7])
                if ev[t, s] == 0 and t > tk["first"]:
                    tk["path"] += float(np.hypot(S[t, s, 10], S[t, s, 11]))
                if ev[t, s] != 0 or t == tk["first"]:
                    if key in last_ev and ev[t, s] != 0:
                        inter_event.append(t - last_ev[key])
                    last_ev[key] = t
            # encounters: pairs whose centroids come within 1.6 (rg_i + rg_j) + 2 px (about touching)
        for t in range(1, len(Yo)):
            ps = np.flatnonzero(pres[t])
            for a in range(len(ps)):
                for b in range(a + 1, len(ps)):
                    sa, sb = ps[a], ps[b]
                    dd = np.hypot(mi(tab[t, sa, 0] - tab[t, sb, 0], H), mi(tab[t, sa, 1] - tab[t, sb, 1], W))
                    close = dd < 1.6 * (S[t, sa, 7] + S[t, sb, 7]) + 2
                    was = pres[t - 1, sa] and pres[t - 1, sb] and uid[t - 1, sa] == uid[t, sa] and \
                        uid[t - 1, sb] == uid[t, sb] and np.hypot(mi(tab[t - 1, sa, 0] - tab[t - 1, sb, 0], H),
                                                                  mi(tab[t - 1, sa, 1] - tab[t - 1, sb, 1], W)) < \
                        1.6 * (S[t - 1, sa, 7] + S[t - 1, sb, 7]) + 2
                    if close and not was:
                        enc_total += 1
                        # outcome: one of the two fuses within the next 5 ticks
                        fused = False
                        for tt in range(t + 1, min(t + 6, len(Yo))):
                            if (ev[tt, sa] in (-1, 3) or ev[tt, sb] in (-1, 3)):
                                fused = True
                                break
                        enc_fused += fused
    n_present = np.concatenate(n_present)
    speeds = np.concatenate(speeds)
    rg_med = float(np.median(np.concatenate(rgs)))
    body_len = 2.4 * rg_med
    lives, paths, nets, complete = [], [], [], []
    for key, tk in tracks.items():
        life = tk["last"] - tk["first"] + 1
        lives.append(life)
        paths.append(tk["path"] / body_len)
        P = np.array(tk["pos"])
        if len(P) > 1:
            dy = np.cumsum(np.r_[0, mi(np.diff(P[:, 0]), H)])
            dx = np.cumsum(np.r_[0, mi(np.diff(P[:, 1]), W)])
            nets.append(float(np.hypot(dy[-1], dx[-1])) / body_len)
        else:
            nets.append(0.0)
    lives, paths, nets = np.array(lives), np.array(paths), np.array(nets)
    long = lives >= 50
    return {
        "ticks": int(T_all), "trajectories": len(D["Yo"]), "steps_per_tick": stride,
        "objects_per_tick": {"median": float(np.median(n_present)), "p10": float(np.percentile(n_present, 10)),
                             "p90": float(np.percentile(n_present, 90)), "max": int(n_present.max()),
                             "frac_ticks_all_slots_full": float((n_present >= K).mean())},
        "mass_median": float(np.median(np.concatenate(masses))), "rg_median_px": rg_med,
        "body_length_px(2.4 rg)": body_len,
        "speed_px_per_tick": {"median": float(np.median(speeds)), "p90": float(np.percentile(speeds, 90))},
        "speed_px_per_step_median": float(np.median(speeds)) / stride,
        "events_per_100_ticks": dict(zip(["births", "deaths", "fusions", "fissions"],
                                         (100 * ev_counts / T_all).tolist())),
        "n_tracks": int(len(lives)),
        "track_life_ticks": {"median": float(np.median(lives)), "p90": float(np.percentile(lives, 90)),
                             "frac_ge_50": float(long.mean())},
        "inter_event_ticks_median": float(np.median(inter_event)) if inter_event else None,
        "path_body_lengths_tracks_ge_50": {"median": float(np.median(paths[long])) if long.any() else None,
                                          "frac_ge_3": float((paths[long] >= 3).mean()) if long.any() else None},
        "net_displacement_body_lengths_tracks_ge_50": float(np.median(nets[long])) if long.any() else None,
        "encounters_per_100_ticks": 100 * enc_total / T_all,
        "encounters_fused_within_5_ticks": float(enc_fused / max(enc_total, 1)),
    }


def coarse_stats(D):
    Y = np.concatenate([y[None] for y in D["Yc"]])        # (J, T, q)
    Z = (Y - Y.mean((0, 1))) / (Y.std((0, 1)) + 1e-12)
    ac = []
    for lag in [1, 2, 4, 8, 16, 32]:
        ac.append(float((Z[:, lag:] * Z[:, :-lag]).mean()))
    occ = float((D["Yc"][0][:, :128] > 0.02).mean()) if len(D["Yc"]) else None
    return {"autocorr_by_lag": dict(zip([1, 2, 4, 8, 16, 32], ac)), "block_occupied_frac(mean>0.02)": occ}


def mass_check(D):
    drift = [float(np.abs(m - m[0]).max() / m[0].min()) for m in D["mass"]]
    return {"max_rel_mass_drift_per_channel": max(drift)}


# ----------------------------------------------------------------------------- inputs
def inputs_analysis(D, name, phi_eff, si=1):
    files = sorted(glob.glob(f"data/{name}/inputs_*_s{si}.npz"))
    if not files:
        return None
    out = {}
    for phi in ("objects", "coarse"):
        eff, sd = phi_eff[phi]
        key = "Yo" if phi == "objects" else "Yc"
        Bkey = "Bo" if phi == "objects" else "Bc"
        per = {}
        for f in files:
            j = int(os.path.basename(f)[7:10])
            jj = D["j"].index(j)
            r = np.load(f)
            t0 = int(r["t0"])
            base = D[key][jj]
            B = D[Bkey][jj]
            # per-state oracle spread at each tau (base + branches), standardised
            reps = np.concatenate([base[None, t0 + 1:t0 + 1 + B.shape[2]], B[si]], 0)[..., eff] / sd[eff]
            Vu_state = ((reps - reps.mean(0)) ** 2).sum((0, 2)) / (reps.shape[0] - 1) / eff.sum()
            natural = (((base[t0 + 1:t0 + 1 + B.shape[2]] - base[t0]) / sd)[:, eff] ** 2).mean(1)
            for cn in r["conds"]:
                cn = str(cn)
                if f"{cn}__{key}" not in r.files:
                    continue
                Yi = r[f"{cn}__{key}"]
                n = min(len(Yi), B.shape[2])
                Dlt = ((Yi[:n] - base[t0 + 1:t0 + 1 + n]) / sd)[:, eff]
                resp = (Dlt ** 2).mean(1)
                rec = per.setdefault(cn, {"resp": [], "snr": [], "rel_nat": [], "moved": [], "on_matter": [],
                                          "admissible": [], "l0diff": [], "maxcoord_snr": []})
                rec["resp"].append(resp)
                rec["snr"].append(resp / Vu_state[:n])
                rec["rel_nat"].append(resp / natural[:n])
                sdu = np.sqrt(((reps - reps.mean(0)) ** 2).sum(0) / (reps.shape[0] - 1)) + 1e-9
                rec["maxcoord_snr"].append((np.abs(Dlt) / sdu[:n]).max(1))
                rec["moved"].append(float(r[f"{cn}__moved"].sum()) if r[f"{cn}__moved"].size else 0.0)
                om = r[f"{cn}__on_matter"]
                rec["on_matter"].append(float((om[:, 0] > 0).mean()) if om.size else 0.0)
                rec["admissible"].append(bool(r[f"{cn}__admissible"].all()) if r[f"{cn}__admissible"].size else True)
                rec["l0diff"].append(r[f"{cn}__l0diff"])
        res = {}
        taus = [1, 2, 4, 8, 16, 32]
        for cn, rec in per.items():
            snr = np.array(rec["snr"])
            res[cn] = {
                "n_states": len(rec["snr"]),
                "admissible_default": bool(all(rec["admissible"])),
                "moved_mass_median": float(np.median(rec["moved"])),
                "frac_trials_moving_over_0.01": float(np.mean(np.array(rec["moved"]) > 1e-2)),
                "frac_input_ticks_with_a_source_on_a_body": float(np.mean(rec["on_matter"])),
                "snr_median_by_tau": {t: float(np.median(snr[:, t - 1])) for t in taus if t <= snr.shape[1]},
                "frac_snr_ge_1_by_tau": {t: float((snr[:, t - 1] >= 1).mean()) for t in taus if t <= snr.shape[1]},
                "split_by_source_on_body": {
                    lab: {"n": int(sel.sum()),
                          "snr_median_by_tau": {t: float(np.median(snr[sel, t - 1])) for t in taus if t <= snr.shape[1]},
                          "moved_mass_median": float(np.median(np.array(rec["moved"])[sel]))}
                    for lab, sel in (("on_body", np.array(rec["on_matter"]) > 0), ("off_body", np.array(rec["on_matter"]) == 0))
                    if sel.any()} if cn.startswith("rand") else None,
                "max_coord_snr_median_by_tau": {t: float(np.median(np.array(rec["maxcoord_snr"])[:, t - 1]))
                                                for t in taus if t <= snr.shape[1]},
                "resp_over_natural_change_median_by_tau": {t: float(np.median(np.array(rec["rel_nat"])[:, t - 1]))
                                                           for t in taus if t <= snr.shape[1]},
                "level0_L1_diff_median_by_tau": dict(zip([1, 2, 4, 8, 16, 24, 32],
                                                         np.median(np.array(rec["l0diff"]), 0).tolist()))
                if len(rec["l0diff"][0]) else None,
            }
        out[phi] = res
    return out


# ----------------------------------------------------------------------------- inputs, replicated
def inputs_rep_analysis(D, name, phi_eff, closures, si=1):
    """Mean shift of the level-1 future caused by a fixed open-loop input program, estimated over
    R = 6 noise realisations, each against its own no-input twin (identical noise)."""
    files = sorted(glob.glob(f"data/{name}/inrep_*_s{si}.npz"))
    if not files:
        return None
    out = {}
    for phi in ("objects", "coarse"):
        eff, sd = phi_eff[phi]
        key, Bkey = ("Yo", "Bo") if phi == "objects" else ("Yc", "Bc")
        H = closures[phi]["horizons_ticks"]
        vbest = np.array(closures[phi]["best_level1"])
        per = {}
        for f in files:
            j = int(os.path.basename(f)[6:9])
            jj = D["j"].index(j)
            r = np.load(f)
            t0 = int(r["t0"])
            base = D[key][jj][:, eff] / sd[eff]
            B = D[Bkey][jj][si][..., eff] / sd[eff]                           # (5, T, q)
            T = B.shape[1]
            twins = np.concatenate([base[None, t0 + 1:t0 + 1 + T], B], 0)     # (6, T, q)
            Vu = ((twins - twins.mean(0)) ** 2).sum((0, 2)) / (twins.shape[0] - 1) / eff.sum()
            for cn in r["conds"]:
                cn = str(cn)
                Yi = r[f"{cn}__{key}"][:, :T][..., eff] / sd[eff]
                Dl = Yi - twins                                                # (6, T, q)
                R = Dl.shape[0]
                m = Dl.mean(0)
                varm = Dl.var(0, ddof=1) / R
                shift2 = ((m ** 2) - varm).sum(1) / eff.sum()                  # unbiased |mean shift|^2
                twin2 = (Dl ** 2).sum(2).mean(0) / eff.sum()
                rec = per.setdefault(cn, {"shift": [], "snr_mean": [], "snr_twin": [], "Vu": []})
                rec["shift"].append(shift2)
                rec["snr_mean"].append(shift2 / Vu)
                rec["snr_twin"].append(twin2 / Vu)
                rec["Vu"].append(Vu)
        res = {}
        for cn, rec in per.items():
            sm, st = np.array(rec["snr_mean"]), np.array(rec["snr_twin"])
            sh = np.array(rec["shift"])
            res[cn] = {
                "n_states": int(sm.shape[0]),
                "mean_shift_snr_vs_oracle_spread_median": {t: float(np.median(sm[:, t - 1])) for t in H},
                "frac_states_mean_shift_snr_ge_1": {t: float((sm[:, t - 1] >= 1).mean()) for t in H},
                "twin_snr_median": {t: float(np.median(st[:, t - 1])) for t in H},
                "mean_shift_vs_level1_prediction_error": {t: float(np.mean(sh[:, t - 1]) / vbest[hi])
                                                          for hi, t in enumerate(H)},
            }
        out[phi] = res
    return out

# ----------------------------------------------------------------------------- steering
def steer_analysis(D, name, si=2, H=128, W=128):
    files = sorted(glob.glob(f"data/{name}/steer_*_s{si}.npz"))
    rows = []
    for f in files:
        r = np.load(f)
        s = int(r["target"])
        if s < 0:
            continue
        j = int(os.path.basename(f)[6:9])
        jj = D["j"].index(j)
        t0 = int(r["t0"])
        btab = D["tab"][jj]
        bYo = D["Yo"][jj].reshape(len(D["Yo"][jj]), -1, LW.NF)
        uid0 = btab[t0, s, 4]
        v0 = bYo[t0, s, 10:12]
        u0 = v0 / max(np.linalg.norm(v0), 1e-9)
        n0 = np.array([-u0[1], u0[0]])
        for strat in ("flank+", "flank-", "lead+", "lead-"):
            if f"{strat}__tab" not in r.files:
                continue
            tab = r[f"{strat}__tab"]
            nt = len(tab)
            sign = 1 if strat.endswith("+") else -1
            alive_s = [k for k in range(nt) if tab[k, s, 0] > 0.5 and tab[k, s, LW.NF + 4] == uid0]
            alive_b = [k for k in range(nt) if btab[t0 + 1 + k, s, 0] > 0.5 and btab[t0 + 1 + k, s, 4] == uid0]
            kend = min(max(alive_s) if alive_s else -1, max(alive_b) if alive_b else -1)
            row = {"traj": j, "slot": s, "strategy": strat, "ticks": nt, "survived_ticks": kend + 1,
                   "admissible_all": bool(r[f"{strat}__admissible"].all()),
                   "steered_ticks": int((r[f"{strat}__cells"][:, 0] >= 0).sum())}
            if kend >= 7:
                ps = np.array([tab[k, s, LW.NF:LW.NF + 2] for k in range(kend + 1)])
                pb = np.array([btab[t0 + 1 + k, s, 0:2] for k in range(kend + 1)])
                start = btab[t0, s, 0:2]

                def unwrap(P):
                    d = np.vstack([mi(P[0] - start, np.array([H, W]))[None],
                                   mi(np.diff(P, axis=0), np.array([H, W]))])
                    return np.cumsum(d, 0)
                Us, Ub = unwrap(ps), unwrap(pb)          # (k, 2) as (dy, dx)
                off = Us[-1] - Ub[-1]
                lat = off[1] * n0[0] + off[0] * n0[1]
                fwd = off[1] * u0[0] + off[0] * u0[1]
                ds = Us[-1] - Us[-8]
                db = Ub[-1] - Ub[-8]
                ang = math.degrees(math.atan2(ds[0], ds[1]) - math.atan2(db[0], db[1]))
                ang = (ang + 180) % 360 - 180
                row.update({"lateral_offset_px(+ = toward commanded side)": float(sign * lat),
                            "forward_offset_px": float(fwd), "heading_change_deg_signed": float(sign * ang),
                            "twin_path_px": float(np.hypot(*Ub[-1])),
                            "mass_ratio_end": float(tab[kend, s, 1] / bYo[t0 + 1 + kend, s, 1])})
            rows.append(row)
    summ = {}
    for strat in ("flank+", "flank-", "lead+", "lead-", "flank", "lead"):
        rr = [x for x in rows if x["strategy"].startswith(strat) and "lateral_offset_px(+ = toward commanded side)" in x]
        if rr:
            lat = np.array([x["lateral_offset_px(+ = toward commanded side)"] for x in rr])
            hd = np.array([x["heading_change_deg_signed"] for x in rr])
            summ[strat] = {"n": len(rr), "lateral_median_px": float(np.median(lat)),
                           "frac_toward_commanded_side": float((lat > 0).mean()),
                           "heading_change_median_deg": float(np.median(hd)),
                           "frac_heading_toward": float((hd > 0).mean()),
                           "survived_full_frac": float(np.mean([x["survived_ticks"] == x["ticks"] for x in rr]))}
    return {"rows": rows, "summary": summ}


def main():
    name = sys.argv[1]
    mlp = "--nomlp" not in sys.argv
    specs, parts = LW.make_specs(name)
    K, stride = parts["tracker"].K, parts["cfg"]["stride"]
    D = load(name)
    res = {"world": name, "cfg": parts["cfg"], "n_traj": len(D["Yo"]), "ticks_per_traj": len(D["Yo"][0]) - 1}
    res["mass"] = mass_check(D)
    eff = {}
    for phi in ("coarse", "objects"):
        cl, e, sd = closure(D, phi, K=K, mlp=mlp)
        res[f"closure_{phi}"] = cl
        eff[phi] = (e, sd)
        print(phi, "ceiling", np.round(cl["ceiling"], 3), "depth", np.round(cl["depth_gain"], 3), flush=True)
    res["objects_stats"] = objects_stats(D, K, stride)
    res["coarse_stats"] = coarse_stats(D)
    res["inputs"] = inputs_analysis(D, name, eff)
    res["inputs_replicated"] = inputs_rep_analysis(D, name, eff, {p: res[f"closure_{p}"] for p in ("objects", "coarse")})
    res["steering"] = steer_analysis(D, name)
    os.makedirs("results", exist_ok=True)
    json.dump(vw.jsonable(res), open(f"results/{name}_certificates.json", "w"), indent=1)
    print(json.dumps(vw.jsonable({k: res[k] for k in ("objects_stats", "coarse_stats", "mass")}), indent=1))


if __name__ == "__main__":
    main()
