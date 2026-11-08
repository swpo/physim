"""sbi_net -- a generative level-1 predictor for the gliders exam, trained with the fair energy score.

Input at anchor tick t for horizon h (8 x 8 block grid, periodic):
  coarse view at lags LAGS (3 channels each, divided by the public level-1 scales),
  an object raster at lag 0 (per block: body count; mass-weighted sums of mass, sub-block offset y/x,
  velocity y/x, rg, channel-1 fraction, shape q1/q2), the program's wind over [t, t+h) (sum and
  ramp-weighted sum, 2 components each, in units of sigma_w), broadcast globals (population at LAGS
  centred by public means and divided by the level-2 scales, one-hot h, h/16, optional theta in
  box units) and Gaussian noise (8 global + 4 per block).
Output: a sample of the level-1 change (192 coordinates in scaled units) and of the level-2 change
(population, 3 scaled coordinates). Loss: fair energy score (RMS norm, as vw.scoring) per example
over M_TRAIN samples, level 1 + level 2. Several nets (one per data set) are trained in lockstep with
jax.vmap; each keeps its best parameters on its own held-out episodes (early stopping).
"""
from __future__ import annotations

import math
import time

import jax
import jax.numpy as jnp
import numpy as np

import sbi_lib as SL

G = SL.G
F32 = jnp.float32


class Cfg:
    LAGS = (0, 1, 2, 4, 8)
    HS = (1, 2, 4, 8, 16)
    C = 48
    BLOCKS = 3
    BATCH = 128
    M_TRAIN = 4
    LR = 1e-3
    WD = 1e-4
    CLIP = 1.0
    EVAL_EVERY = 250
    N_VAL = 1024
    NG_NOISE = 8
    NL_NOISE = 4


N_RASTER = 10


# ----------------------------------------------------------------------------- per-tick grids (numpy)
def tick_grids(obs):
    """obs (E, T1, 336) -> Cs (E, T1, G, G, 3) coarse / scales, R (E, T1, G, G, 10) object raster,
    Pop (E, T1, 3) centred, scaled population. float32."""
    y = np.asarray(obs, np.float64)
    E, T1, _ = y.shape
    Cs = (y[..., :SL.NC].reshape(E, T1, 3, G, G) / SL.SC1.reshape(3, G, G)).transpose(0, 1, 3, 4, 2)
    O = y[..., SL.NC:SL.N_OBS].reshape(E, T1, SL.GW.K, SL.GW.NF)
    pres = (O[..., 0] > 0.5).astype(float)
    mass, frac = O[..., 1], O[..., 2]
    Hpx = SL.GW.H
    cx = (np.arctan2(O[..., 4], O[..., 3]) * Hpx / (2 * np.pi)) % Hpx
    cy = (np.arctan2(O[..., 6], O[..., 5]) * Hpx / (2 * np.pi)) % Hpx
    b = Hpx // G
    bi = np.floor(cy / b).astype(int) % G
    bj = np.floor(cx / b).astype(int) % G
    oy = cy / b - np.floor(cy / b) - 0.5
    ox = cx / b - np.floor(cx / b) - 0.5
    w = pres * mass / 150.0
    vals = np.stack([pres, w, w * oy, w * ox, w * O[..., 11] / 2.0, w * O[..., 10] / 2.0, w * O[..., 7] / 6.0,
                     w * frac, w * O[..., 8], w * O[..., 9]], -1)                     # (E, T1, K, 10)
    R = np.zeros((E, T1, G * G, N_RASTER))
    flat = bi * G + bj
    ee, tt = np.meshgrid(np.arange(E), np.arange(T1), indexing="ij")
    for k in range(SL.GW.K):
        np.add.at(R, (ee, tt, flat[..., k]), vals[..., k, :])
    R = R.reshape(E, T1, G, G, N_RASTER)
    Pop = (SL.GW.population(y) - SL.POP_MEAN) / SL.SC2
    return Cs.astype(np.float32), R.astype(np.float32), Pop.astype(np.float32)


