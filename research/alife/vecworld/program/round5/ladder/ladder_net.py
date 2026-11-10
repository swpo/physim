"""ladder_net -- one generative predictor per observed view, trained with the fair energy score.

The round-4 net (round4/sbi/sbi_net.py: noise inputs, fair energy score with the RMS norm, several nets
trained in lockstep with jax.vmap, best held-out parameters kept) restricted to what a cell's agent
observes. Each net sees its own view only and predicts the change of that view over h ticks:

  block   periodic conv net on the 8 x 8 block grid (sbi_net's trunk, the 3 x 3 convolutions written as
          matmuls over shifted copies): block numbers at lags LAGS, the
          program's wind over [t, t+h) (sum and ramp-weighted sum per block), globals, noise -> 192 changes
  object  slot net shared over the 12 slots (two rounds of mean pooling over present slots): a slot's 12
          features at lags LAGS, the program's wind at its block and over the 3 x 3 blocks around it,
          globals, noise -> 144 changes
  pop     MLP: the 5 population numbers at lags LAGS, the program's nats and mean wind over [t, t+h),
          globals, noise -> 5 changes

Globals: one-hot horizon, h / 16, and for conditioned nets theta in box units, zero-padded to 8 (hidden
sets are nested; a parameter that is not hidden sits at 0 = its default). A conditioned net trained on
simulations over the prior box gives the policies C (theta = truth), PM (theta = 0), P0 (theta drawn from
the conditioned prior per sample) and S(N) (theta drawn from the posterior at budget N per sample); the
unconditioned net trained on N Lab episodes is D(N).
"""
from __future__ import annotations

import math
import time

import jax
import jax.numpy as jnp
import numpy as np

import ladder_lib as LL

G, K, NF, NC, NO = LL.G, LL.K, LL.NF, LL.NC, LL.NO
F32 = jnp.float32


class Cfg:
    LAGS = (0, 1, 2, 4, 8)
    HS = (1, 2, 4, 8, 16)
    C = 48              # block net channels
    BLOCKS = 3
    SLOT_H = 128        # object net width
    POP_H = 128         # pop net width
    BATCH = 128
    M_TRAIN = 4
    LR = 1e-3
    WD = 1e-4
    CLIP = 1.0
    EVAL_EVERY = 250
    N_VAL = 1024
    NG_NOISE = 8
    NL_NOISE = 4
    DMAX = LL.DMAX


# ----------------------------------------------------------------------------- arrays (numpy)
def _cum0(a):
    return np.concatenate([np.zeros_like(a[:, :1]), np.cumsum(a, 1)], 1).astype(np.float32)


def view_arrays(view, obs, U, SC):
    """obs (E, T1, 336), U (E, T1 - 1, NW) -> the view's state array X (scaled), wind cumulative sums CU
    and CtU (sum of u_s and of s u_s up to each tick, units of sigma_w), and for objects the slots' blocks."""
    y = np.asarray(obs, np.float64)
    E, T1, _ = y.shape
    Ug = np.asarray(U, np.float64).reshape(E, T1 - 1, 2, G, G).transpose(0, 1, 3, 4, 2) / LL.SIG
    s = np.arange(T1 - 1, dtype=float)
    out = {}
    if view == "block":
        out["X"] = (y[..., :NC].reshape(E, T1, 3, G, G) / LL.SC1.reshape(3, G, G)).transpose(0, 1, 3, 4, 2)
        W = Ug
        sh = s[None, :, None, None, None]
    elif view == "object":
        O = y[..., NC:NC + NO].reshape(E, T1, K, NF)
        out["X"] = O / SC["SCF"]
        out["blk"] = LL.slot_blocks(O).astype(np.int32)
        nb = sum(np.roll(np.roll(Ug, dy, 2), dx, 3) for dy in (-1, 0, 1) for dx in (-1, 0, 1)) / 9.0
        W = np.concatenate([Ug, nb], -1).reshape(E, T1 - 1, G * G, 4)
        sh = s[None, :, None, None]
        out["pthr"] = np.float32(0.5 / SC["SCF"][0])
    else:
        out["X"] = (LL.pop5(y) - SC["POPM"]) / SC["SCP"]
        nats = 0.5 * (Ug ** 2).sum((2, 3, 4)) / 100.0
        W = np.concatenate([nats[..., None], Ug.mean((2, 3))], -1)
        sh = s[None, :, None]
    out["X"] = out["X"].astype(np.float32)
    out["CU"], out["CtU"] = _cum0(W), _cum0(W * sh)
    return out


