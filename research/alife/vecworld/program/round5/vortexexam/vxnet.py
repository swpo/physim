"""vxnet -- level-2 predictors for the fed-vortex exam pilot: one feature map, three predictor families.

Example = (episode, anchor state a, horizon h in vxlib.HS). Inputs (all functions of the revealed level-1
history up to a, the public program over [a, a + h) and public constants):
  hist    selected level-1 summaries (vxlib.S2_NAMES) at lags LAGS before a, centred and scaled by public constants
  time    (a - 60) / 100 (time since the labelling)
  law     the replicator terms at a: s (1 - s), 1 - 2 s, and (N - N_ref) / sc_N
  prog    nats / 200, max |u| / 0.05, ticks with input / 4, coefficients used / 4 of the program over [a, a + h)
  h       one-hot
  theta   (conditional predictors only) the hidden parameters in box units
Target: the change of level 2, ((N(a + h) - N(a)) / sc_N, (s_b(a + h) - s_b(a)) / sc_s).

Families (each outputs samples):
  net    an MLP with Gaussian noise inputs, trained with the fair energy score (the exam's rule), as round4/sbi's
         sbi_net (same optimiser, clipping, schedule, early stopping on held-out episodes); several nets (one per
         data set) are trained in lockstep with jax.vmap.
  ridge  linear in the inputs, one model per horizon; samples = mean + resampled joint residuals (the LINEAR
         level-2 predictor of the round-3 closure, with level-1 summaries added).
  law    the level-2 effective law with fitted constants (roadmap policy T): per horizon
             d s_b = b1 s (1 - s) + b2 (1 - 2 s) + e_s,      d N = c0 + c1 (N - N_ref) + e_N
         (replicator-mutator drift for the share, linear relaxation for the count); residuals resampled jointly
         with the share residual scaled by sqrt(s (1 - s) + 0.02). Conditional version: every constant is linear
         in theta (box units). It never runs level 0.
"""
from __future__ import annotations

import math
import time

import jax
import jax.numpy as jnp
import numpy as np

import vxlib as VX

F32 = jnp.float32
LAGS = (0, 1, 2, 4, 8, 16, 32, 64)
HIST = ("N", "s_b", "fb_mass", "fb_mean", "fb_sd", "mixed", "log_mass_tot", "log_mass_mean", "speed_mean",
        "near_lo", "near_hi", "turnover")
# public centring / scaling constants of the history channels and of level 2 (set from job 1; see prior.json)
CONST = {"centre": {"N": 10.0, "s_b": 0.3, "fb_mass": 0.3, "fb_mean": 0.3, "fb_sd": 0.2, "mixed": 0.5,
                    "log_mass_tot": 5.0, "log_mass_mean": 3.0, "speed_mean": 0.5, "near_lo": 0.1, "near_hi": 0.1,
                    "turnover": 1.0},
         "scale": {"N": 3.0, "s_b": 0.3, "fb_mass": 0.3, "fb_mean": 0.3, "fb_sd": 0.15, "mixed": 0.3,
                   "log_mass_tot": 0.5, "log_mass_mean": 0.5, "speed_mean": 0.3, "near_lo": 0.15, "near_hi": 0.15,
                   "turnover": 1.5},
         "sc_N": 3.0, "sc_s": 0.15, "N_ref": 10.0}
A_MIN, STRIDE = 100, 2


def set_const(c):
    for k, v in c.items():
        if isinstance(v, dict):
            CONST[k].update(v)
        else:
            CONST[k] = v


def sc2():
    return np.array([CONST["sc_N"], CONST["sc_s"]], float)


def n_feat(d_theta=0):
    return len(HIST) * len(LAGS) + 1 + 3 + 4 + len(VX.HS) + d_theta


