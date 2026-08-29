"""assay_batch.py — rung-synchronized BATCHED adaptive-horizon assay (blobkit 0.3).

"A generation is one tensor": B candidate worlds ride ONE padded (B, nf_max,
N, N) device tensor through the LOCKED assay_v2 ladder (T0=2500 -> x2 -> cap
20000, chunked continuation, never re-simulated). This is the assay layer the
GPU port was built for (docs/blobs/accelerating-blobs.html): the deployed 0.2
fleet drives the GPU one world per process (kernel-level wins only); this
module adds the population-level wins the optimization log certified:

  #1 batched population tensor, one jit -> init_soup_gpu_batch /
     advance_gpu_batch (certified G2/D4). ZERO new stepping code in this file.
  #2 activator-only pulls at record points (full state only on the CREC /
     snapshot grid) -> inherited from sim_gpu._driver_kw's pull_fn.
  #3 threaded host record + JAX async-dispatch overlap -> advance_gpu_batch
     overlap=True + BLOBGPU_REC_THREADS (defaulted to 8 here; the log
     measured 16-vs-8 a wash). Per-lane battery+criteria at rung boundaries
     run on a CPU process pool (this is where the vcpus go).
  #4 CUDA graphs: rejected in the log; not revisited.
  #5 roofline: the kernel is cuFFT-bound; wins are batching + host overlap,
     not micro-tuning.

DESIGN (rung-synchronized ladder). All lanes enter at T0 and double together,
so the ladder is globally synchronized: rungs are T = t0 * 2^k, capped
(2500, 5000, 10000, 20000 at the locked defaults). Per rung:
  1. advance ALL live lanes to T on one tensor (advance_gpu_batch);
  2. per live lane: snapshot -> LOCKED metrics_v2.full_battery + LOCKED
     assay_v2.horizon_criteria (imported, never reimplemented) on a CPU
     process pool; the decision branch is a line-for-line mirror of
     assay_v2b.run_assay_b (same order, same constants, same why strings);
  3. lanes whose criteria don't fire EXIT with their finalized results;
  4. survivors REPACK at the rung boundary: exited rows dropped, batch padded
     up to the next size in B_pad=(4, 8, 16, 32) with inert ballast rows
     (state duplicates of a survivor, recorded by nobody). Fixed shapes
     within a rung; a module-level stepper cache keys on the packed struct
     signature so rungs/calls at the same signature reuse the jit cache
     (<= len(B_pad) batch shapes per signature).

Repack continuation is EXACT: the device->host->device state roundtrip
preserves bits (same dtype), per-world threefry keys are rebuilt from the
same seeds and fold on the ABSOLUTE step index (a world's noise stream is
independent of batch shape/padding — the blobgpu contract), and padded slots
are inert BY PARAMETER CONSTRUCTION. Each lane's trajectory therefore equals
its single-world run bit-for-bit on the same backend/dtype (gated:
verify_v03/ V1 vs run_assay_b singles).

Science fidelity: every decision uses the LOCKED code paths
(assay_v2.horizon_criteria, metrics_v2.full_battery/lean_summary, constants
T0_DEFAULT/T_CAP) imported from the locked modules. Results rows are
schema-identical to assay_v2b.run_assay_b rows plus lane metadata
(lane, batched=True; backend="gpu_batch"). Known non-science divergences vs
singles rows (documented, not gated): wall_total shares the batch clock,
wall_sim is the driver's amortized per-world share, results_path defaults to
None (the pod worker passes it explicitly), and save_npz is not offered.

Usage:
    from blobkit.assay_batch import run_assay_batch
    outs = run_assay_batch([(g1, 1), (g2, 1), ...])       # f32, jax device
    outs = run_assay_batch(jobs, dtype="f64")             # parity gates
Each out is the dict run_assay_b returns (battery + horizon + summary), in
job order. Callers using the process pool (battery_procs > 0, the default)
from a script must guard __main__ (spawn context).
"""
import hashlib, os, time
import multiprocessing as mp
from concurrent.futures import ProcessPoolExecutor

