"""gworld -- the A_gliders wind world with hidden global parameters (track 2, gliders_exam study).

Level 0 is the wind variant of track2/actuation/wind.py (one call = one tick = 20 Flow-Lenia substeps,
wind a~ = u + sigma_w eta drawn once per tick, field E(a~) added to the flow in every substep), without
the matter kick, and with parameters that wind.py keeps static made traceable, so that every member of a
batch can carry its own hidden theta inside one compiled program:

    p = {R, r, a, b, w, m, s, h}  (Flow-Lenia params, as port/flowlenia_jax)
        + theta_A, n              (alpha mixing: alpha = clip((A_sum / theta_A)^n, 0, 1); static in the port)
        + gw                      (wind response gain: the flow receives gw * E(a~); the charge stays
                                   1/2 |u|^2 / sigma_w^2 because the KL is that of the a~ sequence)

Hidden-parameter candidates (theta, all dimensionless, default = prior mean = A_gliders):
    lR      radius scale:  (R + 15) <- lR (R + 15)  (every kernel radius scales by lR)
    dm      growth centre: m <- m + dm * s          (shift in units of each kernel's own width)
    ls      growth width:  s <- ls * s
    lh      growth height: h <- lh * h               (scales the affinity and so the growth flow)
    lA      alpha critical mass: theta_A <- lA * 2.0
    n       alpha exponent: n (default 2.0)
    gw      wind gain (default 1.0)
    dm_00, dm_01, dm_10, dm_11   dm restricted to one kernel group (source channel c0 -> target c1)
    ls_00, ls_01, ls_10, ls_11   ls restricted to one kernel group
    lh_00, lh_01, lh_10, lh_11   lh restricted to one kernel group (not scanned)
Kernel groups (c0, c1): 00 = kernels 0-3, 01 = 4-9, 10 = 10-11, 11 = 12-19.

No file of vw1/port or vw1/vw is changed; this module imports their pure functions.
"""
from __future__ import annotations

import os
import sys
from types import SimpleNamespace

sys.dont_write_bytecode = True
PORT = "/home/user/evalwork/vecworld/vw1/port"
ACT = "/home/user/evalwork/vecworld/program/track2/actuation"
for _p in (PORT, ACT):
    if _p not in sys.path:
        sys.path.insert(0, _p)
import _paths  # noqa: E402,F401

import jax  # noqa: E402
import jax.numpy as jnp  # noqa: E402
import numpy as np  # noqa: E402

import vw  # noqa: E402
from vw.core import Noise  # noqa: E402
import flowlenia_jax as FJ  # noqa: E402
import phi as PH  # noqa: E402
import wind as WD  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
RES = os.path.join(HERE, "results")
os.makedirs(RES, exist_ok=True)

G, STRIDE, NOISE_STD, BURN = WD.G, WD.STRIDE, WD.NOISE_STD, WD.BURN_TICKS
NW, H, W = WD.NW, WD.H, WD.W
NC, NO, K, NF = WD.NC, WD.NO, WD.K_SLOTS, WD.NF
SIGMA_W = 0.05                     # the actuation study's recommended background wind
_ST_INIT, _ST_BURN, _ST_PROC, _ST_DYN = 1, 2, 3, 6

CFG, P0, META = FJ.load_world("A_gliders")
C0 = np.asarray(CFG.c0)
C1 = np.asarray(CFG.c1)
GROUPS = {f"{a}{b}": np.flatnonzero((C0 == a) & (C1 == b)) for a in (0, 1) for b in (0, 1)}
DEFAULT = {"lR": 1.0, "dm": 0.0, "ls": 1.0, "lh": 1.0, "lA": 1.0, "n": 2.0, "gw": 1.0,
           **{f"dm_{g}": 0.0 for g in GROUPS}, **{f"lh_{g}": 1.0 for g in GROUPS},
           **{f"ls_{g}": 1.0 for g in GROUPS}}


