"""ccert -- CPU certification worker of the study `bias2` (see c5.py). Several run in parallel.

usage: python -B ccert.py WORKER_ID          (B5_WORLD)
Claims latent files $B5_WORK/<world>/lat/<phi>__cert<h>.npz (atomic rename of the .ready marker; hand designs
first) and certifies each with the SAME fixed predictor family as round 4 and learned_phi2 (lphi.certify:
closure_lib.closure_ext, the VW-0 family mean / persistence / AR(1) / ridge on 1, 2, 4, 8 lags / kNN,
per-coordinate standardisation, 4 folds by trajectory, plus the local equivariant ridge 'lridge' on the 8 x 8
grid; MLP off) against the branch futures at h = 1, 2, 4, 8, 16, with the Gaussian log-det measures.
Also, on the certification half's base trajectories:
  non-triviality  within-trajectory variance share, participation ratio (the effective dimension), the share of
                  variance in the box mean and how much the box mean moves in time (0 for a conserved quantity)
  agreement       with every target hand design (c5.agree_targets()), both directions, by PER-BLOCK LOCAL READOUTS
                  with weights shared over blocks (the round-4 checker's point: a ridge over all 64 block values
                  can undo local smoothing, so it cannot tell a block variable from its smoothed version):
                    loc1   linear readout from the same block's c numbers
                    loc1q  the same plus squares and products (a pointwise nonlinear readout)
                    loc9   linear readout from the 3 x 3 block neighbourhood
                    glob   round 4's metric: ridge from all 64 c numbers to all 64 c' numbers
                  cross-validated over 4 folds of trajectories, pooled SSE / SST with standardised target columns,
                  every 2nd tick.
-> $B5_WORK/<world>/cert/<stem>.npz (per-item errors, oracle, item trajectories), <stem>.json; JSON and a float32
copy of the per-item errors also in $B5_OUT.
Exits when no work is left and ctrain wrote lat/DONE, or at the certification deadline.
"""
import glob
import json
import os
import sys
import time
import traceback

import numpy as np

import c5

CL, LP = c5.setup_paths(closure=True)
WID = sys.argv[1] if len(sys.argv) > 1 else "0"
LAT = c5.work_dir("lat")
CERT = c5.work_dir("cert")
OUTC = c5.out_dir("cert")
OUTI = c5.out_dir("items")
T0 = time.time()
LAMS = (1e-4, 1e-2, 1.0, 1e2)
G = c5.G
NB = G * G
TSTRIDE = 1 if c5.TINY else 2
MODES = ("loc1", "loc1q", "loc9", "glob")


def log(*a):
    c5.progress(f"[ccert {WID} {time.time() - T0:7.1f}s] " + " ".join(str(x) for x in a))


def _std(A):
    s = A.std(0)
    keep = s > 1e-9 * max(float(s.max()), 1e-30)
    return (A[:, keep] - A[:, keep].mean(0)) / s[keep], int(keep.sum())


def cv_r2(X, Y, groups):
    """Round 4's agreement metric: cross-validated ridge R^2 of Y on X (columns standardised, equal weight per Y
    column), pooled SSE / SST over held-out trajectory folds; the penalty minimising the pooled SSE."""
    X, kx = _std(X)
    Y, ky = _std(Y)
    if kx == 0 or ky == 0:
        return None
    sse = np.zeros(len(LAMS))
    sst = 0.0
    for f in np.unique(groups):
        tr, te = groups != f, groups == f
        mx, my = X[tr].mean(0), Y[tr].mean(0)
        Xc = X[tr] - mx
        ev, U = np.linalg.eigh(Xc.T @ Xc)
        UB = U.T @ (Xc.T @ (Y[tr] - my))
        Xt = (X[te] - mx) @ U
        for i, lam in enumerate(LAMS):
            P = Xt @ (UB / (ev + lam * tr.sum())[:, None]) + my
            sse[i] += ((Y[te] - P) ** 2).sum()
        sst += ((Y[te] - my) ** 2).sum()
    return float(1 - sse.min() / sst)


def block_rows(Z, c):
    """(n, c * 64) channel-major -> (n, 64, c)."""
    return Z.reshape(len(Z), c, NB).transpose(0, 2, 1)


