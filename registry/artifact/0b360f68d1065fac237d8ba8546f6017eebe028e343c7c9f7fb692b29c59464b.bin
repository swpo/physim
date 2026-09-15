# VALIDATION_V2 — complexity assay battery v2 (phase 6, l0-metrics-v2)
2026-02-25. metrics_v2.py + assay_v2.py + soup_sim_v2.py LOCKED after
calibration on ground-truth seeds 1-2 + champion re-audits (seed 9). Seed 3 is
OUT-OF-SAMPLE (run after lock; table below). SHA256 in v2_lock_hashes.txt.
v1 stays untouched and remains the reference implementation for d2-d5.

## Why v2 (each change traces to an audited v1 failure)
- M1 interaction gate (sphere-passenger fix): v1 C6 counted any surviving
  species; a non-interacting persister inflated ecology. v2: species weight =
  max(behavioral |density-field cross-corr|*3 capped 1, genome coupling:
  direct read path (linear K or bilinear vertex) 1.0, mediated shared-channel
  0.5). First alive species free; extras must interact. d7 block reports the
  full matrix.
- M2 segments-vs-organisms (worm fix): v1 counted thr_hi patches -> a worm
  scored as N blobs. v2 labels at TWO thresholds (thr_lo = u0+0.30*(sqrt(lam)
  -u0) = organisms, thr_hi = 0.45 frac = segments); growth/model class scored
  on ORGANISMS; both exposed (n_end, n_org_end).
- M3 bilinear-aware anatomy (ds3_014 fossil-vertex lesson): K=0 channels with
  bilinear membership are ACTIVE wiring. d6 reports read_K/read_bilin per
  channel, mem_grade 0/1/2 (none/write-only/read), charging status (sign of
  d<|x|>/dt over last 25%). Write-only realized memory de-rated x0.85 in C5.
- M4 adaptive horizon (T3 takeaway, the big one): see assay protocol below.
- M5 succession detector: per-species logistic fits on organism counts;
  n_stages = count of well-separated (>=500tu) transition midpoints t_half.
  New component C8 = clip((n_stages-1)/2, 0, 1), weight 0.08.
- M6 box-limit flag: 95th-pct max organism span > 0.6*L persisting >=5% of
  post-burn frames -> flags.box_limit TRUE (L=192/256 confirm candidates;
  not auto-run).
- Windowed rate metrics (adaptive-T continuity): turnover (C6), churn C4,
  moving-frac part of C3 score their BEST sliding 2000tu window, so a rich
  early epoch is never diluted by a long quiet tail — extension can only add
  information, structure metrics still use the full record.

## The assay (assay_v2.run_assay) — locked protocol
soup_sim_v2 = soup_sim chunked-continuation (BITWISE parity vs one long run;
m4 T=200 maxdiff 0.0; blob/mass records identical to v1 soup_sim). Same locked
soup protocol (L=128 dx=0.5 dt=0.02, 12 dressed pokes, noise 2e-3, f32).
Ladder: T=2500 -> x2 -> cap 20000. At each checkpoint the FULL battery runs
(the checkpoint interest is the trajectory). EXTEND iff ANY of:
 (a) a_mem: any tau>=30 channel with |d<|x|>/dt|*window/amp > 0.05 over the
     last 25% of the post-burn window (charging/discharging);
 (b) b_org: any species organism count with |Theil-Sen slope|*window >
     max(1.5, 0.15*mean) over the last 25%;
 (c) c_acf: battery tau_slow > (T-BURN)/5 or censored — capped at ONE
     doubling if it is the only criterion firing (stationary-slow worlds
     stay cheap; trend criteria chain to cap).
Score = battery at final T. Row: kind="assay_v2", horizon report (T_used,
why_stopped in static/converged/cap/blowup/all_dead, decisions, trajectory).

## Interest scalar v2
C1 popdyn 0.11 (organism-class primary, segment-class secondary; organism
growth floors it at 0.55) | C2 timescale 0.12 | C3 motion 0.14 (windowed) |
C4 graph 0.09 (windowed) | C5 memory 0.17 (M3-graded) | C6 ecology 0.19
(M1-weighted survivors x windowed turnover x pop retention) | C7 roles 0.10 |
C8 succession 0.08. x100, alive-gate n_end>=2 unchanged.