def wind_cums(U):
    """U (E, T, NW) -> CU, CtU (E, T+1, G, G, 2): cumulative sums of u_s and of s u_s, in units of sigma_w."""
    U = np.asarray(U, np.float64)
    E, T, _ = U.shape
    Ug = U.reshape(E, T, 2, G, G).transpose(0, 1, 3, 4, 2) / SL.SIG
    s = np.arange(T, dtype=float)[None, :, None, None, None]
    z = np.zeros((E, 1, G, G, 2))
    CU = np.concatenate([z, np.cumsum(Ug, 1)], 1)
    CtU = np.concatenate([z, np.cumsum(Ug * s, 1)], 1)
    return CU.astype(np.float32), CtU.astype(np.float32)


def make_dataset(obs, U, theta_u=None, val_frac=0.1, seed=0, max_lag=None):
    """Arrays for one net: grids, wind cumsums, example index (episode, t, h-index) split by episode."""
    Cs, R, Pop = tick_grids(obs)
    CU, CtU = wind_cums(U)
    E, T1 = Cs.shape[:2]
    lag = max(Cfg.LAGS) if max_lag is None else max_lag
    rng = np.random.default_rng(seed)
    perm = rng.permutation(E)
    n_val = max(1, int(round(val_frac * E))) if E > 1 else 0
    val_ep = np.zeros(E, bool)
    val_ep[perm[:n_val]] = True
    ex = []
    for hi, h in enumerate(Cfg.HS):
        for t in range(lag, T1 - h):
            ex.append(np.stack([np.arange(E), np.full(E, t), np.full(E, hi)], 1))
    ex = np.concatenate(ex) if ex else np.zeros((0, 3), int)
    tr = ex[~val_ep[ex[:, 0]]] if n_val else ex
    va = ex[val_ep[ex[:, 0]]] if n_val else ex[:0]
    if len(va) > Cfg.N_VAL:
        va = va[rng.choice(len(va), Cfg.N_VAL, replace=False)]
    th = np.zeros((E, 4), np.float32) if theta_u is None else np.asarray(theta_u, np.float32)
    return {"Cs": Cs, "R": R, "Pop": Pop, "CU": CU, "CtU": CtU, "th": th, "tr": tr.astype(np.int32),
            "va": va.astype(np.int32), "n_ep": E, "n_val_ep": int(n_val)}


def stack_datasets(dsets):
    """Pad and stack datasets along a leading net axis."""
    E = max(d["Cs"].shape[0] for d in dsets)
    ntr = max(len(d["tr"]) for d in dsets)
    nva = max(max(len(d["va"]) for d in dsets), 1)

    def pad(a, n):
        a = np.asarray(a)
        if len(a) == n:
            return a
        z = np.zeros((n - len(a),) + a.shape[1:], a.dtype)
        return np.concatenate([a, z], 0)
    out = {k: jnp.asarray(np.stack([pad(d[k], E) for d in dsets])) for k in ("Cs", "R", "Pop", "CU", "CtU", "th")}
    out["tr"] = jnp.asarray(np.stack([pad(d["tr"], ntr) for d in dsets]))
    out["va"] = jnp.asarray(np.stack([pad(d["va"], nva) for d in dsets]))
    out["n_tr"] = jnp.asarray(np.array([len(d["tr"]) for d in dsets], np.int32))
    out["n_va"] = jnp.asarray(np.array([len(d["va"]) for d in dsets], np.int32))
    return out


# ----------------------------------------------------------------------------- network
def n_in_channels(cond):
    L = len(Cfg.LAGS)
    return 3 * L + N_RASTER + 4 + 3 * L + len(Cfg.HS) + 1 + (4 if cond else 0) + Cfg.NG_NOISE + Cfg.NL_NOISE


