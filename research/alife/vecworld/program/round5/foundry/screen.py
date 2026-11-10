"""screen -- cheap certificates of a batch of worlds (study foundry, round 5).

One "draw" is one world (one theta). For every draw, in one compiled program per chunk of draws:

  main run   M members: init, `burn` ticks, then T recorded ticks. Per tick: the block view y (Q x G x G),
             the fraction of matter relocated, masses, extremes; the blob tracker on the first M_trk members.
  test set   the last M - M_fit members at n_snap snapshot ticks (T/n_snap, 2T/n_snap, ...): NS test states.
  branches   from each test state R replicas with fresh noise for HB ticks (the small-branch oracle and
             the noise-twin divergence), and R2 replicas under a neighbouring theta' (sensitivity to the
             hidden weights).
  closure    a fixed cheap predictor fitted per world in closed form on the M_fit fit members: a local,
             translation-equivariant ridge (3 x 3 block neighbourhood x Q channels x 2 lags + bias -> the
             Q channels of the centre block at t + h), evaluated on the test states against the replicas.
             All in units of the climatological variance per channel (standardised with the fit members):
                 V_clim, V_pers (persistence), V_pred (ridge), V_orc (unbiased replica variance),
                 ceiling c(h) = (V_clim - V_pred) / (V_clim - V_orc), gap g(h) = V_pred - V_orc.
  twins      V_orc(h) for h = 1..HB and the fine L1 distance (fraction of matter placed differently)
             between replicas 0 and 1.
  theta'     plug-in loss PL(h) = |mean_theta - mean_theta'|^2 - V_orc/R - V_orc'/R2 (bias-corrected), and
             the fine L1 distance between replica 0 of theta and of theta'.
  tracker    bodies, mass in bodies, radius, instantaneous and 8-tick net speed, births/deaths/fusions/
             fissions, overflow counters.
  spectrum   radial power spectrum of the final total density (mean over members).

The functions are generic in the world (`WorldDef`), so the gliders world can be measured by the same code.
Data are passed to the compiled functions as arguments (never closed over).
"""
from __future__ import annotations

import os
import sys
from dataclasses import dataclass
from typing import Any, Callable

sys.dont_write_bytecode = True
HERE = os.path.dirname(os.path.abspath(__file__))
if HERE not in sys.path:
    sys.path.insert(0, HERE)

import jax  # noqa: E402
import jax.numpy as jnp  # noqa: E402
import numpy as np  # noqa: E402
from jax import lax  # noqa: E402

import tnca as TN  # noqa: E402  (sets the vw path, float64)
import vw  # noqa: E402
from vw.core import Noise  # noqa: E402
from vw import objects as OB  # noqa: E402

HZ = (1, 2, 4, 8, 16, 32)
_K_INIT, _K_BURN, _K_DYN, _K_BR, _K_BR2 = 1, 2, 3, 100, 200


@dataclass(frozen=True)
class Sizes:
    M: int = 6
    M_fit: int = 4
    M_trk: int = 2
    burn: int = 50
    T: int = 240
    n_snap: int = 4
    R: int = 4
    R2: int = 2
    HB: int = 32
    G: int = 8
    lag_v: int = 8            # lag of the net-speed measure (ticks)
    frame_every: int = 0      # > 0: return frames of member 0 every this many ticks
    ridge: float = 1e-4

    @property
    def NS(self) -> int:
        return (self.M - self.M_fit) * self.n_snap

    @property
    def hz(self):
        return tuple(h for h in HZ if h <= self.HB)


@dataclass(frozen=True)
class WorldDef:
    """What the screen needs from a world family."""
    name: str
    shape: tuple                 # (C, H, W)
    init: Callable               # (th, key) -> x
    tick: Callable               # (th, x, Noise) -> x
    view: Callable               # x -> (Q, G, G)
    trk: Any                     # vw.objects.BlobTracker
    trk_field: Callable          # x -> field given to the tracker