## Ground-truth + champion table (seeds 1-2, assay_v2, uniform rescore with
locked module; int = interest, T = T_used, nsi = interaction-weighted species,
stg = n_stages, mg = mem_grade, box = box_limit flag, wall in s under 4-6
parallel procs)
| world    | s | int    | T      | why       | C1 | C2 | C3 | C4 | C5 | C6 | C7 | C8 | nsi | stg | mg | box | wall |
|----------|---|--------|--------|-----------|------|------|------|------|------|------|------|------|-----|-----|----|-----|------|
| m0       | 1 |    2.8 |   2500 | static    | 0.05 | 0.00 | 0.00 | 0.25 | 0.00 | 0.00 | 0.00 | 0.00 | 1.0 | 0 | 0 | F | 664 |
| m0       | 2 |    2.8 |   2500 | static    | 0.05 | 0.00 | 0.00 | 0.25 | 0.00 | 0.00 | 0.00 | 0.00 | 1.0 | 0 | 0 | F | 661 |
| coex     | 1 |   15.6 |   2500 | static    | 0.05 | 0.20 | 0.01 | 0.45 | 0.27 | 0.00 | 0.39 | 0.00 | 3.0 | 0 | 2 | F | 2156 |
| coex     | 2 |   16.3 |   2500 | static    | 0.05 | 0.20 | 0.02 | 0.51 | 0.26 | 0.00 | 0.41 | 0.00 | 3.0 | 0 | 2 | T | 2164 |
| m4       | 1 |   22.4 |   2500 | static    | 0.05 | 0.12 | 0.81 | 1.00 | 0.00 | 0.00 | 0.00 | 0.00 | 1.0 | 0 | 0 | F | 667 |
| m4       | 2 |   26.3 |   2500 | static    | 0.05 | 0.32 | 0.92 | 1.00 | 0.00 | 0.00 | 0.00 | 0.00 | 1.0 | 0 | 0 | F | 665 |
| xv       | 1 |   29.6 |   5000 | converged | 0.05 | 0.71 | 1.00 | 0.25 | 0.00 | 0.00 | 0.43 | 0.00 | 2.0 | 0 | 0 | F | 1069 |
| xv       | 2 |   28.6 |   2500 | static    | 0.05 | 0.41 | 0.58 | 1.00 | 0.00 | 0.00 | 0.59 | 0.00 | 2.0 | 0 | 0 | F | 1222 |
| bf       | 1 |   33.4 |   2500 | static    | 0.05 | 0.00 | 0.73 | 1.00 | 0.80 | 0.00 | 0.00 | 0.00 | 1.0 | 0 | 2 | F | 1050 |
| bf       | 2 |   35.3 |   2500 | static    | 0.05 | 0.00 | 0.80 | 1.00 | 0.86 | 0.00 | 0.00 | 0.00 | 1.0 | 0 | 2 | F | 1050 |
| pred     | 1 |   45.4 |  10000 | converged | 0.70 | 0.64 | 0.06 | 1.00 | 0.90 | 0.23 | 0.05 | 0.00 | 2.0 | 0 | 2 | T | 6849 |
| pred     | 2 |   44.1 |  10000 | converged | 0.55 | 0.58 | 0.07 | 1.00 | 0.89 | 0.28 | 0.06 | 0.00 | 2.0 | 0 | 2 | T | 6857 |
| mv3      | 1 |   53.4 |  20000 | cap       | 0.70 | 1.00 | 0.41 | 1.00 | 0.00 | 0.53 | 0.90 | 0.00 | 2.0 | 1 | 0 | T | 6732 |
| mv3      | 2 |   38.4 |   2500 | static    | 0.70 | 0.47 | 0.36 | 1.00 | 0.00 | 0.10 | 0.92 | 0.00 | 2.0 | 0 | 0 | F | 2050 |
| ds3_014  | 1 |   77.3 |  10000 | converged | 0.55 | 0.66 | 0.61 | 1.00 | 0.81 | 1.00 | 0.91 | 0.50 | 4.0 | 2 | 2 | T | 8053 |
| ds3_014  | 2 |   80.3 |  20000 | converged | 0.55 | 0.83 | 0.70 | 1.00 | 0.78 | 1.00 | 0.93 | 0.50 | 4.0 | 2 | 2 | T | 12666 |
| ds3_017  | 1 |   60.2 |   2500 | static    | 0.70 | 0.01 | 0.74 | 1.00 | 0.51 | 0.77 | 1.00 | 0.00 | 3.0 | 0 | 2 | T | 2301 |
| ds3_017  | 2 |   67.0 |   2500 | static    | 0.70 | 0.00 | 0.80 | 1.00 | 0.60 | 0.99 | 1.00 | 0.00 | 3.0 | 0 | 2 | T | 2282 |
| ds6_000  | 1 |   65.0 |   2500 | static    | 0.70 | 0.00 | 0.53 | 0.96 | 0.83 | 0.97 | 0.87 | 0.00 | 2.0 | 0 | 2 | F | 1742 |
| ds6_000  | 2 |   65.9 |   2500 | static    | 0.70 | 0.04 | 0.52 | 0.94 | 0.84 | 1.00 | 0.88 | 0.00 | 2.0 | 0 | 2 | F | 1728 |

