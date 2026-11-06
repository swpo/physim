"""vw.ports -- the two ports through which an agent meets a world.

InputPort    on level 0: an admissible set (information constraints, all public and permutation
             invariant), the actuable subset of the level-0 input vector, multiplicative actuation
             noise, and a hidden permutation embedding agent coordinate j -> actuator in_map[j].
ObservePort  on the observed level L_k: a hidden permutation of its flattened state, optional
             hidden sign flips, additive Gaussian noise, clipping and quantisation.

Lens view.   Together the ports form a lens between the world and the agent: `put` sends an agent
             command a to an actuator vector u = embed(realise(a)); `get` sends a level-k state to an
             observation. Changing the apparatus (other constraints, more noise, a different
             embedding) composes another lens on the agent side; here that is `with_ports` on a
             WorldSpec, which re-binds both maps. Constraints are declared in agent coordinates and
             mean the same in actuator coordinates because the embedding is a permutation (the only
             linear maps that preserve every constraint family below; see spec/DESIGN.md section 2).

Rules kept from VW-0: admissibility depends only on the command, the card and the agent's own
past commands (never on hidden state); a violation raises InputViolation and nothing runs or is
charged; programs are validated as a whole before any of them runs.

Change from VW-0 (the zero-sum tolerance review finding): an accepted command is CANONICALISED
before it reaches the world. Under zero_sum the accepted command is projected to an exact zero
sum (or, with a value step, snapped to integer multiples whose integer sum must be exactly zero),
and actuation noise is re-projected. Every accepted command therefore has |sum| at round-off
level, so a level whose kick conserves mass for zero-sum u (additive kicks) or for every u
(pooling kicks) cannot gain mass from tolerance slack.
"""
from __future__ import annotations

import dataclasses
import math
from dataclasses import dataclass
from typing import Mapping, Optional

import jax
import jax.numpy as jnp
import numpy as np


class InputViolation(ValueError):
    """An input or program broke a declared constraint. Nothing ran and nothing was charged."""


class BudgetExhausted(RuntimeError):
    """The declared exploration budget (ticks) would be exceeded. Nothing ran."""