def loc_features(Z, c, mode):
    """Per-block readout inputs (n * 64, d): loc1 the block's own c numbers; loc1q plus squares and products;
    loc9 the 3 x 3 periodic neighbourhood (9 c)."""
    if mode == "loc9":
        Zg = Z.reshape(len(Z), c, G, G)
        F = np.stack([np.roll(Zg, (-dy, -dx), (2, 3)) for dy in (-1, 0, 1) for dx in (-1, 0, 1)], 1)   # (n, 9, c, 8, 8)
        return F.reshape(len(Z), 9 * c, NB).transpose(0, 2, 1).reshape(-1, 9 * c)
    X = block_rows(Z, c).reshape(-1, c)
    if mode == "loc1q":
        X = (X - X.mean(0)) / np.maximum(X.std(0), 1e-300)
        X = np.concatenate([X] + [(X[:, i] * X[:, j])[:, None] for i in range(c) for j in range(i, c)], 1)
    return X


def local_r2(X, Y, fold):
    """Cross-validated least-squares R^2 of Y (m, k) on X (m, d) with an intercept; rows grouped by fold (m,);
    pooled SSE / SST over held-out folds with standardised Y columns. Normal equations per fold, tiny ridge."""
    sx, sy = X.std(0), Y.std(0)
    kx, ky = sx > 1e-9 * max(float(sx.max()), 1e-30), sy > 1e-9 * max(float(sy.max()), 1e-30)
    if not kx.any() or not ky.any():
        return None
    X = (X[:, kx] - X[:, kx].mean(0)) / sx[kx]
    Y = (Y[:, ky] - Y[:, ky].mean(0)) / sy[ky]
    X1 = np.concatenate([X, np.ones((len(X), 1))], 1)
    folds = np.unique(fold)
    XtX = {f: X1[fold == f].T @ X1[fold == f] for f in folds}
    XtY = {f: X1[fold == f].T @ Y[fold == f] for f in folds}
    A, B = sum(XtX.values()), sum(XtY.values())
    sse = sst = 0.0
    d = X1.shape[1]
    for f in folds:
        Atr, Btr = A - XtX[f], B - XtY[f]
        W = np.linalg.solve(Atr + 1e-8 * np.trace(Atr) / d * np.eye(d), Btr)
        te = fold == f
        ntr = Atr[-1, -1]
        my = Btr[-1] / ntr                                           # training mean of Y
        sse += ((Y[te] - X1[te] @ W) ** 2).sum()
        sst += ((Y[te] - my) ** 2).sum()
    return float(1 - sse / sst)


def agreement(Z, cz, H, ch_, fold_frames):
    """All readout modes, both directions, between latent Z (n, cz * 64) and hand design H (n, ch_ * 64)."""
    fold_b = np.repeat(fold_frames, NB)
    out = {}
    tz, th = block_rows(Z, cz).reshape(-1, cz), block_rows(H, ch_).reshape(-1, ch_)
    for mode in ("loc1", "loc1q", "loc9"):
        out[mode] = {"H_from_Z": local_r2(loc_features(Z, cz, mode), th, fold_b),
                     "Z_from_H": local_r2(loc_features(H, ch_, mode), tz, fold_b)}
    out["glob"] = {"H_from_Z": cv_r2(Z, H, fold_frames), "Z_from_H": cv_r2(H, Z, fold_frames)}
    return out


def nontriv(Zt, c):
    Jn, T, q = Zt.shape
    Z = Zt.reshape(-1, q)
    s = Z.std(0)
    keep = s > 1e-9 * max(float(s.max()), 1e-30)
    r_dyn = float(np.mean(Zt[..., keep].var(1).mean(0) / Z[:, keep].var(0)))
    C = np.corrcoef(Z[:, keep].T) if keep.sum() > 1 else np.ones((1, 1))
    ev = np.clip(np.linalg.eigvalsh(np.atleast_2d(C)), 0, None)
    out = {"r_dyn": r_dyn, "participation_ratio": float(ev.sum() ** 2 / (ev ** 2).sum()), "n_nonconst": int(keep.sum())}
    # the box mean of each channel: its share of the variance and how much it moves within a trajectory
    Zc = Zt.reshape(Jn, T, c, NB)
    gm = Zc.mean(-1)                                                 # (J, T, c)
    v_all = Zc.transpose(0, 1, 3, 2).reshape(-1, c).var(0)           # pooled over trajectories, ticks, blocks
    v_all = np.maximum(v_all, 1e-300)
    out["box_mean_var_share"] = (gm.reshape(-1, c).var(0) / v_all).tolist()            # 1/64 for independent blocks
    out["box_mean_time_var_x64"] = (64 * gm.var(1).mean(0) / v_all).tolist()            # 0 if the box sum is conserved
    out["box_mean_drift_sd"] = (np.abs(gm[:, -1] - gm[:, 0]).mean(0) / np.sqrt(v_all)).tolist()
    Zs = (Zc - Zc.mean((0, 1, 3), keepdims=True)) / np.sqrt(v_all)[None, None, :, None]
    out["block_autocorr"] = {str(h): [float(np.mean(Zs[:, :-h, k] * Zs[:, h:, k])) for k in range(c)] for h in c5.HZ}
    return out


