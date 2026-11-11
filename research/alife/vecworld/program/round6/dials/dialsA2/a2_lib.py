"""a2_lib -- study dialsA2 (round 6, dials): the pieces study A did not have.

PILOT ONLY: nothing written with these functions may be reused as an exam.

  trainers   round 5's base-net trainer and study A's lockstep fine-tuning with many steps per dispatch (a
             lax.scan), as the runner's review of r6-dialsa-002 asked. Same loss (ladder_net.loss_fn, fair_es),
             AdamW (ladder_net._adamw), cosine schedule, validation (ladder_net's and a_nets' evaluations);
             the fine-tunes take a rate per net, so several rates share one lockstep group (DECLARED R8, R11).
  designed   the 8 designed arms of DECLARED R6 (dose series and two controls) as program functions, and the
             designed family's simulator (xlaw's runner, a class table instead of ladder_lib.CLASSES).
  H, H_mix   the told-form recipe (DECLARED R14): 21 level-1 summaries, a projection per arm or class, round
             5's emulator and importance sampler in 5 dimensions (theta, eta), prior = round 5's viability prior
             times uniform eta on [0, 4].
Nothing in vw, round 5, defect_gliders or dialsA is changed; their modules are imported.
"""
from __future__ import annotations

import math
import os
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
_A = os.path.join(os.path.dirname(HERE), "dialsA")
if _A not in sys.path:
    sys.path.insert(0, _A)
import xlaw as X  # noqa: E402
import a_nets as AN  # noqa: E402

import jax  # noqa: E402
import jax.numpy as jnp  # noqa: E402
import numpy as np  # noqa: E402

from vw.harness import program_dense  # noqa: E402

LL, NN, SL, GW, PL = X.LL, X.NN, X.SL, X.GW, X.PL
G, NW, NC, SIG = X.G, X.NW, X.NC, X.SIG
F32 = jnp.float32
VIEW = "block"
ETA_MAX = 4.0


class TRN:
    SCAN = 50           # base and D nets: steps per dispatch
    FT_DISPATCH = 4     # fine-tunes: evaluation blocks (of FT.GRID steps) per dispatch


# ============================================================================ base and D nets
_TF = {}


def _lr_cos(it, steps):
    """Round 5's schedule (ladder_net.train_nets): warm-up 100 steps, cosine to a floor of 0.1."""
    return NN.Cfg.LR * jnp.minimum(1.0, it / 100.0) * (0.1 + 0.9 * 0.5 * (1.0 + jnp.cos(jnp.pi * it / steps)))


def _train_fn(cond, keys, nscan):
    k = (cond, NN.Cfg.BATCH, NN.Cfg.M_TRAIN, NN.Cfg.LAGS, NN.Cfg.HS, keys, nscan)
    if k not in _TF:
        B, M = NN.Cfg.BATCH, NN.Cfg.M_TRAIN

        def step_one(p, s, Dk, key, lr):                       # = ladder_net._fns.step_one
            k1, k2 = jax.random.split(key)
            u = jax.random.uniform(k1, (B,))
            i = jnp.minimum((u * Dk["n_tr"]).astype(jnp.int32), Dk["n_tr"] - 1)
            ex = Dk["tr"][i]
            l, g = jax.value_and_grad(NN.loss_fn)(p, VIEW, Dk, ex[:, 0], ex[:, 1], ex[:, 2], k2, M, cond)
            p, s = NN._adamw(p, g, s, lr)
            return p, s, l
        vstep = jax.vmap(step_one, in_axes=(0, 0, {kk: 0 for kk in keys}, 0, None))

        def multi(P, st, D, key, it0, steps):
            Kn = jax.tree_util.tree_leaves(P)[0].shape[0]

            def body(c, j):
                P, st = c
                it = (it0 + j + 1).astype(F32)
                P, st, l = vstep(P, st, D, jax.random.split(jax.random.fold_in(key, j), Kn), _lr_cos(it, steps))
                return (P, st), l
            (P, st), ls = jax.lax.scan(body, (P, st), jnp.arange(nscan))
            return P, st, ls[-1]
        _TF[k] = jax.jit(multi)
    return _TF[k]


