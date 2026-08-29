"""proto_asyncapply.py — PROTOTYPE of 0.4 H-A: ASYNC APPLY in the rung loop.

Post-procrec Amdahl (H100, workload 697bcb716916): extract went to a spawn
pool (1.10x, 42.3 -> 46.5 w/h) but every record point still BARRIERS the
driver loop: _FlushPool.map waits for all B extract futures + applies them
before the loop may pull the next chunk. Instrumented post-procrec row:
other=575 s (per-point flush waits + rung sync) vs dispatch 375 s, battery
379 s, pull 59 s — the barrier, not the extraction, is now the wall.

THIS prototype moves the barrier from per-record-point to RUNG boundaries:

  submit   record_fn submits the extract future and returns immediately
           (recorded_at set at submit = stock control flow for needs_record);
  drain    ONE apply thread consumes futures FIFO (global submission order
           = per-lane order) and replays the stock stateful tail
           (recbench.apply_record: appends, dead_since/status rules, snap
           pops, _t_stopped on exits). Lanes whose status flipped while
           their extract was in flight are SKIPPED — exactly what the stock
           driver's record_one does — so record streams match stock even
           across mid-rung blowups (test_blowup gates this edge).
  barrier  ONLY (1) when the record point t == steps_target (the rung's
           final record: criteria need the full stream) and (2) after
           run_chunks returns (safety: epilogue fixup for late exits).
  backpressure  at most MAX_POINTS record points may be in flight
           (bounds payload memory: K x B x ~1.6 MB; K=4, B=32 -> ~200 MB).

Ladder DECISIONS are unchanged by construction: the rung-final barrier
completes every apply before assay_batch snapshots records for
horizon_criteria — same inputs, same order, same bits (gate_batch).

Known non-science divergences (documented): (i) S["snap_t"]/status reads by
full_pull_needed/needs_record can be STALE by up to the queue depth ->
occasional extra full pulls / wasted extracts on already-exited lanes
(extract short-circuits on non-finite fields, so no crashes); (ii)
run_chunks' return list is recomputed post-barrier (stock computes it
inline). Record STREAMS, statuses, t_step, snaps are bitwise stock.

Usage (bench-only; subsumes proto_procrec — do not install both):
    import proto_asyncapply as AA
    AA.install(procs=8, max_points=4)
    ... run_assay_batch(...) ...
    AA.uninstall()
"""
import atexit
import collections
import multiprocessing as mp
import os
import threading
import time
from concurrent.futures import ProcessPoolExecutor

import numpy as np

import recbench as RB
from blobkit.soup import driver as DRV

MAX_POINTS = 4

_STATE = dict(pool=None, orig=None, procs=None, max_points=MAX_POINTS,
              stats=dict(records=0, points=0, submit_s=0.0, apply_s=0.0,
                         backpressure_s=0.0, barrier_s=0.0, skipped=0,
                         max_queue=0))


def _ensure_pool(procs):
    if _STATE["pool"] is None or _STATE["procs"] != procs:
        if _STATE["pool"] is not None:
            _STATE["pool"].shutdown(wait=False, cancel_futures=True)
        _STATE["pool"] = ProcessPoolExecutor(
            max_workers=procs, mp_context=mp.get_context("spawn"))
        _STATE["procs"] = procs
        _STATE["pool"].submit(os.getpid).result()      # warm spawn
    return _STATE["pool"]


