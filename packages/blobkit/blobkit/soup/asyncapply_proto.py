"""blobkit.soup.asyncapply_proto — H-A async record apply [PROTOTYPE-GATED].

PROTOTYPE-GATED (blobkit 0.3.3): verbatim promotion of the blobkit-perf
thread's proto_asyncapply.py (perf/ bench flag --asyncapply). 0.4 makes
this driver-native; until then the fleet enables it via island_config
{"apply_mode": "async"} (pod_worker_batch calls install() pre-shard-loop).

Gates passed (perf/results/, 2026-08-29): gate_batch bitwise vs stock
(record streams, statuses, snaps, t_step; 4 lanes T=500 gpu backend);
test_blowup staleness edge (mid-queue blowup: stock record_one semantics);
assay-level decision identity (multi-rung, interest/T_used/why/n_ext).
Claim row: part of the 92.2 w/h devrec+async run (t2 frozen workload
697bcb716916; 2.18x vs 0.3.2 stock).

Mechanism: every record point SUBMITS the pure extract half of the locked
sim_cpu._record to a spawn process pool (jax-free import chain — the
_batteryproc lesson) and returns; ONE daemon drain thread applies deltas
FIFO through the verbatim stateful tail; the rung loop barriers ONLY at
rung-final record points (criteria see the full stream) and at exit.
Known stale-reads (snap_t head, status) are conservative-by-construction;
see AsyncRecorder notes.

Usage:
    from blobkit.soup import asyncapply_proto as AA
    AA.install()            # wrap driver.run_chunks; idempotent
    ...                     # run_assay_batch / advance_gpu_batch as usual
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

from .. import genome as G
from . import driver as DRV
from . import sim_cpu as SC
from .sim_v1 import blob_list_fast, coarse

MAX_POINTS = 4


# ------------------------------------------------- extract / apply split
# Verbatim from the gated perf/recbench.py (identity_gate PASS m0+pred
# incl. snaps/dead/status): extract = pure half of the LOCKED
# sim_cpu._record (jax-free, picklable); apply = stateful tail.
def extract_record(ctx, acts, chans_mem, t, want_snap_f64=False):
    """Pure half of sim_cpu._record (verbatim math, no S mutation).
    ctx: dict(na, dx, L, thr_a, thr_lo, memch, rec, crec).
    acts: (na, N, N) activator fields (any float dtype, natural layout).
    chans_mem: {c: (N, N) field} for ctx['memch'] (only needed on CREC).
    -> delta dict; apply_record() replays it into S (stateful rules)."""
    na, dx, L = ctx["na"], ctx["dx"], ctx["L"]
    rec, crec = ctx["rec"], ctx["crec"]
    d = dict(t=t, rec=(t % rec == 0), crec=(t % crec == 0))
    if d["rec"]:
        if not np.isfinite(acts).all():
            d["blowup"] = True
            return d
        blobs, mass, ntot = [], [], 0
        for i in range(na):
            u = np.asarray(acts[i], np.float64)
            bl = blob_list_fast(u, ctx["thr_a"][i], dx, L)
            blobs.append([[b["y"], b["x"], b["area"], b["peak"]]
                          for b in bl])
            mass.append(float(np.clip(u - ctx["thr_a"][i], 0, None)
                              .sum() * dx * dx))
            ntot += len(bl)
        d["blobs"], d["mass"], d["ntot"] = blobs, mass, ntot
    if d["crec"]:
        patches, orgs = [], []
        for i in range(na):
            u = np.asarray(acts[i], np.float64)
            labm, k = G.periodic_label(u > ctx["thr_a"][i])
            sz = [float((labm == j).sum()) * dx * dx for j in range(1, k + 1)]
            patches.append(dict(n=k, sizes=sz,
                                cover=float((u > ctx["thr_a"][i]).mean())))
            orgs.append(SC.org_patches(u, ctx["thr_lo"][i], dx, L))
        d["patches"], d["orgs"] = patches, orgs
        d["memf"] = {c: coarse(np.asarray(chans_mem[c], np.float64))
                     for c in ctx["memch"]}
    if want_snap_f64:
        d["acts_f64"] = np.asarray(acts, np.float64).copy()
    return d




def apply_record(S, d, t):
    """Stateful half of sim_cpu._record (verbatim order/rules). Returns
    False on blowup/dead exit, mirroring _record's return."""
    dt = S["dt"]
    tt = t * dt
    na = S["na"]
    if d["rec"]:
        if d.get("blowup"):
            S["status"] = "blowup"
            return False
        for i in range(na):
            S["blobs"][i].append(d["blobs"][i])
            S["mass"][i].append(d["mass"][i])
        S["ts"].append(tt)
        if d["ntot"] == 0:
            if S["dead_since"] is None:
                S["dead_since"] = tt
            if tt - S["dead_since"] > 200.0 and tt > 400.0:
                S["status"] = "all_dead"
                return False
        else:
            S["dead_since"] = None
    if d["crec"]:
        S["cts"].append(tt)
        for i in range(na):
            S["patches"][i].append(d["patches"][i])
            S["orgs"][i].append(d["orgs"][i])
        for c in S["memch"]:
            S["memf"][c].append(d["memf"][c])
    while S["snap_t"] and tt >= S["snap_t"][0] - 1e-9:
        S["snaps"][S["snap_t"].pop(0)] = d["acts_f64"]
    return True




def ctx_of(S):
    return dict(na=S["na"], dx=S["dx"], L=S["L"],
                thr_a=np.asarray(S["thr_a"]), thr_lo=np.asarray(S["thr_lo"]),
                memch=list(S["memch"]), rec=S["rec"], crec=S["crec"])




def payload_of(S, t):
    """(ctx, acts, chans_mem, snap_due) for extract at step t."""
    na = S["na"]
    F = S["F"]
    chans_mem = ({c: F[na + c] for c in S["memch"]}
                 if t % S["crec"] == 0 else {})
    tt = t * S["dt"]
    snap_due = bool(S["snap_t"] and tt >= S["snap_t"][0] - 1e-9)
    return ctx_of(S), F[:na], chans_mem, snap_due


def _extract_star(args):
    return extract_record(*args)

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
        fut = self.pool.submit(_extract_star,
                               (ctx_of(S), Fh[:na], chans_mem, t,
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
                    ok = apply_record(S, d, t)
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
    from .. import worlds as W
    from . import sim_gpu as SG

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
    from .. import worlds as W
    from . import sim_cpu as _SC2

    g = W.load("m0")
    S0 = _SC2.init_soup(g, L=64.0, seed=1, workers=1)
    _SC2.advance(S0, 250.0)
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