def train_nets(dsets, cond=False, steps=3000, seed=0, log=None, tag="", deadline=None, eval_every=250):
    """ladder_net.train_nets with TRN.SCAN steps per dispatch (steps and eval_every multiples of it).
    Returns (list of best-validation params, info) with info as ladder_net's (best_val, best_step, hist, ...)."""
    nscan = TRN.SCAN
    if steps % nscan or eval_every % nscan:
        raise ValueError(f"steps {steps} and eval_every {eval_every} must be multiples of {nscan}")
    Kn = len(dsets)
    if Kn > NN.Cfg.MAX_LOCK:
        raise ValueError(f"{Kn} nets in lockstep, at most {NN.Cfg.MAX_LOCK}")
    NN.check_elems(VIEW, cond, Kn, NN.Cfg.BATCH * NN.Cfg.M_TRAIN, "training step")
    NN.check_elems(VIEW, cond, 1, NN.Cfg.EVAL_ROWS * NN.Cfg.EVAL_DRAWS, "validation chunk")
    D = NN.stack_datasets(dsets)
    keys_d = tuple(sorted(D))
    multi = _train_fn(cond, keys_d, nscan)
    veval = NN._fns(VIEW, cond, keys_d)[1]                     # round 5's jitted validation (D an argument)
    keys = jax.random.split(jax.random.key(seed), Kn)
    P = jax.vmap(lambda k: NN.init_params(VIEW, k, cond))(keys)
    st = {"t": jnp.zeros((Kn,), F32), "m": jax.tree_util.tree_map(jnp.zeros_like, P),
          "v": jax.tree_util.tree_map(jnp.zeros_like, P)}
    best, best_val, best_step = P, np.full(Kn, np.inf), np.zeros(Kn, int)
    hist, key, t0 = [], jax.random.key(seed + 1), time.time()
    has_val = np.array([d["n_val_ep"] > 0 for d in dsets])
    stopped, it, t_first = None, 0, None
    steps_f = jnp.asarray(float(steps), F32)
    while it < steps:
        key, sub = jax.random.split(key)
        P, st, l = multi(P, st, D, sub, jnp.asarray(it, jnp.int32), steps_f)
        it += nscan
        if t_first is None:
            l.block_until_ready()
            t_first = time.time()
        if it % eval_every == 0 or it == steps:
            v = np.asarray(veval(P, D))
            v = np.where(has_val, v, -it)
            v = np.where(np.isfinite(v), v, np.inf)
            better = v < best_val
            if better.any():
                bm = jnp.asarray(better)
                best = jax.tree_util.tree_map(
                    lambda a, b: jnp.where(bm.reshape((-1,) + (1,) * (a.ndim - 1)), a, b), P, best)
                best_val = np.where(better, v, best_val)
                best_step = np.where(better, it, best_step)
            hist.append({"step": it, "train_loss_mean": float(np.nanmean(np.asarray(l))), "val": np.round(v, 6).tolist()})
            if log and (it % (8 * eval_every) == 0 or it == steps):
                log(f"  net{tag} step {it}/{steps} train {float(np.nanmean(np.asarray(l))):.4f} "
                    f"val {np.round(v[:8], 4).tolist()} ({time.time() - t0:.0f}s)")
            if deadline is not None and time.time() > deadline and it < steps:
                stopped = it
                break
    params = [jax.tree_util.tree_map(lambda a, k=k: a[k], best) for k in range(Kn)]
    ms = (time.time() - t_first) / max(it - nscan, 1) * 1e3 if t_first else float("nan")
    info = {"best_val": best_val.tolist(), "best_step": best_step.tolist(), "hist": hist, "seconds": time.time() - t0,
            "steps": int(steps), "stopped_early": stopped, "ms_per_step": ms, "steps_per_dispatch": nscan,
            "eval_every": int(eval_every), "n_train_examples": [len(d["tr"]) for d in dsets],
            "n_episodes": [d["n_ep"] for d in dsets]}
    del D
    return params, info