def make_dataset(view, obs, U, SC, theta_u=None, val_frac=0.1, seed=0):
    """Arrays for one net and its example index (episode, t, h-index), split by episode."""
    D = view_arrays(view, obs, U, SC)
    E, T1 = D["X"].shape[:2]
    lag = max(Cfg.LAGS)
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
    D["th"] = np.zeros((E, Cfg.DMAX), np.float32) if theta_u is None else LL.pad_u(theta_u)
    D.update(tr=tr.astype(np.int32), va=va.astype(np.int32), n_ep=E, n_val_ep=int(n_val))
    return D


_ARR = ("X", "CU", "CtU", "th", "blk")


def stack_datasets(dsets):
    """Pad and stack datasets along a leading net axis (device arrays; passed to the jitted steps as
    arguments, never closed over)."""
    E = max(d["X"].shape[0] for d in dsets)
    ntr = max(len(d["tr"]) for d in dsets)
    nva = max(max(len(d["va"]) for d in dsets), 1)

    def pad(a, n):
        a = np.asarray(a)
        if len(a) == n:
            return a
        return np.concatenate([a, np.zeros((n - len(a),) + a.shape[1:], a.dtype)], 0)
    out = {k: jnp.asarray(np.stack([pad(d[k], E) for d in dsets])) for k in _ARR if k in dsets[0]}
    if "pthr" in dsets[0]:
        out["pthr"] = jnp.asarray(np.array([d["pthr"] for d in dsets], np.float32))
    out["tr"] = jnp.asarray(np.stack([pad(d["tr"], ntr) for d in dsets]))
    out["va"] = jnp.asarray(np.stack([pad(d["va"], nva) for d in dsets]))
    out["n_tr"] = jnp.asarray(np.array([len(d["tr"]) for d in dsets], np.int32))
    out["n_va"] = jnp.asarray(np.array([len(d["va"]) for d in dsets], np.int32))
    for k, v in out.items():
        assert v.size < 2 ** 31, f"device array {k} has {v.size} elements"
    return out


# ----------------------------------------------------------------------------- networks
def n_glob(cond):
    return len(Cfg.HS) + 1 + (Cfg.DMAX if cond else 0) + Cfg.NG_NOISE


def n_in(view, cond):
    L = len(Cfg.LAGS)
    if view == "block":
        return 3 * L + 4 + n_glob(cond) + Cfg.NL_NOISE
    if view == "object":
        return NF * L + 8 + n_glob(cond) + Cfg.NL_NOISE
    return 5 * L + 6 + n_glob(cond)


def _dense(k, ci, co, scale=1.0):
    return {"w": jax.random.normal(k, (ci, co), F32) * scale * math.sqrt(1.0 / ci), "b": jnp.zeros((co,), F32)}


def init_params(view, key, cond):
    cin = n_in(view, cond)
    ks = iter(jax.random.split(key, 16))
    if view == "block":
        C = Cfg.C

        def conv(k, ci, co, scale=1.0):
            return {"w": jax.random.normal(k, (3, 3, ci, co), F32) * scale * math.sqrt(2.0 / (9 * ci)),
                    "b": jnp.zeros((co,), F32)}
        return {"in": conv(next(ks), cin, C),
                "blocks": [{"c1": conv(next(ks), C, C), "c2": conv(next(ks), C, C, 0.2)} for _ in range(Cfg.BLOCKS)],
                "out": _dense(next(ks), C, 3, 0.1)}
    if view == "object":
        Hd = Cfg.SLOT_H
        return {"e1": _dense(next(ks), cin, Hd, 1.4), "e2": _dense(next(ks), Hd, Hd, 1.4),
                "m1": _dense(next(ks), 2 * Hd, Hd, 1.4), "m2": _dense(next(ks), 2 * Hd, Hd, 1.4),
                "out": _dense(next(ks), Hd, NF, 0.1)}
    Hd = Cfg.POP_H
    return {"l1": _dense(next(ks), cin, Hd, 1.4), "l2": _dense(next(ks), Hd, Hd, 1.4),
            "l3": _dense(next(ks), Hd, Hd, 1.4), "out": _dense(next(ks), Hd, 5, 0.1)}


