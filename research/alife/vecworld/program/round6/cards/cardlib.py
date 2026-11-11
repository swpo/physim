"""cardlib -- WORLD CARDS (round 6, study cards): one tool, the same card for every world.

A world enters through a thin `Adapter` (adapters.py): init and tick with the hidden part `th` as an ARGUMENT,
the input channel (dimension, noise std, how to aim), two memoryless field views (a G x G block view and the
same view at half the block size), a vw.objects.BlobTracker with the field it reads, and a rule that moves the
hidden part by a fraction eps of its declared prior. Nothing here knows which world it is.

SIMULATION (JAX; one compiled program per adapter, hidden parts and data are arguments)
  main     M members: init, `burn` free ticks (a traced integer, so the late window reuses the program), the
           tracker started, then T recorded ticks. Per tick and member: block view g (Q, G, G), fine view f
           (Q, 2G, 2G), the tracker's slot table (K x 11) and counters, the share of matter relocated.
  tests    the last M - M_fit members at n_snap snapshot ticks: NS test states (level-0 state + tracker memory).
  branch   from each test state, HB ticks of `Bb` arms that differ in (hidden part, noise key, input):
             rep   R replicas, fresh independent noise                     -> oracle, noise twins
             nb    for each eps in sz.eps and direction d < n_dir: R2 replicas under a neighbour of the hidden
                   part at distance eps of the prior, on the noise of rep 0 .. R2 - 1 -> the hidden part's weight
             act   for each (kind, nats) in sz.arms: R_u replicas with the noise keys of rep 0..R_u-1 and an
                   input of `nats` nats spread over the first T_in ticks; kind 'aimed' puts it where the
                   matter is (adapter.aim), 'blind' on as many random coordinates -> paired displacement

ANALYSIS (numpy, from the small records; runs on the pod and again here)
  Three kinds of level, each with ONE fixed cheap predictor family fitted in closed form on the fit members:
    grid     the block view: local translation-equivariant ridge, 3 x 3 blocks x Q channels x 2 lags (the
             foundry screen's predictor)
    bodies   the tracker's slot list read as per-body increments (wrapped displacement, log-mass change over
             h ticks of a body that keeps its identity): ridge on the body's own last displacement, mass, size
             and kind share (a single-body law); a second fit adds the block view around the body
    pop      a population vector of the slot list (count, tracked mass, mean speed, sd and max of body mass,
             kind share): global ridge on 2 lags; a quadratic variant; the kind-share law of the fed-vortex
             world, ds = b1 s (1 - s) + b2 (1 - 2 s), fitted for every world
  For every level and horizon h in 1, 2, 4, 8, 16, 32 ticks, in units of the level's climatological variance:
    V_clim, V_pers, V_pred (cheap family), V_orc (replica variance);
    predictable fraction PF = 1 - V_orc / V_clim; closure ceiling c = (V_clim - min(V_pred, V_clim)) /
    (V_clim - V_orc); closure gap = min(V_pred, V_clim) - V_orc.
  Stationarity: the share of a level's variance that is a function of the tick alone, estimated without bias
  as the covariance over ticks of the member-means of two disjoint halves of the fit members.
  Hidden part: plug-in loss PL(eps, h) = |mean_theta' - mean_theta|^2, estimated without bias from paired
  differences under common noise, |mean d|^2 - var(d) / R2 (round 5's unpaired form is kept as pl_unpaired; the
  check on a closed-form world shows it cannot resolve a loss below about 0.01 of the variance), and its ratio
  to V_orc. Actions: paired displacement D = |y_u - y_0|^2 with common noise, its
  predictable part MS = |mean d|^2 - var(d) / R_u, both against the twin floor 2 V_orc.
  Learned variable: time-lagged slow features of the 2 x 2 fine sub-blocks (a linear family that contains the
  hand block view), learned on one half of the fit members and compared with the hand view on the other half
  by the same predictor.
"""
from __future__ import annotations

import os
import sys
import time
from dataclasses import dataclass, field
from typing import Any, Callable

sys.dont_write_bytecode = True
HERE = os.path.dirname(os.path.abspath(__file__))
VEC = os.path.abspath(os.path.join(HERE, "..", "..", ".."))           # research/alife/vecworld
VW1 = os.path.join(VEC, "vw1")
if VW1 not in sys.path:
    sys.path.insert(0, VW1)

import jax  # noqa: E402
import jax.numpy as jnp  # noqa: E402
import numpy as np  # noqa: E402
from jax import lax  # noqa: E402

import vw  # noqa: E402  (enables float64)
from vw.core import Noise  # noqa: E402

HZ = (1, 2, 4, 8, 16, 32)
TABCOLS = (0, 1, 2, 7, 10, 11, 12, 13, 14, 15, 16)   # of the tracker's slot table (vw.objects)
P_, MS_, FR_, RG_, VX_, VY_, CY_, CX_, AGE_, EV_, UID_ = range(11)
POP_NAMES = ("count", "tracked_mass", "mean_speed", "mass_sd", "mass_max", "kind_share")
_K_INIT, _K_DYN, _K_REP, _K_NB = 1, 3, 100, 200
MAX_ELEMS = 2 ** 30                                  # size guard: no array above this many elements
QUIET_DLOGM = float(np.log(1.5))                     # a body's step is "quiet" if it keeps its identity, has no tracker
#                                                      event at either end and its mass changes by less than x 1.5


@dataclass(frozen=True)
class Sizes:
    M: int = 16
    M_fit: int = 8
    T: int = 400
    n_snap: int = 4
    R: int = 6
    R2: int = 2
    n_dir: int = 2
    eps: tuple = (0.03, 0.1, 1.0)
    arms: tuple = (("aimed", 200.0), ("blind", 200.0), ("aimed", 50.0), ("aimed", 800.0))
    R_u: int = 2
    x_eps: float = 1.0            # the response-difference arms: hidden part moved by x_eps (direction 0), ...
    x_arm: tuple = ("aimed", 200.0)   # ... run without input and with this input, on the noise of rep 0 .. R_u - 1
    T_in: int = 4
    HB: int = 32
    ridge: float = 1e-4
    n_boot: int = 200

    @property
    def M_test(self) -> int:
        return self.M - self.M_fit

    @property
    def NS(self) -> int:
        return self.M_test * self.n_snap

    @property
    def Bb(self) -> int:
        return self.R + len(self.eps) * self.n_dir * self.R2 + len(self.arms) * self.R_u + 2 * self.R_u

    @property
    def hz(self) -> tuple:
        return tuple(h for h in HZ if h <= self.HB)

    def layout(self) -> dict:
        """Arm indices of the branch batch."""
        i = self.R
        nb = {}
        for e in self.eps:
            for d in range(self.n_dir):
                nb[(e, d)] = list(range(i, i + self.R2))
                i += self.R2
        act = {}
        for a in self.arms:
            act[a] = list(range(i, i + self.R_u))
            i += self.R_u
        xb = list(range(i, i + self.R_u))
        xa = list(range(i + self.R_u, i + 2 * self.R_u))
        i += 2 * self.R_u
        assert i == self.Bb
        return {"rep": list(range(self.R)), "nb": nb, "act": act, "xb": xb, "xa": xa}

    def member_ticks(self, burn: int) -> int:
        return self.M * (burn + self.T) + self.NS * self.Bb * self.HB


@dataclass(frozen=True, eq=False)
class Adapter:
    name: str
    family: str
    init: Callable                # (th, key) -> x (pytree)
    tick: Callable                # (th, x, Noise, u (m,)) -> x
    m: int                        # input dimension
    sigma_u: float                # input noise std: an input u costs |u|^2 / (2 sigma_u^2) nats per tick
    grid: Callable                # x -> (Q, G, G)
    fine: Callable                # x -> (Q, 2G, 2G)
    trk: Any                      # vw.objects.BlobTracker
    trk_field: Callable           # x -> (C, H, W) the field the tracker reads (also the matter for distances)
    theta0: Any                   # the hidden part (pytree of numpy arrays)
    neighbour: Callable           # (theta, eps, d) -> theta' (numpy), a move of eps of the declared prior
    aim: Callable                 # (field (C, H, W) numpy, rng, aimed: bool) -> unit pattern (m,)
    G: int = 8
    Hpx: int = 64
    burn: int = 50
    late_gap: int = 1000
    state_batch: int = 8
    grid_names: tuple = ()
    meta: dict = field(default_factory=dict)


