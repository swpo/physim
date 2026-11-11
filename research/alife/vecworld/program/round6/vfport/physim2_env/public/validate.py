"""physim2.validate -- check a submission in YOUR box, with the grader's own rules and runner (public code).

    python -m physim2.validate submission          (or lab.validate("submission"))

What runs: the freeze rules of physim2/_rules.py (regular files only, size cap, predict.py at the top), then
your predictor on two public example requests through physim2/_item.py, the same driver the grader uses (one
request per process, CPU, memory and wall-clock limits), three calls in all: example 0 twice with the same seed
(the samples must be identical) and example 1.
The example requests were simulated at the prior mean with public noise: passing says nothing about accuracy.

AS IT WILL BE GRADED. Grading happens in a fresh container that holds only submission/ (read-only), TASK.md and
the original physim2 package: nothing else you wrote exists there. This check therefore runs the predictor from
a clean copy of the submission ALONE, in a temporary directory next to a copy of the physim2 package, and,
when the laboratory started it (lab.validate, lab.submit), as the box's unprivileged user while /workspace is
closed to that user (its mode is 0700 for the seconds the check runs, and is put back afterwards). A predictor
that reads a file outside its own directory, or that names its own files by an absolute path below
/workspace, fails here as it would fail in grading: load your files relative to predict.py.

Where it runs: ONLY inside an exam box, which the environment marks with /etc/physim2/predictor_uid. Started by
the laboratory (lab.validate, lab.submit) the predictor runs as that unprivileged uid and its leftovers are
removed; started by you (python -m physim2.validate) it runs as you, under the limits only (the driver's
--no-box). Without the marker nothing runs: this check executes the predict.py it is given, and a machine that
is not an exam box is no place for that.

`check_shapes` and `validate` below are copied verbatim from agentenv's evaluator/submission.py (lines 94-125);
`run_request` has the same signature and return value as the function they called there.
"""
from __future__ import annotations

import base64
import io
import json
import os
import shutil
import stat
import subprocess
import sys
import tarfile
import tempfile

import numpy as np

from . import _rules

HERE = os.path.dirname(os.path.abspath(__file__))
WORKSPACE = os.path.dirname(HERE)
UID_FILE = "/etc/physim2/predictor_uid"
NOT_A_BOX = f"this check runs inside an exam box only ({UID_FILE} is missing or not root's); nothing was run"
ROUTE_VAR, ROUTE_VALUE = "PHYSIM2_BOX_CLEANUP", "disposable-box"      # set by the laboratory's route only (see _item.py)
GRADED_WHERE = ("Grading happens in a fresh container that holds only submission/ (read-only, at /workspace/submission), TASK.md and "
                "the original physim2 package: nothing else you wrote exists there, and there is no laboratory and no network. ")
AS_GRADED = ("This check ran your predictor the same way: from a clean copy of the directory alone, as an unprivileged user that "
             "could not read /workspace.")
NOT_AS_GRADED = ("This check ran your predictor from a clean copy of the directory alone but with YOUR rights: it could still read "
                 "/workspace. Only lab.validate(...) proves that it runs where it is graded.")


def package_changes(workspace: str = WORKSPACE) -> int | None:
    """How many files of physim2/ in this workspace differ from the package the box was given (MANIFEST.json),
    or are missing. The grader uses the original package, whatever this one looks like. None: no manifest."""
    import hashlib
    try:
        with open(os.path.join(HERE, "MANIFEST.json")) as f:
            man = json.load(f)
    except (OSError, ValueError):
        return None
    n = 0
    for rel, digest in man.items():
        if not rel.startswith("physim2/") or rel.endswith("MANIFEST.json"):
            continue
        try:
            with open(os.path.join(workspace, rel), "rb") as f:
                n += hashlib.sha256(f.read()).hexdigest() != digest
        except OSError:
            n += 1
    return n


def box_uid():
    """The predictor uid the environment wrote into this box, or None outside a prepared box."""
    try:
        st = os.lstat(UID_FILE)
        if not stat.S_ISREG(st.st_mode) or st.st_uid != 0:
            return None
        with open(UID_FILE) as f:
            return int(f.read(32).strip())
    except (OSError, ValueError):
        return None