def _lin(x, p):
    return x @ p["w"] + p["b"]


def _conv(x, p):
    """Periodic 3 x 3 convolution as a matmul over the 9 shifted copies of x (N, G, G, ci): under jax.vmap over
    nets this is a batched matmul (gradients of a vmapped lax.conv are very slow; round-4 lesson)."""
    cols = jnp.concatenate([jnp.roll(x, (-dy, -dx), (1, 2)) for dy in (-1, 0, 1) for dx in (-1, 0, 1)], -1)
    w = p["w"]
    return cols @ w.reshape(9 * w.shape[2], w.shape[3]) + p["b"]


def apply(view, params, inp):
    """Inputs from build_inputs -> a sample of the scaled change of the view, (N, dim)."""
    if view == "block":
        h = jax.nn.gelu(_conv(inp, params["in"]))
        for blk in params["blocks"]:
            h = h + _conv(jax.nn.gelu(_conv(h, blk["c1"])), blk["c2"])
        d = _lin(jax.nn.gelu(h), params["out"])
        return d.reshape(d.shape[0], -1)                                   # (N, G * G * 3), layout (G, G, 3)
    if view == "object":
        x, mask = inp["x"], inp["mask"]                                    # (N, K, cin), (N, K, 1)
        den = jnp.maximum(mask.sum(1, keepdims=True), 1.0)
        h = jax.nn.gelu(_lin(jax.nn.gelu(_lin(x, params["e1"])), params["e2"]))
        for nm in ("m1", "m2"):
            c = (h * mask).sum(1, keepdims=True) / den
            h = h + jax.nn.gelu(_lin(jnp.concatenate([h, jnp.broadcast_to(c, h.shape)], -1), params[nm]))
        d = _lin(h, params["out"])
        return d.reshape(d.shape[0], -1)                                   # (N, K * NF), slot-major
    h = jax.nn.gelu(_lin(inp, params["l1"]))
    h = h + jax.nn.gelu(_lin(h, params["l2"]))
    h = h + jax.nn.gelu(_lin(h, params["l3"]))
    return _lin(h, params["out"])