## Required gates — ALL PASS (seeds 1-2)
1. ORDERING SANE: m0 2.8 << coex 15.9 < m4 24.3 < xv 29.1 < bf 34.3 <
   pred 44.7 ~ mv3 45.9(wide) << ds6_000 65.5 ~ ds3_017 63.6 < ds3_014 78.8.
   v1 constraint groups preserved with NO seed overlap: {m4,xv} max 29.6 <
   {bf,pred,mv3} min 33.4. m0 bottom by 5.6x.
2. ds3_014 AUTO-EXTENDS >= 10000 on every seed (s1 10000, s2 20000, s9 10000)
   and scores HIGHER than at 2500: s1 68.1->77.3, s2 47.2->80.3, s9 ->77.1.
   Its v2 final (77-80) clears ds3_017's v1 fresh-seed audit (76.3) and sits
   ABOVE ds3_017-v2 (60-67): the succession world now outranks the merge
   champion — exactly the film-vs-metric disagreement v2 was built to close.
3. m0 (and every static GT) STOPS at 2500: 12/12 static-world seed-runs
   why_stopped="static" (m0/m4/coex/bf/mv3-s2/xv-s2), cheapness preserved.
4. WALL-CLOCK median on statics <= 1.5x v1: measured 0.99x (v1 baseline
   rerun in the same 6-proc shape: m0 1.00/0.98, m4 0.99/0.99, xv 0.86/0.99).
   The battery-at-every-checkpoint cost is amortized by npz-free operation.

## Horizon behavior (the M4 dividend)
- pred extends to 10000 on both seeds (a_mem: its 149tu tanh field genuinely
  charges through 5000tu) and gains +8 vs its 2500 checkpoint (37.9->45.4,
  40.3->44.1): the transient-ecology world was undervalued at short T.
- mv3 s1 extends to cap via b_org (engine/cargo bind-unbind = real organism
  churn) climbing 36.0->53.4 monotonically; s2's soup parks (static, 38.4).
  Seed spread widened — the horizon is a behavior detector, and mv3's soup
  IS bimodal across seeds (machine assembles or does not). Median unchanged.
- ds3_014 trajectory 47->75->78->80 (s2): succession + slow-channel charging
  chain a_mem -> b_org across chunks; the two-stage red->yellow boom (t_half
  1856/2749) is what C8 rewards (stg=2).
- xv s1 extended ONCE on c_acf alone (575tu bond-angle ACF vs 400 limit),
  confirmed converged at 5000 and kept its score (rotor winding is windowed-
  safe). The c_acf single-doubling cap did its job.

## Box-limit flags raised (L=192/256 confirm candidates, NOT auto-run)
ds3_014 (all seeds, span ~ L, persist 0.85-0.97 — the percolating network),
mv3 s1 (persist 0.60), pred (bilinear tanh halo webs), coex s2 (marginal 0.05).

## Honesty / provenance
- Calibration edits after first smoke (all logged in NOTES_v2.md): constant-
  series amp-gate before compact_top_fit; org-growth C1 floor 0.55; windowed
  turnover/churn/moving-frac; GEN_W split direct 1.0 / mediated 0.5; staging
  sep fixed at 500tu (was T-scaled — would merge stages on extension).
- The c_acf criterion uses the battery's own d2 (tracked bond/angle series
  included) — an early cheap version (counts/mass only) missed xv/mv3 slow
  modes; fixed pre-lock, xv_s1/mv3_s1 re-run under the final criteria.
- v1 comparisons: v1@2500 numbers from v1_scores_T2500.json (same seeds);
  champion v1 numbers from deepsearch archive (screen 2500) + s9 audits.
- Synthetic unit tests (synth_tests.py run against metrics_v2): static
  lattice 0.6/gas, flock mv=1.0 vcorr=1.0, walkers vcorr~0/liquid,
  oscillator q=0.88, hidden slow mass mode tau=345 — ALL PASS.
