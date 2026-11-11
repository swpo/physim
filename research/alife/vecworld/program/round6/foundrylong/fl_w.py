"""fl_w -- study foundrylong, stage 2 (prototype): a hypothesis policy whose hypothesis is the 250 hidden numbers.

The hidden level-0 state is never observed, only the block view (block means of the two kinds and of S^2). W
marginalises the state with an ensemble of the candidate world's OWN states (spun up under the candidate weights),
held to the observed block means of both kinds at every observed tick:

  nudge        per block and kind, scale the cells so that the block means equal the observed ones (keeps the
               within-block pattern of the member, positivity, and the observed mass)
  assimilate   tick by tick over an observed window: one-tick forecast with fresh noise, record its block view,
               then nudge to the observed frame
  fit loss     fair energy score of the one-tick forecasts against the observed frames (in units of the per-channel
               SD of the observations), mean over ticks and episodes; gradients flow through each one-tick forecast
               (the nudged state is a constant: truncated, one tick)
  predict      assimilate the item's 17 frames at the fitted weights, then simulate under the item's program

Everything is a pure function of (theta, arrays, keys); batching by jax.vmap. float64 like the world.
PILOT ONLY: nothing produced with this module may be reused as an exam.
"""
from __future__ import annotations

import math
import os
import sys

sys.dont_write_bytecode = True
HERE = os.path.dirname(os.path.abspath(__file__))
if HERE not in sys.path:
    sys.path.insert(0, HERE)
import fl_lib as LL  # noqa: E402

FL = LL.FL
import jax  # noqa: E402
import jax.numpy as jnp  # noqa: E402
from jax import lax  # noqa: E402

import tnca as TN  # noqa: E402
from vw.core import Noise  # noqa: E402

FAM = TN.FAM
G, BPX, C = FAM.GW, FAM.H // FAM.GW, FAM.C
NW, NOBS = FAM.NW, (FAM.C + 1) * FAM.GW * FAM.GW


def view(x):
    return TN.block_view(x).reshape(-1)


def up(a):
    return jnp.repeat(jnp.repeat(a, BPX, -2), BPX, -1)


def nudge(x, y):
    """x (C, H, W) >= 0, y (NOBS,) observed block view -> x with the observed block means of every kind."""
    m = x.reshape(C, G, BPX, G, BPX).mean((2, 4))
    f = y.reshape(C + 1, G, G)[:C] / jnp.maximum(m, 1e-30)
    return x * up(f)


def spin(th, keys, burn: int):
    """Members of the candidate world after its own burn-in: (M, C, H, W)."""
    def one(k):
        x = TN.init(th, jax.random.fold_in(k, 1), FAM)
        kb = jax.random.fold_in(k, 2)
        x, _ = lax.scan(lambda x, t: (TN.tick_free(th, x, Noise(kb, t), FAM), None), x, jnp.arange(burn))
        return x
    return jax.vmap(one)(keys)


def _tick(th, x, k, t, u):
    return TN.tick(th, x, Noise(k, t), u, FAM)


_tick_remat = jax.checkpoint(_tick)


def assimilate(th, x, Y, U, keys, t0=0, stop=True, remat=False):
    """x (M, C, H, W) members; Y (T + 1, NOBS) observed frames; U (T, NW) commands of the T ticks; keys (M,).
    Returns (members held to Y[T], YF (T, M, NOBS) one-tick forecasts made before each nudge).
    remat: recompute each tick in the backward pass (memory of one state per member and tick)."""
    x = jax.vmap(nudge, (0, None))(x, Y[0])
    tk = _tick_remat if remat else _tick

    def body(x, inp):
        t, y, u = inp
        xs = lax.stop_gradient(x) if stop else x
        xf = jax.vmap(lambda xx, k: tk(th, xx, k, t, u))(xs, keys)
        return jax.vmap(nudge, (0, None))(xf, y), jax.vmap(view)(xf)
    T = U.shape[0]
    return lax.scan(body, x, (t0 + jnp.arange(T), Y[1:], U))


def forecast(th, x, U, keys, t0):
    """Free simulation of the members under the commands U (T, NW): block views (T, M, NOBS)."""
    def body(x, inp):
        t, u = inp
        xn = jax.vmap(lambda xx, k: TN.tick(th, xx, Noise(k, t), u, FAM))(x, keys)
        return xn, jax.vmap(view)(xn)
    _, Y = lax.scan(body, x, (t0 + jnp.arange(U.shape[0]), U))
    return Y


