"""evaluator.submission -- snapshot, validate and run a submitted predictor (one fresh process per request).

snapshot      copies regular files only (no symlinks, bounded size) from the agent's directory to an
              evaluator-owned directory and returns a manifest of SHA-256 hashes
run_request   one request -> one sandboxed process (evaluator.sandbox: rlimits, wall clock, clean environment,
              and when root: hidden paths absent, no network, unprivileged uid) -> samples or an error
validate      two public example requests: runs, shapes, finite values, same seed -> same samples.
              No accuracy feedback: the requests come from the public prior mean, not the hidden world.
"""
from __future__ import annotations

import hashlib
import json
import os
import shutil
import sys
import tempfile

import numpy as np

from . import sandbox

PYTHON = sys.executable
NOBODY = 65534


def snapshot(src: str, dst: str, max_mib: float) -> dict:
    src = os.path.realpath(src)
    if not os.path.isdir(src):
        raise ValueError("submission directory not found")
    files, total = [], 0
    for root, dirs, names in os.walk(src, followlinks=False):
        dirs[:] = [d for d in sorted(dirs) if not os.path.islink(os.path.join(root, d)) and d != "__pycache__"]
        for nm in sorted(names):
            p = os.path.join(root, nm)
            if os.path.islink(p) or not os.path.isfile(p):
                continue
            total += os.path.getsize(p)
            if total > max_mib * 2 ** 20:
                raise ValueError(f"submission larger than {max_mib:g} MiB")
            files.append(os.path.relpath(p, src))
    if "predict.py" not in files:
        raise ValueError("submission has no predict.py")
    if os.path.exists(dst):
        shutil.rmtree(dst)
    man = []
    for rel in files:
        out = os.path.join(dst, rel)
        os.makedirs(os.path.dirname(out), exist_ok=True)
        with open(os.path.join(src, rel), "rb") as f:
            data = f.read()
        with open(out, "wb") as f:
            f.write(data)
        os.chmod(out, 0o444)
        man.append({"path": rel, "bytes": len(data), "sha256": hashlib.sha256(data).hexdigest()})
    for root, dirs, _ in os.walk(dst):
        os.chmod(root, 0o555)
    return {"files": man, "bytes": total}


def run_request(sub_dir: str, public_dir: str, req: dict, limits: dict, hide=(), work=None) -> dict:
    """Returns {"ok", "samples" {level: array} | "error", "cpu_s", "wall_s", "timed_out"}."""
    tmp = tempfile.mkdtemp(prefix="req-", dir=work)
    os.chmod(tmp, 0o777)
    try:
        rq, out, err = (os.path.join(tmp, n) for n in ("request.npz", "reply.npz", "stderr.txt"))
        np.savez(rq, **req)
        os.chmod(rq, 0o444)
        binds = [(sub_dir, "submission", "ro"), (public_dir, "public", "ro"), (tmp, "io", "rw")]
        pth = sandbox.plan(binds)
        runner = os.path.join(pth["public"], "physim2", "predict_runner.py")
        with open(err, "wb") as ef:
            r = sandbox.run([PYTHON, "-I", "-B", runner, pth["submission"], os.path.join(pth["io"], "request.npz"),
                             os.path.join(pth["io"], "reply.npz")], cwd=pth["io"], binds=binds,
                            cpu_seconds=limits.get("cpu_seconds"), wall_seconds=limits.get("wall_seconds"),
                            memory_gib=limits.get("memory_gib"), hide=hide, uid=NOBODY, no_network=True, stderr=ef)
        res = {"cpu_s": r["cpu_s"], "wall_s": r["wall_s"], "timed_out": r["timed_out"], "layers": r["layers"]}
        if r["returncode"] != 0 or not os.path.exists(out):
            msg = open(err, "rb").read()[-1500:].decode("utf-8", "replace")
            cap = limits.get("cpu_seconds")
            why = ("wall-clock limit" if r["timed_out"] else "CPU-time limit" if cap and r["cpu_s"] >= 0.98 * cap
                   else f"exit code {r['returncode']}")
            return dict(res, ok=False, error=f"predictor failed ({why}): {msg}")
        try:
            z = np.load(out, allow_pickle=False)
            S = {int(k[5:]): np.asarray(z[k], float) for k in z.files}
        except Exception as e:
            return dict(res, ok=False, error=f"unreadable reply: {type(e).__name__}")
        return dict(res, ok=True, samples=S)
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


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
