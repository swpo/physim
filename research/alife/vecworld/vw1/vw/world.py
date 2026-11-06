"""vw.world -- supervenient worlds: WorldSpec (declaration), World (instance), Ensemble, Designer.

A SUPERVENIENT WORLD is a chain L0 -> L1 -> ... -> Ln: only L0 (the base Level) has a law; the
upper levels are coarse-grainings whose effective law is induced, never written. An InputPort sits
on L0 and an ObservePort on L_k (k = observe_at, default the top of the chain).

WorldSpec  the declaration (no hidden permutations). Composition operators act on specs.
World      an instance: spec + world_seed (which draws the hidden permutations) + params. It
           exposes the agent API (card, reset, step, run) and `designer` (privileged API).

Timeline (as VW-0): reset returns o(0); each tick t validates a(t), realises and embeds it,
runs the law once (u enters through the level's own kick), updates every tracking memory and
emits o(t+1). Noise is counter-based: for a member with key K, the law at tick t draws from
Noise(fold_in(K, PROC), t), actuation from fold_in(fold_in(K, ACT), t), observation from
fold_in(fold_in(K, OBS), t). Members that share K share all noise (common random numbers, used
for branching); the noise of a member never depends on the ensemble size.

Change from VW-0: episode keys include the world seed, so two replicas (same law, different
world seeds) reset to the same seed are NOT the same hidden trajectory; in VW-0 they were, and
comparing them would hand the agent the relative permutation.

The pure functions of an instance (all jit-compiled, batched by vmap):
    _init_member(params, k_init, k_dyn) -> Carry       init + burn-in (no input)
    _tick(params, carry, a)            -> Carry        one tick, agent coordinates a (n_in,)
    _obs(carry) / _clean(carry)        -> (n_obs,)     noisy / noise-free observation
    _rollout(params, carry_B, A (T,B,n_in), rec)       scan over T ticks, records per tick
"""
from __future__ import annotations

import dataclasses
import math
from dataclasses import dataclass, field
from typing import Any, Mapping, NamedTuple, Optional, Sequence

import jax
import jax.numpy as jnp
import numpy as np

from .core import CoarseGrain, Level, Noise, flat
from .ports import Admissible, BudgetExhausted, InputPort, InputViolation, ObservePort

CONTRACT = "VW-1"
_SALT = 0x565731
_S_PERM = 0
_NS_EPISODE, _NS_EPISODE_FRESH, _NS_EXAM, _NS_DESIGNER, _NS_BRANCH, _NS_CERT = 0, 1, 2, 3, 4, 5
_ST_INIT, _ST_BURN, _ST_PROC, _ST_ACT, _ST_OBS, _ST_DYN = 1, 2, 3, 4, 5, 6
MAX_SEED = 2 ** 62


def make_key(*ints) -> jax.Array:
    """A typed PRNG key that is a deterministic function of integers (each < 2**64)."""
    k = jax.random.key(_SALT)
    for i in ints:
        i = int(i)
        if i < 0:
            raise ValueError("make_key: integers must be >= 0")
        k = jax.random.fold_in(k, i & 0xFFFFFFFF)
        k = jax.random.fold_in(k, (i >> 32) & 0xFFFFFFFF)
    return k


def member_keys(base, n: int):
    return jax.vmap(lambda j: jax.random.fold_in(base, j))(jnp.arange(n))


class Carry(NamedTuple):
    """Per-member simulation state: level-0 state, chain memories, agent time, member key."""
    x: Any
    mem: Any
    t: Any
    key: Any