def init_params(key, cond):
    C, cin = Cfg.C, n_in_channels(cond)
    ks = iter(jax.random.split(key, 4 + 2 * Cfg.BLOCKS))

    def conv(k, ci, co, scale=1.0):
        return {"w": (jax.random.normal(k, (3, 3, ci, co), F32) * scale * math.sqrt(2.0 / (9 * ci))),
                "b": jnp.zeros((co,), F32)}

    def dense(k, ci, co, scale=1.0):
        return {"w": jax.random.normal(k, (ci, co), F32) * scale * math.sqrt(1.0 / ci), "b": jnp.zeros((co,), F32)}
    return {"in": conv(next(ks), cin, C),
            "blocks": [{"c1": conv(next(ks), C, C), "c2": conv(next(ks), C, C, 0.2)} for _ in range(Cfg.BLOCKS)],
            "out": dense(next(ks), C, 3, 0.1), "g1": dense(next(ks), C, 64), "g2": dense(next(ks), 64, 3, 0.1)}


def _conv(x, p):
    xp = jnp.pad(x, ((0, 0), (1, 1), (1, 1), (0, 0)), mode="wrap")
    y = jax.lax.conv_general_dilated(xp, p["w"], (1, 1), "VALID", dimension_numbers=("NHWC", "HWIO", "NHWC"))
    return y + p["b"]


def apply(params, x):
    """x (N, G, G, cin) -> d1 (N, G, G, 3), d2 (N, 3)."""
    h = jax.nn.gelu(_conv(x, params["in"]))
    for blk in params["blocks"]:
        h = h + _conv(jax.nn.gelu(_conv(h, blk["c1"])), blk["c2"])
    h = jax.nn.gelu(h)
    d1 = h @ params["out"]["w"] + params["out"]["b"]
    g = jax.nn.gelu(h.mean((1, 2)) @ params["g1"]["w"] + params["g1"]["b"])
    d2 = g @ params["g2"]["w"] + params["g2"]["b"]
    return d1, d2


# ----------------------------------------------------------------------------- inputs and loss
def build_inputs(D, e, t, hi, key, m, cond, theta=None):
    """Inputs for examples (e, t, hi) (n,) of one dataset D, m noise draws each -> (n*m, G, G, cin)
    and the base (n, ...) arrays; theta (n, 4) overrides D['th'][e] when given."""
    HS = jnp.asarray(Cfg.HS)
    LAGS = jnp.asarray(Cfg.LAGS)
    n = e.shape[0]
    h = HS[hi]
    tl = t[:, None] - LAGS[None]                                          # (n, L)
    cs = D["Cs"][e[:, None], tl]                                          # (n, L, G, G, 3)
    cs = jnp.moveaxis(cs, 1, 3).reshape(n, G, G, -1)
    r = D["R"][e, t]
    cu1 = D["CU"][e, t + h] - D["CU"][e, t]
    ct1 = D["CtU"][e, t + h] - D["CtU"][e, t]
    hf = h.astype(F32)[:, None, None, None]
    w2 = ((t + h).astype(F32)[:, None, None, None] * cu1 - ct1) / hf
    pop = D["Pop"][e[:, None], tl].reshape(n, -1)
    glob = [pop, jax.nn.one_hot(hi, len(Cfg.HS), dtype=F32), (h.astype(F32) / 16.0)[:, None]]
    if cond:
        glob.append(D["th"][e] if theta is None else theta)
    glob = jnp.concatenate(glob, 1)                                       # (n, ng)
    base = jnp.concatenate([cs, r, cu1, w2], -1)                          # (n, G, G, cb)
    k1, k2 = jax.random.split(key)
    zg = jax.random.normal(k1, (n, m, Cfg.NG_NOISE), F32)
    zl = jax.random.normal(k2, (n, m, G, G, Cfg.NL_NOISE), F32)
    gb = jnp.concatenate([jnp.broadcast_to(glob[:, None], (n, m, glob.shape[1])), zg], -1)
    gb = jnp.broadcast_to(gb[:, :, None, None, :], (n, m, G, G, gb.shape[-1]))
    bb = jnp.broadcast_to(base[:, None], (n, m) + base.shape[1:])
    x = jnp.concatenate([bb, gb, zl], -1)
    return x.reshape((n * m,) + x.shape[2:])


