
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