import numpy as np

import blobkit
from . import _batteryproc as _BP
from . import metrics_v2 as MV2
from . import genome as G
from .assay_v2 import T0_DEFAULT, T_CAP, js, horizon_criteria
from .soup import sim_cpu as SC
from .soup import sim_gpu as SG
from .soup.sim_v1 import NOISE

B_PAD_DEFAULT = (4, 8, 16, 32)

# nf padding buckets [blobkit 0.3.2]: pack_genomes pads every lane to the
# batch's nf_max, so a mixed call makes narrow worlds pay wide-world FLOPs
# (H100 V2 audit: union4 mixes span nf 3-14 => 2-4x padding waste; the
# accelerating-blobs 396 w/h figure was nf-homogeneous pop-96). CALLERS
# partition jobs by nf_bucket() and issue one run_assay_batch per bucket;
# run_assay_batch itself NEVER re-partitions a call (per-call identity is
# exactly what the V1 gates certify).
NF_BUCKETS = (4, 7, 10, 14)


def nf_bucket(g, buckets=NF_BUCKETS):
    """Padding bucket for a genome: nf = na+nc rounded UP to the bucket
    ladder (>max(buckets) worlds return their own nf; the fleet size cap
    MAX_FIELDS=14 rejects those upstream). [blobkit 0.3.2]"""
    nf = len(g["acts"]) + len(g["chans"])
    for b in buckets:
        if nf <= b:
            return int(b)
    return int(nf)

_LOCKS12 = None


def _locks12():
    """First 12 hex of sha256(_locks.json): the lock-table fingerprint every
    batched results row carries (retrospective L1/L3b provenance)."""
    global _LOCKS12
    if _LOCKS12 is None:
        p = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                         "_locks.json")
        _LOCKS12 = hashlib.sha256(open(p, "rb").read()).hexdigest()[:12]
    return _LOCKS12

# --------------------------------------------------------- stepper cache
# make_stepper returns a fresh closure each call and jax.jit caches per
# (closure id, shapes): fresh closure = guaranteed recompile. Caching ONE
# closure per packed-struct signature turns every repack/call at the same
# signature into a jit-cache hit (at most len(B_pad) shapes each).
_STEPPERS = {}


def _stepper(struct, N, noise):
    key = (struct["na_max"], struct["nc_max"], struct["nb_max"],
           bool(struct["has_bilin"]), tuple(struct["tanh_slots"]),
           int(N), float(noise))
    st = _STEPPERS.get(key)
    if st is None:
        st = SG.make_stepper(struct, N, 0.5, 0.02, noise=noise)
        _STEPPERS[key] = st
    return st


def _pad_B(n, ladder):
    for b in sorted(ladder):
        if n <= b:
            return int(b)
    return int(n)


def _shutdown_pool(pool):
    """Teardown that cannot hang: a BROKEN executor deadlocks
    shutdown(wait=True) on its feeder queue (observed on the GPU pod —
    and a deadlock HANGS rather than raises, so it must be detected UP
    FRONT via the executor's broken flag, not caught after)."""
    if pool is None:
        return
    broken = bool(getattr(pool, "_broken", False))
    try:
        if broken:
            pool.shutdown(wait=False, cancel_futures=True)
        else:
            pool.shutdown(wait=True)
    except Exception:
        try:
            pool.shutdown(wait=False, cancel_futures=True)
        except Exception:
            pass


# --------------------------------------------------------- battery worker
# 0.3.1: the pool worker lives in blobkit._batteryproc (tiny, jax-free
# import chain) so SPAWNED workers never touch jax/sim_gpu. See its
# docstring for the GPU fork-deadlock post-mortem.
_battery_worker = _BP.battery_worker


