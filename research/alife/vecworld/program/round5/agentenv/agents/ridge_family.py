"""ridge_family -- the one predictor family of the reference policies (D, P0, prior mean, S, C).

A direct ridge regression per horizon h on the last three revealed level-1 frames and the test program's inputs
over the horizon, predicting the change of level 1 (and of level 2 where level 2 is not a function of the
predicted level-1 frame). The penalty is chosen per horizon by cross-validation over episodes (4 folds), and the
predictive spread is a resampled table of out-of-fold residual vectors, so the same recipe is usable from a
handful of real episodes (D) to thousands of simulated ones (P0, S, C).
Self-contained numpy: this file is copied into the submission next to predict.py and model.npz.

ring      features: 3 frames (18) + block-summed inputs for every tick of the horizon (6 h) + 1; level 2 is the
          public linear statistic of the sampled level-1 frame.
gliders   the round-3 pilot's patch ridge (program/track2/gliders_exam/pilot.py, vectorised as in
          round4/sbi/sbi_lib.py): per 16-px block, the 3 x 3 block neighbourhood of 3 frames of the coarse view
          and of the summed wind (100 features, weights shared by all blocks); level 2 (count, tracked mass,
          mean speed of the objects readout) by its own small ridge.
"""
import zlib

import numpy as np

# ----------------------------------------------------------------------------- ring
_RG, _RN, _RSIG = 6, 24, 0.3
_ang = 2 * np.pi * np.arange(_RG) / _RG
_RL2 = np.stack([np.ones(_RG), np.cos(_ang), np.sin(_ang)])


