"""evaluator.instance -- hidden exam instances: the secret, the hidden parameters, the frozen exam.

make_instance   draws a fresh 256-bit secret (os.urandom) and a hidden theta from the public prior under the
                public viability rule, at run time, and writes hidden/instance.json (mode 0600). Nothing here
                is ever committed: results keep only the secret's commitment hash.
build_exam      vw.harness.HistoryExam on the hidden world (secret exam namespace, unreachable from Lab labels):
                history items, R replicate truths per item, a climatology pool; frozen to hidden/exam.npz so
                that every submission is graded on the same items. Also writes two public example requests
                (simulated at the prior mean with public noise) for format validation.
FrozenExam      the frozen arrays with the fair energy score per (item, cell), the oracle (leave one out) and
                the climatology K.
"""
from __future__ import annotations

import importlib
import json
import os
import sys
import time

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)
from physim2 import _vendor_path as _vp  # noqa: E402

_vp.add("vw1")                                             # the vw library (development tree)

DEFAULT_CFG = {
    "exam": {"n_items": 64, "R": 16, "n_clim": 128, "P": None, "queries": None},
    "lab": {"max_ticks": 4000, "reset_cost": 1, "total_nats": None},
    "predictor": {"n_samples": 32, "cpu_seconds": 60, "wall_seconds": 120, "memory_gib": 4, "artifact_mib": 64},
    "envelope": {"cpus": 4, "wall_hours": 24, "memory_gib": 8, "gpu": False},
    "validation": {"max_attempts": 64},
}


def merge_cfg(cfg: dict | None) -> dict:
    out = json.loads(json.dumps(DEFAULT_CFG))
    for k, v in (cfg or {}).items():
        if isinstance(v, dict) and isinstance(out.get(k), dict):
            out[k].update(v)
        else:
            out[k] = v
    return out


def world_module(name: str):
    return importlib.import_module(f"physim2.world_{name}")


def exam_decl(W, cfg) -> dict:
    """The public exam declaration: prefix, queries per level, cells."""
    P = int(cfg["exam"]["P"] or W.P_PREFIX)
    q = cfg["exam"]["queries"] or W.QUERIES
    q = {int(l): sorted(int(t) for t in ts) for l, ts in q.items()}
    return {"P": P, "queries": q, "H": max(max(v) for v in q.values()),
            "cells": [(l, t) for l in sorted(q) for t in q[l]]}


def make_instance(world: str, cfg: dict | None, hidden_dir: str, max_tries: int = 64) -> dict:
    from vw.secret import Secret
    W = world_module(world)
    cfg = merge_cfg(cfg)
    os.makedirs(hidden_dir, mode=0o700, exist_ok=True)
    os.chmod(hidden_dir, 0o700)
    sec = Secret()                                        # os.urandom(32): never derived from public integers
    rng = sec.rng("theta-draws")
    theta, tries = None, 0
    while theta is None:
        cand = W.prior_sample(rng, 1)
        tries += 1
        if bool(W.viable(cand, seed=int(rng.integers(2 ** 31)))[0]):
            theta = cand[0]
        elif tries >= max_tries:
            raise RuntimeError("make_instance: no viable draw")
    inst = {"world": world, "theta_names": list(W.THETA_NAMES), "theta": [float(v) for v in theta],
            "secret_hex": sec.hex(), "secret_commitment": sec.commitment(), "config": cfg,
            "prior_draws_tried": tries, "created_unix": time.time(),
            "note": "HIDDEN: never commit, never mount into an agent or predictor sandbox"}
    f = os.path.join(hidden_dir, "instance.json")
    fd = os.open(f, os.O_WRONLY | os.O_CREAT | os.O_TRUNC, 0o600)
    with os.fdopen(fd, "w") as fh:
        json.dump(inst, fh, indent=1)
    return {"world": world, "secret_commitment": inst["secret_commitment"], "prior_draws_tried": tries}


def load_instance(hidden_dir: str):
    from vw.secret import Secret
    inst = json.load(open(os.path.join(hidden_dir, "instance.json")))
    return inst, world_module(inst["world"]), Secret.from_hex(inst["secret_hex"])