# ----------------------------------------------------------------------------- declaration
@dataclass(frozen=True, eq=False)
class WorldSpec:
    """Declaration of a supervenient world (no hidden permutations; see World for instances).

    base         the level-0 Level (the only law)
    chain        coarse-grainings L0 -> L1 -> ... -> Ln
    inport       InputPort on L0 (input enters through base.step's kick)
    outport      ObservePort on L_observe_at
    observe_at   index k of the observed level (default len(chain))
    burn_in      ticks of free evolution before t = 0 (with init-derived noise)
    replay       'none' | 'initial' | 'full' (see DESIGN.md section 4)
    max_ticks    exploration budget (None: unlimited)
    public_notes text shown on the card; everything here is public, so keep structure out of it
    name, meta   designer-only (never on the card)
    """
    base: Level
    chain: tuple = ()
    inport: InputPort = InputPort()
    outport: ObservePort = ObservePort()
    observe_at: Optional[int] = None
    burn_in: int = 0
    replay: str = "initial"
    max_ticks: Optional[int] = None
    public_notes: str = ""
    name: str = "world"
    meta: Mapping = field(default_factory=dict)

    def __post_init__(self):
        object.__setattr__(self, "chain", tuple(self.chain))
        if self.replay not in ("none", "initial", "full"):
            raise ValueError("WorldSpec: replay must be 'none', 'initial' or 'full'")
        if self.observe_at is not None and not 0 <= self.observe_at <= len(self.chain):
            raise ValueError("WorldSpec: observe_at outside [0, len(chain)]")
        if self.burn_in < 0:
            raise ValueError("WorldSpec: burn_in must be >= 0")
        for c in self.chain:
            if not isinstance(c, CoarseGrain):
                raise TypeError("WorldSpec: chain entries must be CoarseGrain")

    @property
    def k_obs(self) -> int:
        return len(self.chain) if self.observe_at is None else self.observe_at

    @property
    def differentiable(self) -> bool:
        return self.base.differentiable and all(c.differentiable for c in self.chain[: self.k_obs])

    @property
    def opaque(self) -> bool:
        return self.base.opaque or any(c.opaque for c in self.chain)

    def replace(self, **kw) -> "WorldSpec":
        return dataclasses.replace(self, **kw)

    def with_ports(self, inport: Optional[InputPort] = None, outport: Optional[ObservePort] = None) -> "WorldSpec":
        """Change the apparatus (the lens between world and agent); permutations are re-drawn."""
        return self.replace(inport=(inport or self.inport).unbound(), outport=(outport or self.outport).unbound())