# --------------------------------------------------------- batch plumbing
def _attach(live_S, states, seeds, pad_rows, dtype, noise):
    """(Re)pack live lanes (+ inert ballast rows) into one device tensor via
    the certified sim_gpu._attach_gpu, then swap in the cached stepper.
    pad_rows: list of (genome, host_state) ballast; never recorded."""
    gens = [S["g"] for S in live_S] + [g for g, _ in pad_rows]
    sts = list(states) + [s for _, s in pad_rows]
    sds = [S["seed"] for S in live_S] + [0] * len(pad_rows)
    assert sds[:len(seeds)] == list(seeds)
    master = dict(worlds=live_S)
    Gd = SG._attach_gpu(master, gens, sts, sds, dtype, noise)
    Gd["step"] = _stepper(Gd["struct"], Gd["N"], noise)
    for S in live_S:
        S["_gpu"] = Gd
    return master


def _repack(live, dtype, noise, B_pad):
    """Rung-boundary repack: drop exited/ballast rows, pad B to the next
    ladder size with ballast duplicates of the last survivor's state.
    Exact continuation (module docstring: bit-preserving roundtrip + seed
    keys + absolute-step noise fold + padding inertness)."""
    Gold = live[0]["S"]["_gpu"]
    F_all = SG._pull(Gold)                    # full pull, natural layout
    states = [F_all[ln["row"]] for ln in live]
    seeds = [ln["seed"] for ln in live]
    n_pad = _pad_B(len(live), B_pad) - len(live)
    pad_rows = [(live[-1]["S"]["g"], states[-1])] * n_pad
    master = _attach([ln["S"] for ln in live], states, seeds, pad_rows,
                     dtype, noise)
    for r, ln in enumerate(live):
        ln["row"] = r
    return master


def _norm_jobs(jobs, t0, cap):
    """jobs entries: (genome, seed) tuples or dicts {genome, seed, t0, cap}.
    Per-lane t0 (confirm floor) / cap (long-horizon lane) default to the
    call-level values. -> (init_jobs, t0s, caps, t0_min)."""
    init_jobs, t0s, caps = [], [], []
    for j in jobs:
        if isinstance(j, dict):
            g, s = j["genome"], j.get("seed", 1)
            t0s.append(float(j.get("t0") or t0))
            caps.append(float(j.get("cap") or cap))
        else:
            g, s = j
            t0s.append(float(t0))
            caps.append(float(cap))
        init_jobs.append((g, int(s)))
    t0_min = min(t0s)
    bad = []
    for i, (a, c) in enumerate(zip(t0s, caps)):
        for v in (a, c):
            r = v / t0_min
            k = round(np.log2(r)) if r > 0 else -1
            if not (r > 0 and abs(r - 2 ** k) < 1e-9 and k >= 0):
                bad.append((i, v))
        if c < a:
            bad.append((i, (a, c)))
    if bad:
        raise ValueError(
            f"per-lane t0/cap must sit on the shared doubling grid "
            f"t0_min*2^k (t0_min={t0_min}) with cap>=t0; offenders {bad}. "
            f"Group jobs with incompatible ladders into separate batches.")
    return init_jobs, t0s, caps, t0_min


