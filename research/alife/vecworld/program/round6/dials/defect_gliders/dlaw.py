"""dlaw -- the gliders wind world with an INCOMPLETE public law (round 6, dials, design study defect_gliders).

The public law is gworld.tick (Flow-Lenia A_gliders, 20 substeps per tick, wind a~ = u + sigma_w eta held for
the tick). The hidden world adds terms that the public simulator does not have. Five candidate kinds, each
with a strength in q (a pytree of traced scalars, so one compiled program runs every candidate and the public
law; all strengths zero = the public law):

    g   GUST      flow term: the wind enters as E (1 + g s_w), s_w = smoothstep((|E| - W0) / DW): the response
                  to wind is nonlinear above a threshold (public: linear, gain 1).
    xw  STRESS    channel coupling: where s_w > 0, channel 0 converts to channel 1 at rate xw KXW s_w per unit
                  time (per-channel mass is conserved by the public law; total mass stays conserved).
    m   SCAR      slow hidden field S in [0, 1]: dS/dt = KON s_w (1 - S) - S / TAU; the affinity (growth) is
                  multiplied by (1 - m S): strong wind leaves a patch where bodies lose cohesion for ~TAU.
    x   DENSE     channel coupling at high density: channel 0 converts to channel 1 at rate x KX s_d,
                  s_d = smoothstep((A_sum - A0) / DA) (collisions, compression).
    t   TERRAIN   static smooth force field: flow <- flow + t T(x), T fixed per hidden world, RMS |T| = T_RMS.

No file of vw, the port or any earlier study is changed; gworld, wind and flowlenia_jax are imported.
With q = None the tick IS gworld.tick (the zero point of the dial is the baseline law by construction);
with traced zeros it is compared with gworld.tick in check_zero.py.
"""
from __future__ import annotations

import os
import sys

sys.dont_write_bytecode = True
HERE = os.path.dirname(os.path.abspath(__file__))
PROG = os.path.dirname(os.path.dirname(os.path.dirname(HERE)))
GEX = os.path.join(PROG, "track2", "gliders_exam")
if GEX not in sys.path:
    sys.path.insert(0, GEX)
import gworld as GW  # noqa: E402

import jax  # noqa: E402
import jax.numpy as jnp  # noqa: E402
import numpy as np  # noqa: E402

from vw.core import Noise  # noqa: E402

FJ, WD, PH = GW.FJ, GW.WD, GW.PH
CFG, NW, G, STRIDE, NOISE_STD, SIG = GW.CFG, GW.NW, GW.G, GW.STRIDE, GW.NOISE_STD, GW.SIGMA_W
H, W, NC = GW.H, GW.W, GW.NC
DT = float(CFG.dt)

# declared constants of the candidates (the dial is the strength; these would be hidden too)
W0, DW = 0.12, 0.05          # wind trigger: 0 below |E| = 0.12, full above 0.17 (results/probe.json)
KXW = 0.09                   # stress conversion rate per unit time at full trigger (xw = 1: 30% per tick)
KON, TAU = 0.25, 80.0        # scar: charge rate per unit time, decay time (20 ticks)
A0, DA, KX = 2.4, 0.4, 0.25  # dense conversion: trigger on A_sum, rate per unit time
T_RMS, T_CORR = 0.08, 12.0   # terrain: RMS force magnitude, correlation length in px
KEYS = ("g", "xw", "m", "x", "t")
SC1 = np.load(os.path.join(GEX, "results", "scales.npz"))["level1"].astype(float)      # (192,) public scales


def qdict(**kw) -> dict:
    """Strengths (float64 scalars); missing = 0."""
    bad = set(kw) - set(KEYS)
    if bad:
        raise KeyError(sorted(bad))
    return {k: jnp.asarray(float(kw.get(k, 0.0))) for k in KEYS}


def smoothstep(z):
    z = jnp.clip(z, 0.0, 1.0)
    return z * z * (3.0 - 2.0 * z)


