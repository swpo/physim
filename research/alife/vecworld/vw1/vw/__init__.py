"""vw -- the VW-1 JAX library: supervenient worlds as a category of open stochastic systems.

Module types (vw.core, vw.ports, vw.world)
    Level(init(params, key), step(params, x, noise, u), input_dim, params, conserved, ...)
    CoarseGrain(phi(x, m), init_memory(x), update_memory(m, x)); identity, compose, product_cg
    Noise(key, t): counter-based randomness; .stream(i) for independent factors, .substep(n, i)
    InputPort(Admissible(k, lo, hi, total, zero_sum, min_interval, quantum, episode_budget), actuable, noise)
    ObservePort(noise, quantum, clip, sign_flip, max_queries)
    WorldSpec(base, chain, inport, outport, observe_at, burn_in, replay, max_ticks, public_notes)
    World(spec, world_seed, params): card(), reset(seed), step(input), run(program, query_times, seed)
    World.designer: state, branch, ensemble, from_states, rollout, program_dense, random_program, certificates

Composition (vw.operators): stack, product (noise 'independent' | 'shared' | ('correlated', rho)),
    couple, stride, refine (+ lifted), commutation_error; product_level, stride_level
Certificates (vw.certificates): closure, leak, input_capacity, observation_capacity,
    invariant_drift, fisher (autodiff), certify
Exam (vw.exam), opaque blocks (vw.opaque), linear-Gaussian family (vw.lingauss), toys (vw.toys).

Importing vw enables float64 in JAX (jax_enable_x64).
"""
import jax

jax.config.update("jax_enable_x64", True)

from .core import (CoarseGrain, Level, Noise, compose, compose_all, flat, identity, product_cg,  # noqa: E402
                   unit_level)
from .ports import Admissible, BudgetExhausted, InputPort, InputViolation, ObservePort  # noqa: E402
from .world import CONTRACT, Carry, Designer, Ensemble, World, WorldSpec, make_key, member_keys  # noqa: E402
from .operators import (commutation_error, couple, lifted, product, product_level, refine, stack,  # noqa: E402
                      stride, stride_level)
from .certificates import (NotDifferentiable, capacity_from_response, certify, closure, fisher,  # noqa: E402
                           input_capacity, invariant_drift, jsonable, leak, logdet, observation_capacity,
                           waterfill)
from .exam import Exam  # noqa: E402
from .opaque import host_coarse_grain, host_level  # noqa: E402

InputConstraints = Admissible   # VW-0 name

__all__ = [n for n in dir() if not n.startswith("_")]