def build_inputs(view, D, e, t, hi, key, m, cond, theta=None):
    """Inputs for examples (e, t, hi) (n,) of one dataset D with m noise draws each (leading axis n * m).
    theta (n, DMAX) overrides D['th'][e] when given (conditioned nets)."""
    HS = jnp.asarray(Cfg.HS)
    LAGS = jnp.asarray(Cfg.LAGS)
    n = e.shape[0]
    h = HS[hi]
    tl = t[:, None] - LAGS[None]
    xs = D["X"][e[:, None], tl]                                            # (n, L, ...)
    cu = D["CU"][e, t + h] - D["CU"][e, t]
    ct = D["CtU"][e, t + h] - D["CtU"][e, t]
    ex = (1,) * (cu.ndim - 1)
    w2 = ((t + h).astype(F32).reshape((n,) + ex) * cu - ct) / h.astype(F32).reshape((n,) + ex)
    glob = [jax.nn.one_hot(hi, len(Cfg.HS), dtype=F32), (h.astype(F32) / 16.0)[:, None]]
    if cond:
        glob.append(D["th"][e] if theta is None else theta)
    k1, k2 = jax.random.split(key)
    zg = jax.random.normal(k1, (n, m, Cfg.NG_NOISE), F32)
    gb = jnp.concatenate([jnp.broadcast_to(jnp.concatenate(glob, 1)[:, None], (n, m, n_glob(cond) - Cfg.NG_NOISE)),
                          zg], -1)                                         # (n, m, ng)
    if view == "block":
        base = jnp.concatenate([jnp.moveaxis(xs, 1, 3).reshape(n, G, G, -1), cu, w2], -1)
        zl = jax.random.normal(k2, (n, m, G, G, Cfg.NL_NOISE), F32)
        x = jnp.concatenate([jnp.broadcast_to(base[:, None], (n, m) + base.shape[1:]),
                             jnp.broadcast_to(gb[:, :, None, None, :], (n, m, G, G, gb.shape[-1])), zl], -1)
        return x.reshape((n * m,) + x.shape[2:])
    if view == "object":
        b = D["blk"][e, t][:, :, None]                                     # (n, K, 1)
        slot = jnp.concatenate([jnp.moveaxis(xs, 1, 2).reshape(n, K, -1),
                                jnp.take_along_axis(cu, b, axis=1), jnp.take_along_axis(w2, b, axis=1)], -1)
        zl = jax.random.normal(k2, (n, m, K, Cfg.NL_NOISE), F32)
        x = jnp.concatenate([jnp.broadcast_to(slot[:, None], (n, m) + slot.shape[1:]),
                             jnp.broadcast_to(gb[:, :, None, :], (n, m, K, gb.shape[-1])), zl], -1)
        mask = (xs[:, 0, :, 0] > D["pthr"]).astype(F32)[:, None, :, None]   # present at lag 0
        mask = jnp.broadcast_to(mask, (n, m, K, 1))
        return {"x": x.reshape(n * m, K, -1), "mask": mask.reshape(n * m, K, 1)}
    base = jnp.concatenate([xs.reshape(n, -1), cu, w2], -1)
    x = jnp.concatenate([jnp.broadcast_to(base[:, None], (n, m, base.shape[-1])), gb], -1)
    return x.reshape(n * m, -1)


def targets(D, e, t, hi):
    h = jnp.asarray(Cfg.HS)[hi]
    return (D["X"][e, t + h] - D["X"][e, t]).reshape(e.shape[0], -1)


def _rms(v):
    return jnp.sqrt(jnp.mean(v ** 2, -1) + 1e-12)


def fair_es(X, y):
    """X (n, m, d) samples, y (n, d) -> (n,) fair energy score with the RMS norm (the training loss; the
    exam's scores come from vw.scoring.energy_fair)."""
    m = X.shape[1]
    t1 = _rms(X - y[:, None]).mean(1)
    t2 = _rms(X[:, :, None] - X[:, None, :]).sum((1, 2)) / (2.0 * m * (m - 1))
    return t1 - t2


def loss_fn(params, view, D, e, t, hi, key, m, cond):
    d = apply(view, params, build_inputs(view, D, e, t, hi, key, m, cond))
    return fair_es(d.reshape(e.shape[0], m, -1), targets(D, e, t, hi)).mean()


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
    return new, {"t": t, "m": mm, "v": vv}


_FN = {}


def _fns(view, cond, keys):
    """Jitted lockstep step and evaluation for (view, cond); the data set is an argument."""
    k = (view, cond, Cfg.BATCH, Cfg.M_TRAIN, Cfg.LAGS, Cfg.HS, keys)
    if k not in _FN:
        B, M = Cfg.BATCH, Cfg.M_TRAIN

        def step_one(p, s, Dk, key, lr):
            k1, k2 = jax.random.split(key)
            u = jax.random.uniform(k1, (B,))
            i = jnp.minimum((u * Dk["n_tr"]).astype(jnp.int32), Dk["n_tr"] - 1)
            ex = Dk["tr"][i]
            l, g = jax.value_and_grad(loss_fn)(p, view, Dk, ex[:, 0], ex[:, 1], ex[:, 2], k2, M, cond)
            p, s = _adamw(p, g, s, lr)
            return p, s, l

        def eval_one(p, Dk):
            ex = Dk["va"]
            nv = ex.shape[0]
            d = apply(view, p, build_inputs(view, Dk, ex[:, 0], ex[:, 1], ex[:, 2], jax.random.key(12345), 8, cond))
            es = fair_es(d.reshape(nv, 8, -1), targets(Dk, ex[:, 0], ex[:, 1], ex[:, 2]))
            mask = (jnp.arange(nv) < Dk["n_va"]).astype(F32)
            return (es * mask).sum() / jnp.maximum(mask.sum(), 1.0)
        Dax = {kk: 0 for kk in keys}
        _FN[k] = (jax.jit(jax.vmap(step_one, in_axes=(0, 0, Dax, 0, None))),
                  jax.jit(jax.vmap(eval_one, in_axes=(0, Dax))))
    return _FN[k]


