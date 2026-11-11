"""a_nets -- study A (round 6, dials): generic repairs of round 5's block-view net.

  FT      fine-tuning of a conditioned net on N Lab episodes, steps by cross-validation over episodes
          (DECLARED R8): many fine-tunes in lockstep (jax.vmap over nets, data passed as arguments).
          The conditioning of every example is drawn from a per-net table TH (rows of theta in box units):
          draws of the public prior for P0's net, the truth repeated for the true-form net.
  RES     the designer's per-block residual (defect_gliders/surrogate.py, res_scores) on a net's predictive
          mean (DECLARED R9): per program class, horizon and region class a ridge from a block's three scaled
          numbers at the anchor (and 1) to the residual of its three numbers.
  misc    structural program classes, saving and loading parameter trees.
Round 5's ladder_net is imported, not changed: its apply, build_inputs, fair_es, targets, _adamw.
"""
from __future__ import annotations

import time

import xlaw as X

import jax
import jax.numpy as jnp
import numpy as np

LL, NN, GW, PL = X.LL, X.NN, X.GW, X.PL
G, NW, NC = X.G, X.NW, X.NC
F32 = jnp.float32
VIEW = "block"
SCB = LL.SC1.reshape(3, G, G)


class FT:
    BATCH = 64          # examples per step (x NN.Cfg.M_TRAIN noise draws)
    LR = 1e-4           # constant: the final rate of the base cosine schedule (NN.Cfg.LR x 0.1)
    STEPS = 400
    GRID = 40           # cross-validation grid (steps); 0 is always a candidate
    LOCK = 16           # fine-tunes in lockstep
    N_TH = 512          # rows of a net's conditioning table
    N_VAL = 512         # most held-out rows per fold (whole chunks of NN.Cfg.EVAL_ROWS)
    FOLDS = 4


# ----------------------------------------------------------------------------- data
def examples(eps, T1):
    """Example index (episode, t, h-index) of the given episodes: every anchor and horizon of base training."""
    eps = np.asarray(eps, int)
    lag = max(NN.Cfg.LAGS)
    ex = [np.stack([eps, np.full(len(eps), t), np.full(len(eps), hi)], 1)
          for hi, h in enumerate(NN.Cfg.HS) for t in range(lag, T1 - h)]
    return np.concatenate(ex).astype(np.int32) if ex and len(eps) else np.zeros((0, 3), np.int32)


def ft_dataset(A, tr_eps, va_eps, seed=0):
    """One fine-tune's data from a world's view arrays A (NN.view_arrays): train and held-out episodes."""
    T1 = A["X"].shape[1]
    tr, va = examples(tr_eps, T1), examples(va_eps, T1)
    if len(va) > FT.N_VAL:
        va = va[np.sort(np.random.default_rng(seed).choice(len(va), FT.N_VAL, replace=False))]
    return {"X": A["X"], "CU": A["CU"], "CtU": A["CtU"], "tr": tr, "va": va}


def stack_fixed(dsets, e_pad, ntr_pad, nva_pad):
    """Stack fine-tune datasets along a leading net axis at FIXED shapes (one compiled program for every
    budget): episodes padded to e_pad, example lists to ntr_pad / nva_pad (padding is never sampled: n_tr,
    n_va carry the true lengths). Device arrays, passed to the jitted functions as arguments."""
    def pad(a, n):
        a = np.asarray(a)
        if len(a) > n:
            raise ValueError(f"array of length {len(a)} does not fit the fixed shape {n}")
        return a if len(a) == n else np.concatenate([a, np.zeros((n - len(a),) + a.shape[1:], a.dtype)], 0)
    out = {k: jnp.asarray(np.stack([pad(d[k], e_pad) for d in dsets])) for k in ("X", "CU", "CtU")}
    out["th"] = jnp.zeros((len(dsets), e_pad, NN.Cfg.DMAX), F32)
    out["tr"] = jnp.asarray(np.stack([pad(d["tr"], ntr_pad) for d in dsets]))
    out["va"] = jnp.asarray(np.stack([pad(d["va"], nva_pad) for d in dsets]))
    out["n_tr"] = jnp.asarray(np.array([len(d["tr"]) for d in dsets], np.int32))
    out["n_va"] = jnp.asarray(np.array([len(d["va"]) for d in dsets], np.int32))
    for k, v in out.items():
        assert v.size < 2 ** 31, f"device array {k} has {v.size} elements"
    return out