def _ring_x(lags, win, sc):
    """lags (n, 3, 6), win (n, h, 24) -> (n, 18 + 6 h + 1)."""
    n = len(lags)
    wb = win.reshape(n, win.shape[1], _RG, _RN // _RG).sum(-1).reshape(n, -1) / _RSIG
    return np.concatenate([(lags / sc).reshape(n, -1), wb, np.ones((n, 1))], 1)


def _rows_ring(Y, U, h, sc1, sc2):
    def rows(j, t):
        lags = np.stack([Y[j, t - l] for l in range(3)], 1)
        win = np.stack([U[j, t + k] for k in range(h)], 1)
        return [(_ring_x(lags, win, sc1)[:, None], ((Y[j, t + h] - Y[j, t]) / sc1)[:, None])]
    return rows


def _predict_ring(M, hist, test, queries, m, rng):
    sc1 = M["sc1"]
    out, lvl1 = {}, {}
    need = sorted(set(t for ts in queries.values() for t in ts))
    for h in need:
        x = _ring_x(hist[None, [-1, -2, -3]], test[None, :h], sc1)[0]
        mu = x @ M[f"W1_{h}"] * sc1 + hist[-1]
        res = M[f"res1_{h}"]
        lvl1[h] = mu[None] + res[rng.integers(0, len(res), m)] * sc1
    for l, ts in queries.items():
        out[l] = np.stack([lvl1[h] if int(l) == 1 else lvl1[h] @ _RL2.T for h in ts], 1)
    return out


# ----------------------------------------------------------------------------- gliders
_G, _NC, _NO, _K, _NF, _SIG, _NW = 8, 192, 144, 12, 12, 0.05, 128
_OFFS = [(dy, dx) for dy in (-1, 0, 1) for dx in (-1, 0, 1)]


def _population(obs):
    """(count, tracked mass, mean speed) of the objects readout: obs (..., 336) -> (..., 3)."""
    S = np.asarray(obs, float)[..., _NC:_NC + _NO]
    S = S.reshape(S.shape[:-1] + (_K, _NF))
    pr = S[..., 0] > 0.5
    n = pr.sum(-1).astype(float)
    mass = np.where(pr, S[..., 1], 0.0).sum(-1)
    sp = np.where(pr, np.hypot(S[..., 10], S[..., 11]), 0.0).sum(-1) / np.maximum(n, 1.0)
    return np.stack([n, mass, sp], -1)


def _nbhd(F):
    return np.concatenate([np.roll(np.roll(F, -dy, -2), -dx, -1) for dy, dx in _OFFS], -3)


def _gl_x1(y3, us, sc1):
    """y3 (N, 3, 336), us (N, 128) -> (N, 64, 100)."""
    N = len(y3)
    sc = sc1.reshape(3, _G, _G)
    fs = [_nbhd(y3[:, l, :_NC].reshape(N, 3, _G, _G) / sc) for l in range(3)]
    fs.append(_nbhd(us.reshape(N, 2, _G, _G) / _SIG))
    X = np.concatenate(fs, 1).reshape(N, -1, _G * _G).transpose(0, 2, 1)
    return np.concatenate([X, np.ones((N, _G * _G, 1))], 2)


def _gl_x2(y3, us, sc2):
    p = _population(y3) / sc2
    nats = 0.5 * (us ** 2).sum(-1) / _SIG ** 2
    return np.concatenate([p.reshape(len(y3), -1), (nats / 100.0)[:, None], np.ones((len(y3), 1))], 1)


def _rows_gliders(Y, U, h, sc1, sc2):
    CU = np.concatenate([np.zeros((Y.shape[0], 1, U.shape[-1])), np.cumsum(U, 1)], 1)
    sc = sc1.reshape(3, _G, _G)

    def rows(j, t):
        y3 = np.stack([Y[j, t], Y[j, t - 1], Y[j, t - 2]], 1)
        us = CU[j, t + h] - CU[j, t]
        T1 = ((Y[j, t + h, :_NC] - Y[j, t, :_NC]).reshape(-1, 3, _G, _G) / sc).reshape(-1, 3, _G * _G).transpose(0, 2, 1)
        T2 = (_population(Y[j, t + h]) - _population(Y[j, t])) / sc2
        return [(_gl_x1(y3, us, sc1), T1), (_gl_x2(y3, us, sc2)[:, None], T2[:, None])]
    return rows


def _predict_gliders(M, hist, test, queries, m, rng):
    sc1, sc2 = M["sc1"], M["sc2"]
    y3 = hist[None, [-1, -2, -3]]
    out = {}
    for l, ts in queries.items():
        arr = []
        for h in ts:
            us = test[:h].sum(0)[None]
            if int(l) == 1:
                mu = (_gl_x1(y3, us, sc1)[0] @ M[f"W1_{h}"]).T.reshape(-1) * sc1 + hist[-1, :_NC]
                res = M[f"res1_{h}"]
                arr.append(mu[None] + res[rng.integers(0, len(res), m)] * sc1)
            else:
                mu = _gl_x2(y3, us, sc2)[0] @ M[f"W2_{h}"] * sc2 + _population(hist[-1])
                res = M[f"res2_{h}"]
                arr.append(mu[None] + res[rng.integers(0, len(res), m)] * sc2)
        out[l] = np.stack(arr, 1)
    return out


# ----------------------------------------------------------------------------- common
LAMS = (0.1, 1.0, 10.0, 100.0, 1000.0, 10000.0)


def _fit_heads(rows, J, T1, h, n_folds, max_res, rng, chunk=2048):
    """Ridge per head with the penalty chosen by cross-validation over episodes, and a table of out-of-fold
    residual vectors (the predictive spread). rows(j, t) -> [(X (n, B, f), T (n, B, o))] per head; the B blocks
    of a head share one weight matrix. Returns [(W (f, o), residuals (n_res, B, o), lambda)]."""
    jj, tt = np.meshgrid(np.arange(J), np.arange(2, T1 - h), indexing="ij")
    jj, tt = jj.ravel(), tt.ravel()
    fold = jj % n_folds
    stats = None
    for s in range(0, len(jj), chunk):
        sl = slice(s, s + chunk)
        heads = rows(jj[sl], tt[sl])
        if stats is None:
            stats = [[[0.0, 0.0, 0.0] for _ in range(n_folds)] for _ in heads]
        for k, (X, T) in enumerate(heads):
            for f in np.unique(fold[sl]):
                m = fold[sl] == f
                A, B = X[m].reshape(-1, X.shape[-1]), T[m].reshape(-1, T.shape[-1])
                st = stats[k][f]
                st[0], st[1], st[2] = st[0] + A.T @ A, st[1] + A.T @ B, st[2] + float((B ** 2).sum())
    out = []
    for st in stats:
        tA, tB = sum(x[0] for x in st), sum(x[1] for x in st)
        eye = np.eye(tA.shape[0])
        best = None
        if n_folds > 1:
            for lam in LAMS:
                Wf, err = [], 0.0
                for A, B, bb in st:
                    Wk = np.linalg.solve(tA - A + lam * eye, tB - B)
                    err += bb - 2 * float((Wk * B).sum()) + float((Wk * (A @ Wk)).sum())
                    Wf.append(Wk)
                if best is None or err < best[0]:
                    best = (err, lam, Wf)
            lam, Wf = best[1], best[2]
        else:
            lam = 1.0
            Wf = [np.linalg.solve(tA + lam * eye, tB)]
        out.append([np.linalg.solve(tA + lam * eye, tB), Wf, lam])
    keep = np.sort(rng.choice(len(jj), size=min(max_res, len(jj)), replace=False))
    res = [[] for _ in out]
    for s in range(0, len(keep), chunk):
        j, t = jj[keep[s:s + chunk]], tt[keep[s:s + chunk]]
        for k, (X, T) in enumerate(rows(j, t)):
            Wsel = np.stack(out[k][1])[j % n_folds]                         # (n, f, o) out-of-fold weights
            res[k].append(T - np.einsum("nbf,nfo->nbo", X, Wsel))
    return [(o[0], np.concatenate(r), o[2]) for o, r in zip(out, res)]


def fit(world, obs, U, queries, scales, max_res=4000, seed=0, n_folds=4) -> dict:
    """obs (J, T + 1, n_obs), U (J, T, n_in) training episodes -> model (dict of arrays)."""
    Y, U = np.asarray(obs, float), np.asarray(U, float)
    hs = sorted(set(int(t) for ts in queries.values() for t in ts))
    rng = np.random.default_rng(seed)
    sc1, sc2 = np.asarray(scales[1], float), np.asarray(scales[2], float)
    J, T1 = Y.shape[:2]
    nf = max(1, min(int(n_folds), J))
    model, lams = {}, []
    for h in hs:
        rows = (_rows_ring if world == "ring" else _rows_gliders)(Y, U, h, sc1, sc2)
        heads = _fit_heads(rows, J, T1, h, nf, max_res, rng)
        for k, (Wt, res, lam) in enumerate(heads):
            r = res.transpose(0, 2, 1).reshape(len(res), -1) if res.shape[1] > 1 else res[:, 0]
            model[f"W{k + 1}_{h}"], model[f"res{k + 1}_{h}"] = Wt.astype(np.float32), r.astype(np.float32)
            lams.append(lam)
    model.update({"world": np.array(world), "sc1": sc1, "sc2": sc2, "hs": np.array(hs), "lams": np.array(lams)})
    return model


def load(path) -> dict:
    z = np.load(path, allow_pickle=False)
    return {k: (str(z[k]) if k == "world" else np.asarray(z[k], float)) for k in z.files}


def predict(M, history, test, queries, n_samples, seed) -> dict:
    hist, test = np.asarray(history, float), np.asarray(test, float)
    rng = np.random.default_rng([int(seed), zlib.crc32(np.ascontiguousarray(hist).tobytes())])
    f = _predict_ring if M["world"] == "ring" else _predict_gliders
    return f(M, hist, test, {int(l): [int(t) for t in ts] for l, ts in queries.items()}, int(n_samples), rng)


PREDICT_PY = '''"""Submission of the scripted reference policy: ridge_family on model.npz."""
import os

import ridge_family as RF

_M = None


def predict(history, program, queries, n_samples, seed):
    global _M
    if _M is None:
        _M = RF.load(os.path.join(os.path.dirname(os.path.abspath(__file__)), "model.npz"))
    return RF.predict(_M, history, program["test"], queries, n_samples, seed)
'''
