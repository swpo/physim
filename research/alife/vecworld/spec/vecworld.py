"""vecworld.py -- reference implementation of the VW-0 vector-world contract.

A world is a hierarchy of hidden vectors (see DESIGN.md):

    level 0   h0(t) in R^n0, evolving under a fixed law F0 (with process noise)
    level 1   h1(t) = Phi(h0(t), m(t)), a fixed many-to-one coarse-graining, with an
              optional tracking memory m(t+1) = M(m(t), h0(t+1)) that is a
              deterministic function of the level-0 history (never an independent state)

The agent observes o(t) = obs(P_out h1(t)) through a hidden permutation P_out and
acts blindly on level 0: its input a(t) (agent coordinates) is placed into the
actuator space through a hidden permutation and kicked into h0 before the law runs:

    h0(t)+  = kick(h0(t), B a(t))        (default kick: addition)
    h0(t+1) = F0(h0(t)+, xi(t))
    o(t+1)  = quantise(clip(sign * h1(t+1)[out_map] + sigma_o * eta(t+1)))

Agent API     VectorWorld.card(), reset(seed), step(input), run(program, query_times, seed)
Designer API  VectorWorld.designer -> Designer: privileged h0/m/h1, ensembles and
              branches with common random numbers, certificate estimators
              (closure, leak, input capacity, observation capacity), Exam harness.
Composition   product/concat, stack, stride, refine, commutation_error.

Noise is a deterministic function of (stream, seed, member key, tick): members of an
ensemble that share (seed, key) receive identical noise, which is how branching runs
with identical noise are made.  Everything is batched over ensemble members.
"""
from __future__ import annotations

import math
from dataclasses import asdict, dataclass, field
from typing import Callable, Mapping, Optional, Sequence

import numpy as np
from scipy.special import digamma

CONTRACT = "VW-0"
_SALT = 0x565730
_S_PERM, _S_INIT, _S_PROC, _S_ACT, _S_OBS, _S_MISC = 0, 1, 2, 3, 4, 5
_NS_EPISODE, _NS_EPISODE_FRESH, _NS_EXAM, _NS_DESIGNER, _NS_BRANCH = 0, 1, 2, 3, 4
MAX_SEED = 2 ** 62


class InputViolation(ValueError):
    """An input or program broke a declared constraint. Nothing ran and nothing was charged."""


class BudgetExhausted(RuntimeError):
    """The declared exploration budget (ticks) would be exceeded. Nothing ran."""


def _rng(*ints) -> np.random.Generator:
    return np.random.default_rng([_SALT, *[int(i) for i in ints]])


