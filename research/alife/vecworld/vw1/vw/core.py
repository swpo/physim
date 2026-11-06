"""vw.core -- the module types of a supervenient world: Noise, Level, CoarseGrain.

Level        an open stochastic dynamical system L = (X, U, A, F, mu). The implementation type
             holds two pure functions of explicit arguments:
                 init(params, key)            -> x          (a draw from mu)
                 step(params, x, noise, u)    -> x'         (a draw from F(x, u))
             x is any pytree of arrays (its shapes are the state space X), u is a flat vector of
             length input_dim (the actuator space U; u = 0 means "no input"), and `noise` is a
             counter-based noise source (below). All randomness of the law comes from `noise`.
             The admissible set A is not part of the level: it is declared on the InputPort, because
             it is an information constraint on the agent, not physics. How u acts on x (additive
             kick, a kick that cannot remove matter that is not there, ...) is physics and belongs
             in step.
CoarseGrain  a many-to-one map Phi: X -> X', optionally with a tracking memory, i.e. a
             deterministic transducer (x, m) -> (x', m'):
                 m(0) = init_memory(x(0)),  m(t+1) = update_memory(m(t), x(t+1)),
                 x'(t) = phi(x(t), m(t)).
             The memory is a deterministic function of the level-below history; it has no noise
             and no input of its own, so (x, m) is a Markov state.

Noise        Noise(key, t): every random number a step draws is a function of (key, t). Two
             operations make composition exact rather than merely equal in distribution:
                 noise.stream(i)      independent sub-stream i, same clock (used by product)
                 noise.substep(n, i)  sub-step i of an n-fold strided tick: clock t*n + i
             Hence stride(stride(L, n), m) and stride(L, n*m) draw identical numbers, and
             stride(product(A, B), n) equals product(stride(A, n), stride(B, n)) pathwise.

All functions here are pure; batching is by jax.vmap over states, keys and inputs (the World
does this), and differentiation w.r.t. params is by jax autodiff when `differentiable`.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Callable, Mapping, Optional

import jax

jax.config.update("jax_enable_x64", True)
import jax.numpy as jnp  # noqa: E402
from jax.flatten_util import ravel_pytree  # noqa: E402

PyTree = Any


# ----------------------------------------------------------------------------- noise
@jax.tree_util.register_pytree_node_class
class Noise:
    """Counter-based noise source: (typed PRNG key, integer clock)."""

    def __init__(self, key, t):
        self.key = key
        self.t = t

    def tree_flatten(self):
        return (self.key, self.t), None

    @classmethod
    def tree_unflatten(cls, aux, children):
        return cls(*children)

    def rng(self):
        """A jax PRNG key for this clock value (use jax.random.split on it for several draws)."""
        return jax.random.fold_in(self.key, self.t)

    def normal(self, shape=(), dtype=jnp.float64):
        return jax.random.normal(self.rng(), shape, dtype)

    def uniform(self, shape=(), minval=0.0, maxval=1.0, dtype=jnp.float64):
        return jax.random.uniform(self.rng(), shape, dtype, minval, maxval)

    def stream(self, i: int) -> "Noise":
        """Independent sub-stream i with the same clock."""
        return Noise(jax.random.fold_in(self.key, i), self.t)

    def substep(self, n: int, i) -> "Noise":
        """Sub-step i (0 <= i < n) of an n-fold tick: the clock becomes t*n + i."""
        return Noise(self.key, self.t * n + i)


def flat(tree) -> jnp.ndarray:
    """Flatten a pytree of arrays to one float vector (leaf order of the pytree)."""
    leaves = jax.tree_util.tree_leaves(tree)
    if not leaves:
        return jnp.zeros((0,))
    if len(leaves) == 1:
        return jnp.ravel(leaves[0])
    return ravel_pytree(tree)[0]


# ----------------------------------------------------------------------------- level
@dataclass(frozen=True, eq=False)
class Level:
    """An open stochastic dynamical system (see module docstring).

    init(params, key) -> x;  step(params, x, noise, u) -> x'.
    Alternatively give step_xi(params, x, xi, u) with xi ~ N(0, I_noise_dim): the Gaussian-
    reparameterised form, which `step` then calls with xi = noise.normal((noise_dim,)). Levels with
    an explicit step_xi can enter correlated-noise products.
    params       declared parameters (pytree; nested dicts allow path selection 'a/b')
    conserved    {name: f(x) -> scalar} declared invariants of free evolution
    """
    init: Callable
    step: Optional[Callable] = None
    input_dim: int = 0
    params: PyTree = None
    noise_dim: Optional[int] = None
    step_xi: Optional[Callable] = None
    conserved: Mapping[str, Callable] = field(default_factory=dict)
    differentiable: bool = True
    opaque: bool = False
    name: str = "level"

    def __post_init__(self):
        if self.step is None:
            if self.step_xi is None or self.noise_dim is None:
                raise ValueError("Level: give step, or step_xi with noise_dim")
            sx, d = self.step_xi, int(self.noise_dim)
            object.__setattr__(self, "step", lambda p, x, noise, u: sx(p, x, noise.normal((d,)), u))
        if self.opaque:
            object.__setattr__(self, "differentiable", False)
        if self.input_dim < 0:
            raise ValueError("Level: input_dim must be >= 0")

    def state_spec(self, params=None):
        """Shapes and dtypes of the state (a pytree of jax.ShapeDtypeStruct)."""
        p = self.params if params is None else params
        return jax.eval_shape(lambda k: self.init(p, k), jax.random.key(0))

    def simulate(self, x0, key, U=None, T: Optional[int] = None, params=None):
        """Trajectory x(0..T) from x0 with Noise(key, t) at step t and inputs U[t] (T, input_dim).
        Returns the stacked states (leading axis T+1). Pure; jit it if called repeatedly."""
        p = self.params if params is None else params
        if U is None:
            U = jnp.zeros((int(T), self.input_dim))
        U = jnp.asarray(U, jnp.float64)

        def body(x, tu):
            t, u = tu
            x = self.step(p, x, Noise(key, t), u)
            return x, x
        _, xs = jax.lax.scan(body, x0, (jnp.arange(U.shape[0]), U))
        return jax.tree_util.tree_map(lambda a, b: jnp.concatenate([a[None], b]), x0, xs)


# ----------------------------------------------------------------------------- coarse-graining
@dataclass(frozen=True, eq=False)
class CoarseGrain:
    """A coarse-graining Phi: X -> X' with optional tracking memory (a transducer).

    phi(x, m) -> x';  init_memory(x) -> m;  update_memory(m, x_new) -> m'.
    Memoryless coarse-grainings use m = () and ignore it."""
    phi: Callable
    init_memory: Optional[Callable] = None
    update_memory: Optional[Callable] = None
    differentiable: bool = True
    opaque: bool = False
    name: str = "phi"

    def __post_init__(self):
        if (self.init_memory is None) != (self.update_memory is None):
            raise ValueError("CoarseGrain: give both init_memory and update_memory, or neither")
        if self.opaque:
            object.__setattr__(self, "differentiable", False)

    @property
    def has_memory(self) -> bool:
        return self.init_memory is not None

    @staticmethod
    def of(f: Callable, name: str = "phi", differentiable: bool = True) -> "CoarseGrain":
        """A memoryless coarse-graining x -> f(x)."""
        return CoarseGrain(phi=lambda x, m: f(x), name=name, differentiable=differentiable)

    def start(self, x):
        """(x'(0), m(0)) from x(0)."""
        m = self.init_memory(x) if self.has_memory else ()
        return self.phi(x, m), m

    def transduce(self, x, m):
        """One transducer step: (x(t+1), m(t)) -> (x'(t+1), m(t+1))."""
        if self.has_memory:
            m = self.update_memory(m, x)
        return self.phi(x, m), m

    def __call__(self, x, m=()):
        return self.phi(x, m)


def identity(name: str = "id") -> CoarseGrain:
    """The identity coarse-graining (exact; the unit of composition)."""
    return CoarseGrain(phi=lambda x, m: x, name=name)


def compose(a: CoarseGrain, b: CoarseGrain, name: Optional[str] = None) -> CoarseGrain:
    """b after a: x -> a -> b. Memory is the pair (m_a, m_b); m_b is driven by a's output."""
    has = a.has_memory or b.has_memory

    def phi(x, m):
        ma, mb = m if has else ((), ())
        return b.phi(a.phi(x, ma), mb)

    def m_init(x):
        ma = a.init_memory(x) if a.has_memory else ()
        mb = b.init_memory(a.phi(x, ma)) if b.has_memory else ()
        return (ma, mb)

    def m_upd(m, x):
        ma, mb = m
        ma = a.update_memory(ma, x) if a.has_memory else ma
        mb = b.update_memory(mb, a.phi(x, ma)) if b.has_memory else mb
        return (ma, mb)

    return CoarseGrain(phi=phi, init_memory=m_init if has else None, update_memory=m_upd if has else None,
                       differentiable=a.differentiable and b.differentiable, opaque=a.opaque or b.opaque,
                       name=name or f"{b.name}.{a.name}")


def compose_all(cgs, name: Optional[str] = None) -> CoarseGrain:
    """Left-to-right composition of a sequence (identity for an empty one)."""
    cgs = list(cgs)
    if not cgs:
        return identity()
    out = cgs[0]
    for c in cgs[1:]:
        out = compose(out, c)
    return out if name is None else CoarseGrain(out.phi, out.init_memory, out.update_memory,
                                                out.differentiable, out.opaque, name)


def product_cg(*cgs: CoarseGrain, name: Optional[str] = None) -> CoarseGrain:
    """Phi_1 x ... x Phi_n on tuple states; memory is the tuple of memories."""
    has = any(c.has_memory for c in cgs)
    n = len(cgs)

    def phi(x, m):
        ms = m if has else ((),) * n
        return tuple(c.phi(xi, mi) for c, xi, mi in zip(cgs, x, ms))

    def m_init(x):
        return tuple(c.init_memory(xi) if c.has_memory else () for c, xi in zip(cgs, x))

    def m_upd(m, x):
        return tuple(c.update_memory(mi, xi) if c.has_memory else mi for c, mi, xi in zip(cgs, m, x))

    return CoarseGrain(phi=phi, init_memory=m_init if has else None, update_memory=m_upd if has else None,
                       differentiable=all(c.differentiable for c in cgs), opaque=any(c.opaque for c in cgs),
                       name=name or " x ".join(c.name for c in cgs))


def unit_level() -> Level:
    """The monoidal unit: a one-point state space (an empty tuple), no input, no noise."""
    return Level(init=lambda p, k: (), step=lambda p, x, noise, u: (), input_dim=0, name="unit")
