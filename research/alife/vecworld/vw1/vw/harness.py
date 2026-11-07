"""vw.harness -- the PhySim-v2 exam harness v0 (EXAM.md sections 1-6, minimal).

Lab          the agent-facing real world: a World behind a Secret (keys cannot be recomputed from
             public integers; reset labels are names, not keys), with a NatsAccountant on the
             input channel and tick / reset budgets. Every rejection happens before anything runs.
Item         one history item: revealed level-k history o(0..P), the prefix program that produced
             it, a held-out open-loop test program and query times {level: [times after P]}.
ProgramMix   the public program distribution: named classes (e.g. 'a' none, 'b' blind random,
             'c' aimed from the history, 'd' large regional) in equal or given shares.
HistoryExam  builds n items from a secret exam namespace (starts from mu after burn-in), R replicate
             truths per item (fresh secret noise, same test program), a climatology pool (no-input
             stationary runs), and scores predictors with the fair energy score per (level, time)
             cell. References: oracle (leave-one-out over the R truths) and climatology. Skill:
             vw.scoring.skill_report.

Predictor protocol (as v1, with a history): predict(item: dict, n_samples: int, seed: int) ->
{level: array (n_samples, len(times), d_level)}; samples with the same index form one trajectory.

Levels above the observed one are declared public statistics of the observation:
derived={level: f(obs (..., n_obs)) -> (..., d)}.
"""
from __future__ import annotations

import math
from dataclasses import dataclass
from typing import Callable, Mapping, Optional, Sequence

import jax.numpy as jnp
import numpy as np

from .nats import NatsAccountant, NatsBudget
from .ports import BudgetExhausted, InputViolation
from .scoring import (energy_fair, energy_loo, energy_v1, skill_report, variogram, variogram_loo)
from .secret import Secret
from .world import Ensemble, World


