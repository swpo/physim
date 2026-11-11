"""physim2.validate -- check a submission in YOUR box, with the grader's own rules and runner (public code).

    python -m physim2.validate submission          (or lab.validate("submission"))

What runs: the freeze rules of physim2/_rules.py (regular files only, size cap, predict.py at the top), then
your predictor on two public example requests through physim2/_item.py, the same driver the grader uses (one
request per process, CPU, memory and wall-clock limits), three calls in all: example 0 twice with the same seed
(the samples must be identical) and example 1.
The example requests were simulated at the prior mean with public noise: passing says nothing about accuracy.

AS IT WILL BE GRADED. Grading happens in a fresh container that holds only submission/ (read-only), TASK.md and
the original physim2 package: nothing else you wrote exists there. This check therefore runs the predictor from
a clean copy of the submission ALONE, in a temporary directory next to a copy of the physim2 package as
MANIFEST.json lists it (a file you changed or removed in physim2/ makes the check fail and is named; a file you
added there is not copied), and, when the laboratory started it (lab.validate, lab.submit), as the box's
unprivileged user while /workspace is closed to that user (its mode is 0700 for the seconds the check runs, and
is put back afterwards) and so is every entry already in /tmp, /dev/shm, /etc/physim2 and /runtime (their "other" rights are taken away
and given back afterwards; both places stay writable, as they are in grading). A predictor that reads a file
outside its own directory, or that names its own files by an absolute path below /workspace, fails here as it
would fail in grading: load your files relative to predict.py.

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
AS_GRADED = ("This check ran your predictor the same way: from a clean copy of the directory alone, next to the original physim2 "
             "package, as an unprivileged user that could not read /workspace, nor anything this box already held in /tmp, /dev/shm, "
             "/etc/physim2 or /runtime.")
NOT_AS_GRADED = ("This check ran your predictor from a clean copy of the directory alone but with YOUR rights: it could still read "
                 "/workspace. Only lab.validate(...) proves that it runs where it is graded.")


def package_entries(workspace: str = WORKSPACE):
    """{relative path below physim2/: sha256} of the package the box was given (MANIFEST.json), or None."""
    try:
        with open(os.path.join(HERE, "MANIFEST.json")) as f:
            man = json.load(f)
    except (OSError, ValueError):
        return None
    if not isinstance(man, dict):
        return None
    return {rel[len("physim2/"):]: d for rel, d in man.items()
            if isinstance(rel, str) and rel.startswith("physim2/") and not rel.endswith("MANIFEST.json")}


def package_differences(workspace: str = WORKSPACE) -> list | None:
    """The files of physim2/ in this workspace that differ from the package the box was given, or are missing
    (relative names, sorted). The grader uses the original package, whatever this one looks like. None: no
    manifest. Files ADDED to physim2/ are not differences: they are simply not copied (copy_package)."""
    import hashlib
    entries = package_entries(workspace)
    if entries is None:
        return None
    bad = []
    for rel, digest in sorted(entries.items()):
        p = os.path.join(workspace, "physim2", rel)
        try:
            if not stat.S_ISREG(os.lstat(p).st_mode):
                bad.append(rel)
                continue
            with open(p, "rb") as f:
                if hashlib.sha256(f.read()).hexdigest() != digest:
                    bad.append(rel)
        except OSError:
            bad.append(rel)
    return bad


def package_changes(workspace: str = WORKSPACE) -> int | None:
    """How many files of physim2/ differ from the package the box was given (see package_differences)."""
    bad = package_differences(workspace)
    return None if bad is None else len(bad)


def copy_package(workspace: str, dst: str) -> None:
    """The public package as the grader's box holds it: the files that MANIFEST.json lists (each checked against
    its sha256 by the caller first) and MANIFEST.json, and nothing else. A file the agent ADDED to physim2/ is
    not in the grader's box, so it is not in this copy either."""
    entries = package_entries(workspace) or {}
    for rel in sorted(list(entries) + ["MANIFEST.json"]):
        parts = [p for p in rel.split("/") if p not in ("", ".")]
        if not parts or ".." in parts:
            continue
        src = os.path.join(workspace, "physim2", *parts)
        out = os.path.join(dst, *parts)
        os.makedirs(os.path.dirname(out), exist_ok=True)
        shutil.copyfile(src, out, follow_symlinks=False)


# The scratch places of the agent's box that a grading box has too, but empty: the predictor must not find there
# what the agent left. For the seconds of the check every entry already in them is closed to other users
# (its mode loses r, w and x for "others"), and is given its mode back afterwards. The places stay writable, as
# they are in grading. (/workspace itself is closed as a whole, below.)
# Round 5 (exam audit X16): also the exam's own places of the box, /etc/physim2 and /runtime, which root can write
# to: a grading box has its own files there, never the agent's (the check itself runs as root and is not affected).
SCRATCH_PLACES = ("/tmp", "/dev/shm", "/etc/physim2", "/runtime")


