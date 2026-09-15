"""build_blob5_truth.py — round-5 truth builder (BLOB2v2, spec 2.6).

Stages per (world, seed):
  pass      ONE deterministic base replay -> exact f32 anchor states +
            degenerate single-member truths (r5_*_anchors.npz). Self-gates:
            bitwise state match at the cached 1700 snapshot, replay==live
            vs the f16 record at A0 tolerance.
  member    ensemble member chunks (independent live replicas, verbatim
            step_chunk dynamics, salted noise streams) -> partial npz.
  assemble  frozen truth npz r5_{world}_s{seed}_truth.npz with a per-array
            sha256 manifest (determinism gate G-R6 compares two builds).

Run (repo root):
  .venv/bin/python environments/physim/tools/build_blob5_truth.py all
  ... all --cache-dir /tmp/r5_verify        # G-R6 second build
Orchestrates subprocesses; ~2h wall for the 6 (world, seed) pairs on an
M4 (10 cores). Idempotent: existing files are skipped.
"""
import argparse
import json
import os
import subprocess
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.normpath(os.path.join(HERE, "..", "..", ".."))
sys.path.insert(0, os.path.join(REPO, "environments", "physim"))
PY = os.environ.get("PHYSIM_BUILD_PY") or os.path.join(
    REPO, ".venv", "bin", "python")
ME = os.path.abspath(__file__)

PAIRS = [("p4g2_044", s, "E1") for s in (928, 929, 930)] + \
        [("p6g8_033", s, "E2") for s in (942, 943, 944)]


def _r5():
    """Import physim.blobround5. On build hosts without the full taskset
    stack (no `verifiers`), bypass physim/__init__ with a package shim —
    the build needs only blobcore/blobround2/blobround5 (numpy + agentenv +
    blobkit)."""
    try:
        from physim import blobround5 as R5
        return R5
    except ModuleNotFoundError:
        import importlib
        import types
        pkg = types.ModuleType("physim")
        pkg.__path__ = [os.path.join(REPO, "environments", "physim",
                                     "physim")]
        sys.modules["physim"] = pkg
        return importlib.import_module("physim.blobround5")


def cmd_pass(a):
    R5 = _r5()
    R5.build_anchors(a.world, a.seed, a.menu, cache_dir=a.cache_dir)
    return 0


def cmd_member(a):
    R5 = _r5()
    R5.run_member_chunk(a.world, a.seed, a.menu, a.cid, a.m0, a.m1,
                        cache_dir=a.cache_dir, workers=1)
    return 0


def cmd_assemble(a):
    R5 = _r5()
    p = R5.assemble_truth(a.world, a.seed, a.menu, cache_dir=a.cache_dir)
    man = json.loads(str(__import__("numpy").load(p)["manifest"]))
    print(f"[assemble] {p}")
    for k, v in man["hashes"].items():
        print(f"  {k}: {v[:16]}")
    return 0


def _run_queue(jobs, max_proc, tag, cap_threads=True):
    """jobs: list of (label, argv). Simple polling scheduler. MEMBER
    workers get single-threaded BLAS/FFT (parallelism lives at the process
    level; uncapped BLAS threads across many workers thrash). PASS jobs
    keep DEFAULT threading: the bitwise 1700-snapshot gate requires the
    same numeric env convention the A0 caches were built with (BLAS thread
    count changes tensordot summation order)."""
    env = {**os.environ}
    if cap_threads:
        env.update({
            "VECLIB_MAXIMUM_THREADS": "1", "OPENBLAS_NUM_THREADS": "1",
            "OMP_NUM_THREADS": "1", "MKL_NUM_THREADS": "1",
            "NUMEXPR_NUM_THREADS": "1"})
    todo = list(jobs)
    live = []
    fail = []
    t0 = time.time()
    n_all = len(todo)
    while todo or live:
        while todo and len(live) < max_proc:
            label, argv = todo.pop(0)
            p = subprocess.Popen(argv, stdout=subprocess.PIPE,
                                 stderr=subprocess.STDOUT, text=True,
                                 env=env)
            live.append((label, p))
            print(f"[{tag}] start {label} ({len(todo)} queued)", flush=True)
        still = []
        for label, p in live:
            if p.poll() is None:
                still.append((label, p))
                continue
            out = p.stdout.read()
            if p.returncode != 0:
                fail.append(label)
                print(f"[{tag}] FAIL {label}\n{out[-2000:]}", flush=True)
            else:
                done = n_all - len(todo) - len(still)
                print(f"[{tag}] done {label} "
                      f"({done}/{n_all}, {(time.time()-t0)/60:.1f} min)",
                      flush=True)
        live = still
        time.sleep(3)
    if fail:
        raise SystemExit(f"[{tag}] {len(fail)} jobs failed: {fail}")


