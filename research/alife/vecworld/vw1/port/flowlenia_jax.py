"""flowlenia_jax -- Flow-Lenia (Plantec et al. 2023) as a VW-1 Level, float64, periodic box.

A port of level0/flowlenia.py (numpy; itself checked against the authors' JAX code) to pure JAX:
same kernels, affinity, periodic Sobel flow, alpha mixing and the mass-conserving reintegration
tracking (a 2*sigma square per source split over the <= 3x3 cells it overlaps, normalised by the
computed weight sum so every source sends out exactly what it holds). The scatter goes into a grid
padded by P = dd + 1 cells whose margins are folded back, in the same order as the numpy code.

Split of the parameters
    params (differentiable pytree, the Level's `params`): R, r, a, b, w, m, s, h
    cfg    (static Python numbers): C, k, c0, c1, dt, sigma, dd, n, theta_A, alpha_src, R_scale, H, W
The kernel FFTs are a function of params (so autodiff reaches kernel widths); `step` recomputes
them unless given precomputed ones (`substep(..., fK=)`), and the strided tick computes them once.

Level (one Flow-Lenia substep; vw.stride makes the VW-0 tick of 20 substeps):
    init(params, key)        -> A0 (C, H, W): init_patches in JAX (same declared distribution)
    step(params, A, noise, u) = reintegrate(kappa(A, u), flow(kappa(A, u)) + std * xi)
    kappa: the VW-0 zero-sum kick (integrate/lenia_world.Level0.kick), one actuator per cell.
"""
from __future__ import annotations

import json
import os
from dataclasses import dataclass
from typing import Optional

import jax

jax.config.update("jax_enable_x64", True)
import jax.numpy as jnp  # noqa: E402
import numpy as np  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
VEC = os.path.dirname(os.path.dirname(HERE))          # .../evalwork/vecworld
L0_DIR = os.path.join(VEC, "level0")

PARAM_KEYS = ("R", "r", "a", "b", "w", "m", "s", "h")


@dataclass(frozen=True)
class FLConfig:
    C: int
    k: int
    c0: tuple
    c1: tuple
    dt: float
    sigma: float
    dd: int
    n: float
    theta_A: float
    alpha_src: str
    R_scale: float
    H: int
    W: int


def load_world(name: str = "A_gliders"):
    """(cfg, params, meta) from level0/worlds/<name>/params.json."""
    P = json.load(open(os.path.join(L0_DIR, "worlds", name, "params.json")))
    p = P["params"]
    size = int(P["init"]["size"])
    cfg = FLConfig(C=int(p["C"]), k=int(p["k"]), c0=tuple(int(i) for i in p["c0"]), c1=tuple(int(i) for i in p["c1"]),
                   dt=float(p["dt"]), sigma=float(p["sigma"]), dd=int(p["dd"]), n=float(p["n"]),
                   theta_A=float(p["theta_A"]), alpha_src=str(p.get("alpha_src", "sum")),
                   R_scale=float(p.get("R_scale", 1.0)), H=size, W=size)
    params = {"R": jnp.asarray(float(p["R"])), **{q: jnp.asarray(np.asarray(p[q], float)) for q in PARAM_KEYS[1:]}}
    return cfg, params, P


def numpy_params(cfg: FLConfig, params) -> dict:
    """Back to the level0/flowlenia.py dict (noise off)."""
    d = {"C": cfg.C, "k": cfg.k, "c0": list(cfg.c0), "c1": list(cfg.c1), "dt": cfg.dt, "sigma": cfg.sigma,
         "dd": cfg.dd, "n": cfg.n, "theta_A": cfg.theta_A, "alpha_src": cfg.alpha_src, "R_scale": cfg.R_scale,
         "noise": {"mode": "none", "std": 0.0, "seed": 0}}
    for q in PARAM_KEYS:
        v = np.asarray(params[q], float)
        d[q] = float(v) if v.ndim == 0 else v.tolist()
    return d


# ----------------------------------------------------------------------------- the law
def kernel_fft(cfg: FLConfig, p):
    H, W = cfg.H, cfg.W
    y = np.minimum(np.arange(H), H - np.arange(H))[:, None].astype(float)
    x = np.minimum(np.arange(W), W - np.arange(W))[None, :].astype(float)
    dist = jnp.asarray(np.sqrt(x ** 2 + y ** 2))
    D = dist[None] / ((p["R"] + 15.0) * p["r"][:, None, None] * cfg.R_scale)          # (k, H, W)
    sig = 0.5 * (jnp.tanh(-(D - 1.0) * 10.0 / 2.0) + 1.0)
    a, b, w = (p[q][:, None, None, :] for q in "abw")
    K = sig * (b * jnp.exp(-(D[..., None] - a) ** 2 / w)).sum(-1)
    K = K / K.sum((1, 2), keepdims=True)
    return jnp.fft.rfft2(K, axes=(-2, -1))


