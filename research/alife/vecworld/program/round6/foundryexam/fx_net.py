"""fx_net -- study foundryexam: the one predictor family of the reference policies (block view).

The round-5 ladder's block net (round5/ladder/ladder_net.py: periodic conv net on the 8 x 8 block grid, 3 x 3
convolutions as matmuls over shifted copies, noise inputs, fair energy score with the RMS norm, several nets
in lockstep with jax.vmap, best held-out parameters kept), changed for worlds that differ in scale and law:

  normalisation  per example by the mean and SD per channel of its own 17-frame history window (ticks
                 t-16..t); the net predicts the change over h ticks in those units
  code           33 summary statistics of a 17-frame window (win_stats). The net receives the code of the
                 example's own window and the mean code of a context set of windows of the same world,
                 both standardised with public constants (D['smu'], D['ssd']), and log2(set size) / 8:
                   mode 'own'     context = the own window (policies C, D, FT, P0)
                   mode 'fixed'   context = own window + D['CN'] windows whose codes sum to D['CS'] (S at test)
                   mode 'random'  context = own window + k windows drawn from the same world's episodes,
                                  k random in {0, 1, 2, ..., 256} (training of the amortised net)
  cfg            (lags, use_code, mode): P0s is lags (0, 1) with use_code False (code inputs zeroed)

Data sets are passed to the jitted functions as arguments, never closed over. float32 throughout.
"""
from __future__ import annotations

import math
import time

import jax
import jax.numpy as jnp
import numpy as np

import fx_lib as FL

G, NB, NCH, NW, SIGW = FL.G, FL.NB, FL.NCH, FL.NW, FL.SIGW
P, H, T1 = FL.P, FL.H, FL.T1
F32 = jnp.float32
NS = 33                              # code length
LAGS_FULL, LAGS_STATE = (0, 1, 2, 4, 8), (0, 1)
KS = (0, 1, 2, 4, 8, 16, 32, 64, 128, 256)


class Cfg:
    HS = FL.HS
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
    EVAL_ROWS = 128
    EVAL_DRAWS = 8
    MAX_LOCK = 16
    KMAX = 256
    MAX_ELEMS = 2 ** 30


# ----------------------------------------------------------------------------- statistics of a window
def win_stats(Xw):
    """Xw (n, 17, G, G, 3) raw block views -> code (n, NS), mean (n, 3), SD floor-protected (n, 3)."""
    mu = Xw.mean((1, 2, 3))
    sd = Xw.std((1, 2, 3))
    sdc = jnp.maximum(sd, 1e-3 * jnp.abs(mu) + 1e-9)
    z = (Xw - mu[:, None, None, None, :]) / sdc[:, None, None, None, :]
    f = [jnp.log(jnp.abs(mu) + 1e-9), jnp.log(sd / (jnp.abs(mu) + 1e-9) + 1e-6)]
    for lag in (1, 2, 4, 8):
        f.append((z[:, lag:] * z[:, :-lag]).mean((1, 2, 3)))
    for dy, dx in ((0, 1), (1, 1), (0, 2)):
        r = 0.5 * (jnp.roll(z, (dy, dx), (2, 3)) + jnp.roll(z, (dx, -dy), (2, 3)))
        f.append((z * r).mean((1, 2, 3)))
    f.append(jnp.stack([(z[..., 0] * z[..., 1]).mean((1, 2, 3)), (z[..., 0] * z[..., 2]).mean((1, 2, 3)),
                        (z[..., 1] * z[..., 2]).mean((1, 2, 3))], -1))
    f.append((z ** 3).mean((1, 2, 3)))
    return jnp.concatenate(f, -1).astype(F32), mu, sdc


_WS = jax.jit(lambda X: win_stats(X)[0])


