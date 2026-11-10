"""physim2.validate -- check a submission in YOUR box, with the grader's own rules and runner (public code).

    python -m physim2.validate submission          (or lab.validate("submission"))

What runs: the freeze rules of physim2/_rules.py (regular files only, size cap, predict.py at the top), then
your predictor on two public example requests through physim2/_item.py, the same driver the grader uses (one
request per process, unprivileged user when this box runs as root, CPU, memory and wall-clock limits), three
calls in all: example 0 twice with the same seed (the samples must be identical) and example 1.
The example requests were simulated at the prior mean with public noise: passing says nothing about accuracy.

`check_shapes` and `validate` below are copied verbatim from agentenv's evaluator/submission.py (lines 94-125);
`run_request` has the same signature and return value as the function they called there.
"""
from __future__ import annotations

import base64
import io
import json
import os
import shutil
import subprocess
import sys
import tarfile
import tempfile

import numpy as np

from . import _rules

HERE = os.path.dirname(os.path.abspath(__file__))
WORKSPACE = os.path.dirname(HERE)


def run_request(sub_dir: str, public_dir: str, req: dict, limits: dict, hide=(), work=None) -> dict:
    """Returns {"ok", "samples" {level: array} | "error", "cpu_s", "wall_s", "timed_out", "layers"}."""
    tmp = tempfile.mkdtemp(prefix="physim2-req-", dir=work)
    try:
        os.chmod(tmp, 0o755)
        rq = os.path.join(tmp, "request.npz")
        np.savez(rq, **req)
        os.chmod(rq, 0o444)
        cmd = [sys.executable, "-I", "-B", os.path.join(HERE, "_item.py"), "--submission", sub_dir,
               "--runner", os.path.join(public_dir, "physim2", "predict_runner.py"), "--request", rq,
               "--cpu", str(limits.get("cpu_seconds") or 0), "--wall", str(limits.get("wall_seconds") or 0),
               "--mem-gib", str(limits.get("memory_gib") or 0)]
        p = subprocess.run(cmd, capture_output=True, text=True)
        try:
            r = json.loads(p.stdout.strip().splitlines()[-1])
        except Exception:
            return {"ok": False, "error": "the request driver failed: " + p.stderr[-300:], "cpu_s": 0.0, "wall_s": 0.0,
                    "timed_out": False, "layers": None}
        res = {"cpu_s": r["cpu_s"], "wall_s": r["wall_s"], "timed_out": r["timed_out"], "layers": r.get("layers")}
        if not r["ok"]:
            return dict(res, ok=False, error=f"predictor failed ({r.get('why')}): {r.get('stderr', '')}")
        try:
            S = _rules.read_reply(base64.b64decode(r["reply_b64"]), 1 << 26)
        except Exception as e:
            return dict(res, ok=False, error=f"unreadable reply: {type(e).__name__}")
        return dict(res, ok=True, samples=S)
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


# ---- verbatim from agentenv evaluator/submission.py:94-125 ----------------------------------------------------
def check_shapes(S: dict, queries: dict, dims: dict, n_samples: int):
    for l, ts in queries.items():
        if l not in S:
            return f"level {l} missing"
        if S[l].shape != (n_samples, len(ts), dims[l]):
            return f"level {l} has shape {S[l].shape}, expected {(n_samples, len(ts), dims[l])}"
        if not np.all(np.isfinite(S[l])):
            return f"level {l} has non-finite values"
    return None


def validate(sub_dir: str, public_dir: str, examples: dict, queries: dict, dims: dict, limits: dict, hide=(),
             work=None) -> dict:
    n = int(limits["n_samples"])
    q = json.dumps({str(l): v for l, v in queries.items()})
    runs = []
    for i, seed in ((0, 0), (0, 0), (1, 1)):
        req = {"history": examples["history"][i], "prefix": examples["prefix"][i], "test": examples["test"][i],
               "queries": q, "n_samples": n, "seed": seed}
        r = run_request(sub_dir, public_dir, req, limits, hide, work)
        if not r["ok"]:
            return {"ok": False, "stage": f"example {i}", "error": r["error"], "cpu_s": r["cpu_s"], "wall_s": r["wall_s"]}
        bad = check_shapes(r["samples"], queries, dims, n)
        if bad:
            return {"ok": False, "stage": f"example {i}", "error": bad}
        runs.append(r)
    same = all(np.array_equal(runs[0]["samples"][l], runs[1]["samples"][l]) for l in queries)
    if not same:
        return {"ok": False, "stage": "reproducibility", "error": "the same request and seed gave different samples"}
    return {"ok": True, "cpu_s_per_request": max(r["cpu_s"] for r in runs), "wall_s_per_request": max(r["wall_s"] for r in runs),
            "limits": {k: limits[k] for k in ("cpu_seconds", "wall_seconds", "memory_gib", "n_samples")},
            "note": "format and reproducibility only; no accuracy feedback"}
# ---- end of the verbatim part ---------------------------------------------------------------------------------


def resolve(path, workspace: str = WORKSPACE) -> str:
    """The submission path, which must lie inside the workspace (as the round-5 laboratory required)."""
    ws = os.path.realpath(workspace)
    p = os.path.realpath(os.path.join(ws, str(path)))
    if not (p == ws or p.startswith(ws + os.sep)):
        raise ValueError("format: the submission path must lie inside the workspace")
    return p


def check(path="submission", decl: dict | None = None, workspace: str = WORKSPACE) -> dict:
    """Freeze rules, then the three example calls. `decl` is lab.card() (or physim2/exam.json, its public part)."""
    if decl is None:
        decl = json.load(open(os.path.join(HERE, "exam.json")))
    limits = decl["predictor_limits"]
    queries = {int(l): v for l, v in decl["exam"]["queries"].items()}
    dims = {int(l): v for l, v in decl["level_dims"].items()}
    src = resolve(path, workspace)
    if not os.path.isdir(src):
        return {"ok": False, "stage": "artifact", "error": "submission directory not found", "finalized": False}
    frozen, man, err = _rules.freeze(_rules.tar_dir(src), ".", limits["artifact_mib"])
    if err:
        return {"ok": False, "stage": "artifact", "error": err, "finalized": False}
    tmp = tempfile.mkdtemp(prefix="physim2-validate-")
    try:
        os.chmod(tmp, 0o755)
        dst = os.path.join(tmp, "submission")
        os.makedirs(dst)
        with tarfile.open(fileobj=io.BytesIO(frozen), mode="r:") as tar:
            tar.extractall(dst, filter="data")
        for root, dirs, files in os.walk(dst):                # read-only, as in the grader's box
            for nm in files:
                os.chmod(os.path.join(root, nm), 0o444)
            os.chmod(root, 0o555)
        ex = np.load(os.path.join(HERE, "examples.npz"))
        rep = validate(dst, workspace, ex, queries, dims, limits)
    finally:
        for root, dirs, files in os.walk(tmp):
            os.chmod(root, 0o755)
        shutil.rmtree(tmp, ignore_errors=True)
    rep["files"] = len(man["files"])
    rep["finalized"] = False
    return rep


if __name__ == "__main__":
    print(json.dumps(check(sys.argv[1] if len(sys.argv) > 1 else "submission"), indent=1, default=str))
