"""wind -- the A_gliders world with a coarse "wind" actuation channel (track 2 actuation probe).

A new level variant built from the port's pure functions (port/flowlenia_jax.py is imported, not
changed). One call of the level is one TICK (20 Flow-Lenia substeps), because the wind is drawn once
per tick and held for all 20 substeps (EXAM 3.3 option 1; vw.stride would apply an input at the first
substep only).

Declared wind channel
    coefficients   a in R^(2 x G x G), G = 8: one force per 16 x 16 px block and component (y, x).
    embedding      E(a) = periodic Gaussian blur (std SMOOTH_PX = 8 px, i.e. half a block, applied by
                   FFT with transfer exp(-2 pi^2 s^2 |k|^2)) of the piecewise-constant block field.
                   E is public and linear, DC gain 1 (a uniform a gives the uniform field a).
    law            every substep of a tick: flow F <- F + E(a~) (both channels) + 0.5 xi (the port's flow
                   noise), then the port's clipped, mass-conserving reintegration.
    noise          a~ = u_w + sigma_w * eta, eta ~ N(0, I_128), drawn once per tick from its own
                   sub-stream (Noise.stream(WIND_STREAM)) of the tick's process key; present at every
                   tick, also when u_w = 0.
    cost           c(u_w) = 0.5 ||u_w||^2 / sigma_w^2 nats per tick (exact: the conditional law of the
                   level-0 path given a~ is the same under every program, so KL(P_u || P_0) is the KL of
                   the a~ sequence; data processing then bounds every level and port).
A force f held 20 substeps moves matter by 20 * dt * f = 4 f px per tick.

The matter kick of the port (flowlenia_jax.kick, before the first substep) is kept in the same level
as the first H*W input coordinates, so one compiled program runs both channels:
    u = [u_kick (H*W) | u_wind (2*G*G)].
With sigma_w = 0 and u_wind = 0 a tick is the port's strided tick (vw.stride(make_level(...), 20)),
same functions and the same noise clocks (checked in check_wind.py).
"""
from __future__ import annotations

import os
import sys

sys.dont_write_bytecode = True
PORT = "/home/user/evalwork/vecworld/vw1/port"
if PORT not in sys.path:
    sys.path.insert(0, PORT)
import _paths  # noqa: E402,F401  (adds vw1, port, VW-0 read-only paths)

import jax  # noqa: E402
import jax.numpy as jnp  # noqa: E402
import numpy as np  # noqa: E402

import vw  # noqa: E402
from vw.core import Noise  # noqa: E402
from vw.world import make_key, member_keys  # noqa: E402,F401
import flowlenia_jax as FJ  # noqa: E402
import phi as PH  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
RES = os.path.join(HERE, "results")
os.makedirs(RES, exist_ok=True)

G, SMOOTH_PX, STRIDE, NOISE_STD, BURN_TICKS = 8, 8.0, 20, 0.5, 50
WIND_STREAM = 7                         # Noise.stream index of the wind draw
_ST_INIT, _ST_BURN, _ST_PROC, _ST_DYN = 1, 2, 3, 6     # vw.world stream ids (same key discipline)
KMAX = 32                               # max kick cells per tick in a program
H = W = 128
HW = H * W
NW = 2 * G * G
NC, NO = 192, 144                       # Phi_coarse, Phi_objects output lengths
K_SLOTS, NF, NS = 12, 12, 17


# ----------------------------------------------------------------------------- the channel
def gauss_hat(h=H, w=W, s=SMOOTH_PX):
    ky = np.fft.fftfreq(h)[:, None]
    kx = np.fft.rfftfreq(w)[None, :]
    return np.exp(-2.0 * (np.pi * s) ** 2 * (ky ** 2 + kx ** 2))


_GH = gauss_hat()          # numpy constant (embedded in every trace)


def wind_field(a):
    """E(a): coefficients (2*G*G,) or (2, G, G) -> field (2, H, W) [y-component, x-component]."""
    a = jnp.reshape(a, (2, G, G))
    b = H // G
    up = jnp.repeat(jnp.repeat(a, b, axis=1), b, axis=2)
    return jnp.fft.irfft2(jnp.fft.rfft2(up, axes=(-2, -1)) * _GH, s=(H, W), axes=(-2, -1))