def features(S, U, anchors, theta_u=None):
    """S (E, T+1, n2) summaries, U (E, T, m) programs, anchors: list of states a (same for every episode).
    Returns X (E, A, nh, F) float32, Y (E, A, nh, 2) float32 (NaN where a + h is beyond the episode), and the
    level 2 at the anchors L2a (E, A, 2). theta_u (E, d) appended when given."""
    S = np.asarray(S, np.float32)
    E, T1, _ = S.shape
    ix = {n: i for i, n in enumerate(VX.S2_NAMES)}
    cen = np.array([CONST["centre"][k] for k in HIST], np.float32)
    scl = np.array([CONST["scale"][k] for k in HIST], np.float32)
    Z = (S[..., [ix[k] for k in HIST]] - cen) / scl                              # (E, T1, nH)
    anchors = np.asarray(anchors, int)
    A = len(anchors)
    lag_idx = np.maximum(anchors[:, None] - np.asarray(LAGS)[None], 0)           # (A, L)
    hist = Z[:, lag_idx].reshape(E, A, -1)                                       # (E, A, L * nH)
    n_a, s_a = S[:, anchors, ix["N"]], S[:, anchors, ix["s_b"]]
    tfe = np.broadcast_to(((anchors - VX.LAB_TICK) / 100.0)[None, :, None], (E, A, 1))
    law = np.stack([s_a * (1 - s_a), 1 - 2 * s_a, (n_a - CONST["N_ref"]) / CONST["sc_N"]], -1)
    base = np.concatenate([hist, tfe, law], -1).astype(np.float32)               # (E, A, Fb)
    Uu = np.zeros((E, 0, 1)) if U is None else np.asarray(U, np.float32)
    T = Uu.shape[1]
    nh = len(VX.HS)
    X = np.zeros((E, A, nh, n_feat(0 if theta_u is None else np.shape(theta_u)[-1])), np.float32)
    Y = np.full((E, A, nh, 2), np.nan, np.float32)
    L2 = np.stack([S[..., ix["N"]], S[..., ix["s_b"]]], -1)                      # (E, T1, 2)
    sq = (Uu ** 2).sum(-1) if T else np.zeros((E, 0))
    csq = np.concatenate([np.zeros((E, 1)), np.cumsum(sq, 1)], 1)                # (E, T+1)
    act = np.concatenate([np.zeros((E, 1)), np.cumsum((sq > 0).astype(float), 1)], 1)
    for j, h in enumerate(VX.HS):
        prog = np.zeros((E, A, 4), np.float32)
        for ai, a in enumerate(anchors):
            b = min(a + h, T)
            if b > a:
                prog[:, ai, 0] = (csq[:, b] - csq[:, a]) / (2 * VX.SIGMA_A ** 2) / 200.0
                w = Uu[:, a:b]
                prog[:, ai, 1] = np.abs(w).max((1, 2)) / 0.05
                prog[:, ai, 2] = (act[:, b] - act[:, a]) / 4.0
                prog[:, ai, 3] = (np.abs(w).max(1) > 0).sum(-1) / 4.0
            if a + h < T1:
                Y[:, ai, j] = (L2[:, a + h] - L2[:, a]) / sc2()
        oh = np.zeros((E, A, nh), np.float32)
        oh[..., j] = 1.0
        parts = [base, prog, oh]
        if theta_u is not None:
            parts.append(np.broadcast_to(np.asarray(theta_u, np.float32)[:, None], (E, A, np.shape(theta_u)[-1])))
        X[:, :, j] = np.concatenate(parts, -1)
    return X, Y, L2[:, anchors]


def train_anchors(T1):
    return list(range(A_MIN, T1 - min(VX.HS), STRIDE))


