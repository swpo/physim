"""blobkit.soup.driver — the shared sim-driver shell (blobkit 0.2, L2).

ONE copy of the chunk-loop logic that was previously duplicated per backend:
advance loop, record cadence (REC grid), full-pull scheduling (CREC grid +
pending snapshots), early-exit rules, chunked-continuation bookkeeping
(t_step / recorded_at / _t_stopped), wall accounting.

The driver owns NO numerics and NO measurement code. Everything physical or
observational is injected:

    step_fn(t, n)          advance the device/host state by n steps from
                           absolute step t (kernel; L1)
    pull_fn(full) -> list  per-world host fields at the current step
                           (full=False may return activator-only views)
    record_fn(S, Fh, t)    backend-provided record extraction (L1->L3 data):
                           mutate S with the record at step t given host
                           fields Fh; set S["recorded_at"]=t; on a
                           blowup/dead exit set S["status"] and
                           S["_t_stopped"]=t. 0.2 backends use the verbatim
                           host-side sim_cpu._record; the seam exists so 0.3
                           can inject a DEVICE-SIDE reduction variant
                           (record from device state, pull_fn unused/cheap)
                           without another refactor.
    reseed_hook(worlds, t) optional; called after every chunk advance.
                           No-op stub in 0.2 — the seam for continuous
                           batching (0.3: refill dead/converged slots with
                           fresh candidates mid-flight).

Used by sim_gpu.advance_gpu / advance_gpu_batch since 0.2 (G2-gated: record
streams bit-identical to the pre-refactor loops). sim_cpu.advance is LOCKED
and still carries its own (equivalent) inline loop; it adopts this driver at
the next relock window (see MANIFEST 0.2).

Known invisible-to-records unifications vs the pre-0.2 loops (documented,
gate-checked): (1) the driver skips the device pull on steps where no world
needs recording (chunk-continuation boundaries; the old batch loop pulled
redundantly); (2) wall_s excludes the caller's argument-validation prelude
(<1 ms, reported rounded to 0.1 s).
"""
import time


def noop_reseed(worlds, t):
    """0.3 continuous-batching seam: intentionally does nothing in 0.2."""


def run_chunks(worlds, steps_target, *, step_fn, pull_fn, record_fn,
               rec, crec, dt, overlap=False, stop_when_dead=False,
               rec_pool=None, progress=None, reseed_hook=None):
    """Advance `worlds` (list of v2 state dicts sharing one stepper) to
    `steps_target` absolute steps, recording on the REC grid exactly once per
    grid point (chunk-safe continuation).

    overlap:        dispatch the next device chunk BEFORE host-side recording
                    of the current pull (JAX async dispatch overlap).
    stop_when_dead: break the loop as soon as no world has status "ok"
                    (single-world contract); False = keep stepping, stop
                    recording (batch contract — padding-inert worlds).
    rec_pool:       optional executor with .map for parallel per-world
                    recording (worlds are independent dicts: thread-safe).
    progress:       optional callback progress(t_tu) every rec*100 steps.
    reseed_hook:    optional hook(worlds, t) after each chunk advance
                    (no-op in 0.2; continuous-batching seam).

    Returns [S["status"] for S in worlds].
    """
    ok_worlds = [S for S in worlds if S["status"] == "ok"]
    if not ok_worlds:
        return [S["status"] for S in worlds]
    t = ok_worlds[0]["t_step"]
    assert all(S["t_step"] == t for S in ok_worlds), "batch worlds out of sync"
    t0w = time.time()

    def full_pull_needed(t_now):
        tt = t_now * dt
        if t_now % crec == 0:
            return True
        for S in worlds:                     # pending snapshot due?
            if S["snap_t"] and tt >= S["snap_t"][0] - 1e-9:
                return True
        return False

    def needs_record(t_now):
        return any(S["status"] == "ok" and S["recorded_at"] < t_now
                   for S in worlds)

    def record_one(args):
        S, Fh, t_now = args
        if S["status"] != "ok" or S["recorded_at"] >= t_now:
            return
        record_fn(S, Fh, t_now)

    def record_all(t_now, F_list):
        if rec_pool is not None:
            list(rec_pool.map(record_one, [(S, Fh, t_now)
                                           for S, Fh in zip(worlds, F_list)]))
        else:
            for S, Fh in zip(worlds, F_list):
                record_one((S, Fh, t_now))

    while t <= steps_target:
        do_rec = needs_record(t)
        F_host = pull_fn(full_pull_needed(t)) if do_rec else None
        if t < steps_target and overlap:
            n = min(rec, steps_target - t)
            step_fn(t, n)                     # dispatch next chunk first
            if do_rec:
                record_all(t, F_host)         # host tracking overlaps device
            t += n
        else:
            if do_rec:
                record_all(t, F_host)
            if stop_when_dead and not any(S["status"] == "ok"
                                          for S in worlds):
                break
            if t == steps_target:
                break
            n = min(rec, steps_target - t)
            step_fn(t, n)
            t += n
        if reseed_hook is not None:
            reseed_hook(worlds, t)
        if progress and (t % (rec * 100) == 0):
            progress(t * dt)

    wall = time.time() - t0w
    for S in worlds:
        if "_t_stopped" in S:
            S["t_step"] = S.pop("_t_stopped")   # stopped this call
        elif S["status"] == "ok":
            S["t_step"] = min(t, steps_target)
        # else: stopped in an earlier call; keep its t_step
        S["wall_s"] += wall / len(worlds)       # amortized per-world wall
    return [S["status"] for S in worlds]