# ----------------------------------------------------------------------------- admissible set
@dataclass(frozen=True)
class Admissible:
    """Declared, public input constraints in agent coordinates (all permutation invariant).

    k              max number of non-zero coordinates per tick (None: no limit)
    lo, hi         bounds on every non-zero value
    total          bound on sum_j |a_j| per tick (None: none)
    zero_sum       sum_j a_j = 0: inputs move mass, never create it
    min_interval   minimum ticks between consecutive non-empty inputs (1: every tick)
    quantum        value step: values must be integer multiples of quantum (None: continuous)
    episode_budget bound on the episode's summed |a| (None: none)
    tol            tolerance of the checks (relative to max(1, sum|a|) for zero_sum)
    """
    k: Optional[int] = None
    lo: float = -1.0
    hi: float = 1.0
    total: Optional[float] = None
    zero_sum: bool = False
    min_interval: int = 1
    quantum: Optional[float] = None
    episode_budget: Optional[float] = None
    tol: float = 1e-9

    def __post_init__(self):
        if self.lo > self.hi:
            raise ValueError("Admissible: lo > hi")
        if self.k is not None and self.k < 1:
            raise ValueError("Admissible: k must be >= 1")
        if self.min_interval < 1:
            raise ValueError("Admissible: min_interval must be >= 1")
        if self.zero_sum and not (self.lo < 0 < self.hi):
            raise ValueError("Admissible: zero_sum needs lo < 0 < hi")
        if self.zero_sum and self.k is not None and self.k < 2:
            raise ValueError("Admissible: zero_sum needs k >= 2")
        if self.quantum is not None and not self.quantum > 0:
            raise ValueError("Admissible: quantum must be > 0")

    # ---- host-side parsing, checking, canonicalisation (public information only) ----
    def normalize(self, inp, n_in: int) -> dict:
        """dict {coord: value} | dense vector of length n_in | None -> {coord: value != 0}."""
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

    def violations(self, a: dict, t: int = 0, last_t: Optional[int] = None, spent: float = 0.0) -> list:
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
        if self.quantum:
            r = v / self.quantum
            if np.abs(r - np.round(r)).max() > 1e-6:
                msgs.append(f"quantum: values must be integer multiples of {self.quantum:g}")
            elif self.zero_sum and int(np.round(r).astype(np.int64).sum()) != 0:
                msgs.append(f"zero-sum: the value steps sum to {int(np.round(r).sum())} quanta, must be 0")
        elif self.zero_sum and abs(v.sum()) > self.tol * max(1.0, l1):
            msgs.append(f"zero-sum: sum(a) = {v.sum():.6g}, must be 0")
        if last_t is not None and t - last_t < self.min_interval:
            msgs.append(f"interval: last non-empty input at t={last_t}; the next is allowed "
                        f"at t={last_t + self.min_interval}, got t={t}")
        if self.episode_budget is not None and spent + l1 > self.episode_budget + self.tol:
            msgs.append(f"budget: episode sum|a| would be {spent + l1:.6g} > {self.episode_budget:g}")
        return msgs

    def check(self, a: dict, t: int = 0, last_t: Optional[int] = None, spent: float = 0.0, where: str = ""):
        msgs = self.violations(a, t, last_t, spent)
        if msgs:
            raise InputViolation(f"{where}input rejected, nothing charged: " + "; ".join(msgs))

    def canonical(self, a: dict) -> dict:
        """The command the world receives for an ACCEPTED command a: values snapped to the value
        step, and under zero_sum an exact zero sum (projection on the support)."""
        if not a:
            return {}
        keys = sorted(a)
        v = np.array([a[j] for j in keys], float)
        if self.quantum:
            v = self.quantum * np.round(v / self.quantum)
        elif self.zero_sum:
            v = v - v.sum() / v.size
            # one more pass removes the residual of the first subtraction (round-off level)
            v[np.argmax(np.abs(v))] -= v.sum()
        return {j: float(x) for j, x in zip(keys, v) if x != 0.0}

    def charge(self, a: dict) -> float:
        return float(sum(abs(x) for x in a.values()))

    # ---- sampling (designer program samplers) ----
    def sample(self, rng: np.random.Generator, n_in: int, max_tries: int = 50) -> dict:
        k = n_in if self.k is None else min(self.k, n_in)
        if self.zero_sum and k < 2:
            return {}
        lo, hi = max(self.lo, -1e6), min(self.hi, 1e6)
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
            if a and not self.violations(a):
                return self.canonical(a)
        return {}

    # ---- jittable saturation onto the per-tick admissible set (used by couplings) ----
    def saturate(self, a):
        """Map a vector into the per-tick admissible set (top-k by magnitude, bounds, zero sum,
        total, value step). Not the Euclidean projection; a declared, deterministic saturation.
        min_interval and episode_budget are not per-tick and are not applied."""
        a = jnp.asarray(a, jnp.float64)
        n = a.shape[0]
        if n == 0:
            return a
        if self.k is not None and self.k < n:
            order = jnp.argsort(-jnp.abs(a))
            keep = jnp.zeros(n, bool).at[order[: self.k]].set(True)
            a = jnp.where(keep, a, 0.0)
        mask = a != 0
        a = jnp.where(mask, jnp.clip(a, self.lo, self.hi), 0.0)
        if self.zero_sum:
            cnt = jnp.maximum(mask.sum(), 1)
            a = jnp.where(mask, a - a.sum() / cnt, 0.0)
            amax, amin = jnp.max(a), jnp.min(a)
            f = jnp.minimum(1.0, jnp.minimum(jnp.where(amax > self.hi, self.hi / jnp.where(amax > 0, amax, 1.0), 1.0),
                                             jnp.where(amin < self.lo, self.lo / jnp.where(amin < 0, amin, -1.0), 1.0)))
            a = a * f
        if self.total is not None:
            l1 = jnp.abs(a).sum()
            a = a * jnp.minimum(1.0, self.total / jnp.where(l1 > 0, l1, 1.0))
        if self.quantum:
            a = self.quantum * jnp.round(a / self.quantum)
            if self.zero_sum:
                a = a.at[jnp.argmax(jnp.abs(a))].add(-a.sum())
        return a

    # ---- structural numbers (input-capacity certificate) ----
    def amplitude(self) -> float:
        b = max(abs(self.lo), abs(self.hi))
        return b if self.total is None else min(b, self.total)

    def atom_amplitude(self) -> float:
        """Amplitude of the elementary admissible move: +b on one coordinate, or +b/-b on a pair."""
        if self.zero_sum:
            b = min(self.hi, -self.lo)
            return b if self.total is None else min(b, self.total / 2)
        return self.amplitude()

    def l2_radius(self, n_in: int) -> float:
        """An upper bound on ||a||_2 over admissible commands."""
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
        return math.log2(sum(math.comb(n_in, j) * len(vals) ** j for j in range(k + 1)))