# ----------------------------------------------------------------------------- instance
class World:
    """A world instance: spec + hidden permutations (from world_seed) + parameter values."""

    def __init__(self, spec: WorldSpec, world_seed: int = 0, params=None):
        self.spec = spec
        self.world_seed = int(world_seed)
        self.params = spec.base.params if params is None else params
        self.k_obs = spec.k_obs
        rng = np.random.default_rng([_SALT, _S_PERM, self.world_seed])
        self.inport = spec.inport.bind(spec.base.input_dim, rng)
        x_spec = spec.base.state_spec(self.params)
        y_spec = jax.eval_shape(self._top_of_state, x_spec)
        self.outport = spec.outport.bind(int(y_spec.shape[0]), rng)
        self._build()
        self._ep: Optional[Ensemble] = None
        self._ep_count = 0
        self._last_in: Optional[int] = None
        self._spent = 0.0
        self.ticks_used = 0
        self._branch_count = 0
        self._designer_count = 0

    # ---------------------------------------------------------------- pure functions
    def _start_mem(self, x):
        mem, y = [], x
        for cg in self.spec.chain:
            m = cg.init_memory(y) if cg.has_memory else ()
            y = cg.phi(y, m)
            mem.append(m)
        return tuple(mem)

    def _update_mem(self, mem, x):
        out, y = [], x
        for cg, m in zip(self.spec.chain, mem):
            if cg.has_memory:
                m = cg.update_memory(m, y)
            y = cg.phi(y, m)
            out.append(m)
        return tuple(out)

    def _levels(self, x, mem, upto: int):
        ys, y = [x], x
        for cg, m in zip(self.spec.chain[:upto], mem[:upto]):
            y = cg.phi(y, m)
            ys.append(y)
        return ys

    def _top_of_state(self, x):
        return flat(self._levels(x, self._start_mem(x), self.k_obs)[-1])

    def _build(self):
        base, ip, op, k = self.spec.base, self.inport, self.outport, self.k_obs
        burn, n_in = int(self.spec.burn_in), self.inport.n_in
        fold = jax.random.fold_in

        def top(c):
            return flat(self._levels(c.x, c.mem, k)[-1])

        def tick(params, c, a):
            a = ip.realise(a, fold(fold(c.key, _ST_ACT), c.t))
            x = base.step(params, c.x, Noise(fold(c.key, _ST_PROC), c.t), ip.embed(a))
            return Carry(x, self._update_mem(c.mem, x), c.t + 1, c.key)

        def obs(c):
            return op.read(top(c), fold(fold(c.key, _ST_OBS), c.t))

        def obs_continuous(c):
            return op.read_continuous(top(c), fold(fold(c.key, _ST_OBS), c.t))

        def clean(c):
            return op.clean(top(c))

        def init_member(params, k_init, k_dyn):
            x = base.init(params, fold(k_init, _ST_INIT))
            c = Carry(x, self._start_mem(x), jnp.zeros((), jnp.int64), fold(k_init, _ST_BURN))
            if burn > 0:
                z = jnp.zeros((n_in,))
                c, _ = jax.lax.scan(lambda cc, _: (tick(params, cc, z), None), c, None, length=burn)
            return Carry(c.x, c.mem, jnp.zeros((), jnp.int64), k_dyn)

        def record(c, rec):
            out = {}
            for r in rec:
                if r == "obs":
                    out[r] = jax.vmap(obs)(c)
                elif r == "obs_continuous":
                    out[r] = jax.vmap(obs_continuous)(c)
                elif r == "clean":
                    out[r] = jax.vmap(clean)(c)
                elif r == "x":
                    out[r] = jax.vmap(lambda cc: flat(cc.x))(c)
                elif r.startswith("L"):
                    j = int(r[1:])
                    out[r] = jax.vmap(lambda cc, j=j: flat(self._levels(cc.x, cc.mem, j)[-1]))(c)
                else:
                    raise ValueError(f"rollout: unknown record {r!r}")
            return out

        def rollout(params, c, A, rec):
            vt = jax.vmap(tick, in_axes=(None, 0, 0))
            first = record(c, rec)

            def body(cc, a):
                cc = vt(params, cc, a)
                return cc, record(cc, rec)
            c, outs = jax.lax.scan(body, c, A)
            return c, {r: jnp.concatenate([first[r][None], outs[r]], 0) for r in rec}

        self._tick, self._obs, self._clean, self._init_member = tick, obs, clean, init_member
        self._obs_continuous = obs_continuous
        self._rollout_fn = rollout
        self._v_init = jax.jit(jax.vmap(init_member, in_axes=(None, 0, 0)))
        self._rollout = jax.jit(rollout, static_argnames=("rec",))
        self._v_obs = jax.jit(jax.vmap(obs))
        self._v_clean = jax.jit(jax.vmap(clean))
        self._v_level = jax.jit(jax.vmap(lambda c, j: flat(self._levels(c.x, c.mem, j)[-1]), in_axes=(0, None)),
                                static_argnums=1)

    # ---------------------------------------------------------------- agent-facing
    @property
    def n_in(self) -> int:
        return self.inport.n_in

    @property
    def n_obs(self) -> int:
        return self.outport.n_obs

    @property
    def in_map(self) -> np.ndarray:
        return np.asarray(self.inport.in_map, int)

    @property
    def out_map(self) -> np.ndarray:
        return np.asarray(self.outport.out_map, int)

    @property
    def out_sign(self) -> np.ndarray:
        return np.asarray(self.outport.out_sign, float)

    @property
    def t(self) -> Optional[int]:
        return None if self._ep is None else self._ep.t

    def card(self) -> dict:
        """The public world card: everything the agent is told. No level or coarse-graining names,
        no state sizes other than n_in and n_obs, no stride or slot counts (VW-0 review lesson)."""
        s = self.spec
        return {
            "contract": CONTRACT, "n_in": self.n_in, "n_obs": self.n_obs,
            "inputs": self.inport.public(), "observation": self.outport.public(),
            "replay": s.replay, "max_ticks": s.max_ticks, "ticks_used": self.ticks_used,
            "timing": "an input given at tick t acts before the law runs; its effect can appear from o(t+1) on",
            "notes": s.public_notes,
        }

    def reset(self, seed: int) -> np.ndarray:
        """Start an episode. Returns o(0). Free (no ticks charged)."""
        seed = self._check_seed(seed)
        self._ep_count += 1
        ws, mode = self.world_seed, self.spec.replay
        if mode == "full":
            ki = make_key(_NS_EPISODE, ws, seed)
            kd = jax.random.fold_in(ki, _ST_DYN)
        elif mode == "initial":
            ki = make_key(_NS_EPISODE, ws, seed)
            kd = make_key(_NS_EPISODE_FRESH, ws, seed, self._ep_count)
        else:
            ki = make_key(_NS_EPISODE_FRESH, ws, seed, self._ep_count)
            kd = jax.random.fold_in(ki, _ST_DYN)
        self._ep = self._new_ensemble(ki[None], kd[None])
        self._last_in, self._spent = None, 0.0
        return self._ep.observe()[0]

    def step(self, inp=None) -> np.ndarray:
        """One tick. inp: None | {agent coord: value} | dense vector of length n_in.
        Returns o(t+1). Violations raise InputViolation; nothing runs or is charged."""
        ep = self._require_episode()
        C = self.inport.admissible
        a = C.normalize(inp, self.n_in)
        C.check(a, ep.t, self._last_in, self._spent)
        self._check_budget(1)
        self._ep = ep.step(self._dense(C.canonical(a)) if a else None)
        self.ticks_used += 1
        if a:
            self._last_in = ep.t
            self._spent += C.charge(a)
        return self._ep.observe()[0]

    def run(self, program, query_times, seed: Optional[int] = None) -> np.ndarray:
        """Run a program of timed inputs; return o at the query times (len(q), n_obs).

        program      iterable of (t, input) or {t: input}; t >= 0 relative to the start
        query_times  integers >= 0 relative to the start (0 = the starting observation)
        seed         if given, reset(seed) first; otherwise continue the current episode
        The whole program is validated first; on any violation nothing runs and nothing is charged."""
        q = [int(x) for x in query_times]
        if not q or min(q) < 0:
            raise InputViolation("format: query_times must be a non-empty list of integers >= 0")
        mq = self.outport.max_queries
        if mq is not None and len(set(q)) > mq:
            raise InputViolation(f"queries: {len(set(q))} distinct query times > max_queries={mq}")
        H = max(q)
        if seed is not None:
            self._check_seed(seed)
            t0, last, spent = 0, None, 0.0
        else:
            ep = self._require_episode()
            t0, last, spent = ep.t, self._last_in, self._spent
        prog = self._validate_program(program, t0, last, spent, H)
        self._check_budget(H)
        if seed is not None:
            self.reset(seed)
        ep = self._ep
        C = self.inport.admissible
        A = np.zeros((H, 1, self.n_in))
        for t, a in prog:
            for j, v in C.canonical(a).items():
                A[t, 0, j] = v
            self._last_in = ep.t + t
            self._spent += C.charge(a)
        c, rec = self._rollout(self.params, ep.carry, jnp.asarray(A), rec=("obs",))
        self._ep = Ensemble(self, c, ep.t + H)
        self.ticks_used += H
        o = np.asarray(rec["obs"][:, 0])
        return o[q]

    # ---------------------------------------------------------------- internals
    def _check_seed(self, seed) -> int:
        if isinstance(seed, bool) or not isinstance(seed, (int, np.integer)) or not 0 <= seed < MAX_SEED:
            raise ValueError(f"seed must be an integer in [0, 2**62), got {seed!r}")
        return int(seed)

    def _require_episode(self) -> "Ensemble":
        if self._ep is None:
            raise RuntimeError("call reset(seed) first")
        return self._ep

    def _check_budget(self, n: int):
        mt = self.spec.max_ticks
        if mt is not None and self.ticks_used + n > mt:
            raise BudgetExhausted(f"budget: {self.ticks_used} + {n} ticks > max_ticks={mt}; nothing ran")

    def _dense(self, a: dict) -> np.ndarray:
        d = np.zeros(self.n_in)
        for j, v in a.items():
            d[j] = v
        return d

    def _validate_program(self, program, t0, last, spent, H) -> list:
        C = self.inport.admissible
        items = list(program.items()) if isinstance(program, Mapping) else list(program or [])
        for entry in items:
            if not isinstance(entry, (tuple, list)) or len(entry) != 2:
                raise InputViolation(f"format: program entries must be (t, input) pairs, got {entry!r}")
            t = entry[0]
            if isinstance(t, bool) or not isinstance(t, (int, np.integer)) or t < 0:
                raise InputViolation(f"format: program times must be integers >= 0, got {t!r}")
        out, seen = [], set()
        for t, inp in sorted(items, key=lambda e: int(e[0])):
            t = int(t)
            if t in seen:
                raise InputViolation(f"format: two program entries at t={t}")
            seen.add(t)
            a = C.normalize(inp, self.n_in)
            if not a:
                continue
            if t >= H:
                raise InputViolation(f"program: input at t={t} is at or after the last query "
                                     f"time {H} and could not affect any queried observation")
            C.check(a, t0 + t, last, spent, where=f"program entry t={t}: ")
            last, spent = t0 + t, spent + C.charge(a)
            out.append((t, a))
        return out

    def _new_ensemble(self, k_init, k_dyn, t: int = 0) -> "Ensemble":
        return Ensemble(self, self._v_init(self.params, k_init, k_dyn), t)

    def _fresh_keys(self, n: int):
        self._branch_count += 1
        return member_keys(make_key(_NS_BRANCH, self.world_seed, self._branch_count), n)

    def _inputs(self, a, B: int, T: int = 1):
        """None | (n_in,) | (B, n_in) | (T, B, n_in) -> (T, B, n_in) array."""
        if a is None:
            return jnp.zeros((T, B, self.n_in))
        a = jnp.asarray(a, jnp.float64)
        if a.ndim == 1:
            a = jnp.broadcast_to(a, (B, self.n_in))
        if a.ndim == 2:
            a = jnp.broadcast_to(a[None], (T, B, self.n_in))
        return a

    @property
    def designer(self) -> "Designer":
        return Designer(self)


