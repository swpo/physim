"""vw.opaque -- declared wrappers for opaque (non-JAX, non-differentiable) blocks.

An opaque block is ordinary host code (numpy, scipy, an algorithmic tracker...) that the world
calls through jax.pure_callback with DECLARED result shapes and dtypes. The wrapped block is a
normal Level or CoarseGrain: it composes with every operator, runs inside jit, scan and vmap, and
its randomness still comes from the Noise key (passed to the host as raw key data, from which the
host seeds numpy), so determinism by key is kept.

What it gives up, declared by opaque=True / differentiable=False:
  * autodiff: no JVP/VJP through the callback; certificates.fisher refuses such worlds
    (NotDifferentiable) and jax.grad raises;
  * compilation: XLA cannot fuse or optimise across the call; every tick is a host round trip;
  * batching: vmap_method='sequential' (default) loops over members on the host; batched=True
    ('expand_dims') hands the host one call with a leading batch axis, but the host code must then
    be vectorised itself (and accept a size-1 batch axis on unbatched arguments);
  * accelerators: on a GPU every call copies device -> host -> device;
  * purity is a promise: the host function must be a deterministic function of its arguments
    (JAX may cache, repeat or drop calls), so no hidden state between calls -- tracker memory must
    be passed in and out as a fixed-shape array.
"""
from __future__ import annotations

from typing import Callable, Optional

import jax
import jax.numpy as jnp
import numpy as np

from .core import CoarseGrain, Level


def _vm(batched: bool) -> str:
    return "expand_dims" if batched else "sequential"


def host_level(init_fn: Callable, step_fn: Callable, state_shape, input_dim: int, dtype=np.float64,
               batched: bool = False, conserved: Optional[dict] = None, name: str = "host-level") -> Level:
    """Wrap host functions as a Level.
    init_fn(key_data uint32 array) -> state (numpy, shape state_shape)
    step_fn(state, key_data, u) -> state
    key_data is jax.random.key_data of the key the world passes; seed numpy from it."""
    spec = jax.ShapeDtypeStruct(tuple(state_shape), dtype)

    def init(params, key):
        return jax.pure_callback(lambda kd: np.asarray(init_fn(np.asarray(kd)), dtype), spec,
                                 jax.random.key_data(key), vmap_method=_vm(batched))

    def step(params, x, noise, u):
        return jax.pure_callback(lambda xx, kd, uu: np.asarray(step_fn(np.asarray(xx), np.asarray(kd), np.asarray(uu)), dtype),
                                 spec, x, jax.random.key_data(noise.rng()), u, vmap_method=_vm(batched))

    return Level(init=init, step=step, input_dim=int(input_dim), params=None, conserved=dict(conserved or {}),
                 opaque=True, name=name)


def host_coarse_grain(phi_fn: Callable, out_shape, init_memory_fn: Optional[Callable] = None,
                      update_memory_fn: Optional[Callable] = None, memory_shape=None, dtype=np.float64,
                      batched: bool = False, name: str = "host-phi") -> CoarseGrain:
    """Wrap host functions as a CoarseGrain (e.g. an algorithmic tracker).
    phi_fn(x, m) -> x' (shape out_shape); init_memory_fn(x) -> m; update_memory_fn(m, x) -> m
    (m has the fixed shape memory_shape). Memoryless: phi_fn(x, None)."""
    ospec = jax.ShapeDtypeStruct(tuple(out_shape), dtype)
    has = init_memory_fn is not None
    vm = _vm(batched)
    if has:
        mspec = jax.ShapeDtypeStruct(tuple(memory_shape), dtype)

        def phi(x, m):
            return jax.pure_callback(lambda xx, mm: np.asarray(phi_fn(np.asarray(xx), np.asarray(mm)), dtype),
                                     ospec, x, m, vmap_method=vm)

        def m_init(x):
            return jax.pure_callback(lambda xx: np.asarray(init_memory_fn(np.asarray(xx)), dtype), mspec, x,
                                     vmap_method=vm)

        def m_upd(m, x):
            return jax.pure_callback(lambda mm, xx: np.asarray(update_memory_fn(np.asarray(mm), np.asarray(xx)), dtype),
                                     mspec, m, x, vmap_method=vm)
        return CoarseGrain(phi=phi, init_memory=m_init, update_memory=m_upd, opaque=True, name=name)

    def phi0(x, m):
        return jax.pure_callback(lambda xx: np.asarray(phi_fn(np.asarray(xx), None), dtype), ospec, x, vmap_method=vm)
    return CoarseGrain(phi=phi0, opaque=True, name=name)


def is_differentiable(obj) -> bool:
    """True if a Level, CoarseGrain or WorldSpec has derivatives on its observed path."""
    return bool(getattr(obj, "differentiable", False))


__all__ = ["host_level", "host_coarse_grain", "is_differentiable", "jnp"]
