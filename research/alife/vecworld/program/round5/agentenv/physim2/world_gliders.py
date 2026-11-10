"""physim2.world_gliders -- the public side of the gliders exam world (Flow-Lenia gliders with a wind channel).

Level 0 (public law, 4 hidden numbers): a field A of 2 channels on a 128 x 128 torus (Flow-Lenia, world
"A_gliders"). Matter is conserved and moves along a flow computed from 20 convolution kernels and growth
functions; localised moving bodies ("gliders") form, drift at about 1.6 px per tick, and sometimes merge or
split. One tick = 20 substeps; every substep adds Gaussian noise (std 0.5) to the flow.
Hidden parameters (theta), applied to the public kernel and growth parameters:
    lR      scales every kernel radius:                (R + 15) <- lR (R + 15)
    dm_00   shifts the growth centres of kernel group channel 0 -> channel 0, in units of each kernel's width
    ls_00   scales the growth widths of the same group
    lh      scales every growth height
Input (the "wind"): 128 coefficients u = one force per 16-px block and component, index
comp * 64 + row * 8 + col with comp 0 = y, 1 = x. The world applies u + eta with eta ~ N(0, 0.05^2 I) drawn
every tick (also when u = 0), smoothed in space (Gaussian, 8 px) and added to the flow for the whole tick: a
force f moves matter by about 4 f px per tick. Cost |u|^2 / (2 * 0.05^2) nats per tick.
Level 1 (observed, 336 numbers per tick, rounded to 0.001):
    [0:192]    the coarse view on the 8 x 8 grid of 16-px blocks: block means of channel 0 (64), of channel 1
               (64), and of (A0 + A1)^2 (64); index = which * 64 + row * 8 + col. THIS PART IS SCORED as level 1.
    [192:336]  the objects readout: 12 slots x 12 features (present, mass, fraction in channel 1, cos and sin of
               x, cos and sin of y on the torus, radius of gyration, two shape numbers, vx, vy) from a public
               tracker of the bodies; empty slots are zero. Not scored itself.
Level 2 (a declared statistic of the objects readout, scored): (number of bodies, tracked mass, mean speed).
Episodes start from the public initial law (10 random patches) followed by 50 ticks of burn-in (not shown).

The module gives the same interface as every physim2 world: constants, level(), scales(), build_world(),
nats_budget(), program_mix(), draw_program(), prior_sample(), viable() and Simulator. The law itself is in
physim2/_vendor (flowlenia_jax.py, wind.py, gworld.py; coarse-grainings in phi.py and vw/objects.py).
"""
from __future__ import annotations

import json
import math
import os

import numpy as np

from . import _vendor_path as _vp

_vp.add("program/track2/gliders_exam", "program/track2/actuation", "vw1/port", "vw1")
import _paths  # noqa: E402,F401
import jax  # noqa: E402
import jax.numpy as jnp  # noqa: E402

import vw  # noqa: E402
from vw.harness import ProgramMix, program_dense  # noqa: E402
from vw.nats import NatsBudget  # noqa: E402
from vw.world import make_key, member_keys  # noqa: E402
import aworld as AW  # noqa: E402
import gworld as GW  # noqa: E402
import phi as PH  # noqa: E402

NAME = "gliders"
_GE = os.path.join(_vp.VEC, "program", "track2", "gliders_exam", "results")
_PR = json.load(open(os.path.join(_GE, "prior.json")))
_SC = np.load(os.path.join(_GE, "scales.npz"))
THETA_NAMES = tuple(_PR["names"])
PRIOR_LO, PRIOR_HI = np.array(_PR["lo"], float), np.array(_PR["hi"], float)
PRIOR_MEAN = (PRIOR_LO + PRIOR_HI) / 2
NC, NO, G = GW.NC, GW.NO, GW.G
N_IN, N_OBS = GW.NW, GW.NC + GW.NO
LEVEL_DIMS = {1: NC, 2: 3}
BURN_IN = GW.BURN
SIGMA_IN = GW.SIGMA_W
IN_LO, IN_HI = -1.0, 1.0
TICK_CAP, EPISODE_CAP = 100.0, 400.0
C_AIM, C_REG = 200.0, 300.0
P_PREFIX = 16
QUERIES = {1: [1, 2, 4, 8, 16], 2: [8, 16]}
QUANTUM = 1e-3
CPU_S_PER_MEMBER_TICK = 0.15
VIABILITY_NOTE = ("A draw is kept only if it passes the public viability rule `W.viable` (one run of 50 + 100 ticks "
                  "without input: finite, 4 to 12 bodies on average and never fewer than 2, median speed at least "
                  "0.5 px per tick); about 92% of the box passes.")