# ----------------------------------------------------------------------------- the real world
class Lab:
    """A World behind a secret, with information and tick budgets (the agent's only real world).

    world       a vw.World (its permutations, if any, are kept; EXAM recommends identity maps)
    secret      Secret; episode keys = HMAC(secret, 'episode', label[, count])
    nats        NatsBudget on agent commands (None: no information budget)
    max_ticks   T_max over the investigation (None: unlimited); resets cost reset_cost ticks each
    """

    def __init__(self, world: World, secret: Secret, nats: Optional[NatsBudget] = None,
                 max_ticks: Optional[int] = None, reset_cost: int = 1, lab_mode: bool = False):
        if world.spec.replay == "full" and not lab_mode:
            raise ValueError("Lab: replay='full' (common random numbers) is a separate lab mode")
        if nats is not None and world.inport.noise > 0:
            raise ValueError("Lab: nats accounting needs inputs that enter as a shift; the port's "
                             "multiplicative actuation noise is not a Gaussian channel")
        if nats is not None and nats.n_in != world.n_in:
            raise ValueError("Lab: NatsBudget dimension differs from the world's n_in")
        self.world = world
        self._sec = secret.child("lab-episodes")
        self.nats = nats
        self.acct = NatsAccountant(nats) if nats is not None else None
        self.max_ticks = max_ticks
        self.reset_cost = int(reset_cost)
        self.ticks_used = 0
        self.n_resets = 0
        self._ep: Optional[Ensemble] = None
        self._count = 0
        self._last_in = None
        self._spent_l1 = 0.0

    # ---- public ----
    def card(self) -> dict:
        c = self.world.card()
        c.update({"max_ticks": self.max_ticks, "ticks_used": self.ticks_used, "reset_cost": self.reset_cost,
                  "keys": "secret (>= 128 bits); reset labels name episodes, they are not keys",
                  "information_budget": None if self.nats is None else self.nats.public()})
        return c

    def usage(self) -> dict:
        u = {"ticks_used": self.ticks_used, "max_ticks": self.max_ticks, "resets": self.n_resets}
        if self.acct is not None:
            u.update(self.acct.usage())
        return u

    def reset(self, label=0) -> np.ndarray:
        """Start an episode at the start named `label` (replay='initial': the same label gives the
        same start, with fresh dynamics noise each time). Costs reset_cost ticks."""
        self._check_ticks(self.reset_cost)
        self.ticks_used += self.reset_cost
        self._start(label)
        return self._ep.observe()[0]

    def step(self, inp=None) -> np.ndarray:
        ep = self._require()
        w, C = self.world, self.world.inport.admissible
        a = C.normalize(inp, w.n_in)
        C.check(a, ep.t, self._last_in, self._spent_l1)
        can = C.canonical(a) if a else {}
        if self.acct is not None and can:
            self.acct.check(can)
        self._check_ticks(1)
        self._ep = ep.step(w._dense(can) if can else None)
        self.ticks_used += 1
        if a:
            self._last_in = ep.t
            self._spent_l1 += C.charge(a)
            if self.acct is not None:
                self.acct.charge(can)
        return self._ep.observe()[0]

    def run(self, program, query_times, label=None) -> np.ndarray:
        """Run an open-loop program; return o at the query times (len(q), n_obs). With label, start
        a new episode first. The whole program is validated (bounds, L1 rules, nats caps, ticks)
        before anything runs; on any violation nothing runs and nothing is charged."""
        w, C = self.world, self.world.inport.admissible
        q = [int(x) for x in query_times]
        if not q or min(q) < 0:
            raise InputViolation("format: query_times must be a non-empty list of integers >= 0")
        H = max(q)
        if label is not None:
            t0, last, spent, ep_nats = 0, None, 0.0, 0.0
            need = H + self.reset_cost
        else:
            ep = self._require()
            t0, last, spent = ep.t, self._last_in, self._spent_l1
            ep_nats = self.acct.episode_used if self.acct is not None else 0.0
            need = H
        prog = w._validate_program(program, t0, last, spent, H)
        canon = [(t, C.canonical(a)) for t, a in prog]
        if self.acct is not None:
            self.acct.check_program(canon, episode_used=ep_nats)
        self._check_ticks(need)
        if label is not None:
            self.ticks_used += self.reset_cost
            self._start(label)
        ep = self._ep
        A = np.zeros((H, 1, w.n_in))
        for (t, a), (_, ca) in zip(prog, canon):
            for j, v in ca.items():
                A[t, 0, j] = v
            self._last_in = ep.t + t
            self._spent_l1 += C.charge(a)
            if self.acct is not None:
                self.acct.charge(ca)
        c, rec = w._rollout(w.params, ep.carry, jnp.asarray(A), rec=("obs",))
        self._ep = Ensemble(w, c, ep.t + H)
        self.ticks_used += H
        return np.asarray(rec["obs"][:, 0])[q]

    # ---- internals ----
    def _start(self, label):
        lab = label if isinstance(label, str) else int(label)
        self._count += 1
        self.n_resets += 1
        mode = self.world.spec.replay
        if mode == "initial":
            ki = self._sec.key("init", lab)
            kd = self._sec.key("dyn", lab, self._count)
        elif mode == "none":
            ki = self._sec.key("init-fresh", lab, self._count)
            kd = self._sec.key("dyn", lab, self._count)
        else:                                   # lab mode: common random numbers
            ki = self._sec.key("init", lab)
            kd = self._sec.key("dyn-full", lab)
        self._ep = self.world._new_ensemble(ki[None], kd[None])
        self._last_in, self._spent_l1 = None, 0.0
        if self.acct is not None:
            self.acct.new_episode()

    def _require(self) -> Ensemble:
        if self._ep is None:
            raise RuntimeError("call reset(label) first")
        return self._ep

    def _check_ticks(self, n: int):
        if self.max_ticks is not None and self.ticks_used + n > self.max_ticks:
            raise BudgetExhausted(f"budget: {self.ticks_used} + {n} ticks > max_ticks={self.max_ticks}; nothing ran")


