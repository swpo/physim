"""vw.exam -- held-out prediction exam for any World (ported from VW-0, batched).

Each item: an episode from a reserved key namespace (the agent cannot reset to it), a prefix
program run by the harness (the agent sees o(0..prefix) and the prefix inputs), then a test
program and query times relative to the end of the prefix. Scored against n_rep replicate futures
branched from the item's hidden state with fresh noise. All items run as one batched ensemble.
"""
from __future__ import annotations

import math
from typing import Callable, Mapping, Optional, Sequence

import jax
import numpy as np

from .world import _NS_EXAM, _ST_DYN, World, make_key, member_keys


def _rng(*ints):
    return np.random.default_rng([0x565731, 61, *[int(i) for i in ints]])


class Exam:
    def __init__(self, world: World, n_items: int = 64, prefix: int = 16, horizon: int = 32,
                 queries: Optional[Sequence[int]] = None, rate: float = 0.5, exam_seed: int = 0,
                 sampler: Optional[Callable] = None):
        self.w, d = world, world.designer
        self.prefix, self.horizon, self.exam_seed = prefix, horizon, exam_seed
        self.queries = sorted(set(queries)) if queries else [q for q in (1, 2, 4, 8, 16, 32, 64, 128) if q <= horizon]
        H = prefix + horizon
        progs = [(sampler or d.random_program)(_rng(exam_seed, i), H, rate) for i in range(n_items)]
        self._P = np.stack([d.program_dense(p, H) for p in progs])          # (n_items, H, n_in)
        ki = member_keys(make_key(_NS_EXAM, world.world_seed, exam_seed), n_items)
        kd = jax.vmap(lambda k: jax.random.fold_in(k, _ST_DYN))(ki)
        ens = world._new_ensemble(ki, kd)
        self._snap, rec = d.rollout(ens, self._P, T=prefix, rec=("obs",))
        self.items = [{"past_obs": rec["obs"][i],
                       "past_program": [(t, a) for t, a in progs[i] if t < prefix],
                       "program": [(t - prefix, a) for t, a in progs[i] if t >= prefix],
                       "query_times": list(self.queries)} for i in range(n_items)]

    def public(self) -> list:
        return [dict(it) for it in self.items]

    def score(self, predictions: Optional[list] = None, n_rep: int = 32,
              references: Optional[Mapping[str, Callable]] = None, ceiling: Optional[str] = None) -> dict:
        """predictions: per item an array (len(queries), n_obs), or None. references: name ->
        callable(item) -> same shape. MSE = expected squared error over replicate futures; 'oracle'
        is the replicate variance (the floor with the hidden state known).
        Skill = (MSE_persistence - MSE) / (MSE_persistence - MSE_ceiling)."""
        d, qs, n = self.w.designer, self.queries, len(self.items)
        preds = {"persistence": [np.tile(it["past_obs"][-1], (len(qs), 1)) for it in self.items]}
        if predictions is not None:
            preds["agent"] = [np.asarray(p, float) for p in predictions]
        for name, f in (references or {}).items():
            preds[name] = [np.asarray(f(it), float) for it in self.items]
        keys = member_keys(make_key(_NS_EXAM, self.w.world_seed, self.exam_seed, 1, n_rep), n * n_rep)
        ens = self._snap.clone(rep=n_rep, keys=keys)
        _, rec = d.rollout(ens, np.repeat(self._P, n_rep, axis=0), T=max(qs), rec=("obs",))
        Y = rec["obs"][:, qs].reshape(n, n_rep, len(qs), -1)                   # (n, R, nq, n_obs)
        orac = ((Y - Y.mean(1, keepdims=True)) ** 2).sum((1, 3)) / (n_rep - 1)  # (n, nq)
        mse = {k: ((Y - np.stack(v)[:, None]) ** 2).sum(3).mean(1) for k, v in preds.items()}
        out = {"queries": qs, "oracle": orac.mean(0), "mse": {k: v.mean(0) for k, v in mse.items()},
               "mse_se": {k: v.std(0, ddof=1) / math.sqrt(n) for k, v in mse.items()}}
        ref = out["mse"][ceiling] if ceiling else out["oracle"]
        base = out["mse"]["persistence"]
        with np.errstate(divide="ignore", invalid="ignore"):
            out["skill"] = {k: (base - v) / (base - ref) for k, v in out["mse"].items()}
        out["ceiling"] = ceiling or "oracle"
        return out