def dev(tree):
    return jax.tree_util.tree_map(lambda a: jnp.asarray(a), tree)


def stack_trees(trees):
    return jax.tree_util.tree_map(lambda *v: jnp.stack([jnp.asarray(a) for a in v]), *trees)


def check_elems(*shapes):
    for s in shapes:
        n = int(np.prod(s))
        if n > MAX_ELEMS:
            raise MemoryError(f"array of shape {s} has {n} elements > {MAX_ELEMS}")


# ----------------------------------------------------------------------------- simulation
def make_fns(ad: Adapter, sz: Sizes):
    """(main, branch): jitted functions; every array is an argument."""
    bt = ad.trk
    fold = jax.random.fold_in
    tabcols = jnp.array(TABCOLS)
    f32 = jnp.float32
    R = sz.R
    vfield = jax.vmap(ad.trk_field)

    def rec_one(x, m):
        d = bt.split(m)
        return dict(g=ad.grid(x).astype(f32), tab=d["table"][:, tabcols].astype(f32), glob=d["globals"].astype(f32))

    def upd(m, x):
        return jax.vmap(lambda mm, xx: bt.update_memory(mm, ad.trk_field(xx)))(m, x)

    def main(th, keys, burn):
        M = keys.shape[0]
        x = jax.vmap(lambda k: ad.init(th, fold(k, _K_INIT)))(keys)
        kd = jax.vmap(lambda k: fold(k, _K_DYN))(keys)
        z = jnp.zeros((ad.m,))

        def step(x, t):
            return jax.vmap(lambda xx, kk: ad.tick(th, xx, Noise(kk, t), z))(x, kd)
        x = lax.fori_loop(0, burn, lambda t, xx: step(xx, t), x)
        m = jax.vmap(lambda xx: bt.init_memory(ad.trk_field(xx)))(x)

        def body(c, t):
            x, m = c
            xn = step(x, t)
            mn = upd(m, xn)
            r = jax.vmap(rec_one)(xn, mn)
            r["f"] = jax.vmap(ad.fine)(xn).astype(f32)
            F0, F1 = vfield(x), vfield(xn)
            r["moved"] = (0.5 * jnp.abs(F1 - F0).sum((1, 2, 3)) / jnp.maximum(jnp.abs(F0).sum((1, 2, 3)), 1e-300)).astype(f32)
            r["fsum"] = F1.sum((1, 2, 3)).astype(f32)
            return (xn, mn), r
        seg = sz.T // sz.n_snap
        r0 = jax.vmap(rec_one)(x, m)
        r0["f"] = jax.vmap(ad.fine)(x).astype(f32)
        recs, sx, sm = [], [], []
        for s in range(sz.n_snap):
            (x, m), r = lax.scan(body, (x, m), burn + jnp.arange(s * seg, (s + 1) * seg))
            recs.append(r)
            sx.append(jax.tree_util.tree_map(lambda a: a[sz.M_fit:], x))
            sm.append(m[sz.M_fit:])
        out = {k: jnp.concatenate([r[k] for r in recs], 0) for k in recs[0]}
        for k in ("g", "tab", "glob", "f"):
            out[k] = jnp.concatenate([r0[k][None], out[k]], 0)                 # (T + 1, M, ...)
        xs = jax.tree_util.tree_map(lambda *a: jnp.concatenate(a, 0), *sx)     # (NS, ...): snapshot-major
        ms = jnp.concatenate(sm, 0)
        Fe = vfield(x)
        out["field_end"] = Fe.astype(f32)
        out["snap_field"] = vfield(xs).astype(f32)
        out["ovf"] = jax.vmap(lambda mm: bt.split(mm)["overflow"])(m).astype(f32)
        out["finite"] = jnp.isfinite(Fe).all() & jnp.isfinite(out["g"]).all()
        t0 = jnp.repeat(burn + (jnp.arange(sz.n_snap) + 1) * seg, sz.M_test)
        return out, xs, ms, t0

    def branch(th_arms, xs, ms, keys, U, t0):
        Bb = keys.shape[1]

        def one_state(args):
            x, m, k, u, t00 = args
            xa = jax.tree_util.tree_map(lambda a: jnp.broadcast_to(a, (Bb,) + a.shape), x)
            ma = jnp.broadcast_to(m, (Bb,) + m.shape)

            def body(c, i):
                xa, ma = c
                xn = jax.vmap(lambda th, xx, kk, uu: ad.tick(th, xx, Noise(kk, t00 + i), uu))(th_arms, xa, k, u[:, i])
                mn = upd(ma, xn)
                r = jax.vmap(rec_one)(xn, mn)
                r["f"] = jax.vmap(ad.fine)(jax.tree_util.tree_map(lambda a: a[:R], xn)).astype(f32)
                F = vfield(xn)
                r["l1"] = (0.5 * jnp.abs(F - F[:1]).sum((1, 2, 3)) / jnp.maximum(jnp.abs(F[0]).sum(), 1e-300)).astype(f32)
                return (xn, mn), r
            _, r = lax.scan(body, (xa, ma), jnp.arange(sz.HB))
            return r
        return lax.map(one_state, (xs, ms, keys, U, t0), batch_size=ad.state_batch)

    return jax.jit(main), jax.jit(branch)


def build_inputs(ad: Adapter, sz: Sizes, snap_field: np.ndarray, seed: int) -> np.ndarray:
    """U (NS, Bb, HB, m): zero except the action arms. An arm of N nats: unit pattern p (aimed or blind),
    u_t = a p for the first T_in ticks with T_in * a^2 / (2 sigma_u^2) = N."""
    lay = sz.layout()
    U = np.zeros((sz.NS, sz.Bb, sz.HB, ad.m))
    for s in range(sz.NS):
        rng = np.random.default_rng([int(seed), 77, s])
        pat = {True: ad.aim(snap_field[s], rng, True), False: ad.aim(snap_field[s], rng, False)}
        for (kind, nats), idx in lay["act"].items():
            p = pat[kind == "aimed"]
            a = np.sqrt(2.0 * nats / sz.T_in) * ad.sigma_u
            U[s, idx, :sz.T_in, :] = a * p[None, None, :]
            if (kind, nats) == tuple(sz.x_arm):
                U[s, lay["xa"], :sz.T_in, :] = a * p[None, None, :]
    return U


def run_world(ad: Adapter, sz: Sizes, fns, theta, seed: int, burn: int, log=None) -> dict:
    """Simulate one world once (one window). Returns host records (numpy) and timings."""
    main, branch = fns
    lay = sz.layout()
    Q = len(ad.grid_names)
    check_elems((sz.NS, sz.HB, sz.Bb, Q, ad.G, ad.G), (sz.NS, sz.HB, sz.R, Q, 2 * ad.G, 2 * ad.G),
                (sz.T + 1, sz.M, Q, 2 * ad.G, 2 * ad.G), (sz.NS, sz.HB, sz.Bb, ad.trk.K, len(TABCOLS)),
                (ad.state_batch, sz.Bb) + tuple(ad.trk.shape))
    base = jax.random.fold_in(jax.random.key(int(seed)), 0)
    keys = jax.vmap(lambda i: jax.random.fold_in(base, i))(jnp.arange(sz.M))
    t1 = time.time()
    out, xs, ms, t0 = main(dev(theta), keys, jnp.asarray(int(burn)))
    out = {k: np.asarray(v) for k, v in out.items()}
    t2 = time.time()
    ths = [theta] * sz.R
    for e in sz.eps:
        for d in range(sz.n_dir):
            ths += [ad.neighbour(theta, e, d)] * sz.R2
    ths += [theta] * (len(sz.arms) * sz.R_u)
    ths += [ad.neighbour(theta, sz.x_eps, 0)] * (2 * sz.R_u)
    th_arms = stack_trees(ths)
    kb = jax.random.fold_in(jax.random.key(int(seed)), 1)
    kid = np.zeros((sz.Bb,), np.int64)
    kid[lay["rep"]] = _K_REP + np.arange(sz.R)
    for idx in lay["nb"].values():
        kid[idx] = _K_REP + np.arange(sz.R2)                      # common noise: the noise of replicas 0 .. R2 - 1
    for idx in list(lay["act"].values()) + [lay["xb"], lay["xa"]]:
        kid[idx] = _K_REP + np.arange(sz.R_u)                     # the noise of replicas 0 .. R_u - 1
    kidj = jnp.asarray(kid, jnp.uint32)
    kk = jax.vmap(lambda s: jax.vmap(lambda a: jax.random.fold_in(jax.random.fold_in(kb, a), s))(kidj))(jnp.arange(sz.NS))
    U = build_inputs(ad, sz, out["snap_field"], seed)
    t3 = time.time()
    b = branch(th_arms, xs, ms, kk, jnp.asarray(U), t0)
    b = {k: np.asarray(v) for k, v in b.items()}                  # (NS, HB, Bb | R, ...)
    t4 = time.time()
    rec = dict(out)
    rec.update({"b_" + k: v for k, v in b.items()})
    rec["t0"] = np.asarray(t0)
    rec["U_norm2"] = (U ** 2).sum((2, 3))                         # (NS, Bb): sum over ticks of |u|^2
    rec["timing"] = dict(main_s=t2 - t1, branch_s=t4 - t3, burn=int(burn),
                         main_member_ticks=sz.M * (int(burn) + sz.T), branch_member_ticks=sz.NS * sz.Bb * sz.HB)
    if log:
        log(f"{ad.name}: main {t2 - t1:.1f}s branch {t4 - t3:.1f}s, {sz.member_ticks(burn)} member-ticks")
    return rec


