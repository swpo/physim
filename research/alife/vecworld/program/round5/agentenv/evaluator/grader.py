"""evaluator.grader -- score frozen submissions on the frozen history items, next to the references.

grade(hidden, submission_dir, public_dir, name)
    runs the submission once per item in a fresh sandboxed process (evaluator.submission.run_request) with the
    declared limits; a request that fails or times out is scored as K for that item; writes
    hidden/grades/<name>.npz with the fair energy score per (item, cell) and a status record.
table(hidden, names)
    the reference table: K (climatology) and O (oracle, leave one out) from the frozen exam, every graded
    policy, pooled L, skill on the K-to-C and K-to-O scales, OES per cell (vw.scoring.skill_report), and the
    acceptance shares sigma and rho when D, P0, S and C are present.

usage: python -m evaluator.grader --hidden DIR --public DIR --submission DIR --name agent
"""
from __future__ import annotations

import argparse
import json
import os
import sys
import time

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

from evaluator import acceptance as ACC  # noqa: E402
from evaluator import instance as INST  # noqa: E402
from evaluator import submission as SUB  # noqa: E402


def grade(hidden: str, sub_dir: str, public_dir: str, name: str, hide=(), log=print, seed: int = 0) -> dict:
    inst, W, _ = INST.load_instance(hidden)
    ex = INST.FrozenExam(hidden)
    lim = inst["config"]["predictor"]
    m = int(lim["n_samples"])
    refs = ex.references()
    work = os.path.join(os.path.dirname(os.path.abspath(hidden)), "work", "grade_tmp")
    os.makedirs(work, exist_ok=True)
    S = {l: np.zeros((ex.n, m, len(ts), ex.dims[l])) for l, ts in ex.queries.items()}
    failed, cpu, wall, errors = np.zeros(ex.n, bool), np.zeros(ex.n), np.zeros(ex.n), []
    t0 = time.time()
    for i in range(ex.n):
        r = SUB.run_request(sub_dir, public_dir, ex.request(i, m, seed), lim, hide=tuple(hide) + (hidden,), work=work)
        cpu[i], wall[i] = r["cpu_s"], r["wall_s"]
        bad = None if not r["ok"] else SUB.check_shapes(r["samples"], ex.queries, ex.dims, m)
        if not r["ok"] or bad:
            failed[i] = True
            errors.append({"item": i, "error": (bad or r["error"])[:300]})
            continue
        for l in ex.queries:
            S[l][i] = r["samples"][l]
    sc = ex.score(S)
    sc[failed] = refs["K"][failed]                        # a failed request is scored as K
    out = {"name": name, "n_items": ex.n, "n_failed": int(failed.sum()), "cpu_s_mean": float(cpu.mean()),
           "cpu_s_max": float(cpu.max()), "wall_s_mean": float(wall.mean()), "seconds": time.time() - t0,
           "errors": errors[:5], "layers": r.get("layers")}
    os.makedirs(os.path.join(hidden, "grades"), exist_ok=True)
    np.savez_compressed(os.path.join(hidden, "grades", f"{name}.npz"), es=sc, failed=failed, cpu=cpu)
    json.dump(out, open(os.path.join(hidden, "grades", f"{name}.json"), "w"), indent=1)
    log(f"graded {name}: failed {out['n_failed']}/{ex.n}, cpu/item {out['cpu_s_mean']:.2f}s")
    return out


def load_scores(hidden: str, names) -> dict:
    ex = INST.FrozenExam(hidden)
    S = dict(ex.references())
    for nm in names:
        f = os.path.join(hidden, "grades", f"{nm}.npz")
        if os.path.exists(f):
            S[nm] = np.load(f)["es"]
    return S, ex


def table(hiddens, names, labels=None, n_boot: int = 2000) -> dict:
    """Pool the per-item scores of one or more hidden worlds (same world type and exam declaration)."""
    from vw.scoring import public_report, skill_report
    hiddens = [hiddens] if isinstance(hiddens, str) else list(hiddens)
    per, worlds, classes, cells = [], [], [], None
    for w, h in enumerate(hiddens):
        S, ex = load_scores(h, names)
        per.append(S)
        worlds += [w] * ex.n
        classes += ex.classes.tolist()
        cells = ex.cells
    keys = [k for k in per[0] if all(k in p for p in per)]
    S = {k: np.concatenate([p[k] for p in per]) for k in keys}
    rep = skill_report({"climatology": S["K"], "oracle": S["O"], **{k: S[k] for k in keys if k not in ("K", "O")}},
                       cells=cells, groups=np.array(classes), n_boot=n_boot)
    valid = np.array(rep["valid"], bool)
    out = {"n_items": int(len(worlds)), "n_worlds": len(hiddens), "cells": [list(c) for c in cells],
           "valid_cells": rep["valid"], "policies": ACC.skill(S, valid),
           "oes": {k: {"mean": rep["aggregate"][k], "se": rep["se"][k], "pooled": rep["aggregate_pooled"][k],
                       "per_cell": rep["oes"][k]} for k in rep["aggregate"]},
           "oes_by_program_class": rep.get("by_group")}
    if all(k in S for k in ("K", "P0", "C")):
        out["acceptance"] = ACC.shares({k: S[k] for k in ("K", "D", "P0", "S", "C") if k in S}, valid,
                                       worlds=np.array(worlds), n_boot=n_boot)
    out["policy_labels"] = labels or {}
    del public_report
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--hidden", required=True)
    ap.add_argument("--public", required=True)
    ap.add_argument("--submission", required=True)
    ap.add_argument("--name", default="agent")
    a = ap.parse_args()
    print(json.dumps(grade(a.hidden, a.submission, a.public, a.name), indent=1))


if __name__ == "__main__":
    main()