def close_entries(places, keep=()) -> list:
    """[(path, mode before)] of every entry directly in `places` (no link, nothing in `keep`) whose mode gave
    "others" any right, after taking those rights away. Never raises."""
    done = []
    for place in places:
        try:
            names = os.listdir(place)
        except OSError:
            continue
        for nm in names:
            p = os.path.join(place, nm)
            if p in keep:
                continue
            try:
                st = os.lstat(p)
                if stat.S_ISLNK(st.st_mode) or not st.st_mode & 0o007:
                    continue
                os.chmod(p, stat.S_IMODE(st.st_mode) & ~0o007)
                done.append((p, stat.S_IMODE(st.st_mode)))
            except OSError:
                continue
    return done


def reopen_entries(done) -> None:
    for p, mode in reversed(done):
        try:
            if not stat.S_ISLNK(os.lstat(p).st_mode):
                os.chmod(p, mode)
        except OSError:
            pass


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
        max_values = int(limits.get("max_reply_values") or 1 << 24)     # as the grader bounds a reply (grading.grade)
        cmd = [sys.executable, "-I", "-B", os.path.join(HERE, "_item.py"), "--submission", sub_dir,
               "--runner", os.path.join(public_dir, "physim2", "predict_runner.py"), "--request", rq,
               "--cpu", str(limits.get("cpu_seconds") or 0), "--wall", str(limits.get("wall_seconds") or 0),
               "--mem-gib", str(limits.get("memory_gib") or 0), "--uid", str(uid), "--no-box",
               "--max-reply-mib", str(_rules.reply_mib(max_values))]
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
            S = _rules.read_reply(base64.b64decode(r["reply_b64"]), max_values)
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
    queries = {int(l): v for l, v in decl["exam"]["queries"].items()}
    dims = {int(l): v for l, v in decl["level_dims"].items()}
    limits = dict(decl["predictor_limits"],                  # the reply bound of grading.grade: samples x values asked for
                  max_reply_values=int(decl["predictor_limits"]["n_samples"]) * sum(len(ts) * dims[l] for l, ts in queries.items()))
    src = resolve(path, workspace)
    if not os.path.isdir(src):
        return {"ok": False, "stage": "artifact", "error": "submission directory not found", "finalized": False}
    frozen, man, err = _rules.freeze(_rules.tar_dir(src), ".", limits["artifact_mib"])
    if err:
        return {"ok": False, "stage": "artifact", "error": err, "finalized": False}
    # Round 4, second pass (exam audit X6): the predictor is run next to the package the GRADER holds, which is the
    # original. A changed or missing file of physim2/ makes this check unable to run it as graded: it fails here
    # and names the files. Files added to physim2/ are left out of the copy, as they are absent in grading.
    diff = package_differences(workspace)
    if diff is None:
        return {"ok": False, "stage": "package", "error": "physim2/MANIFEST.json is missing or unreadable: the check cannot tell "
                "which package the grader holds", "finalized": False}
    if diff:
        return {"ok": False, "stage": "package", "package_changed_files": len(diff), "finalized": False,
                "error": (f"{len(diff)} file(s) of physim2/ differ from the package this box was given or are missing ("
                          + ", ".join(diff[:8]) + (", ..." if len(diff) > 8 else "") + "). The grader runs your predictor next to the "
                          "ORIGINAL package, so this check cannot run it as graded. Put the original files back (physim2/MANIFEST.json "
                          "lists each with its sha256); keep your own code in submission/.")}
    tmp = tempfile.mkdtemp(prefix="physim2-validate-")
    # Started by the laboratory (root, route variable): the predictor will run as the box's unprivileged user, and
    # for that user /workspace is closed while the check runs, as it does not exist where the predictor is graded;
    # so is every entry the box already holds in SCRATCH_PLACES, which in grading are empty or hold the exam's own files.
    hide = os.geteuid() == 0 and os.environ.get(ROUTE_VAR) == ROUTE_VALUE
    mode, closed, scratch_closed = None, [], False
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
        # the public package next to it, as in the grader's box: the manifest's files only (a copy: /workspace
        # itself is closed below)
        copy_package(workspace, os.path.join(tmp, "physim2"))
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
            closed = close_entries(SCRATCH_PLACES, keep={tmp})
            scratch_closed = True
        rep = validate(dst, tmp, ex, queries, dims, limits)
    finally:
        reopen_entries(closed)
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
    rep["as_graded"] = bool(hide and mode is not None and scratch_closed)
    rep["grading"] = GRADED_WHERE + (AS_GRADED if rep["as_graded"] else NOT_AS_GRADED)
    return rep


if __name__ == "__main__":
    _rep = check(sys.argv[1] if len(sys.argv) > 1 else "submission")
    print(json.dumps(_rep, indent=1, default=str))
    if not _rep.get("as_graded"):                            # round 5 (X16): said once more, apart from the report (stdout stays JSON)
        print("NOTE: run by you, this check is NOT the check as graded (your predictor ran with your rights and could read "
              "/workspace). Run lab.validate(\"submission\") (or the tool op validate) for the check as graded.", file=sys.stderr)