def fair_es(X, y):
    """X (M, d) ensemble, y (d,): fair energy score with the RMS norm."""
    M = X.shape[0]
    rms = lambda v: jnp.sqrt(jnp.mean(v * v, -1) + 1e-12)
    return rms(X - y[None]).mean() - rms(X[:, None] - X[None]).sum() / (2.0 * M * (M - 1))   # as vw.scoring.energy_fair


def episode_loss(th, x, Y, U, keys, scale, remat=False):
    """Mean over the ticks of an observed episode of the fair energy score of the one-tick forecasts (scaled)."""
    _, YF = assimilate(th, x, Y, U, keys, remat=remat)
    return jax.vmap(lambda yf, y: fair_es(yf / scale, y / scale))(YF, Y[1:]).mean()


def lab_loss(th, X0, Ys, Us, keys, scale, remat=False):
    """X0 (E, M, C, H, W) members per episode, Ys (E, T + 1, NOBS), Us (E, T, NW), keys (E, M)."""
    return jax.vmap(lambda x, Y, U, k: episode_loss(th, x, Y, U, k, scale, remat))(X0, Ys, Us, keys).mean()


# ----------------------------------------------------------------------------- the hypothesis: coordinates and fit
# z: 248 unconstrained-ish numbers, all of order 1 under the prior. The net weights in units of their prior SD; the
# log-uniform scalars and kappa as the position of log(value) in their range (kappa's range starts at 1e-6, which
# stands for kappa = 0); the uniform scalars as the position in their range. dens is not fitted: the nudge holds every
# member to the observed block means, so the fit loss does not depend on it; it is set from the observed mean mass.
NETS = (("W1", (FAM.F, FAM.HID), FAM.G1 / FAM.F ** 0.5), ("b1", (FAM.HID,), 1.0), ("W2", (FAM.HID, FAM.O), FAM.HID ** -0.5))
BOX = (("beta", "log", 2.0, 60.0, ()), ("alpha", "log", 0.3, 30.0, ()), ("kappa", "log", 1e-6, 0.1, ()),
       ("gam", "lin", 0.0, 2.0, ()), ("mu", "lin", 0.05, 0.25, ()), ("gr", "lin", 0.0, 3.0, ()), ("wq", "lin", 0.0, 2.0, (FAM.C,)))
NZ_NET = sum(math.prod(s) for _, s, _ in NETS)
NZ = NZ_NET + sum(math.prod(s) if s else 1 for *_, s in BOX)


def to_z(th):
    parts = [jnp.ravel(jnp.asarray(th[k]) / sd) for k, _, sd in NETS]
    for k, kind, lo, hi, _ in BOX:
        v = jnp.ravel(jnp.asarray(th[k], jnp.float64))
        if kind == "log":
            parts.append((jnp.log(jnp.maximum(v, lo)) - jnp.log(lo)) / (jnp.log(hi) - jnp.log(lo)))
        else:
            parts.append((v - lo) / (hi - lo))
    return jnp.concatenate(parts)


def from_z(z, dens):
    th, i = {}, 0
    for k, shp, sd in NETS:
        n = math.prod(shp)
        th[k] = z[i:i + n].reshape(shp) * sd
        i += n
    for k, kind, lo, hi, shp in BOX:
        n = math.prod(shp) if shp else 1
        v = jnp.clip(z[i:i + n], 0.0, 1.0)
        v = jnp.exp(jnp.log(lo) + v * (jnp.log(hi) - jnp.log(lo))) if kind == "log" else lo + v * (hi - lo)
        th[k] = v.reshape(shp) if shp else v[0]
        i += n
    th["dens"] = jnp.asarray(dens)
    return th


def clip_z(z):
    return z.at[NZ_NET:].set(jnp.clip(z[NZ_NET:], 0.0, 1.0))


def dens_of(Ys):
    """The observed mean mass per kind (block means of the two kinds, averaged): (C,)."""
    return jnp.asarray(Ys).reshape(-1, C + 1, G * G)[:, :C].mean((0, 2))


def nudged_states(th, x, Y, U, keys):
    """The assimilation's members after the nudge at every observed tick: (T + 1, M, C, H, W); no gradient."""
    th = jax.tree_util.tree_map(lax.stop_gradient, th)
    x0 = jax.vmap(nudge, (0, None))(x, Y[0])

    def body(x, inp):
        t, y, u = inp
        xn = jax.vmap(nudge, (0, None))(jax.vmap(lambda xx, k: _tick(th, xx, k, t, u))(x, keys), y)
        return xn, xn
    _, XS = lax.scan(body, x0, (jnp.arange(U.shape[0]), Y[1:], U))
    return jnp.concatenate([x0[None], XS], 0)