def sobel(X):
    sy = jnp.roll(X, -1, -2) - jnp.roll(X, 1, -2)
    gy = 2.0 * sy + jnp.roll(sy, 1, -1) + jnp.roll(sy, -1, -1)
    sx = jnp.roll(X, -1, -1) - jnp.roll(X, 1, -1)
    gx = 2.0 * sx + jnp.roll(sx, 1, -2) + jnp.roll(sx, -1, -2)
    return gy, gx


def affinity(cfg: FLConfig, p, A, fK):
    H, W = cfg.H, cfg.W
    fA = jnp.fft.rfft2(A, axes=(-2, -1))
    Uk = jnp.fft.irfft2(fA[np.asarray(cfg.c0)] * fK, s=(H, W), axes=(-2, -1))
    G = (2.0 * jnp.exp(-0.5 * ((Uk - p["m"][:, None, None]) / p["s"][:, None, None]) ** 2) - 1.0) * p["h"][:, None, None]
    # sum of the kernels feeding each channel (a segment sum: no matmul, so no BLAS reordering)
    c1 = np.asarray(cfg.c1)
    return jnp.stack([G[np.flatnonzero(c1 == c)].sum(0) for c in range(cfg.C)])


def flow(cfg: FLConfig, p, A, fK):
    # optimization barriers (here and in substep) stop XLA from re-computing the affinity and the
    # flow inside each of the reintegration's consumer fusions: 2.2x faster per substep on CPU
    U = jax.lax.optimization_barrier(affinity(cfg, p, A, fK))
    gUy, gUx = sobel(U)
    gAy, gAx = sobel(A.sum(0))
    src = A.sum(0, keepdims=True) if cfg.alpha_src == "sum" else A
    alpha = jnp.clip((src / cfg.theta_A) ** cfg.n, 0.0, 1.0)
    return gUy * (1.0 - alpha) - gAy * alpha, gUx * (1.0 - alpha) - gAx * alpha


def reintegrate(cfg: FLConfig, A, Fy, Fx):
    C, H, W = A.shape
    sig, dt, P = cfg.sigma, cfg.dt, cfg.dd + 1
    ma = cfg.dd - sig
    Hp, Wp = H + 2 * P, W + 2 * P
    dy = jnp.clip(dt * Fy, -ma, ma)
    dx = jnp.clip(dt * Fx, -ma, ma)
    ry, rx = jnp.rint(dy), jnp.rint(dx)
    fy, fx = dy - ry, dx - rx
    wy = [jnp.clip(jnp.minimum(o + 0.5, fy + sig) - jnp.maximum(o - 0.5, fy - sig), 0, None) for o in (-1, 0, 1)]
    wx = [jnp.clip(jnp.minimum(o + 0.5, fx + sig) - jnp.maximum(o - 0.5, fx - sig), 0, None) for o in (-1, 0, 1)]
    An = A / ((wy[0] + wy[1] + wy[2]) * (wx[0] + wx[1] + wx[2]))
    iyy = jnp.arange(H)[:, None] + P
    ixx = jnp.arange(W)[None, :] + P
    pbase = (jnp.arange(C) * Hp * Wp)[:, None, None]
    base = pbase + (ry.astype(jnp.int64) + iyy) * Wp + (rx.astype(jnp.int64) + ixx)
    vals, idx = [], []
    for i, o in enumerate((-1, 0, 1)):
        t = An * wy[i]
        for j, o2 in enumerate((-1, 0, 1)):
            vals.append(t * wx[j])
            idx.append(base + (o * Wp + o2))
    vals = jnp.stack(vals).ravel()
    idx = jnp.stack(idx).ravel()
    out = jnp.zeros(C * Hp * Wp).at[idx].add(vals, indices_are_sorted=False, unique_indices=False)
    out = out.reshape(C, Hp, Wp)
    out = out.at[:, P:2 * P, :].add(out[:, H + P:, :])
    out = out.at[:, H:H + P, :].add(out[:, :P, :])
    out = out.at[:, :, P:2 * P].add(out[:, :, W + P:])
    out = out.at[:, :, W:W + P].add(out[:, :, :P])
    return out[:, P:H + P, P:W + P]