def cmd_all(a):
    R5 = _r5()
    only = set(a.only.split(",")) if a.only else None
    pairs = [p for p in PAIRS
             if only is None or p[2] in only or p[0] in only]
    if a.only and not pairs:
        raise SystemExit(f"--only {a.only!r} matched no (world, menu) pair")
    stages = a.stages.split(",") if a.stages != "all" else \
        ["pass", "members", "assemble"]
    cd = ["--cache-dir", a.cache_dir] if a.cache_dir else []
    # stage 1: base passes (heavy RAM: frame cache per proc -> 3 at a time)
    jobs = []
    for world, seed, menu in pairs:
        if "pass" not in stages:
            continue
        if os.path.exists(R5._anchors_path(world, seed, a.cache_dir)):
            continue
        jobs.append((f"pass:{world}:s{seed}", [
            PY, ME, "pass", "--world", world, "--seed", str(seed),
            "--menu", menu] + cd))
    _run_queue(jobs, 3, "pass", cap_threads=False)
    # stage 2: member chunks
    jobs = []
    for world, seed, menu in pairs:
        if "members" not in stages:
            continue
        if os.path.exists(R5.truth_path(world, seed, a.cache_dir)):
            continue
        for cid, m0, m1 in R5.member_jobs(menu):
            if os.path.exists(R5._partial_path(world, seed, cid, m0, m1,
                                               a.cache_dir)):
                continue
            jobs.append((f"{world}:s{seed}:{cid}:m{m0}-{m1}", [
                PY, ME, "member", "--world", world, "--seed", str(seed),
                "--menu", menu, "--cid", cid, "--m0", str(m0),
                "--m1", str(m1)] + cd))
    _run_queue(jobs, a.jobs, "member")
    if "assemble" not in stages:
        print("[all] MEMBERS COMPLETE (assemble skipped)", flush=True)
        return 0
    # stage 3: assemble + manifest print
    for world, seed, menu in pairs:
        R5.assemble_truth(world, seed, menu, cache_dir=a.cache_dir)
        import numpy as np
        man = json.loads(str(np.load(
            R5.truth_path(world, seed, a.cache_dir))["manifest"]))
        h = __import__("hashlib").sha256(
            json.dumps(man["hashes"], sort_keys=True).encode()).hexdigest()
        print(f"[all] {world} s{seed} truth frozen; combined {h[:16]}",
              flush=True)
    print("[all] BUILD COMPLETE", flush=True)
    return 0


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)
    for name in ("pass", "member", "assemble"):
        s = sub.add_parser(name)
        s.add_argument("--world", required=True)
        s.add_argument("--seed", type=int, required=True)
        s.add_argument("--menu", required=True)
        s.add_argument("--cache-dir", default=None)
        if name == "member":
            s.add_argument("--cid", required=True)
            s.add_argument("--m0", type=int, required=True)
            s.add_argument("--m1", type=int, required=True)
    s = sub.add_parser("all")
    s.add_argument("--jobs", type=int, default=8)
    s.add_argument("--cache-dir", default=None)
    s.add_argument("--only", default="", help="menu tags and/or worlds")
    s.add_argument("--stages", default="all",
                   help="comma set of pass,members,assemble")
    a = ap.parse_args()
    sys.exit({"pass": cmd_pass, "member": cmd_member,
              "assemble": cmd_assemble, "all": cmd_all}[a.cmd](a))