def episode_stats(X, chunk: int = 2048) -> np.ndarray:
    """X (E, T1, G, G, 3) -> codes of the two windows [0, 16] and [16, 32] of every episode, (E, 2, NS)."""
    E = X.shape[0]
    out = np.zeros((E, 2, NS), np.float32)
    for s in range(0, E, chunk):
        xb = np.asarray(X[s:s + chunk], np.float32)
        n = xb.shape[0]
        if n < chunk and E > chunk:
            xb = np.concatenate([xb, np.repeat(xb[:1], chunk - n, 0)])
        out[s:s + n, 0] = np.asarray(_WS(jnp.asarray(xb[:, :P + 1])))[:n]
        out[s:s + n, 1] = np.asarray(_WS(jnp.asarray(xb[:, P:])))[:n]
    return out


# ----------------------------------------------------------------------------- arrays (numpy)
def _cum0(a):
    return np.concatenate([np.zeros_like(a[:, :1]), np.cumsum(a, 1)], 1).astype(np.float32)


def to_grid(obs):
    """(E, T, NOBS) -> (E, T, G, G, 3) float32."""
    o = np.asarray(obs)
    return o.reshape(o.shape[0], o.shape[1], NCH, G, G).transpose(0, 1, 3, 4, 2).astype(np.float32)


def from_grid(x):
    """(..., G, G, 3) -> (..., NOBS)."""
    return np.moveaxis(x, -1, -3).reshape(x.shape[:-3] + (NCH * NB,))


def base_arrays(obs, U):
    X = to_grid(obs)
    E = X.shape[0]
    Ug = np.asarray(U, np.float64).reshape(E, P + H, 2, G, G).transpose(0, 1, 3, 4, 2) / SIGW
    s = np.arange(P + H, dtype=float)[None, :, None, None, None]
    return {"X": X, "CU": _cum0(Ug), "CtU": _cum0(Ug * s)}


def make_dataset(obs, U, smu, ssd, val_frac=0.1, seed=0, world_of=None, ST=None, EW=None):
    """Arrays of one net and its example index (episode, t, h-index); anchors t in [16, 32 - h]. Held-out
    episodes: a random tenth, or, with world_of (E,), every episode of a random tenth of the worlds.
    ST (E, 2, NS) + EW (episodes per world, world-major order): the tables of mode 'random'."""
    D = base_arrays(obs, U)
    E = D["X"].shape[0]
    rng = np.random.default_rng(seed)
    val_ep = np.zeros(E, bool)
    if world_of is not None:
        ws = np.unique(world_of)
        nv = max(1, int(round(val_frac * len(ws)))) if len(ws) > 1 else 0
        val_ep = np.isin(world_of, rng.permutation(ws)[:nv])
    elif E > 1:
        val_ep[rng.permutation(E)[:max(1, int(round(val_frac * E)))]] = True
    ex = []
    for hi, h in enumerate(Cfg.HS):
        for t in range(P, T1 - h):
            ex.append(np.stack([np.arange(E), np.full(E, t), np.full(E, hi)], 1))
    ex = np.concatenate(ex)
    tr, va = ex[~val_ep[ex[:, 0]]], ex[val_ep[ex[:, 0]]]
    if len(va) > Cfg.N_VAL:
        va = va[rng.choice(len(va), Cfg.N_VAL, replace=False)]
    D.update(tr=tr.astype(np.int32), va=va.astype(np.int32), n_ep=E, n_val_ep=int(val_ep.sum()),
             smu=np.asarray(smu, np.float32), ssd=np.asarray(ssd, np.float32),
             CS=np.zeros((E, NS), np.float32), CN=np.zeros((E,), np.float32))
    if ST is not None:
        D["ST"] = np.asarray(ST, np.float32)
        D["EW"] = np.int32(EW)
    return D


_ARR = ("X", "CU", "CtU", "CS", "CN", "ST")
_CONST = ("smu", "ssd", "EW")