def base_params() -> dict:
    p = {k: jnp.asarray(v) for k, v in P0.items()}
    p.update(theta_A=jnp.asarray(float(CFG.theta_A)), n=jnp.asarray(float(CFG.n)), gw=jnp.asarray(1.0))
    return p


def theta_to_params(th: dict) -> dict:
    """Full parameter pytree (float64 arrays) from a partial theta dict (missing keys = default)."""
    t = dict(DEFAULT)
    t.update({k: float(v) for k, v in th.items()})
    unknown = set(th) - set(DEFAULT)
    if unknown:
        raise KeyError(f"unknown hidden parameters {sorted(unknown)}")
    m0, s0, h0 = (np.asarray(P0[q], float) for q in "msh")
    dm = np.full(20, t["dm"])
    lh = np.full(20, t["lh"])
    ls = np.full(20, t["ls"])
    for g, idx in GROUPS.items():
        dm[idx] += t[f"dm_{g}"]
        lh[idx] *= t[f"lh_{g}"]
        ls[idx] *= t[f"ls_{g}"]
    p = base_params()
    p["R"] = jnp.asarray((float(P0["R"]) + 15.0) * t["lR"] - 15.0)
    p["m"] = jnp.asarray(m0 + dm * s0)
    p["s"] = jnp.asarray(s0 * ls)
    p["h"] = jnp.asarray(h0 * lh)
    p["theta_A"] = jnp.asarray(2.0 * t["lA"])
    p["n"] = jnp.asarray(t["n"])
    p["gw"] = jnp.asarray(t["gw"])
    return p


def stack_params(plist) -> dict:
    return jax.tree_util.tree_map(lambda *v: jnp.stack(v), *plist)


# ----------------------------------------------------------------------------- the law
def _flow(p, A, fK):
    U = jax.lax.optimization_barrier(FJ.affinity(CFG, p, A, fK))
    gUy, gUx = FJ.sobel(U)
    gAy, gAx = FJ.sobel(A.sum(0))
    src = A.sum(0, keepdims=True)
    alpha = jnp.clip((src / p["theta_A"]) ** p["n"], 0.0, 1.0)
    return gUy * (1.0 - alpha) - gAy * alpha, gUx * (1.0 - alpha) - gAx * alpha


def tick(p, A, nz, u_w, sigma_w):
    """One tick: wind a~ = u_w + sigma_w eta (eta from nz.stream(7)), 20 substeps of flow + gw E(a~)
    + 0.5 xi, clipped mass-conserving reintegration (port functions)."""
    a = u_w + sigma_w * nz.stream(WD.WIND_STREAM).normal((NW,))
    F = p["gw"] * WD.wind_field(a)
    fK = FJ.kernel_fft(CFG, p)
    shape = (CFG.C, CFG.H, CFG.W)

    def body(A, i):
        xi = nz.substep(STRIDE, i).normal((2,) + shape)
        Fy, Fx = _flow(p, A, fK)
        Fy = Fy + NOISE_STD * xi[0] + F[0]
        Fx = Fx + NOISE_STD * xi[1] + F[1]
        Fy, Fx = jax.lax.optimization_barrier((Fy, Fx))
        return FJ.reintegrate(CFG, A, Fy, Fx), None
    A, _ = jax.lax.scan(body, A, jnp.arange(STRIDE))
    return A


def level(sigma_w: float = SIGMA_W, params=None) -> vw.Level:
    """The world's level 0 as a vw.Level: one tick per step, input = the 128 wind coefficients."""
    sw = float(sigma_w)
    lev0, _, _ = FJ.make_level("A_gliders", NOISE_STD)

    def step(p, A, nz, u):
        return tick(p, A, nz, u, sw)
    cons = {f"mass_c{c}": (lambda c: (lambda A: A[c].sum()))(c) for c in range(CFG.C)}
    return vw.Level(init=lev0.init, step=step, input_dim=NW, params=base_params() if params is None else params,
                    conserved=cons, name=f"FlowLenia[A_gliders]+wind(sigma_w={sw})^tick, hidden globals")