# ----------------------------------------------------------------------------- ensemble
class Ensemble:
    """B members of one world simulated in lockstep (privileged, designer side). Immutable:
    step and clone return new ensembles. Members that share a key share all noise."""

    def __init__(self, world: World, carry: Carry, t: int):
        self.world, self.carry, self.t = world, carry, int(t)

    @property
    def B(self) -> int:
        return int(self.carry.t.shape[0])

    @property
    def x(self):
        """Batched level-0 state (pytree with leading axis B)."""
        return self.carry.x

    def x_flat(self) -> np.ndarray:
        return np.asarray(jax.vmap(flat)(self.carry.x))

    def step(self, a=None) -> "Ensemble":
        """Advance one tick with agent-coordinate input a (None, (n_in,) or (B, n_in)); no checks
        (the designer may apply any input)."""
        c, _ = self.world._rollout(self.world.params, self.carry, self.world._inputs(a, self.B, 1), rec=())
        return Ensemble(self.world, c, self.t + 1)

    def observe(self) -> np.ndarray:
        return np.asarray(self.world._v_obs(self.carry))

    def clean(self) -> np.ndarray:
        """Noise-free observations in the agent basis."""
        return np.asarray(self.world._v_clean(self.carry))

    def level(self, j: int) -> np.ndarray:
        """Flattened level-j states in the designer (un-permuted) basis."""
        return np.asarray(self.world._v_level(self.carry, int(j)))

    def clone(self, rep: int = 1, idx=None, fresh: bool = False, keys=None) -> "Ensemble":
        """Copies of members idx, each repeated rep times (member-major). fresh=False: copies share
        their parent's noise; fresh=True: every copy gets new, independent noise (keys: explicit
        new member keys, for reproducible certificates)."""
        idx = np.arange(self.B) if idx is None else np.asarray(idx)
        sel = jnp.asarray(np.repeat(idx, rep))
        c = jax.tree_util.tree_map(lambda a: a[sel], self.carry)
        if keys is not None:
            c = c._replace(key=keys)
        elif fresh:
            c = c._replace(key=self.world._fresh_keys(int(sel.shape[0])))
        return Ensemble(self.world, c, self.t)

    def invariants(self) -> dict:
        cons = self.world.spec.base.conserved
        return {k: np.asarray(jax.vmap(f)(self.carry.x), float) for k, f in cons.items()}