def build_exam(hidden_dir: str, log=print) -> dict:
    from vw.harness import HistoryExam
    inst, W, sec = load_instance(hidden_dir)
    cfg = inst["config"]
    d = exam_decl(W, cfg)

    class Exam(HistoryExam):
        def _level(self, l, obs):
            return np.asarray(W.level(l, obs))

    t0 = time.time()
    world = W.build_world(np.array(inst["theta"]))
    ex = Exam(world, sec.child("exam"), W.program_mix(), n_items=int(cfg["exam"]["n_items"]), prefix=d["P"],
              queries=d["queries"], R=int(cfg["exam"]["R"]), derived={l: (lambda o, l=l: W.level(l, o)) for l in d["queries"]},
              scales=W.scales(), nats=W.nats_budget(), n_clim=int(cfg["exam"]["n_clim"]), name="exam")
    n, P, H = ex.n, ex.P, ex.H
    blob = {"history": np.stack([it.history for it in ex.items]), "prefix": np.zeros((n, P, W.N_IN)),
            "test": ex._Ptest, "classes": ex.classes, "ids": np.array([it.id for it in ex.items], np.int64),
            "meta": json.dumps({"P": P, "H": H, "queries": {str(l): v for l, v in ex.queries.items()},
                                "cells": [list(c) for c in ex.cells], "R": ex.R, "n_clim": int(cfg["exam"]["n_clim"]),
                                "world": inst["world"]})}
    for l in ex.queries:
        blob[f"truth{l}"] = ex.truths[l]
        blob[f"clim{l}"] = ex.clim[l]
        blob[f"scale{l}"] = ex.scales[l]
    np.savez_compressed(os.path.join(hidden_dir, "exam.npz"), **blob)
    # two public example requests for validate/submit (prior-mean theta, public noise): no hidden information
    sim = W.Simulator(chunk=2)
    e = sim.episodes(np.tile(W.PRIOR_MEAN, (2, 1)), seed=12345, P=P, H=H)
    np.savez_compressed(os.path.join(hidden_dir, "examples.npz"), history=e["obs"][:, :P + 1],
                        prefix=np.zeros((2, P, W.N_IN)), test=e["U"][:, P:])
    mt = n * (W.BURN_IN + P) + n * ex.R * H + int(cfg["exam"]["n_clim"]) * (W.BURN_IN + H)
    info = {"n_items": n, "R": ex.R, "member_ticks": int(mt), "seconds": time.time() - t0,
            "classes": {c: int((ex.classes == c).sum()) for c in sorted(set(ex.classes.tolist()))}}
    log(f"exam built: {info}")
    return info


class FrozenExam:
    def __init__(self, hidden_dir: str):
        z = np.load(os.path.join(hidden_dir, "exam.npz"), allow_pickle=False)
        m = json.loads(str(z["meta"]))
        self.P, self.H, self.R = m["P"], m["H"], m["R"]
        self.queries = {int(l): v for l, v in m["queries"].items()}
        self.cells = [tuple(c) for c in m["cells"]]
        self.history, self.prefix, self.test = z["history"], z["prefix"], z["test"]
        self.classes, self.ids = z["classes"], z["ids"]
        self.truths = {l: z[f"truth{l}"] for l in self.queries}
        self.clim = {l: z[f"clim{l}"] for l in self.queries}
        self.scales = {l: z[f"scale{l}"] for l in self.queries}
        self.n = self.history.shape[0]
        self.dims = {l: self.truths[l].shape[-1] for l in self.queries}

    def request(self, i: int, n_samples: int, seed: int) -> dict:
        return {"history": self.history[i], "prefix": self.prefix[i], "test": self.test[i],
                "queries": json.dumps({str(l): v for l, v in self.queries.items()}), "n_samples": n_samples, "seed": seed}

    def score(self, S: dict) -> np.ndarray:
        """Fair energy score per (item, cell) of samples S = {level: (n, m, n_times, d)}."""
        from vw.scoring import energy_fair
        cols = []
        for l, t in self.cells:
            j = self.queries[l].index(t)
            cols.append(energy_fair(np.asarray(S[l])[:, :, j], self.truths[l][:, :, j], self.scales[l]))
        return np.stack(cols, 1)

    def references(self) -> dict:
        """O: the oracle (leave-one-out over the R replicate truths); K: the climatology pool."""
        from vw.scoring import energy_fair, energy_loo
        O, K = [], []
        for l, t in self.cells:
            j = self.queries[l].index(t)
            Y = self.truths[l][:, :, j]
            O.append(energy_loo(Y, self.scales[l], True))
            pool = self.clim[l][:, j]
            K.append(energy_fair(np.broadcast_to(pool[None], (self.n,) + pool.shape), Y, self.scales[l]))
        return {"O": np.stack(O, 1), "K": np.stack(K, 1)}