def targets(D, e, t, hi):
    h = jnp.asarray(Cfg.HS)[hi]
    y1 = D["Cs"][e, t + h] - D["Cs"][e, t]
    y2 = D["Pop"][e, t + h] - D["Pop"][e, t]
    return y1.reshape(e.shape[0], -1), y2


def _rms(v):
    return jnp.sqrt(jnp.mean(v ** 2, -1) + 1e-12)


def fair_es(X, y):
    """X (n, m, d) samples, y (n, d) -> (n,) fair energy score with the RMS norm."""
    m = X.shape[1]
    t1 = _rms(X - y[:, None]).mean(1)
    Dxx = _rms(X[:, :, None] - X[:, None, :])
    t2 = Dxx.sum((1, 2)) / (2.0 * m * (m - 1))
    return t1 - t2


def loss_fn(params, D, e, t, hi, key, m, cond):
    x = build_inputs(D, e, t, hi, key, m, cond)
    d1, d2 = apply(params, x)
    n = e.shape[0]
    y1, y2 = targets(D, e, t, hi)
    es1 = fair_es(d1.reshape(n, m, -1), y1)
    es2 = fair_es(d2.reshape(n, m, -1), y2)
    return (es1 + es2).mean(), (es1.mean(), es2.mean())


# ----------------------------------------------------------------------------- multi-net training
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
    return new, {"t": t, "m": mm, "v": vv}, gn


def train_nets(dsets, cond=False, steps=3000, seed=0, log=None, tag=""):
    """Train one net per dataset in lockstep (vmap). Returns (list of best params, info)."""
    K = len(dsets)
    D = stack_datasets(dsets)
    keys = jax.random.split(jax.random.key(seed), K)
    P = jax.vmap(lambda k: init_params(k, cond))(keys)
    zeros = jax.tree_util.tree_map(jnp.zeros_like, P)
    st = {"t": jnp.zeros((K,), F32), "m": zeros, "v": jax.tree_util.tree_map(jnp.zeros_like, P)}
    B, M = Cfg.BATCH, Cfg.M_TRAIN

    def step_one(p, s, Dk, key, lr):
        k1, k2 = jax.random.split(key)
        u = jax.random.uniform(k1, (B,))
        i = jnp.minimum((u * Dk["n_tr"]).astype(jnp.int32), Dk["n_tr"] - 1)
        ex = Dk["tr"][i]
        (l, aux), g = jax.value_and_grad(loss_fn, has_aux=True)(p, Dk, ex[:, 0], ex[:, 1], ex[:, 2], k2, M, cond)
        p, s, gn = _adamw(p, g, s, lr)
        return p, s, l

    def eval_one(p, Dk):
        nv = Dk["va"].shape[0]
        ex = Dk["va"]
        x = build_inputs(Dk, ex[:, 0], ex[:, 1], ex[:, 2], jax.random.key(12345), 8, cond)
        d1, d2 = apply(p, x)
        y1, y2 = targets(Dk, ex[:, 0], ex[:, 1], ex[:, 2])
        es = fair_es(d1.reshape(nv, 8, -1), y1) + fair_es(d2.reshape(nv, 8, -1), y2)
        mask = (jnp.arange(nv) < Dk["n_va"]).astype(F32)
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
            hist.append({"step": it, "train_loss": np.asarray(l).tolist(), "val": v.tolist()})
            if log:
                log(f"  net{tag} step {it}/{steps} train {np.round(np.asarray(l), 4).tolist()} "
                    f"val {np.round(v, 4).tolist()} ({time.time() - t0:.0f}s)")
    params = [jax.tree_util.tree_map(lambda a, k=k: a[k], best) for k in range(K)]
    info = {"best_val": best_val.tolist(), "best_step": best_step.tolist(), "hist": hist,
            "seconds": time.time() - t0, "steps": steps, "n_train_examples": [len(d["tr"]) for d in dsets],
            "n_episodes": [d["n_ep"] for d in dsets]}
    return params, info