# ----------------------------------------------------------------------------- input port
@dataclass(frozen=True)
class InputPort:
    """Input port on level 0.

    admissible  the public constraints (agent coordinates)
    actuable    indices of the level-0 input vector the agent can reach (None: all)
    noise       multiplicative actuation noise std on the support (re-projected under zero_sum);
                constraints bind the command, not the realisation
    in_map      hidden embedding, agent coordinate j -> actuator in_map[j] (drawn by World.bind)
    """
    admissible: Admissible = Admissible()
    actuable: Optional[tuple] = None
    noise: float = 0.0
    in_map: Optional[tuple] = None
    n_u: Optional[int] = None

    def __post_init__(self):
        if self.noise < 0:
            raise ValueError("InputPort: noise must be >= 0")

    def actuators(self, n_u: int) -> np.ndarray:
        act = np.arange(n_u) if self.actuable is None else np.asarray(self.actuable, int)
        if n_u and (act.size == 0 or act.min() < 0 or act.max() >= n_u or np.unique(act).size != act.size):
            raise ValueError("InputPort.actuable must be distinct indices in [0, n_u)")
        return act

    def bind(self, n_u: int, rng: np.random.Generator) -> "InputPort":
        act = self.actuators(n_u)
        perm = rng.permutation(act.size)
        in_map = self.in_map if self.in_map is not None else tuple(int(i) for i in act[perm])
        return dataclasses.replace(self, in_map=tuple(in_map), n_u=int(n_u))

    def unbound(self) -> "InputPort":
        return dataclasses.replace(self, in_map=None, n_u=None)

    @property
    def n_in(self) -> int:
        return len(self.in_map)

    # ---- jittable maps ----
    def realise(self, a, key):
        """Actuation noise on the support; re-projected to zero sum under zero_sum."""
        if self.noise <= 0:
            return a
        mask = a != 0
        a2 = a * (1.0 + self.noise * jax.random.normal(key, a.shape))
        if self.admissible.zero_sum:
            cnt = jnp.maximum(mask.sum(), 1)
            a2 = jnp.where(mask, a2 - a2.sum() / cnt, 0.0)
        return a2

    def embed(self, a):
        """Agent coordinates (n_in,) -> actuator vector (n_u,)."""
        u = jnp.zeros((self.n_u,), jnp.float64)
        if self.n_in == 0:
            return u
        return u.at[np.asarray(self.in_map)].set(a)

    def public(self) -> dict:
        d = dataclasses.asdict(self.admissible)
        d["actuation_noise"] = self.noise
        return d


# ----------------------------------------------------------------------------- observe port
@dataclass(frozen=True)
class ObservePort:
    """Observation port on level k: o = Q(clip(S P y + noise * eta)).

    noise        additive Gaussian noise std per coordinate
    quantum      quantisation step (None: none)
    clip         (lo, hi) saturation (None: none)
    sign_flip    hidden sign flips (declared option)
    max_queries  max query times per program (None: no limit)
    out_map      hidden permutation: observation j <- level-k coordinate out_map[j] (drawn by bind)
    out_sign     hidden signs (all +1 unless sign_flip)
    """
    noise: float = 0.0
    quantum: Optional[float] = None
    clip: Optional[tuple] = None
    sign_flip: bool = False
    max_queries: Optional[int] = None
    out_map: Optional[tuple] = None
    out_sign: Optional[tuple] = None

    def bind(self, n_obs: int, rng: np.random.Generator) -> "ObservePort":
        perm = rng.permutation(n_obs)
        sign = rng.choice([-1.0, 1.0], n_obs) if self.sign_flip else np.ones(n_obs)
        om = self.out_map if self.out_map is not None else tuple(int(i) for i in perm)
        os_ = self.out_sign if self.out_sign is not None else tuple(float(s) for s in sign)
        if sorted(om) != list(range(n_obs)) or len(os_) != n_obs:
            raise ValueError("ObservePort: out_map must be a permutation of the observed level")
        return dataclasses.replace(self, out_map=tuple(om), out_sign=tuple(os_))

    def unbound(self) -> "ObservePort":
        return dataclasses.replace(self, out_map=None, out_sign=None)

    @property
    def n_obs(self) -> int:
        return len(self.out_map)

    @property
    def resolution_var(self) -> float:
        return self.noise ** 2 + ((self.quantum ** 2) / 12.0 if self.quantum else 0.0)

    # ---- jittable maps ----
    def clean(self, y):
        """Noise-free observation (agent basis) of a flat level-k vector."""
        if self.n_obs == 0:
            return y
        return y[np.asarray(self.out_map)] * jnp.asarray(self.out_sign)

    def read_continuous(self, y, key):
        """Noisy, unclipped, unquantised observation (the channel the Fisher certificate uses)."""
        o = self.clean(y)
        if self.noise > 0:
            o = o + self.noise * jax.random.normal(key, o.shape)
        return o

    def read(self, y, key):
        o = self.read_continuous(y, key)
        if self.clip is not None:
            o = jnp.clip(o, self.clip[0], self.clip[1])
        if self.quantum:
            o = self.quantum * jnp.round(o / self.quantum)
        return o

    def public(self) -> dict:
        return {"noise": self.noise, "quantum": self.quantum, "clip": self.clip,
                "sign_flip": self.sign_flip, "max_queries": self.max_queries}