def run_request(sub_dir: str, public_dir: str, req: dict, limits: dict, hide=(), work=None) -> dict:
    """Returns {"ok", "samples" {level: array} | "error", "cpu_s", "wall_s", "timed_out", "layers"}."""
    uid = box_uid()
    if uid is None:
        return {"ok": False, "error": NOT_A_BOX, "cpu_s": 0.0, "wall_s": 0.0, "timed_out": False, "layers": None}
    tmp = tempfile.mkdtemp(prefix="physim2-req-", dir=work)
    try:
        os.chmod(tmp, 0o755)
        rq = os.path.join(tmp, "request.npz")
        np.savez(rq, **req)
        os.chmod(rq, 0o444)
        cmd = [sys.executable, "-I", "-B", os.path.join(HERE, "_item.py"), "--submission", sub_dir,
               "--runner", os.path.join(public_dir, "physim2", "predict_runner.py"), "--request", rq,
               "--cpu", str(limits.get("cpu_seconds") or 0), "--wall", str(limits.get("wall_seconds") or 0),
               "--mem-gib", str(limits.get("memory_gib") or 0), "--uid", str(uid), "--no-box"]
        # --no-box matters only when YOU start this check (no route variable): the predictor then runs as you.
        # Started by the laboratory, the driver drops to `uid` and cleans up, or refuses and runs nothing.
        p = subprocess.run(cmd, capture_output=True, text=True)
        try:
            r = json.loads(p.stdout.strip().splitlines()[-1])
        except Exception:
            return {"ok": False, "error": "the request driver failed: " + p.stderr[-300:], "cpu_s": 0.0, "wall_s": 0.0,
                    "timed_out": False, "layers": None}
        res = {"cpu_s": r["cpu_s"], "wall_s": r["wall_s"], "timed_out": r["timed_out"], "layers": r.get("layers")}
        if r.get("driver_error"):
            return dict(res, ok=False, error="the request driver refused or failed: " + str(r["driver_error"]))
        if not r["ok"]:
            return dict(res, ok=False, error=f"predictor failed ({r.get('why')}): {r.get('stderr', '')}")
        try:
            S = _rules.read_reply(base64.b64decode(r["reply_b64"]), 1 << 24)
        except ValueError as e:
            return dict(res, ok=False, error=f"unreadable reply: {e}")
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
    if box_uid() is None:
        return {"ok": False, "stage": "validator", "error": NOT_A_BOX, "finalized": False}
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
    # Started by the laboratory (root, route variable): the predictor will run as the box's unprivileged user, and
    # for that user /workspace is closed while the check runs, as it does not exist where the predictor is graded.
    hide = os.geteuid() == 0 and os.environ.get(ROUTE_VAR) == ROUTE_VALUE
    mode = None
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
        # the public package next to it, as in the grader's box (a copy: /workspace itself is closed below)
        shutil.copytree(HERE, os.path.join(tmp, "physim2"), symlinks=False, ignore=shutil.ignore_patterns("__pycache__"))
        for root, dirs, files in os.walk(os.path.join(tmp, "physim2")):
            os.chmod(root, 0o755)
            for nm in files:
                os.chmod(os.path.join(root, nm), 0o644)
        ex = np.load(os.path.join(HERE, "examples.npz"))
        ex = {k: np.asarray(ex[k]) for k in ("history", "prefix", "test")}
        if hide:
            ws = os.path.realpath(workspace)
            st = os.lstat(ws)
            if stat.S_ISDIR(st.st_mode) and st.st_uid == 0 and ws not in ("/", "/tmp"):
                mode = stat.S_IMODE(st.st_mode)
                os.chmod(ws, 0o700)
        rep = validate(dst, tmp, ex, queries, dims, limits)
    finally:
        if mode is not None:
            try:
                os.chmod(os.path.realpath(workspace), mode)
            except OSError:
                pass
        for root, dirs, files in os.walk(tmp):
            os.chmod(root, 0o755)
        shutil.rmtree(tmp, ignore_errors=True)
    rep["files"] = len(man["files"])
    rep["finalized"] = False
    rep["as_graded"] = bool(hide and mode is not None)
    rep["grading"] = GRADED_WHERE + (AS_GRADED if rep["as_graded"] else NOT_AS_GRADED)
    changed = package_changes(workspace)
    if changed:
        rep["package_changed_files"] = int(changed)
        rep["grading"] += (f" Note: {int(changed)} file(s) of physim2/ in this workspace differ from the original package; the grader "
                           "uses the original.")
    return rep


if __name__ == "__main__":
    print(json.dumps(check(sys.argv[1] if len(sys.argv) > 1 else "submission"), indent=1, default=str))
