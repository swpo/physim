# V3 PILOT HARVEST (gens 1-7, both islands; snapshots ~/v3work/isl{1,2}_final.tgz)
Success criterion: >=5 economy cells (C9>=0.4 & interest>=60). RESULT: **76 distinct
cells (union)** — isl1 60 / isl2 50; 516 economy rows total. VERDICT: **PASS, 15x bar.**

## Headline findings
1. **merge_spatial_ic validated** — highest hit-rate operator by far:
   op                lanes  econ-rows  rate
   merge_spatial_ic   112       92     0.82   <- v3 flagship (8 lanes/gen only)
   merge_slow_tanh     42       27     0.64
   mint_bilin         168      100     0.60
   delete_bilin        56       32     0.57
   merge_cross_edge   219      116     0.53
   add_chan           112       57     0.51
   mutate             224       89     0.40
   merge_share_chan    51        2     0.04
   dup_act            112        1     0.01
   immigrate          280        0     0.00   <- direct rows only; supplies parents
   (origin-attributed: confirm rows mapped to base candidate's operator)
2. **C9 does not escalate across gens**: max C9 0.85 (isl1 g1) / 0.80 (isl2 g6);
   per-gen econ-row counts stable (22-56); mean C9 flat ~0.25. Economy niches are
   found early (v2-seeded archive + strong operators) and maintained, not
   compounded. 7 gens sufficed for the pilot question.
3. Confirmation depth: 74 (isl1) / 73 (isl2) archive cells seed3-confirmed.
4. Strict spatial_class "economy" is rare: 6 rows (most econ-threshold rows
   classify "structured") — the C9 partial-mode (t9/e9/r9, no s9) gates the
   class conservatively.
5. Best single rows: p1g1_009_s3 I=77.2 C9=0.85 (isl1); p2g6_032_s2 I=76.2
   C9=0.80 (isl2). Top-10 film candidates: 4 are merge_spatial_ic children
   (p1g2_051/052_s3, p1g4_050_s3, p2g7_049_s3 — all I~80-82, C9~0.65).

## Continuation call (gens 8-12 from snapshots)
DEFAULT: NO for same-config continuation — breadth would grow, C9 ceiling would
not (flat trajectory). IF continuing, respec first: (a) reallocate dead lanes
(immigrate 40/gen->10, dup_act 8->0, share_chan 4->0) into merge_spatial_ic
(8->24) + mint_bilin; (b) raise W9 (0.25->0.4) so selection presses C9 directly;
(c) consider full-C9 (s9) confirms for econ elites (CPU assay_v3 on top-K only,
~5 lanes/gen affordable). These are config/selection changes, not engine work.

## Ops notes (for the record)
- Pilot-2 engine fixes (blobkit 0.3.5 ic-on-GPU + pooled rescore) held: ~3.5-4.5
  h/gen, zero worker crashes over 7 gens x 2 islands.
- Confirm settlement through gen 7 done on both islands (CONFIRM7_SETTLED in
  driver.log; two-stage async drain).
- Total spend ~= $110-115 of $150 cap (incl. the 9.5h slow launch + fix window).
- Archive entries lack C9 (ingest field subset); this doc joins results.json.
  Fix candidate for any continuation: carry C9/C9_factors/spatial_class into
  archive rows at ingest.
- Film pipeline: npzs in snapshots out/runs/; candidates above.