def dataset(S, U, theta_u=None, val_frac=0.1, seed=0, max_val=4096):
    """Training arrays of one data set, split by episode: dict Xtr, Ytr, Xva, Yva, n_ep, n_val_ep."""
    X, Y, _ = features(S, U, train_anchors(S.shape[1]), theta_u)
    E = X.shape[0]
    rng = np.random.default_rng(seed)
    perm = rng.permutation(E)
    n_val = max(1, int(round(val_frac * E))) if E >= 4 else 0
    val = np.zeros(E, bool)
    val[perm[:n_val]] = True

    def flat(sel):
        x, y = X[sel].reshape(-1, X.shape[-1]), Y[sel].reshape(-1, 2)
        ok = np.isfinite(y).all(1)
        return x[ok], y[ok]
    xtr, ytr = flat(~val)
    xva, yva = flat(val) if n_val else (xtr[:0], ytr[:0])
    if len(xva) > max_val:
        k = rng.choice(len(xva), max_val, replace=False)
        xva, yva = xva[k], yva[k]
    return {"Xtr": xtr, "Ytr": ytr, "Xva": xva, "Yva": yva, "n_ep": E, "n_val_ep": int(n_val)}


# ----------------------------------------------------------------------------- net (fair energy score)
class Cfg:
    WIDTH = 128
    DEPTH = 3
    NOISE = 8
    BATCH = 256
    M_TRAIN = 8
    LR = 1e-3
    WD = 1e-4
    CLIP = 1.0
    EVAL_EVERY = 250


def init_params(key, n_in):
    ks = jax.random.split(key, Cfg.DEPTH + 1)
    dims = [n_in + Cfg.NOISE] + [Cfg.WIDTH] * Cfg.DEPTH
    layers = [{"w": jax.random.normal(ks[i], (dims[i], dims[i + 1]), F32) * math.sqrt(2.0 / dims[i]),
               "b": jnp.zeros((dims[i + 1],), F32)} for i in range(Cfg.DEPTH)]
    out = {"w": jax.random.normal(ks[-1], (Cfg.WIDTH, 2), F32) * 0.1 * math.sqrt(1.0 / Cfg.WIDTH),
           "b": jnp.zeros((2,), F32)}
    return {"layers": layers, "out": out}


def apply(params, x, z):
    h = jnp.concatenate([x, z], -1)
    for lyr in params["layers"]:
        h = jax.nn.gelu(h @ lyr["w"] + lyr["b"])
    return h @ params["out"]["w"] + params["out"]["b"]


def _rms(v):
    return jnp.sqrt(jnp.mean(v ** 2, -1) + 1e-12)


def fair_es(X, y):
    """X (n, m, d) samples, y (n, d) -> (n,) fair energy score with the RMS norm (as vw.scoring)."""
    m = X.shape[1]
    t1 = _rms(X - y[:, None]).mean(1)
    Dxx = _rms(X[:, :, None] - X[:, None, :])
    return t1 - Dxx.sum((1, 2)) / (2.0 * m * (m - 1))


def sample(params, x, key, m):
    """x (n, F) -> (n, m, 2) samples of the scaled change."""
    n = x.shape[0]
    z = jax.random.normal(key, (n, m, Cfg.NOISE), F32)
    xb = jnp.broadcast_to(x[:, None], (n, m, x.shape[1]))
    return apply(params, xb, z)


def _adamw(params, grads, st, lr):
    b1, b2, eps = 0.9, 0.999, 1e-8
    gn = jnp.sqrt(sum(jnp.sum(g ** 2) for g in jax.tree_util.tree_leaves(grads)))
    sc = jnp.minimum(1.0, Cfg.CLIP / (gn + 1e-9))
    grads = jax.tree_util.tree_map(lambda g: g * sc, grads)
    t = st["t"] + 1
    mm = jax.tree_util.tree_map(lambda a, g: b1 * a + (1 - b1) * g, st["m"], grads)
    vv = jax.tree_util.tree_map(lambda a, g: b2 * a + (1 - b2) * g * g, st["v"], grads)
    c1, c2 = 1 - b1 ** t, 1 - b2 ** t
    new = jax.tree_util.tree_map(lambda p, a, b: p - lr * (a / c1 / (jnp.sqrt(b / c2) + eps) + Cfg.WD * p),
                                 params, mm, vv)
    return new, {"t": t, "m": mm, "v": vv}