def fixed_shapes(n_max, T1):
    per_ep = len(examples([0], T1))
    R = NN.Cfg.EVAL_ROWS
    return int(n_max), int(n_max * per_ep), int(-(-FT.N_VAL // R) * R)


# ----------------------------------------------------------------------------- lockstep fine-tuning
_FN = {}


def _fns(keys):
    k = (FT.BATCH, NN.Cfg.M_TRAIN, NN.Cfg.LAGS, NN.Cfg.HS, NN.Cfg.EVAL_ROWS, NN.Cfg.EVAL_DRAWS, keys)
    if k not in _FN:
        B, M, R, ND = FT.BATCH, NN.Cfg.M_TRAIN, NN.Cfg.EVAL_ROWS, NN.Cfg.EVAL_DRAWS

        def step_one(p, s, Dk, TH, key, lr):
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

        def eval_one(a):
            """Held-out fair energy score of ONE net in chunks of R rows (a sequential loop: the largest
            array is R x ND samples of one net, whatever the number of nets)."""
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
        _FN[k] = (jax.jit(jax.vmap(step_one, in_axes=(0, 0, Dax, 0, 0, None))),
                  jax.jit(lambda P, D, TH: jax.lax.map(eval_one, (P, D, TH))))
    return _FN[k]


def _stack_trees(trees):
    return jax.tree_util.tree_map(lambda *a: jnp.stack(a), *trees)


def ft_lockstep(P_init, dsets, TH, shapes, steps, seed, grid=None, snap_at=None, evaluate=True):
    """Fine-tune len(dsets) nets in lockstep for `steps` steps at the constant rate FT.LR.
    P_init list of parameter trees; TH (Kn, N_TH, DMAX); shapes = fixed_shapes(...).
    evaluate: held-out score at steps 0, grid, 2 grid, ... -> curve (Kn, steps // grid + 1).
    snap_at (Kn,) ints (multiples of grid; 0 = the start): the parameters of net k at step snap_at[k].
    Returns (curve or None, list of parameter trees or None, seconds per step without the first)."""
    grid = FT.GRID if grid is None else int(grid)
    Kn = len(dsets)
    NN.check_elems(VIEW, True, Kn, FT.BATCH * NN.Cfg.M_TRAIN, "fine-tune step")
    NN.check_elems(VIEW, True, 1, NN.Cfg.EVAL_ROWS * NN.Cfg.EVAL_DRAWS, "fine-tune validation chunk")
    D = stack_fixed(dsets, *shapes)
    vstep, veval = _fns(tuple(sorted(D)))
    P = _stack_trees(P_init)
    TH = jnp.asarray(np.asarray(TH), F32)
    st = {"t": jnp.zeros((Kn,), F32), "m": jax.tree_util.tree_map(jnp.zeros_like, P),
          "v": jax.tree_util.tree_map(jnp.zeros_like, P)}
    curve = [np.asarray(veval(P, D, TH))] if evaluate else None
    snap = P
    sa = None if snap_at is None else np.asarray(snap_at, int)
    key = jax.random.key(seed)
    t1 = None
    for it in range(1, steps + 1):
        key, sub = jax.random.split(key)
        P, st, l = vstep(P, st, D, TH, jax.random.split(sub, Kn), FT.LR)
        if it == 1:
            l.block_until_ready()
            t1 = time.time()                       # the first step holds the compilation
        if it % grid == 0:
            if evaluate:
                curve.append(np.asarray(veval(P, D, TH)))
            if sa is not None and (sa == it).any():
                bm = jnp.asarray(sa == it)
                snap = jax.tree_util.tree_map(
                    lambda a, b: jnp.where(bm.reshape((-1,) + (1,) * (a.ndim - 1)), a, b), P, snap)
    l.block_until_ready()
    dt = (time.time() - t1) / max(steps - 1, 1) if t1 else float("nan")
    out = None if sa is None else [jax.tree_util.tree_map(lambda a, k=k: a[k], snap) for k in range(Kn)]
    return (None if curve is None else np.array(curve).T), out, dt


def folds_of(n):
    """Cross-validation folds over the first n episodes: min(FT.FOLDS, n) folds, episode j in fold j mod K."""
    K = min(FT.FOLDS, n)
    return [([j for j in range(n) if j % K != f], [j for j in range(n) if j % K == f]) for f in range(K)]


def finetune_cv(tasks, shapes, steps, seed, log=None, tag=""):
    """Cross-validated fine-tuning of many nets (DECLARED R8).
    tasks: list of dicts {id, base (parameter tree), A (view arrays of the world's episodes), eps (list of
    episode indices to use), TH (N_TH, DMAX)}.
    Returns ({id: parameter tree}, {id: {"curve": mean CV curve, "steps": chosen}}, timing)."""
    t0 = time.time()
    grid = FT.GRID
    cv, owner = [], []
    for ti, tk in enumerate(tasks):
        eps = list(tk["eps"])
        for tr, va in folds_of(len(eps)):
            cv.append((tk, [eps[j] for j in tr], [eps[j] for j in va]))
            owner.append(ti)
    curves = np.zeros((len(cv), steps // grid + 1))
    dts, sec_cv, sec_fin = [], [], []
    for s0 in range(0, len(cv), FT.LOCK):
        tg = time.time()
        part = cv[s0:s0 + FT.LOCK]
        n = len(part)
        part = part + [part[-1]] * (FT.LOCK - n)                     # whole lockstep groups: one compiled shape
        dsets = [ft_dataset(tk["A"], tr, va, seed=seed + s0 + j) for j, (tk, tr, va) in enumerate(part)]
        cu, _, dt = ft_lockstep([tk["base"] for tk, _, _ in part], dsets, np.stack([tk["TH"] for tk, _, _ in part]),
                                shapes, steps, seed + 7 * s0 + 1, grid=grid)
        curves[s0:s0 + n] = cu[:n]
        dts.append(dt)
        sec_cv.append(time.time() - tg)
        if log and (s0 // FT.LOCK) % 8 == 0:
            log(f"  ft{tag} cv group {s0 // FT.LOCK + 1}/{-(-len(cv) // FT.LOCK)} {dt * 1e3:.1f} ms/step "
                f"({time.time() - t0:.0f}s)")
    owner = np.array(owner)
    info, chosen = {}, []
    for ti, tk in enumerate(tasks):
        c = curves[owner == ti].mean(0)
        c = np.where(np.isfinite(c), c, np.inf)
        s = int(np.argmin(c)) * grid
        info[tk["id"]] = {"curve": c.tolist(), "steps": s, "n_folds": int((owner == ti).sum())}
        chosen.append(s)
    chosen = np.array(chosen)
    out = {tk["id"]: tk["base"] for tk in tasks}                     # 0 steps: the base net unchanged
    todo = [ti for ti in range(len(tasks)) if chosen[ti] > 0]
    for s0 in range(0, len(todo), FT.LOCK):
        tg = time.time()
        part = todo[s0:s0 + FT.LOCK]
        n = len(part)
        part = part + [part[-1]] * (FT.LOCK - n)
        dsets = [ft_dataset(tasks[ti]["A"], list(tasks[ti]["eps"]), [], seed=0) for ti in part]
        _, prm, dt = ft_lockstep([tasks[ti]["base"] for ti in part], dsets, np.stack([tasks[ti]["TH"] for ti in part]),
                                 shapes, int(chosen[part].max()), seed + 7 * s0 + 100003, grid=grid,
                                 snap_at=chosen[part], evaluate=False)
        for j in range(n):
            out[tasks[part[j]]["id"]] = prm[j]
        dts.append(dt)
        sec_fin.append(time.time() - tg)
    timing = {"seconds": time.time() - t0, "ms_per_lockstep_step_median": float(np.median(dts) * 1e3) if dts else None,
              "n_cv_runs": len(cv), "n_final_runs": len(todo), "steps": int(steps), "grid": int(grid),
              "group_seconds_cv": sec_cv, "group_seconds_final": sec_fin}
    return out, info, timing


# ----------------------------------------------------------------------------- the residual (RES)
def region(Ub):
    """(G, G) int: 0 far, 1 neighbour of a block with input, 2 block with input at any tick (the designer's)."""
    on = np.abs(np.asarray(Ub, float).reshape(-1, 2, G, G)).sum((0, 1)) > 0
    nb = np.zeros_like(on)
    for dy in (-1, 0, 1):
        for dx in (-1, 0, 1):
            nb |= np.roll(np.roll(on, dy, 0), dx, 1)
    return nb.astype(int) + on.astype(int)


def program_class(Ub):
    """Class of a dense test program (H, NW) from its structure alone, which the public mix fixes:
    'a' no input; 'd' regional: ticks 0-3, 16 blocks each, one force; 'c' aimed: ticks 0-3, 4 blocks each,
    one force; 'b' anything else (blind). An aimed push that found no body is empty and reads as 'a'."""
    U = np.asarray(Ub, float).reshape(-1, 2, G, G)
    act = np.flatnonzero(np.abs(U).sum((1, 2, 3)) > 0)
    if act.size == 0:
        return "a"
    if list(act) == list(range(GW.T_IN)):
        nb, one = [], True
        for t in act:
            on = np.abs(U[t]).sum(0) > 0
            nb.append(int(on.sum()))
            for c in range(2):
                v = U[t, c][on]
                one &= bool(np.allclose(v, v[0], rtol=1e-9, atol=1e-12))
        if one and all(n == 16 for n in nb):
            return "d"
        if one and all(n == 4 for n in nb):
            return "c"
    return "b"


def block_scaled(y):
    """(..., 192) block view -> (..., 3, G, G) in the public scales."""
    y = np.asarray(y, float)
    return y.reshape(y.shape[:-1] + (3, G, G)) / SCB


def res_fit(z0, R, reg, cls, lam=0.05):
    """z0 (n, 3, G, G) scaled block numbers at the anchor; R (n, nh, 3, G, G) scaled residuals (truth minus
    the net's predictive mean); reg (n, G, G) region classes; cls (n,) program classes.
    -> {(class, horizon index, region): W (4, 3)}; ridge lam x rows, as surrogate.res_scores."""
    n, nh = R.shape[:2]
    f = np.concatenate([z0, np.ones_like(z0[:, :1])], 1).transpose(0, 2, 3, 1)       # (n, G, G, 4)
    Rt = R.transpose(0, 1, 3, 4, 2)                                                  # (n, nh, G, G, 3)
    W = {}
    cls = np.asarray(cls)
    for c in sorted(set(cls.tolist())):
        ii = np.flatnonzero(cls == c)
        for k in (0, 1, 2):
            m = reg[ii] == k
            if not m.any():
                continue
            Xl = f[ii][m]
            A = Xl.T @ Xl + lam * len(Xl) * np.eye(4)
            for ih in range(nh):
                W[(c, ih, k)] = np.linalg.solve(A, Xl.T @ Rt[ii, ih][m])
    return W


def res_apply(W, z0, reg, cls, nh):
    """The fitted correction for items: (n, nh, 192) in the exam's units (zero where nothing was fitted)."""
    n = len(z0)
    f = np.concatenate([z0, np.ones_like(z0[:, :1])], 1).transpose(0, 2, 3, 1)
    out = np.zeros((n, nh, G, G, 3))
    for i in range(n):
        for k in (0, 1, 2):
            m = reg[i] == k
            if not m.any():
                continue
            for ih in range(nh):
                Wk = W.get((cls[i], ih, k))
                if Wk is not None:
                    out[i, ih][m] = f[i][m] @ Wk
    return (out.transpose(0, 1, 4, 2, 3) * SCB).reshape(n, nh, NC)


def lab_items(obs, U, P):
    """Lab episodes as exam-shaped items (history = the first P + 1 observations, program = the rest)."""
    return [{"id": i, "history": np.asarray(obs[i, :P + 1], float), "program": PL.dense_to_prog(np.asarray(U[i, P:], float))}
            for i in range(len(obs))]


# ----------------------------------------------------------------------------- parameter trees on disk
def tree_to_arrays(prefix, tree):
    return {f"{prefix}/{i:02d}": np.asarray(a) for i, a in enumerate(jax.tree_util.tree_leaves(tree))}


def tree_from_arrays(prefix, arrs, template):
    leaves, treedef = jax.tree_util.tree_flatten(template)
    return treedef.unflatten([jnp.asarray(arrs[f"{prefix}/{i:02d}"]) for i in range(len(leaves))])
