# DESIGN_DEVREC.md — device-side record path + pipeline (0.4 flagship)

Status: PROTOTYPED + CLAIMED (2026-08-29). Every number below is a measured
row in `perf/results/experiments.jsonl` (pod H100 PCIe, jax 0.4.38, N=256
real advanced states) or `perf/results/rows.jsonl`. Prototype
`proto_devrec.py` (+`--devrec` bench flag) passed all parity gates
(gate_batch inline + async: PASS, worst rel err 3.8e-13 vs 1e-12 tol,
ZERO fallbacks; assay-level decision identity PASS) and the pod claim row
landed: **t2 frozen workload 697bcb716916: 42.31 -> 92.20 w/h (2.18x),
zero fallbacks over 4779 device points / 14737 lane-records**. E4 added:
the global x64 flag does NOT change f32 stepper bits (state+records
sha-identical) — the f64-accumulator policy is deploy-safe.

## 0. What the experiments established (E-rows)

| # | question | answer |
|---|----------|--------|
| E1 | naive min-neighbor label propagation | correct partition, but 496 sweeps on real labyrinths; 0.94 ms/field fused. Right math, wrong algorithm. |
| E1b | sweep + pointer-jumping | STALLS — unions land at pixels; 3/12 fields never converge. Rejected. |
| E1c | scatter-min ROOT merging (label-equivalence; `jnp.at[roots].min(neighbor_min)`) | (outer=4, jumps=8) converges on all 11 real fields AND a serpentine spiral (diameter ~N²/8); partition == `G.periodic_label` exactly; 0.12 ms/field labels-only (B=12). Device convergence flag = one probe iter == no-op. |
| E2b | segment stats on converged labels (sort-based dense rank + scatter-add + scatter-max) | PARITY OK vs `blob_list_fast` on all real fields: same blob sets, area/peak exact, worst rel err 5.5e-7 (f32 sums). ccl+stats+pull e2e 1.58 ms/field at B=11 vs host 12.0 ms/field = 7.6x. |
| E2c | f64 accumulators (JAX_ENABLE_X64) | POLICY PASS: integer/max outputs bit-exact, worst centroid rel err 1.1e-15 (<< 1e-12 gate); e2e 0.91 ms/field at B=11 — f64 is NOT slower here (sort dominates, not the adds). |
| E3 | can stats-jit overlap step-jit? | NO — one XLA compute stream: interleaved == serial sum (ratio 1.000). Stats must be BUDGETED, not hidden. Stats for a full 32-lane b14 call: +34.9 ms (f32, 128 fields) on top of a 410 ms step chunk. |
| E3d | tiny-row/acts pull after async step | full acts pull (32,4,256,256) f32 = 28.8 ms; stats rows (B,256,7-ish) are ~100x smaller -> negligible. |
| — | host baseline (t2 instrumented, workload 697bcb716916) | record 2299 s cum / x1.5 eff at 8 threads = ~60% of the 1505 s wall. Post-procrec (x1.10) barrier analysis: other=575 s. |

## 1. Architecture

One extra jitted call per REC point, per batched call; everything else is
plumbing that already exists (0.2 driver seams + procrec/async-apply
machinery from this thread):

    [device, one stream]                         [host]
    step_chunk(F, ...)          250 steps
    acts = F[:, :na_max]        (view)
    mask = acts > thr_dev       (B*na fields fused)
    lab  = ccl(mask)            scatter-min root merge, outer=4, jumps=8
    rows = stats(lab, acts)     dense-rank + segment f64 sums/max
                                -> (Bna, MAXL, 7) + nlab + converged
    ------ tiny D2H pull (~0.5 MB) ------------------------------------
                                 assemble blob dicts (rows -> blob_list
                                   format, angle/centroid on host f64)
                                 apply_record (async, H-A machinery)
                                 CREC/orgs/memf: UNCHANGED host path
                                   (procrec pool) until phase 2
    barrier: rung decision points only (H-A)