def train_nets(dsets, steps=3000, seed=0, log=None, tag=""):
    """One net per data set, trained in lockstep (vmap); data are passed to the jitted step as arguments.
    Returns (list of best params, info)."""
    K = len(dsets)
    n_in = dsets[0]["Xtr"].shape[1]
    ntr = max(len(d["Xtr"]) for d in dsets)
    nva = max(max(len(d["Xva"]) for d in dsets), 1)

    def pad(a, n):
        a = np.asarray(a, np.float32)
        if len(a) == n:
            return a
        return np.concatenate([a, np.zeros((n - len(a),) + a.shape[1:], np.float32)], 0)
    D = {"Xtr": jnp.asarray(np.stack([pad(d["Xtr"], ntr) for d in dsets])),
         "Ytr": jnp.asarray(np.stack([pad(d["Ytr"], ntr) for d in dsets])),
         "Xva": jnp.asarray(np.stack([pad(d["Xva"], nva) for d in dsets])),
         "Yva": jnp.asarray(np.stack([pad(d["Yva"], nva) for d in dsets])),
         "n_tr": jnp.asarray(np.array([len(d["Xtr"]) for d in dsets], np.int32)),
         "n_va": jnp.asarray(np.array([len(d["Xva"]) for d in dsets], np.int32))}
    keys = jax.random.split(jax.random.key(seed), K)
    P = jax.vmap(lambda k: init_params(k, n_in))(keys)
    st = {"t": jnp.zeros((K,), F32), "m": jax.tree_util.tree_map(jnp.zeros_like, P),
          "v": jax.tree_util.tree_map(jnp.zeros_like, P)}
    B, M = Cfg.BATCH, Cfg.M_TRAIN

    def loss(p, x, y, key):
        return fair_es(sample(p, x, key, M), y).mean()

    def step_one(p, s, Dk, key, lr):
        k1, k2 = jax.random.split(key)
        u = jax.random.uniform(k1, (B,))
        i = jnp.minimum((u * Dk["n_tr"]).astype(jnp.int32), Dk["n_tr"] - 1)
        l, g = jax.value_and_grad(loss)(p, Dk["Xtr"][i], Dk["Ytr"][i], k2)
        p, s = _adamw(p, g, s, lr)
        return p, s, l

    def eval_one(p, Dk):
        es = fair_es(sample(p, Dk["Xva"], jax.random.key(12345), 16), Dk["Yva"])
        mask = (jnp.arange(Dk["Xva"].shape[0]) < Dk["n_va"]).astype(F32)
        return (es * mask).sum() / jnp.maximum(mask.sum(), 1.0)

    Dax = {k: 0 for k in D}
    vstep = jax.jit(jax.vmap(step_one, in_axes=(0, 0, Dax, 0, None)))
    veval = jax.jit(jax.vmap(eval_one, in_axes=(0, Dax)))
    best = P
    best_val = np.full(K, np.inf)
    best_step = np.zeros(K, int)
    hist = []
    key = jax.random.key(seed + 1)
    t0 = time.time()
    has_val = np.array([d["n_val_ep"] > 0 for d in dsets])
    for it in range(1, steps + 1):
        frac = it / steps
        lr = Cfg.LR * min(1.0, it / 100) * (0.1 + 0.9 * 0.5 * (1 + math.cos(math.pi * frac)))
        key, sub = jax.random.split(key)
        P, st, l = vstep(P, st, D, jax.random.split(sub, K), lr)
        if it % Cfg.EVAL_EVERY == 0 or it == steps:
            v = np.asarray(veval(P, D))
            v = np.where(has_val, v, -it)             # no held-out episodes: keep the last parameters
            better = v < best_val
            if better.any():
                bm = jnp.asarray(better)
                best = jax.tree_util.tree_map(lambda a, b: jnp.where(bm.reshape((-1,) + (1,) * (a.ndim - 1)), a, b),
                                              P, best)
                best_val = np.where(better, v, best_val)
                best_step = np.where(better, it, best_step)
            hist.append({"step": it, "train_loss": np.round(np.asarray(l), 5).tolist(), "val": np.round(v, 5).tolist()})
            if log and (it % (4 * Cfg.EVAL_EVERY) == 0 or it == steps):
                log(f"  net{tag} step {it}/{steps} train {np.round(np.asarray(l), 4).tolist()[:8]} "
                    f"val {np.round(v, 4).tolist()[:8]} ({time.time() - t0:.0f}s)")
    params = [jax.tree_util.tree_map(lambda a, k=k: a[k], best) for k in range(K)]
    info = {"best_val": best_val.tolist(), "best_step": best_step.tolist(), "hist": hist[-4:],
            "seconds": time.time() - t0, "steps": steps, "n_train_examples": [len(d["Xtr"]) for d in dsets],
            "n_episodes": [d["n_ep"] for d in dsets]}
    del vstep, veval, D
    return params, info


