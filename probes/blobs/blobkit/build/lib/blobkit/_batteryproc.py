"""blobkit._batteryproc — the battery pool worker, in a deliberately tiny
module (blobkit 0.3.1; timeout containment 0.3.4).

run_assay_batch's ProcessPoolExecutor uses the SPAWN context (forking after
JAX/CUDA init is undefined and killed workers on GPU hosts — the 0.3.0 fleet
bug). A spawned worker imports the module that defines its function: keeping
the function HERE (instead of in assay_batch) means workers import only
blobkit.__init__ + this module + (inside the call) metrics_v2/assay_v2 —
i.e. the numpy/scipy metrics chain. Never jax, never sim_gpu, never the
executor machinery.

[0.3.4] PER-LANE BATTERY TIMEOUT. Prod wedge (isl6, 2026-08-29): a battery
worker sat ACTIVE 4h+ inside metrics_v1.build_tracks — greedy track
matching is O(frames x blobs^2) pure-Python and a dense long-T world made
it effectively unbounded. Containment (this module, worker-side so no pool
slot leaks and no future-timeout machinery):

  1. every battery call is guarded by a SIGALRM wall-clock timeout
     (BLOBKIT_BATTERY_TIMEOUT seconds, default 300; 0 disables; the greedy
     loop is Python-bytecode-level, so the alarm preempts it promptly);
  2. on timeout the battery is retried ONCE with TRACK SUBSAMPLING:
     build_tracks sees every BLOBKIT_BATTERY_SUBSAMPLE-th record frame
     (default 4) with track frame indices remapped to the original grid
     (time axes stay correct; matching is 4x coarser -> ~16x cheaper).
     Tracks feed the motion/graph metrics only; all other metrics see the
     full record. The lane's battery dict (and results row) carries
     {"battery_mode": "subsampled"} — these worlds' motion metrics are
     coarser, and rows say so;
  3. if the retry ALSO times out, the lane returns a battery_timeout
     assay_error (contained per lane; the batch continues).

The guard only arms in a MAIN thread on platforms with SIGALRM (fleet =
Linux; spawned pool workers run tasks in their main thread). Elsewhere it
degrades to the unguarded 0.3.2 behavior.
"""
import os
import signal
import threading


class BatteryTimeout(Exception):
    """Battery wall-clock timeout (see module docstring)."""


def _timeout_s():
    try:
        return float(os.environ.get("BLOBKIT_BATTERY_TIMEOUT", "300") or 0)
    except ValueError:
        return 300.0


def _stride():
    try:
        return max(int(os.environ.get("BLOBKIT_BATTERY_SUBSAMPLE", "4")), 2)
    except ValueError:
        return 4


def _with_timeout(fn, seconds):
    """Run fn() under a SIGALRM wall-clock guard. No-op guard when
    seconds<=0, off the main thread, or without SIGALRM (Windows)."""
    if (seconds <= 0 or not hasattr(signal, "SIGALRM")
            or threading.current_thread() is not threading.main_thread()):
        return fn()

    def _handler(signum, frame):
        raise BatteryTimeout()

    old = signal.signal(signal.SIGALRM, _handler)
    signal.setitimer(signal.ITIMER_REAL, float(seconds))
    try:
        return fn()
    finally:
        signal.setitimer(signal.ITIMER_REAL, 0.0)
        signal.signal(signal.SIGALRM, old)


def _build_tracks_strided(MV1, rec, stride):
    """build_tracks on every stride-th record frame (LAST frame always
    included: survivor filters test ks[-1] against nT-1-GAP_TOL), track
    frame indices remapped to the ORIGINAL grid so downstream consumers
    (track_speeds' dt from ks*REC, window masks, end-of-record filters)
    keep the real time axis. Motion classes survive 4x coarser matching
    (metrics_v1 tolerance); rows are flagged battery_mode=subsampled."""
    import numpy as np
    nT = len(rec["t"])
    idx = list(range(0, nT, stride))
    if idx and idx[-1] != nT - 1:
        idx.append(nT - 1)
    sub = dict(rec)
    sub["t"] = np.asarray(rec["t"])[idx]
    sub["blobs"] = {i: [rec["blobs"][i][k] for k in idx]
                    for i in range(rec["na"])}
    tracks = MV1.build_tracks(sub)
    for tr in tracks:
        tr["ks"] = [idx[k] for k in tr["ks"]]
    return tracks


def _subsampled_battery(rec, genome, stride):
    """full_battery with build_tracks swapped for the strided variant.
    The swap is scoped (try/finally) and process-local (pool workers are
    separate processes; inline callers restore before returning)."""
    from . import metrics_v1 as MV1
    from . import metrics_v2 as MV2
    orig = MV2.build_tracks
    MV2.build_tracks = lambda r: _build_tracks_strided(MV1, r, stride)
    try:
        return MV2.full_battery(rec, genome=genome)
    finally:
        MV2.build_tracks = orig


def guarded_battery(rec, genome):
    """LOCKED battery with the 0.3.4 timeout->subsample->error ladder.
    Returns (out|None, err|None); out carries battery_mode="subsampled"
    iff the retry path scored the lane."""
    from . import metrics_v2 as MV2
    timeout = _timeout_s()
    try:
        return _with_timeout(
            lambda: MV2.full_battery(dict(rec), genome=genome), timeout),             None
    except BatteryTimeout:
        pass
    stride = _stride()
    try:
        out = _with_timeout(
            lambda: _subsampled_battery(dict(rec), genome, stride), timeout)
        out["battery_mode"] = "subsampled"
        return out, None
    except BatteryTimeout:
        return None, (f"battery_timeout({timeout:.0f}s; subsample x"
                      f"{stride} retry also timed out)")
    except Exception as e:                        # retry-path crash
        return None, repr(e)[:300]


def battery_worker(args):
    """LOCKED battery + LOCKED criteria for one lane (CPU, pool-safe).
    Exceptions are captured per lane (a no_blobs-style battery crash on one
    lane must not abort the other B-1 lanes; the singles path lets it
    propagate to the caller — pod_lib.evaluate catches it there).
    [0.3.4] battery runs under guarded_battery (timeout -> subsampled
    retry -> contained error; module docstring)."""
    from .assay_v2 import horizon_criteria
    rec, genome = args
    try:
        out, err = guarded_battery(rec, genome)
        if err is not None:
            return None, None, err
        crit = horizon_criteria(rec, genome, D=out["D"])
        return out, crit, None
    except Exception as e:                        # contained, reported per lane
        return None, None, repr(e)[:300]
