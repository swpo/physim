# blobkit 0.3.0 verification — batched-ladder assay driver

Date: 2026-08-28. Dev venv: `/tmp/bk02venv` (py3.11.14, numpy 2.4.6, scipy
1.17.1, jax 0.4.38 CPU). Fresh-install venv: `/tmp/bk03fresh`. Artifacts:
`verify_v03/`. Controller directives applied: local CPU-JAX walls are
expected slow — V1 gates run at reduced (legal) t0/cap; V2 local numbers are
REFERENCE ONLY, the binding throughput gate is the same script on the H100
pod (`--device H100`).

## Identity chain

`run_assay_batch` (batch, jax) is gated bitwise against
`run_assay_b(backend=gpu)` singles (same backend, same dtype). Those singles
are themselves certified against the LOCKED CPU assay by 0.2 G1/G2 + the
blobgpu GATES.md (f64 noise=0 bitwise trajectory parity; descriptor-level
with noise — GPU threefry is a different RNG stream than CPU PCG64 by
design). So: batch == jax single (bitwise, this file) == locked assay
(0.2/GATES chain).

## Gates

| gate | what | result |
|---|---|---|
| W1 | mechanical smoke: 2 m0 lanes f32 pool battery + pad-to-4 ballast; then 4-lane heterogeneous batch (see V1a) | **PASS** (W1.json, smoke4.txt; 2-lane run interest 2.80 == locked m0 ref; heterogeneous covered by V1a) |
| V1a | ONE f32 batch [m0 s7, m4 s1, mv3 s1, bf s1] t0=1250 cap=2500 B_pad=(2,4) vs 4 singles — bitwise canon (wall stripped) | **PASS 4/4 bitwise** (V1a.json; walls: batch 914s, singles 462s — local CPU-JAX, reference only) |
| V1b | f64 [m0 s7, mv3 s1] t0=2500 cap=5000 B_pad=(1,2) vs singles — f64 chain anchor | **PASS 2/2 bitwise** (V1b.json) |
| V1c | f32 [m0 s7, mv3 s1] t0=2500 cap=5000 B_pad=(2,) — non-deterministic ladder, extra evidence | **PASS 2/2 bitwise** (V1c.json) |
| V1d | f32 [m0 (t0=cap=2500), mv3 (t0=cap=5000)] B_pad=(1,2): m0 exits rung 1 DETERMINISTICALLY, repack 2->1 under a live lane riding its t0 floor, mv3 decides at 5000 | **PASS 2/2 bitwise** (V1d.json; mv3 rides t0 floor across the 2->1 repack, decides at 5000: fired=[b_org], why=cap) |
| V1e | same as V1d with B_pad=(2,): repack disabled — exited m0 row rides as inert ballast; no-cross-talk identity | **PASS 2/2 bitwise** (V1e.json; ballast path; mv3 out == V1d's bit-for-bit) |
| V2 | throughput, union4 mixed lanes, batched vs sequential singles (same backend): local CPU-JAX reference + PERF_REFERENCE.json emission; BINDING on H100 (`--device H100`, target >=2.5x, post ref 396 w/h) | **local reference recorded** (V2.json): 8 lanes, batch 5667.2s (5.1 w/h) vs sequential 3993.2s (7.2 w/h) -> ratio 0.7x local. HONEST NOTE: on CPU-JAX batching pays the padding FLOPs (nf_max x B tensor on saturated cores) with no launch-overhead pool to amortize — the mechanism the batch exploits exists only on the GPU; local ratio <1 was anticipated by the controller directive. Decision agreement 7/8; the 1 flip (p2g3_032: batch exits 2500, single extends to 10000) is a T=2500 criteria-threshold flip in the known f32 engine-noise regime (certification gates f32 decisions at the DISTRIBUTION level; V1a-e prove the ladder machinery bitwise). PERF_REFERENCE.json emitted (binding=false). **Binding gate = same script `--device H100` on the pod (controller)** |
| V3a | relock: _locks.json regenerated (44 files), verify_locks() green, no unexpected drift | **PASS** (V3a.json: 44 files, clean-import verify_locks ok) |
| V3b | fresh-venv pip install + import smoke + `run_assay_batch` entry present + locks green | **PASS** (V3b.log: fresh venv, locks green, jax lazy) |
| V3c | `make_bundle(backend="gpu_batch")` emission: pod_worker_batch/pod_gen_batch/pod_run_batch.sh present, config template extended; offline grouping + collect/g0import unit runs | **PASS** (V3c.json: emission + grouping/collect/g0import unit runs) |

## Coverage notes

- V1a covers: heterogeneous packing (1..3 acts, bilin bf, tanh channels,
  8-field mv3), pooled battery decisions, rung-1 exits, canon identity of
  the FULL out dict (battery numbers, C-scores, flags, horizon, summary).
- V1d covers: per-lane t0 confirm floors (lane rides undecided below its
  floor), rung-boundary repack with a LIVE lane (device->host->device
  roundtrip continuation), doubling after repack, cap exit at a per-lane
  cap. V1e covers the ballast (no-repack) variant of the same ladder.
- Extension identity: in f32 none of the packaged fast worlds extends by
  criteria at the locked constants (mv3 s1 f32 exits static at 2500; its
  f64 run is the extender). V1d/V1e therefore FORCE multi-rung ladders via
  t0 floors — the rung loop, continuation, and repack machinery are
  identity-gated independently of which criterion fires. Criteria-fired
  extension identity at full t0/cap on the standard grid is exercised by
  V1b (f64) and re-verified on the GPU pod (H100 rerun of v1_run.py a-e +
  long worlds mv3/ds3_014 full ladder).
- Batch rows carry provenance: blobkit version, locks fingerprint (12-hex
  sha256 of _locks.json), engine="gpu_batch" (+ lane, batched=True).

## Deferred to the GPU pod (explicit)

1. V1 full-ladder long worlds (mv3 s1, ds3_014 s9 to standard cap) on
   device; 2. BINDING V2 (32 lanes, --device H100, >=2.5x + w/h floor);
3. GPU-device rerun of the 0.2 G2 record-stream identity (was already
   deferred by 0.2).

## Local close-out note (controller directive)

Local evidence closed with: V1a-e bitwise identity (+ V1a re-verified on
0.3.1), spawn/teardown hardening tests H1-H4, V2 local reference + perf
floor emission. Binding V2 and full-ladder long-world identity run on the
H100 (controller). The V2 7/8 probe (v2_probe_lane0.py) was STOPPED on the
close-out directive — CPU-JAX decision divergences in the f32 engine-noise
regime are distribution-gated per certification and not chased locally; the
probe script stays in verify_v03/ for the pod checklist.

## 0.3.1 hotfix gates (GPU teardown hardening)

| gate | what | result |
|---|---|---|
| H1 | spawn-context pool battery == inline (real m0 record; worker module jax-free import chain asserted) | **PASS** (/tmp/bk031_spawntest.py) |
| H2 | broken-flag shutdown returns promptly (no feeder-queue join) | **PASS** (same script) |
| H3 | end-to-end sabotaged pool: BrokenProcessPool on first rung -> serial fallback -> correct results -> shutdown(wait=False, cancel_futures=True) | **PASS** (/tmp/bk031_breaktest.py) |
| H4 | V1a rerun on 0.3.1 (4-lane heterogeneous, f32) | **PASS 4/4 bitwise** (V1a.json, walls batch 1039.5s/singles 657.2s — probe ran concurrently) |
| H5 | relock 45 files + clean-import verify_locks + version 0.3.1 | **PASS** |

Device-side verification of the fix (the actual GPU teardown) = parent's
device-gate rerun.