# ----------------------------------------------------------------------------- analysis helpers (numpy)
def _nb3(z):
    return np.concatenate([np.roll(z, (dy, dx), (-2, -1)) for dy in (-1, 0, 1) for dx in (-1, 0, 1)], -3)


def _rows(a):
    """(..., F, G, G) -> (n, F)."""
    return np.moveaxis(a, -3, -1).reshape(-1, a.shape[-3])


def _ridge(X, Ys, lam):
    n, nf = X.shape
    A = X.T @ X + lam * n * np.eye(nf)
    return [np.linalg.solve(A, X.T @ Y) for Y in Ys]


def _boot(rng, n, nb):
    return rng.integers(0, n, size=(nb, n))


def _ratios(vc, vo, vp, vs):
    """Card ratios from the four variances. The cheap family is {climatology, persistence, the ridge}: its error
    is the smallest of the three (ceil_raw: the ridge or climatology only, round 5's definition)."""
    vch = np.minimum(np.minimum(vp, vs), vc)
    den = vc - vo
    den = np.where(np.abs(den) > 1e-12, den, np.nan)
    return dict(pf=1.0 - vo / np.maximum(vc, 1e-300), ceil=(vc - vch) / den, ceil_raw=(vc - np.minimum(vp, vc)) / den,
                ceil_pers=(vc - np.minimum(vs, vc)) / den, gap=vch - vo)


def _summ(per_state: dict, rng, nb):
    """Means over test states, the ratios of the means, the same from the MEDIANS over test states (suffix
    _med: the typical state; the means can be carried by a few states far from the climatology), and bootstrap
    standard errors over test states. per_state: name -> (nh, n_states)."""
    KS = ("v_clim", "v_orc", "v_pred", "v_pers")
    m = {k: np.nanmean(per_state[k], 1) for k in KS}
    md = {k: np.nanmedian(per_state[k], 1) for k in KS}
    out = {k: v.tolist() for k, v in m.items()}
    out.update({k + "_med": v.tolist() for k, v in md.items()})
    out.update({k: v.tolist() for k, v in _ratios(*(m[k] for k in KS)).items()})
    out.update({k + "_med": v.tolist() for k, v in _ratios(*(md[k] for k in KS)).items()})
    NS = per_state["v_clim"].shape[1]
    if NS > 2 and nb > 0:
        idx = _boot(rng, NS, nb)
        res = {k: per_state[k][:, idx] for k in KS}                           # (nh, nb, NS)
        sb = _ratios(*(np.nanmean(res[k], 2) for k in KS))
        sm = _ratios(*(np.nanmedian(res[k], 2) for k in KS))
        for k, v in sb.items():
            out[k + "_se"] = np.nanstd(v, 1).tolist()
        for k, v in sm.items():
            out[k + "_med_se"] = np.nanstd(v, 1).tolist()
        for k in ("v_orc", "v_pred", "v_clim"):
            out[k + "_se"] = np.nanmean(res[k], 2).std(1).tolist()
    return out


def _tick_share(zf):
    """zf (T + 1, Mf, ...) standardised: share of the variance carried by a function of the tick alone, as the
    covariance over ticks of the means of two disjoint member halves (unbiased for the common tick function)."""
    Mf = zf.shape[1]
    if Mf < 2:
        return float("nan")
    ax = tuple(range(1, zf.ndim))
    a = zf[:, 0::2].mean(ax)
    b = zf[:, 1::2].mean(ax)
    tot = zf.var()
    return float(np.mean((a - a.mean()) * (b - b.mean())) / max(tot, 1e-300))


def _member_share(zm):
    """zm (T + 1, M, d) standardised level means per member: the share of the variance of the member-and-tick
    series that lies between the time-means of the members (members stuck in different regimes; for an ergodic
    level about 2 x correlation time / T)."""
    tot = zm.var((0, 1))
    return float(zm.mean(0).var(0).sum() / max(tot.sum(), 1e-12))


def _pl(zh, idx, R, R2, ax):
    """Plug-in loss per state, two unbiased estimators of |mean_theta' - mean_theta|^2 averaged over the level.
    zh (NS, Bb, ...): arms idx hold R2 replicas under theta' driven by the noise of replicas 0 .. R2 - 1.
    paired    d_r = y'_r - y_r (common noise): |mean_r d|^2 - var_r(d) / R2
    unpaired  round 5's form on independent noise: theta' arms against replicas R2 .. R - 1:
              |m' - m|^2 - V' / R2 - V / (R - R2)"""
    zb = zh[:, idx]
    d = zb - zh[:, :R2]
    paired = (d.mean(1) ** 2).mean(ax) - d.var(1, ddof=1).mean(ax) / R2
    zi = zh[:, R2:R]
    unp = ((zi.mean(1) - zb.mean(1)) ** 2).mean(ax) - zb.var(1, ddof=1).mean(ax) / R2 - zi.var(1, ddof=1).mean(ax) / (R - R2)
    return paired, unp


def _act(zu, z0, ax):
    """Paired displacement and its predictable part per state. zu, z0 (NS, R_u, ...)."""
    d = zu - z0
    Ru = d.shape[1]
    D = (d ** 2).mean(1).mean(ax)
    ms = (d.mean(1) ** 2).mean(ax) - ((d.var(1, ddof=1).mean(ax) / Ru) if Ru > 1 else 0.0)
    return D, ms


