# NOTES_v2 (build log, l0-metrics-v2)
- soup_sim_v2: chunked continuation, PARITY bitwise vs single run (m4 T=200 test,
  maxdiff 0.0) and vs original soup_sim (blob/mass records identical).
- metrics_v2 fixes during smoke:
  * compact_top_fit calls a constant organism series "oscillator q=0" -> amp-gate
    before fit; osc with q<0.05 scored 0.05.
  * C1 = max(organism-class, segment-class-with-growth-guard): mv3's bind/unbind
    switch oscillation is segment-level, keep; growth claims need ORGANISM growth.
  * organism growth floor: org_growth -> C1 >= 0.55 (ds3_014 switch-dwell gate ate it).
  * genome coupling: DIRECT (K or bilinear read path) w=1.0; SHARED-writer
    (mediated habitat, ds3_014 yellow-blue) w=0.5.
  * staging sep: absolute 500tu (T-scaled sep would merge stages on extension).
- horizon on saved v1 records (truncated to 2500): all 12 static GT seeds STOP;
  pred s1/s2 extend (a_mem: its tanh field really is charging at 2500);
  ds3_014 extends (a_mem 1.09 + b_org); ds3_017 extends (b_org).
- wall baseline for cost gate: v2 assay m0 s7 = 130s wall_sim at T=2500 (2 workers,
  under light load). v1 baseline must be measured same-shape: run soup_assay
  T=2500 on statics for the comparison table.

## Progress checkpoints
- SMOKE PASS m0 s7: STOP@2500 static, 2.8 (v1 3.1), wall 130s solo.
- SMOKE PASS ds3_014 s9: EXTEND 2500(a_mem+b_org) -> 5000(b_org) -> 10000 STOP
  converged. Box-limit TRUE (span ~ L). After windowed-turnover fix (WTURN=2000
  best-window; extension must never punish): 77.1 v2@10000 vs v1 60.7 @5000 /
  68.8 @2500-screen. C6 1.0, C8 0.5 (2 stages: sp0 t_half 1856, sp3 2749).
- GT preview after all fixes (T=5000 saved runs, seeds 1-3):
  m0 2.8 << coex 18-23 < m4 24-28 < xv 30-40 < bf 36-38 ~ pred 38-43 < mv3 37-50.
  mv3 s1/s3 GAIN from windowed turnover (their engine/cargo churn is real
  ecology: births/deaths of bound structures) — watch ordering at lock.
- Wave A+B (12 static assays, seeds 1-2): ALL stop@2500 "static". xv s2 40.2?
  -> no: 28.6 in assay (T=2500); 40.2 was the T=5000 preview number.
- Wave C: ds6_000 s1/s2 STOP@2500 at 65.0/65.9 (v1 63.9); pred s1/s2 EXTEND.
