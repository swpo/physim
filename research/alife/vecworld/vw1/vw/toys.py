"""vw.toys -- small nonlinear test worlds.

mass_ring   non-negative matter on a ring: a pooling kick (a source removes at most the matter
            present; the sinks receive exactly what was removed, in proportion), diffusion and
            mass-conserving random fluxes between neighbours. Total mass is conserved for every
            input, admissible or not: inputs move matter, never create it.
block_sums  memoryless coarse-graining: sums over G equal blocks.
peak_tracker_np  an algorithmic tracker in numpy (argmax with hysteresis and an age counter):
            an opaque, non-differentiable CoarseGrain with memory, for vw.opaque.
"""
from __future__ import annotations

import jax
import jax.numpy as jnp
import numpy as np

from .core import CoarseGrain, Level
from .ports import Admissible, InputPort, ObservePort
from .world import WorldSpec


def pool_kick(x, u):
    """Move matter: sources (u < 0) give min(-u, x); sinks (u > 0) share the pooled matter in
    proportion to u. Conserves sum(x) to round-off for every u and keeps x >= 0."""
    take = jnp.where(u < 0, jnp.minimum(-u, jnp.maximum(x, 0.0)), 0.0)
    w = jnp.where(u > 0, u, 0.0)
    ws = w.sum()
    has = ws > 0
    take = jnp.where(has, take, 0.0)
    give = take.sum() * w / jnp.where(has, ws, 1.0)
    return x - take + give


def additive_kick(x, u):
    return x + u


def mass_ring_level(n: int = 32, D: float = 0.15, sigma: float = 1.0, kick=pool_kick, name: str = "mass-ring") -> Level:
    def init(p, key):
        k1, k2 = jax.random.split(key)
        c = jax.random.uniform(k1, (), minval=0.0, maxval=n)
        i = jnp.arange(n)
        d = jnp.minimum(jnp.abs(i - c), n - jnp.abs(i - c))
        return 0.05 + 2.0 * jnp.exp(-d ** 2 / 8.0) + 0.02 * jax.random.uniform(k2, (n,))

    def step(p, x, nz, u):
        x = kick(x, u)
        x = x + D * (jnp.roll(x, 1) + jnp.roll(x, -1) - 2 * x)
        f = 0.25 * jnp.tanh(sigma * nz.normal((n,))) * jnp.minimum(x, jnp.roll(x, -1))   # flux i -> i+1
        return x - f + jnp.roll(f, 1)

    return Level(init=init, step=step, input_dim=n, conserved={"mass": jnp.sum}, name=name)


def block_sums(n: int, G: int, name: str = "blocks") -> CoarseGrain:
    b = n // G
    return CoarseGrain.of(lambda x: x.reshape(G, b).sum(1), name=name)


def mass_ring(n: int = 32, G: int = 8, inputs: Admissible = Admissible(k=4, lo=-1.0, hi=1.0, total=2.0, zero_sum=True),
              obs_noise: float = 0.05, kick=pool_kick, **kw) -> WorldSpec:
    return WorldSpec(base=mass_ring_level(n, kick=kick, **kw), chain=(block_sums(n, G),),
                     inport=InputPort(admissible=inputs), outport=ObservePort(noise=obs_noise), name="mass-ring")


# ----------------------------------------------------------------------------- numpy tracker
def _circ(a, b, n):
    d = abs(a - b) % n
    return min(d, n - d)


def peak_init_np(x):
    return np.array([float(np.argmax(x)), 0.0])


def peak_update_np(m, x, jump: int = 3):
    n = x.shape[0]
    pos, age = float(m[0]), float(m[1])
    c = int(np.argmax(x))
    if _circ(c, int(pos), n) <= jump:
        return np.array([float(c), age + 1.0])
    return np.array([pos, age + 1.0]) if x[int(pos)] > 0.5 * x[c] else np.array([float(c), 0.0])


def peak_phi_np(x, m):
    n = x.shape[0]
    pos = int(m[0])
    return np.array([np.cos(2 * np.pi * pos / n), np.sin(2 * np.pi * pos / n), x[pos], m[1]])