# --------------------------------------------------------------- the ladder
def run_assay_batch(jobs, dtype="f32", L=128.0, t0=T0_DEFAULT, cap=T_CAP,
                    kicks_map=None, noise=NOISE, results_path=None,
                    verbose=True, battery_procs=None, B_pad=B_PAD_DEFAULT,
                    tag=None, save_npz_map=None):
    """Batched adaptive-horizon assay. jobs: list of (genome, seed) tuples,
    or dicts {genome, seed, t0?, cap?} for per-lane confirm floors /
    long-horizon caps (fleet t0/cap values are powers-of-2 multiples of
    2500, so the rung grid stays globally synchronized; a lane with
    t0 > current rung rides the tensor undecided until its floor — record
    streams are identical to singles by chunk-safe continuation).

    Returns a list of out dicts in job order, each identical in contract to
    assay_v2b.run_assay_b's return (metrics_v2 battery + horizon + summary).
    battery_procs: CPU pool size for per-lane batteries (0 = inline;
    default min(8, cpu_count)). results_path: append per-lane rows (schema =
    run_assay_b rows + lane/batched; default None = no file writes).
    Keep len(jobs) <= max(B_pad) per call for jit-shape stability. All lanes
    share L (one grid N per tensor): group L192 jobs into their own batch.
    PADDING EFFICIENCY [0.3.2]: also group jobs by nf_bucket(genome) before
    calling — a mixed-nf call pads everyone to the widest lane (2-4x FLOPs
    waste on realistic mixes; see NF_BUCKETS note). This function does not
    re-partition: one call = one tensor, always.
    save_npz_map: {job_index: path} — save the lane's final record npz at
    exit (the singles' save_npz, per lane)."""
    os.environ.setdefault("BLOBGPU_REC_THREADS", "8")
    t_wall0 = time.time()
    if battery_procs is None:
        battery_procs = min(8, os.cpu_count() or 1)
    init_jobs, t0s, caps, t0_min = _norm_jobs(jobs, t0, cap)

    # 1) init all lanes: certified batch init (bit-identical seeded states)
    master = SG.init_soup_gpu_batch(init_jobs, L=L, dtype=dtype, noise=noise,
                                    kicks_map=kicks_map)
    Gd = master["worlds"][0]["_gpu"]          # swap in the cached stepper
    Gd["step"] = _stepper(Gd["struct"], Gd["N"], noise)
    lanes = []
    for i, ((g, seed), S) in enumerate(zip(init_jobs, master["worlds"])):
        lanes.append(dict(idx=i, row=i, S=S, g=g, seed=seed,
                          t0=t0s[i], cap=caps[i],
                          tag=g.get("id", "anon"), n_ext=0, c_used=0,
                          traj=[], decisions=[], out=None, why=None,
                          rec_T=None, out_final=None))
    live = list(lanes)
    if _pad_B(len(live), B_pad) != len(live):
        master = _repack(live, dtype, noise, B_pad)   # t=0 roundtrip (exact)

    # SPAWN context is mandatory: fork-after-jax/CUDA-init killed workers on
    # GPU hosts and shutdown then deadlocked on the broken feeder queue
    # (0.3.0 fleet bug). Workers run _batteryproc.battery_worker (jax-free).
    pool = (ProcessPoolExecutor(max_workers=battery_procs,
                                mp_context=mp.get_context("spawn"))
            if battery_procs > 0 else None)

    def finalize(ln, why, err=None):
        """Line-for-line mirror of run_assay_b's tail for one lane. err:
        contained battery exception (singles would raise to the caller;
        batch reports it in out["assay_error"] and scores the lane 0)."""
        S, g = ln["S"], ln["g"]
        rec = SG.snapshot_rec_gpu(S)
        out, traj = ln["out"], ln["traj"]
        if err is None and (out is None or rec["T"] != traj[-1][0]):
            try:
                out = MV2.full_battery(dict(rec), genome=g)
                traj.append((rec["T"], round(out["interest"], 2)))
            except Exception as e:
                err = repr(e)[:300]
        if err is not None:
            out = dict(out or {})
            out["assay_error"] = err
            out.setdefault("interest", 0.0)
            out.setdefault("C", {})
            out.setdefault("flags", {})
        out["horizon"] = dict(T_used=rec["T"], why_stopped=why,
                              n_extensions=ln["n_ext"],
                              decisions=ln["decisions"],
                              interest_trajectory=traj,
                              wall_total=round(time.time() - t_wall0, 1))
        if err is None:
            out["summary"] = MV2.lean_summary(out)
        else:
            out["summary"] = dict(assay_error=err)
        out["summary"]["horizon"] = dict(T_used=rec["T"], why=why,
                                         next=ln["n_ext"])
        if results_path:
            row = dict(kind="assay_v2", world=g.get("id"),
                       tag=f"v2_{tag or ln['tag']}", seed=ln["seed"],
                       T=rec["T"], L=L, dtype=rec["dtype"],
                       status=rec["status"], wall_sim=rec["wall_s"],
                       wall_total=round(time.time() - t_wall0, 1),
                       metrics="metrics_v2", horizon=js(out["horizon"]),
                       battery=js(dict(C=out["C"], interest=out["interest"],
                                       flags=out["flags"])),
                       summary=js(out["summary"]))
            row["backend"] = "gpu_batch"
            row["lane"] = ln["idx"]
            row["batched"] = True
            row["blobkit"] = blobkit.__version__      # provenance (L1/L3b/L5)
            row["locks"] = _locks12()
            row["engine"] = "gpu_batch"
            G.append_result(row, path=results_path)
        if save_npz_map and ln["idx"] in save_npz_map:
            SC.save_run(rec, save_npz_map[ln["idx"]])
        ln["out_final"] = out
        ln["why"] = why

    T = float(t0_min)
    try:
        while live:
            # 2) one rung: advance ALL live lanes on one tensor
            SG.advance_gpu_batch(master, T)

            # battery + criteria per live lane (LOCKED code, CPU pool);
            # lanes below their t0 floor ride undecided (confirm lanes)
            payloads, ok_lanes = [], []
            for ln in live:
                if ln["S"]["status"] == "ok" and T >= ln["t0"] - 1e-9:
                    rec = SG.snapshot_rec_gpu(ln["S"])
                    ln["rec_T"] = rec["T"]
                    payloads.append((rec, ln["g"]))
                    ok_lanes.append(ln)
            if pool is not None and len(payloads) > 1:
                try:
                    results = list(pool.map(_battery_worker, payloads))
                except Exception:
                    # pool broke (BrokenExecutor & co): correctness first —
                    # finish THIS rung serially in-process, retire the pool
                    # (broken executors deadlock shutdown(wait=True)).
                    results = [_battery_worker(p) for p in payloads]
                    _shutdown_pool(pool)
                    pool = None
            else:
                results = [_battery_worker(p) for p in payloads]
            by_lane = {id(ln): r for ln, r in zip(ok_lanes, results)}

            # per-lane decision: line-for-line mirror of run_assay_b's loop
            survivors = []
            for ln in live:
                S = ln["S"]
                if S["status"] != "ok":
                    finalize(ln, S["status"])
                    continue
                if id(ln) not in by_lane:        # below t0 floor: ride on
                    survivors.append(ln)
                    continue
                out, crit, err = by_lane[id(ln)]
                if err is not None:              # contained battery crash
                    finalize(ln, "assay_error", err=err)
                    S["status"] = "exited"
                    continue
                ln["out"] = out
                ln["traj"].append((ln["rec_T"], round(out["interest"], 2)))
                fired = [k for k in ("a_mem", "b_org", "c_acf") if crit[k]]
                ln["decisions"].append(dict(T=T, fired=fired,
                                            detail=crit["detail"]))
                if verbose:
                    print(f"[assay_batch {ln['tag']} s{ln['seed']} "
                          f"lane{ln['idx']}] T={T:.0f} "
                          f"interest={out['interest']:.1f} fired={fired}",
                          flush=True)
                if not fired:
                    finalize(ln, "converged" if ln["n_ext"] else "static")
                    S["status"] = "exited"   # driver skips; row = ballast
                    continue
                if T >= ln["cap"]:
                    finalize(ln, "cap")
                    S["status"] = "exited"
                    continue
                # criterion (c) alone grants at most ONE doubling
                if fired == ["c_acf"]:
                    if ln["c_used"] >= 1:
                        finalize(ln, "converged")
                        S["status"] = "exited"
                        continue
                    ln["c_used"] += 1
                ln["n_ext"] += 1
                survivors.append(ln)

            # 3) rung boundary: repack survivors (drop exited rows)
            if not survivors:
                break
            cur_B = len(live[0]["S"]["_gpu"]["gens"])   # tensor width (B)
            live = survivors
            if _pad_B(len(live), B_pad) < cur_B:
                master = _repack(live, dtype, noise, B_pad)
            # else: same tensor, worlds list stays FULL length (row-parallel
            # to the tensor); exited lanes are skipped by the driver via
            # their "exited" status and keep stepping as inert ballast.
            T = min(T * 2, max(ln["cap"] for ln in live))
    finally:
        _shutdown_pool(pool)

    return [ln["out_final"] for ln in lanes]