# --------------------------------------------------------------------------- constraints
@dataclass(frozen=True)
class InputConstraints:
    """Declared, public input constraints, in agent coordinates (all permutation invariant).

    k              max number of non-zero coordinates per tick (None: no limit)
    lo, hi         bounds on every non-zero value
    total          bound on sum_j |a_j| per tick (None: none)
    zero_sum       sum_j a_j must be 0: inputs move mass, never create it
    min_interval   minimum ticks between consecutive non-empty inputs (1: every tick)
    quantum        values must be integer multiples of quantum (None: continuous)
    episode_budget bound on the episode's summed |a| (None: none)
    noise          multiplicative actuation noise (std) applied to the support; with
                   zero_sum the realised kick is re-projected to zero sum.  Constraints
                   apply to the command, not the realisation.
    """
    k: Optional[int] = None
    lo: float = -1.0
    hi: float = 1.0
    total: Optional[float] = None
    zero_sum: bool = False
    min_interval: int = 1
    quantum: Optional[float] = None
    episode_budget: Optional[float] = None
    noise: float = 0.0
    tol: float = 1e-9

    def __post_init__(self):
        if self.lo > self.hi:
            raise ValueError("InputConstraints: lo > hi")
        if self.k is not None and self.k < 1:
            raise ValueError("InputConstraints: k must be >= 1")
        if self.min_interval < 1:
            raise ValueError("InputConstraints: min_interval must be >= 1")
        if self.zero_sum and not (self.lo < 0 < self.hi):
            raise ValueError("InputConstraints: zero_sum needs lo < 0 < hi")
        if self.zero_sum and self.k is not None and self.k < 2:
            raise ValueError("InputConstraints: zero_sum needs k >= 2")
        if self.noise < 0:
            raise ValueError("InputConstraints: noise must be >= 0")

    # ---- parsing and checking (depend only on public information) ----
    def normalize(self, inp, n_in: int) -> dict:
        """dict {coord: value} | dense vector of length n_in | None  ->  {coord: value != 0}."""
        if inp is None:
            return {}
        if isinstance(inp, Mapping):
            out = {}
            for key, v in inp.items():
                if isinstance(key, bool) or not isinstance(key, (int, np.integer)):
                    raise InputViolation(f"format: coordinate keys must be integers, got {key!r}")
                j = int(key)
                if not 0 <= j < n_in:
                    raise InputViolation(f"format: coordinate {j} outside [0, {n_in})")
                try:
                    v = float(v)
                except (TypeError, ValueError):
                    raise InputViolation(f"format: value for coordinate {j} is not a number: {v!r}")
                if not math.isfinite(v):
                    raise InputViolation(f"format: value for coordinate {j} is not finite")
                if v != 0.0:
                    out[j] = v
            return out
        arr = np.asarray(inp, dtype=float)
        if arr.shape != (n_in,):
            raise InputViolation(f"format: a dense input must have shape ({n_in},), got {arr.shape}")
        if not np.all(np.isfinite(arr)):
            raise InputViolation("format: dense input has non-finite values")
        return {int(j): float(arr[j]) for j in np.flatnonzero(arr)}

    def violations(self, a: dict, t: int, last_t: Optional[int], spent: float) -> list:
        if not a:
            return []
        msgs = []
        v = np.fromiter(a.values(), float)
        l1 = float(np.abs(v).sum())
        if self.k is not None and v.size > self.k:
            msgs.append(f"sparsity: {v.size} non-zero coordinates > k={self.k}")
        if v.min() < self.lo - self.tol or v.max() > self.hi + self.tol:
            msgs.append(f"bound: non-zero values must lie in [{self.lo:g}, {self.hi:g}] "
                        f"(got min {v.min():.6g}, max {v.max():.6g})")
        if self.total is not None and l1 > self.total + self.tol:
            msgs.append(f"total: sum|a| = {l1:.6g} > total={self.total:g}")
        if self.zero_sum and abs(v.sum()) > self.tol * max(1.0, l1):
            msgs.append(f"zero-sum: sum(a) = {v.sum():.6g}, must be 0")
        if self.quantum:
            dev = np.abs(v / self.quantum - np.round(v / self.quantum)).max()
            if dev > 1e-6:
                msgs.append(f"quantum: values must be integer multiples of {self.quantum:g}")
        if last_t is not None and t - last_t < self.min_interval:
            msgs.append(f"interval: last non-empty input at t={last_t}; the next is allowed "
                        f"at t={last_t + self.min_interval}, got t={t}")
        if self.episode_budget is not None and spent + l1 > self.episode_budget + self.tol:
            msgs.append(f"budget: episode sum|a| would be {spent + l1:.6g} > {self.episode_budget:g}")
        return msgs

    def check(self, a: dict, t: int, last_t: Optional[int], spent: float, where: str = ""):
        msgs = self.violations(a, t, last_t, spent)
        if msgs:
            raise InputViolation(f"{where}input rejected, nothing charged: " + "; ".join(msgs))

    # ---- sampling (used by designer program samplers) ----
    def sample(self, rng: np.random.Generator, n_in: int, max_tries: int = 50) -> dict:
        k = n_in if self.k is None else min(self.k, n_in)
        if self.zero_sum and k < 2:
            return {}
        lo = max(self.lo, -1e6)
        hi = min(self.hi, 1e6)
        for _ in range(max_tries):
            idx = rng.choice(n_in, size=k, replace=False)
            v = rng.uniform(lo, hi, size=k)
            if self.zero_sum:
                v = v - v.mean()
                f = 1.0
                if v.max() > hi:
                    f = min(f, hi / v.max())
                if v.min() < lo:
                    f = min(f, lo / v.min())
                v = v * f
            if self.total is not None and np.abs(v).sum() > self.total:
                v = v * (self.total / np.abs(v).sum())
            if self.quantum:
                v = self.quantum * np.round(v / self.quantum)
                if self.zero_sum:
                    v[0] -= v.sum()
            a = {int(i): float(x) for i, x in zip(idx, v) if x != 0.0}
            if a and not self.violations(a, 0, None, 0.0):
                return a
        return {}

    # ---- structural numbers used by the input-capacity certificate ----
    def amplitude(self) -> float:
        b = max(abs(self.lo), abs(self.hi))
        if self.total is not None:
            b = min(b, self.total)
        return b

    def atom_amplitude(self) -> float:
        """Amplitude of the elementary admissible move: +b on one coordinate, or +b/-b on a pair."""
        if self.zero_sum:
            b = min(self.hi, -self.lo)
            return b if self.total is None else min(b, self.total / 2)
        return self.amplitude()

    def l2_radius(self, n_in: int) -> float:
        """An upper bound on ||a||_2 over admissible inputs."""
        k = n_in if self.k is None else min(self.k, n_in)
        b = max(abs(self.lo), abs(self.hi))
        if self.zero_sum:
            r = b * math.sqrt(2 * (k // 2)) if math.isfinite(b) else math.inf
            return r if self.total is None else min(r, self.total / math.sqrt(2))
        r = b * math.sqrt(k) if math.isfinite(b) else math.inf
        return r if self.total is None else min(r, self.total)

    def excitable_dim(self, n_in: int) -> int:
        k = n_in if self.k is None else min(self.k, n_in)
        return k - int(self.zero_sum)

    def command_bits(self, n_in: int) -> float:
        """Upper bound on log2(#admissible commands per tick); inf for continuous values."""
        if not self.quantum:
            return math.inf
        q = self.quantum
        vals = [m for m in range(int(math.floor(self.lo / q)), int(math.ceil(self.hi / q)) + 1)
                if m != 0 and self.lo - 1e-12 <= m * q <= self.hi + 1e-12]
        k = n_in if self.k is None else min(self.k, n_in)
        n = sum(math.comb(n_in, j) * len(vals) ** j for j in range(k + 1))
        return math.log2(n)


@dataclass(frozen=True)
class ObservationSpec:
    """Declared, public observation constraints (coordinate-wise, hence permutation invariant).

    noise        additive Gaussian noise std on every observed coordinate
    quantum      observation quantisation step (None: none)
    clip         (lo, hi) saturation range (None: none)
    sign_flip    hidden sign flips of observation coordinates (VW-0 default False)
    max_queries  max query times per program (None: no limit)
    """
    noise: float = 0.0
    quantum: Optional[float] = None
    clip: Optional[tuple] = None
    sign_flip: bool = False
    max_queries: Optional[int] = None

    @property
    def resolution_var(self) -> float:
        return self.noise ** 2 + ((self.quantum ** 2) / 12.0 if self.quantum else 0.0)


# --------------------------------------------------------------------------- world spec
@dataclass
class WorldSpec:
    """Everything that defines a world. All callables are batched over members (axis 0).

    law(h0 (B,n0), xi (B,noise_dim)) -> (B,n0)     level-0 law F0; xi are standard normals
    coarse(h0 (B,n0), m (B,n_m)) -> (B,n1)         coarse-graining Phi (fixed, many-to-one)
    init(rng) -> (n0,)                             one initial level-0 state
    memory_init(h0) -> (B,n_m); memory_update(m, h0_new) -> (B,n_m)   optional tracking memory
    n_u, actuable                                  actuator space (default: level-0 coords) and
                                                   the coordinates the agent can reach
    kick(h0 (B,n0), u (B,n_u)) -> (B,n0)           how inputs enter (default h0 + u)
    invariants {name: f(h0) -> (B,)}               declared conserved quantities (designer check)
    render(h1 (n1,)) -> anything                   designer-only, un-permuted rendering hook
    """
    n0: int
    n1: int
    law: Callable
    coarse: Callable
    init: Callable
    noise_dim: int = 0
    n_m: int = 0
    memory_init: Optional[Callable] = None
    memory_update: Optional[Callable] = None
    n_u: Optional[int] = None
    actuable: Optional[Sequence[int]] = None
    kick: Optional[Callable] = None
    inputs: InputConstraints = field(default_factory=InputConstraints)
    observation: ObservationSpec = field(default_factory=ObservationSpec)
    burn_in: int = 0
    replay: str = "initial"
    max_ticks: Optional[int] = None
    invariants: Mapping[str, Callable] = field(default_factory=dict)
    render: Optional[Callable] = None
    name: str = "world"
    notes: str = ""

    def __post_init__(self):
        if self.n_u is None:
            self.n_u = self.n0
        if self.kick is None and self.n_u != self.n0:
            raise ValueError("WorldSpec: a custom kick is required when n_u != n0")
        if self.replay not in ("none", "initial", "full"):
            raise ValueError("WorldSpec: replay must be 'none', 'initial' or 'full'")
        if (self.memory_init is None) != (self.memory_update is None):
            raise ValueError("WorldSpec: give both memory_init and memory_update, or neither")
        if self.memory_init is None and self.n_m != 0:
            raise ValueError("WorldSpec: n_m > 0 needs memory functions")


# --------------------------------------------------------------------------- ensemble
class Ensemble:
    """B members of one world, simulated in lockstep with privileged access (designer side).

    Members sharing (seed, key) receive identical process, actuation and observation noise.
    """

    def __init__(self, world: "VectorWorld", h0, m, seed: tuple, keys, tick: int):
        self.world = world
        self.h0 = np.asarray(h0, float)
        self.m = np.asarray(m, float).reshape(self.h0.shape[0], -1)
        self.seed = tuple(int(s) for s in seed)
        self.keys = np.asarray(keys, np.int64)
        self.tick = int(tick)

    @property
    def B(self) -> int:
        return self.h0.shape[0]

    @property
    def t(self) -> int:
        """Agent time (0 at the end of the burn-in)."""
        return self.tick - self.world.spec.burn_in

    def normals(self, stream: int, dim: int) -> np.ndarray:
        if dim == 0:
            return np.zeros((self.B, 0))
        K = int(self.keys.max()) + 1
        return _rng(stream, *self.seed, self.tick).standard_normal((K, dim))[self.keys]

    def step(self, a=None) -> "Ensemble":
        """Advance one tick. a: None, (n_in,) shared, or (B, n_in) per member (agent coords).
        No constraint checking here: the designer may apply any input."""
        spec = self.world.spec
        h = self.h0
        if a is not None:
            a = np.asarray(a, float)
            if a.ndim == 1:
                a = np.broadcast_to(a, (self.B, a.shape[0]))
            if np.any(a):
                if spec.inputs.noise > 0:
                    mask = a != 0
                    a2 = a * (1.0 + spec.inputs.noise * self.normals(_S_ACT, a.shape[1]))
                    if spec.inputs.zero_sum:
                        cnt = np.maximum(mask.sum(1, keepdims=True), 1)
                        a2 = a2 - mask * (a2.sum(1, keepdims=True) / cnt)
                    a = a2
                u = np.zeros((self.B, spec.n_u))
                u[:, self.world.in_map] = a
                h = spec.kick(h, u) if spec.kick is not None else h + u
        h = np.asarray(spec.law(h, self.normals(_S_PROC, spec.noise_dim)), float)
        self.tick += 1
        if spec.memory_update is not None:
            self.m = np.asarray(spec.memory_update(self.m, h), float).reshape(self.B, -1)
        self.h0 = h
        return self

    def h1(self) -> np.ndarray:
        """Level-1 vectors in the designer's (true, un-permuted) basis."""
        return np.asarray(self.world.spec.coarse(self.h0, self.m), float)

    def h1_agent(self) -> np.ndarray:
        """Noise-free level-1 vectors in the agent's observation coordinates."""
        return self.h1()[:, self.world.out_map] * self.world.out_sign

    def observe(self) -> np.ndarray:
        ob = self.world.spec.observation
        y = self.h1_agent()
        if ob.noise > 0:
            y = y + ob.noise * self.normals(_S_OBS, y.shape[1])
        if ob.clip is not None:
            y = np.clip(y, ob.clip[0], ob.clip[1])
        if ob.quantum:
            y = ob.quantum * np.round(y / ob.quantum)
        return y

    def clone(self, rep: int = 1, idx=None, fresh: bool = False) -> "Ensemble":
        """Copies of members idx, each repeated rep times (member-major order).
        fresh=False: copies share their parent's noise (identical noise);
        fresh=True: every copy gets new, independent noise."""
        idx = np.arange(self.B) if idx is None else np.asarray(idx)
        sel = np.repeat(idx, rep)
        if fresh:
            seed, keys = self.world._fresh_seed(), np.arange(sel.size)
        else:
            seed, keys = self.seed, self.keys[sel].copy()
        return Ensemble(self.world, self.h0[sel].copy(), self.m[sel].copy(), seed, keys, self.tick)

    def invariants(self) -> dict:
        return {k: np.asarray(f(self.h0), float) for k, f in self.world.spec.invariants.items()}


# --------------------------------------------------------------------------- world
class VectorWorld:
    """A VW-0 world instance: a WorldSpec plus hidden permutations drawn from world_seed."""

    def __init__(self, spec: WorldSpec, world_seed: int = 0):
        self.spec = spec
        self.world_seed = int(world_seed)
        rng = _rng(_S_PERM, self.world_seed)
        act = np.arange(spec.n_u) if spec.actuable is None else np.asarray(spec.actuable, int)
        if act.size == 0 or act.min() < 0 or act.max() >= spec.n_u or np.unique(act).size != act.size:
            raise ValueError("WorldSpec.actuable must be distinct indices in [0, n_u)")
        self.in_map = act[rng.permutation(act.size)]          # agent input j -> actuator index
        self.out_map = rng.permutation(spec.n1)                 # agent obs j  <- level-1 index
        self.out_sign = (rng.choice([-1.0, 1.0], spec.n1) if spec.observation.sign_flip
                         else np.ones(spec.n1))
        self._ep: Optional[Ensemble] = None
        self._ep_count = 0
        self._last_in: Optional[int] = None
        self._spent = 0.0
        self.ticks_used = 0
        self._branch_count = 0
        self._designer_count = 0

    # ------------------------------------------------------------- agent-facing
    @property
    def n_in(self) -> int:
        return int(self.in_map.size)

    @property
    def n_obs(self) -> int:
        return int(self.spec.n1)

    @property
    def t(self) -> Optional[int]:
        return None if self._ep is None else self._ep.t

    def card(self) -> dict:
        """The public world card: everything the agent is told."""
        s = self.spec
        return {
            "contract": CONTRACT, "name": s.name, "n_in": self.n_in, "n_obs": self.n_obs,
            "inputs": asdict(s.inputs), "observation": asdict(s.observation),
            "replay": s.replay, "max_ticks": s.max_ticks, "ticks_used": self.ticks_used,
            "timing": "an input given at tick t is added to level 0 before the law runs; "
                      "its effect can appear from o(t+1) on",
            "notes": s.notes,
        }

    def reset(self, seed: int) -> np.ndarray:
        """Start an episode. Returns o(0). Free (no ticks charged)."""
        seed = self._check_seed(seed)
        self._ep_count += 1
        mode = self.spec.replay
        if mode == "full":
            si = sd = (_NS_EPISODE, seed)
        elif mode == "initial":
            si, sd = (_NS_EPISODE, seed), (_NS_EPISODE_FRESH, seed, self._ep_count)
        else:
            si = sd = (_NS_EPISODE_FRESH, seed, self._ep_count)
        self._ep = self._new_ensemble(1, si, sd)
        self._last_in, self._spent = None, 0.0
        return self._ep.observe()[0]

    def step(self, inp=None) -> np.ndarray:
        """One tick. inp: None | {agent coord: value} | dense vector of length n_in.
        Returns o(t+1). Violations raise InputViolation; nothing runs or is charged."""
        ep = self._require_episode()
        a = self.spec.inputs.normalize(inp, self.n_in)
        self.spec.inputs.check(a, ep.t, self._last_in, self._spent)
        self._check_budget(1)
        ep.step(self._dense(a) if a else None)
        self.ticks_used += 1
        if a:
            self._last_in = ep.t - 1
            self._spent += sum(abs(v) for v in a.values())
        return ep.observe()[0]

    def run(self, program, query_times, seed: Optional[int] = None) -> np.ndarray:
        """Run a program of timed inputs and return o at the query times.

        program      iterable of (t, input) or {t: input}; t >= 0 relative to the start
        query_times  integer times >= 0 relative to the start (0 = the starting observation)
        seed         if given, reset(seed) first; otherwise continue the current episode
        Returns an array (len(query_times), n_obs) in the order of query_times. The whole
        program is validated first; on any violation nothing runs and nothing is charged."""
        q = [int(x) for x in query_times]
        if not q or min(q) < 0:
            raise InputViolation("format: query_times must be a non-empty list of integers >= 0")
        mq = self.spec.observation.max_queries
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
        want = set(q)
        got = {0: ep.observe()[0]} if 0 in want else {}
        pdict = dict(prog)
        for s in range(H):
            a = pdict.get(s)
            ep.step(self._dense(a) if a else None)
            self.ticks_used += 1
            if a:
                self._last_in = ep.t - 1
                self._spent += sum(abs(v) for v in a.values())
            if s + 1 in want:
                got[s + 1] = ep.observe()[0]
        return np.stack([got[x] for x in q])

    # ------------------------------------------------------------- internals
    def _check_seed(self, seed) -> int:
        if isinstance(seed, bool) or not isinstance(seed, (int, np.integer)) or not 0 <= seed < MAX_SEED:
            raise ValueError(f"seed must be an integer in [0, 2**62), got {seed!r}")
        return int(seed)

    def _require_episode(self) -> Ensemble:
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
        C = self.spec.inputs
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
            last, spent = t0 + t, spent + sum(abs(v) for v in a.values())
            out.append((t, a))
        return out

    def _new_ensemble(self, B: int, seed_init: tuple, seed_dyn: Optional[tuple] = None) -> Ensemble:
        spec = self.spec
        h0 = np.stack([np.asarray(spec.init(_rng(_S_INIT, *seed_init, j)), float).reshape(spec.n0)
                       for j in range(B)])
        m = (np.asarray(spec.memory_init(h0), float).reshape(B, -1) if spec.memory_init
             else np.zeros((B, 0)))
        ens = Ensemble(self, h0, m, seed_init, np.arange(B), 0)
        for _ in range(spec.burn_in):
            ens.step(None)
        if seed_dyn is not None:
            ens.seed = tuple(int(s) for s in seed_dyn)
        return ens

    def _fresh_seed(self) -> tuple:
        self._branch_count += 1
        return (_NS_BRANCH, self._branch_count)

    @property
    def designer(self) -> "Designer":
        return Designer(self)


# --------------------------------------------------------------------------- statistics helpers
def logdet(S: np.ndarray, dof: Optional[float] = None) -> float:
    """log det S; with dof, the Wishart-unbiased version for S = (residual scatter)/dof."""
    sign, ld = np.linalg.slogdet(S)
    if sign <= 0:
        return -math.inf
    if dof is None or not math.isfinite(dof):
        return float(ld)
    q = S.shape[0]
    i = np.arange(1, q + 1)
    return float(ld - (q * math.log(2.0 / dof) + digamma((dof - i + 1) / 2.0).sum()))


def ols_residuals(X: np.ndarray, Y: np.ndarray):
    """Least-squares residuals of Y on [1, X]; returns (E, dof)."""
    N = Y.shape[0]
    Xc = np.ones((N, 1)) if X.shape[1] == 0 else np.column_stack([np.ones(N), X])
    coef, _, rank, _ = np.linalg.lstsq(Xc, Y, rcond=None)
    return Y - Xc @ coef, N - rank


def within_cov(Y: np.ndarray):
    """Y (N, R, q): average within-group covariance (ddof 1); returns (S, dof)."""
    N, R, _ = Y.shape
    D = Y - Y.mean(1, keepdims=True)
    return np.einsum("nri,nrj->ij", D, D) / (N * (R - 1)), N * (R - 1)


def inv_sqrt(S: np.ndarray, floor: float = 1e-12) -> np.ndarray:
    w, U = np.linalg.eigh((S + S.T) / 2)
    w = np.maximum(w, floor * max(w.max(), 1e-300))
    return (U / np.sqrt(w)) @ U.T


def whiten_basis(S: np.ndarray, tol: float = 1e-9, n_pc: Optional[int] = None) -> np.ndarray:
    """W (n, r) with W^T S W = I on the numerical support of S (top n_pc directions if given)."""
    w, U = np.linalg.eigh((S + S.T) / 2)
    order = np.argsort(w)[::-1]
    w, U = w[order], U[:, order]
    keep = w > tol * w[0]
    if n_pc is not None:
        keep[n_pc:] = False
    return U[:, keep] / np.sqrt(w[keep])


def leak_spectrum(S_post: np.ndarray, S_prior: np.ndarray, tol: float = 1e-9,
                  n_pc: Optional[int] = None) -> np.ndarray:
    """Eigenvalues of the posterior covariance in prior-whitened coordinates (ascending)."""
    W = whiten_basis(S_prior, tol, n_pc)
    return np.sort(np.linalg.eigvalsh(W.T @ S_post @ W))


def waterfill(gains, power: float):
    """Capacity (nats) of parallel channels y_i = sqrt(g_i) x_i + N(0,1) with sum E x_i^2 <= power."""
    g = np.sort(np.asarray(gains, float))[::-1]
    g = g[g > 1e-300]
    if power <= 0 or g.size == 0 or not math.isfinite(power):
        return (0.0 if power <= 0 or g.size == 0 else math.inf), 0
    inv = 1.0 / g
    for n in range(g.size, 0, -1):
        mu = (power + inv[:n].sum()) / n
        if mu > inv[n - 1]:
            break
    p = np.maximum(mu - inv, 0.0)
    return float(0.5 * np.sum(np.log1p(g * p))), int((p > 0).sum())


def capacity_from_response(G: np.ndarray, S_noise: np.ndarray, C: InputConstraints, n_in: int,
                           max_pairs: int = 4000, seed: int = 0) -> dict:
    """Input-capacity numbers from a one-tick response G (n_obs*L, n_in) and the agent-relevant
    noise covariance S_noise of the same level-1 future block."""
    Wn = inv_sqrt(S_noise)
    R = Wn @ G
    if C.zero_sum:
        Q, _ = np.linalg.qr(np.column_stack([np.ones(n_in), np.eye(n_in)[:, : n_in - 1]]))
        Qb = Q[:, 1:]
    else:
        Qb = np.eye(n_in)
    sv = np.linalg.svd(R @ Qb, compute_uv=False)
    b, rho, ba = C.amplitude(), C.l2_radius(n_in), C.atom_amplitude()
    cap, n_act = waterfill(sv ** 2, rho ** 2)
    if C.zero_sum:
        pairs = [(i, j) for i in range(n_in) for j in range(i + 1, n_in)]
        if len(pairs) > max_pairs:
            sel = np.random.default_rng(seed).choice(len(pairs), max_pairs, replace=False)
            pairs = [pairs[s] for s in sel]
        I = np.array([p[0] for p in pairs])
        J = np.array([p[1] for p in pairs])
        snr = ba ** 2 * ((R[:, I] - R[:, J]) ** 2).sum(0)
    else:
        snr = ba ** 2 * (R ** 2).sum(0)
    d_exc = C.excitable_dim(n_in)
    d_vis = int((b * sv >= 1.0).sum())
    return {
        "excitable_dim_per_tick": d_exc,
        "singular_values": sv,
        "visible_dim": d_vis,
        "visible_dim_per_tick": min(d_exc, d_vis),
        "capacity_bits_upper": cap / math.log(2),
        "capacity_channels": n_act,
        "l2_radius": rho,
        "atom_snr_median": float(np.median(snr)), "atom_snr_min": float(snr.min()),
        "atom_snr_max": float(snr.max()), "atom_visible_frac": float((snr >= 1.0).mean()),
        "command_bits_upper": C.command_bits(n_in),
    }


def closure_tables(Se: dict, Se_dof: dict, Su: dict, Su_dof: dict, horizons, pasts,
                   Seb: Optional[dict] = None, Seb_dof: Optional[dict] = None,
                   Sub: Optional[dict] = None, Sub_dof: Optional[dict] = None, blocks=()) -> dict:
    """Closure numbers from error covariances. Se[(tau,p)]: level-1-only predictor (past window
    p) of o(t+tau); Su[tau]: oracle with (h0(t), m(t)). Dof None means exact (closed form)."""
    H, P = list(horizons), list(pasts)
    V0 = np.array([np.trace(Se[(h, 0)]) if (h, 0) in Se else np.nan for h in H])
    Vu = np.array([np.trace(Su[h]) for h in H])
    Ve = np.array([[np.trace(Se[(h, p)]) for p in P] for h in H])
    gap = np.array([[0.5 * (logdet(Se[(h, p)], Se_dof.get((h, p))) - logdet(Su[h], Su_dof.get(h)))
                     for p in P] for h in H])
    with np.errstate(divide="ignore", invalid="ignore"):
        ceiling = (V0[:, None] - Ve) / (V0[:, None] - Vu[:, None])
        predictable = (V0[:, None] - Ve) / V0[:, None]
    out = {"horizons": H, "pasts": P, "V0": V0, "Vu": Vu, "Ve": Ve, "gap_nats": gap,
           "ceiling": ceiling, "predictable": predictable}
    if 1 in H and 1 in P:
        i, j1, jm = H.index(1), P.index(1), len(P) - 1
        out["atay"] = {"leak": gap[i, j1], "residual": gap[i, jm], "memory": gap[i, j1] - gap[i, jm],
                       "p_max": P[jm]}
    if blocks:
        out["blocks"] = list(blocks)
        out["block_gap_nats"] = np.array(
            [[0.5 * (logdet(Seb[(L, p)], (Seb_dof or {}).get((L, p))) - logdet(Sub[L], (Sub_dof or {}).get(L)))
              for p in P] for L in blocks])
    return out


def _avg_tables(tabs: list, keys: Sequence[str]) -> dict:
    out = dict(tabs[0])
    for k in keys:
        if k in tabs[0]:
            out[k] = np.mean([t[k] for t in tabs], axis=0)
    if "atay" in tabs[0]:
        out["atay"] = {k: (float(np.mean([t["atay"][k] for t in tabs])) if k != "p_max" else tabs[0]["atay"][k])
                       for k in tabs[0]["atay"]}
    return out


_TABLE_KEYS = ("V0", "Vu", "Ve", "gap_nats", "ceiling", "predictable", "block_gap_nats")


# --------------------------------------------------------------------------- designer
class Designer:
    """Privileged, designer-side access to a VectorWorld (never shown to the agent)."""

    def __init__(self, world: VectorWorld):
        self.w = world

    # ---- privileged state and ensembles ----
    def state(self) -> dict:
        ep = self.w._require_episode()
        return {"t": ep.t, "h0": ep.h0[0].copy(), "m": ep.m[0].copy(), "h1": ep.h1()[0],
                "in_map": self.w.in_map.copy(), "out_map": self.w.out_map.copy(),
                "out_sign": self.w.out_sign.copy()}

    def branch(self, rep: int = 1, fresh: bool = False) -> Ensemble:
        """Copies of the agent's current episode (identical noise unless fresh)."""
        return self.w._require_episode().clone(rep=rep, fresh=fresh)

    def ensemble(self, B: int, seed=None) -> Ensemble:
        """B independent members from the declared initial distribution (after burn-in)."""
        if seed is None:
            self.w._designer_count += 1
            seed = (self.w._designer_count,)
        seed = (_NS_DESIGNER,) + (tuple(seed) if isinstance(seed, (tuple, list)) else (int(seed),))
        return self.w._new_ensemble(B, seed)

    def from_states(self, h0, m=None, tick: Optional[int] = None) -> Ensemble:
        """An ensemble placed in given level-0 states (memory initialised from them if absent)."""
        spec = self.w.spec
        h0 = np.atleast_2d(np.array(h0, float))
        if m is None:
            m = spec.memory_init(h0) if spec.memory_init else np.zeros((h0.shape[0], 0))
        return Ensemble(self.w, h0, m, self.w._fresh_seed(), np.arange(h0.shape[0]),
                        spec.burn_in if tick is None else tick)

    # ---- programs ----
    def program_dense(self, program, H: int, validate: bool = True) -> np.ndarray:
        P = np.zeros((max(H, 0), self.w.n_in))
        if not program:
            return P
        H_all = max([H] + [int(e[0]) + 1 for e in program])      # validate the whole program
        prog = (self.w._validate_program(program, 0, None, 0.0, H_all) if validate else
                [(int(t), self.w.spec.inputs.normalize(a, self.w.n_in)) for t, a in program])
        for t, a in prog:
            if 0 <= t < H:
                for j, v in a.items():
                    P[t, j] = v
        return P

    def random_program(self, rng: np.random.Generator, H: int, rate: float = 0.5) -> list:
        """Random admissible program over [0, H): at each allowed tick, with probability
        `rate`, a random admissible input (full support k, uniform values)."""
        C, prog, last, spent = self.w.spec.inputs, [], None, 0.0
        for t in range(H):
            if rng.random() >= rate or (last is not None and t - last < C.min_interval):
                continue
            a = C.sample(rng, self.w.n_in)
            l1 = sum(abs(v) for v in a.values())
            if not a or (C.episode_budget is not None and spent + l1 > C.episode_budget):
                continue
            prog.append((t, a))
            last, spent = t, spent + l1
        return prog

    def rollout(self, ens: Ensemble, P: Optional[np.ndarray], t_end: int, obs=(), h0=(), h1=()) -> dict:
        """Advance ens to agent time t_end applying dense program rows P[t]; record o, h0 and
        noise-free agent-basis h1 at the requested agent times."""
        obs, h0, h1 = set(obs), set(h0), set(h1)
        rec = {"obs": {}, "h0": {}, "h1": {}}

        def grab():
            t = ens.t
            if t in obs:
                rec["obs"][t] = ens.observe()
            if t in h0:
                rec["h0"][t] = ens.h0.copy()
            if t in h1:
                rec["h1"][t] = ens.h1_agent()

        grab()
        while ens.t < t_end:
            t = ens.t
            a = P[t] if (P is not None and 0 <= t < len(P) and np.any(P[t])) else None
            ens.step(a)
            grab()
        return rec

    # ---- certificate 1: closure ceiling ----
    def closure(self, horizons=(1, 2, 4, 8, 16), pasts=(0, 1, 2, 4, 8, 16), blocks=(),
                n_traj: int = 20000, n_oracle: int = 4000, n_rep: int = 16, programs=None,
                n_programs: int = 0, rate: float = 0.5, folds: int = 8, seed: int = 0) -> dict:
        """Level-1-only predictor (past window p, linear) versus the oracle with privileged
        (h0(t), m(t)) (Monte Carlo over n_rep fresh-noise branches), conditional on an
        open-loop program, at several horizons and pasts; plus block futures o(t+1..t+L).
        Returns tables averaged over programs, fold standard errors and per-program tables."""
        horizons, pasts, blocks = sorted(set(horizons)), sorted(set(pasts) | {0}), sorted(set(blocks))
        pmax = max(pasts)
        t0 = max(pmax - 1, 0)
        taus = sorted(set(horizons) | set(range(1, (max(blocks) if blocks else 0) + 1)))
        H = t0 + max(taus)
        rng = _rng(_S_MISC, 11, seed)
        progs = [[]] if programs is None else [list(p) for p in programs]
        progs += [self.random_program(rng, H, rate) for _ in range(n_programs)]
        n_or = min(n_oracle, n_traj)
        per, per_se = [], []
        for pi, prog in enumerate(progs):
            P = self.program_dense(prog, H)
            ens = self.ensemble(n_traj, seed=(11, seed, pi))
            rec = self.rollout(ens, P, t0, obs=range(t0 + 1))
            past = np.stack([rec["obs"][t] for t in range(t0 + 1)], axis=1)
            orc = ens.clone(rep=n_rep, idx=np.arange(n_or), fresh=True)
            fut = self.rollout(ens, P, t0 + max(taus), obs=[t0 + s for s in taus])["obs"]
            ofut = self.rollout(orc, P, t0 + max(taus), obs=[t0 + s for s in taus])["obs"]
            Y = {s: fut[t0 + s] for s in taus}
            Yo = {s: ofut[t0 + s].reshape(n_or, n_rep, -1) for s in taus}
            Yb = {L: np.concatenate([Y[s] for s in range(1, L + 1)], 1) for L in blocks}
            Yob = {L: np.concatenate([Yo[s] for s in range(1, L + 1)], 2) for L in blocks}
            fold_m = np.array_split(_rng(_S_MISC, 12, seed, pi).permutation(n_traj), folds)
            fold_o = np.array_split(_rng(_S_MISC, 13, seed, pi).permutation(n_or), folds)
            tabs = []
            for f in range(folds + 1):
                im = np.arange(n_traj) if f == folds else fold_m[f]
                io = np.arange(n_or) if f == folds else fold_o[f]
                Se, Sed, Seb, Sebd = {}, {}, {}, {}
                cols = [Y[s][im] for s in horizons] + [Yb[L][im] for L in blocks]
                widths = [c.shape[1] for c in cols]
                Ybig = np.concatenate(cols, 1)
                for p in pasts:
                    X = past[im, t0 + 1 - p:, :].reshape(im.size, -1) if p > 0 else np.zeros((im.size, 0))
                    E, dof = ols_residuals(X, Ybig)
                    o = 0
                    for c, w in enumerate(widths):
                        Ec = E[:, o:o + w]
                        o += w
                        S = Ec.T @ Ec / dof
                        if c < len(horizons):
                            Se[(horizons[c], p)], Sed[(horizons[c], p)] = S, dof
                        else:
                            L = blocks[c - len(horizons)]
                            Seb[(L, p)], Sebd[(L, p)] = S, dof
                Su, Sud, Sub, Subd = {}, {}, {}, {}
                for s in horizons:
                    Su[s], Sud[s] = within_cov(Yo[s][io])
                for L in blocks:
                    Sub[L], Subd[L] = within_cov(Yob[L][io])
                tabs.append(closure_tables(Se, Sed, Su, Sud, horizons, pasts, Seb, Sebd, Sub, Subd, blocks))
            full, fl = tabs[-1], tabs[:-1]
            se = {k: np.std([t[k] for t in fl], axis=0, ddof=1) / math.sqrt(folds)
                  for k in _TABLE_KEYS if k in full}
            per.append(full)
            per_se.append(se)
        out = _avg_tables(per, _TABLE_KEYS)
        out["se"] = {k: np.sqrt(np.sum([s[k] ** 2 for s in per_se], axis=0)) / len(per_se) for k in per_se[0]}
        out["per_program"] = per
        out["n_programs"] = len(progs)
        return out

    # ---- certificate 2: leak (readability of level 0 from level-1 pasts) ----
    def leak(self, pasts=(0, 1, 2, 4, 8, 16), n_traj: int = 20000, program=None, n_pc: Optional[int] = None,
             threshold: float = 0.5, seed: int = 0) -> dict:
        """Gaussian-proxy posterior of h0(t) given the level-1 window o(t-p+1..t) (linear
        regression, designer has h0), in prior-whitened coordinates. mu_i = 1: direction
        hidden; mu_i -> 0: direction read off. info = -1/2 sum log mu (nats)."""
        pasts = sorted(set(pasts))
        t0 = max(max(pasts) - 1, 0)
        P = self.program_dense(program or [], t0 + 1)
        ens = self.ensemble(n_traj, seed=(21, seed))
        rec = self.rollout(ens, P, t0, obs=range(t0 + 1), h0=[t0])
        past = np.stack([rec["obs"][t] for t in range(t0 + 1)], axis=1)
        h = rec["h0"][t0]
        Sh = np.cov(h.T, ddof=1).reshape(h.shape[1], h.shape[1])
        W = whiten_basis(Sh, n_pc=n_pc)
        Z = (h - h.mean(0)) @ W
        r = Z.shape[1]
        mus, info, dims = [], [], []
        for p in pasts:
            X = past[:, t0 + 1 - p:, :].reshape(n_traj, -1) if p > 0 else np.zeros((n_traj, 0))
            E, dof = ols_residuals(X, Z)
            S = E.T @ E / dof
            mu = np.sort(np.linalg.eigvalsh(S))
            mus.append(mu)
            info.append(0.5 * (logdet(np.eye(r), n_traj - 1) - logdet(S, dof)))
            dims.append(int((mu < threshold).sum()))
        return {"pasts": pasts, "rank": r, "mu": mus, "info_nats": np.array(info), "dim": np.array(dims),
                "threshold": threshold, "hidden_frac": 1.0 - np.array(dims) / max(r, 1)}

    # ---- certificate 3: input capacity ----
    def input_capacity(self, L: int = 8, p: int = 8, n_states: int = 8, n_traj: int = 20000,
                       delta: Optional[float] = None, program=None, seed: int = 0) -> dict:
        """One-tick response of the noise-free level-1 future o(t+1..t+L) to each agent input
        coordinate (branches with identical noise; designer may apply any input), whitened by
        the level-1-only prediction-error covariance of that future block (past window p)."""
        C, n = self.w.spec.inputs, self.w.n_in
        delta = C.amplitude() if delta is None else delta
        t0 = max(p - 1, 0)
        P = self.program_dense(program or [], t0 + L)
        base = self.ensemble(n_states, seed=(31, seed))
        self.rollout(base, P, t0)
        cp = base.clone(rep=n + 1)
        A = np.tile(P[t0], (cp.B, 1)) if len(P) > t0 else np.zeros((cp.B, n))
        for s in range(n_states):
            A[s * (n + 1) + 1 + np.arange(n), np.arange(n)] += delta
        cp.step(A)
        rec = self.rollout(cp, P, t0 + L, h1=range(t0 + 1, t0 + L + 1))
        Yr = np.stack([rec["h1"][t0 + s] for s in range(1, L + 1)], 1).reshape(n_states, n + 1, L, -1)
        G = ((Yr[:, 1:] - Yr[:, :1]) / delta).mean(0)            # (n, L, n_obs)
        Gblk = G.reshape(n, -1).T                                 # (L*n_obs, n)
        ens = self.ensemble(n_traj, seed=(32, seed))
        rec = self.rollout(ens, P, t0 + L, obs=range(t0 + L + 1))
        X = (np.stack([rec["obs"][t] for t in range(t0 + 1 - p, t0 + 1)], 1).reshape(n_traj, -1)
             if p > 0 else np.zeros((n_traj, 0)))
        Yb = np.concatenate([rec["obs"][t0 + s] for s in range(1, L + 1)], 1)
        E, dof = ols_residuals(X, Yb)
        out = capacity_from_response(Gblk, E.T @ E / dof, C, n, seed=seed)
        out.update({"L": L, "p": p, "response": Gblk})
        return out

    # ---- certificate 4: observation capacity ----
    def observation_capacity(self, pasts=(1, 16), n_traj: int = 20000, program=None, seed: int = 0) -> dict:
        """Information the next observation carries about the hidden state beyond a past
        window, r(p) = I(o(t+1); h0(t+1), m(t+1) | o window) (Gaussian proxy, nats/tick), and the
        coordinate-wise channel bound sum_j 1/2 log(1 + Var h1_j / resolution variance)."""
        pasts = sorted(set(pasts))
        var = self.w.spec.observation.resolution_var
        t0 = max(max(pasts) - 1, 0)
        P = self.program_dense(program or [], t0 + 1)
        ens = self.ensemble(n_traj, seed=(41, seed))
        rec = self.rollout(ens, P, t0 + 1, obs=range(t0 + 2), h1=[t0])
        past = np.stack([rec["obs"][t] for t in range(t0 + 1)], axis=1)
        y = rec["obs"][t0 + 1]
        n_obs = y.shape[1]
        rates = []
        for p in pasts:
            X = past[:, t0 + 1 - p:, :].reshape(n_traj, -1) if p > 0 else np.zeros((n_traj, 0))
            E, dof = ols_residuals(X, y)
            rates.append(math.inf if var <= 0 else 0.5 * (logdet(E.T @ E / dof, dof) - n_obs * math.log(var)))
        v1 = rec["h1"][t0].var(0, ddof=1)
        raw = math.inf if var <= 0 else float(0.5 * np.log2(1 + v1 / var).sum())
        return {"pasts": pasts, "rate_bits": np.array(rates) / math.log(2), "channel_bits_upper": raw,
                "resolution_var": var}

    # ---- invariants ----
    def invariant_drift(self, T: int = 100, B: int = 64, seed: int = 0) -> dict:
        ens = self.ensemble(B, seed=(51, seed))
        I0 = ens.invariants()
        self.rollout(ens, None, ens.t + T)
        I1 = ens.invariants()
        return {k: float(np.abs(I1[k] - I0[k]).max()) for k in I0}

    # ---- bundle ----
    def certify(self, horizons=(1, 2, 4, 8, 16), pasts=(0, 1, 2, 4, 8, 16), n_traj: int = 20000,
                n_programs: int = 2, L: int = 8, seed: int = 0, thresholds: Optional[dict] = None) -> dict:
        """All four certificates plus provisional VW-0 admission flags."""
        th = {"predictable_min": 0.1, "ceiling_min": 0.5, "hidden_frac_min": 0.5, "atom_snr_min": 1.0}
        th.update(thresholds or {})
        cl = self.closure(horizons, pasts, blocks=(L,), n_traj=n_traj, n_programs=n_programs, seed=seed)
        lk = self.leak(pasts, n_traj=n_traj, seed=seed)
        ic = self.input_capacity(L=L, p=max(pasts), n_traj=n_traj, seed=seed)
        oc = self.observation_capacity((1, max(pasts)), n_traj=n_traj, seed=seed)
        i1 = cl["horizons"].index(min(cl["horizons"]))
        drift = self.invariant_drift() if self.w.spec.invariants else {}
        flags = {
            "invariants_conserved": bool(all(v <= th.get("invariant_tol", 1e-6) for v in drift.values())),
            "finite_resolution": self.w.spec.observation.resolution_var > 0,
            "nontrivial": bool(cl["predictable"][i1, -1] >= th["predictable_min"]),
            "is_a_level": bool(cl["ceiling"][i1, -1] >= th["ceiling_min"]),
            "level0_hidden": bool(lk["hidden_frac"][-1] >= th["hidden_frac_min"]),
            "inputs_visible": bool(ic["atom_snr_max"] >= th["atom_snr_min"]),
        }
        return {"contract": CONTRACT, "world": self.w.spec.name, "closure": cl, "leak": lk,
                "input_capacity": ic, "observation_capacity": oc,
                "invariant_drift": drift,
                "flags": flags, "thresholds": th}


# --------------------------------------------------------------------------- exam
class Exam:
    """Held-out prediction exam. Each item: a reserved-seed episode, a prefix program run by the
    harness (the agent sees o(0..prefix) and the prefix inputs), then a test program and query
    times relative to the end of the prefix. Scored against n_rep replicate futures drawn from
    the same hidden state with fresh noise."""

    def __init__(self, world: VectorWorld, n_items: int = 64, prefix: int = 16, horizon: int = 32,
                 queries: Optional[Sequence[int]] = None, rate: float = 0.5, exam_seed: int = 0,
                 sampler: Optional[Callable] = None):
        self.w, d = world, world.designer
        self.prefix, self.horizon = prefix, horizon
        self.queries = sorted(set(queries)) if queries else [q for q in (1, 2, 4, 8, 16, 32, 64, 128) if q <= horizon]
        self.items, self._snap, self._dense = [], [], []
        for i in range(n_items):
            rng = _rng(_S_MISC, 61, exam_seed, i)
            full = (sampler or d.random_program)(rng, prefix + horizon, rate)
            Pd = d.program_dense(full, prefix + horizon)
            ens = world._new_ensemble(1, (_NS_EXAM, exam_seed, i), (_NS_EXAM, exam_seed, i))
            rec = d.rollout(ens, Pd, prefix, obs=range(prefix + 1))
            self._snap.append(ens)
            self._dense.append(Pd)
            self.items.append({
                "past_obs": np.stack([rec["obs"][t][0] for t in range(prefix + 1)]),
                "past_program": [(t, a) for t, a in full if t < prefix],
                "program": [(t - prefix, a) for t, a in full if t >= prefix],
                "query_times": list(self.queries),
            })

    def public(self) -> list:
        return [dict(it) for it in self.items]

    def score(self, predictions: Optional[list] = None, n_rep: int = 32,
              references: Optional[Mapping[str, Callable]] = None, ceiling: Optional[str] = None) -> dict:
        """predictions: per item an array (len(queries), n_obs), or None. references: name ->
        callable(item) -> same shape (designer predictors). MSE is the expected squared error
        over replicate futures; 'oracle' is the replicate variance (the floor with h0 known).
        Skill = (MSE_persistence - MSE)/(MSE_persistence - MSE_ceiling)."""
        d, qs = self.w.designer, self.queries
        preds = {"persistence": [np.tile(it["past_obs"][-1], (len(qs), 1)) for it in self.items]}
        if predictions is not None:
            preds["agent"] = [np.asarray(p, float) for p in predictions]
        for name, f in (references or {}).items():
            preds[name] = [np.asarray(f(it), float) for it in self.items]
        mse = {k: np.zeros((len(self.items), len(qs))) for k in preds}
        orac = np.zeros((len(self.items), len(qs)))
        for i, (snap, Pd) in enumerate(zip(self._snap, self._dense)):
            ens = snap.clone(rep=n_rep, fresh=True)
            rec = d.rollout(ens, Pd, self.prefix + max(qs), obs=[self.prefix + q for q in qs])
            Y = np.stack([rec["obs"][self.prefix + q] for q in qs], 1)       # (R, nq, n_obs)
            orac[i] = ((Y - Y.mean(0)) ** 2).sum((0, 2)) / (n_rep - 1)
            for k in preds:
                mse[k][i] = ((Y - preds[k][i][None]) ** 2).sum(2).mean(0)
        out = {"queries": qs, "oracle": orac.mean(0), "mse": {k: v.mean(0) for k, v in mse.items()},
               "mse_se": {k: v.std(0, ddof=1) / math.sqrt(len(self.items)) for k, v in mse.items()}}
        ref = out["mse"][ceiling] if ceiling else out["oracle"]
        base = out["mse"]["persistence"]
        with np.errstate(divide="ignore", invalid="ignore"):
            out["skill"] = {k: (base - v) / (base - ref) for k, v in out["mse"].items()}
        out["ceiling"] = ceiling or "oracle"
        return out


# --------------------------------------------------------------------------- composition
def _slices(sizes):
    o = np.concatenate([[0], np.cumsum(sizes)]).astype(int)
    return [slice(o[i], o[i + 1]) for i in range(len(sizes))]


def product(*specs: WorldSpec, coupling: Optional[Callable] = None, inputs: Optional[InputConstraints] = None,
            observation: Optional[ObservationSpec] = None, name: Optional[str] = None) -> WorldSpec:
    """Direct sum (coupling=None) or coupled product of worlds. Level 0 is the concatenation;
    the law is blockwise plus coupling(h0_pre) (an exchange term, e.g. diffusive_coupling);
    Phi, memory and actuators are blockwise. The composite is anonymised jointly, so the agent
    is not told which coordinates belong to which block. Default inputs: the first block's
    constraints with k summed."""
    S0, S1, SX, SM, SU = (_slices([s.n0 for s in specs]), _slices([s.n1 for s in specs]),
                          _slices([s.noise_dim for s in specs]), _slices([s.n_m for s in specs]),
                          _slices([s.n_u for s in specs]))

    def law(h, xi):
        out = np.concatenate([s.law(h[:, a], xi[:, x]) for s, a, x in zip(specs, S0, SX)], 1)
        return out if coupling is None else out + coupling(h)

    def coarse(h, m):
        return np.concatenate([s.coarse(h[:, a], m[:, b]) for s, a, b in zip(specs, S0, SM)], 1)

    def init(rng):
        return np.concatenate([np.asarray(s.init(rng), float).reshape(-1) for s in specs])

    has_mem = any(s.memory_init for s in specs)

    def m_init(h):
        return np.concatenate([s.memory_init(h[:, a]) if s.memory_init else np.zeros((h.shape[0], 0))
                               for s, a in zip(specs, S0)], 1)

    def m_upd(m, h):
        return np.concatenate([s.memory_update(m[:, b], h[:, a]) if s.memory_update else m[:, b]
                               for s, a, b in zip(specs, S0, SM)], 1)

    custom = any(s.kick is not None for s in specs)

    def kick(h, u):
        return np.concatenate([(s.kick(h[:, a], u[:, c]) if s.kick else h[:, a] + u[:, c])
                               for s, a, c in zip(specs, S0, SU)], 1)

    act = np.concatenate([(np.arange(s.n_u) if s.actuable is None else np.asarray(s.actuable, int)) + c.start
                          for s, c in zip(specs, SU)])
    if inputs is None:
        ks = [s.inputs.k for s in specs]
        kw = asdict(specs[0].inputs)
        kw["k"] = None if any(k is None for k in ks) else int(sum(ks))
        inputs = InputConstraints(**kw)
    inv = {}
    for i, (s, a) in enumerate(zip(specs, S0)):
        for k, f in s.invariants.items():
            inv[f"{i}.{k}"] = (lambda f, a: (lambda h: f(h[:, a])))(f, a)
    return WorldSpec(
        n0=sum(s.n0 for s in specs), n1=sum(s.n1 for s in specs), law=law, coarse=coarse, init=init,
        noise_dim=sum(s.noise_dim for s in specs), n_m=sum(s.n_m for s in specs),
        memory_init=m_init if has_mem else None, memory_update=m_upd if has_mem else None,
        n_u=sum(s.n_u for s in specs), actuable=act, kick=kick if custom else None,
        inputs=inputs, observation=observation or specs[0].observation,
        burn_in=max(s.burn_in for s in specs), replay=specs[0].replay, max_ticks=specs[0].max_ticks,
        invariants=inv, name=name or " + ".join(s.name for s in specs))


def concat(a: WorldSpec, b: WorldSpec, **kw) -> WorldSpec:
    return product(a, b, **kw)


def diffusive_coupling(sizes: Sequence[int], edges: Sequence[tuple], coords: Sequence[int], kappa: float) -> Callable:
    """Exchange term for a coupled product of len(sizes) blocks: along each edge (i, j) the
    listed local coordinates relax toward each other at rate kappa (conserves their sum)."""
    S = _slices(sizes)
    coords = np.asarray(coords, int)

    def J(h):
        out = np.zeros_like(h)
        for i, j in edges:
            ci, cj = S[i].start + coords, S[j].start + coords
            f = kappa * (h[:, cj] - h[:, ci])
            out[:, ci] += f
            out[:, cj] -= f
        return out
    return J


def stack(spec: WorldSpec, coarse2: Callable, n2: int, memory2_init: Optional[Callable] = None,
          memory2_update: Optional[Callable] = None, n_m2: int = 0, observation: Optional[ObservationSpec] = None,
          name: Optional[str] = None) -> WorldSpec:
    """Level 2 = Phi2(h1, m2) observed instead of level 1; the agent still acts on level 0.
    Memory is (m1, m2); m2 updates from the new h1."""
    n1m = spec.n_m

    def coarse(h, m):
        return coarse2(spec.coarse(h, m[:, :n1m]), m[:, n1m:])

    has = spec.memory_init is not None or memory2_init is not None

    def m_init(h):
        m1 = spec.memory_init(h) if spec.memory_init else np.zeros((h.shape[0], 0))
        m2 = memory2_init(spec.coarse(h, m1)) if memory2_init else np.zeros((h.shape[0], 0))
        return np.concatenate([m1, m2], 1)

    def m_upd(m, h):
        m1 = spec.memory_update(m[:, :n1m], h) if spec.memory_update else m[:, :n1m]
        m2 = memory2_update(m[:, n1m:], spec.coarse(h, m1)) if memory2_update else m[:, n1m:]
        return np.concatenate([m1, m2], 1)

    d = dict(spec.__dict__)
    d.update(n1=n2, coarse=coarse, n_m=n1m + n_m2, memory_init=m_init if has else None,
             memory_update=m_upd if has else None, observation=observation or spec.observation,
             name=name or f"stack({spec.name})")
    return WorldSpec(**d)


def stride(spec: WorldSpec, s: int, name: Optional[str] = None) -> WorldSpec:
    """Temporal coarse-graining: one tick = s level-0 ticks; the input is kicked in before the
    first sub-tick; memory updates once per strided tick."""
    nd = spec.noise_dim

    def law(h, xi):
        for i in range(s):
            h = spec.law(h, xi[:, i * nd:(i + 1) * nd])
        return h

    d = dict(spec.__dict__)
    d.update(law=law, noise_dim=nd * s, burn_in=-(-spec.burn_in // s), name=name or f"stride{s}({spec.name})")
    return WorldSpec(**d)


def refine(spec: WorldSpec, law: Callable, n_fine: int, psi: Callable, init: Callable, noise_dim: int,
           lift: Optional[Callable] = None, actuable: Optional[Sequence[int]] = None,
           burn_in: Optional[int] = None, name: Optional[str] = None) -> WorldSpec:
    """Extend downward: a level -1 state x in R^n_fine with law `law`, whose coarse-graining
    psi(x) (B,n0) is meant to reproduce the known level 0. The new world's level 0 is x and
    its coarse-graining is Phi(psi(x), m). Actuation: lift(u) (B,n_u)->(B,n_fine) keeps the old
    actuators (lifted actuation, psi(x + lift(u)) = psi(x) + u for linear psi); lift=None
    actuates fine coordinates directly (`actuable`, default all)."""
    if lift is not None and spec.kick is not None:
        raise ValueError("refine: lifted actuation composes with additive kicks only")

    def coarse(x, m):
        return spec.coarse(psi(x), m)

    m_init = (lambda x: spec.memory_init(psi(x))) if spec.memory_init else None
    m_upd = (lambda m, x: spec.memory_update(m, psi(x))) if spec.memory_update else None
    inv = {k: (lambda f: (lambda x: f(psi(x))))(f) for k, f in spec.invariants.items()}
    if lift is not None:
        n_u, act, kick = spec.n_u, spec.actuable, (lambda x, u: x + lift(u))
    else:
        n_u, act, kick = n_fine, actuable, None
    return WorldSpec(
        n0=n_fine, n1=spec.n1, law=law, coarse=coarse, init=init, noise_dim=noise_dim, n_m=spec.n_m,
        memory_init=m_init, memory_update=m_upd, n_u=n_u, actuable=act, kick=kick,
        inputs=spec.inputs, observation=spec.observation,
        burn_in=spec.burn_in if burn_in is None else burn_in, replay=spec.replay,
        max_ticks=spec.max_ticks, invariants=inv, name=name or f"refine({spec.name})")


def commutation_error(fine: VectorWorld, psi: Callable, coarse: VectorWorld, T: int = 1,
                      n: int = 2000, n_rep: int = 32, seed: int = 0) -> dict:
    """Distributional commutation error of a refinement: delta2 = E|| E[psi(x(T)) | x] -
    E[h0(T) | h0 = psi(x)] ||^2 over x from the fine world's initial distribution, free
    evolution, Monte Carlo over fresh-noise branches (bias from MC variance removed)."""
    df, dc = fine.designer, coarse.designer
    x = df.ensemble(n, seed=(71, seed))
    xb = x.clone(rep=n_rep, fresh=True)
    df.rollout(xb, None, xb.t + T)
    yf = psi(xb.h0).reshape(n, n_rep, -1)
    cb = dc.from_states(np.repeat(psi(x.h0), n_rep, axis=0))
    dc.rollout(cb, None, cb.t + T)
    yc = cb.h0.reshape(n, n_rep, -1)
    raw = ((yf.mean(1) - yc.mean(1)) ** 2).sum(1).mean()
    bias = (yf.var(1, ddof=1).sum(1).mean() + yc.var(1, ddof=1).sum(1).mean()) / n_rep
    return {"T": T, "delta2": float(raw - bias), "raw": float(raw), "mc_bias": float(bias)}


# --------------------------------------------------------------------------- json
def jsonable(obj):
    """Recursively convert numpy containers to plain JSON types (inf/nan -> strings)."""
    if isinstance(obj, dict):
        return {str(k): jsonable(v) for k, v in obj.items()}
    if isinstance(obj, (list, tuple)):
        return [jsonable(v) for v in obj]
    if isinstance(obj, np.ndarray):
        return jsonable(obj.tolist())
    if isinstance(obj, (np.floating, float)):
        f = float(obj)
        return f if math.isfinite(f) else str(f)
    if isinstance(obj, (np.integer,)):
        return int(obj)
    if isinstance(obj, (np.bool_,)):
        return bool(obj)
    return obj
