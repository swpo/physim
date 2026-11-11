"""fl_lib -- study foundrylong (round 6): the long-horizon hidden-weights exam on the foundry automaton.

The pilot's modules are reused by import (../foundryexam/fx_lib.py as FL, fx_net.py as NN). Their episode constants
are module globals, so this module sets them BEFORE fx_net is imported: H = 32 test ticks, 49 frames per episode,
query horizons (8, 16, 32). Nothing in the pilot's files is changed.

New here (DECLARED.md, "Training driver"):
  make_ds     a data set with the example index sorted by horizon, and held-out rows per horizon
  train       several nets in lockstep; examples drawn with equal weight per horizon; held-out loss per horizon;
              the best parameters kept PER HORIZON; schedule 'cos75' (warm-up, cosine to a tenth over the first 75%
              of the steps, then held) or 'const'; `take` = fixed steps to keep instead of the best held-out step
  samples_h   samples for exam items, horizon j answered by the parameters kept for horizon j
  ft_cv       fine-tuning tuned by k-fold cross-validation over Lab episodes (rate and steps per world and horizon)

PILOT ONLY: nothing produced with this module may be reused as an exam.
"""
from __future__ import annotations

import math
import os
import sys
import time

sys.dont_write_bytecode = True
HERE = os.path.dirname(os.path.abspath(__file__))
FXDIR = os.path.abspath(os.path.join(HERE, "..", "foundryexam"))
if FXDIR not in sys.path:
    sys.path.insert(0, FXDIR)
if "fx_net" in sys.modules or "fx_lib" in sys.modules:
    raise ImportError("fl_lib must be imported before fx_lib / fx_net (it sets their episode constants)")

import fx_lib as FL  # noqa: E402

H_TEST, HORIZONS = 32, (8, 16, 32)
FL.H = H_TEST
FL.T1 = FL.P + FL.H + 1
FL.HS = HORIZONS

import fx_net as NN  # noqa: E402  (binds P, H, T1 and Cfg.HS from fx_lib at import)

assert (NN.P, NN.H, NN.T1, tuple(NN.Cfg.HS)) == (16, 32, 49, HORIZONS), "fx_net did not take the long-horizon constants"

import jax  # noqa: E402
import jax.numpy as jnp  # noqa: E402
import numpy as np  # noqa: E402

P, H, T1, HS = FL.P, FL.H, FL.T1, FL.HS
NH = len(HS)
G, NB, NCH, NW, NOBS = FL.G, FL.NB, FL.NCH, FL.NW, FL.NOBS
F32 = jnp.float32
C_FULL = (NN.LAGS_FULL, True, "own")
NV_H = 1024                         # held-out rows per horizon, at most
ANCHORS = tuple(T1 - h - P for h in HS)          # anchors per episode and horizon: (25, 17, 1)


class pilot_shape:
    """Context: the pilot's 33-frame episode (H = 16) for the exam-time gate, which is defined on that window."""

    def __enter__(self):
        FL.H, FL.T1 = 16, FL.P + 17
        return self

    def __exit__(self, *a):
        FL.H, FL.T1 = H, T1


