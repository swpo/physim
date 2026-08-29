# HYPOTHESES.md — blobkit throughput ledger (perf thread)

Rule: NO perf claim without a bench row (perf/bench.py; rows in
perf/results/rows.jsonl). This file ranks the open hypotheses; each entry
names the mechanism, the expected gain, the benchmark tier that would prove
it, and the cost to try. Update status lines with row references only.

## Measured baseline (evidence anchors)

- H100 f32 full assay, 32-lane union4-strata mix (nf 3-14; T mix
  20x2500 / 6x5000 / 4x10000 / 2x20000):
  0.3.1 single-tensor 100 w/h; 0.3.2 nf-bucketed (4 calls) 86.5 w/h;
  sequential singles 91 w/h. GPU util 60-99% -> NOT flop-bound at B=32.
- Post reference 396 w/h was B=96, nf-homogeneous, tracking-only (no
  battery, no ladder): ceiling-ish, not comparable.
- Battery measured 0.25 s/world (pool amortized). Sim-only estimate ~550 s
  of the 1152 s batch wall -> ~half the wall is host round-trips (full-state
  pull + _record every rec point), per-rung sync, compile, repack.
- Harvest joint distribution (n=2079 assayed worlds, deepsearch evo2):
  T share 2500:69.0% / 5000:12.9% / 10000:12.2% / 20000:5.9%;
  nf-bucket share b4:15.4 / b7:17.2 / b10:14.9 / b14:52.5%.
- Confirm-lane T is KNOWN a priori: t0 floor = screen's T_used stamp.
  In the harvest, 82.0% of 783 confirms stopped exactly at the stamp,
  18.0% extended past it, 0% below (they cannot go below by construction).
  Screens are predictable only via the base rate: P(T=2500|screen) =
  99.6% (b4) / 88.9% (b7) / 79.9% (b10) / 58.2% (b14).
- Local CPU-JAX T1 (this suite, N=256): us/world-step b4 ~1290, b7 ~2790,
  b10 ~4110, b14 ~5170 -> cost is ~linear in nf_max; B=1 vs B=4 vs B=8 flat
  on CPU (no batch amortization; expect the opposite on H100).
- Local T2 rows (0.3.2 reference, laptop CPU-JAX): t2mini 34.3 w/h
  (workload 69dadaa2ea68, 629 s, ladder exercised, 0 errors); instrumented
  t2smoke: dispatch 99.3 s of 102.3 s wall (97%), pull 0.07 s, record
  1.95 s (502 record points, ~3.9 ms each), battery 0.48 s. On CPU the
  KERNEL is the wall — H-A/H-C are GPU-host phenomena and can only be
  proven/disproven by GPU rows; local rows validate the harness and price
  the host-side record/battery components.

## Ranked ledger

### H-C  Fewer/cheaper host syncs on the record path        [rank 1]
(2026-08-29 REVISION: "host syncs" was the wrong noun — the H100
instrumented row shows the PULL is cheap (40 s) and the host-side RECORD
TRACKING is the wall, serialized by the GIL. Mechanism text below kept
for the C1/C2 designs; see Status + GAINS.md for the measured story.)
Mechanism: today every REC point (5 tu = 250 steps) pulls the FULL padded
f32 state (B, nf_max, N, N) to host (activator-only pull exists but
full_pull_needed fires every CREC=25tu and at snapshots) and runs the locked
CPU `_record` per lane. At B=32/nf14/N256 a full pull is ~200 MB per CREC;
the device idles while the host converts + tracks unless overlap hides it.
Two sub-moves, in cost order:
  C1 batched pulls: accumulate K record points ON DEVICE (ring buffer of
     activator fields, (K, B, na_max, N, N) slices), pull every K-th point
     in one transfer, then run the K host records back-to-back. Fewer,
     larger PCIe transfers + fewer dispatch stalls; record code untouched.
  C2 device-side reductions (0.4 roadmap / mjlab T1 lesson): compute the
     REC-grid scalars (per-act blob count via threshold+label is the hard
     one; mass/cover/coarse memf are trivial reductions) on device; pull
     scalars every REC, fields only at CREC/snapshots. Blob LISTS (y,x,
     area,peak per blob) are required by the locked metrics — so either
     (a) keep full pulls at CREC only and accept REC-grid lists from a
     device labeling kernel, or (b) restrict C2 to the scalar streams and
     shrink, not remove, the REC pulls. Science gate: records must stay
     bit-identical (V1-style) or the change is a new metrics version.