def _nva(n):
    """Rows of the padded validation index: whole chunks of EVAL_ROWS, at least N_VAL (one shape for all nets)."""
    n = max(n, Cfg.N_VAL, 1)
    return -(-n // Cfg.EVAL_ROWS) * Cfg.EVAL_ROWS


def stack_datasets(dsets, pad=None):
    """Pad and stack along a leading net axis (device arrays). pad = (episodes, training rows): pad to at
    least these sizes, so that groups with different data sizes share one compiled program (padding rows are
    never sampled: the example index only names real episodes and n_tr, n_va give the real row counts)."""
    E = max(d["X"].shape[0] for d in dsets)
    ntr = max(len(d["tr"]) for d in dsets)
    if pad is not None:
        E, ntr = max(E, int(pad[0])), max(ntr, int(pad[1]))
    nva = _nva(max(len(d["va"]) for d in dsets))

    def pad(a, n):
        a = np.asarray(a)
        if len(a) == n:
            return a
        return np.concatenate([a, np.zeros((n - len(a),) + a.shape[1:], a.dtype)], 0)
    out = {k: jnp.asarray(np.stack([pad(d[k], E) for d in dsets])) for k in _ARR if k in dsets[0]}
    for k in _CONST:
        if k in dsets[0]:
            out[k] = jnp.asarray(np.stack([d[k] for d in dsets]))
    out["tr"] = jnp.asarray(np.stack([pad(d["tr"], ntr) for d in dsets]))
    out["va"] = jnp.asarray(np.stack([pad(d["va"], nva) for d in dsets]))
    out["n_tr"] = jnp.asarray(np.array([len(d["tr"]) for d in dsets], np.int32))
    out["n_va"] = jnp.asarray(np.array([len(d["va"]) for d in dsets], np.int32))
    for k, v in out.items():
        assert v.size < 2 ** 31, f"device array {k} has {v.size} elements"
    return out


# ----------------------------------------------------------------------------- network
def n_glob():
    return len(Cfg.HS) + 1 + 2 * NS + 1 + Cfg.NG_NOISE


def n_in(lags):
    return 3 * len(lags) + 4 + n_glob() + Cfg.NL_NOISE


def check_elems(lags, n_nets, n_samples, what):
    n = int(n_nets) * int(n_samples) * NB * 9 * max(Cfg.C, n_in(lags))
    if n >= Cfg.MAX_ELEMS:
        raise ValueError(f"{what}: an array of {n:.3g} elements ({n_nets} nets x {n_samples} samples), "
                         f"limit {Cfg.MAX_ELEMS:.3g}")
    return n


def init_params(key, lags):
    cin, C = n_in(lags), Cfg.C
    ks = iter(jax.random.split(key, 16))

    def conv(k, ci, co, scale=1.0):
        return {"w": jax.random.normal(k, (3, 3, ci, co), F32) * scale * math.sqrt(2.0 / (9 * ci)),
                "b": jnp.zeros((co,), F32)}
    return {"in": conv(next(ks), cin, C),
            "blocks": [{"c1": conv(next(ks), C, C), "c2": conv(next(ks), C, C, 0.2)} for _ in range(Cfg.BLOCKS)],
            "out": {"w": jax.random.normal(next(ks), (C, 3), F32) * 0.1 * math.sqrt(1.0 / C), "b": jnp.zeros((3,), F32)}}


def _conv(x, p):
    cols = jnp.concatenate([jnp.roll(x, (-dy, -dx), (1, 2)) for dy in (-1, 0, 1) for dx in (-1, 0, 1)], -1)
    w = p["w"]
    return cols @ w.reshape(9 * w.shape[2], w.shape[3]) + p["b"]


def apply(params, inp):
    h = jax.nn.gelu(_conv(inp, params["in"]))
    for blk in params["blocks"]:
        h = h + _conv(jax.nn.gelu(_conv(h, blk["c1"])), blk["c2"])
    return jax.nn.gelu(h) @ params["out"]["w"] + params["out"]["b"]            # (N, G, G, 3)


def build_inputs(cfg, D, e, t, hi, key, m):
    """Inputs of examples (e, t, hi) (n,) with m noise draws each -> (n * m, G, G, cin), and (mu, sdc)."""
    lags, use_code, mode = cfg
    HSa = jnp.asarray(Cfg.HS)
    n = e.shape[0]
    h = HSa[hi]
    Xw = D["X"][e[:, None], t[:, None] - P + jnp.arange(P + 1)[None]]             # (n, 17, G, G, 3)
    own, mu, sdc = win_stats(Xw)
    k0, k1, k2, k3 = jax.random.split(key, 4)
    if mode == "random":
        EW = D["EW"]
        kk = jnp.asarray(KS)[jax.random.randint(k0, (n,), 0, len(KS))]
        ke, kw = jax.random.split(k3)
        ce = (e // EW)[:, None] * EW + jax.random.randint(ke, (n, Cfg.KMAX), 0, EW)
        cw = jax.random.randint(kw, (n, Cfg.KMAX), 0, 2)
        msk = (jnp.arange(Cfg.KMAX)[None] < kk[:, None]).astype(F32)
        cs = (D["ST"][ce, cw] * msk[..., None]).sum(1)
        cn = kk.astype(F32)
    elif mode == "fixed":
        cs, cn = D["CS"][e], D["CN"][e]
    else:
        cs, cn = jnp.zeros((n, NS), F32), jnp.zeros((n,), F32)
    ctx = (own + cs) / (1.0 + cn)[:, None]
    std = lambda c: jnp.clip((c - D["smu"]) / D["ssd"], -5.0, 5.0)
    code = jnp.concatenate([std(own), std(ctx), jnp.minimum(jnp.log2(1.0 + cn) / 8.0, 1.0)[:, None]], 1)
    if not use_code:
        code = jnp.zeros_like(code)
    xs = (Xw[:, P - jnp.asarray(lags)] - mu[:, None, None, None, :]) / sdc[:, None, None, None, :]    # (n, L, G, G, 3)
    cu = D["CU"][e, t + h] - D["CU"][e, t]
    ct = D["CtU"][e, t + h] - D["CtU"][e, t]
    w2 = ((t + h).astype(F32).reshape(n, 1, 1, 1) * cu - ct) / h.astype(F32).reshape(n, 1, 1, 1)
    glob = jnp.concatenate([jax.nn.one_hot(hi, len(Cfg.HS), dtype=F32), (h.astype(F32) / 16.0)[:, None], code], 1)
    zg = jax.random.normal(k1, (n, m, Cfg.NG_NOISE), F32)
    gb = jnp.concatenate([jnp.broadcast_to(glob[:, None], (n, m, glob.shape[1])), zg], -1)
    base = jnp.concatenate([jnp.moveaxis(xs, 1, 3).reshape(n, G, G, -1), cu, w2], -1).astype(F32)
    zl = jax.random.normal(k2, (n, m, G, G, Cfg.NL_NOISE), F32)
    x = jnp.concatenate([jnp.broadcast_to(base[:, None], (n, m) + base.shape[1:]),
                         jnp.broadcast_to(gb[:, :, None, None, :], (n, m, G, G, gb.shape[-1])), zl], -1)
    return x.reshape((n * m,) + x.shape[2:]), mu, sdc


def _rms(v):
    return jnp.sqrt(jnp.mean(v ** 2, -1) + 1e-12)


def fair_es(X, y):
    m = X.shape[1]
    t1 = _rms(X - y[:, None]).mean(1)
    t2 = _rms(X[:, :, None] - X[:, None, :]).sum((1, 2)) / (2.0 * m * (m - 1))
    return t1 - t2


def _es_examples(params, cfg, D, e, t, hi, key, m):
    inp, mu, sdc = build_inputs(cfg, D, e, t, hi, key, m)
    d = apply(params, inp).reshape(e.shape[0], m, -1)
    h = jnp.asarray(Cfg.HS)[hi]
    tgt = ((D["X"][e, t + h] - D["X"][e, t]) / sdc[:, None, None, :]).reshape(e.shape[0], -1)
    return fair_es(d, tgt)


def loss_fn(params, cfg, D, e, t, hi, key, m):
    return _es_examples(params, cfg, D, e, t, hi, key, m).mean()


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


_FN = {}


def _fns(cfg, keys, shared, batch):
    k = (cfg, keys, shared, batch, Cfg.M_TRAIN, Cfg.EVAL_ROWS, Cfg.EVAL_DRAWS, Cfg.KMAX)
    if k not in _FN:
        B, M = batch, Cfg.M_TRAIN
        ecfg = cfg

        def step_one(p, s, Dk, key, lr):
            k1, k2 = jax.random.split(key)
            u = jax.random.uniform(k1, (B,))
            i = jnp.minimum((u * Dk["n_tr"]).astype(jnp.int32), Dk["n_tr"] - 1)
            ex = Dk["tr"][i]
            l, g = jax.value_and_grad(loss_fn)(p, cfg, Dk, ex[:, 0], ex[:, 1], ex[:, 2], k2, M)
            p, s = _adamw(p, g, s, lr)
            return p, s, l

        R, ND = Cfg.EVAL_ROWS, Cfg.EVAL_DRAWS

        def eval_one(p, Dk):
            nv = Dk["va"].shape[0]
            exc = Dk["va"].reshape(nv // R, R, 3)
            idx = jnp.arange(nv).reshape(nv // R, R)

            def chunk(b):
                ex, ii = b
                kk = jax.random.fold_in(jax.random.key(12345), ii[0])
                es = _es_examples(p, ecfg, Dk, ex[:, 0], ex[:, 1], ex[:, 2], kk, ND)
                mask = (ii < Dk["n_va"]).astype(F32)
                return (es * mask).sum(), mask.sum()
            sm, cn = jax.lax.map(chunk, (exc, idx))
            return sm.sum() / jnp.maximum(cn.sum(), 1.0)
        if shared:
            vstep = jax.jit(jax.vmap(step_one, in_axes=(0, 0, None, 0, None)))
            veval = jax.jit(lambda Pp, D: jax.lax.map(lambda p: eval_one(p, D), Pp))
        else:
            Dax = {kk: 0 for kk in keys}
            vstep = jax.jit(jax.vmap(step_one, in_axes=(0, 0, Dax, 0, None)))
            veval = jax.jit(lambda Pp, D: jax.lax.map(lambda a: eval_one(a[0], a[1]), (Pp, D)))
        _FN[k] = (vstep, veval)
    return _FN[k]


def device_dataset(d, pad=None):
    def padn(a, n):
        a = np.asarray(a)
        if n is None or len(a) >= n:
            return a
        return np.concatenate([a, np.zeros((n - len(a),) + a.shape[1:], a.dtype)], 0)
    E, ntr = (None, None) if pad is None else (int(pad[0]), int(pad[1]))
    out = {k: jnp.asarray(padn(d[k], E)) for k in _ARR if k in d}
    out.update({k: jnp.asarray(d[k]) for k in _CONST if k in d})
    out["tr"], out["va"] = jnp.asarray(padn(d["tr"], ntr)), jnp.asarray(_pad_va(d["va"]))
    out["n_tr"], out["n_va"] = jnp.asarray(np.int32(len(d["tr"]))), jnp.asarray(np.int32(len(d["va"])))
    for k, v in out.items():
        assert v.size < 2 ** 31, f"device array {k} has {v.size} elements"
    return out


def _pad_va(va):
    nva = _nva(len(va))
    return np.concatenate([va, np.zeros((nva - len(va), 3), va.dtype)], 0) if len(va) < nva else va


def train(cfg, dsets, steps, seeds, lr=None, init=None, batch=None, log=None, tag="", deadline=None, eval_every=None,
          pad=None):
    """Train len(seeds) nets in lockstep. dsets: a list of data sets (one per net) or ONE data set shared by
    all nets (seeds differ). init: list of parameter trees to start from (fine-tuning; step 0 is then
    evaluated, so a fine-tuned net is never worse on its held-out episodes than its start).
    Returns (list of best params, info); info['hist'] holds every evaluation of every net."""
    Kn = len(seeds)
    shared = isinstance(dsets, dict)
    lr0 = Cfg.LR if lr is None else lr
    batch = Cfg.BATCH if batch is None else batch
    ee = Cfg.EVAL_EVERY if eval_every is None else eval_every
    if Kn > Cfg.MAX_LOCK:
        raise ValueError(f"{Kn} nets in lockstep, at most {Cfg.MAX_LOCK}")
    check_elems(cfg[0], Kn, batch * Cfg.M_TRAIN, "training step")
    check_elems(cfg[0], 1, Cfg.EVAL_ROWS * Cfg.EVAL_DRAWS, "validation chunk")
    t_call = time.time()
    if shared:
        D = device_dataset(dsets, pad)
        has_val = np.array([dsets["n_val_ep"] > 0] * Kn)
        n_ex, n_ep = [len(dsets["tr"])] * Kn, [dsets["n_ep"]] * Kn
    else:
        assert len(dsets) == Kn
        D = stack_datasets(dsets, pad)
        has_val = np.array([d["n_val_ep"] > 0 for d in dsets])
        n_ex, n_ep = [len(d["tr"]) for d in dsets], [d["n_ep"] for d in dsets]
    vstep, veval = _fns(cfg, tuple(sorted(D)), shared, batch)
    keys = jnp.stack([jax.random.key(int(s)) for s in seeds])
    if init is None:
        Pm = jax.vmap(lambda k: init_params(k, cfg[0]))(keys)
    else:
        Pm = jax.tree_util.tree_map(lambda *a: jnp.stack(a), *init)
    st = {"t": jnp.zeros((Kn,), F32), "m": jax.tree_util.tree_map(jnp.zeros_like, Pm),
          "v": jax.tree_util.tree_map(jnp.zeros_like, Pm)}
    best, best_val, best_step = Pm, np.full(Kn, np.inf), np.zeros(Kn, int)
    hist, t0 = [], time.time()
    key = jax.random.key(int(seeds[0]) * 7919 + 1)
    stopped = None

    def evaluate(it, l):
        nonlocal best, best_val, best_step
        v = np.asarray(veval(Pm, D), np.float64)
        v = np.where(has_val, v, -float(it))
        v = np.where(np.isfinite(v), v, np.inf)
        better = v < best_val
        if better.any():
            bm = jnp.asarray(better)
            best = jax.tree_util.tree_map(
                lambda a, b: jnp.where(bm.reshape((-1,) + (1,) * (a.ndim - 1)), a, b), Pm, best)
            best_val = np.where(better, v, best_val)
            best_step = np.where(better, it, best_step)
        hist.append({"step": it, "train": None if l is None else float(np.nanmean(np.asarray(l))),
                     "val": [float(x) for x in v]})
        return v
    if init is not None:
        evaluate(0, None)
    it = 0
    while it < steps:
        it += 1
        warm = min(1.0, it / 100) if init is None else 1.0
        lr_t = lr0 * warm * (0.1 + 0.9 * 0.5 * (1 + math.cos(math.pi * it / steps)))
        key, sub = jax.random.split(key)
        Pm, st, l = vstep(Pm, st, D, jax.random.split(sub, Kn), lr_t)
        if it % ee == 0 or it == steps:
            v = evaluate(it, l)
            if log and (it % (4 * ee) == 0 or it == steps):
                log(f"  net{tag} step {it}/{steps} train {float(np.nanmean(np.asarray(l))):.4f} "
                    f"val {np.round(v[:6], 4).tolist()} ({time.time() - t0:.0f}s)")
            if deadline is not None and time.time() > deadline and it < steps:
                stopped = it
                break
    params = [jax.tree_util.tree_map(lambda a, k=k: a[k], best) for k in range(Kn)]
    info = {"best_val": best_val.tolist(), "best_step": best_step.tolist(), "hist": hist, "seconds": time.time() - t0,
            "seconds_with_setup": time.time() - t_call, "steps": steps, "stopped_early": stopped, "lr": lr0,
            "batch": batch, "n_train_examples": n_ex, "n_episodes": n_ep, "seeds": [int(s) for s in seeds],
            "cfg": [list(cfg[0]), bool(cfg[1]), cfg[2]], "converged": convergence(hist, steps, init is not None)}
    del D
    return params, info


def convergence(hist, steps, finetune=False):
    """Criterion 6 of DESIGN.md per net: improvement of the held-out loss over the last fifth of the schedule
    as a share of (first - best); converged if below 0.02 (or if the loss never improved on its first value)."""
    if len(hist) < 3:
        return None
    S = np.array([hh["step"] for hh in hist])
    V = np.array([hh["val"] for hh in hist], float)                       # (n_eval, K)
    if not np.isfinite(V).all() or (V < 0).any():
        return None
    first, bestv = V[0], V.min(0)
    i80 = int(np.searchsorted(S, 0.8 * steps, side="left"))
    i80 = min(max(i80, 0), len(S) - 2)
    late = V[i80] - V[i80:].min(0)
    den = np.maximum(first - bestv, 1e-12)
    share = np.where(first - bestv > 1e-9, late / den, 0.0)
    return {"late_share": [float(x) for x in share], "ok": [bool(x < 0.02) for x in share]}


# ----------------------------------------------------------------------------- prediction for exam items
def item_dataset(hist, Ptest, smu, ssd, CS=None, CN=None):
    """Item histories (n, P + 1, NOBS) and test programs (n, H, NW) as a device data set (anchor t = P)."""
    n = hist.shape[0]
    obs = np.concatenate([hist, np.repeat(hist[:, -1:], H, 1)], 1)
    U = np.zeros((n, P + H, NW))
    U[:, P:] = Ptest
    D = {k: jnp.asarray(v) for k, v in base_arrays(obs, U).items()}
    D["smu"], D["ssd"] = jnp.asarray(smu, F32), jnp.asarray(ssd, F32)
    D["CS"] = jnp.zeros((n, NS), F32) if CS is None else jnp.asarray(np.broadcast_to(CS, (n, NS)), F32)
    D["CN"] = jnp.zeros((n,), F32) if CN is None else jnp.full((n,), float(CN), F32)
    return D


_SAMPLER = {}


def net_samples(cfg, params, D, m, seed):
    """(n_items, m, len(HS), NOBS) samples in raw units. cfg mode 'random' is sampled as 'fixed'."""
    cfg = (cfg[0], cfg[1], "fixed" if cfg[2] == "random" else cfg[2])
    k = (cfg, m)
    if k not in _SAMPLER:
        def f(p, D, e, t, hi, key):
            inp, mu, sdc = build_inputs(cfg, D, e, t, hi, key, m)
            d = apply(p, inp).reshape(e.shape[0], m, G, G, 3)
            return (D["X"][e, t][:, None] + d * sdc[:, None, None, None, :])
        _SAMPLER[k] = jax.jit(f)
    fn = _SAMPLER[k]
    n = D["X"].shape[0]
    check_elems(cfg[0], 1, n * m, "sampling")
    e = jnp.arange(n)
    out = np.zeros((n, m, len(Cfg.HS), NCH * NB))
    key = jax.random.key(int(seed))
    for j in range(len(Cfg.HS)):
        key, sub = jax.random.split(key)
        y = np.asarray(fn(params, D, e, jnp.full((n,), P), jnp.full((n,), j), sub), np.float64)
        out[:, :, j] = from_grid(y)
    return out