def train_nets(view, dsets, cond=False, steps=3000, seed=0, log=None, tag="", deadline=None, time_budget=None,
               min_steps=300):
    """Train one net per dataset in lockstep (vmap). Returns (list of best params, info). deadline (epoch
    seconds): training stops at the next evaluation after it (info['stopped_early']). time_budget (seconds,
    counted from the call): after 30 timed steps the number of steps is cut (never below min_steps, never
    raised) so that the whole cosine schedule fits the budget (info['steps'] is the number used)."""
    Kn = len(dsets)
    t_call = time.time()
    steps_asked = steps
    D = stack_datasets(dsets)
    vstep, veval = _fns(view, cond, tuple(sorted(D)))
    keys = jax.random.split(jax.random.key(seed), Kn)
    P = jax.vmap(lambda k: init_params(view, k, cond))(keys)
    st = {"t": jnp.zeros((Kn,), F32), "m": jax.tree_util.tree_map(jnp.zeros_like, P),
          "v": jax.tree_util.tree_map(jnp.zeros_like, P)}
    best, best_val, best_step = P, np.full(Kn, np.inf), np.zeros(Kn, int)
    hist, key, t0 = [], jax.random.key(seed + 1), time.time()
    has_val = np.array([d["n_val_ep"] > 0 for d in dsets])
    stopped = None
    it, t1, probe = 0, None, 30
    while it < steps:
        it += 1
        lr = Cfg.LR * min(1.0, it / 100) * (0.1 + 0.9 * 0.5 * (1 + math.cos(math.pi * it / steps)))
        key, sub = jax.random.split(key)
        P, st, l = vstep(P, st, D, jax.random.split(sub, Kn), lr)
        if time_budget is not None and steps > 2 * probe:
            if it == 1:
                l.block_until_ready()
                t1 = time.time()                          # the first step holds the compilation
            elif it == probe:
                l.block_until_ready()
                dt = (time.time() - t1) / (probe - 1)
                fit = int(0.85 * (time_budget - (time.time() - t_call)) / max(dt, 1e-6))
                new = max(min(steps, fit), min(steps, min_steps))
                if new < steps:
                    if log:
                        log(f"  net{tag} steps {steps} -> {new} ({dt * 1e3:.1f} ms/step, budget {time_budget:.0f}s)")
                    steps = new
        if it % Cfg.EVAL_EVERY == 0 or it == steps:
            v = np.asarray(veval(P, D))
            v = np.where(has_val, v, -it)                 # no held-out episodes: keep the last parameters
            v = np.where(np.isfinite(v), v, np.inf)
            better = v < best_val
            if better.any():
                bm = jnp.asarray(better)
                best = jax.tree_util.tree_map(
                    lambda a, b: jnp.where(bm.reshape((-1,) + (1,) * (a.ndim - 1)), a, b), P, best)
                best_val = np.where(better, v, best_val)
                best_step = np.where(better, it, best_step)
            hist.append({"step": it, "train_loss_mean": float(np.nanmean(np.asarray(l))), "val_mean": float(np.mean(v[np.isfinite(v)])) if np.isfinite(v).any() else None})
            if log and (it % (4 * Cfg.EVAL_EVERY) == 0 or it == steps):
                log(f"  net{tag} step {it}/{steps} train {float(np.nanmean(np.asarray(l))):.4f} "
                    f"val {np.round(v[:8], 4).tolist()} ({time.time() - t0:.0f}s)")
            if deadline is not None and time.time() > deadline and it < steps:
                stopped = it
                break
    params = [jax.tree_util.tree_map(lambda a, k=k: a[k], best) for k in range(Kn)]
    info = {"best_val": best_val.tolist(), "best_step": best_step.tolist(), "hist": hist,
            "seconds": time.time() - t0, "steps": steps, "steps_asked": steps_asked, "stopped_early": stopped,
            "seconds_with_setup": time.time() - t_call,
            "time_budget": time_budget,
            "n_train_examples": [len(d["tr"]) for d in dsets], "n_episodes": [d["n_ep"] for d in dsets]}
    del D
    return params, info