# ----------------------------------------------------------------------------- data sets
def make_ds(obs, U, smu, ssd, val_ep=None, val_frac=0.1, seed=0, world_of=None, nv_h=None):
    """Arrays of one net. Example index rows (episode, anchor t, horizon index), anchors t in [16, 49 - h).
    Training rows are sorted by horizon (off, cnt give each horizon's block). Held-out episodes: `val_ep` (bool
    mask), else a random tenth of the episodes, or with world_of every episode of a random tenth of the worlds;
    val_frac = 0: none. Held-out rows: at most nv_h per horizon."""
    nv_h = NV_H if nv_h is None else nv_h
    D = NN.base_arrays(obs, U)
    E = D["X"].shape[0]
    rng = np.random.default_rng(seed)
    if val_ep is None:
        val_ep = np.zeros(E, bool)
        if val_frac > 0:
            if world_of is not None:
                ws = np.unique(world_of)
                nv = max(1, int(round(val_frac * len(ws)))) if len(ws) > 1 else 0
                val_ep = np.isin(world_of, rng.permutation(ws)[:nv])
            elif E > 1:
                val_ep[rng.permutation(E)[:max(1, int(round(val_frac * E)))]] = True
    val_ep = np.asarray(val_ep, bool)
    e_tr, e_va = np.flatnonzero(~val_ep), np.flatnonzero(val_ep)
    tr, va, cnt = [], [], []
    for hi, h in enumerate(HS):
        ts = np.arange(P, T1 - h)

        def rows(es):
            a = np.stack(np.meshgrid(es, ts, indexing="ij"), -1).reshape(-1, 2)
            return np.concatenate([a, np.full((len(a), 1), hi)], 1).astype(np.int32)
        a = rows(e_tr)
        tr.append(a)
        cnt.append(len(a))
        b = rows(e_va)
        if len(b) > nv_h:
            b = b[np.sort(rng.choice(len(b), nv_h, replace=False))]
        va.append(b)
    D.update(tr=np.concatenate(tr), cnt=np.array(cnt, np.int32), off=np.concatenate([[0], np.cumsum(cnt)[:-1]]).astype(np.int32),
             va=np.concatenate(va) if e_va.size else np.zeros((0, 3), np.int32), n_ep=E, n_val_ep=int(val_ep.sum()),
             smu=np.asarray(smu, np.float32), ssd=np.asarray(ssd, np.float32))
    return D


_ARR = ("X", "CU", "CtU")
_CONST = ("smu", "ssd", "cnt", "off")


def _padn(a, n):
    a = np.asarray(a)
    if len(a) >= n:
        return a
    return np.concatenate([a, np.zeros((n - len(a),) + a.shape[1:], a.dtype)], 0)


def _va_arrays(d, nva):
    va = _padn(d["va"], nva)
    w = np.zeros((nva, NH), np.float32)
    n = len(d["va"])
    if n:
        w[np.arange(n), d["va"][:, 2]] = 1.0
    return va, w


