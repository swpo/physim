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
    XS = nudged_states(th, x, Y, U, keys)

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