def level(l: int, obs):
    obs = np.asarray(obs)
    return obs[..., :NC] if int(l) == 1 else GW.population(obs)


def scales() -> dict:
    return {1: np.asarray(_SC["level1"], float), 2: np.asarray(_SC["level2"], float)}


def _theta_dict(th) -> dict:
    return {k: float(v) for k, v in zip(THETA_NAMES, np.asarray(th, float))}


def build_world(theta, burn_in=None) -> vw.World:
    """The world at parameters theta (gliders_exam/pilot.build_world: wind input, coarse + objects observation,
    quantum 0.001, burn-in 50 ticks, replay 'initial'); the hidden side builds the real world with this function."""
    params = GW.theta_to_params(_theta_dict(theta))
    lev = GW.level(SIGMA_IN, params)
    pc = PH.phi_coarse(GW.CFG, G)
    po, _, _ = PH.phi_objects_jax("A_gliders")
    spec = vw.WorldSpec(base=lev, chain=(PH.pair(pc, po),),
                        inport=vw.InputPort(admissible=vw.Admissible(k=None, lo=IN_LO, hi=IN_HI), in_map=tuple(range(N_IN))),
                        outport=vw.ObservePort(noise=0.0, quantum=QUANTUM, out_map=tuple(range(N_OBS)),
                                               out_sign=tuple([1.0] * N_OBS)),
                        burn_in=BURN_IN, replay="initial", name="gliders_wind_hidden4",
                        public_notes="wind input: 128 coefficients (2 x 8 x 8), cost |u|^2 / (2 sigma_w^2) nats")
    return AW.MapWorld(spec, world_seed=0, params=params)


def nats_budget(total=None) -> NatsBudget:
    return NatsBudget.isotropic(N_IN, SIGMA_IN, tick=TICK_CAP, episode=EPISODE_CAP, total=total,
                                note="wind coefficients enter as a shift before N(0, sigma_w^2 I) actuation noise")


def prior_sample(rng, n: int) -> np.ndarray:
    """Uniform draws from the box (the viability rule is not applied here; see viable())."""
    return PRIOR_LO + (PRIOR_HI - PRIOR_LO) * rng.random((int(n), len(THETA_NAMES)))


def viable(thetas, seed=0) -> np.ndarray:
    """The public viability rule applied to the hidden draw (viab_joint.viability): one member per theta,
    50 burn-in + 100 free ticks. Costs 150 member-ticks per theta."""
    import viab_joint as VJ
    th = np.atleast_2d(np.asarray(thetas, float))
    rows, _ = VJ.viability(list(THETA_NAMES), list(th), member_keys(make_key(771, int(seed) % (2 ** 31)), len(th)))
    return np.array([r["viable"] for r in rows], bool)


# ----------------------------------------------------------------------------- exam program classes
def _dense_to_prog(U):
    return [(int(t), {int(j): float(U[t, j]) for j in np.flatnonzero(U[t])}) for t in range(U.shape[0]) if np.any(U[t])]


def _none(rng, hist, H, left):
    return []


def _blind(rng, hist, H, left, k=8, rate=0.25, cmax=50.0):
    """(b) 8 random coefficients at random ticks (rate 0.25), U(0, 50] nats each."""
    U = np.zeros((H, N_IN))
    for t in range(H):
        if rng.random() >= rate or left <= 1e-6:
            continue
        idx = rng.choice(N_IN, size=k, replace=False)
        v = rng.standard_normal(k)
        c_t = min(rng.uniform(0, cmax), left)
        v *= math.sqrt(2 * c_t * SIGMA_IN ** 2 / float((v ** 2).sum())) * (1 - 1e-9)
        v = np.clip(v, -0.99, 0.99)
        U[t, idx] = v
        left -= GW.nats_of(v)
    return _dense_to_prog(U)


def _aimed(rng, hist, H, left):
    """(c) 200 nats over 4 ticks on the 2 x 2 blocks around the fastest body of the last revealed frame,
    along its left normal (gworld.aimed_push)."""
    U, _ = GW.aimed_push(hist[-1, NC:NC + NO], min(C_AIM, left), SIGMA_IN, H=H)
    return _dense_to_prog(U)


def _regional(rng, hist, H, left):
    """(d) 300 nats over 4 ticks on the 4 x 4 blocks around the heaviest 2 x 2 group, random direction
    (gworld.regional_push)."""
    U = GW.regional_push(hist[-1, :NC], rng.uniform(0, 2 * np.pi), min(C_REG, left), SIGMA_IN, H=H)
    return _dense_to_prog(U)