# ============================================================================ fine-tunes in lockstep, rate per net
_FF = {}


def _ft_fn(keys, grid, nblk, evaluate):
    k = (AN.FT.BATCH, NN.Cfg.M_TRAIN, NN.Cfg.LAGS, NN.Cfg.HS, NN.Cfg.EVAL_ROWS, NN.Cfg.EVAL_DRAWS, keys, grid, nblk,
         evaluate)
    if k not in _FF:
        B, M, R, ND = AN.FT.BATCH, NN.Cfg.M_TRAIN, NN.Cfg.EVAL_ROWS, NN.Cfg.EVAL_DRAWS

        def step_one(p, s, Dk, TH, key, lr):                   # = a_nets._fns.step_one, lr per net
            k1, k2, k3 = jax.random.split(key, 3)
            u = jax.random.uniform(k1, (B,))
            i = jnp.minimum((u * Dk["n_tr"]).astype(jnp.int32), Dk["n_tr"] - 1)
            ex = Dk["tr"][i]
            th = TH[jax.random.randint(k3, (B,), 0, TH.shape[0])]

            def loss(pp):
                d = NN.apply(VIEW, pp, NN.build_inputs(VIEW, Dk, ex[:, 0], ex[:, 1], ex[:, 2], k2, M, True, theta=th))
                return NN.fair_es(d.reshape(B, M, -1), NN.targets(Dk, ex[:, 0], ex[:, 1], ex[:, 2])).mean()
            l, g = jax.value_and_grad(loss)(p)
            p, s = NN._adamw(p, g, s, lr)
            return p, s, l

        def eval_one(a):                                        # = a_nets._fns.eval_one
            p, Dk, TH = a
            nv = Dk["va"].shape[0]
            exc = Dk["va"].reshape(nv // R, R, 3)
            idx = jnp.arange(nv).reshape(nv // R, R)

            def chunk(b):
                ex, ii = b
                ka, kb = jax.random.split(jax.random.fold_in(jax.random.key(12345), ii[0]))
                th = TH[jax.random.randint(kb, (R,), 0, TH.shape[0])]
                d = NN.apply(VIEW, p, NN.build_inputs(VIEW, Dk, ex[:, 0], ex[:, 1], ex[:, 2], ka, ND, True, theta=th))
                es = NN.fair_es(d.reshape(R, ND, -1), NN.targets(Dk, ex[:, 0], ex[:, 1], ex[:, 2]))
                mask = (ii < Dk["n_va"]).astype(F32)
                return (es * mask).sum(), mask.sum()
            sm, cn = jax.lax.map(chunk, (exc, idx))
            return sm.sum() / jnp.maximum(cn.sum(), 1.0)
        Dax = {kk: 0 for kk in keys}
        vstep = jax.vmap(step_one, in_axes=(0, 0, Dax, 0, 0, 0))

        def veval(P, D, TH):
            return jax.lax.map(eval_one, (P, D, TH))

        def run(P, st, snap, D, TH, key, lr, it0, snap_at):
            Kn = jax.tree_util.tree_leaves(P)[0].shape[0]

            def blk(c, b):
                P, st, snap = c

                def body(c2, j):
                    P, st = c2
                    kk = jax.random.split(jax.random.fold_in(key, b * grid + j), Kn)
                    P, st, l = vstep(P, st, D, TH, kk, lr)
                    return (P, st), l
                (P, st), _ = jax.lax.scan(body, (P, st), jnp.arange(grid))
                it = it0 + (b + 1) * grid
                v = veval(P, D, TH) if evaluate else jnp.zeros((Kn,), F32)
                m = snap_at == it
                snap = jax.tree_util.tree_map(
                    lambda a, s: jnp.where(m.reshape((-1,) + (1,) * (a.ndim - 1)), a, s), P, snap)
                return (P, st, snap), v
            (P, st, snap), vs = jax.lax.scan(blk, (P, st, snap), jnp.arange(nblk))
            return P, st, snap, vs
        _FF[k] = (jax.jit(run), jax.jit(veval))
    return _FF[k]


def ft_lockstep(P_init, dsets, TH, lrs, shapes, steps, seed, snap_at=None, evaluate=True):
    """a_nets.ft_lockstep with a rate per net (lrs (Kn,)) and FT_DISPATCH x GRID steps per dispatch.
    Returns (curve (Kn, steps // GRID + 1) or None, list of snapshots at snap_at or None, ms per step)."""
    grid = AN.FT.GRID
    nblk = TRN.FT_DISPATCH
    if steps % (grid * nblk):
        raise ValueError(f"fine-tune steps {steps} must be a multiple of {grid * nblk}")
    Kn = len(dsets)
    NN.check_elems(VIEW, True, Kn, AN.FT.BATCH * NN.Cfg.M_TRAIN, "fine-tune step")
    NN.check_elems(VIEW, True, 1, NN.Cfg.EVAL_ROWS * NN.Cfg.EVAL_DRAWS, "fine-tune validation chunk")
    D = AN.stack_fixed(dsets, *shapes)
    run, veval = _ft_fn(tuple(sorted(D)), grid, nblk, bool(evaluate))
    P = AN._stack_trees(P_init)
    TH = jnp.asarray(np.asarray(TH), F32)
    lr = jnp.asarray(np.asarray(lrs, np.float32))
    st = {"t": jnp.zeros((Kn,), F32), "m": jax.tree_util.tree_map(jnp.zeros_like, P),
          "v": jax.tree_util.tree_map(jnp.zeros_like, P)}
    sa = jnp.asarray(np.zeros(Kn, np.int32) if snap_at is None else np.asarray(snap_at, np.int32))
    curve = [np.asarray(veval(P, D, TH))] if evaluate else None
    snap = P
    key = jax.random.key(seed)
    t1, it = None, 0
    while it < steps:
        key, sub = jax.random.split(key)
        P, st, snap, vs = run(P, st, snap, D, TH, sub, lr, jnp.asarray(it, jnp.int32), sa)
        it += grid * nblk
        if evaluate:
            curve.extend(list(np.asarray(vs)))
        if t1 is None:
            jax.block_until_ready(P)
            t1 = time.time()
    jax.block_until_ready(P)
    n_after = steps - grid * nblk
    ms = (time.time() - t1) / n_after * 1e3 if n_after > 0 else float("nan")
    out = None if snap_at is None else [jax.tree_util.tree_map(lambda a, k=k: a[k], snap) for k in range(Kn)]
    return (None if curve is None else np.array(curve).T), out, ms


def finetune_cv(tasks, shapes, steps, rates, seed, log=None, tag=""):
    """Cross-validated fine-tuning (DECLARED R11) of many nets at several rates, in lockstep groups of
    AN.FT.LOCK runs. tasks: dicts {id, base, A, eps, cls, TH}. Per task the (rate, steps) with the least mean
    held-out score over its folds (0 steps: the base net unchanged); then the final fine-tune on all its
    episodes at that point. Returns ({id: params}, {id: info}, timing)."""
    t0 = time.time()
    grid = AN.FT.GRID
    runs = []                                                    # (task index, rate index, train eps, held-out eps)
    for ti, tk in enumerate(tasks):
        eps = list(tk["eps"])
        for ri in range(len(rates)):
            for tr, va in AN.folds_of(len(eps), tk.get("cls")):
                runs.append((ti, ri, [eps[j] for j in tr], [eps[j] for j in va]))
    npt = steps // grid + 1
    curves = np.zeros((len(runs), npt))
    ms_l, sec_cv, sec_fin = [], [], []
    L = AN.FT.LOCK
    for s0 in range(0, len(runs), L):
        tg = time.time()
        part = runs[s0:s0 + L]
        n = len(part)
        part = part + [part[-1]] * (L - n)
        dsets = [AN.ft_dataset(tasks[ti]["A"], tr, va, seed=seed + s0 + j) for j, (ti, ri, tr, va) in enumerate(part)]
        cu, _, ms = ft_lockstep([tasks[ti]["base"] for ti, _, _, _ in part], dsets,
                                np.stack([tasks[ti]["TH"] for ti, _, _, _ in part]),
                                [rates[ri] for _, ri, _, _ in part], shapes, steps, seed + 7 * s0 + 1)
        curves[s0:s0 + n] = cu[:n]
        ms_l.append(ms)
        sec_cv.append(time.time() - tg)
        if log and (s0 // L) % 16 == 0:
            log(f"  ft{tag} cv group {s0 // L + 1}/{-(-len(runs) // L)} {ms:.1f} ms/step ({time.time() - t0:.0f}s)")
    tix = np.array([r[0] for r in runs])
    rix = np.array([r[1] for r in runs])
    info, choice = {}, []
    for ti, tk in enumerate(tasks):
        c = np.stack([curves[(tix == ti) & (rix == ri)].mean(0) for ri in range(len(rates))])   # (n_rates, npt)
        c = np.where(np.isfinite(c), c, np.inf)
        ri, k = np.unravel_index(int(np.argmin(c)), c.shape)
        s = int(k) * grid
        info[tk["id"]] = {"curves": c.tolist(), "rate": float(rates[ri]) if s > 0 else 0.0, "rate_index": int(ri),
                          "steps": s, "n_folds": int(((tix == ti) & (rix == 0)).sum())}
        choice.append((s, ri))
    out = {tk["id"]: tk["base"] for tk in tasks}
    todo = [ti for ti in range(len(tasks)) if choice[ti][0] > 0]
    unit = grid * TRN.FT_DISPATCH
    for s0 in range(0, len(todo), L):
        tg = time.time()
        part = todo[s0:s0 + L]
        n = len(part)
        part = part + [part[-1]] * (L - n)
        dsets = [AN.ft_dataset(tasks[ti]["A"], list(tasks[ti]["eps"]), [], seed=0) for ti in part]
        mx = max(choice[ti][0] for ti in part)
        _, prm, ms = ft_lockstep([tasks[ti]["base"] for ti in part], dsets, np.stack([tasks[ti]["TH"] for ti in part]),
                                 [rates[choice[ti][1]] for ti in part], shapes, -(-mx // unit) * unit,
                                 seed + 7 * s0 + 100003, snap_at=[choice[ti][0] for ti in part], evaluate=False)
        for j in range(n):
            out[tasks[part[j]]["id"]] = prm[j]
        sec_fin.append(time.time() - tg)
    timing = {"seconds": time.time() - t0, "ms_per_lockstep_step_median": float(np.nanmedian(ms_l)) if ms_l else None,
              "n_cv_runs": len(runs), "n_final_runs": len(todo), "steps": int(steps), "grid": int(grid),
              "rates": [float(r) for r in rates], "group_seconds_cv": sec_cv, "group_seconds_final": sec_fin}
    return out, info, timing


def widen_decision(group_curves, rates, steps):
    """DECLARED R11 on one group's mean curves (n_rates, npt): 'steps' if the best point is past 80% of the
    steps; 'rate' if it is at 0 steps or at the first grid point of the smallest rate; else None (interior)."""
    c = np.asarray(group_curves, float)
    ri, k = np.unravel_index(int(np.argmin(c)), c.shape)
    s = int(k) * AN.FT.GRID
    smallest = int(np.argmin(rates))
    if s > 0.8 * steps:
        return "steps", s, float(rates[ri])
    if s == 0 or (s == AN.FT.GRID and ri == smallest):
        return "rate", s, float(rates[ri]) if s > 0 else 0.0
    return None, s, float(rates[ri])


# ============================================================================ designed arms (DECLARED R6)
ARMS = [(12.5, 4, "heavy"), (25.0, 4, "heavy"), (37.5, 4, "heavy"), (50.0, 4, "heavy"),
        (100.0, 1, "heavy"), (100.0, 2, "heavy"), (100.0, 2, "empty"), (100.0, 2, "c1")]
DES = tuple(f"x{i}" for i in range(len(ARMS)))


def _group_sums(v):
    v = np.asarray(v, float).reshape(G, G)
    return v + np.roll(v, -1, 0) + np.roll(v, -1, 1) + np.roll(np.roll(v, -1, 0), -1, 1)


def target_group(yc, kind):
    """(i0, j0), top-left block of the 2 x 2 group the arm pushes (periodic)."""
    yc = np.asarray(yc, float)
    if kind == "heavy":
        return GW.heaviest_group(yc)
    if kind == "empty":
        s = _group_sums(yc[2 * G * G:3 * G * G])
        i, j = np.unravel_index(int(np.argmin(s)), s.shape)
    else:
        s = _group_sums(yc[G * G:2 * G * G] - yc[:G * G])
        i, j = np.unravel_index(int(np.argmax(s)), s.shape)
    return int(i), int(j)


def designed_dense(arm, yc, angle, H):
    per_tick, ticks, kind = ARMS[arm]
    i0, j0 = target_group(yc, kind)
    f = SIG * math.sqrt(per_tick / 2.0) * (1 - 1e-9)
    n = np.array([math.sin(angle), math.cos(angle)])
    U = np.zeros((H, 2, G, G))
    rows, cols = [i0, (i0 + 1) % G], [j0, (j0 + 1) % G]
    for t in range(min(ticks, H)):
        for c in range(2):
            U[t, c][np.ix_(rows, cols)] = f * n[c]
    return U.reshape(H, NW)


def _arm_fn(arm):
    def f(rng, hist, H, left):
        U = designed_dense(arm, np.asarray(hist)[-1, :NC], rng.uniform(0, 2 * math.pi), H)
        if GW.nats_of(U) > left + 1e-9:
            raise ValueError(f"designed arm {arm} needs {GW.nats_of(U):.1f} nats, {left:.1f} left")
        return PL.dense_to_prog(U)
    return f


CLASSES = {"a": LL.CLASSES["a"], "c": LL.CLASSES["c"], "d": LL.CLASSES["d"], **{DES[i]: _arm_fn(i) for i in range(len(ARMS))}}
TRIG = ("c", "d")


def sim_designed(RN, names, thetas, etas, keys, seed, P=16, H=16, chunk=256, classes=None, log=None):
    """xlaw.sim_episodes_x with this module's class table (designed arms) under the hidden law."""
    th = np.atleast_2d(np.asarray(thetas, float))
    et = np.asarray(etas, float)
    B = len(th)
    classes = np.asarray(classes)
    OBS = np.zeros((B, P + H + 1, X.N_OBS), np.float32)
    UU = np.zeros((B, P + H, NW), np.float32)
    nats = np.zeros(B)
    for s in range(0, B, chunk):
        e = min(s + chunk, B)
        nb = e - s
        Pp = X.params_batch_x(names, SL._pad(th[s:e], chunk), SL._pad(et[s:e], chunk))
        k = SL._pad_keys(keys[s:e], chunk)
        sig = jnp.full((chunk,), SIG)
        A, m = RN.init_burn(Pp, k, sig)
        kd = GW.dyn_keys(k)
        y1, _, _, A, m = RN.run(Pp, A, m, kd, jnp.zeros((chunk,), jnp.int64), jnp.zeros((chunk, P, NW)), sig)
        y1 = SL.quantize(np.asarray(y1)[:nb])
        U = np.zeros((chunk, H, NW))
        for b in range(nb):
            prog = CLASSES[classes[s + b]](np.random.default_rng([int(seed), 1, s + b]), y1[b], H, SL.EP_CAP)
            U[b] = program_dense(prog, H, NW)
            nats[s + b] = GW.nats_of(U[b])
        y2, _, _, A, m = RN.run(Pp, A, m, kd, jnp.full((chunk,), P, jnp.int64), jnp.asarray(U), sig)
        y2 = SL.quantize(np.asarray(y2)[:nb])
        OBS[s:e] = np.concatenate([y1, y2[:, 1:]], 1)
        UU[s:e, P:] = U[:nb]
        if log:
            log(f"  sim_designed {e}/{B}")
    return {"obs": OBS, "U": UU, "cls": classes, "nats": nats, "eta": et}


# ============================================================================ H and H_mix (DECLARED R14)
LOST_H = (1, 2, 4, 8, 16)
LOCAL_H = (1, 2, 4)


def summaries(obs, U, P):
    """(B, 21): round 5's 13 block-view features, the share of the channel-0 block sum lost from the anchor
    to 1, 2, 4, 8, 16 ticks after it, and the share lost in the blocks under input at 1, 2, 4 ticks."""
    y = np.asarray(obs, float)
    Uf = np.asarray(U, float)
    B, T1, _ = y.shape
    F = LL.view_features(VIEW, y, Uf, P)
    c0 = y[:, :, :G * G]
    tot = c0.sum(-1)
    lost = [1.0 - tot[:, min(P + h, T1 - 1)] / np.maximum(tot[:, P], 1e-9) for h in LOST_H]
    on = (np.abs(Uf[:, P:].reshape(B, -1, 2, G * G)).sum((1, 2)) > 0).astype(float)          # (B, 64)
    loc0 = (c0[:, P] * on).sum(-1)
    loc = [np.where(loc0 > 1e-9, 1.0 - (c0[:, min(P + h, T1 - 1)] * on).sum(-1) / np.maximum(loc0, 1e-9), 0.0)
           for h in LOCAL_H]
    return np.concatenate([F, np.stack(lost + loc, 1)], 1)


def u5(th_u, eta):
    """(theta in box units, eta) -> the 5-vector on [-1, 1]^5 (eta / 2 - 1)."""
    return np.concatenate([np.asarray(th_u, float), (np.asarray(eta, float) / 2.0 - 1.0)[:, None]], 1)


def cond_of_u5(u):
    """Posterior draws u (..., 5) -> the true-form net's conditioning (theta_u, eta / 4)."""
    u = np.asarray(u, float)
    return np.concatenate([u[..., :4], ((u[..., 4:5] + 1.0) / 2.0)], -1)


class Prior5:
    """Round 5's viability prior on theta (box units) times uniform eta on [0, ETA_MAX] (u_5 uniform)."""

    def __init__(self, pv):
        self.pv = pv

    def logp(self, u):
        return self.pv.logp(np.asarray(u)[:, :4])


class ArmProjection:
    """sbi_lib.Projection fitted per arm or class: summaries -> (theta_u, eta / 2 - 1)."""

    def fit(self, F, cls, U5):
        F, cls, U5 = np.asarray(F, float), np.asarray(cls), np.asarray(U5, float)
        self.p = {c: SL.Projection().fit(F[cls == c], U5[cls == c]) for c in sorted(set(cls.tolist()))}
        self.r2 = {c: p.r2 for c, p in self.p.items()}
        return self

    def __call__(self, F, cls):
        F, cls = np.asarray(F, float), np.asarray(cls)
        out = np.zeros((len(F), 5))
        for c, p in self.p.items():
            m = cls == c
            if m.any():
                out[m] = p(F[m])
        missing = sorted(set(cls.tolist()) - set(self.p))
        if missing:
            raise KeyError(f"no projection for classes {missing}")
        return out


def fit_told_form(F, cls, U5pt, KD, rng):
    """Projection per arm / class and round 5's emulator over 5 parameters. F (N KD, 21), cls (N KD,),
    U5pt (N, 5): the family's design points. Returns (projection, emulator)."""
    U5ep = np.repeat(U5pt, KD, 0)
    proj = ArmProjection().fit(F, cls, U5ep)
    S = proj(F, cls).reshape(len(U5pt), KD, 5)
    em = LL.Emulator().fit(U5pt, S, rng=rng)
    return proj, em