def tnca_world(fam: TN.Family = TN.FAM, G: int = 8) -> WorldDef:
    return WorldDef(name="tnca", shape=(fam.C, fam.H, fam.W), init=lambda th, k: TN.init(th, k, fam),
                    tick=lambda th, x, nz: TN.tick_free(th, x, nz, fam), view=lambda x: TN.block_view(x, G),
                    trk=TN.tracker(fam), trk_field=TN.tracker_field)


# ----------------------------------------------------------------------------- simulation
_TAB = (0, 1, 7, 10, 11, 12, 13, 14, 15, 16)      # present, mass, rg, vx, vy, cy, cx, age, event, uid
_P, _MS, _RG, _VX, _VY, _CY, _CX, _AGE, _EV, _UID = range(10)


def simulate_one(wd: WorldDef, sz: Sizes, th, th2, key):
    """Everything simulated for one draw. Returns a dict of device arrays."""
    C, H, W = wd.shape
    M, Mt = sz.M, sz.M_trk
    bt = wd.trk
    fold = jax.random.fold_in
    mk = jax.vmap(lambda i: fold(key, i))(jnp.arange(M))
    x = jax.vmap(lambda k: wd.init(th, fold(k, _K_INIT)))(mk)
    kb = jax.vmap(lambda k: fold(k, _K_BURN))(mk)
    kd = jax.vmap(lambda k: fold(k, _K_DYN))(mk)
    step = lambda x, k, t: jax.vmap(lambda xx, kk: wd.tick(th, xx, Noise(kk, t)))(x, k)
    mass0 = x.sum((1, 2, 3))

    x, _ = lax.scan(lambda x, t: (step(x, kb, t), None), x, jnp.arange(sz.burn))
    m = jax.vmap(lambda xx: bt.init_memory(wd.trk_field(xx)))(x[:Mt])
    g0 = jax.vmap(lambda mm: bt.split(mm)["globals"])(m)

    def tab(m):
        return jax.vmap(lambda mm: bt.split(mm)["table"][:, jnp.array(_TAB)])(m)

    def body(c, t):
        x, m = c
        xn = step(x, kd, t)
        mn = jax.vmap(lambda mm, xx: bt.update_memory(mm, wd.trk_field(xx)))(m, xn[:Mt])
        S = xn.sum(1)
        rec = dict(y=jax.vmap(wd.view)(xn),
                   moved=0.5 * jnp.abs(xn - x).sum((1, 2, 3)) / x.sum((1, 2, 3)),
                   mass=xn.sum((2, 3)), xmin=xn.min((1, 2, 3)), smax=S.max((1, 2)),
                   pr=S.sum((1, 2)) ** 2 / (H * W * (S * S).sum((1, 2))),
                   tab=tab(mn))
        if sz.frame_every:
            rec["x0"] = xn[0].astype(jnp.float32)
        return (xn, mn), rec

    seg = sz.T // sz.n_snap
    recs, snaps = [], []
    y0 = jax.vmap(wd.view)(x)
    tab0 = tab(m)
    x_start = x[0]
    for s in range(sz.n_snap):
        (x, m), rec = lax.scan(body, (x, m), jnp.arange(s * seg, (s + 1) * seg))
        if sz.frame_every:
            rec["x0"] = rec["x0"][sz.frame_every - 1::sz.frame_every]
        recs.append(rec)
        snaps.append(x[sz.M_fit:])
    rec = {k: jnp.concatenate([r[k] for r in recs], 0) for k in recs[0]}
    out = dict(rec)
    out["y"] = jnp.concatenate([y0[None], rec["y"]], 0)               # (T + 1, M, Q, G, G)
    out["tab"] = jnp.concatenate([tab0[None], rec["tab"]], 0)         # (T + 1, Mt, K, 10)
    out["mass0"] = mass0
    out["glob"] = jax.vmap(lambda mm: bt.split(mm)["globals"])(m) - g0
    out["ovf"] = jax.vmap(lambda mm: bt.split(mm)["overflow"])(m)
    out["x_end"] = x
    if sz.frame_every:
        out["x0"] = jnp.concatenate([x_start[None].astype(jnp.float32), out["x0"]], 0)

    # branches from the test states: R replicas under theta, R2 under theta'
    xs = jnp.stack(snaps, 0).reshape((sz.NS, C, H, W))
    si = jnp.arange(sz.NS)
    ka = jax.vmap(lambda i: jax.vmap(lambda r: fold(fold(key, _K_BR + r), i))(jnp.arange(sz.R)))(si)
    k2 = jax.vmap(lambda i: jax.vmap(lambda r: fold(fold(key, _K_BR2 + r), i))(jnp.arange(sz.R2)))(si)
    xa = jnp.broadcast_to(xs[:, None], (sz.NS, sz.R, C, H, W))
    xb = jnp.broadcast_to(xs[:, None], (sz.NS, sz.R2, C, H, W))
    msum = xs.sum((1, 2, 3))
    vv = lambda f: jax.vmap(jax.vmap(f))

    def bbody(c, t):
        xa, xb = c
        xa = vv(lambda xx, kk: wd.tick(th, xx, Noise(kk, t)))(xa, ka)
        xb = vv(lambda xx, kk: wd.tick(th2, xx, Noise(kk, t)))(xb, k2)
        d_tw = 0.5 * jnp.abs(xa[:, 0] - xa[:, 1]).sum((1, 2, 3)) / msum
        d_th = 0.5 * jnp.abs(xa[:, 0] - xb[:, 0]).sum((1, 2, 3)) / msum
        return (xa, xb), (vv(wd.view)(xa), vv(wd.view)(xb), d_tw, d_th)
    _, (ya, yb, d_tw, d_th) = lax.scan(bbody, (xa, xb), jnp.arange(sz.HB))
    out.update(ya=ya, yb=yb, d_tw=d_tw, d_th=d_th)                    # (HB, NS, R | R2, Q, G, G), (HB, NS)
    return out