# ----------------------------------------------------------------------------- items and programs
@dataclass
class Item:
    id: int
    history: np.ndarray                 # (P + 1, n_obs): o(0..P)
    prefix_program: list                # [(t, {j: v})], 0 <= t < P
    program: list                       # [(t, {j: v})], t >= 0 relative to P
    queries: dict                       # {level: [times >= 1 after P]}
    klass: str = ""                     # program class (evaluator metadata)

    def public(self) -> dict:
        return {"id": self.id, "history": self.history.copy(), "prefix_program": list(self.prefix_program),
                "program": list(self.program), "queries": {k: list(v) for k, v in self.queries.items()}}


def program_dense(program, H: int, n_in: int) -> np.ndarray:
    """[(t, {j: v})] -> (H, n_in)."""
    P = np.zeros((H, n_in))
    for t, a in program or []:
        if 0 <= int(t) < H:
            for j, v in a.items():
                P[int(t), int(j)] = v
    return P


class ProgramMix:
    """Public program distribution: classes name -> f(rng, history (P+1, n_obs), H, nats_left) ->
    program [(t, {j: v})]; drawn in the given shares (default equal)."""

    def __init__(self, classes: Mapping[str, Callable], shares: Optional[Mapping[str, float]] = None):
        self.classes = dict(classes)
        s = np.array([1.0 if shares is None else float(shares[k]) for k in self.classes])
        self.names, self.p = list(self.classes), s / s.sum()

    def assign(self, n: int) -> list:
        """Balanced class labels for n items (deterministic quotas, then shuffled by the caller)."""
        q = np.floor(self.p * n).astype(int)
        q[: n - q.sum()] += 1
        return [k for k, c in zip(self.names, q) for _ in range(c)]


def no_input(rng, history, H, nats_left):
    return []


def blind_random(budget: NatsBudget, k: int = 2, rate: float = 0.25):
    """Random k-site pushes at random ticks, each costing U(0, tick cap], until the episode budget."""
    n_in = budget.n_in

    def f(rng, history, H, nats_left):
        prog, left = [], nats_left
        cap = budget.tick if budget.tick is not None else left
        for t in range(H):
            if rng.random() >= rate or left <= 1e-9:
                continue
            idx = rng.choice(n_in, size=k, replace=False)
            v = np.zeros(n_in)
            v[idx] = rng.standard_normal(k)
            c_target = min(rng.uniform(0, cap), left)
            c = budget.cost(v)
            if not (c > 0 and math.isfinite(c)):
                continue
            v *= math.sqrt(c_target / c) * (1 - 1e-9)
            prog.append((t, {int(j): float(v[j]) for j in idx}))
            left -= budget.cost(v)
        return prog
    return f


