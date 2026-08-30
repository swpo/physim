## 0.3.4 — per-lane battery timeout (2026-08-29, wedge fix)

Prod wedge (isl6, 4h+): a battery pool worker sat ACTIVE+GIL inside
metrics_v1.build_tracks — greedy track matching is O(frames x blobs^2)
pure Python; a dense long-T world made it effectively unbounded (also
explains the 163-181 min g2/g3 walls as near-misses).

Containment ladder (worker-side, _batteryproc.guarded_battery):
  1. SIGALRM wall-clock guard around every battery call
     (BLOBKIT_BATTERY_TIMEOUT, default 300 s; 0 disables; arms only in a
     main thread with SIGALRM — spawn pool workers qualify);
  2. on timeout, ONE retry with TRACK SUBSAMPLING: build_tracks sees every
     BLOBKIT_BATTERY_SUBSAMPLE-th record frame (default 4; last frame
     always kept — survivor filters test ks[-1]) with ks remapped to the
     original grid (time axes exact; matching ~16x cheaper). Tracks feed
     motion/graph metrics only; everything else sees the full record.
     Battery dict + results rows carry {"battery_mode": "subsampled"}
     (honesty: those worlds' motion metrics are coarser);
  3. second timeout -> battery_timeout assay_error (lane contained,
     batch continues).

Re-locked: _batteryproc.py (guard + ladder + strided build_tracks),
assay_batch.py (finalize -> guarded_battery + row battery_mode),
data/fleet/pod_worker_batch.py (row battery_mode). Version 0.3.4,
47 files locked.

Gates (verify_v03/, installed wheel): T1 identity — m0/pred battery +
criteria EQUAL to the 0.3.3 reference (ref_033.json captured pre-upgrade;
subsample never engages below timeout); T2 ladder — synthetic dense
record (400 frames x 260 blobs) times out at 20 s and SCORES subsampled;
T3 double-timeout contained in 4 s; T4 battery_worker identity; POOL
path — SIGALRM fires inside spawn workers (dense lane subsampled, normal
lane full, wall 27 s). Logs: V1a via test_034.log, pool_test.log.

## 0.3.3 — gated record-path prototypes packaged (2026-08-29, perf integration)

The blobkit-perf thread's GATED prototypes ship in-package so the fleet
can run them via island_config (0.4 makes them driver-native):

- NEW `soup/devrec_proto.py`: device-side REC-grid records — scatter-min
  root-merge CCL (outer=5/jumps=8 + device convergence flag) + dense-rank
  f64 segment stats fused over (B*na_max) fields; routes on the driver's
  pull signal (full=False = REC-only points, no host field pull); host
  assembles blob rows (np.angle f64, verbatim blob_list_fast math) and
  applies the verbatim _record REC tail; CREC/snaps/fallback lanes
  (unconverged/overflow/non-finite) take the stock host path.
- NEW `soup/asyncapply_proto.py`: H-A async apply — record extracts on a
  spawn process pool (jax-free workers), ONE drain thread applies FIFO,
  barriers only at rung-final points; carries the verbatim extract/apply
  split of the locked sim_cpu._record.
- `data/fleet/pod_worker_batch.py` (re-locked): island_config hook —
  {"record_mode": "device"} -> devrec install (composes with
  {"apply_mode": "async"}); {"apply_mode": "async"} alone -> asyncapply.
  {"record_procs": N} sizes the spawn pool.
- `deploy_tools.py` (re-locked): gpu_batch config template defaults
  record_mode=device, apply_mode=async (set "host"/"sync" for 0.3.2
  behavior).

Evidence (perf/, all rows in perf/results/): parity gates PASS (blob sets
identical, area/peak exact, y/x/mass <= 3.8e-13 vs 1e-12 tol, ZERO
fallbacks; asyncapply BITWISE; assay-level decision identity; x64-flag
flip bit-safe for the f32 stepper). CLAIM ROW on the frozen t2 workload
697bcb716916 (H100): 42.31 -> 92.20 w/h (2.18x, --devrec --asyncapply).
0.3.3 smoke (installed wheel, CPU-JAX): asyncapply bitwise PASS; devrec
worst 1.3e-15, 78 device points, 0 fallbacks (verify_v03/V1a_033.log);
make_bundle template + pod_worker_batch hook fire correctly
(hook_smoke_033.py). Locks: 47 files (2 new).


## 0.3.2 — nf-bucket call partitioning (2026-08-28, perf fix)

Binding V2 on the H100 FAILED at 1.1x (batch 100 w/h vs seq 91 w/h,
32-lane union4-strata mix; battery measured NOT the wall at 0.25s/world).
Root cause: PADDING WASTE — pack_genomes pads every lane to the call's
nf_max; union4 worlds span nf 3-14, so a 3-field world pays 14-field FLOPs
(~2-4x waste on realistic mixes; the accelerating-blobs 396 w/h figure was
nf-HOMOGENEOUS pop-96).

Fix (driver-level; locked engine + assay untouched):
- `assay_batch.py`: new `nf_bucket(g)` helper + `NF_BUCKETS=(4,7,10,14)`
  (nf rounded UP; >14 returns own nf — rejected upstream by MAX_FIELDS).
  `run_assay_batch` itself never re-partitions a call: one call = one
  tensor (per-call identity is exactly what the V1 gates certify).
- `data/fleet/pod_worker_batch.py`: grouping key extended to
  (L, grid-class, nf_bucket) — one run_assay_batch call per bucket — and
  lanes within a bucket are ordered by DESCENDING expected T (confirm t0
  floors / lane caps), so likely-extenders stay adjacent and survivors
  repack densely on later rungs.
- `verify_v03/v2_run.py`: same bucketing + ordering (it calls
  run_assay_batch directly); V2.json gains `nf_buckets`.

Gates: unit tests (nf_bucket ladder; offline stubbed grouping: 5 mixed jobs
-> 3 calls with nf_max 3/8/11, descending-T order inside the bucket, rows
correct); V1a rerun on 0.3.2 PASS 4/4 bitwise (bucketing is call
partitioning, not an engine change); V2 path smoke end-to-end (4 lanes ->
2 bucketed calls, results merged in job order, PERF_REFERENCE emitted).
Locks: 45 files, re-locked assay_batch.py + data/fleet/pod_worker_batch.py;
version 0.3.2. Binding V2 rerun on the pod = controller.