# ----------------------------------------------------------------------------- prediction for exam items
def item_arrays(view, items, H, SC):
    """Item histories (P+1 obs) + programs as arrays with one episode per item (anchor t = P)."""
    hist = np.stack([np.asarray(it["history"], float) for it in items])            # (n, P+1, 336)
    n, P1, _ = hist.shape
    obs = np.concatenate([hist, np.repeat(hist[:, -1:], H, 1)], 1)                 # future rows unused
    U = np.zeros((n, P1 - 1 + H, LL.NW))
    for i, it in enumerate(items):
        U[i, P1 - 1:] = LL.program_dense(it["program"], H, LL.NW)
    A = view_arrays(view, obs, U, SC)
    D = {k: jnp.asarray(v) for k, v in A.items()}
    D["th"] = jnp.zeros((n, Cfg.DMAX), F32)
    return D, P1 - 1, hist


_SAMPLER = {}


def _sampler(view, cond, m_inner):
    k = (view, cond, m_inner, Cfg.LAGS, Cfg.HS)
    if k not in _SAMPLER:
        def f(p, D, e, t, hi, key, th):
            return apply(view, p, build_inputs(view, D, e, t, hi, key, m_inner, cond, theta=th))
        _SAMPLER[k] = jax.jit(f)
    return _SAMPLER[k]


def net_samples(view, params, items, m, seed, hs, SC, cond=False, theta_u=None):
    """(n_items, m, len(hs), dim) samples of the view at the query times, in the exam's units.
    theta_u (conditioned nets): (d,) for all samples, or (n_items, m, d) per sample (prior or posterior draws)."""
    H = max(Cfg.HS)
    D, P, hist = item_arrays(view, items, H, SC)
    n = len(items)
    per_sample = cond and theta_u is not None and np.ndim(theta_u) == 3
    if per_sample:
        e = jnp.asarray(np.repeat(np.arange(n), m))
        th = jnp.asarray(LL.pad_u(theta_u).reshape(n * m, Cfg.DMAX))
        m_inner = 1
    else:
        e = jnp.arange(n)
        th = jnp.asarray(np.broadcast_to(LL.pad_u(theta_u), (n, Cfg.DMAX))) if cond else None
        m_inner = m
    fn = _sampler(view, cond, m_inner)
    dim = LL.DIM[view]
    out = np.zeros((n, m, len(hs), dim))
    key = jax.random.key(seed)
    X0 = np.asarray(D["X"][:, P], np.float64)
    for j, h in enumerate(hs):
        key, sub = jax.random.split(key)
        d = np.asarray(fn(params, D, e, jnp.full(e.shape, P), jnp.full(e.shape, Cfg.HS.index(h)), sub, th),
                       np.float64).reshape(n, m, -1)
        if view == "block":
            cs = (X0[:, None] + d.reshape(n, m, G, G, 3)).transpose(0, 1, 4, 2, 3).reshape(n, m, -1)
            out[:, :, j] = cs * SC["SC1"]
        elif view == "object":
            out[:, :, j] = (X0.reshape(n, 1, -1) + d) * SC["SCO"]
        else:
            out[:, :, j] = (X0[:, None] + d) * SC["SCP"] + SC["POPM"]
    return out