def episode_loss_k(th, x, Y, U, keys, scale, anchors, k: int):
    """The exam's own score on a Lab episode: from the assimilated members at each anchor tick a (array, a + k <= T),
    a free forecast of k ticks under the episode's commands, scored by the fair energy score against Y[a + k].
    Gradient through the k forecast ticks (recomputed in the backward pass), not through the assimilation."""
    T = U.shape[0]
    XS = nudged_states(th, x, Y[: T - k + 1], U[: T - k], keys)              # anchors are at most T - k

    def one(a):
        xa = lax.dynamic_index_in_dim(XS, a, 0, keepdims=False)
        Ua = lax.dynamic_slice_in_dim(U, a, k, 0)
        kf = jax.vmap(lambda kk: jax.random.fold_in(kk, 1000 + a))(keys)

        def body(x, inp):
            t, u = inp
            return jax.vmap(lambda xx, kk: _tick_remat(th, xx, kk, t, u))(x, kf), None
        xk, _ = lax.scan(body, xa, (a + jnp.arange(k), Ua))
        y = lax.dynamic_index_in_dim(Y, a + k, 0, keepdims=False)
        return fair_es(jax.vmap(view)(xk) / scale, y / scale)
    return jax.vmap(one)(anchors).mean()


def fit_step_fn_k(k: int):
    """value_and_grad of the k-tick Lab loss with respect to z; anchors (E, A) per episode."""
    def f(z, dens, X0, Ys, Us, keys, scale, anchors):
        th = from_z(z, dens)
        return jax.vmap(lambda x, Y, U, kk, an: episode_loss_k(th, x, Y, U, kk, scale, an, k))(X0, Ys, Us, keys, anchors).mean()
    return jax.jit(jax.value_and_grad(f))


def lab_loss_k(th, X0, Ys, Us, keys, scale, anchors, k: int):
    return jax.vmap(lambda x, Y, U, kk, an: episode_loss_k(th, x, Y, U, kk, scale, an, k))(X0, Ys, Us, keys, anchors).mean()


def fit_step_fn(remat=True):
    """value_and_grad of the Lab fit loss with respect to z, jitted."""
    def f(z, dens, X0, Ys, Us, keys, scale):
        return lab_loss(from_z(z, dens), X0, Ys, Us, keys, scale, remat)
    return jax.jit(jax.value_and_grad(f))


def adam(z, g, st, lr, b1=0.9, b2=0.999, eps=1e-8):
    m, v, n = st
    n = n + 1
    m = b1 * m + (1 - b1) * g
    v = b2 * v + (1 - b2) * g * g
    z = z - lr * (m / (1 - b1 ** n)) / (jnp.sqrt(v / (1 - b2 ** n)) + eps)
    return clip_z(z), (m, v, n)


def predict(th, x, hist, Ptest, keys, queries):
    """One item: assimilate its history (P + 1, NOBS) from members x (M, ...), then simulate under its test
    program (H, NW). Returns samples (M, len(queries), NOBS)."""
    P = hist.shape[0] - 1
    xa, _ = assimilate(th, x, hist, jnp.zeros((P, NW)), keys)
    kf = jax.vmap(lambda k: jax.random.fold_in(k, 77))(keys)
    Y = forecast(th, xa, Ptest, kf, P)                                  # (H, M, NOBS)
    return jnp.moveaxis(Y[jnp.asarray(queries) - 1], 0, 1)


# ----------------------------------------------------------------------------- stage 2: designed Lab programs (addendum 3)
def designed_prog(e: int, last_frame) -> "np.ndarray":
    """(H, NW) designed program of Lab episode e: the episode cap spread evenly over all H test ticks (EP_CAP / H =
    12.5 nats per tick); even test ticks an aimed push on the densest block of the last revealed frame, odd ticks a
    regional push on the 3 x 3 blocks around it; direction 2 pi (e mod 8) / 8. Uses nothing of the hidden world."""
    import numpy as np
    U = np.zeros((FL.H, NW))
    b = FL._densest(last_frame)
    r, c = divmod(b, G)
    phi = 2.0 * math.pi * (e % 8) / 8.0
    s2 = 2.0 * (FL.EP_CAP / FL.H) * FL.SIGW ** 2 * (1 - 1e-9)          # sum of u^2 per tick
    reg = [((r + dy) % G) * G + (c + dx) % G for dy in (-1, 0, 1) for dx in (-1, 0, 1)]
    for t in range(FL.H):
        blocks = [b] if t % 2 == 0 else reg
        a = math.sqrt(s2 / len(blocks))
        for bb in blocks:
            U[t, bb], U[t, G * G + bb] = a * math.cos(phi), a * math.sin(phi)
    return np.clip(U, -FL.U_MAX * 0.999, FL.U_MAX * 0.999)