# ----------------------------------------------------------------------------- designer
class Designer:
    """Privileged access to a World (never shown to the agent)."""

    def __init__(self, world: World):
        self.w = world

    # ---- state, branches, ensembles ----
    def state(self) -> dict:
        ep = self.w._require_episode()
        c = jax.tree_util.tree_map(lambda a: a[0], ep.carry)
        lv = self.w._levels(c.x, c.mem, len(self.w.spec.chain))
        return {"t": ep.t, "x": c.x, "x_flat": np.asarray(flat(c.x)), "mem": c.mem,
                "levels": [np.asarray(flat(y)) for y in lv], "observed": np.asarray(flat(lv[self.w.k_obs])),
                "in_map": self.w.in_map.copy(), "out_map": self.w.out_map.copy(), "out_sign": self.w.out_sign.copy()}

    def branch(self, rep: int = 1, fresh: bool = False) -> Ensemble:
        """Copies of the agent's current episode (identical noise unless fresh)."""
        return self.w._require_episode().clone(rep=rep, fresh=fresh)

    def ensemble(self, B: int, seed=None) -> Ensemble:
        """B independent members from the declared initial distribution (after burn-in)."""
        if seed is None:
            self.w._designer_count += 1
            seed = (self.w._designer_count,)
        seed = tuple(seed) if isinstance(seed, (tuple, list)) else (int(seed),)
        ki = member_keys(make_key(_NS_DESIGNER, self.w.world_seed, *seed), B)
        kd = jax.vmap(lambda k: jax.random.fold_in(k, _ST_DYN))(ki)
        return self.w._new_ensemble(ki, kd)

    def from_states(self, x, mem=None, t: int = 0, keys=None) -> Ensemble:
        """An ensemble placed in given batched level-0 states (memories started from them)."""
        x = jax.tree_util.tree_map(jnp.asarray, x)
        B = int(jax.tree_util.tree_leaves(x)[0].shape[0])
        if mem is None:
            mem = jax.vmap(self.w._start_mem)(x)
        keys = self.w._fresh_keys(B) if keys is None else keys
        return Ensemble(self.w, Carry(x, mem, jnp.full((B,), t, jnp.int64), keys), t)

    # ---- programs ----
    def program_dense(self, program, H: int, validate: bool = True) -> np.ndarray:
        P = np.zeros((max(H, 0), self.w.n_in))
        if not program:
            return P
        C = self.w.inport.admissible
        H_all = max([H] + [int(e[0]) + 1 for e in program])
        prog = (self.w._validate_program(program, 0, None, 0.0, H_all) if validate else
                [(int(t), C.normalize(a, self.w.n_in)) for t, a in program])
        for t, a in prog:
            if 0 <= t < H:
                for j, v in (C.canonical(a) if validate else a).items():
                    P[t, j] = v
        return P

    def random_program(self, rng: np.random.Generator, H: int, rate: float = 0.5) -> list:
        """Random admissible program over [0, H)."""
        C, prog, last, spent = self.w.inport.admissible, [], None, 0.0
        for t in range(H):
            if rng.random() >= rate or (last is not None and t - last < C.min_interval):
                continue
            a = C.sample(rng, self.w.n_in)
            l1 = C.charge(a)
            if not a or (C.episode_budget is not None and spent + l1 > C.episode_budget):
                continue
            prog.append((t, a))
            last, spent = t, spent + l1
        return prog

    def rollout(self, ens: Ensemble, P=None, T: Optional[int] = None, t_end: Optional[int] = None,
                rec: Sequence[str] = ("obs",)):
        """Advance ens by T ticks (or to agent time t_end) applying the dense program P, indexed by
        absolute agent time ((H, n_in) shared or (B, H, n_in) per member; rows past H are zero).
        Records, at agent times ens.t .. ens.t+T, any of 'obs', 'obs_continuous', 'clean' (noise-
        free agent basis), 'x' (flat level 0), 'L<j>' (flat level j, designer basis).
        Returns (new ensemble, {name: array (B, T+1, d)})."""
        if T is None:
            T = int(t_end) - ens.t
        T = int(T)
        if T < 0:
            raise ValueError("rollout: negative duration")
        n_in, B, t0 = self.w.n_in, ens.B, ens.t
        A = np.zeros((T, B, n_in))
        if P is not None:
            P = np.asarray(P, float)
            if P.ndim == 2:
                rows = P[t0:t0 + T]
                A[:rows.shape[0]] = rows[:, None, :]
            else:
                rows = P[:, t0:t0 + T]
                A[:rows.shape[1]] = np.transpose(rows, (1, 0, 2))
        c, out = self.w._rollout(self.w.params, ens.carry, jnp.asarray(A), rec=tuple(rec))
        return Ensemble(self.w, c, t0 + T), {k: np.asarray(jnp.swapaxes(v, 0, 1)) for k, v in out.items()}

    # ---- certificates (vw.certificates) ----
    def closure(self, *a, **kw):
        from .certificates import closure
        return closure(self.w, *a, **kw)

    def leak(self, *a, **kw):
        from .certificates import leak
        return leak(self.w, *a, **kw)

    def input_capacity(self, *a, **kw):
        from .certificates import input_capacity
        return input_capacity(self.w, *a, **kw)

    def observation_capacity(self, *a, **kw):
        from .certificates import observation_capacity
        return observation_capacity(self.w, *a, **kw)

    def invariant_drift(self, *a, **kw):
        from .certificates import invariant_drift
        return invariant_drift(self.w, *a, **kw)

    def fisher(self, *a, **kw):
        from .certificates import fisher
        return fisher(self.w, *a, **kw)

    def certify(self, *a, **kw):
        from .certificates import certify
        return certify(self.w, *a, **kw)