_SAMPLER = {}


def net_samples(params, X, m, seed):
    """X (n, nh, F) or (n, m, nh, F) (per-sample inputs, e.g. posterior draws of theta) -> (n, m, nh, 2) samples
    of the scaled change."""
    X = np.asarray(X, np.float32)
    per_sample = X.ndim == 4
    n = X.shape[0]
    nh = X.shape[-2]
    if "f" not in _SAMPLER:
        _SAMPLER["f"] = jax.jit(lambda p, x, key, mm: sample(p, x, key, mm), static_argnums=3)
    f = _SAMPLER["f"]
    if per_sample:
        out = f(params, jnp.asarray(X.reshape(n * m * nh, -1)), jax.random.key(seed), 1)
        return np.asarray(out).reshape(n, m, nh, 2)
    out = f(params, jnp.asarray(X.reshape(n * nh, -1)), jax.random.key(seed), m)
    return np.asarray(out).reshape(n, nh, m, 2).transpose(0, 2, 1, 3)


# ----------------------------------------------------------------------------- ridge (linear) and law (T)
def _law_cols(X, d_theta):
    """Columns of the feature vector used by the law: s(1-s), 1-2s, (N - N_ref)/sc_N, and theta."""
    o = len(HIST) * len(LAGS) + 1
    th = X[..., X.shape[-1] - d_theta:] if d_theta else None
    return X[..., o], X[..., o + 1], X[..., o + 2], th


def _h_index(X, d_theta):
    o = len(HIST) * len(LAGS) + 1 + 3 + 4
    return np.argmax(X[..., o:o + len(VX.HS)], -1)


def fit_ridge(ds, lam=1.0, max_res=20000, seed=0):
    """Per horizon: ridge of the scaled change on the inputs (the one-hot dropped) + bias; residual table."""
    X, Y = np.asarray(ds["Xtr"], float), np.asarray(ds["Ytr"], float)
    o = len(HIST) * len(LAGS) + 1 + 3 + 4
    keep = np.r_[np.arange(o), np.arange(o + len(VX.HS), X.shape[1])]
    hi = np.argmax(X[:, o:o + len(VX.HS)], 1)
    rng = np.random.default_rng(seed)
    model = {"keep": keep}
    for j in range(len(VX.HS)):
        sel = hi == j
        A = np.concatenate([X[sel][:, keep], np.ones((sel.sum(), 1))], 1)
        P = lam * np.eye(A.shape[1])
        P[-1, -1] = 0
        W = np.linalg.solve(A.T @ A + P, A.T @ Y[sel])
        res = Y[sel] - A @ W
        if len(res) > max_res:
            res = res[rng.choice(len(res), max_res, replace=False)]
        model[j] = (W, res)
    return model


