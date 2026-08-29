"""proto_procrec.py — PROTOTYPE of 0.4 fix (a): record tracking in a
spawn-safe PROCESS pool (same pattern as batteries), driven at the
rec_pool/record_fn seam. NO locked file is edited: DRV.run_chunks is
runtime-wrapped (Probe pattern) to inject (i) a record_fn that SUBMITS the
pure extract half of the locked _record to a spawn ProcessPoolExecutor and
(ii) a rec_pool shim whose .map flushes the futures and APPLIES the deltas
on the host thread before returning (so driver bookkeeping — recorded_at,
statuses, early exits — keeps its exact stock semantics and ordering).

Split contract (recbench.extract_record / apply_record): extract = verbatim
_record math on (acts, chans_mem) payloads, jax-free + picklable (the
_batteryproc lesson: spawn workers must never import jax); apply = verbatim
stateful tail (list appends, dead_since/status rules, snap pops). Identity
vs stock _record: recbench.identity_gate() (PASS) + this module's
t2-level gate (gate_batch: statuses/T_used/records bitwise on a small
gpu-backend batch, stock vs proto).

Usage (bench-only):
    import proto_procrec as PP
    PP.install(procs=8)      # wrap; idempotent
    ... run_assay_batch(...) ...
    PP.uninstall()

Measured motivation (H100 t2 instrumented, workload 697bcb716916): record
2299 s cum vs 1505 s wall at 8 REC THREADS = x1.5 effective; local t2record
microbench: threads saturate x2.4, spawn procs x4.0 (8 procs, laptop), GIL
probe blob_list_fast x1.79 @ 2 threads -> the thread pool is GIL-bound.
"""
import atexit
import multiprocessing as mp
import os
import time
from concurrent.futures import ProcessPoolExecutor

import numpy as np

import recbench as RB
from blobkit.soup import driver as DRV

_STATE = dict(pool=None, orig=None, procs=None,
              stats=dict(records=0, submit_s=0.0, flush_s=0.0))


def _ensure_pool(procs):
    if _STATE["pool"] is None or _STATE["procs"] != procs:
        if _STATE["pool"] is not None:
            _STATE["pool"].shutdown(wait=False, cancel_futures=True)
        _STATE["pool"] = ProcessPoolExecutor(
            max_workers=procs, mp_context=mp.get_context("spawn"))
        _STATE["procs"] = procs
        # warm: spawn + imports out of the measured section
        fut = _STATE["pool"].submit(os.getpid)
        fut.result()
    return _STATE["pool"]


class _FlushPool:
    """rec_pool shim: .map(record_one, argss) drives the stock skip logic
    (record_one), which calls our record_fn (submit); then flushes futures
    and applies deltas in submission order before returning."""

    def __init__(self, pending):
        self._pending = pending

    def map(self, fn, argss):
        for a in argss:
            fn(a)                      # stock record_one -> _proc_record_fn
        t0 = time.perf_counter()
        for (S, fut, t) in self._pending:
            d = fut.result()
            ok = RB.apply_record(S, d, t)
            S["recorded_at"] = t
            if not ok:
                S["_t_stopped"] = t    # _record_host contract
        _STATE["stats"]["flush_s"] += time.perf_counter() - t0
        self._pending.clear()
        return []


def install(procs=None):
    """Wrap DRV.run_chunks so batched advances record via the process pool.
    Idempotent. procs default: min(8, cpu_count)."""
    if _STATE["orig"] is not None:
        return
    procs = procs or min(8, os.cpu_count() or 1)
    pool = _ensure_pool(procs)
    orig = DRV.run_chunks
    _STATE["orig"] = orig

    def run_chunks(worlds, steps_target, *, step_fn, pull_fn, record_fn,
                   rec_pool=None, **kw):
        pending = []

        def proc_record_fn(S, Fh, t):
            t0 = time.perf_counter()
            na = S["na"]
            S["F"] = Fh                              # _record_host contract
            chans_mem = ({c: Fh[na + c] for c in S["memch"]}
                         if t % S["crec"] == 0 else {})
            tt = t * S["dt"]
            snap_due = bool(S["snap_t"] and tt >= S["snap_t"][0] - 1e-9)
            fut = pool.submit(RB._extract_star,
                              (RB.ctx_of(S), Fh[:na], chans_mem, t,
                               snap_due))
            pending.append((S, fut, t))
            _STATE["stats"]["records"] += 1
            _STATE["stats"]["submit_s"] += time.perf_counter() - t0

        return orig(worlds, steps_target, step_fn=step_fn, pull_fn=pull_fn,
                    record_fn=proc_record_fn, rec_pool=_FlushPool(pending),
                    **kw)

    DRV.run_chunks = run_chunks


def uninstall(shutdown=True):
    if _STATE["orig"] is not None:
        DRV.run_chunks = _STATE["orig"]
        _STATE["orig"] = None
    if shutdown and _STATE["pool"] is not None:
        _STATE["pool"].shutdown(wait=False, cancel_futures=True)
        _STATE["pool"] = None


def stats():
    return dict(_STATE["stats"])


atexit.register(uninstall)


# ---------------------------------------------------------------- gate
def gate_batch(n=4, L=64.0, T=500.0, verbose=True):
    """t2-level identity: gpu-backend batch advanced with STOCK record path
    vs PROTO path — record streams, statuses, snaps must be EXACTLY equal.
    (Same device dtype, same seeds; record path must not perturb anything.)"""
    from blobkit import worlds as W
    from blobkit.soup import sim_gpu as SG

    def run(proto):
        names = (["m0", "pred"] * n)[:n]
        jobs = [(W.load(nm), 1 + i) for i, nm in enumerate(names)]
        master = SG.init_soup_gpu_batch(jobs, L=L, dtype="f32")
        if proto:
            install()
        try:
            SG.advance_gpu_batch(master, T)
        finally:
            if proto:
                uninstall(shutdown=False)
        return master["worlds"]

    A = run(False)
    B = run(True)
    ok = True
    for i, (Sa, Sb) in enumerate(zip(A, B)):
        same = (Sa["ts"] == Sb["ts"] and Sa["cts"] == Sb["cts"]
                and Sa["mass"] == Sb["mass"] and Sa["blobs"] == Sb["blobs"]
                and Sa["patches"] == Sb["patches"]
                and str(Sa["orgs"]) == str(Sb["orgs"])
                and all(np.array_equal(np.asarray(Sa["memf"][c][k]),
                                       np.asarray(Sb["memf"][c][k]))
                        for c in Sa["memf"]
                        for k in range(len(Sa["memf"][c])))
                and Sa["status"] == Sb["status"]
                and sorted(Sa["snaps"]) == sorted(Sb["snaps"])
                and all(np.array_equal(Sa["snaps"][k], Sb["snaps"][k])
                        for k in Sa["snaps"])
                and Sa["t_step"] == Sb["t_step"])
        ok &= same
        if verbose:
            print(f"[gate_batch lane{i}] {'PASS' if same else 'FAIL'} "
                  f"({len(Sa['ts'])} rec, {len(Sa['cts'])} crec, "
                  f"status {Sa['status']})", flush=True)
    return ok
