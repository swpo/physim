"""bcert -- CPU certification worker of the round-4 study `bias` (see b4.py). Several run in parallel.

usage: python -B bcert.py WORKER_ID
Claims latent files $B4_WORK/lat/<phi>__cert<h>.npz (atomic rename of the .ready marker; hand designs first) and
certifies each with the SAME fixed predictor family as learned_phi2 (lphi.certify: closure_lib.closure_ext, the
VW-0 family mean / persistence / AR(1) / ridge on 1, 2, 4, 8 lags / kNN, per-coordinate standardisation, 4 folds
by trajectory, plus the local equivariant ridge 'lridge' on the 8 x 8 grid; MLP off) against the branch futures at
h = 1, 2, 4, 8, 16, with the Gaussian log-det measures. Also on the certification half's base trajectories:
non-triviality (within-trajectory variance share, participation ratio) and agreement with every hand design,
R^2(H | Z) and R^2(Z | H), cross-validated ridge (4 folds by trajectory, penalty from a grid).
-> $B4_WORK/cert/<stem>.npz (per-item errors, oracle, item trajectories), <stem>.json; JSON also in $B4_OUT/cert/.
Exits when no work is left and btrain wrote lat/DONE, or at the certification deadline.
"""
import glob
import json
import os
import sys
import time
import traceback

import numpy as np

import b4

CL, LP = b4.setup_paths(closure=True)
WID = sys.argv[1] if len(sys.argv) > 1 else "0"
LAT = b4.work_dir("lat")
CERT = b4.work_dir("cert")
OUTC = b4.out_dir("cert")
OUTI = b4.out_dir("items")
T0 = time.time()
LAMS = (1e-4, 1e-2, 1.0, 1e2)


def log(*a):
    b4.progress(f"[bcert {WID} {time.time() - T0:7.1f}s] " + " ".join(str(x) for x in a))


def _std(A):
    s = A.std(0)
    keep = s > 1e-9 * max(float(s.max()), 1e-30)
    return (A[:, keep] - A[:, keep].mean(0)) / s[keep], int(keep.sum())


def cv_r2(X, Y, groups):
    """Cross-validated ridge R^2 of Y on X (columns standardised, equal weight per Y column), pooled SSE / SST
    over held-out trajectory folds; the penalty (relative to the fold size) minimising the pooled SSE."""
    X, kx = _std(X)
    Y, ky = _std(Y)
    if kx == 0 or ky == 0:
        return {"R2": 0.0 if ky else None, "lam": None}
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
    i = int(np.argmin(sse))
    return {"R2": float(1 - sse[i] / sst), "lam": LAMS[i]}


def nontriv(Zt):
    J, T, q = Zt.shape
    Z = Zt.reshape(-1, q)
    s = Z.std(0)
    keep = s > 1e-9 * max(float(s.max()), 1e-30)
    r_dyn = float(np.mean(Zt[..., keep].var(1).mean(0) / Z[:, keep].var(0)))
    C = np.corrcoef(Z[:, keep].T) if keep.sum() > 1 else np.ones((1, 1))
    ev = np.clip(np.linalg.eigvalsh(np.atleast_2d(C)), 0, None)
    return {"r_dyn": r_dyn, "participation_ratio": float(ev.sum() ** 2 / (ev ** 2).sum()), "n_nonconst": int(keep.sum())}


_HAND = {}


def hand_Zt(k, ch):
    if (k, ch) not in _HAND:
        _HAND[(k, ch)] = np.load(f"{LAT}/hand_{k}__cert{ch}.npz")["Zt"].astype(np.float64)
    return _HAND[(k, ch)]


def process(path):
    t1 = time.time()
    stem = os.path.basename(path)[:-4]
    d = np.load(path)
    meta = json.loads(str(d["meta"]))
    Zt, ZB = d["Zt"].astype(np.float64), d["ZB"].astype(np.float64)
    gshape = tuple(int(v) for v in d["gshape"])
    ch = stem.rsplit("__cert", 1)[1]
    res = {"stem": stem, "meta": meta, "q": int(Zt.shape[-1])}
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
    groups = np.repeat(np.arange(Zt.shape[0]) % 4, Zt.shape[1])
    Zf = Zt.reshape(-1, Zt.shape[-1])
    res["nontriv"] = nontriv(Zt)
    agr = {}
    for k in b4.HAND:
        try:
            Hk = hand_Zt(k, ch)
            H = Hk.reshape(-1, Hk.shape[-1])
            agr[k] = {"R2_H_from_Z": cv_r2(Zf, H, groups), "R2_Z_from_H": cv_r2(H, Zf, groups)}
        except Exception as exc:
            agr[k] = {"error": repr(exc)}
    res["agreement"] = agr
    res["seconds"] = {"certify": t_cert, "total": time.time() - t1}
    b4.jdump(res, f"{CERT}/{stem}.json")
    b4.jdump(res, f"{OUTC}/{stem}.json")
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
    dl = b4.deadline("cert")
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
            log(f"{res['stem']} q={res['q']} ceiling-input ok in {res['seconds']['total']:.1f}s")
        except Exception as exc:
            log(f"{os.path.basename(p)} FAILED: {exc!r}")
            with open(os.path.join(b4.out_dir(), f"cert_errors_{WID}.txt"), "a") as f:
                f.write(f"{p}\n{traceback.format_exc()}\n")
    log(f"worker exits after {n} items")


if __name__ == "__main__":
    main()
