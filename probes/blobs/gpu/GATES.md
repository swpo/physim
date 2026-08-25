# GATES.md — blobgpu correctness gates (LOCKED before the pod battery)
2026-02-25. These gates were written and frozen BEFORE the headline benchmark
runs. Any change to this file after the parity battery = a new validation round.

The program is paranoid about numerics for a reason: the A5-dt trap
(membrane/SUMMARY.md). The A5 pair under IMEX at dt=0.02 slides through its
true bond minimum d*=15.7, hits the 14.4 replication saddle and replicates
(~2600tu) — a pure integrator artifact, reproduced independently in two CPU
engines. dt<=0.005 freezes d*=15.71. Statics can be silently altered by
integrator details; "it looks fine" is not a gate. Hence:

## Gate F64 — trajectory parity (deterministic)
For each of the 7 ground-truth worlds (frozen in data/gt_worlds.json, verified
== live builders): CPU kernel (soup_sim_v2, f64, noise=0) vs GPU kernel
(blobgpu, f64, noise=0), bit-identical seeded ICs (same init_soup), L=128,
T=100tu (5000 steps).
  PASS: relative L2 field error < 1e-5 per world, single AND batched-7 modes.
  Status 2026-02-25 local (CPU-JAX): PASS, worst 1.7e-13. Pod run must repeat.

## Gate PAD — padding inertness
Padding a world into a larger (na_max, nc_max) batch layout must not change
its dynamics: padded field slots stay exactly 0 (all backends); trajectory
equality vs the solo run is BITWISE on CPU backends. On GPU, cuFFT selects
different kernel decompositions for different batch shapes, so cross-shape
runs differ in the last bits (measured ~3e-6 relL2 after 200 f32 steps at
64^2 — pure fp reassociation); the GPU gate is relL2 <= 1e-5 at short T plus
Gate DET (same-shape bitwise determinism, tests/test_determinism.py).
  PASS: tests/test_padding.py. Status: PASS local (bitwise), PASS pod (tol).

## Gate DET — same-shape determinism (exact, all backends)
Identical batch, seeds, backend, run twice -> bitwise identical after 500
noisy steps. PASS: tests/test_determinism.py.

## Gate CHUNK — chunked continuation (exact, all backends)
advance(25) x4 == advance(100) bitwise (fields + records), with noise on
(absolute-step key folds; batch shape constant across chunks, so this IS
bitwise on GPU too). PASS: tests/test_chunking.py. Status: PASS local.

## Gate ANCHOR — bond statics (the A5-dt regression test)
Pair of certified stamps at d0=16, L=64, noise=0, GPU f32 (production dtype):
  A1. A4s (tau=2.5, Dv=1.6, stamp_A4) dt=0.02, T=2000:
      status ok (2 blobs throughout), d* in [15.40 +- 0.5%] = [15.323, 15.477].
  A2. A5 (tau=2.5, Dv=2.0, stamp_P7s) dt=0.005, T=3000:
      status ok, d* in [15.70 +- 0.5%] = [15.622, 15.779].
  A3. A5 dt=0.02: must REPRODUCE the artifact — pair slides through 15.7 and
      replicates (status=replicated) in T<=4000. A GPU port that "fixes" the
      trap has different numerics and FAILS this gate.

## Gate PARITY — descriptor parity on the locked assay (statistical)
GPU soup runs (f32 + working noise 2e-3, T=5000, L=128, seeds 1-3, protocol
verbatim via soup_sim_v2.init_soup + GPU stepping) scored LOCALLY with the
LOCKED metrics_v1 (untouched, hash-checked). Reference: v1_scores_all.json
(CPU f32, T=5000, seeds 1-3).
Noise realizations differ by construction (threefry vs PCG64), so the gate is
band-based, declared here:
  Per-world CPU band B_w = [min_s I_cpu, max_s I_cpu], width W_w; expanded band
  B+_w = [min - max(0.25*W_w, 1.0), max + max(0.25*W_w, 1.0)].
  P1: per-world GPU 3-seed MEAN in B+_w for all 7 worlds.
  P2: >= 2 of 3 individual GPU seeds in B+_w for every world.
  P3: rank order of world means preserved where CPU bands do not overlap
      (m0 < coex < m4 < {xv} < {bf, pred} < mv3).
  P4: no systematic drift: |mean_w(mean_s I_gpu - mean_s I_cpu)| <= 2.0
      interest points (within-world seed scatter is 2-5 points).
  PASS requires P1-P4 all true. Any FAIL = investigate, no re-rolling seeds.

## Numerics pins (why these are part of the contract)
* einsum precision = HIGHEST: A100 would otherwise use TF32 tensor cores for
  f32 contractions (~1e-3 relative error per op) — a silent integrator change.
* exp(-D k^2 dt) computed in f64 then cast (CPU convention).
* Reaction with OLD u; noise BEFORE diffusion; same op order as soup_sim_v2.
* f32 is the production dtype (matches the locked CPU assay, gate PAR-F32).