def basis_profile():
    """Numerical properties of E: g_b(p) for one block b at the corner block; sum_b g_b(p)^2 map
    (the background field variance at p is sigma_w^2 * that sum, per component)."""
    E1 = np.zeros((2, G, G))
    E1[0, 0, 0] = 1.0
    g = np.asarray(wind_field(jnp.asarray(E1)))[0]            # (H, W): block (0, 0), centre (7.5, 7.5)
    s2 = np.zeros((H, W))
    b = H // G
    for i in range(G):
        for j in range(G):
            s2 += np.roll(np.roll(g, i * b, 0), j * b, 1) ** 2
    return g, s2


def nats(u_w, sigma_w):
    """Charge of a wind command (or a stack of them): 0.5 ||u||^2 / sigma_w^2, summed."""
    u_w = np.asarray(u_w, float)
    return 0.5 * float((u_w ** 2).sum()) / sigma_w ** 2


# ----------------------------------------------------------------------------- the level
class WindWorld:
    """Pure functions of the wind variant. sigma_w is an argument of the tick, so one compiled
    program can run members of the wind world (sigma_w > 0) and the original world (sigma_w = 0)."""

    def __init__(self, name="A_gliders", noise_std=NOISE_STD):
        lev0, cfg, meta = FJ.make_level(name, noise_std)
        self.lev0, self.cfg, self.meta, self.params = lev0, cfg, meta, lev0.params
        self.std = float(noise_std)
        self.pc = PH.phi_coarse(cfg, G)
        po, trv, _ = PH.phi_objects_jax(name)
        self.po, self.bt = po, trv.bt
        self.shape = (cfg.C, cfg.H, cfg.W)

    # one tick of level 0 ------------------------------------------------------
    def tick_x(self, p, A, nz, u_k, u_w, sigma_w):
        cfg, std, shape = self.cfg, self.std, self.shape
        a = u_w + sigma_w * nz.stream(WIND_STREAM).normal((NW,))
        F = wind_field(a)
        fK = FJ.kernel_fft(cfg, p)

        def body(A, i):
            A = FJ.kick(cfg, A, jnp.where(i == 0, 1.0, 0.0) * u_k)
            xi = nz.substep(STRIDE, i).normal((2,) + shape)
            Fy, Fx = FJ.flow(cfg, p, A, fK)
            Fy = Fy + std * xi[0] + F[0]
            Fx = Fx + std * xi[1] + F[1]
            Fy, Fx = jax.lax.optimization_barrier((Fy, Fx))
            return FJ.reintegrate(cfg, A, Fy, Fx), None
        A, _ = jax.lax.scan(body, A, jnp.arange(STRIDE))
        return A

    def level(self, sigma_w):
        """The variant as a vw.Level (one tick per step); u = [u_kick (H*W) | u_wind (2*G*G)]."""
        sw = float(sigma_w)

        def step(p, A, nz, u):
            return self.tick_x(p, A, nz, u[:HW], u[HW:], sw)
        cons = {f"mass_c{c}": (lambda c: (lambda A: A[c].sum()))(c) for c in range(self.cfg.C)}
        return vw.Level(init=self.lev0.init, step=step, input_dim=HW + NW, params=self.params, conserved=cons,
                        name=f"FlowLenia[A_gliders]+wind(sigma_w={sw}, G={G}, smooth={SMOOTH_PX}px)^tick")

    # observation ---------------------------------------------------------------
    def obs(self, A, m):
        return jnp.concatenate([self.pc.phi(A, ()), self.bt.phi(A, m)])

    def table(self, m):
        d = self.bt.split(m)
        return d["table"], d["globals"]

    # runners -------------------------------------------------------------------
    def make_run(self, record_moved: bool = False):
        """run(p, A (B,C,H,W), m (B,n_m), key (B,), t0 (B,), kidx (B,T,KMAX) int, kval (B,T,KMAX),
        uw (B,T,NW), sig (B,)) -> records y (B,T+1,336), tab (B,T+1,K,NS), glob (B,T+1,5), A_end, m_end.
        record_moved=True appends moved (B,T): matter moved by each tick's kick (half the L1 change of
        the field; the kick is applied before tick_x, which then kicks with zero = the identity, so
        the law is unchanged bit for bit). Members run one after another (lax.map): the cache-friendly
        batching of aworld.MapWorld."""
        bt, fold, cfg = self.bt, jax.random.fold_in, self.cfg

        def one(args):
            p, A, m, key, t0, kidx, kval, uw, sig = args
            kp = fold(key, _ST_PROC)

            def rec(A, m):
                tb, gl = self.table(m)
                return self.obs(A, m), tb, gl

            def body(c, inp):
                A, m, t = c
                ki, kv, w = inp
                uk = jnp.zeros((HW,)).at[ki].add(kv)
                if record_moved:
                    Ak = FJ.kick(cfg, A, uk)
                    mv = 0.5 * jnp.abs(Ak - A).sum()
                    A = self.tick_x(p, Ak, Noise(kp, t), jnp.zeros((HW,)), w, sig)
                else:
                    A = self.tick_x(p, A, Noise(kp, t), uk, w, sig)
                m = bt.update_memory(m, A)
                r = rec(A, m)
                return (A, m, t + 1), (r + (mv,) if record_moved else r)
            y0, tb0, g0 = rec(A, m)
            (A, m, _), outs = jax.lax.scan(body, (A, m, t0), (kidx, kval, uw))
            cat = lambda a, b: jnp.concatenate([a[None], b], 0)
            res = (cat(y0, outs[0]), cat(tb0, outs[1]), cat(g0, outs[2]))
            return res + ((outs[3],) if record_moved else ()) + (A, m)

        @jax.jit
        def run(p, A, m, key, t0, kidx, kval, uw, sig):
            B = A.shape[0]
            P = jax.tree_util.tree_map(lambda v: jnp.broadcast_to(v, (B,) + v.shape), p)
            return jax.lax.map(one, (P, A, m, key, t0, kidx, kval, uw, sig))
        return run

    def make_init(self):
        """init_burn(p, k_init (B,), sig (B,)) -> (A, m) after init + BURN_TICKS ticks with wind noise
        sigma_w (no input); keys as vw.World.init_member: x from fold(k, INIT), burn-in process noise
        from fold(fold(k, BURN), PROC) at t = 0..49. Dynamics then use fold(k, DYN) from t = 0."""
        bt, fold = self.bt, jax.random.fold_in

        def one(args):
            p, k, sig = args
            A = self.lev0.init(p, fold(k, _ST_INIT))
            m = bt.init_memory(A)
            kp = fold(fold(k, _ST_BURN), _ST_PROC)
            z, zw = jnp.zeros((HW,)), jnp.zeros((NW,))

            def body(c, t):
                A, m = c
                A = self.tick_x(p, A, Noise(kp, t), z, zw, sig)
                return (A, bt.update_memory(m, A)), None
            (A, m), _ = jax.lax.scan(body, (A, m), jnp.arange(BURN_TICKS))
            return A, m

        @jax.jit
        def init_burn(p, k, sig):
            B = k.shape[0]
            P = jax.tree_util.tree_map(lambda v: jnp.broadcast_to(v, (B,) + v.shape), p)
            return jax.lax.map(one, (P, k, sig))
        return init_burn


def host_to_jax_memory(m_host):
    """VW-0 host tracker memory (..., 16593) -> vw.objects memory (..., 16597): + zero overflow block."""
    m_host = np.asarray(m_host, float)
    return np.concatenate([m_host, np.zeros(m_host.shape[:-1] + (4,))], -1)


def mi(d, L):
    return (d + L / 2) % L - L / 2


def closure_sd():
    """Per-coordinate standardisation of the closure study (std over the 36 x 301 free level-1
    trajectories of sim_A/sim_B, as integrate/analyze.closure); eff = non-constant coordinates."""
    Ys = [np.load(f"/home/user/evalwork/vecworld/vw1/fresh/closure/results/sim_{t}.npz")["Y"] for t in "AB"]
    Y = np.concatenate([y.reshape(-1, y.shape[-1]) for y in Ys]).astype(float)
    out = {}
    for nm, sl in (("coarse", slice(0, NC)), ("objects", slice(NC, NC + NO))):
        sd = Y[:, sl].std(0)
        eff = sd > 1e-6 * max(sd.max(), 1e-12)
        out[nm] = (np.where(eff, sd, 1.0), eff)
    return out
