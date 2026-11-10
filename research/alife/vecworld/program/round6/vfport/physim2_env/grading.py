"""The reward's work: the frozen exam item by item in the fresh verifier box, scored on the worker.

One request at a time (memo hole 1): the worker writes ONE request file into the box, root starts the public
driver (public/_item.py), which runs agentenv's predict_runner.py as an unprivileged user under the declared
limits, returns the reply and then kills that user's processes and deletes everything it owns. The next item's
request only then enters the box. Truths, the climatology pool, item ids and program classes never enter it.

Arithmetic: agentenv's, unchanged and by import -- FrozenExam.request / score / references
(evaluator/instance.py:149-172), check_shapes (evaluator/submission.py:94-102), failed item = K
(evaluator/grader.py:45-56), pooled L and skill (evaluator/acceptance.py:61-68).
"""
from __future__ import annotations

import base64
import io
import json
import os
import time

import numpy as np

from ._paths import use_agentenv
from .public import _rules

RUNTIME_DIR = "/runtime"
UID = 1000


def exam(hidden: str):
    use_agentenv()
    from evaluator import instance as INST
    return INST.FrozenExam(hidden)


def request_bytes(ex, i: int, m: int, seed: int) -> bytes:
    buf = io.BytesIO()
    np.savez(buf, **ex.request(i, m, seed))
    return buf.getvalue()


def save(hidden: str, name: str, es, failed, cpu, record: dict) -> None:
    """Per-item scores stay on the worker, in the format evaluator.grader.table() reads."""
    os.makedirs(os.path.join(hidden, "grades"), exist_ok=True)
    np.savez_compressed(os.path.join(hidden, "grades", f"{name}.npz"), es=es, failed=failed, cpu=cpu)
    json.dump(record, open(os.path.join(hidden, "grades", f"{name}.json"), "w"), indent=1)


def summary(ex, es, refs) -> dict:
    """Pooled L of this predictor, of K and of O, and the skill on the K-to-O scale, over the cells whose
    K-to-O gap is significant (vw.scoring.cells_ok, decided on the references before any agent): the same
    number as policies[...]["vs_O"] of evaluator.grader.table for this world."""
    use_agentenv()
    from evaluator import acceptance as ACC
    from vw.scoring import cells_ok
    valid = np.asarray(cells_ok(refs["K"], refs["O"], 3.0), bool)
    if not valid.any():
        valid = np.ones(len(valid), bool)
    s = ACC.skill({"K": refs["K"], "O": refs["O"], "agent": es}, valid)
    return {"L": s["agent"]["L"], "L_K": s["K"]["L"], "L_O": s["O"]["L"], "skill_vs_O": s["agent"]["vs_O"],
            "valid_cells": valid.tolist()}


def score_as_k(hidden: str, name: str, reason: str) -> dict:
    """No usable predictor: every item is scored as K (run_rollout.finalize, lines 103-108)."""
    ex = exam(hidden)
    refs = ex.references()
    es = refs["K"].copy()
    rec = {"name": name, "n_items": ex.n, "n_failed": ex.n, "reason": reason, "errors": [], "seconds": 0.0}
    save(hidden, name, es, np.ones(ex.n, bool), np.zeros(ex.n), rec)
    return dict(summary(ex, es, refs), n_items=ex.n, n_failed=ex.n, reason=reason)


async def box_cpu_seconds(runtime) -> float | None:
    """CPU seconds consumed so far by every process of the box (its cgroup counter; cgroup v2, then v1)."""
    try:
        r = await runtime.run(["sh", "-c", "cat /sys/fs/cgroup/cpu.stat 2>/dev/null | awk '$1==\"usage_usec\"{print $2/1e6; f=1} END{exit !f}' "
                                           "|| awk '{print $1/1e9}' /sys/fs/cgroup/cpuacct/cpuacct.usage"], {})
        return float(r.stdout.strip().splitlines()[-1]) if r.exit_code == 0 else None
    except Exception:
        return None


async def stage(runtime, workdir: str) -> dict:
    """Trusted staging after the artifacts are restored: the driver and its directory, root-owned and
    read-only; the restored submission read-only and owned by root. No submitted code runs here."""
    here = os.path.dirname(os.path.abspath(__file__))
    await runtime.write(f"{RUNTIME_DIR}/item.py", open(os.path.join(here, "public", "_item.py"), "rb").read())
    sub = f"{workdir}/submission"
    r = await runtime.run(["sh", "-c",
                           f'umask 022; mkdir -p {RUNTIME_DIR} && chown -R 0:0 {RUNTIME_DIR} && chmod 755 {RUNTIME_DIR} && chmod 644 {RUNTIME_DIR}/item.py; '
                           f'if [ -d {sub} ]; then chown -R -h 0:0 {sub} && chmod -R a-w,a+rX {sub}; fi; '
                           f'chown -R -h 0:0 {workdir}/physim2 {workdir}/TASK.md && chmod -R go-w {workdir}; '
                           f'test -f {sub}/predict.py && echo HAS_PREDICT || echo NO_PREDICT'], {})
    if r.exit_code:
        raise RuntimeError("staging the verifier box failed")
    scan = await runtime.run(["python3", "-I", "-B", f"{RUNTIME_DIR}/item.py", "--scan", "--uid", str(UID)], {})
    rep = json.loads(scan.stdout.strip().splitlines()[-1]) if scan.exit_code == 0 and scan.stdout.strip() else {}
    return {"has_predict": "HAS_PREDICT" in r.stdout, "scan": rep}