def _hidden_and_actions(za_h, v_orc_s, sz: Sizes, lay, ax, rng):
    """za_h: list over horizons of (NS, Bb, ...) standardised branch values. -> dict of lists over horizons."""
    out = {"pl": {}, "act": {}}
    R = sz.R
    for e in sz.eps:
        rows, rows_u = [], []
        for i, zh in enumerate(za_h):
            both = [_pl(zh, lay["nb"][(e, d)], R, sz.R2, ax) for d in range(sz.n_dir)]
            rows.append(np.mean([b[0] for b in both], 0))
            rows_u.append(np.mean([b[1] for b in both], 0))
        rows, rows_u = np.asarray(rows), np.asarray(rows_u)                   # (nh, NS)
        vo = np.asarray(v_orc_s).mean(1)
        vom = np.median(np.asarray(v_orc_s), 1)
        out["pl"][str(e)] = dict(pl=rows.mean(1).tolist(), pl_se=(rows.std(1) / np.sqrt(rows.shape[1])).tolist(),
                                 pl_over_vorc=(rows.mean(1) / np.maximum(vo, 1e-12)).tolist(),
                                 pl_unpaired=rows_u.mean(1).tolist(),
                                 pl_unpaired_se=(rows_u.std(1) / np.sqrt(rows_u.shape[1])).tolist(),
                                 pl_unpaired_over_vorc=(rows_u.mean(1) / np.maximum(vo, 1e-12)).tolist(),
                                 pl_med=np.median(rows, 1).tolist(),
                                 pl_over_vorc_med=(np.median(rows, 1) / np.maximum(vom, 1e-12)).tolist())
    for (kind, nats), idx in lay["act"].items():
        Ds, Ms = [], []
        for zh in za_h:
            D, ms = _act(zh[:, idx], zh[:, :sz.R_u], ax)
            Ds.append(D)
            Ms.append(ms)
        Ds, Ms = np.asarray(Ds), np.asarray(Ms)
        vo = np.asarray(v_orc_s).mean(1)
        out["act"][f"{kind}_{int(nats)}"] = dict(
            D=Ds.mean(1).tolist(), D_se=(Ds.std(1) / np.sqrt(Ds.shape[1])).tolist(),
            MS=Ms.mean(1).tolist(), MS_se=(Ms.std(1) / np.sqrt(Ms.shape[1])).tolist(),
            D_over_floor=(Ds.mean(1) / np.maximum(2.0 * vo, 1e-12)).tolist(),
            MS_over_vorc=(Ms.mean(1) / np.maximum(vo, 1e-12)).tolist(),
            D_med=np.median(Ds, 1).tolist(), MS_med=np.median(Ms, 1).tolist(),
            MS_over_vorc_med=(np.median(Ms, 1) / np.maximum(np.median(np.asarray(v_orc_s), 1), 1e-12)).tolist())
    # does the response to the input depend on the hidden part? d = response under theta, d' under theta' (same
    # noise, same input); RD = |mean d' - mean d|^2 - (var d + var d') / R_u; and the paired displacement of the
    # hidden-part move itself with common noise
    Ru = sz.R_u
    ia = lay["act"][tuple(sz.x_arm)]
    RDs, PPs, MSs = [], [], []
    for zh in za_h:
        d = zh[:, ia] - zh[:, :Ru]
        d2 = zh[:, lay["xa"]] - zh[:, lay["xb"]]
        corr = ((d.var(1, ddof=1) + d2.var(1, ddof=1)).mean(ax) / Ru) if Ru > 1 else 0.0
        RDs.append(((d2.mean(1) - d.mean(1)) ** 2).mean(ax) - corr)
        PPs.append(((zh[:, lay["xb"]] - zh[:, :Ru]) ** 2).mean(1).mean(ax))
        MSs.append((d.mean(1) ** 2).mean(ax) - ((d.var(1, ddof=1).mean(ax) / Ru) if Ru > 1 else 0.0))
    RDs, PPs, MSs = np.asarray(RDs), np.asarray(PPs), np.asarray(MSs)
    vo = np.asarray(v_orc_s).mean(1)
    out["xresp"] = dict(eps=sz.x_eps, arm=list(sz.x_arm), RD=RDs.mean(1).tolist(),
                        RD_se=(RDs.std(1) / np.sqrt(RDs.shape[1])).tolist(),
                        RD_over_vorc=(RDs.mean(1) / np.maximum(vo, 1e-12)).tolist(),
                        RD_over_vorc_med=(np.median(RDs, 1) / np.maximum(np.median(np.asarray(v_orc_s), 1), 1e-12)).tolist(),
                        RD_over_MS=(RDs.mean(1) / np.where(np.abs(MSs.mean(1)) > 1e-12, MSs.mean(1), np.nan)).tolist(),
                        paired_theta_D=PPs.mean(1).tolist(),
                        paired_theta_D_over_floor=(PPs.mean(1) / np.maximum(2.0 * vo, 1e-12)).tolist())
    return out