def kick(cfg: FLConfig, A, u):
    """VW-0 kick (lenia_world.Level0.kick) for one member, jittable. u (H*W,): commanded matter
    moves per cell. A source (u < 0) removes min(-u, A_sum) with the cell's channel composition;
    for a zero-sum command the sinks (u > 0) receive the pooled matter in the commanded
    proportions (mass of every channel conserved to round-off); a non-zero-sum command (designer
    probes only; never reaches the world through the VW-1 port, which canonicalises to zero sum)
    adds its positive part split equally over channels, as in VW-0."""
    C, HW = cfg.C, cfg.H * cfg.W
    Af = A.reshape(C, HW)
    src, snk = u < 0, u > 0
    S = Af.sum(0)
    take = jnp.where(src, jnp.minimum(-u, jnp.maximum(S, 0.0)), 0.0)
    frac = jnp.where(src & (S > 0), take / jnp.maximum(S, 1e-300), 0.0)
    removed = Af * frac[None, :]
    pooled = removed.sum(1)
    w = jnp.where(snk, u, 0.0)
    ws = w.sum()
    zs = jnp.abs(u.sum()) <= 1e-9 * jnp.maximum(1.0, jnp.abs(u).sum())
    give_c = jnp.where((ws > 0) & (pooled.sum() > 0), pooled[:, None] * (w / jnp.where(ws > 0, ws, 1.0))[None, :], 0.0)
    give_n = jnp.broadcast_to(w[None, :] / C, Af.shape)
    Af = Af - removed + jnp.where(zs, give_c, give_n)
    Af = jnp.where(src[None, :], jnp.maximum(Af, 0.0), Af)
    return Af.reshape(A.shape)


def substep(cfg: FLConfig, p, A, xi=None, std: float = 0.0, fK=None):
    """One Flow-Lenia update A(t) -> A(t + dt) (no kick); xi (2, C, H, W) standard normals."""
    fK = kernel_fft(cfg, p) if fK is None else fK
    Fy, Fx = flow(cfg, p, A, fK)
    if xi is not None and std > 0:
        Fy = Fy + std * xi[0]
        Fx = Fx + std * xi[1]
    Fy, Fx = jax.lax.optimization_barrier((Fy, Fx))
    return reintegrate(cfg, A, Fy, Fx)


# ----------------------------------------------------------------------------- initial law
def init_patches(cfg: FLConfig, key, n_patches: int = 10, L: int = 12, amp: float = 1.0, tries: int = 200):
    """flowlenia.init_patches in JAX: n_patches LxL patches of U(0, amp) per channel at random,
    non-overlapping (torus distance >= 1.2 L) centres by rejection with `tries` draws per patch
    (the last draw is kept when none passes, as in numpy). Same distribution, other random stream."""
    C, H, W = cfg.C, cfg.H, cfg.W
    A = jnp.zeros((C, H, W))
    min_sep2 = (L * 1.2) ** 2
    ks = jax.random.split(key, 2 * n_patches)
    cents = []
    for j in range(n_patches):
        cy = jax.random.randint(jax.random.fold_in(ks[2 * j], 0), (tries,), 0, H)
        cx = jax.random.randint(jax.random.fold_in(ks[2 * j], 1), (tries,), 0, W)
        if cents:
            ok = jnp.ones((tries,), bool)
            for (y0, x0) in cents:
                dy = jnp.minimum(jnp.abs(cy - y0), H - jnp.abs(cy - y0))
                dx = jnp.minimum(jnp.abs(cx - x0), W - jnp.abs(cx - x0))
                ok = ok & (dy ** 2 + dx ** 2 >= min_sep2)
            i = jnp.where(ok.any(), jnp.argmax(ok), tries - 1)
        else:
            i = 0
        c = (cy[i], cx[i])
        cents.append(c)
        ys = (jnp.arange(L) + c[0] - L // 2) % H
        xs = (jnp.arange(L) + c[1] - L // 2) % W
        vals = jax.random.uniform(ks[2 * j + 1], (C, L, L), minval=0.0, maxval=amp)
        A = A.at[:, ys[:, None], xs[None, :]].set(vals)
    return A


# ----------------------------------------------------------------------------- the Level
def make_level(name: str = "A_gliders", noise_std: float = 0.5, init_cfg: Optional[dict] = None):
    """(Level, cfg, meta): one Flow-Lenia substep with the VW-0 kick and flow noise noise_std."""
    import vw
    cfg, params, meta = load_world(name)
    ic = dict(meta["init"]) if init_cfg is None else dict(init_cfg)
    npch, L = int(ic.get("n_patches", 10)), int(ic.get("L", 12))
    std = float(noise_std)
    shape = (cfg.C, cfg.H, cfg.W)

    def init(p, key):
        return init_patches(cfg, key, npch, L)

    def step(p, A, nz, u):
        A = kick(cfg, A, u)
        xi = nz.normal((2,) + shape) if std > 0 else None
        return substep(cfg, p, A, xi, std)

    cons = {f"mass_c{c}": (lambda c: (lambda A: A[c].sum()))(c) for c in range(cfg.C)}
    lev = vw.Level(init=init, step=step, input_dim=cfg.H * cfg.W, params=params, conserved=cons,
                   name=f"FlowLenia[{name}]")
    return lev, cfg, meta
