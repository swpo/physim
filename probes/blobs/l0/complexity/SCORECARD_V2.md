# SCORECARD — l0-metrics-v2 (phase 6 complexity battery v2 + adaptive assay)

## Deliverables (all in probes/blobs/l0/complexity/; v1 untouched)
- metrics_v2.py    LOCKED battery v2: M1 interaction-gated ecology, M2
                   organism/segment duality, M3 bilinear-aware memory grading
                   + charging, M5 succession C8, M6 box-limit, windowed rate
                   metrics; reuses locked v1 d2-d5 verbatim.
- assay_v2.py      LOCKED adaptive-horizon driver (M4): 2500 -> x2 -> 20000,
                   extend on slow-channel charging / organism trends / ACF
                   non-convergence; battery at each checkpoint; horizon report.
- soup_sim_v2.py   chunked-continuation simulator, BITWISE parity vs single
                   run and vs v1 soup_sim records; organism (thr_lo) patches
                   + periodic-safe spans recorded on the CREC grid.
- ASSAY_V2_API.md  the evolve-v2 contract (genome-in; return layout; cell-key
                   fields incl. n_species_int, org_model, n_stages, mem_grade).
- VALIDATION_V2.md full table (10 worlds x seeds 1-2 + seed-3 out-of-sample),
                   gates, horizon behavior, honesty notes.
- run_val_v2.py / run_v1_baseline.py / aggregate_v2.py; v2_scores_s12.json;
  v2_lock_hashes.txt; runs_v2/*.npz (raw runs incl. every extension chunk);
  results.json rows kind="assay_v2" for every run (save-as-you-go).

## Validation verdict (seeds 1-2 calibration; seed 3 OUT-OF-SAMPLE all-pass)
- Ordering (means s1-3): m0 2.8 << coex 15.0 < m4 23.7 < xv 30.8 < bf 34.2
  < mv3 41.2 ~ pred 45.3 << ds3_017 65.4 ~ ds6_000 65.6 < ds3_014 75.6.
  v1 group structure preserved; champions 20+ points above designed worlds.
- REQUIRED ds3_014 behavior: auto-extends on every seed where its succession
  is still running (s1 10000/77.3, s2 20000/80.3, s9 10000/77.1 — all >=10000
  and above its 2500 checkpoints 68.1/47.2; also above its v1 screen 68.8 and
  v1 audit 60.7). Seed 3's succession completes EARLY (t_half 1140/1863) and
  the assay honestly converges at 5000 with 69.2, both stages still detected
  (C8=0.5): the horizon tracks when the story ends, not a fixed schedule.
  ds3_014-v2 (75.6 mean) now ranks ABOVE ds3_017-v2 (65.4) — the film-vs-
  metric disagreement v2 was built to close is closed.
- m0/statics: every static seed-run stops at 2500 (18/18 incl. seed 3); wall
  median 0.99x v1 in a same-shape baseline (gate <=1.5x) — adaptivity costs
  boring candidates nothing.
- Horizon dividends beyond the brief: pred +8 (charging tanh ecology was
  undervalued at 2500), mv3 s1 36->53 at cap (bind/unbind organism churn is
  real dynamics; its soup is honestly bimodal across seeds).
- Box-limit flags (M6): ds3_014 all seeds (span ~ L), mv3 s1, pred both
  seeds -> the L=192/256 confirm list, deferred as instructed.

## Key numbers for the searcher (evolve-v2)
- Call: assay_v2.run_assay(genome, seed, results_path=your results_v2.json).
- Cell-key fields ready: D.d7.n_species_int (passenger-proof species count),
  D.d1.org_model/org_growth (organism-level class), D.d1.n_stages (0/1/2/3),
  D.d6.mem_grade (0/1/2 with bilinear reads = 2 — ds3_014's fossil vertex
  grades ACTIVE), D.d5 phase/wind unchanged.
- Cost model: static candidate = 1.0x v1 T2500; extending candidate pays
  ~2x per doubling plus ~40-90s battery per checkpoint. ds3_014-class runs
  ~8000-12700s wall under parallel load (4-6 procs); budget accordingly.

## Honesty
- mv3 seed variance (38 vs 53) is a real property of its soup, surfaced (not
  created) by the horizon: the machine either assembles or does not. Median
  robust; org_model bin recommended for cell keys rather than raw score.
- coex fell slightly (16 vs v1 17-18): its C6 was turnover-free already; C8
  dilution (new weight mass) explains ~all static-world deltas (x0.92).
- ds3_017 v2 62-67 vs v1 73-76: no succession (C8=0) + C2~0 (its slow modes
  converge fast) — it remains #2. The gap to ds3_014 reversed BECAUSE of the
  horizon, which is the intended lesson of the exercise.
- One criteria rewrite happened pre-lock (c_acf from cheap counts-only to
  battery d2): xv_s1/mv3_s1 were re-run under final criteria; all other rows
  were produced by code whose decisions match the final module (verified on
  saved records).

## LOCK ANNOUNCEMENT
metrics_v2.py + assay_v2.py + soup_sim_v2.py are LOCKED (SHA256 in
v2_lock_hashes.txt). The evolve-v2 searcher should consume assay_v2.run_assay
per ASSAY_V2_API.md (contract unchanged since pinning). Seed-3 out-of-sample
completed post-lock with zero edits and zero gate violations.