# ----------------------------------------------------------------------------- grid level
def grid_card(Y, YA, sz: Sizes, ts, fit_idx, with_arms=True, extra=None, extra_test=None, seed=0, detail=True):
    """Y (T + 1, M, Q, G, G) main run; YA (NS, HB, B', Q, G, G) branches (the first R arms are the replicas).
    fit_idx: members used for standardisation and the ridge. extra (T + 1, M, E, G, G), extra_test: optional
    additional features at time t (cross-level test). Returns the level's card entries."""
    rng = np.random.default_rng([seed, 11])
    T, M = Y.shape[0] - 1, Y.shape[1]
    Q, G = Y.shape[2], Y.shape[-1]
    hz, R, lay = sz.hz, sz.R, sz.layout()
    Y = Y.astype(np.float64)
    yf = Y[:, fit_idx]
    mu = yf.mean((0, 1, 3, 4))
    sd = yf.std((0, 1, 3, 4))
    sdc = np.maximum(sd, 1e-12 * np.maximum(np.abs(mu), 1e-300))
    live = sd > 1e-9 * np.maximum(np.abs(mu), 1e-12)                          # channels that vary at all
    sh = (None, None, slice(None), None, None)
    z = (Y - mu[sh]) / sdc[sh]
    za = (YA.astype(np.float64) - mu[(None, None, None, slice(None), None, None)]) / sdc[(None, None, None, slice(None), None, None)]
    hmax = max(hz)
    nt = T - hmax
    feat = np.concatenate([_nb3(z[1:]), _nb3(z[:-1])], 2)                     # (T, M, 18 Q, G, G): t = 1 .. T
    if extra is not None:
        feat = np.concatenate([feat, extra[1:]], 2)
    Xf = _rows(feat[:nt, fit_idx])
    Xf = np.concatenate([Xf, np.ones((Xf.shape[0], 1))], 1)
    Wt = _ridge(Xf, [_rows(z[1 + h:1 + h + nt, fit_idx]) for h in hz], sz.ridge)
    fit_mse = [float(np.mean((Xf @ W - _rows(z[1 + h:1 + h + nt, fit_idx])) ** 2)) for W, h in zip(Wt, hz)]
    del Xf
    test_idx = np.arange(sz.M_fit, M)
    zs = np.concatenate([z[t, test_idx] for t in ts], 0)                      # (NS, Q, G, G), snapshot-major
    fs = np.concatenate([feat[t - 1, test_idx] for t in ts], 0)
    NS = zs.shape[0]
    Xs = np.concatenate([np.moveaxis(fs, 1, -1), np.ones((NS, G, G, 1))], -1)
    ax = (1, 2, 3)
    per = {k: [] for k in ("v_clim", "v_pers", "v_pred", "v_orc")}
    za_h, ex_cells = [], {}
    q_orc, q_pred, q_clim = [], [], []
    for i, h in enumerate(hz):
        zh = za[:, h - 1]                                                     # (NS, B', Q, G, G)
        zr = zh[:, :R]
        pred = np.moveaxis(Xs @ Wt[i], -1, 1)                                 # (NS, Q, G, G)
        vo_cell = zr.var(1, ddof=1)                                           # (NS, Q, G, G)
        ep_cell = ((zr - pred[:, None]) ** 2).mean(1)
        per["v_clim"].append((zr ** 2).mean((1, 2, 3, 4)))
        per["v_pers"].append(((zr - zs[:, None]) ** 2).mean((1, 2, 3, 4)))
        per["v_pred"].append(ep_cell.mean(ax))
        per["v_orc"].append(vo_cell.mean(ax))
        q_orc.append(vo_cell.mean((0, 2, 3)))
        q_pred.append(ep_cell.mean((0, 2, 3)))
        q_clim.append((zr ** 2).mean((0, 1, 3, 4)))
        za_h.append(zh)
        if h in (4, 8):
            ex = np.maximum((ep_cell - vo_cell).mean(1), 0.0).ravel()        # excess per (state, block)
            srt = np.sort(ex)[::-1]
            k = max(1, len(srt) // 10)
            ex_cells[h] = float(srt[:k].sum() / max(srt.sum(), 1e-300))
    per = {k: np.asarray(v) for k, v in per.items()}
    out = _summ(per, rng, sz.n_boot)
    out.update(hz=list(hz), fit_mse=fit_mse, mean=mu.tolist(), std=sd.tolist(), live=live.tolist(),
               v_orc_q=np.asarray(q_orc).tolist(), v_pred_q=np.asarray(q_pred).tolist(),
               v_clim_q=np.asarray(q_clim).tolist(), n_fit_rows=int(nt * len(fit_idx) * G * G), n_test=int(NS))
    out["excess_top10pct_share"] = {str(k): v for k, v in ex_cells.items()}
    if detail:
        zf = z[:, fit_idx]
        out["tick_share"] = _tick_share(zf)
        out["tick_share_q"] = [_tick_share(zf[:, :, q]) for q in range(Q)]
        out["member_share"] = _member_share(np.moveaxis(z, 2, -1).reshape(T + 1, M, -1, Q).mean(2))
        out["d"] = int(live.sum() * G * G)
        out["var_static"] = float(np.mean(zf.mean(0) ** 2))
        out["autocorr"] = [float(np.mean(zf[h:] * zf[:-h])) for h in hz]
        out["vp_main"] = [float(np.mean((zf[h:] - zf[:-h]) ** 2)) for h in hz]
        out["block_corr1"] = float(0.5 * (np.mean(zf * np.roll(zf, 1, -1)) + np.mean(zf * np.roll(zf, 1, -2))))
        T3 = (T + 1) // 3
        a, b = zf[:T3], zf[-T3:]
        out["within_window"] = dict(d_mean=(b.mean((0, 1, 3, 4)) - a.mean((0, 1, 3, 4))).tolist(),
                                    log_sd_ratio=np.log(np.maximum(b.std((0, 1, 3, 4)), 1e-12)
                                                        / np.maximum(a.std((0, 1, 3, 4)), 1e-12)).tolist())
    if with_arms:
        out.update(_hidden_and_actions(za_h, per["v_orc"], sz, lay, ax, rng))
    out["_per_state"] = {k: v.astype(np.float32) for k, v in per.items()}
    return out


# ----------------------------------------------------------------------------- slow features of the fine view
def slow_features(F, fit_idx, Q, G, tau=8):
    """Time-lagged slow features of the 2 x 2 sub-block patches. F (T + 1, M, Q, 2G, 2G) -> (W (4Q, Q), mu, sd,
    eigenvalues): the Q linear combinations of a block's 4Q sub-block means with the largest symmetrised
    lag-tau autocorrelation (TICA), unit variance on the fit members."""
    P = patches(F, Q, G)                                                      # (T + 1, M, G, G, 4Q)
    X = P[:, fit_idx].astype(np.float64)
    mu = X.mean((0, 1, 2, 3))
    sd = np.maximum(X.std((0, 1, 2, 3)), 1e-12)
    Xz = (X - mu) / sd
    a = Xz[:-tau].reshape(-1, 4 * Q)
    b = Xz[tau:].reshape(-1, 4 * Q)
    n = a.shape[0]
    C0 = (a.T @ a + b.T @ b) / (2 * n)
    Ct = (a.T @ b + b.T @ a) / (2 * n)
    w, V = np.linalg.eigh(C0)
    keep = w > 1e-8 * w.max()
    Wh = V[:, keep] / np.sqrt(w[keep])
    lam, U = np.linalg.eigh(Wh.T @ Ct @ Wh)
    order = np.argsort(lam)[::-1][:Q]
    return Wh @ U[:, order], mu, sd, lam[order]


def patches(F, Q, G):
    """(..., Q, 2G, 2G) -> (..., G, G, 4Q)."""
    lead = F.shape[:-3]
    X = F.reshape(lead + (Q, G, 2, G, 2))
    X = np.moveaxis(X, (-5, -3, -1), (-3, -2, -1))                            # (..., G, G, Q, 2, 2)
    return X.reshape(lead + (G, G, 4 * Q))


def apply_features(F, W, mu, sd, Q, G):
    """Fine view -> learned block variable (..., Q, G, G)."""
    P = (patches(F, Q, G).astype(np.float64) - mu) / sd
    return np.moveaxis(P @ W, -1, -3)


# ----------------------------------------------------------------------------- bodies and population
def _mi(d, L):
    return d - L * np.round(d / L)


def pop_vector(tab):
    """(..., K, 11) slot tables -> (..., 6) population vector (POP_NAMES)."""
    p = tab[..., P_] > 0.5
    n = p.sum(-1).astype(np.float64)
    mass = np.where(p, tab[..., MS_], 0.0).astype(np.float64)
    nn = np.maximum(n, 1.0)
    mm = mass.sum(-1) / nn
    spd = (np.sqrt(tab[..., VX_].astype(np.float64) ** 2 + tab[..., VY_] ** 2) * p).sum(-1) / nn
    msd = np.sqrt(np.maximum((np.where(p, (mass - mm[..., None]) ** 2, 0.0)).sum(-1) / nn, 0.0))
    ks = (p & (tab[..., FR_] > 0.5)).sum(-1) / nn
    return np.stack([n, mass.sum(-1), spd, msd, mass.max(-1), ks], -1)


def structure_card(rec, sz: Sizes, Hpx: int, lag=8):
    """Bodies and their statistics from the main run's slot tables (all members)."""
    tab = rec["tab"].astype(np.float64)                                       # (T + 1, M, K, 11)
    T = tab.shape[0] - 1
    p = tab[..., P_] > 0.5
    nb = p.sum(-1)
    out = dict(nb_mean=float(nb.mean()), nb_std=float(nb.std()), nb_max=int(nb.max()), K=int(tab.shape[2]))
    npres = max(int(p.sum()), 1)
    fs = rec["fsum"].astype(np.float64)                                       # (T, M)
    out["body_frac"] = float(((tab[1:, ..., MS_] * p[1:]).sum(-1) / np.maximum(np.abs(fs), 1e-300)).mean())
    out["body_mass"] = float((tab[..., MS_] * p).sum() / npres)
    out["rg"] = float((tab[..., RG_] * p).sum() / npres)
    old = p & (tab[..., AGE_] >= 1)
    out["v_inst"] = float((np.sqrt(tab[..., VX_] ** 2 + tab[..., VY_] ** 2) * old).sum() / max(int(old.sum()), 1))
    surv = {}
    for L in (8, 32, 128):
        if L >= T:
            continue
        same = p[L:] & p[:-L] & (tab[L:, ..., UID_] == tab[:-L, ..., UID_])
        surv[L] = float(same.sum() / max(int(p[:-L].sum()), 1))
        if L == lag:
            dy = _mi(tab[L:, ..., CY_] - tab[:-L, ..., CY_], Hpx)
            dx = _mi(tab[L:, ..., CX_] - tab[:-L, ..., CX_], Hpx)
            out["v_net"] = float((np.sqrt(dy ** 2 + dx ** 2) * same).sum() / max(int(same.sum()), 1) / L)
    out["survive"] = {str(k): v for k, v in surv.items()}
    s32 = surv.get(32, surv.get(8, float("nan")))
    L0 = 32 if 32 in surv else 8
    out["half_life_ticks"] = float(L0 * np.log(2.0) / max(-np.log(max(s32, 1e-12)), 1e-12)) if s32 < 1 else float("inf")
    if p[:-L0].sum() < 20:                                                    # too few body-ticks to say
        out["half_life_ticks"] = float("nan")
    out["age_mean"] = float((tab[..., AGE_] * p).sum() / npres)
    g = rec["glob"].astype(np.float64)                                        # (T + 1, M, 5)
    dg = (g[-1] - g[0]).mean(0) * 100.0 / T
    out.update(births100=float(dg[1]), deaths100=float(dg[2]), fusions100=float(dg[3]), fissions100=float(dg[4]),
               events100=float(dg[3] + dg[4]))
    out["events100_per_body"] = float((dg[3] + dg[4]) / max(out["nb_mean"], 1e-9))
    ov = rec["ovf"]
    out["ovf_raw_ticks"], out["ovf_kept_ticks"] = float(ov[:, 0].max()), float(ov[:, 1].max())
    out["slots_full_share"] = float((nb >= tab.shape[2]).mean())
    out["moved"] = float(rec["moved"][T // 2:].mean())
    out["body_speed_len"] = float(out.get("v_net", 0.0) / max(2.0 * out["rg"], 1e-9))
    # spectrum of the final total field
    S = rec["field_end"].astype(np.float64).sum(1)
    H, W = S.shape[-2:]
    Pw = np.abs(np.fft.fft2(S - S.mean((1, 2), keepdims=True))) ** 2
    ky = np.fft.fftfreq(H)[:, None] * H
    kx = np.fft.fftfreq(W)[None, :] * W
    r = np.minimum(np.rint(np.sqrt(ky ** 2 + kx ** 2)).astype(int), H // 2).ravel()
    spec = np.stack([np.bincount(r, weights=q.ravel(), minlength=H // 2 + 1) for q in Pw]).mean(0)
    spec = spec / max(spec.sum(), 1e-300)
    out["wavelength_px"] = float(H / max((spec * np.arange(H // 2 + 1)).sum(), 1e-9))
    out["cv_cell"] = float((S.std((1, 2)) / np.maximum(np.abs(S).mean((1, 2)), 1e-300)).mean())
    out["pr"] = float((S.sum((1, 2)) ** 2 / (H * W * np.maximum((S * S).sum((1, 2)), 1e-300))).mean())
    return out


def _body_feats(t0, t1, Hpx, zg=None, G=8):
    """Features of the slots of table t1 given the table one tick earlier t0: (..., K, F) and validity (..., K)."""
    ok = (t0[..., P_] > 0.5) & (t1[..., P_] > 0.5) & (t0[..., UID_] == t1[..., UID_]) & (t1[..., EV_] == 0)
    d1y = _mi(t1[..., CY_] - t0[..., CY_], Hpx)
    d1x = _mi(t1[..., CX_] - t0[..., CX_], Hpx)
    lm1 = np.log(np.maximum(t1[..., MS_], 1e-12))
    lm0 = np.log(np.maximum(t0[..., MS_], 1e-12))
    f = [d1y, d1x, lm1, lm1 - lm0, t1[..., RG_], t1[..., FR_]]
    F = np.stack(f, -1)
    if zg is not None:                                                        # zg (..., Q, G, G) at the same tick
        b = Hpx / G
        iy = np.floor(np.mod(t1[..., CY_], Hpx) / b).astype(int) % G
        ix = np.floor(np.mod(t1[..., CX_], Hpx) / b).astype(int) % G
        nbf = _nb3(zg)                                                        # (..., 9Q, G, G)
        nbf = np.moveaxis(nbf, -3, -1)                                        # (..., G, G, 9Q)
        lead = t1.shape[:-2]
        idx = np.indices(lead + (t1.shape[-2],))
        sel = nbf[tuple(idx[:-1]) + (iy, ix)] if lead else nbf[iy, ix]
        F = np.concatenate([F, sel], -1)
    return F, ok


def _body_targets(t1, th, Hpx):
    same = (th[..., P_] > 0.5) & (th[..., UID_] == t1[..., UID_])
    dy = _mi(th[..., CY_] - t1[..., CY_], Hpx)
    dx = _mi(th[..., CX_] - t1[..., CX_], Hpx)
    dl = np.log(np.maximum(th[..., MS_], 1e-12)) - np.log(np.maximum(t1[..., MS_], 1e-12))
    quiet = same & (th[..., EV_] == 0) & (np.abs(dl) < QUIET_DLOGM)
    return np.stack([dy, dx, dl], -1), quiet, same


def bodies_card(rec, sz: Sizes, ts, Hpx, G, zgrid=None, seed=0):
    """The single-body law on QUIET steps: per-body increments over h ticks (wrapped displacement; log-mass
    change) predicted from the body's own state by a ridge; oracle from the replicas (rows quiet in every
    replica). Displacement and mass are scored separately. With zgrid (standardised block view of the main run,
    (T + 1, M, Q, G, G)) a second fit adds the 3 x 3 block neighbourhood of the body (its surroundings).
    Baseline 'pers' = constant velocity, constant mass."""
    rng = np.random.default_rng([seed, 13])
    tab = rec["tab"].astype(np.float64)
    ta = rec["b_tab"].astype(np.float64)                                      # (NS, HB, Bb, K, 11)
    T, M = tab.shape[0] - 1, tab.shape[1]
    hz, R = sz.hz, sz.R
    fit = np.arange(sz.M_fit)
    test = np.arange(sz.M_fit, M)
    nt = T - max(hz)
    out = dict(hz=list(hz))
    variants = {"single": None}
    if zgrid is not None:
        variants["field"] = zgrid
    PARTS = (("disp", slice(0, 2)), ("mass", slice(2, 3)))
    KS = ("v_clim", "v_pred", "v_pers", "v_orc")
    F_fit, ok_fit, F_test, ok_test = {}, {}, {}, {}
    for name, zg in variants.items():
        F_fit[name], ok_fit[name] = _body_feats(tab[0:nt, fit], tab[1:nt + 1, fit], Hpx,
                                                None if zg is None else zg[1:nt + 1, fit], G)
        ft, okt = [], []
        for t in ts:
            a, b = _body_feats(tab[t - 1, test], tab[t, test], Hpx, None if zg is None else zg[t, test], G)
            ft.append(a)
            okt.append(b)
        F_test[name], ok_test[name] = np.concatenate(ft, 0), np.concatenate(okt, 0)   # (NS, K, F), (NS, K)
    tab_s = np.concatenate([tab[t, test] for t in ts], 0)                     # (NS, K, 11)
    pres_s = tab_s[..., P_] > 0.5
    pres_f = tab[1:nt + 1, fit][..., P_] > 0.5
    res = {name: {p: {k: [] for k in KS} for p, _ in PARTS} for name in variants}
    n_rows, surv_all, surv_any, quiet, scales = [], [], [], [], []
    for h in hz:
        Yf, okh, _ = _body_targets(tab[1:nt + 1, fit], tab[1 + h:nt + 1 + h, fit], Hpx)
        Yr, okr, samer = _body_targets(tab_s[:, None], ta[:, h - 1, :R], Hpx)  # (NS, R, K, 3), (NS, R, K)
        surv_any.append(float(samer[np.broadcast_to(pres_s[:, None], samer.shape)].mean()) if pres_s.any() else float("nan"))
        surv_all.append(float(samer.all(1)[pres_s].mean()) if pres_s.any() else float("nan"))
        quiet.append(float(okh[pres_f].mean()) if pres_f.any() else float("nan"))
        allr = okr.all(1)                                                     # (NS, K): quiet in every replica
        for name in variants:
            okf = ok_fit[name] & okh
            oks = ok_test[name] & allr
            X, Yt = F_fit[name][okf], Yf[okf]
            if name == "single":
                n_rows.append([int(X.shape[0]), int(oks.sum())])
            if X.shape[0] < 50 or oks.sum() < 5:
                for p, _ in PARTS:
                    for k in KS:
                        res[name][p][k].append(np.full((1,), np.nan))
                if name == "single":
                    scales.append([float("nan")] * 2)
                continue
            fm, fsd = X.mean(0), np.maximum(X.std(0), 1e-9)
            ym = Yt.mean(0)
            sdd = np.sqrt(max(((Yt[:, :2] - ym[:2]) ** 2).mean(), 1e-12))     # pooled displacement scale (px)
            ysd = np.array([sdd, sdd, max(Yt[:, 2].std(), 1e-9)])
            if name == "single":
                scales.append([float(sdd), float(ysd[2])])
            Xz = np.concatenate([(X - fm) / fsd, np.ones((X.shape[0], 1))], 1)
            Wt = _ridge(Xz, [(Yt - ym) / ysd], 1e-3)[0]
            Fs = F_test[name][oks]
            pred = np.concatenate([(Fs - fm) / fsd, np.ones((Fs.shape[0], 1))], 1) @ Wt          # (n, 3)
            yr = (np.moveaxis(Yr, 1, 2)[oks] - ym) / ysd                      # (n, R, 3)
            sidx = np.nonzero(oks)[0]                                         # state of each row
            inert = np.stack([(h * Fs[:, 0] - ym[0]) / ysd[0], (h * Fs[:, 1] - ym[1]) / ysd[1],
                              np.full(Fs.shape[0], (0.0 - ym[2]) / ysd[2])], -1)
            err = dict(v_clim=(yr ** 2).mean(1), v_pred=((yr - pred[:, None]) ** 2).mean(1),
                       v_pers=((yr - inert[:, None]) ** 2).mean(1), v_orc=yr.var(1, ddof=1))
            cnt = np.bincount(sidx, minlength=sz.NS)
            for p, sl in PARTS:
                for k in KS:
                    s = np.bincount(sidx, weights=err[k][:, sl].mean(1), minlength=sz.NS)
                    res[name][p][k].append((s / np.maximum(cnt, 1))[cnt > 0])   # per state (states with a row)
    for name in variants:
        out[name] = {}
        for p, _ in PARTS:
            r = res[name][p]
            ent = {k: [float(np.nanmean(v)) if np.isfinite(v).any() else float("nan") for v in r[k]] for k in KS}
            emd = {k: [float(np.nanmedian(v)) if np.isfinite(v).any() else float("nan") for v in r[k]] for k in KS}
            ent.update({k + "_med": v for k, v in emd.items()})
            ent.update({k: v.tolist() for k, v in _ratios(*(np.asarray(ent[k]) for k in ("v_clim", "v_orc", "v_pred", "v_pers"))).items()})
            ent.update({k + "_med": v.tolist() for k, v in
                        _ratios(*(np.asarray(emd[k]) for k in ("v_clim", "v_orc", "v_pred", "v_pers"))).items()})
            se = []
            for i in range(len(hz)):
                c, o, pz = r["v_clim"][i], r["v_orc"][i], r["v_pred"][i]
                n = len(c)
                if n < 3 or not np.isfinite(c).all():
                    se.append(float("nan"))
                    continue
                idx = _boot(rng, n, sz.n_boot)
                c, o, pz = c[idx].mean(1), o[idx].mean(1), pz[idx].mean(1)
                se.append(float(np.nanstd((c - np.minimum(pz, c)) / np.where(np.abs(c - o) > 1e-12, c - o, np.nan))))
            ent["ceil_se"] = se
            out[name][p] = ent
    out["n_rows_fit_test"] = n_rows
    out["scale_disp_px_dlogm"] = scales
    out["survive_replica"] = surv_any
    out["survive_all_replicas"] = surv_all
    out["quiet_share"] = quiet
    return out


def _quad(z):
    d = z.shape[-1]
    iu = np.triu_indices(d)
    return (z[..., :, None] * z[..., None, :])[..., iu[0], iu[1]]


def pop_card(rec, sz: Sizes, ts, grid_moments=None, grid_moments_test=None, seed=0):
    """The population level: global ridge (linear, quadratic), the kind-share law, stationarity, hidden part,
    actions. grid_moments (T + 1, M, E): optional features of the block view (cross-level test)."""
    rng = np.random.default_rng([seed, 17])
    Y = pop_vector(rec["tab"])                                                # (T + 1, M, 6)
    YA = pop_vector(rec["b_tab"])                                             # (NS, HB, Bb, 6)
    T, M = Y.shape[0] - 1, Y.shape[1]
    hz, R, lay = sz.hz, sz.R, sz.layout()
    fit = np.arange(sz.M_fit)
    test = np.arange(sz.M_fit, M)
    yf = Y[:, fit]
    mu, sd = yf.mean((0, 1)), yf.std((0, 1))
    mbody = mu[1] / max(mu[0], 1e-9)
    floor = np.array([0.25, 0.01 * abs(mu[1]), max(0.01 * abs(mu[2]), 1e-3), 0.01 * mbody, 0.01 * abs(mu[4]), 0.02])
    live = (sd > floor) & (mu[0] >= 0.5)        # a component that moves less than its resolution is a constant
    out = dict(hz=list(hz), names=list(POP_NAMES), mean=mu.tolist(), std=sd.tolist(), live=live.tolist(),
               floor=floor.tolist())
    if live.sum() == 0:
        out["empty"] = True
        return out
    li = np.nonzero(live)[0]
    z = (Y[..., li] - mu[li]) / sd[li]
    za = (YA[..., li] - mu[li]) / sd[li]
    hmax = max(hz)
    nt = T - hmax

    def feats(zt, zt1, kind, gm=None):
        f = [zt, zt1]
        if kind == "quad":
            f.append(_quad(zt))
        if gm is not None:
            f.append(gm)
        f.append(np.ones(zt.shape[:-1] + (1,)))
        return np.concatenate(f, -1)
    zs = np.concatenate([z[t, test] for t in ts], 0)                          # (NS, d)
    zs1 = np.concatenate([z[t - 1, test] for t in ts], 0)
    kinds = ["lin", "quad"] + (["lin+grid"] if grid_moments is not None else [])
    per = {k: {q: [] for q in ("v_clim", "v_pers", "v_pred", "v_orc")} for k in kinds}
    za_h, comp = [], {k: [] for k in ("v_clim", "v_pers", "v_pred", "v_orc")}
    for h in hz:
        zr = za[:, h - 1, :R]                                                 # (NS, R, d)
        vo = zr.var(1, ddof=1)
        za_h.append(za[:, h - 1])
        Yt = z[1 + h:1 + h + nt, fit].reshape(-1, len(li))
        for k in kinds:
            gm = grid_moments[1:nt + 1, fit] if k == "lin+grid" else None
            Xf = feats(z[1:nt + 1, fit], z[0:nt, fit], "quad" if k == "quad" else "lin", gm).reshape(Yt.shape[0], -1)
            W = _ridge(Xf, [Yt], 1e-3)[0]
            gms = np.concatenate([grid_moments[t, test] for t in ts], 0) if k == "lin+grid" else None
            pred = feats(zs, zs1, "quad" if k == "quad" else "lin", gms) @ W
            ep = ((zr - pred[:, None]) ** 2).mean(1)
            per[k]["v_clim"].append((zr ** 2).mean((1, 2)))
            per[k]["v_pers"].append(((zr - zs[:, None]) ** 2).mean((1, 2)))
            per[k]["v_pred"].append(ep.mean(1))
            per[k]["v_orc"].append(vo.mean(1))
            if k == "lin":
                comp["v_clim"].append((zr ** 2).mean((0, 1)))
                comp["v_pers"].append(((zr - zs[:, None]) ** 2).mean((0, 1)))
                comp["v_pred"].append(ep.mean(0))
                comp["v_orc"].append(vo.mean(0))
    for k in kinds:
        out[k] = _summ({q: np.asarray(v) for q, v in per[k].items()}, rng, sz.n_boot)
    cc = {k: np.asarray(v) for k, v in comp.items()}                          # (nh, d_live)
    den = np.where(np.abs(cc["v_clim"] - cc["v_orc"]) > 1e-12, cc["v_clim"] - cc["v_orc"], np.nan)
    out["components"] = dict(names=[POP_NAMES[i] for i in li],
                             pf=(1 - cc["v_orc"] / np.maximum(cc["v_clim"], 1e-300)).tolist(),
                             ceil=((cc["v_clim"] - np.minimum(np.minimum(cc["v_pred"], cc["v_pers"]), cc["v_clim"])) / den).tolist(),
                             v_orc=cc["v_orc"].tolist())
    zf = z[:, fit]
    out["tick_share"] = _tick_share(zf)
    out["tick_share_q"] = {POP_NAMES[i]: _tick_share(zf[:, :, j]) for j, i in enumerate(li)}
    out["member_share"] = _member_share(z)
    out["member_share_q"] = {POP_NAMES[i]: _member_share(z[:, :, j:j + 1]) for j, i in enumerate(li)}
    out["autocorr"] = [float(np.mean(zf[h:] * zf[:-h])) for h in hz]
    T3 = (T + 1) // 3
    out["within_window"] = dict(d_mean=(zf[-T3:].mean((0, 1)) - zf[:T3].mean((0, 1))).tolist(),
                                names=[POP_NAMES[i] for i in li])
    v_orc_s = np.asarray(per["lin"]["v_orc"])
    out.update(_hidden_and_actions(za_h, v_orc_s, sz, lay, (1,), rng))
    # the kind-share law ds = b1 s (1 - s) + b2 (1 - 2 s) on the raw share, against a constant and a line
    s = Y[..., 5]
    sa = YA[..., 5]
    law = {"hz": list(hz), "law": [], "const": [], "lin": [], "pf": [], "sd_ds": []}
    if live[5]:
        ss = np.concatenate([s[t, test] for t in ts], 0)
        for h in hz:
            ds = (s[1 + h:1 + h + nt, fit] - s[1:nt + 1, fit]).ravel()
            s0 = s[1:nt + 1, fit].ravel()
            dr = sa[:, h - 1, :R] - ss[:, None]                               # (NS, R)
            vo = dr.var(1, ddof=1).mean()
            vc = (dr ** 2).mean()
            row = {}
            for name, fn in (("law", lambda v: np.stack([v * (1 - v), 1 - 2 * v], -1)),
                             ("const", lambda v: np.ones(v.shape + (1,))),
                             ("lin", lambda v: np.stack([np.ones_like(v), v], -1))):
                X = fn(s0)
                W = np.linalg.lstsq(X, ds, rcond=None)[0]
                row[name] = ((dr - (fn(ss) @ W)[:, None]) ** 2).mean()
            den = vc - vo
            for name in ("law", "const", "lin"):
                law[name].append(float((vc - min(row[name], vc)) / den) if abs(den) > 1e-12 else float("nan"))
            law["pf"].append(float(1 - vo / max(vc, 1e-300)))
            law["sd_ds"].append(float(np.sqrt(vc)))
    out["kind_share_law"] = law
    return out


# ----------------------------------------------------------------------------- the card of one run
def analyse(rec, sz: Sizes, meta: dict, seed: int = 0, with_learned: bool = True) -> dict:
    """All card entries of one simulated window. meta: Hpx, G, grid_names (the adapter's)."""
    Hpx, G = int(meta["Hpx"]), int(meta["G"])
    Q = rec["g"].shape[2]
    seg = sz.T // sz.n_snap
    ts = [(s + 1) * seg for s in range(sz.n_snap)]
    fit = np.arange(sz.M_fit)
    lay = sz.layout()
    card = dict(sizes=dict(M=sz.M, M_fit=sz.M_fit, T=sz.T, NS=sz.NS, R=sz.R, R2=sz.R2, n_dir=sz.n_dir, eps=list(sz.eps),
                           arms=[list(a) for a in sz.arms], R_u=sz.R_u, T_in=sz.T_in, HB=sz.HB, Bb=sz.Bb),
                finite=bool(rec["finite"]), timing=rec["timing"])
    # grid level (the full card of the level)
    g = grid_card(rec["g"], rec["b_g"], sz, ts, fit, seed=seed)
    per_state_grid = g.pop("_per_state")
    card["grid"] = g
    # structure, bodies, population
    card["structure"] = structure_card(rec, sz, Hpx)
    Y = rec["g"].astype(np.float64)
    mu = np.asarray(g["mean"])
    sd = np.maximum(np.asarray(g["std"]), 1e-12 * np.maximum(np.abs(mu), 1e-300))
    zgrid = (Y - mu[None, None, :, None, None]) / sd[None, None, :, None, None]
    card["bodies"] = bodies_card(rec, sz, ts, Hpx, G, zgrid=zgrid, seed=seed)
    gm = np.concatenate([zgrid.mean((3, 4)), zgrid.std((3, 4))], -1)          # (T + 1, M, 2Q) block-view moments
    card["pop"] = pop_card(rec, sz, ts, grid_moments=gm, seed=seed)
    # cross-level: does the slot list add to the block view's cheap predictor? raster of the bodies per block
    tab = rec["tab"].astype(np.float64)
    ras = body_raster(tab, Hpx, G)                                            # (T + 1, M, 3, G, G)
    rs = np.maximum(ras[:, fit].std((0, 1, 3, 4)), 1e-9)
    ras = ras / rs[None, None, :, None, None]
    gx = grid_card(rec["g"], rec["b_g"][:, :, :sz.R], sz, ts, fit, with_arms=False, extra=_nb3(ras), seed=seed, detail=False)
    gx.pop("_per_state")
    card["cross"] = dict(
        bodies_to_grid=dict(hz=list(sz.hz), v_pred_grid=g["v_pred"], v_pred_grid_plus_bodies=gx["v_pred"],
                            gain=(np.asarray(g["v_pred"]) - np.asarray(gx["v_pred"])).tolist(),
                            ceil_plus=gx["ceil"]),
        grid_to_bodies=dict(hz=list(sz.hz), ceil_single=card["bodies"]["single"]["disp"]["ceil"],
                            ceil_field=card["bodies"]["field"]["disp"]["ceil"],
                            gain=(np.asarray(card["bodies"]["single"]["disp"]["v_pred"]) -
                                  np.asarray(card["bodies"]["field"]["disp"]["v_pred"])).tolist()))
    if "lin+grid" in card["pop"]:
        card["cross"]["grid_to_pop"] = dict(hz=list(sz.hz), gain=(np.asarray(card["pop"]["lin"]["v_pred"]) -
                                                                 np.asarray(card["pop"]["lin+grid"]["v_pred"])).tolist())
        card["cross"]["pop_over_persistence"] = dict(hz=list(sz.hz), gain=(np.asarray(card["pop"]["lin"]["v_pers"]) -
                                                                           np.asarray(card["pop"]["lin"]["v_pred"])).tolist())
    # noise twins and the hidden part at level 0 (share of matter placed differently)
    l1 = rec["b_l1"].astype(np.float64)                                       # (NS, HB, Bb): distance to arm 0
    tw = l1[:, :, 1:sz.R].mean((0, 2))
    card["twins"] = dict(l1=[float(tw[h - 1]) for h in sz.hz], l1_all=tw.tolist())
    with np.errstate(divide="ignore", invalid="ignore"):
        r = np.log2(max(tw[min(7, sz.HB - 1)], 1e-300) / max(tw[1], 1e-300)) / 6.0
    card["twins"]["doubling_ticks_2_8"] = float(1.0 / r) if r > 1e-6 else float("inf")
    # the same under a neighbour of the hidden part driven by the noise of replica 0 (the hidden part alone)
    card["twins"]["theta_l1"] = {str(e): [float(np.mean([l1[:, h - 1, lay["nb"][(e, d)][0]].mean() for d in range(sz.n_dir)]))
                                         for h in sz.hz] for e in sz.eps}
    card["nats_check"] = {f"{k}_{int(n)}": float(rec["U_norm2"][:, idx].mean() / (2.0 * meta["sigma_u"] ** 2))
                          for (k, n), idx in lay["act"].items()}
    # learned variable: slow features on half A of the fit members, both variables judged on half B
    LK = ("pf", "ceil", "gap", "v_orc", "v_pred", "v_clim", "ceil_se", "pf_med", "ceil_med", "gap_med", "ceil_med_se")
    if with_learned and sz.M_fit >= 4:
        hA, hB = fit[: sz.M_fit // 2], fit[sz.M_fit // 2:]
        ent = {}
        for tag, (ha, hb) in (("AB", (hA, hB)), ("BA", (hB, hA))):
            W, pmu, psd, lam = slow_features(rec["f"], ha, Q, G)
            L = apply_features(rec["f"], W, pmu, psd, Q, G)
            LA = apply_features(rec["b_f"], W, pmu, psd, Q, G)                # (NS, HB, R, Q, G, G)
            cl = grid_card(L, LA, sz, ts, hb, with_arms=False, seed=seed, detail=False)
            ch = grid_card(rec["g"], rec["b_g"][:, :, :sz.R], sz, ts, hb, with_arms=False, seed=seed, detail=False)
            # is it the same variable? R^2 of each learned component on the hand channels (fit half hb, per block)
            Lz = _rows(L[:, hb])
            Hz = _rows(zgrid[:, hb])
            Hz1 = np.concatenate([Hz, np.ones((Hz.shape[0], 1))], 1)
            coef = np.linalg.lstsq(Hz1, Lz, rcond=None)[0]
            r2 = 1.0 - ((Lz - Hz1 @ coef) ** 2).mean(0) / np.maximum(Lz.var(0), 1e-300)
            ent[tag] = dict(lam=lam.tolist(), r2_on_hand=r2.tolist(),
                            learned={k: cl.get(k) for k in LK}, hand={k: ch.get(k) for k in LK})
        card["learned"] = ent
    card["_per_state_grid"] = per_state_grid
    card["grid_shape"] = [G, G]
    card["grid_names"] = list(meta.get("grid_names", []))
    return card


def body_raster(tab, Hpx, G):
    """Slot tables (T + 1, M, K, 11) -> (T + 1, M, 3, G, G): per block, the mass of the bodies centred there and
    their mass-weighted velocity (y, x)."""
    p = tab[..., P_] > 0.5
    b = Hpx / G
    iy = np.floor(np.mod(tab[..., CY_], Hpx) / b).astype(int) % G
    ix = np.floor(np.mod(tab[..., CX_], Hpx) / b).astype(int) % G
    T1, M, K = p.shape
    out = np.zeros((T1, M, 3, G, G))
    tt, mm, _ = np.indices(p.shape)
    w = np.where(p, tab[..., MS_], 0.0)
    for c, v in enumerate((w, w * tab[..., VY_], w * tab[..., VX_])):
        np.add.at(out, (tt, mm, c, iy, ix), v)
    return out


def strip(card: dict) -> dict:
    """JSON-safe copy without the private arrays."""
    def conv(v):
        if isinstance(v, dict):
            return {str(k): conv(x) for k, x in v.items() if not str(k).startswith("_")}
        if isinstance(v, (list, tuple)):
            return [conv(x) for x in v]
        if isinstance(v, np.ndarray):
            return conv(v.tolist())
        if isinstance(v, (np.floating, float)):
            f = float(v)
            return f if np.isfinite(f) else None
        if isinstance(v, (np.integer,)):
            return int(v)
        if isinstance(v, (np.bool_,)):
            return bool(v)
        return v
    return conv(card)