def terrain(seed: int) -> np.ndarray:
    """A hidden static force field (2, H, W): minus the gradient of a smooth Gaussian random potential
    (spectral filter exp(-(k T_CORR)^2 / 2)), scaled to RMS magnitude T_RMS."""
    rng = np.random.default_rng([int(seed), 77])
    ky = 2 * np.pi * np.fft.fftfreq(H)[:, None]
    kx = 2 * np.pi * np.fft.fftfreq(W)[None, :]
    V = np.fft.ifft2(np.fft.fft2(rng.standard_normal((H, W))) * np.exp(-0.5 * (ky ** 2 + kx ** 2) * T_CORR ** 2)).real
    Ty = -(np.roll(V, -1, 0) - np.roll(V, 1, 0)) / 2
    Tx = -(np.roll(V, -1, 1) - np.roll(V, 1, 1)) / 2
    T = np.stack([Ty, Tx])
    return T * (T_RMS / np.sqrt((T ** 2).sum(0).mean()))


def _flow(p, A, fK, aff_scale):
    U = jax.lax.optimization_barrier(FJ.affinity(CFG, p, A, fK) * aff_scale)
    gUy, gUx = FJ.sobel(U)
    gAy, gAx = FJ.sobel(A.sum(0))
    src = A.sum(0, keepdims=True)
    alpha = jnp.clip((src / p["theta_A"]) ** p["n"], 0.0, 1.0)
    return gUy * (1.0 - alpha) - gAy * alpha, gUx * (1.0 - alpha) - gAx * alpha


def tick(p, q, T, A, S, nz, u_w, sigma_w):
    """One tick of the hidden world: (A (C, H, W), S (H, W)) -> (A, S). q = None: the public law."""
    if q is None:
        return GW.tick(p, A, nz, u_w, sigma_w), S
    a = u_w + sigma_w * nz.stream(WD.WIND_STREAM).normal((NW,))
    E = WD.wind_field(a)
    sw = smoothstep((jnp.sqrt(E[0] ** 2 + E[1] ** 2) - W0) / DW)             # (H, W), fixed over the tick
    F = p["gw"] * E * (1.0 + q["g"] * sw)
    fK = FJ.kernel_fft(CFG, p)
    shape = (CFG.C, CFG.H, CFG.W)

    def body(c, i):
        A, S = c
        xi = nz.substep(STRIDE, i).normal((2,) + shape)
        Fy, Fx = _flow(p, A, fK, (1.0 - q["m"] * S)[None])
        Fy = Fy + NOISE_STD * xi[0] + F[0] + q["t"] * T[0]
        Fx = Fx + NOISE_STD * xi[1] + F[1] + q["t"] * T[1]
        Fy, Fx = jax.lax.optimization_barrier((Fy, Fx))
        A = FJ.reintegrate(CFG, A, Fy, Fx)
        sd = smoothstep((A.sum(0) - A0) / DA)
        conv = A[0] * (1.0 - jnp.exp(-DT * (q["xw"] * KXW * sw + q["x"] * KX * sd)))
        A = jnp.stack([A[0] - conv, A[1] + conv])
        S = S + DT * (KON * sw * (1.0 - S) - S / TAU)
        return (A, S), None
    (A, S), _ = jax.lax.scan(body, (A, S), jnp.arange(STRIDE))
    return A, S