def program_mix() -> ProgramMix:
    """The public distribution of exam test programs (the round-3 pilot's mix), equal shares; each class is
    f(rng, history, H, nats_left) -> [(t, {coefficient: value})]."""
    return ProgramMix({"a": _none, "b": _blind, "c": _aimed, "d": _regional})


def draw_program(cls: str, rng, history, H: int) -> np.ndarray:
    """A dense (H, n_in) test program of class cls built from the revealed history (P + 1, n_obs)."""
    return program_dense(program_mix().classes[cls](rng, np.asarray(history, float), H, EPISODE_CAP), H, N_IN)


# ----------------------------------------------------------------------------- the agent's simulator
def quantize(y):
    return QUANTUM * np.round(np.asarray(y, float) / QUANTUM)


class Simulator:
    """Your own copy of the public law: any theta per member, your own noise (never the real world's).

    episodes(thetas, seed, P, H, classes=None) -> dict
        exam-shaped episodes, one per row of thetas (B, 4): initial law + 50 burn-in ticks, P ticks without
        input, then an H-tick test program of the public mix built from o(0..P). obs (B, P + H + 1, 336)
        (rounded like the real observations), U (B, P + H, 128), cls (B,).
    free_run(thetas, seed, T) -> obs (B, T + 1, 336) without input.
    Members run one after another on one core (jax.lax.map), `chunk` members per compiled call; the first call
    of each shape compiles (tens of seconds). To use several cores, run several processes with different seeds.
    member_ticks counts simulated member-ticks, burn-in included (about 0.15 CPU-seconds each)."""

    def __init__(self, burn_in=None, chunk: int = 8):
        self.RN = GW.Runner()
        self.chunk = int(chunk)
        self.member_ticks = 0

    def _batch(self, th, seed, s):
        c = self.chunk
        pad = np.concatenate([th, np.repeat(th[-1:], c - len(th), 0)], 0) if len(th) < c else th
        P = GW.stack_params([GW.theta_to_params(_theta_dict(t)) for t in pad])
        k = member_keys(make_key(4242, int(seed) % (2 ** 31), int(s)), c)
        return P, k, jnp.full((c,), SIGMA_IN)

    def episodes(self, thetas, seed, P=P_PREFIX, H=16, classes=None) -> dict:
        th = np.atleast_2d(np.asarray(thetas, float))
        B, c = len(th), self.chunk
        rng = np.random.default_rng([int(seed), 11])
        names = program_mix().names
        cls = np.asarray(rng.choice(names, size=B) if classes is None else classes)
        OBS = np.zeros((B, P + H + 1, N_OBS), np.float32)
        UU = np.zeros((B, P + H, N_IN), np.float32)
        for s in range(0, B, c):
            nb = min(c, B - s)
            Pp, k, sig = self._batch(th[s:s + c], seed, s)
            A, m = self.RN.init_burn(Pp, k, sig)
            kd = GW.dyn_keys(k)
            y1, _, _, A, m = self.RN.run(Pp, A, m, kd, jnp.zeros((c,), jnp.int64), jnp.zeros((c, P, N_IN)), sig)
            y1 = quantize(np.asarray(y1)[:nb])
            U = np.zeros((c, H, N_IN))
            for b in range(nb):
                U[b] = draw_program(str(cls[s + b]), np.random.default_rng([int(seed), 12, s + b]), y1[b], H)
            y2, _, _, _, _ = self.RN.run(Pp, A, m, kd, jnp.full((c,), P, jnp.int64), jnp.asarray(U), sig)
            OBS[s:s + nb] = np.concatenate([y1, quantize(np.asarray(y2)[:nb])[:, 1:]], 1)
            UU[s:s + nb, P:] = U[:nb]
            self.member_ticks += c * (BURN_IN + P + H)
        return {"obs": OBS.astype(np.float64), "U": UU.astype(np.float64), "cls": cls}

    def free_run(self, thetas, seed, T: int) -> np.ndarray:
        th = np.atleast_2d(np.asarray(thetas, float))
        B, c = len(th), self.chunk
        out = np.zeros((B, int(T) + 1, N_OBS))
        for s in range(0, B, c):
            nb = min(c, B - s)
            Pp, k, sig = self._batch(th[s:s + c], seed, s)
            A, m = self.RN.init_burn(Pp, k, sig)
            y, _, _, _, _ = self.RN.run(Pp, A, m, GW.dyn_keys(k), jnp.zeros((c,), jnp.int64), jnp.zeros((c, int(T), N_IN)), sig)
            out[s:s + nb] = quantize(np.asarray(y)[:nb])
            self.member_ticks += c * (BURN_IN + int(T))
        return out