Key structural choices, each pinned by an E-row:

- **CCL = scatter-min root merging** (E1c). Per outer iter: `jumps`
  pointer-jump compressions (`lab <- min(lab, lab[lab])` on the flat
  (B, N²+1) table with a background sink slot) then neighbor-min via 4
  periodic `jnp.roll`s scattered into ROOT slots with `.at[brow, roots]
  .min(nmin)`. outer=4/jumps=8 converged EVERYTHING we could throw at it;
  ship (outer=5, jumps=8) for margin + the device `converged` flag.
- **Fallback, not failure** (E5 for free): if `converged[b]` is False for
  any field, THAT lane's record falls back to host `blob_list_fast` for
  this point (stock path; procrec pool). Guaranteed-correct hybrid;
  fallback rate is a bench counter (expected 0 — spiral converges).
- **Stats = one fused segment pass** (E2b/E2c): sort-based dense rank
  (argsort of labels, cumsum of boundaries = per-field blob index), then
  scatter-add segments for mass/area/trig moments (periodic centroid via
  circular mean, exactly the host math) + scatter-max for peak. MAXL=256
  rows/field with an overflow flag -> host fallback for that field
  (labyrinth fields have <40 blobs; 256 is 6x headroom).
- **f64 accumulators always-on for the stats kernel** (E2c: free). The
  stats jit is compiled with x64 enabled scoped to these arrays (weights
  cast from the f32 field exactly like the host's `np.float64(u)`).
- **No stream tricks** (E3): jax = one compute stream; the stats call
  runs after the step chunk in the same queue. It still wins because
  34.9 ms of device stats replaces ~704 ms of effective host record
  (32-lane b14 point). Pull of stat rows is negligible (E3d).
- **Blob-dict assembly + record-list mutation stays on host** in the
  H-A async-apply drain thread: rows -> `[[y, x, area, peak], ...]`
  (angle() in host f64 — parity with `blob_list_fast`'s np.angle), then
  `apply_record` verbatim. Mass series = the `tot` sum row (dx² scaled).
- **CREC (patches/orgs/memf) and snapshots: unchanged host path, phase 1.**
  They are 1-in-5 points and carried by procrec+async-apply; moving orgs
  (thr_lo labeling + spans) to device is phase 2 using the same CCL
  (second threshold), only if the post-phase-1 instrumented row says so.

## 2. Timing budget per REC point (b14 32-lane call, na<=4 -> 128 fields)

Measured components (E3/E3d/E2b/E2c, `rows.jsonl` t1-gpu):

| component | today (host record) | devrec phase 1 |
|-----------|--------------------:|---------------:|
| step chunk (250 steps, B=32 b14) | 410 ms | 410 ms |
| acts pull (32,4,256,256) | 28.8 ms (in wall when not overlapped) | only at CREC points |
| host record 32 lanes (pred-class 33 ms ea / x1.5 eff) | ~704 ms (partially overlapped; measured net: record dominates wall) | — |
| device ccl+stats (128 fields, f32; f64 same order) | — | ~35 ms (E3; f64 variant to re-measure at 128 fields, E2c says ~parity) |
| stat-row pull (128 x 256 x 7 f64 ≈ 1.8 MB) | — | ~1-3 ms (E3d scaling) |
| host assemble+apply (tiny lists; async drain) | — | hidden under next chunk (H-A) |
| **REC-point total (device queue)** | **410 + record-bound host** | **~445-450 ms** |

Per-rung derivation (rung 2500 tu = 10 chunks of 25 tu... at REC=5 tu, 250
steps/chunk = 5 tu: 500 REC points per 2500 tu): today the record path
contributes ~2299 s cum / 4 calls ≈ 575 s-cum per call-mix; devrec turns
each REC point into step+stats ≈ 445 ms vs step+record-wait. Projected t2
(workload 697bcb716916, 16 lanes, T-mix as frozen):

    sim chunks (dispatch, measured) ......... 493 s   (instrumented row)
    devrec stats +8.5% of dispatch .......... +42 s   (35/410 scaling)
    battery (rung ends, pool) ............... 356 s -> hidden partially by
                                              H-A only at rung boundaries;
                                              worst case stays 356 s
    pulls: CREC-only full pulls ............. ~10 s   (1/5 of 40 s + rows)
    residual host apply (async, hidden) ..... ~0
    ------------------------------------------------
    projected wall ~ 493+42+356+10+overheads ≈ 900 s -> ~64 w/h
    with H-A hiding battery under speculative next rung (phase 3) or
    bigger B (post-devrec re-rank): -> 130-220 w/h corridor

Honest uncertainty: battery 356 s is now the co-equal pole; devrec+H-A
alone gets ~1.5x on the frozen workload; the full corridor needs the
post-devrec instrumented row to re-rank (exactly what the bench emits).

## 3. Parity contract (approved policy)

1. **Exact (bitwise):** component PARTITION (canonical bijection check vs
   `G.periodic_label`), blob COUNT, AREA counts, PEAK values, and all
   INTEGER outputs. Gate: every devrec record point in the gate runs must
   produce the same blob SET as `blob_list_fast` (order-insensitive
   match on (area, peak) exact + centroid within tolerance).
2. **Tolerance (1e-12 rel):** SUM outputs (mass `tot`, trig moments ->
   centroids). f64 device accumulation measured at 1.1e-15 worst — 3
   orders of margin. Gate compares y/x/mass per matched blob.
3. **Record-stream identity:** the assembled `[[y,x,area,peak],...]` rows
   and `mass` floats go through `apply_record` — byte-compare of the
   final record dicts vs stock host runs on gate worlds (m0, pred, coex,
   ds3_014; T=500 multi-rung), modulo the documented float tolerance on
   y/x/mass (expected: EQUAL in repr for area/peak; <=1e-12 for the rest).
4. **Decision identity:** T_used / why_stopped / n_extensions / interest
   identical on the gate ladder (same bar as async-apply's
   gate_assay_async.py — reuse it with --devrec).
5. **Fallback containment:** unconverged CCL or MAXL overflow -> host
   path for that (lane, field, point); counter in the bench row; any
   fallback >0 on gate workloads = investigate before ship.

## 4. Failure containment

- NaN/blowup: mask of non-finite acts computed on device with the stats
  (one `jnp.isfinite` reduction per field, free); non-finite -> lane
  flagged, host `_record` handles the blowup path stock (it needs the
  field anyway at CREC; blowup exit pulls full state once).
- Pool loss (procrec/battery): existing broken-pool fallbacks unchanged.
- Devrec jit failure at runtime (OOM on huge B): flag off -> stock path;
  the wrapper is per-call, not per-process.

## 5. Integration plan (P4)

`proto_devrec.py` (bench-only, like proto_procrec/proto_asyncapply):
wrap `DRV.run_chunks`; replace `record_fn` for REC-grid points where
`t % crec != 0` with: device stats call + async assemble/apply via the
H-A recorder. CREC points and snapshots go stock (full pull + procrec
extract). `--devrec` flag in bench.py composes with `--asyncapply`.
0.4 engineering: the same split lands in `sim_gpu` as a `record_mode=
"device"` driver kwarg + `_record_device()` beside `_record_host()`
(the seam driver.py documented for exactly this); relock + V1-style gate.

## 6. Phase 2/3 (post-claim options, re-ranked by instrumented rows)

- orgs/patches on device (same CCL at thr_lo; spans need per-component
  min/max scatter — cheap): removes CREC extract from host.
- memf coarse: a (BLOCK x BLOCK) mean pool on device — trivial.
- battery overlap (H-A speculative rung k+1): the remaining 356 s pole.
- B=64/96 pooled calls: kernel scales (T1 gpu cells flat per-world);
  devrec stats scale linearly with fields — re-bench.