Expected gain: the 1152s wall carries ~600s of non-sim host time; C1
alone should cut the pull+stall share materially (order 1.2-1.5x on T2);
C2 approaches the tracking-only regime (396 w/h was measured WITHOUT the
record-per-rec-point burden — treat 1.5-2.5x on T2-gpu as plausible).
Proof: T2 (t2/t2-gpu) w/h before/after; T1 pullcadence microbench bounds
the per-pull cost (already in the suite: pull_full_ms vs pull_acts_ms).
Cost to try: C1 medium (driver + sim_gpu pull_fn seam, no locked-file
edits — record_fn contract already allows it); C2 high (device labeling
kernel + parity gates).
Status: DIAGNOSED + prototype gated (2026-08-29). H100 instrumented t2
(workload 697bcb716916): record 2299 s cum vs 1505 s wall at 8 REC
threads = x1.5 effective -> record tracking IS the wall (60%+), NOT the
PCIe pull (40 s). t2record microbench: thread pool saturates x2.4
(GIL-bound: blob_list_fast x1.79 @2T, periodic_label x1.18); spawn
process pool keeps scaling (x4.0 @8 procs laptop; payloads 1.6 MB /
0.1 ms pickle). FIX (a) = record extract on a spawn process pool;
prototype proto_procrec.py + `bench.py t2 --procrec`, identity gates
PASS (extract+apply == stock _record; batch record streams bitwise).
Expected on pod: x2.75-4.2 (GAINS.md table). C2 re-ranked to 0.4+
(blob lists ~90% of record cum; needs device periodic labeling).

### H-B  Fill the device: cross-gen lane pooling to B>=64-96 [rank 2]
Mechanism: the H100 is under-worked at B=32 (util 60-99%, and the 396 w/h
reference was B=96). Screens from generation k+1 do not depend on gen k's
confirms — the pod can pool lanes ACROSS generations (and across islands)
into one 64-96-lane tensor per nf bucket; the driver's reseed_hook seam
(0.2) is the insertion point for refilling exited rows mid-flight
(continuous batching) without waiting for rung boundaries.
Expected gain: kernel-level, sub-linear but real: if B=96 uniform gave
~4x tracking-only throughput vs B=32-with-battery, a full-assay B=96
should recover a large slice; bounded by H-C (host path saturates first).
Order 1.3-2x on T2-gpu once H-C1 lands; measurable TODAY via T1 cells
(b14_B32 vs b14_B64 vs b14_B96 us/world-step on GPU).
Proof: T1 gpu profile cells (already configured: B=8/32/64/96 at b14);
then a T3 variant with pooled screens (t3 pools two synthetic gens).
Cost to try: T1 evidence free (next pod window); prod pooling medium
(pod_gen_batch scheduling change, no engine edits); reseed_hook continuous
batching high (repack identity gates).
Status: OPEN. T1-gpu rows pending pod window.

### H-A  Record-path overlap across rungs                    [rank 3]
Mechanism: advance_gpu_batch already overlaps WITHIN a rung (dispatch next
chunk, then record current pull; BLOBGPU_REC_THREADS). But at every RUNG
boundary the pipeline drains: full pull -> per-lane battery (0.25 s/world
x up to 32 lanes) -> criteria -> repack -> next rung. The device idles
during battery/criteria/repack. Fix (mjlab lesson, driver seam exists):
dispatch rung k+1 SPECULATIVELY for all lanes at the boundary (survivor
prediction: assume everyone extends — 31% do overall, but the lanes that
reach rung k>0 extend at ~50%+), run batteries on host while the device
steps; kill/ignore rows whose criteria said stop (they are padding-inert
by construction). Rung k+1 work for lanes that exit is wasted device time,
but the device was idle anyway; net win when battery wall > wasted-step
wall, which is exactly the measured regime at B<=32.
Expected gain: removes up to n_rungs x (battery+repack) stalls per call:
~0.25 s/world battery + sync each rung; on the 1152 s batch wall with 4
rungs this is order 5-15% alone, more when combined with H-B (bigger B
=> bigger per-rung battery bill to hide).
Proof: T2 instrumented rows (probe.battery / probe.other vs wall) before/
after; headline = T2 w/h. T1 unaffected (control).
Cost to try: medium-high — assay_batch driver change; identity gate: rows
must be BITWISE equal to 0.3.2 (speculative steps only touch rows that
would have stepped anyway or are discarded; noise streams fold on absolute
step so discarded work does not perturb survivors).
Status: OPEN.