# ----------------------------------------------------------------------------- measures
def _nb3(z):
    """3 x 3 periodic block neighbourhood: (..., Q, G, G) -> (..., 9 Q, G, G)."""
    return jnp.concatenate([jnp.roll(z, (dy, dx), (-2, -1)) for dy in (-1, 0, 1) for dx in (-1, 0, 1)], -3)


def _radial_bins(H, W):
    ky = np.fft.fftfreq(H)[:, None] * H
    kx = np.fft.fftfreq(W)[None, :] * W
    r = np.rint(np.sqrt(ky ** 2 + kx ** 2)).astype(np.int32)
    return np.minimum(r, H // 2)                                      # (H, W) bins 0 .. H/2


def measure_one(wd: WorldDef, sz: Sizes, o):
    """The cheap certificates of one draw from simulate_one's output. Returns a dict of small arrays."""
    C, H, W = wd.shape
    T, Mf, NS, R, R2, G = sz.T, sz.M_fit, sz.NS, sz.R, sz.R2, sz.G
    hz = sz.hz
    y = o["y"]                                                        # (T + 1, M, Q, G, G)
    Q = y.shape[2]
    res = {}
    # ---- validity, density, activity
    mtot = o["mass"].sum(-1)                                          # (T, M)
    res["finite"] = (jnp.isfinite(o["x_end"]).all() & jnp.isfinite(y).all()).astype(jnp.float64)
    res["mass_drift"] = jnp.abs(mtot - o["mass0"][None]).max() / o["mass0"].min()
    res["kind_drift"] = (jnp.abs(o["mass"] - o["mass"][:1]).max((0, 1)) / o["mass"][0].mean(0))
    res["xmin"] = o["xmin"].min()
    res["smax"] = o["smax"].max()
    res["smax_end"] = o["smax"][-1].mean()
    res["pr"] = o["pr"][T // 2:].mean()
    res["moved"] = o["moved"][T // 2:].mean()
    S = o["x_end"].sum(1)                                             # (M, H, W)
    res["mean_S"] = S.mean()
    res["cv_cell"] = (S.std((1, 2)) / S.mean((1, 2))).mean()
    res["kind_frac0"] = o["mass"][-1, :, 0].mean() / mtot[-1].mean()
    # ---- spectrum of the final total density
    P = jnp.abs(jnp.fft.fft2(S - S.mean((1, 2), keepdims=True))) ** 2
    bins = jnp.asarray(_radial_bins(H, W)).reshape(-1)
    nb = H // 2 + 1
    spec = jax.vmap(lambda p: jnp.zeros((nb,)).at[bins].add(p.reshape(-1)))(P).mean(0)
    res["spec"] = spec / jnp.maximum(spec.sum(), 1e-300)
    kbar = (res["spec"] * jnp.arange(nb)).sum()
    res["wavelength"] = H / jnp.maximum(kbar, 1e-9)
    # ---- block view: standardise with the fit members
    yf = y[:, :Mf]
    mu = yf.mean((0, 1, 3, 4))
    sd = jnp.sqrt(yf.var((0, 1, 3, 4)))
    sdc = jnp.maximum(sd, 1e-12 * jnp.maximum(jnp.abs(mu), 1e-300))
    res["y_mean"], res["y_std"] = mu, sd
    res["cv_block"] = sd[:C].sum() / jnp.maximum(mu[:C].sum(), 1e-300)   # rough contrast of the block masses
    z = (y - mu[None, None, :, None, None]) / sdc[None, None, :, None, None]
    # spatial part of the block variance (time-mean pattern) vs temporal part
    zt = z[:, :Mf]
    res["var_static"] = jnp.mean(zt.mean(0) ** 2)                     # share of the variance that never moves
    # persistence error on the main run (all fit members), per horizon: E |z(t+h) - z(t)|^2
    res["vp_main"] = jnp.stack([jnp.mean((zt[h:] - zt[:-h]) ** 2) for h in hz])
    # ---- cheap predictor: local ridge on (z(t), z(t-1)) 3 x 3 neighbourhoods
    hmax = max(hz)
    nt = T - hmax                                                     # t = 1 .. T - hmax
    feat = jnp.concatenate([_nb3(z[1:]), _nb3(z[:-1])], 2)            # (T, M, 18 Q, G, G) at t = 1..T
    nf = 18 * Q + 1

    def flat(a):                                                      # (n_t, m, F, G, G) -> (n, F)
        return jnp.moveaxis(a, 2, -1).reshape(-1, a.shape[2])
    Xf = flat(feat[:nt, :Mf])
    Xf = jnp.concatenate([Xf, jnp.ones((Xf.shape[0], 1))], 1)
    n = Xf.shape[0]
    A = Xf.T @ Xf + sz.ridge * n * jnp.eye(nf)
    B = jnp.stack([Xf.T @ flat(z[1 + h:1 + h + nt, :Mf]) for h in hz], 0)        # (nh, nf, Q)
    Wt = jax.vmap(lambda b: jnp.linalg.solve(A, b))(B)                # (nh, nf, Q)
    res["fit_mse"] = jnp.stack([jnp.mean((Xf @ Wt[i] - flat(z[1 + h:1 + h + nt, :Mf])) ** 2) for i, h in enumerate(hz)])
    # ---- test states
    seg = T // sz.n_snap
    ts = jnp.arange(1, sz.n_snap + 1) * seg                           # snapshot ticks
    zs = z[ts][:, Mf:]                                                # (n_snap, M_test, Q, G, G) = z at the test states
    fs = feat[ts - 1][:, Mf:]                                         # features at t = ts (feat index t - 1)
    zs = zs.reshape((NS,) + zs.shape[2:])
    fs = fs.reshape((NS,) + fs.shape[2:])
    Xs = jnp.concatenate([jnp.moveaxis(fs, 1, -1), jnp.ones((NS, G, G, 1))], -1)     # (NS, G, G, nf)
    za = (o["ya"] - mu[:, None, None]) / sdc[:, None, None]           # (HB, NS, R, Q, G, G)
    zb = (o["yb"] - mu[:, None, None]) / sdc[:, None, None]
    hidx = jnp.array([h - 1 for h in hz])
    zah, zbh = za[hidx], zb[hidx]                                     # (nh, NS, R, Q, G, G)
    pred = jnp.moveaxis(jnp.einsum("sgkf,hfq->hsgkq", Xs, Wt), -1, 2)  # (nh, NS, Q, G, G)
    ax = (2, 3, 4, 5)
    v_clim = jnp.mean(zah ** 2, ax)                                   # (nh, NS)
    v_pers = jnp.mean((zah - zs[None, :, None]) ** 2, ax)
    v_pred = jnp.mean((zah - pred[:, :, None]) ** 2, ax)
    ma, mb = zah.mean(2), zbh.mean(2)
    v_orc = jnp.mean(((zah - ma[:, :, None]) ** 2).sum(2) / (R - 1), (2, 3, 4))
    v_orc2 = (jnp.mean(((zbh - mb[:, :, None]) ** 2).sum(2) / (R2 - 1), (2, 3, 4)) if R2 > 1
              else jnp.zeros_like(v_orc))
    pl = jnp.mean((ma - mb) ** 2, (2, 3, 4)) - v_orc / R - (v_orc2 / R2 if R2 > 1 else v_orc / R2)
    for k, v in (("v_clim", v_clim), ("v_pers", v_pers), ("v_pred", v_pred), ("v_orc", v_orc), ("pl", pl),
                 ("v_orc2", v_orc2)):
        res[k] = v.mean(1)
        res[k + "_se"] = v.std(1) / jnp.sqrt(NS)
    den = v_clim.mean(1) - v_orc.mean(1)
    res["ceil"] = (v_clim.mean(1) - v_pred.mean(1)) / jnp.where(jnp.abs(den) > 1e-12, den, jnp.nan)
    res["ceil_pers"] = (v_clim.mean(1) - v_pers.mean(1)) / jnp.where(jnp.abs(den) > 1e-12, den, jnp.nan)
    # per-channel oracle and predictor error at each horizon (which block variable is hard)
    res["v_orc_q"] = jnp.mean(((zah - ma[:, :, None]) ** 2).sum(2) / (R - 1), (1, 3, 4))      # (nh, Q)
    res["v_pred_q"] = jnp.mean((zah - pred[:, :, None]) ** 2, (1, 2, 4, 5))
    # ---- twins: replica variance at every tick, fine L1 distances
    mall = za.mean(2)
    res["twin_v"] = jnp.mean(((za - mall[:, :, None]) ** 2).sum(2) / (R - 1), (1, 2, 3, 4))   # (HB,)
    res["twin_l1"] = o["d_tw"].mean(1)
    res["theta_l1"] = o["d_th"].mean(1)
    # ---- tracker
    tb = o["tab"]                                                     # (T + 1, Mt, K, 10)
    p = tb[..., _P] > 0.5
    nbod = p.sum(-1)
    res["nb_mean"], res["nb_std"], res["nb_max"] = nbod.mean(), nbod.std(), nbod.max().astype(jnp.float64)
    npres = jnp.maximum(p.sum(), 1)
    res["body_frac"] = (tb[..., _MS] * p).sum(-1).mean() / wd.trk_field(o["x_end"][0]).sum()
    res["body_mass"] = (tb[..., _MS] * p).sum() / npres
    res["rg"] = (tb[..., _RG] * p).sum() / npres
    old = p & (tb[..., _AGE] >= 1)
    res["v_inst"] = (jnp.sqrt(tb[..., _VX] ** 2 + tb[..., _VY] ** 2) * old).sum() / jnp.maximum(old.sum(), 1)
    L = sz.lag_v
    same = p[L:] & p[:-L] & (tb[L:, ..., _UID] == tb[:-L, ..., _UID])
    mi = lambda d, n: d - n * jnp.round(d / n)
    dy, dx = mi(tb[L:, ..., _CY] - tb[:-L, ..., _CY], H), mi(tb[L:, ..., _CX] - tb[:-L, ..., _CX], W)
    res["v_net"] = (jnp.sqrt(dy ** 2 + dx ** 2) * same).sum() / jnp.maximum(same.sum(), 1) / L
    res["survive"] = same.sum() / jnp.maximum(p[:-L].sum(), 1)        # slot-ticks whose body is there L ticks on
    res["age_mean"] = (tb[..., _AGE] * p).sum() / npres
    res["glob"] = o["glob"].mean(0)                                   # per tracked member over T ticks
    res["ovf"] = o["ovf"].max(0)
    res["thumb"] = o["x_end"][0].astype(jnp.float32)
    return res


def make_chunk_fn(wd: WorldDef, sz: Sizes, map_batch: int = 16):
    """A jitted function (thetas, thetas2, keys) -> measures for a chunk of draws (leading axis D).
    Simulation is vmapped over the draws; the measures run draw by draw in sub-batches (lax.map)."""

    def chunk(ths, ths2, keys):
        o = jax.vmap(lambda th, th2, k: simulate_one(wd, sz, th, th2, k))(ths, ths2, keys)
        extra = {}
        if sz.frame_every:
            extra["frames"] = o.pop("x0")
            extra["tab"] = o["tab"][:, ::sz.frame_every, 0]           # member 0 at the frame ticks
        res = lax.map(lambda oo: measure_one(wd, sz, oo), o, batch_size=map_batch)
        res.update(extra)
        return res
    return jax.jit(chunk)


def to_host(res) -> dict:
    """Device results -> numpy (float32 for floats)."""
    out = {}
    for k, v in res.items():
        a = np.asarray(v)
        out[k] = a.astype(np.float32) if a.dtype.kind == "f" else a
    return out


def quantise(x, q: float = 99.9):
    """float (..., C, H, W) -> uint8 with one scale per leading index 0 (the draw)."""
    x = np.asarray(x, np.float32)
    sc = np.percentile(x.reshape(x.shape[0], -1), q, axis=1) + 1e-30
    u = np.clip(x / sc.reshape((-1,) + (1,) * (x.ndim - 1)) * 255.0, 0, 255).astype(np.uint8)
    return u, sc.astype(np.float32)


# ----------------------------------------------------------------------------- the gliders world, same measures
def gliders_world(G: int = 8) -> tuple:
    """(WorldDef, params) of the Flow-Lenia gliders world of vw1/port (tick = 20 substeps, noise 0.5, no
    input), with its own block view (G x G blocks of 16 px) and its own tracker settings."""
    port = os.path.join(TN.VW1, "port")
    if port not in sys.path:
        sys.path.insert(0, port)
    import _paths  # noqa: F401
    import flowlenia_jax as FJ
    import phi as PH
    lev0, cfg, meta = FJ.make_level("A_gliders", 0.5)
    _, trv, _ = PH.phi_objects_jax("A_gliders")
    shape = (cfg.C, cfg.H, cfg.W)

    def tick(p, A, nz):
        fK = FJ.kernel_fft(cfg, p)

        def body(A, i):
            xi = nz.substep(20, i).normal((2,) + shape)
            return FJ.substep(cfg, p, A, xi, 0.5, fK), None
        A, _ = lax.scan(body, A, jnp.arange(20))
        return A
    wd = WorldDef(name="gliders", shape=shape, init=lambda p, k: lev0.init(p, k), tick=tick,
                  view=lambda x: TN.block_view(x, G), trk=trv.bt, trk_field=lambda x: x)
    return wd, lev0.params