# ----------------------------------------------------------------------------- prediction for exam items
def item_dataset(items, H):
    """Item histories (P+1 obs) + programs as a dataset with one episode per item (anchor t = P)."""
    hist = np.stack([np.asarray(it["history"], float) for it in items])            # (n, P+1, 336)
    n, P1, _ = hist.shape
    obs = np.concatenate([hist, np.repeat(hist[:, -1:], H, 1)], 1)                 # future rows unused
    U = np.zeros((n, P1 - 1 + H, SL.NW))
    for i, it in enumerate(items):
        U[i, P1 - 1:] = SL.program_dense(it["program"], H, SL.NW)
    Cs, R, Pop = tick_grids(obs)
    CU, CtU = wind_cums(U)
    return {"Cs": jnp.asarray(Cs), "R": jnp.asarray(R), "Pop": jnp.asarray(Pop), "CU": jnp.asarray(CU),
            "CtU": jnp.asarray(CtU), "th": jnp.zeros((n, 4), F32)}, P1 - 1, hist


_SAMPLE_CACHE = {}


def _sampler(cond, m_inner):
    k = (cond, m_inner)
    if k not in _SAMPLE_CACHE:
        def f(p, D, e, t, hi, key, th):
            return apply(p, build_inputs(D, e, t, hi, key, m_inner, cond, theta=th))
        _SAMPLE_CACHE[k] = jax.jit(f)
    return _SAMPLE_CACHE[k]


def net_samples(params, items, m, seed, hs1, hs2, cond=False, theta_u=None):
    """Samples per item: list of {1: (m, len(hs1), 192), 2: (m, len(hs2), 3)} in the exam's units.
    theta_u (cond nets only): (4,) for all samples, or (n_items, m, 4) per sample (posterior draws)."""
    H = max(Cfg.HS)
    D, P, hist = item_dataset(items, H)
    n = len(items)
    hs = sorted(set(hs1) | set(hs2))
    per_sample = cond and theta_u is not None and np.ndim(theta_u) == 3
    if per_sample:
        e = jnp.asarray(np.repeat(np.arange(n), m))
        th = jnp.asarray(np.asarray(theta_u, np.float32).reshape(n * m, 4))
        m_inner = 1
    else:
        e = jnp.arange(n)
        th = jnp.asarray(np.broadcast_to(np.asarray(theta_u, np.float32), (n, 4))) if cond else None
        m_inner = m
    fn = _sampler(cond, m_inner)
    out1 = np.zeros((n, m, len(hs), SL.NC))
    out2 = np.zeros((n, m, len(hs), 3))
    rng_key = jax.random.key(seed)
    c0 = np.asarray(D["Cs"][:, P])                                                 # (n, G, G, 3)
    pop0 = SL.GW.population(hist[:, -1])                                           # (n, 3)
    for j, h in enumerate(hs):
        hi = Cfg.HS.index(h)
        rng_key, sub = jax.random.split(rng_key)
        d1, d2 = fn(params, D, e, jnp.full(e.shape, P), jnp.full(e.shape, hi), sub, th)
        d1 = np.asarray(d1).reshape(n, m, G, G, 3)
        d2 = np.asarray(d2).reshape(n, m, 3)
        cs = c0[:, None] + d1
        out1[:, :, j] = cs.transpose(0, 1, 4, 2, 3).reshape(n, m, -1) * SL.SC1
        out2[:, :, j] = pop0[:, None] + d2 * SL.SC2
    i1 = [hs.index(h) for h in hs1]
    i2 = [hs.index(h) for h in hs2]
    return [{1: out1[i][:, i1], 2: out2[i][:, i2]} for i in range(n)]