_HAND = {}


def hand_Zt(k, ch):
    if (k, ch) not in _HAND:
        d = np.load(f"{LAT}/hand_{k}__cert{ch}.npz")
        _HAND[(k, ch)] = (d["Zt"].astype(np.float64)[:, ::TSTRIDE], int(d["gshape"][0]))
    return _HAND[(k, ch)]


def process(path):
    t1 = time.time()
    stem = os.path.basename(path)[:-4]
    d = np.load(path)
    meta = json.loads(str(d["meta"]))
    Zt, ZB = d["Zt"].astype(np.float64), d["ZB"].astype(np.float64)
    gshape = tuple(int(v) for v in d["gshape"])
    c = gshape[0]
    ch = stem.rsplit("__cert", 1)[1]
    res = {"stem": stem, "meta": {k: v for k, v in meta.items() if k != "val_hist"}, "q": int(Zt.shape[-1])}
    cert = LP.certify(Zt, ZB, gshape=gshape)
    names = sorted(cert["err"])
    np.savez(f"{CERT}/{stem}.npz", names=np.array(names), err=np.stack([cert["err"][n] for n in names]),
             orac=cert["orac"], item_j=cert["item_j"])
    np.savez_compressed(f"{OUTI}/{stem}.npz", names=np.array(names),
                        err=np.stack([cert["err"][n] for n in names]).astype(np.float32),
                        orac=cert["orac"].astype(np.float32), item_j=cert["item_j"])
    res["ld"] = {k: (np.asarray(v).tolist() if not isinstance(v, list) else v) for k, v in cert["ld"].items()}
    res["n_eff"] = cert["n_eff"]
    t_cert = time.time() - t1
    res["nontriv"] = nontriv(Zt, c)
    Zs = Zt[:, ::TSTRIDE]
    fold_frames = np.repeat(np.arange(Zs.shape[0]) % 4, Zs.shape[1])
    Zf = Zs.reshape(-1, Zs.shape[-1])
    agr = {}
    for k in c5.agree_targets():
        try:
            Hk, chh = hand_Zt(k, ch)
            agr[k] = agreement(Zf, c, Hk.reshape(-1, Hk.shape[-1]), chh, fold_frames)
        except Exception as exc:
            agr[k] = {"error": repr(exc)}
    res["agreement"] = agr
    res["seconds"] = {"certify": t_cert, "total": time.time() - t1}
    c5.jdump(res, f"{CERT}/{stem}.json")
    c5.jdump(res, f"{OUTC}/{stem}.json")
    return res


def claim():
    """Oldest .ready file, hand designs first; atomic rename to .claimed.<WID>."""
    rd = glob.glob(f"{LAT}/*.npz.ready")
    rd.sort(key=lambda p: (0 if os.path.basename(p).startswith("hand_") else 1, os.path.getmtime(p) if os.path.exists(p) else 0))
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
    dl = c5.deadline("cert")
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
            log(f"{res['stem']} q={res['q']} ok in {res['seconds']['total']:.1f}s (certify {res['seconds']['certify']:.1f}s)")
        except Exception as exc:
            log(f"{os.path.basename(p)} FAILED: {exc!r}")
            with open(os.path.join(c5.out_dir(), f"cert_errors_{WID}.txt"), "a") as f:
                f.write(f"{p}\n{traceback.format_exc()}\n")
    log(f"worker exits after {n} items")


if __name__ == "__main__":
    main()