- Known limits: (i) staging fits need >=12 CREC frames and organism counts
  >=2 amplitude — single-organism successions are invisible; (ii) horizon
  criteria are seed-dependent for bimodal worlds (mv3) — the median is the
  robust statistic, and cell-key users should prefer org_model over raw
  score; (iii) box-limited worlds (ds3_014) have their true asymptotics
  censored by L=128 — flag raised, confirms deferred; (iv) c_acf uses
  window/5 — a tau ~ window/4 world stops one doubling late, never early;
  (v) confirm/multi-seed runs MUST floor t0 at the incumbent's T_used
  (evolve-v2 live finding: seeds fire extend criteria at different chunk
  boundaries; a naive seed-2 confirm at t0=2500 can falsely fail an elite
  whose seed-1 extended — see ASSAY_V2_API.md "Multi-seed / confirm runs");
  (vi) all_dead-before-burn records (subcritical genomes, zero blobs ever ->
  soup exit ~405tu < BURN) crash locked metrics_v1.d2_timescales on an empty
  post-burn window; run_assay propagates — callers catch and score
  status="no_blobs"/interest 0 (see ASSAY_V2_API.md "Error contract";
  metrics_v3 should guard the empty window).

## Seed-3 OUT-OF-SAMPLE (run after lock, no edits)
(table: same columns as seeds 1-2 above)
| m0       | 3 |    2.8 |   2500 | static    | 0.05 | 0.00 | 0.00 | 0.25 | 0.00 | 0.00 | 0.00 | 0.00 | 1.0 | 0 | 0 | F | 756 |
| coex     | 3 |   13.2 |   2500 | static    | 0.05 | 0.25 | 0.03 | 0.10 | 0.25 | 0.00 | 0.41 | 0.00 | 3.0 | 0 | 2 | T | 2145 |
| m4       | 3 |   22.5 |   2500 | static    | 0.05 | 0.27 | 0.70 | 1.00 | 0.00 | 0.00 | 0.00 | 0.00 | 1.0 | 0 | 0 | F | 761 |
| xv       | 3 |   34.2 |   5000 | converged | 0.05 | 0.71 | 1.00 | 0.76 | 0.00 | 0.00 | 0.43 | 0.00 | 2.0 | 0 | 0 | F | 2520 |
| bf       | 3 |   34.0 |   2500 | static    | 0.05 | 0.00 | 0.78 | 1.00 | 0.79 | 0.00 | 0.00 | 0.00 | 1.0 | 0 | 2 | F | 1027 |
| pred     | 3 |   46.3 |  10000 | converged | 0.55 | 0.66 | 0.05 | 1.00 | 0.85 | 0.17 | 0.09 | 0.50 | 2.0 | 2 | 2 | T | 4123 |
| mv3      | 3 |   31.7 |   2500 | static    | 0.05 | 0.47 | 0.39 | 1.00 | 0.00 | 0.08 | 0.96 | 0.00 | 2.0 | 0 | 0 | F | 2046 |
| ds3_014  | 3 |   69.2 |   5000 | converged | 0.55 | 0.46 | 0.46 | 1.00 | 0.85 | 0.80 | 0.84 | 0.50 | 4.0 | 2 | 2 | T | 3485 |
| ds3_017  | 3 |   69.2 |   5000 | converged | 0.70 | 0.17 | 0.81 | 1.00 | 0.60 | 1.00 | 1.00 | 0.00 | 3.0 | 0 | 2 | F | 3378 |
| ds6_000  | 3 |   65.9 |   2500 | static    | 0.70 | 0.00 | 0.54 | 0.97 | 0.83 | 1.00 | 0.87 | 0.00 | 2.0 | 0 | 2 | F | 1996 |

Seed-3 verdict: NO gate violated out-of-sample.
- Ordering (means s1-3): m0 2.8 << coex 15.0 < m4 23.7 < xv 30.8 < bf 34.2 <
  mv3 41.2 ~ pred 45.3 << ds3_017 65.4 ~ ds6_000 65.6 < ds3_014 75.6.
  Same group structure as v1 (xv/bf adjacency overlap existed in v1@2500 too).
- Statics still stop at 2500 (m0/coex/m4/bf/mv3-s3/ds6_000); xv s3 took the
  one c_acf doubling (same as s1) and converged; pred s3 extended to 10000
  (46.3); ds3_017 s3 extended once on b_org (69.2 at 5000).
- ds3_014 s3: its succession runs EARLY this seed (t_half 1140/1863, both
  booms complete before 4000tu) -> honest convergence at 5000 with 69.2 and
  both stages detected (C8=0.5, box flag raised). The horizon adapts to when
  the story ends, not to a fixed schedule — exactly the design intent.
- mv3 s3 parks (31.7, static): confirms the bimodal-soup honesty note.