### H-D  T-stratified packing using KNOWN T floors           [rank 4]
Mechanism: rung-synchronized calls waste device rows as ballast when lanes
exit early: at the measured T shares, a B=32 mixed call steps ~24% pure
ballast row-tu (B_pad ladder 32->16->8->4; expected useful 4770 tu/world
vs 6250 stepped). Confirm jobs carry t0/T stamps A PRIORI (82% exact,
never below), so the scheduler can pack SAME-FLOOR confirms together:
a t0=20000 confirm batch has zero early-exit ballast by construction;
mixed screens (T unknown, but 58-99% stop at 2500 depending on bucket)
pack separately and drain via B_pad repacks as today.
Expected gain: bounded by the ballast share: <=1.31x ideal at B=32 mixed;
realistic 1.05-1.15x on T2 (repacks already reclaim most ballast; the win
is fewer repacks + denser late rungs). Cheap because it is pure scheduling.
Proof: T2 with stratified grouping vs 0.3.2 grouping (same lanes, same
hash modulo grouping flag) — one boolean in the bench config; plus
pod-side: wall per generation at equal lane sets.
Cost to try: LOW (pod_worker_batch grouping key + t2 variant config).
Status: OPEN. Note: grouping by floor REDUCES per-call B (smaller
buckets) — on CPU-JAX T1 shows no B amortization, on GPU it fights H-B;
net sign must come from a T2-gpu row, do not ship on intuition.

### H-E  Compile cache / persistent worker across gens       [rank 5]
Mechanism: make_stepper jit-compiles per (na_max, nc_max, nb_max,
has_bilin, tanh_slots, N, noise) x batch shape. The in-process _STEPPERS
cache already dedups within a worker process, but the fleet runs one
pod_worker_batch PROCESS per shard/generation -> every process re-jits
every (bucket, B_pad) shape it touches (measured here: 2-5 s per shape on
CPU; similar order on GPU). Two moves:
  E1 persistent worker: keep ONE process serving all generations
     (pod_gen_batch already loops in-process for async confirms; extend to
     the whole campaign loop). Zero-risk, structural.
  E2 JAX persistent compilation cache (jax.config
     jax_compilation_cache_dir) so cold processes warm-start; needs
     jax>=0.4.30 behavior checks on CUDA + cache-key stability across
     driver versions.
Expected gain: compile is per-shape one-off: 4 buckets x ~4 B_pad shapes
x ~3-5 s ~= 1-2 min per process launch; on a 1152 s generation that is
5-10%; larger for short generations and CI smokes (t2smoke pays ~10-20 s
compile for ~60 s of work).
Proof: T2 rep0 vs rep1 gap (bench.py --repeat 2 exposes warm-vs-cold in
one row pair) + a t2smoke row with/without jax cache dir env.
Cost to try: E1 low; E2 low (env var + verify cache hits in logs).
Status: OPEN. Local T1/T2 rows already carry compile_s per cell.

### Parked / rejected

- CUDA graphs: rejected in the blobgpu optimization log (0.3 docstring #4).
- Micro-tuning the kernel (fusion, layouts): roofline says cuFFT-bound;
  wins live in batching + host path (#5 in the assay_batch docstring).
- f16/bf16 stepping: numerics change -> new science version, out of scope
  for a perf thread (would need full re-certification).
- nf-bucket LADDER refinement (more buckets): 0.3.2 already partitions
  calls by bucket; finer buckets shrink B per call, fighting H-B. Revisit
  only with T2-gpu evidence at B>=64.

## Priority order for the next GPU window

1. DONE 2026-08-29: T1 gpu profile + T2 t2 baseline (42.3 w/h) +
   instrumented T2 -> record tracking = the wall (see H-C status).
2. NEXT: `bench.py t2 --config t2 --device gpu --procrec` on workload
   697bcb716916 -> the fix-(a) claim row (expected x2.75-4.2, GAINS.md).
3. Then re-instrument (--procrec --instrument): what binds post-fix?
   (dispatch? battery? -> re-rank H-B/H-A with data.)
4. H-D grouping flag -> T2 variant row (cheap).
5. H-A speculative-rung prototype only if post-(a) shows rung-boundary
   stalls still matter.