def run_lab_designed(world, secret, n: int, chunk: int) -> dict:
    """A Lab of n designed episodes (labels 0..n-1, so episode e starts from the same state and free-tick noise as
    episode e of the mix Lab with the same secret: a paired comparison of programs)."""
    import numpy as np
    lab = FL.FBatchLab(world, secret, nats=FL.budget(), max_ticks=None, reset_cost=1)
    out = []
    for s in range(0, n, chunk):
        e = min(n, s + chunk)
        mk = lambda i, hist, s=s: FL.dense_to_prog(designed_prog(s + i, np.asarray(hist)[-1]))
        out.append(lab.run_batch(list(range(s, e)), FL.P, FL.H, mk))
    res = {k: np.concatenate([o[k] for o in out]) for k in out[0]}
    res["cls"] = np.array(["z"] * n)
    res["usage"] = lab.usage()
    return res


# ----------------------------------------------------------------------------- stage 2: batched fit (B fits at once)
def lab_scale(labY):
    """Per-channel SD of the Lab frames (public), repeated over blocks: (NOBS,)."""
    import numpy as np
    sd = np.asarray(labY, float).reshape(-1, C + 1, G * G).std((0, 2))
    return np.repeat(np.maximum(sd, 1e-12), G * G)


_FNS = {}


def _fns(k: int, burn: int):
    key = (k, burn)
    if key not in _FNS:
        def one_loss(z, dens, X0, Ys, Us, keys, scale, anchors):
            th = from_z(z, dens)
            return jax.vmap(lambda x, Y, U, kk, an: episode_loss_k(th, x, Y, U, kk, scale, an, k))(X0, Ys, Us, keys, anchors).mean()
        vg = jax.jit(jax.vmap(jax.value_and_grad(one_loss)))
        ev = jax.jit(jax.vmap(one_loss))
        sp = jax.jit(jax.vmap(lambda z, dens, keys: spin(from_z(z, dens), keys, burn)))
        _FNS[key] = (vg, ev, sp)
    return _FNS[key]


def fit_batch(Z0, dens, labY, labU, scale, key, steps=200, lr=(0.03, 0.01), lr_switch=0.75, eb=8, M=4, A=2, k=16,
              pool=16, burn=300, respin=50, t_max=None, log=None, tag=""):
    """Adam on B fits at once. Z0 (B, NZ) starts; dens (B, C); labY (B, E, T + 1, NOBS); labU (B, E, T, NW); scale
    (B, NOBS). Each step: eb random episodes per fit, M members from the fit's pool (spun at its current weights,
    renewed every `respin` steps), A random anchors in [0, T - k]; noise keys fixed per (fit, episode) (common random
    numbers). Assimilation only up to the last anchor. Returns (Z (B, NZ), trace (steps, B))."""
    import numpy as np
    vg, _, sp = _fns(k, burn)
    B, E, T1 = labY.shape[:3]
    T = T1 - 1
    amax = T - k
    Z = jnp.asarray(Z0)
    st = (jnp.zeros_like(Z), jnp.zeros_like(Z), 0)
    rng = np.random.default_rng(int(jax.random.randint(key, (), 0, 2 ** 31 - 1)))
    kb = lambda tag_, n: jax.vmap(lambda b: jax.vmap(lambda j: jax.random.fold_in(jax.random.fold_in(jax.random.fold_in(key, tag_), b), j))(jnp.arange(n)))(jnp.arange(B))
    ep_keys = kb(1, E * M).reshape(B, E, M)
    Y, U = jnp.asarray(labY), jnp.asarray(labU)
    dens = jnp.asarray(dens)
    scale = jnp.asarray(scale)
    trace = []
    t0 = __import__("time").time()
    for it in range(steps):
        if it % respin == 0:
            P_ = sp(Z, dens, kb(100 + it, pool))                                   # (B, pool, C, H, W)
        ei = np.stack([rng.choice(E, eb, replace=False) for _ in range(B)])        # (B, eb)
        an = rng.integers(0, amax + 1, (B, eb, A))
        mi = rng.integers(0, pool, (B, eb * M))
        X0 = jnp.take_along_axis(P_, jnp.asarray(mi)[:, :, None, None, None], 1).reshape((B, eb, M) + P_.shape[2:])
        bi = jnp.arange(B)[:, None]
        Ys = Y[bi, jnp.asarray(ei), : amax + k + 1]
        Us = U[bi, jnp.asarray(ei), : amax + k]
        keys = ep_keys[bi, jnp.asarray(ei)]
        l, g = vg(Z, dens, X0, Ys, Us, keys, scale, jnp.asarray(an))
        rate = lr[0] if it < lr_switch * steps else lr[1]
        Z, st = adam(Z, g, st, rate)
        trace.append(np.asarray(l))
        if log and (it + 1) % 50 == 0:
            log(f"  fit{tag} step {it + 1}/{steps}: window loss median {float(np.median(trace[-1])):.4f} ({__import__('time').time() - t0:.0f}s)")
        if t_max is not None and __import__("time").time() - t0 > t_max:
            if log:
                log(f"  fit{tag}: stopped at step {it + 1} by its time limit")
            break
    return Z, np.stack(trace)