def ridge_samples(model, X, m, seed):
    """X (n, nh, F) or (n, m, nh, F) -> (n, m, nh, 2)."""
    X = np.asarray(X, float)
    if X.ndim == 3:
        X = np.broadcast_to(X[:, None], (X.shape[0], m) + X.shape[1:])
    n, _, nh, _ = X.shape
    rng = np.random.default_rng(seed)
    out = np.zeros((n, m, nh, 2))
    for j in range(nh):
        W, res = model[j]
        A = np.concatenate([X[:, :, j][..., model["keep"]], np.ones((n, m, 1))], -1)
        out[:, :, j] = A @ W + res[rng.integers(0, len(res), size=(n, m))]
    return out


def _law_design(X, d_theta):
    g, mterm, nd, th = _law_cols(X, d_theta)
    one = np.ones_like(g)
    cs, cn = [g, mterm], [one, nd]
    if d_theta:
        for i in range(d_theta):
            cs += [g * th[..., i], mterm * th[..., i]]
            cn += [th[..., i], nd * th[..., i]]
    return np.stack(cs, -1), np.stack(cn, -1), g


def fit_law(ds, d_theta=0, max_res=20000, seed=0):
    """The level-2 effective law per horizon (module docstring); constants linear in theta if d_theta > 0."""
    X, Y = np.asarray(ds["Xtr"], float), np.asarray(ds["Ytr"], float)
    hi = _h_index(X, d_theta)
    rng = np.random.default_rng(seed)
    model = {"d_theta": d_theta}
    for j in range(len(VX.HS)):
        sel = hi == j
        As, An, g = _law_design(X[sel], d_theta)
        bs = np.linalg.lstsq(As, Y[sel][:, 1], rcond=None)[0]
        bn = np.linalg.lstsq(An, Y[sel][:, 0], rcond=None)[0]
        rs = (Y[sel][:, 1] - As @ bs) / np.sqrt(g + 0.02)
        rn = Y[sel][:, 0] - An @ bn
        res = np.stack([rn, rs], 1)
        if len(res) > max_res:
            res = res[rng.choice(len(res), max_res, replace=False)]
        model[j] = (bs, bn, res)
    return model


def law_samples(model, X, m, seed):
    X = np.asarray(X, float)
    if X.ndim == 3:
        X = np.broadcast_to(X[:, None], (X.shape[0], m) + X.shape[1:])
    n, _, nh, _ = X.shape
    rng = np.random.default_rng(seed)
    out = np.zeros((n, m, nh, 2))
    for j in range(nh):
        bs, bn, res = model[j]
        As, An, g = _law_design(X[:, :, j], model["d_theta"])
        r = res[rng.integers(0, len(res), size=(n, m))]
        out[:, :, j, 0] = An @ bn + r[..., 0]
        out[:, :, j, 1] = As @ bs + r[..., 1] * np.sqrt(g + 0.02)
    return out


def with_theta(X, theta_u):
    """Replace the theta columns of X (n, nh, F) by theta_u: (d,) for all, or (n, m, d) per sample ->
    (n, nh, F) or (n, m, nh, F)."""
    X = np.asarray(X, np.float32)
    th = np.asarray(theta_u, np.float32)
    d = th.shape[-1]
    if th.ndim == 1:
        out = X.copy()
        out[..., -d:] = th
        return out
    n, m = th.shape[:2]
    out = np.broadcast_to(X[:, None], (n, m) + X.shape[1:]).copy()
    out[..., -d:] = th[:, :, None, :]
    return out


def to_level2(samples, L2a):
    """Scaled changes (n, m, nh, 2) + level 2 at the anchor (n, 2) -> level-2 samples; N >= 0, s_b in [0, 1]."""
    y = L2a[:, None, None, :] + np.asarray(samples, float) * sc2()
    y[..., 0] = np.maximum(y[..., 0], 0.0)
    y[..., 1] = np.clip(y[..., 1], 0.0, 1.0)
    return y