class AsyncRecorder:
    """FIFO async apply machine. submit() from the driver thread; ONE
    daemon drain thread applies in submission order; barrier() blocks
    until the queue is empty and re-raises any apply/extract exception."""

    def __init__(self, pool, stats, max_points=MAX_POINTS):
        self.pool = pool
        self.stats = stats
        self.max_points = max_points
        self.q = collections.deque()          # (S, fut, t) | None poison
        self.points = collections.OrderedDict()   # t -> n pending applies
        self.cv = threading.Condition()
        self.exc = None
        self._idle = True
        self.thread = threading.Thread(target=self._drain, daemon=True)
        self.thread.start()

    # ------------------------------------------------- driver-thread side
    def submit(self, S, Fh, t):
        """The async record_fn body (contract of sim_gpu._record_host)."""
        t0 = time.perf_counter()
        na = S["na"]
        S["F"] = Fh                                    # stock contract
        chans_mem = ({c: Fh[na + c] for c in S["memch"]}
                     if t % S["crec"] == 0 else {})
        tt = t * S["dt"]
        # stale-safe snap check: drain thread pops snap_t concurrently.
        # Sorted snap times + FIFO applies make a stale head CONSERVATIVE
        # (extra f64 copy at worst, never a missed snap; see docstring).
        st = S["snap_t"]
        try:
            snap_due = bool(st) and tt >= st[0] - 1e-9
        except IndexError:
            snap_due = False
        fut = self.pool.submit(RB._extract_star,
                               (RB.ctx_of(S), Fh[:na], chans_mem, t,
                                snap_due))
        with self.cv:
            self.q.append((S, fut, t))
            self.points[t] = self.points.get(t, 0) + 1
            self.stats["max_queue"] = max(self.stats["max_queue"],
                                          len(self.q))
            self._idle = False
            self.cv.notify_all()
        S["recorded_at"] = t                           # stock control flow
        self.stats["records"] += 1
        self.stats["submit_s"] += time.perf_counter() - t0

    def point_done(self, t, steps_target):
        """End of one record point: rung-final barrier, else backpressure."""
        self.stats["points"] += 1
        if t >= steps_target:
            self.barrier()
            return
        t0 = time.perf_counter()
        with self.cv:
            while len(self.points) > self.max_points and self.exc is None:
                self.cv.wait(0.5)
        self.stats["backpressure_s"] += time.perf_counter() - t0
        self._raise_if_failed()

    def barrier(self):
        t0 = time.perf_counter()
        with self.cv:
            while (self.q or not self._idle) and self.exc is None:
                self.cv.wait(0.5)
        self.stats["barrier_s"] += time.perf_counter() - t0
        self._raise_if_failed()

    def close(self):
        with self.cv:
            self.q.append(None)
            self.cv.notify_all()
        self.thread.join(timeout=60)

    def _raise_if_failed(self):
        if self.exc is not None:
            exc, self.exc = self.exc, None
            raise exc

    # --------------------------------------------------- drain-thread side
    def _drain(self):
        while True:
            with self.cv:
                while not self.q:
                    self._idle = True
                    self.cv.notify_all()
                    self.cv.wait()
                item = self.q.popleft()
                self._idle = False
            if item is None:
                with self.cv:
                    self._idle = True
                    self.cv.notify_all()
                return
            S, fut, t = item
            t0 = time.perf_counter()
            try:
                d = fut.result()
                # stale-ok skip: stock record_one gates on status at record
                # time; a lane that exited while this extract was in flight
                # must not be applied (its stock stream ended at the exit).
                if S["status"] == "ok":
                    ok = RB.apply_record(S, d, t)
                    if not ok:
                        S["_t_stopped"] = t            # _record_host contract
                else:
                    self.stats["skipped"] += 1
            except BaseException as e:                 # propagate at barrier
                self.exc = e
            self.stats["apply_s"] += time.perf_counter() - t0
            with self.cv:
                n = self.points.get(t, 0) - 1
                if n <= 0:
                    self.points.pop(t, None)
                else:
                    self.points[t] = n
                if not self.q:
                    self._idle = True
                self.cv.notify_all()


class _AsyncPointPool:
    """rec_pool shim: map() drives the stock skip logic (record_one), which
    calls our submitting record_fn; then hands the point boundary to the
    recorder (rung-final barrier / backpressure) and returns. ALWAYS passed
    to the driver (replacing its ThreadPoolExecutor), so the point hook
    fires for every batch size."""

    def __init__(self, recorder, steps_target):
        self.rec = recorder
        self.steps_target = steps_target

    def map(self, fn, argss):
        argss = list(argss)
        for a in argss:
            fn(a)                        # stock record_one -> submit
        if argss:
            self.rec.point_done(argss[0][2], self.steps_target)
        return []