class DRunner:
    """Batched runs with per-member strengths q (lax.map over members, as gworld.Runner).
    init_burn(P, Q, T, k (B,), sig (B,)) -> A, S, m, obs (B, 336)   [tracker on, for aimed programs]
    fut(P, Q, T, A, S, key (B,), t0 (B,), uw (B, Tn, NW), sig (B,)) -> y (B, Tn + 1, 192), A_end, S_end
    T is one terrain (2, H, W) shared by the batch."""

    def __init__(self, burn: int = GW.BURN):
        po, trv, _ = PH.phi_objects_jax("A_gliders")
        self.bt = trv.bt
        self.pc = PH.phi_coarse(CFG, G)
        lev0, _, _ = FJ.make_level("A_gliders", NOISE_STD)
        self.init0 = lev0.init
        self.burn = int(burn)
        self.init_burn = jax.jit(self._init_burn)
        self.fut = jax.jit(self._fut)

    def _init_burn(self, P, Q, T, k, sig):
        bt, fold = self.bt, jax.random.fold_in

        def one(args):
            p, q, kk, sg = args
            A = self.init0(p, fold(kk, GW._ST_INIT))
            S = jnp.zeros((H, W))
            m = bt.init_memory(A)
            kp = fold(fold(kk, GW._ST_BURN), GW._ST_PROC)
            zw = jnp.zeros((NW,))

            def body(c, t):
                A, S, m = c
                A, S = tick(p, q, T, A, S, Noise(kp, t), zw, sg)
                return (A, S, bt.update_memory(m, A)), None
            (A, S, m), _ = jax.lax.scan(body, (A, S, m), jnp.arange(self.burn))
            return A, S, m, jnp.concatenate([self.pc.phi(A, ()), bt.phi(A, m)])
        return jax.lax.map(one, (P, Q, k, sig))

    def _fut(self, P, Q, T, A, S, key, t0, uw, sig):
        fold = jax.random.fold_in

        def one(args):
            p, q, A, S, kk, t0, uw, sg = args
            kp = fold(kk, GW._ST_PROC)

            def body(c, w):
                A, S, t = c
                A, S = tick(p, q, T, A, S, Noise(kp, t), w, sg)
                return (A, S, t + 1), self.pc.phi(A, ())
            y0 = self.pc.phi(A, ())
            (A, S, _), ys = jax.lax.scan(body, (A, S, t0), uw)
            return jnp.concatenate([y0[None], ys], 0), A, S
        return jax.lax.map(one, (P, Q, A, S, key, t0, uw, sig))


def stack(trees):
    return jax.tree_util.tree_map(lambda *v: jnp.stack(v), *trees)


def rep(tree, n):
    return jax.tree_util.tree_map(lambda v: jnp.broadcast_to(v, (n,) + v.shape), tree)


# ----------------------------------------------------------------------------- designed probes (<= 200 nats)
def strong_push(yc, angle, ticks=2, per_tick=100.0, H_=8):
    """Designed probe for the wind-triggered candidates: the largest force the tick cap (100 nats) allows on
    the 2 x 2 blocks at the heaviest group, for `ticks` ticks (200 nats): f = sigma_w sqrt(per_tick / 2),
    peak field 0.32 (against 0.23 for the exam mix's aimed push and 0.15 for its regional push)."""
    i0, j0 = GW.heaviest_group(yc)
    f = SIG * np.sqrt(per_tick / 2.0) * (1 - 1e-9)
    n = np.array([np.sin(angle), np.cos(angle)])
    U = np.zeros((H_, 2, G, G))
    rows, cols = [i0, (i0 + 1) % G], [j0, (j0 + 1) % G]
    for t in range(ticks):
        for c in range(2):
            U[t, c][np.ix_(rows, cols)] = f * n[c]
    return U.reshape(H_, NW)


def squeeze(yc, ticks=2, per_tick=100.0, H_=8):
    """Designed probe for the density-triggered candidate: a converging wind on the 2 x 4 blocks around the
    heaviest group (left half pushes right, right half pushes left), 100 nats per tick for `ticks` ticks."""
    i0, j0 = GW.heaviest_group(yc)
    f = SIG * np.sqrt(per_tick / 2.0) * (1 - 1e-9)
    U = np.zeros((H_, 2, G, G))
    rows = [i0, (i0 + 1) % G]
    for t in range(ticks):
        U[t, 1][np.ix_(rows, [(j0 - 1) % G, j0])] = +f / np.sqrt(2)
        U[t, 1][np.ix_(rows, [(j0 + 1) % G, (j0 + 2) % G])] = -f / np.sqrt(2)
    return U.reshape(H_, NW)
