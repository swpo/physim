"""physim2.world_ring -- the public side of the ring exam world (a cheap, closed-form mechanics world).

Level 0 (public law, hidden theta = (D, gamma, c)): a ring of 24 sites,
    x(t+1) = A x(t) + u(t) + 0.3 xi(t),   xi ~ N(0, I)
    A = (1 - gamma) (I - D Lap + c Adv)            diffusion D, damping gamma, advection c
    x(0) ~ the stationary law of the same theta (no burn-in needed).
Input u: all 24 sites, a shift before the Gaussian noise; cost |u|^2 / (2 * 0.3^2) nats per tick.
Level 1 (observed): the 6 block sums of 4 neighbouring sites, plus observation noise N(0, 0.3^2).
Level 2 (a declared statistic of level 1): (total, cos mode 1, sin mode 1) of the 6 values.
Prior (public): D ~ U(0.05, 0.25), gamma ~ U(0.02, 0.12), c ~ U(-0.3, 0.3).

The module gives the same interface as every physim2 world: constants, level(), scales(), build_world(),
nats_budget(), program_mix(), prior_sample(), viable() and Simulator (your own copy of the law, run at
any theta with your own noise).
"""
from __future__ import annotations

import math

import numpy as np

from . import _vendor_path as _vp

_vp.add("vw1")
import jax  # noqa: E402
import jax.numpy as jnp  # noqa: E402

import vw  # noqa: E402
from vw.harness import ProgramMix, blind_random, no_input, program_dense  # noqa: E402
from vw.nats import NatsBudget  # noqa: E402

NAME = "ring"
N, G, SIGMA, R_OBS = 24, 6, 0.3, 0.3
THETA_NAMES = ("D", "gamma", "c")
PRIOR_LO = np.array([0.05, 0.02, -0.3])
PRIOR_HI = np.array([0.25, 0.12, 0.3])
PRIOR_MEAN = (PRIOR_LO + PRIOR_HI) / 2
N_IN, N_OBS = N, G
LEVEL_DIMS = {1: G, 2: 3}
BURN_IN = 0
SIGMA_IN = SIGMA
IN_LO, IN_HI = -3.0, 3.0
TICK_CAP, EPISODE_CAP = 2.0, 8.0
P_PREFIX = 16
QUERIES = {1: [1, 2, 4, 8, 16], 2: [16, 32]}
CPU_S_PER_MEMBER_TICK = 2e-5         # order of magnitude, one core, batched