async def grade(runtime, hidden: str, name: str, limits: dict, workdir: str, *, seed: int = 0, cleanup: bool = True,
                deadline: float | None = None) -> dict:
    """The loop of evaluator/grader.py:34-64, with the request sent into the box one item at a time."""
    use_agentenv()
    from evaluator import submission as SUB
    ex = exam(hidden)
    m = int(limits["n_samples"])
    refs = ex.references()
    S = {l: np.zeros((ex.n, m, len(ts), ex.dims[l])) for l, ts in ex.queries.items()}
    max_values = 4 * m * sum(len(ts) * ex.dims[l] for l, ts in ex.queries.items())
    failed, cpu, wall, errors = np.zeros(ex.n, bool), np.zeros(ex.n), np.zeros(ex.n), []
    cleanups, layers, dirty = [], None, None
    cmd = ["python3", "-I", "-B", f"{RUNTIME_DIR}/item.py", "--submission", f"{workdir}/submission",
           "--runner", f"{workdir}/physim2/predict_runner.py", "--request", f"{RUNTIME_DIR}/request.npz",
           "--cpu", str(limits.get("cpu_seconds") or 0), "--wall", str(limits.get("wall_seconds") or 0),
           "--mem-gib", str(limits.get("memory_gib") or 0), "--uid", str(UID)] + ([] if cleanup else ["--no-cleanup"])
    t0 = time.time()
    for i in range(ex.n):
        bad = None
        if dirty is not None:
            bad = "the box could not be cleaned after an earlier item"
        elif deadline is not None and time.time() > deadline:
            bad = "grading ran out of time"
        if bad is None:
            try:
                await runtime.write(f"{RUNTIME_DIR}/request.npz", request_bytes(ex, i, m, seed))
                out = await runtime.run(cmd, {})
                r = json.loads(out.stdout.strip().splitlines()[-1])
            except Exception as e:                           # the box or the driver, not the predictor
                r = {"ok": False, "why": "driver error", "stderr": type(e).__name__, "cpu_s": 0.0, "wall_s": 0.0}
            cpu[i], wall[i] = r.get("cpu_s", 0.0), r.get("wall_s", 0.0)
            layers = r.get("layers") or layers
            c = r.get("cleanup")
            if c is not None:
                cleanups.append({"item": i, "killed": c["killed"], "removed": c["removed"], "ipc_removed": c["ipc_removed"]})
                if c["left_pids"] or c["left_files"]:
                    dirty = i
            if not r.get("ok"):
                bad = f"predictor failed ({r.get('why')}): {r.get('stderr', '')}"
            else:
                try:
                    smp = _rules.read_reply(base64.b64decode(r["reply_b64"]), max_values)
                    bad = SUB.check_shapes(smp, ex.queries, ex.dims, m)
                except Exception as e:
                    bad = f"unreadable reply: {type(e).__name__}"
        if bad:
            failed[i] = True
            errors.append({"item": i, "error": bad[:4000]})
            continue
        for l in ex.queries:
            S[l][i] = smp[l]
    sc = ex.score(S)
    sc[failed] = refs["K"][failed]                           # a failed request is scored as K
    rec = {"name": name, "n_items": ex.n, "n_failed": int(failed.sum()), "cpu_s_mean": float(cpu.mean()),
           "cpu_s_max": float(cpu.max()), "wall_s_mean": float(wall.mean()), "seconds": time.time() - t0,
           "errors": errors, "layers": layers, "cleanups": cleanups, "box_not_clean_after_item": dirty,
           "cleanup_between_items": cleanup}
    save(hidden, name, sc, failed, cpu, rec)
    return dict(summary(ex, sc, refs), n_items=ex.n, n_failed=int(failed.sum()), cpu_s_mean=float(cpu.mean()),
                cpu_s_max=float(cpu.max()), wall_s_mean=float(wall.mean()), seconds=time.time() - t0, layers=layers,
                items_with_leftovers=sum(1 for c in cleanups if c["killed"] or c["removed"] or c["ipc_removed"]),
                box_not_clean_after_item=dirty, cleanup_between_items=cleanup)