# ----------------------------------------------------------------------------- designer runners
class Runner:
    """Batched designer runs with PER-MEMBER parameters (lax.map over members, as aworld.MapWorld).
    init_burn(P, k (B,), sig (B,)) -> (A, m); run(P, A, m, key (B,), t0 (B,), uw (B, T, NW), sig (B,))
    -> y (B, T+1, 336), ext (B, T+1, K, 5) [cy, cx, age, event, uid], glob (B, T+1, 5), A_end, m_end."""

    def __init__(self):
        po, trv, _ = PH.phi_objects_jax("A_gliders")
        self.bt = trv.bt
        self.pc = PH.phi_coarse(CFG, G)
        lev0, _, _ = FJ.make_level("A_gliders", NOISE_STD)
        self.init0 = lev0.init
        self.init_burn = jax.jit(self._init_burn)
        self.run = jax.jit(self._run)

    def obs(self, A, m):
        return jnp.concatenate([self.pc.phi(A, ()), self.bt.phi(A, m)])

    def _init_burn(self, P, k, sig):
        bt, fold = self.bt, jax.random.fold_in

        def one(args):
            p, kk, sg = args
            A = self.init0(p, fold(kk, _ST_INIT))
            m = bt.init_memory(A)
            kp = fold(fold(kk, _ST_BURN), _ST_PROC)
            zw = jnp.zeros((NW,))

            def body(c, t):
                A, m = c
                A = tick(p, A, Noise(kp, t), zw, sg)
                return (A, bt.update_memory(m, A)), None
            (A, m), _ = jax.lax.scan(body, (A, m), jnp.arange(BURN))
            return A, m
        return jax.lax.map(one, (P, k, sig))

    def _run(self, P, A, m, key, t0, uw, sig):
        bt, fold = self.bt, jax.random.fold_in

        def one(args):
            p, A, m, kk, t0, uw, sg = args
            kp = fold(kk, _ST_PROC)

            def rec(A, m):
                d = bt.split(m)
                return self.obs(A, m), d["table"][:, NF:], d["globals"]

            def body(c, w):
                A, m, t = c
                A = tick(p, A, Noise(kp, t), w, sg)
                m = bt.update_memory(m, A)
                return (A, m, t + 1), rec(A, m)
            r0 = rec(A, m)
            (A, m, _), outs = jax.lax.scan(body, (A, m, t0), uw)
            cat = lambda a, b: jnp.concatenate([a[None], b], 0)
            return tuple(cat(a, b) for a, b in zip(r0, outs)) + (A, m)
        return jax.lax.map(one, (P, A, m, key, t0, uw, sig))


def dyn_keys(k_init):
    return jax.vmap(lambda k: jax.random.fold_in(k, _ST_DYN))(k_init)


# ----------------------------------------------------------------------------- level-1/2 readouts
def unpack_objects(yo):
    """yo (..., 144) -> dict of (..., K) arrays: present, mass, rg, speed, cy, cx, vy, vx."""
    S = np.asarray(yo, float).reshape(yo.shape[:-1] + (K, NF))
    pres = S[..., 0] > 0.5
    cx = (np.arctan2(S[..., 4], S[..., 3]) * W / (2 * np.pi)) % W
    cy = (np.arctan2(S[..., 6], S[..., 5]) * H / (2 * np.pi)) % H
    return {"present": pres, "mass": S[..., 1], "rg": S[..., 7], "speed": np.hypot(S[..., 10], S[..., 11]),
            "cy": cy, "cx": cx, "vy": S[..., 11], "vx": S[..., 10]}


def population(obs):
    """Level 2 (declared statistic of the observation): (count, tracked mass, mean speed) of the
    objects readout; obs (..., 336) -> (..., 3). Pointwise in time (phi.population without the fusion EMA)."""
    d = unpack_objects(np.asarray(obs)[..., NC:NC + NO])
    pr = d["present"]
    n = pr.sum(-1).astype(float)
    mass = np.where(pr, d["mass"], 0.0).sum(-1)
    sp = np.where(pr, d["speed"], 0.0).sum(-1) / np.maximum(n, 1.0)
    return np.stack([n, mass, sp], -1)