_I = np.eye(N)
_LAP = 2 * _I - np.roll(_I, 1, 0) - np.roll(_I, -1, 0)
_ADV = (np.roll(_I, 1, 0) - np.roll(_I, -1, 0)) / 2
_CMAT = np.kron(np.eye(G), np.ones((1, N // G)))
_ang = 2 * np.pi * np.arange(G) / G
_L2 = np.stack([np.ones(G), np.cos(_ang), np.sin(_ang)])


def level(l: int, obs):
    """Level-l coordinates of observations (..., n_obs): level 1 = the observation, level 2 = 3 modes."""
    obs = np.asarray(obs)
    return obs if int(l) == 1 else obs @ _L2.T


def scales() -> dict:
    """Public coordinate scales (from the prior predictive stationary law), used by the score."""
    return {1: np.full(G, 1.5), 2: np.array([4.3, 2.7, 2.7])}


def _theta_dict(th):
    return {k: jnp.asarray(float(v)) for k, v in zip(THETA_NAMES, th)}


def _A(p):
    return (1 - p["gamma"]) * (jnp.eye(N) - p["D"] * jnp.asarray(_LAP) + p["c"] * jnp.asarray(_ADV))


def _chol_stat(p):
    k = 2 * jnp.pi * jnp.arange(N) / N
    lam2 = (1 - p["gamma"]) ** 2 * ((1 - 2 * p["D"] * (1 - jnp.cos(k))) ** 2 + (p["c"] * jnp.sin(k)) ** 2)
    s = SIGMA ** 2 / (1 - lam2)
    d = jnp.arange(N)
    col = (s[None, :] * jnp.cos(k[None, :] * d[:, None])).sum(1) / N
    idx = (jnp.arange(N)[:, None] - jnp.arange(N)[None, :]) % N
    S = col[idx]
    return jnp.linalg.cholesky((S + S.T) / 2)


def _spec() -> vw.WorldSpec:
    def init(p, key):
        return _chol_stat(p) @ jax.random.normal(key, (N,))

    def step_xi(p, x, xi, u):
        return _A(p) @ x + u + SIGMA * xi
    lev = vw.Level(init=init, step_xi=step_xi, noise_dim=N, input_dim=N, params=_theta_dict(PRIOR_MEAN),
                   conserved={}, name="ring3")
    C = jnp.asarray(_CMAT)
    return vw.WorldSpec(base=lev, chain=(vw.CoarseGrain.of(lambda x: C @ x, name="blocks"),),
                        inport=vw.InputPort(admissible=vw.Admissible(lo=IN_LO, hi=IN_HI), in_map=tuple(range(N))),
                        outport=vw.ObservePort(noise=R_OBS, out_map=tuple(range(G)), out_sign=(1.0,) * G),
                        replay="initial", name="ring3")


def build_world(theta, burn_in=None) -> vw.World:
    """The world at parameters theta (the hidden side builds the real world with this same function)."""
    return vw.World(_spec(), 0, params=_theta_dict(theta))


def nats_budget(total=None) -> NatsBudget:
    return NatsBudget.isotropic(N, SIGMA, tick=TICK_CAP, episode=EPISODE_CAP, total=total,
                                note="u is a shift before N(0, 0.3^2 I) process noise on every site")


def prior_sample(rng, n: int) -> np.ndarray:
    return PRIOR_LO + (PRIOR_HI - PRIOR_LO) * rng.random((int(n), len(THETA_NAMES)))


def viable(thetas, seed=0) -> np.ndarray:
    """The public selection rule applied to hidden draws (none in this world)."""
    return np.ones(len(np.atleast_2d(thetas)), bool)


# ----------------------------------------------------------------------------- exam program classes
def _block_push(block, sign, nats):
    a = math.sqrt(2 * nats * SIGMA ** 2 / 4) * (1 - 1e-9)
    return {int(j): float(sign * a) for j in range(4 * block, 4 * block + 4)}


def _aimed(rng, history, H_, nats_left):
    """(c) oppose the largest block anomaly of the last revealed frame at the tick cap."""
    o = history[-1]
    dev = o - o.mean()
    b = int(np.argmax(np.abs(dev)))
    prog, left, t = [], nats_left, 0
    while left >= TICK_CAP - 1e-9 and t < H_:
        prog.append((t, _block_push(b, -np.sign(dev[b]) or 1.0, TICK_CAP)))
        left -= TICK_CAP
        t += 1
    return prog


def _regional(rng, history, H_, nats_left):
    """(d) a random 2-block region pushed uniformly at the tick cap until the episode budget."""
    b0, sign = int(rng.integers(G)), float(rng.choice([-1.0, 1.0]))
    a = math.sqrt(2 * TICK_CAP * SIGMA ** 2 / 8) * (1 - 1e-9)
    sites = [(4 * b0 + j) % N for j in range(8)]
    prog, left, t = [], nats_left, 0
    while left >= TICK_CAP - 1e-9 and t < H_:
        prog.append((t, {s: sign * a for s in sites}))
        left -= TICK_CAP
        t += 1
    return prog


def program_mix() -> ProgramMix:
    """The public distribution of exam test programs: classes 'a' none, 'b' blind random, 'c' aimed from
    the revealed history, 'd' regional; equal shares. Each class is f(rng, history, H, nats_left) ->
    [(t, {site: value})]."""
    return ProgramMix({"a": no_input, "b": blind_random(nats_budget(), k=2, rate=0.25), "c": _aimed, "d": _regional})


def draw_program(cls: str, rng, history, H: int) -> np.ndarray:
    """A dense (H, n_in) test program of class cls built from the revealed history (P + 1, n_obs)."""
    return program_dense(program_mix().classes[cls](rng, np.asarray(history), H, EPISODE_CAP), H, N_IN)


# ----------------------------------------------------------------------------- the agent's simulator
class Simulator:
    """Your own copy of the public law: any theta, your own noise (never the real world's).

    episodes(thetas, seed, P, H, classes=None) -> dict
        exam-shaped episodes, one per row of thetas (B, 3): start from the initial law, P ticks without
        input, then an H-tick test program of the public mix built from o(0..P) (class per member from
        `classes`, default uniform over the mix). obs (B, P + H + 1, n_obs), U (B, P + H, n_in), cls (B,).
    free_run(thetas, seed, T) -> obs (B, T + 1, n_obs) without input.
    member_ticks counts simulated member-ticks."""

    def __init__(self, burn_in=None, chunk=None):
        self.w = build_world(PRIOR_MEAN)
        w = self.w

        def start(p, ki, kd, A):
            c = jax.vmap(w._init_member, in_axes=(None, 0, 0))(p, ki[None], kd[None])
            c, rec = w._rollout_fn(p, c, A[:, None], ("obs",))
            return c, rec["obs"][:, 0]

        def cont(p, c, A):
            c, rec = w._rollout_fn(p, c, A[:, None], ("obs",))
            return c, rec["obs"][:, 0]
        self._start = jax.jit(jax.vmap(start))
        self._cont = jax.jit(jax.vmap(cont))
        self.member_ticks = 0

    def _keys(self, seed, B):
        base = jax.random.key(int(seed) % (2 ** 31))
        k = jax.random.split(base, 2 * B)
        return k[:B], k[B:]

    def _params(self, thetas):
        th = np.atleast_2d(np.asarray(thetas, float))
        return {k: jnp.asarray(th[:, i]) for i, k in enumerate(THETA_NAMES)}, len(th)

    def episodes(self, thetas, seed, P=P_PREFIX, H=32, classes=None) -> dict:
        p, B = self._params(thetas)
        ki, kd = self._keys(seed, B)
        rng = np.random.default_rng([int(seed), 11])
        mix = program_mix()
        cls = np.asarray(rng.choice(mix.names, size=B) if classes is None else classes)
        c, o1 = self._start(p, ki, kd, jnp.zeros((B, P, N_IN)))
        o1 = np.asarray(o1)
        U = np.zeros((B, H, N_IN))
        for b in range(B):
            U[b] = draw_program(str(cls[b]), np.random.default_rng([int(seed), 12, b]), o1[b], H)
        _, o2 = self._cont(p, c, jnp.asarray(U))
        self.member_ticks += B * (P + H)
        obs = np.concatenate([o1, np.asarray(o2)[:, 1:]], 1)
        return {"obs": obs, "U": np.concatenate([np.zeros((B, P, N_IN)), U], 1), "cls": cls}

    def free_run(self, thetas, seed, T: int) -> np.ndarray:
        p, B = self._params(thetas)
        ki, kd = self._keys(seed, B)
        _, o = self._start(p, ki, kd, jnp.zeros((B, int(T), N_IN)))
        self.member_ticks += B * int(T)
        return np.asarray(o)