def install(procs=None, max_points=None):
    """Wrap DRV.run_chunks: async-apply record path. Idempotent."""
    if _STATE["orig"] is not None:
        return
    procs = procs or min(8, os.cpu_count() or 1)
    max_points = max_points or _STATE["max_points"]
    pool = _ensure_pool(procs)
    orig = DRV.run_chunks
    _STATE["orig"] = orig

    def run_chunks(worlds, steps_target, *, step_fn, pull_fn, record_fn,
                   rec_pool=None, **kw):
        recorder = AsyncRecorder(pool, _STATE["stats"],
                                 max_points=max_points)
        shim = _AsyncPointPool(recorder, steps_target)

        def async_record_fn(S, Fh, t):
            recorder.submit(S, Fh, t)

        try:
            orig(worlds, steps_target, step_fn=step_fn, pull_fn=pull_fn,
                 record_fn=async_record_fn, rec_pool=shim, **kw)
            # safety barrier: a rung can end without a final record point
            # (e.g. every lane exited mid-rung); epilogue then ran with
            # applies pending -> fix late exits before anyone reads state.
            recorder.barrier()
        finally:
            recorder.close()
        for S in worlds:
            if "_t_stopped" in S:
                S["t_step"] = S.pop("_t_stopped")
        return [S["status"] for S in worlds]

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


# ------------------------------------------------------------------ gates
def gate_batch(n=4, L=64.0, T=500.0, verbose=True):
    """Bitwise identity vs stock on a gpu-backend batch (same harness as
    proto_procrec.gate_batch): record streams, statuses, snaps, t_step."""
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


def test_blowup(verbose=True):
    """Staleness edge gate: a lane blows mid-queue while later extracts for
    it are already in flight (submitted under stale status=='ok'). Async
    applies must (i) append nothing at/after the blowup point, (ii) set
    status='blowup' and t_step at the DETECTION point, (iii) skip the
    stale later applies — exactly stock record_one semantics."""
    import copy
    from blobkit import worlds as W
    from blobkit.soup import sim_cpu as SC

    g = W.load("m0")
    S0 = SC.init_soup(g, L=64.0, seed=1, workers=1)
    SC.advance(S0, 250.0)
    S0["snap_t"] = []
    rec_i = S0["rec"]
    t_base = ((S0["t_step"] // S0["crec"]) + 1) * S0["crec"]
    pts = [t_base + k * rec_i for k in range(5)]
    F_good = np.asarray(S0["F"]).copy()
    F_bad = F_good.copy()
    F_bad[0] = np.nan

    # stock reference: record_one semantics over the same (point, field) seq
    A = copy.deepcopy(S0)
    for k, t in enumerate(pts):
        if A["status"] != "ok" or A["recorded_at"] >= t:
            continue
        A["F"] = F_good if k < 2 else F_bad
        ok = SC._record(A, t)
        A["recorded_at"] = t
        if not ok:
            A["_t_stopped"] = t
    if "_t_stopped" in A:
        A["t_step"] = A.pop("_t_stopped")

    # async: ALL five extracts submitted before any apply lands (max_points
    # high = worst-case staleness), then barrier.
    B = copy.deepcopy(S0)
    pool = _ensure_pool(2)
    recorder = AsyncRecorder(pool, dict(_STATE["stats"]), max_points=99)
    try:
        for k, t in enumerate(pts):
            if B["status"] != "ok" or B["recorded_at"] >= t:
                continue                       # (never fires: stale-ok)
            recorder.submit(B, F_good if k < 2 else F_bad, t)
        recorder.barrier()
    finally:
        recorder.close()
    if "_t_stopped" in B:
        B["t_step"] = B.pop("_t_stopped")

    same = (A["ts"] == B["ts"] and A["mass"] == B["mass"]
            and A["blobs"] == B["blobs"] and A["cts"] == B["cts"]
            and A["status"] == B["status"] == "blowup"
            and A["t_step"] == B["t_step"] == pts[2]
            and A["dead_since"] == B["dead_since"])
    if verbose:
        print(f"[test_blowup] {'PASS' if same else 'FAIL'} "
              f"(status {B['status']}, t_stop {B['t_step']} == {pts[2]}, "
              f"{len(B['ts'])} records kept)", flush=True)
    return same