# ----------------------------------------------------------------------------- the exam
class HistoryExam:
    """History items with replicate truths, references and fair scoring (designer side).

    world      the hidden world (World with the true params)
    secret     Secret; the exam uses its own child namespace, unreachable from Lab labels
    programs   ProgramMix for the test programs; prefix: callable(rng, P) -> program (default none)
    queries    {level: [times after P]}; level k_obs is the observation, others via `derived`
    scales     {level: (d,) public scales} dividing coordinates before scoring
    nats       NatsBudget: prefix + test program of an item obey its tick and episode caps
    """

    def __init__(self, world: World, secret: Secret, programs: ProgramMix, n_items: int = 64, prefix: int = 16,
                 queries: Optional[Mapping[int, Sequence[int]]] = None, R: int = 16,
                 derived: Optional[Mapping[int, Callable]] = None, scales: Optional[Mapping[int, np.ndarray]] = None,
                 nats: Optional[NatsBudget] = None, prefix_program: Optional[Callable] = None,
                 n_clim: int = 256, vs_weights: Optional[Mapping[int, np.ndarray]] = None, name: str = "exam"):
        self.w, self.k = world, world.k_obs
        self.P, self.R, self.n = int(prefix), int(R), int(n_items)
        self.queries = {int(l): sorted(set(int(t) for t in ts)) for l, ts in
                        (queries or {world.k_obs: [1, 2, 4, 8, 16]}).items()}
        if min(min(v) for v in self.queries.values()) < 1:
            raise ValueError("HistoryExam: query times must be >= 1 (after the revealed history)")
        self.derived = dict(derived or {})
        for l in self.queries:
            if l != self.k and l not in self.derived:
                raise ValueError(f"HistoryExam: level {l} needs a derived statistic of the observation")
        self.H = max(max(v) for v in self.queries.values())
        self.cells = [(l, t) for l in sorted(self.queries) for t in self.queries[l]]
        self.nats = nats
        self.vs_weights = dict(vs_weights or {})
        sec = secret.child("exam", name)
        n, R, P, H, n_in = self.n, self.R, self.P, self.H, world.n_in
        d = world.designer

        # starts from mu (after the declared burn-in), prefix, history
        ens = world._new_ensemble(sec.keys(n, "start"), sec.keys(n, "prefix-dyn"))
        pre = [(prefix_program(sec.rng("prefix", i), P) if prefix_program else []) for i in range(n)]
        Ppre = np.stack([program_dense(p, P, n_in) for p in pre])
        if nats is not None:
            for i, p in enumerate(pre):
                NatsAccountant(nats).check_program(p, where=f"item {i} prefix ")
        ens, rec = d.rollout(ens, Ppre if P > 0 else None, T=P, rec=("obs",))
        hist = rec["obs"]                                                  # (n, P+1, n_obs)
        self._snap = ens

        # test programs (classes in balanced shares, order shuffled by the secret)
        labels = programs.assign(n)
        sec.rng("order").shuffle(labels)
        self.items, progs = [], []
        for i in range(n):
            rng = sec.rng("program", i)
            used = NatsAccountant(nats).check_program(pre[i]) if nats is not None else 0.0
            left = (nats.episode - used) if (nats is not None and nats.episode is not None) else math.inf
            prog = programs.classes[labels[i]](rng, hist[i], H, left)
            prog = [(int(t), {int(j): float(v) for j, v in a.items()}) for t, a in prog]
            world._validate_program(prog, P, None, 0.0, H)                 # bounds, sparsity, L1
            if nats is not None:
                NatsAccountant(nats).check_program(prog, where=f"item {i} test ", episode_used=used)
            progs.append(prog)
            self.items.append(Item(id=sec.label("item", i), history=hist[i], prefix_program=pre[i], program=prog,
                                   queries={l: list(v) for l, v in self.queries.items()}, klass=labels[i]))
        self._Ptest = np.stack([program_dense(p, H, n_in) for p in progs])  # (n, H, n_in)

        # replicate truths: R branches per item with fresh secret noise, same test program
        rep = self._snap.clone(rep=R, keys=sec.keys(n * R, "truth"))
        Pfull = np.concatenate([np.zeros((n, P, n_in)), self._Ptest], 1)  # indexed by absolute time
        _, rec = d.rollout(rep, np.repeat(Pfull, R, axis=0), T=H, rec=("obs",))
        obs = rec["obs"].reshape(n, R, H + 1, -1)
        self.truths = {l: self._level(l, obs[:, :, self.queries[l]]) for l in self.queries}   # (n, R, nt, d)

        # climatology pool: no-input runs from mu (after burn-in)
        cl = world._new_ensemble(sec.keys(n_clim, "clim-start"), sec.keys(n_clim, "clim-dyn"))
        _, rec = d.rollout(cl, None, T=H, rec=("obs",))
        self.clim = {l: self._level(l, rec["obs"][:, self.queries[l]]) for l in self.queries}  # (n_clim, nt, d)
        self.scales = {l: (np.ones(self.truths[l].shape[-1]) if scales is None or l not in scales
                           else np.asarray(scales[l], float)) for l in self.queries}

    def _level(self, l, obs):
        return obs if l == self.k else np.asarray(self.derived[l](obs))

    # ---- public side ----
    def public(self) -> list:
        return [it.public() for it in self.items]

    @property
    def classes(self) -> np.ndarray:
        return np.array([it.klass for it in self.items])

    def collect(self, predict: Callable, n_samples: int = 64, seed: int = 0) -> list:
        """Call predict once per item (no state may carry between items); validate the format."""
        out = []
        for it in self.items:
            s = predict(it.public(), n_samples, seed)
            chk = {}
            for l, ts in self.queries.items():
                a = np.asarray(s[l], float)
                want = (n_samples, len(ts), self.truths[l].shape[-1])
                if a.shape != want:
                    raise ValueError(f"predictor: level {l} samples have shape {a.shape}, expected {want}")
                if not np.all(np.isfinite(a)):
                    raise ValueError("predictor: non-finite samples")
                chk[l] = a
            out.append(chk)
        return out

    # ---- scoring ----
    def _per_cell(self, fn_pair, fn_loo=None, samples=None, pool=None) -> np.ndarray:
        cols = []
        for l, t in self.cells:
            j = self.queries[l].index(t)
            Y = self.truths[l][:, :, j]                                       # (n, R, d)
            sc = self.scales[l]
            if samples is not None:
                X = np.stack([s[l][:, j] for s in samples])                  # (n, m, d)
                cols.append(fn_pair(X, Y, sc, l))
            elif pool is not None:
                X = np.broadcast_to(pool[l][:, j][None], (self.n,) + pool[l][:, j].shape)
                cols.append(fn_pair(X, Y, sc, l))
            else:
                cols.append(fn_loo(Y, sc, l))
        return np.stack(cols, 1)                                              # (n, n_cells)

    def score(self, samples: list) -> dict:
        """Per item and cell: fair ES, v1 ES, fair VS (cells with d >= 2; else nan)."""
        return {"es": self._per_cell(lambda X, Y, s, l: energy_fair(X, Y, s), samples=samples),
                "es_v1": self._per_cell(lambda X, Y, s, l: energy_v1(X, Y, s), samples=samples),
                "vs": self._per_cell(self._vs_pair, samples=samples)}

    def _vs_pair(self, X, Y, s, l):
        if X.shape[-1] < 2:
            return np.full(X.shape[0], np.nan)
        return variogram(X, Y, 0.5, self.vs_weights.get(l), s, fair=True)

    def references(self, n_clim_samples: Optional[int] = None) -> dict:
        """oracle (leave-one-out over the R truths, fair and v1) and climatology (the pool)."""
        pool = self.clim
        if n_clim_samples is not None:
            pool = {l: v[:n_clim_samples] for l, v in pool.items()}
        return {
            "oracle": {"es": self._per_cell(None, lambda Y, s, l: energy_loo(Y, s, True)),
                       "es_v1": self._per_cell(None, lambda Y, s, l: energy_loo(Y, s, False)),
                       "vs": self._per_cell(None, lambda Y, s, l: (variogram_loo(Y, 0.5, self.vs_weights.get(l), s)
                                                                    if Y.shape[-1] > 1 else np.full(Y.shape[0], np.nan)))},
            "climatology": {"es": self._per_cell(lambda X, Y, s, l: energy_fair(X, Y, s), pool=pool),
                            "es_v1": self._per_cell(lambda X, Y, s, l: energy_v1(X, Y, s), pool=pool),
                            "vs": self._per_cell(self._vs_pair, pool=pool)}}

    def report(self, scored: Mapping[str, dict], key: str = "es", refs: Optional[dict] = None, **kw) -> dict:
        """skill_report over the references and every scored predictor (by program class too)."""
        refs = refs or self.references()
        S = {"climatology": refs["climatology"][key], "oracle": refs["oracle"][key]}
        S.update({k: v[key] for k, v in scored.items()})
        cols = ~np.isnan(S["oracle"]).any(0)
        S = {k: v[:, cols] for k, v in S.items()}
        cells = [c for c, ok in zip(self.cells, cols) if ok]
        return skill_report(S, cells=cells, groups=self.classes, **kw)