def eval_batch(Z, dens, labY, labU, scale, key, M=4, k=16, pool=8, burn=300, every=8, E_max=None, E_chunk=8):
    """Fit loss of B weight vectors on all (or the first E_max) Lab episodes: fixed keys, M members from a pool spun
    at each weight vector with the same keys, anchors 0, every, ..., T - k; episodes in chunks of E_chunk (memory).
    Returns (B,)."""
    import numpy as np
    _, ev, sp = _fns(k, burn)
    B, E = labY.shape[:2]
    E = E if E_max is None else min(E, E_max)
    T = labY.shape[2] - 1
    kb = lambda tag_, n: jax.vmap(lambda b: jax.vmap(lambda j: jax.random.fold_in(jax.random.fold_in(key, tag_), j))(jnp.arange(n)))(jnp.arange(B))
    P_ = sp(jnp.asarray(Z), jnp.asarray(dens), kb(7, pool))
    mi = np.arange(E * M) % pool
    X0 = P_[:, mi].reshape((B, E, M) + P_.shape[2:])
    keys = kb(8, E * M).reshape(B, E, M)
    tot = np.zeros(B)
    for e0 in range(0, E, E_chunk):
        e1 = min(E, e0 + E_chunk)
        an = jnp.asarray(np.tile(np.arange(0, T - k + 1, every), (B, e1 - e0, 1)))
        tot += (e1 - e0) * np.asarray(ev(jnp.asarray(Z), jnp.asarray(dens), X0[:, e0:e1], jnp.asarray(labY[:, e0:e1]),
                                         jnp.asarray(labU[:, e0:e1]), keys[:, e0:e1], jnp.asarray(scale), an))
    return tot / E


_PRED = {}


def predict_items(th, hist, Ptest, key, m=24, burn=300, chunk=16, queries=(8, 16, 32)):
    """W's samples for every item of one world: (n_items, m, len(queries), NOBS). A pool of m members spun at th;
    every item assimilates its history from the pool with its own noise keys, then simulates under its program."""
    import numpy as np
    kq = (tuple(queries), burn)
    if kq not in _PRED:
        _PRED[kq] = (jax.jit(spin, static_argnums=2),
                     jax.jit(lambda th, x, h, p, kk: jax.vmap(lambda hh, pp, k_: predict(th, x, hh, pp, k_, list(queries)))(h, p, kk)))
    sp, pr = _PRED[kq]
    x = sp(th, jax.vmap(lambda j: jax.random.fold_in(key, j))(jnp.arange(m)), burn)
    n = hist.shape[0]
    out = []
    for s in range(0, n, chunk):
        e = min(n, s + chunk)
        kk = jax.vmap(lambda i: jax.vmap(lambda j: jax.random.fold_in(jax.random.fold_in(key, 1000 + i), j))(jnp.arange(m)))(jnp.arange(s, e))
        out.append(np.asarray(pr(th, x, jnp.asarray(hist[s:e]), jnp.asarray(Ptest[s:e]), kk)))
    return np.concatenate(out)