def device_data(dsets, pad=None):
    """One data set (shared by all nets) or a list (one per net, stacked on a leading axis). pad = (episodes,
    training rows[, held-out rows]): at least these sizes, so that groups of different size share one compiled
    program. Padding rows are never drawn (cnt, off name real rows only) and carry zero weight in the held-out loss."""
    shared = isinstance(dsets, dict)
    ds = [dsets] if shared else list(dsets)
    E = max(d["X"].shape[0] for d in ds)
    ntr = max(len(d["tr"]) for d in ds)
    if pad is not None:
        E, ntr = max(E, int(pad[0])), max(ntr, int(pad[1]))
    R = NN.Cfg.EVAL_ROWS
    nva = max(len(d["va"]) for d in ds)
    if pad is not None and len(pad) > 2:
        nva = max(nva, int(pad[2]))
    nva = max(R, -(-nva // R) * R)
    cols = {k: [_padn(d[k], E) for d in ds] for k in _ARR}
    cols.update({k: [d[k] for d in ds] for k in _CONST})
    cols["tr"] = [_padn(d["tr"], ntr) for d in ds]
    vv = [_va_arrays(d, nva) for d in ds]
    cols["va"], cols["vw"] = [v[0] for v in vv], [v[1] for v in vv]
    out = {k: jnp.asarray(v[0] if shared else np.stack(v)) for k, v in cols.items()}
    for k, v in out.items():
        assert v.size < 2 ** 31, f"device array {k} has {v.size} elements"
    has_val = np.array([[bool((d["va"][:, 2] == j).any()) if len(d["va"]) else False for j in range(NH)] for d in ds])
    return out, has_val


# ----------------------------------------------------------------------------- training
_FN = {}


def _fns(cfg, shared, batch):
    k = (cfg, shared, batch, NN.Cfg.M_TRAIN, NN.Cfg.EVAL_ROWS, NN.Cfg.EVAL_DRAWS, NN.Cfg.CHUNK)
    if k in _FN:
        return _FN[k]
    B, M = batch, NN.Cfg.M_TRAIN

    def step_one(p, s, Dk, key, lr):
        k1, k2, k3 = jax.random.split(key, 3)
        hi = jax.random.randint(k1, (B,), 0, NH)                       # equal weight per horizon
        c = Dk["cnt"][hi]
        i = Dk["off"][hi] + jnp.minimum((jax.random.uniform(k2, (B,)) * c).astype(jnp.int32), c - 1)
        ex = Dk["tr"][i]
        l, g = jax.value_and_grad(NN.loss_fn)(p, cfg, Dk, ex[:, 0], ex[:, 1], ex[:, 2], k3, M)
        p, s = NN._adamw(p, g, s, lr)
        return p, s, l

    def step_many(p, s, Dk, keys_, lrs):
        def body(c, kl):
            pp, ss, ll = step_one(c[0], c[1], Dk, kl[0], kl[1])
            return (pp, ss), ll
        (p, s), ls = jax.lax.scan(body, (p, s), (keys_, lrs))
        return p, s, ls[-1]

    R, ND = NN.Cfg.EVAL_ROWS, NN.Cfg.EVAL_DRAWS

    def eval_one(p, Dk):
        nv = Dk["va"].shape[0]
        exc = Dk["va"].reshape(nv // R, R, 3)
        wc = Dk["vw"].reshape(nv // R, R, NH)
        first = jnp.arange(nv // R) * R

        def chunk(b):
            ex, w, i0 = b
            es = NN._es_examples(p, cfg, Dk, ex[:, 0], ex[:, 1], ex[:, 2], jax.random.fold_in(jax.random.key(12345), i0), ND)
            return (es[:, None] * w).sum(0), w.sum(0)
        sm, cn = jax.lax.map(chunk, (exc, wc, first))
        return sm.sum(0) / jnp.maximum(cn.sum(0), 1.0)                # (NH,)
    if shared:
        vstep = jax.jit(jax.vmap(step_many, in_axes=(0, 0, None, 0, None)))
        veval = jax.jit(lambda Pp, D: jax.lax.map(lambda p: eval_one(p, D), Pp))
    else:
        vstep = jax.jit(jax.vmap(step_many, in_axes=(0, 0, 0, 0, None)))
        veval = jax.jit(lambda Pp, D: jax.lax.map(lambda a: eval_one(a[0], a[1]), (Pp, D)))
    _FN[k] = (vstep, veval)
    return _FN[k]


def lr_at(i, steps, lr0, sched, warm):
    if sched == "const":
        return lr0
    w = min(1.0, i / 100) if warm else 1.0
    f = min(1.0, i / (0.75 * steps))
    return lr0 * w * (0.1 + 0.9 * 0.5 * (1 + math.cos(math.pi * f)))


def stack_trees(trees):
    return jax.tree_util.tree_map(lambda *a: jnp.stack(a), *trees)


def tree_at(tree, *idx):
    return jax.tree_util.tree_map(lambda a: a[idx], tree)


def train(dsets, steps, seeds, lr=None, init=None, batch=None, sched="cos75", eval_every=None, take=None, pad=None,
          log=None, tag="", deadline=None, cfg=C_FULL):
    """Train len(seeds) nets in lockstep on one shared data set (dict) or one data set per net (list).
    init: list of parameter trees (fine-tuning; step 0 is then a candidate). take: (K, NH) int steps: keep the
    parameters at exactly these steps (a multiple of eval_every; 0 = init) instead of the best held-out step.
    Returns (best, info): best is a parameter tree with leading axes (NH, K); info['val'] = [(step, (K, NH))]."""
    Kn = len(seeds)
    shared = isinstance(dsets, dict)
    lr0 = NN.Cfg.LR if lr is None else lr
    batch = NN.Cfg.BATCH if batch is None else batch
    ee = NN.Cfg.EVAL_EVERY if eval_every is None else eval_every
    CH = NN.Cfg.CHUNK
    if steps % CH or ee % CH:
        raise ValueError(f"train: steps {steps} and eval_every {ee} must be multiples of Cfg.CHUNK = {CH}")
    if Kn > NN.Cfg.MAX_LOCK:
        raise ValueError(f"{Kn} nets in lockstep, at most {NN.Cfg.MAX_LOCK}")
    NN.check_elems(cfg[0], Kn, batch * NN.Cfg.M_TRAIN, "training step")
    NN.check_elems(cfg[0], 1, NN.Cfg.EVAL_ROWS * NN.Cfg.EVAL_DRAWS, "validation chunk")
    t_call = time.time()
    D, has_val = device_data(dsets, pad)
    if shared:
        has_val = np.repeat(has_val, Kn, 0)
    ds = [dsets] * Kn if shared else list(dsets)
    vstep, veval = _fns(cfg, shared, batch)
    keys = jnp.stack([jax.random.key(int(s)) for s in seeds])
    Pm = jax.vmap(lambda k: NN.init_params(k, cfg[0]))(keys) if init is None else stack_trees(init)
    st = {"t": jnp.zeros((Kn,), F32), "m": jax.tree_util.tree_map(jnp.zeros_like, Pm),
          "v": jax.tree_util.tree_map(jnp.zeros_like, Pm)}
    best = jax.tree_util.tree_map(lambda a: jnp.stack([a] * NH), Pm)             # (NH, K, ...)
    best_val, best_step = np.full((Kn, NH), np.inf), np.zeros((Kn, NH), int)
    take = None if take is None else np.asarray(take, int).reshape(Kn, NH)
    hist, t0 = [], time.time()
    key = jax.random.key(int(seeds[0]) * 7919 + 1)

    def keep(mask):                                                               # mask (K, NH) bool
        nonlocal best
        if mask.any():
            bm = jnp.asarray(mask.T)                                              # (NH, K)
            best = jax.tree_util.tree_map(
                lambda b, a: jnp.where(bm.reshape(bm.shape + (1,) * (a.ndim - 1)), a[None], b), best, Pm)

    def evaluate(it, l):
        nonlocal best_val, best_step
        if take is not None:
            keep(take == it)
            return None
        v = np.asarray(veval(Pm, D), np.float64)                                  # (K, NH)
        v = np.where(has_val, v, -float(it))                                      # no held-out rows: the last step
        v = np.where(np.isfinite(v), v, np.inf)
        better = v < best_val
        keep(better)
        best_val = np.where(better, v, best_val)
        best_step = np.where(better, it, best_step)
        hist.append((int(it), v.tolist(), None if l is None else float(np.nanmean(np.asarray(l)))))
        return v
    if init is not None:
        evaluate(0, None)
    it, first, timed, t_steps, stopped = 0, True, 0, 0.0, None
    while it < steps:
        lrs = jnp.asarray([lr_at(i, steps, lr0, sched, init is None) for i in range(it + 1, it + CH + 1)], F32)
        it += CH
        key, sub = jax.random.split(key)
        td = time.time()
        Pm, st, l = vstep(Pm, st, D, jax.random.split(sub, Kn * CH).reshape(Kn, CH), lrs)
        l.block_until_ready()
        if first:
            first = False
        else:
            timed += CH
            t_steps += time.time() - td
        if it % ee == 0 or it == steps:
            v = evaluate(it, l)
            if log and v is not None and (it % (8 * ee) == 0 or it == steps):
                log(f"  net{tag} step {it}/{steps} train {float(np.nanmean(np.asarray(l))):.4f} "
                    f"val(h) {np.round(v[:3], 4).tolist()} ({time.time() - t0:.0f}s)")
            if deadline is not None and time.time() > deadline and it < steps:
                stopped = it
                break
    ms = 1e3 * t_steps / timed if timed else None
    info = {"steps": steps, "sched": sched, "lr": lr0, "batch": batch, "eval_every": ee, "seeds": [int(s) for s in seeds],
            "n_ep": [d["n_ep"] for d in ds], "n_val_ep": [d["n_val_ep"] for d in ds], "cnt": [d["cnt"].tolist() for d in ds],
            "val": hist, "best_step": best_step.tolist(), "best_val": np.where(np.isfinite(best_val), best_val, -1).tolist(),
            "has_val": has_val.tolist(), "ms_per_step": ms, "seconds": time.time() - t0,
            "seconds_with_setup": time.time() - t_call, "stopped_early": stopped,
            "take": None if take is None else take.tolist()}
    if take is None:
        info.update(rule(hist, steps, best_step, has_val, finetune=init is not None))
    del D
    return best, info


def rule(hist, steps, best_step, has_val, finetune=False):
    """DECLARED.md S2 per net and horizon: trained if the best held-out step is in the first 80% of the schedule.
    late_gain: fall of the held-out loss after the 80% point as a share of (first - best) (the pilot's criterion 6)."""
    S = np.array([h[0] for h in hist])
    V = np.array([h[1] for h in hist], float)                                     # (n_eval, K, NH)
    trained = (best_step <= 0.8 * steps) & has_val
    late = np.full(best_step.shape, np.nan)
    if len(S) >= 3 and S[-1] >= 0.8 * steps:
        i80 = min(int(np.searchsorted(S, 0.8 * steps, side="left")), len(S) - 1)
        den = V[0] - V.min(0)
        late = np.where(den > 1e-9, (V[i80] - V[i80:].min(0)) / np.maximum(den, 1e-12), 0.0)
        late = np.where(has_val, late, np.nan)
    return {"trained": trained.tolist(), "late_gain": np.where(np.isfinite(late), late, -1).tolist()}


# ----------------------------------------------------------------------------- prediction for exam items
_SAMPLER = {}


def samples_h(best_k, D, m, seed, cfg=C_FULL):
    """best_k: parameter tree with a leading horizon axis (NH, ...). (n_items, m, NH, NOBS) samples in raw units;
    the query at horizon j is answered by the parameters kept for horizon j."""
    k = (cfg, m)
    if k not in _SAMPLER:
        def f(p, D, e, t, hi, key):
            inp, mu, sdc = NN.build_inputs(cfg, D, e, t, hi, key, m)
            d = NN.apply(p, inp).reshape(e.shape[0], m, G, G, 3)
            return D["X"][e, t][:, None] + d * sdc[:, None, None, None, :]
        _SAMPLER[k] = jax.jit(f)
    fn = _SAMPLER[k]
    n = D["X"].shape[0]
    NN.check_elems(cfg[0], 1, n * m, "sampling")
    e = jnp.arange(n)
    out = np.zeros((n, m, NH, NOBS))
    key = jax.random.key(int(seed))
    for j in range(NH):
        key, sub = jax.random.split(key)
        y = np.asarray(fn(tree_at(best_k, j), D, e, jnp.full((n,), P), jnp.full((n,), j), sub), np.float64)
        out[:, :, j] = NN.from_grid(y)
    return out


def host(tree):
    return jax.tree_util.tree_map(lambda a: np.asarray(a), tree)


def flat_params(tree) -> dict:
    """Parameter tree -> flat dict of numpy arrays (for np.savez); unflat_params is its inverse."""
    out = {}

    def rec(t, pre):
        if isinstance(t, dict):
            for k in sorted(t):
                rec(t[k], pre + [str(k)])
        elif isinstance(t, (list, tuple)):
            for i, v in enumerate(t):
                rec(v, pre + [f"#{i}"])
        else:
            out["/".join(pre)] = np.asarray(t, np.float32)
    rec(tree, [])
    return out


def unflat_params(flat: dict):
    root = {}
    for k, v in flat.items():
        parts = k.split("/")
        d = root
        for p_ in parts[:-1]:
            d = d.setdefault(p_, {})
        d[parts[-1]] = jnp.asarray(v)

    def fix(t):
        if not isinstance(t, dict):
            return t
        if t and all(k.startswith("#") for k in t):
            return [fix(t[f"#{i}"]) for i in range(len(t))]
        return {k: fix(v) for k, v in t.items()}
    return fix(root)


# ----------------------------------------------------------------------------- FT: cross-validated fine-tuning
def ft_cv(lab_obs, lab_U, N, init_k, smu, ssd, seeds, lrs, s_max, folds=4, batch=64, eval_every=50, lock=16, pad=None,
          log=None, tag="", deadline=None):
    """Fine-tune per hidden world on its first N Lab episodes (DECLARED.md, FT(N)).
    lab_obs[i], lab_U[i]: the Lab of world i; init_k[i]: the starting parameters of world i (one tree).
    1. `folds`-fold cross-validation over the N episodes (fold of episode e = e mod folds) for every rate in lrs:
       constant rate, held-out fair energy score per horizon at steps 0, eval_every, ..., s_max.
    2. Per world and horizon the (rate, step) with the lowest mean held-out loss over the folds.
    3. One run per rate on all N episodes; the parameters at the chosen step of the chosen rate are kept.
    Returns (best: tree with leading axes (NH, n_worlds), info)."""
    nW = len(lab_obs)
    pad = (N, sum(ANCHORS) * N) if pad is None else pad
    n_ev = s_max // eval_every + 1
    cv = np.full((len(lrs), n_ev, nW, folds, NH), np.nan)
    t0 = time.time()
    for f in range(folds):
        dsf = [make_ds(lab_obs[i][:N], lab_U[i][:N], smu, ssd, val_ep=(np.arange(N) % folds == f)) for i in range(nW)]
        for li, lr in enumerate(lrs):
            for s in range(0, nW, lock):
                if deadline is not None and time.time() > deadline:
                    raise TimeoutError(f"ft_cv{tag}: deadline during cross-validation")
                sl = slice(s, min(nW, s + lock))
                _, inf = train(dsf[sl], s_max, seeds[sl], lr=lr, init=init_k[sl], batch=batch, sched="const",
                               eval_every=eval_every, pad=pad)
                V = np.array([h[1] for h in inf["val"]])                          # (n_ev, K, NH)
                hv = np.array(inf["has_val"])
                cv[li, :, sl, f] = np.where(hv[None], V, np.nan)
        del dsf
    m = np.nanmean(cv, 3)                                                         # (n_lr, n_ev, nW, NH)
    flat = m.reshape(len(lrs) * n_ev, nW, NH)
    flat = np.where(np.isfinite(flat), flat, np.inf)
    arg = flat.argmin(0)                                                          # (nW, NH)
    li_best, step_best = arg // n_ev, (arg % n_ev) * eval_every
    if log:
        log(f"  ft_cv{tag}: N {N}, cross-validation {time.time() - t0:.0f}s; chosen steps (median per horizon) "
            f"{np.median(step_best, 0).tolist()}, rates {[float(np.median(np.array(lrs)[li_best[:, j]])) for j in range(NH)]}")
    dsa = [make_ds(lab_obs[i][:N], lab_U[i][:N], smu, ssd, val_frac=0.0) for i in range(nW)]
    best = stack_trees([stack_trees([init_k[i]] * NH) for i in range(nW)])       # (nW, NH, ...): step 0 = the start
    best = jax.tree_util.tree_map(lambda a: jnp.swapaxes(a, 0, 1), best)          # (NH, nW, ...)
    for li, lr in enumerate(lrs):
        tk = np.where(li_best == li, step_best, -1)                               # (nW, NH)
        if not (tk > 0).any():
            continue
        for s in range(0, nW, lock):
            sl = slice(s, min(nW, s + lock))
            if not (tk[sl] > 0).any():
                continue
            b, _ = train(dsa[sl], s_max, seeds[sl], lr=lr, init=init_k[sl], batch=batch, sched="const",
                         eval_every=eval_every, take=tk[sl], pad=pad)
            msk = jnp.asarray((tk[sl] > 0).T)                                     # (NH, k)
            best = jax.tree_util.tree_map(
                lambda B_, b_: B_.at[:, sl].set(jnp.where(msk.reshape(msk.shape + (1,) * (b_.ndim - 2)), b_, B_[:, sl])),
                best, b)
    info = {"N": N, "lrs": list(lrs), "s_max": s_max, "eval_every": eval_every, "folds": folds, "batch": batch,
            "cv_mean": np.where(np.isfinite(m), m, -1).tolist(), "lr_index": li_best.tolist(), "step": step_best.tolist(),
            "lr": np.array(lrs)[li_best].tolist(), "trained": (step_best < s_max).tolist(), "seeds": [int(s) for s in seeds],
            "seconds": time.time() - t0}
    return best, info
