"""Reviewer's own closure-ceiling estimate for A_gliders from the saved base/branch level-1 data.

Independent of analyze.py: own folds (contiguous blocks of trajectories), own predictors (training
mean, persistence, per-coordinate AR(1) toward the mean, ridge on two lags predicting the change),
own lambda choice (inner held-out trajectories). Errors per coordinate in units of each
coordinate's stationary variance; the oracle is the unbiased within-replicate variance of the
6 replicate futures (base continuation + 5 fresh-noise branches) from the true (h0, m).
"""
import glob
import json
import sys

import numpy as np

D = "/home/user/evalwork/vecworld/integrate/data/A_gliders"
HZ = [1, 2, 4, 8, 16, 32]
LAMS = [1e-2, 1e-1, 1, 10, 100, 1e3, 1e4]
out = {}
for phi, key in (("objects", "Yo"), ("coarse", "Yc")):
    Ys, Bs, ticks = [], [], []
    for f in sorted(glob.glob(f"{D}/base_*.npz")):
        d = np.load(f)
        b = np.load(f.replace("base_", "branch_"))
        Ys.append(d[key])
        Bs.append(b[key])
        ticks.append(d["st_tick"] - int(d["burn_in"]))
    J = len(Ys)
    sd = np.concatenate(Ys).std(0)
    eff = sd > 1e-6 * sd.max()
    Ys = [Y[:, eff] / sd[eff] for Y in Ys]
    Bs = [B[..., eff] / sd[eff] for B in Bs]
    q = int(eff.sum())
    items = [(j, i, int(t)) for j in range(J) for i, t in enumerate(ticks[j])]
    FUT = np.stack([np.stack([np.stack([Ys[j][t + h] for h in HZ])] +
                             [np.stack([Bs[j][i, r, h - 1] for h in HZ]) for r in range(Bs[j].shape[1])])
                    for j, i, t in items])                                  # (n, R, nH, q)
    R = FUT.shape[1]
    Vu = (((FUT - FUT.mean(1, keepdims=True)) ** 2).sum((1, 3)) / (R - 1) / q).mean(0)
    fold = np.array([j * 4 // J for j in range(J)])                         # contiguous blocks
    P = {nm: np.zeros((len(items), len(HZ), q)) for nm in ("mean", "persist", "ar1", "ridge2")}

    def pairs(js, h):
        X, Y = [], []
        for j in js:
            Y_ = Ys[j]
            ts = np.arange(1, len(Y_) - h)
            X.append(np.concatenate([Y_[ts], Y_[ts] - Y_[ts - 1]], 1))
            Y.append(Y_[ts + h] - Y_[ts])
        return np.concatenate(X), np.concatenate(Y)

    def ridge(X, Y, lam):
        mx, my = X.mean(0), Y.mean(0)
        Xc = X - mx
        Wt = np.linalg.solve(Xc.T @ Xc + lam * len(X) * np.eye(X.shape[1]), Xc.T @ (Y - my))
        return lambda x: (x - mx) @ Wt + my

    lam_used = {}
    for f in range(4):
        tr = [j for j in range(J) if fold[j] != f]
        te = [n for n, (j, i, t) in enumerate(items) if fold[j] == f]
        mu = np.concatenate([Ys[j] for j in tr]).mean(0)
        inner_va = tr[-2:]
        inner_fit = tr[:-2]
        for hi, h in enumerate(HZ):
            # AR(1) toward the training mean
            a = np.concatenate([Ys[j][:-h] for j in tr]) - mu
            bb = np.concatenate([Ys[j][h:] for j in tr]) - mu
            rho = (a * bb).sum(0) / np.maximum((a * a).sum(0), 1e-12)
            # ridge, lambda from inner held-out trajectories
            Xf, Yf = pairs(inner_fit, h)
            Xv, Yv = pairs(inner_va, h)
            errs = [((ridge(Xf, Yf, lam)(Xv) - Yv) ** 2).mean() for lam in LAMS]
            lam = LAMS[int(np.argmin(errs))]
            lam_used[f"{f}_{h}"] = lam
            Xa, Ya = pairs(tr, h)
            pr = ridge(Xa, Ya, lam)
            for n in te:
                j, i, t = items[n]
                y = Ys[j][t]
                P["mean"][n, hi] = mu
                P["persist"][n, hi] = y
                P["ar1"][n, hi] = mu + rho * (y - mu)
                P["ridge2"][n, hi] = y + pr(np.concatenate([y, y - Ys[j][t - 1]])[None])[0]
    V = {nm: (((FUT - p[:, None]) ** 2).sum(3).mean(1) / q).mean(0) for nm, p in P.items()}
    best = np.min(np.stack(list(V.values())), 0)
    V0 = V["mean"]
    out[phi] = {"n_items": len(items), "replicates": R, "n_eff": q, "V0": V0.round(4).tolist(),
                "V_oracle": Vu.round(4).tolist(), "V": {k: v.round(4).tolist() for k, v in V.items()},
                "best": [min(V, key=lambda k: V[k][hi]) for hi in range(len(HZ))],
                "ceiling": ((V0 - best) / (V0 - Vu)).round(3).tolist(),
                "depth_gain": ((best - Vu) / V0).round(3).tolist()}
    print(phi, json.dumps(out[phi]))
json.dump(out, open("/home/user/evalwork/vecworld_integrate_review/closure_mine.json", "w"), indent=1)