def coarse(obs):
    return np.asarray(obs)[..., :NC]


# ----------------------------------------------------------------------------- wind programs
# Built from agent-visible information only (the last revealed observation). Dense form (H, NW);
# coefficient index = comp * G * G + row * G + col, comp 0 = y, 1 = x (wind.wind_field layout).
T_IN = 4


def heaviest_group(yc):
    """(i0, j0): top-left block of the 2 x 2 group (periodic) with the largest sum of the block mean
    of A_sum^2 (coarse coordinates 128..191)."""
    m2 = np.asarray(yc, float)[2 * G * G:3 * G * G].reshape(G, G)
    s = m2 + np.roll(m2, -1, 0) + np.roll(m2, -1, 1) + np.roll(np.roll(m2, -1, 0), -1, 1)
    i, j = np.unravel_index(int(np.argmax(s)), s.shape)
    return int(i), int(j)


def regional_push(yc, angle, C, sigma_w=SIGMA_W, H=16, T_in=T_IN):
    """Class (d): uniform force in direction angle on the 4 x 4 blocks around the heaviest 2 x 2 group,
    ticks 0..T_in-1, C nats in all (C / T_in per tick): f = sigma_w sqrt(C / (8 T_in))."""
    i0, j0 = heaviest_group(yc)
    f = sigma_w * np.sqrt(C / (8.0 * T_in))
    n = np.array([np.sin(angle), np.cos(angle)])          # (y, x)
    U = np.zeros((H, 2, G, G))
    rows = [(i0 + d) % G for d in (-1, 0, 1, 2)]
    cols = [(j0 + d) % G for d in (-1, 0, 1, 2)]
    for t in range(min(T_in, H)):
        for c in range(2):
            U[t, c][np.ix_(rows, cols)] = f * n[c]
    return U.reshape(H, NW)


def aimed_push(yo, C, sigma_w=SIGMA_W, H=16, T_in=T_IN):
    """Class (c): actuation/programs.wind_aimed from the revealed objects readout: target = fastest
    body with speed >= 0.6 px/tick (else the heaviest), force along its left normal on the 2 x 2 blocks
    around its extrapolated path, C nats in all. Returns (U (H, NW), found)."""
    d = unpack_objects(np.asarray(yo)[None])
    pres = np.flatnonzero(d["present"][0])
    U = np.zeros((H, 2, G, G))
    if pres.size == 0:
        return U.reshape(H, NW), False
    sp = d["speed"][0][pres]
    s = pres[int(np.argmax(sp))] if sp.max() >= 0.6 else pres[int(np.argmax(d["mass"][0][pres]))]
    p0 = np.array([d["cy"][0, s], d["cx"][0, s]])
    v = np.array([d["vy"][0, s], d["vx"][0, s]])
    spd = float(np.hypot(*v))
    u = v / spd if spd > 1e-6 else np.array([0.0, 1.0])
    n = np.array([u[1], -u[0]])
    f = sigma_w * np.sqrt(C / (2.0 * T_in))
    b = H_PX // G
    for t in range(min(T_in, H)):
        p = p0 + v * (t + 0.5)
        i0 = int(np.floor((p[0] - (b - 1) / 2) / b)) % G
        j0 = int(np.floor((p[1] - (b - 1) / 2) / b)) % G
        rows, cols = [i0, (i0 + 1) % G], [j0, (j0 + 1) % G]
        for c in range(2):
            U[t, c][np.ix_(rows, cols)] = f * n[c]
    return U.reshape(H, NW), True


H_PX = H


def nats_of(U, sigma_w=SIGMA_W):
    return 0.5 * float((np.asarray(U) ** 2).sum()) / sigma_w ** 2
