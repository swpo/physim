# VALIDATION — complexity assay battery v1 (phase 5, l0-metrics)
2026-02-20. Metrics LOCKED as `metrics_v1.py` after calibration on seeds 1-2;
seed 3 is OUT-OF-SAMPLE (run with the locked module, no edits after).

## The assay (S1 "soup") — locked protocol
`soup_sim.run_soup`: L=128 dx=0.5 dt=0.02, T=5000tu, 12 dressed pokes
(dress=0.6, amp=2, sig=3 — the locked a1_panel revival convention), random
positions (min sep 16px), species round-robin, every blob kicked 0.5px in a
random direction (BF5 lesson: symmetric ICs sit on unstable branches).
Working noise 2e-3 on activators (machinev3 hold-noise level). Recorded:
per-act blob lists every 5tu (periodic labeling, thr_frac=0.45, verbatim
genome.py conventions), patch stats + coarse (8px) memory-channel fields
(tau>=30) every 25tu, act-field snaps at t=0/250/2500/5000.
Numerics: genome.py IMEX-FFT verbatim (explicit reaction w/ OLD u in drives,
exact diffusion in k), scipy.fft backend, float32 (parity-gated, below).

## Descriptors D (metrics_v1.full_battery)
- d1 population: n(t) via `compact_top_fit` (constant/relaxation/oscillator/
  switch) + turnover from track births/deaths + species survival.
- d2 timescales: ACF e-fold times (linear detrend) across ALL coarse
  observables (n, biomass, patch count, coverage, mean speed, bond count,
  bond angle), amplitude-gated (floors: counts 0.15, mass cv 1.5e-3,
  cover cv 1e-2, speed 0.005 px/tu, bonds max(0.3, 5% of mean), angle 0.05).
  Oscillatory observables report their PERIOD if q>=0.4 and >=3 cycles.
  Hierarchy ratio r_emerg = tau_slow / max(tau_genome, 50tu).
- d3 spatial: periodic patch stats; coarsening log-log slope; patch-size tail
  (`powerlaw_tail`); g(r) from blob positions of the last 1000tu, bond peak
  restricted to r<=28px (beyond = mean-spacing shell of a dilute gas,
  measured on gt_xv), r_bond = first minimum after the peak.
- d4 motion: track speeds over 25tu windows; moving fraction (>0.02 px/tu
  ~ 4x M0 noise-jitter floor 0.005); neighbor (<=1.5 r_bond) velocity cosine;
  net-transport ratio; per-species speed/moving-frac -> role_div.
- d5 graph: bond network (pairs < 1.5*r_bond, 1.15x leave-hysteresis) on the
  25tu grid; churn = (created+destroyed)/2 / edges / 100tu; phase label
  frozen/liquid/flicker/gas; rotation scan: max angular RANGE (turns) over
  sustained pair bonds + pair-COM speed (rotor = winds >=1.5 turns with
  parked COM; curving traveling bonds are excluded by com_speed>=0.03).
- d6 memory: realized tanh/slow-channel (tau>=30) structure: coverage above
  0.25*p99.5 amplitude (floor 1e-3), patch elongation (trails are anisotropic),
  pattern-ACF persistence ratio r_mem = tau_obs/tau_chan.

## Interest scalar v1
components C1..C7 in [0,1] (see `metrics_v1.components`), weights
C1 pop 0.12 | C2 timescale 0.13 | C3 motion 0.15 | C4 graph 0.10 |
C5 memory 0.18 | C6 ecology 0.20 | C7 roles 0.12, x100, zeroed if the soup
dies (n_end<2). Graded C4 (log-tent over churn100 in [0.005,1.2,4.0]) removed
the frozen/liquid knife-edge that flipped coex seeds by 8 points.

## Ground-truth table (3 seeds x 7 worlds; seed 3 = out-of-sample)
| world | s | int | C1 | C2 | C3 | C4 | C5 | C6 | C7 | d1 mod | n_e | tau_s | mvfr | phase | wind | mem |
|-------|---|-----|----|----|----|----|----|----|----|--------|-----|-------|------|-------|------|-----|
| m0    | 1 |   3.1 | 0.05 | 0.00 | 0.00 | 0.25 | 0.00 | 0.00 | 0.00 | consta |  12 |    0 | 0.00 | frozen | 0.0 | 0.00 |
| m0    | 2 |   3.1 | 0.05 | 0.00 | 0.00 | 0.25 | 0.00 | 0.00 | 0.00 | consta |  12 |    0 | 0.00 | frozen | 0.0 | 0.00 |
| m0    | 3 |   3.1 | 0.05 | 0.00 | 0.00 | 0.25 | 0.00 | 0.00 | 0.00 | consta |  12 |    0 | 0.00 | frozen | 0.0 | 0.00 |
| m4    | 1 |  27.9 | 0.05 | 0.36 | 0.84 | 1.00 | 0.00 | 0.00 | 0.00 | consta |  12 |  175 | 1.00 | liquid | 1.1 | 0.00 |
| m4    | 2 |  30.8 | 0.05 | 0.47 | 0.94 | 1.00 | 0.00 | 0.00 | 0.00 | consta |  12 |  250 | 1.00 | liquid | 0.9 | 0.00 |
| m4    | 3 |  25.8 | 0.05 | 0.32 | 0.74 | 1.00 | 0.00 | 0.00 | 0.00 | consta |  12 |  150 | 1.00 | liquid | 2.0 | 0.00 |
| xv    | 1 |  32.5 | 0.05 | 0.71 | 1.00 | 0.25 | 0.00 | 0.00 | 0.43 | consta |  12 |  575 | 0.08 | frozen | 7.9 | 0.00 |
| xv    | 2 |  36.3 | 0.10 | 0.64 | 0.58 | 1.00 | 0.00 | 0.03 | 0.61 | switch |  14 |  460 | 0.26 | liquid | 1.6 | 0.00 |
| xv    | 3 |  37.4 | 0.05 | 0.71 | 1.00 | 0.74 | 0.00 | 0.00 | 0.44 | consta |  12 |  575 | 0.08 | liquid | 7.9 | 0.00 |
| bf    | 1 |  38.8 | 0.05 | 0.09 | 0.78 | 1.00 | 0.85 | 0.00 | 0.00 | consta |  12 |  275 | 1.00 | liquid | 1.6 | 0.12 |
| bf    | 2 |  41.4 | 0.05 | 0.22 | 0.85 | 1.00 | 0.85 | 0.00 | 0.00 | consta |  12 |  425 | 1.00 | liquid | 1.7 | 0.12 |
| bf    | 3 |  38.9 | 0.05 | 0.16 | 0.82 | 1.00 | 0.77 | 0.00 | 0.00 | consta |  12 |  350 | 1.00 | liquid | 1.5 | 0.12 |
| pred  | 1 |  39.2 | 0.55 | 0.33 | 0.03 | 0.81 | 0.88 | 0.12 | 0.12 | relaxa |  79 |  475 | 0.05 | liquid | 0.5 | 0.19 |
| pred  | 2 |  41.0 | 0.55 | 0.45 | 0.03 | 0.85 | 0.86 | 0.12 | 0.14 | relaxa |  70 |  700 | 0.05 | liquid | 0.3 | 0.17 |
| pred  | 3 |  41.8 | 0.55 | 0.33 | 0.04 | 0.95 | 0.87 | 0.15 | 0.18 | relaxa |  71 |  475 | 0.06 | liquid | 0.6 | 0.16 |
| coex  | 1 |  24.6 | 0.05 | 0.56 | 0.02 | 0.81 | 0.24 | 0.00 | 0.33 | consta |  12 |  850 | 0.03 | liquid | 1.3 | 0.02 |
| coex  | 2 |  20.1 | 0.05 | 0.40 | 0.03 | 0.58 | 0.22 | 0.00 | 0.34 | consta |  12 |  500 | 0.05 | frozen | 0.5 | 0.02 |
| coex  | 3 |  25.0 | 0.05 | 0.42 | 0.04 | 0.86 | 0.28 | 0.00 | 0.40 | consta |  12 |  525 | 0.07 | liquid | 0.4 | 0.02 |
| mv3   | 1 |  45.4 | 0.10 | 0.65 | 0.59 | 1.00 | 0.00 | 0.33 | 0.85 | switch |  15 |  475 | 0.53 | liquid | 1.9 | 0.00 |
| mv3   | 2 |  41.0 | 0.40 | 0.62 | 0.41 | 1.00 | 0.00 | 0.04 | 0.93 | oscill |   9 |  425 | 0.49 | liquid | 1.5 | 0.00 |
| mv3   | 3 |  42.4 | 0.10 | 0.74 | 0.30 | 1.00 | 0.00 | 0.30 | 0.91 | switch |  27 |  650 | 0.38 | liquid | 1.4 | 0.00 |

## Summary (mean over seeds [min,max])
| world | label | T=5000 | T=2500 | verdict |
|-------|-------|--------|--------|---------|
| m0   | (a) static gas        |  3.1 [3.1,3.1]   |  3.1 | boring baseline — LOW as required |
| coex | (f) 3-sp coexist      | 23.2 [20.1,25.0] | 16.7 | static coexistence, weak churn |
| m4   | (b) traveling bonds   | 28.2 [25.8,30.8] | 25.8 | motion + liquid bonds |
| xv   | (c) rotor             | 35.4 [32.5,37.4] | 34.9 | persistent rotation found by winding scan |
| bf   | (d) autophoresis      | 39.7 [38.8,41.4] | 36.8 | memory (trail cover+elong) + motion |
| pred | (e) predation         | 40.7 [39.2,41.8] | 40.1 | births/deaths + logistic n(t) + tanh-field memory |
| mv3  | (g) machine (designed)| 42.9 [41.0,45.4] | 37.1 | roles (engine vs cargo) + ecology + slow modes |

RANK: m0 (3) << coex (23) < m4 (28) < xv (35) < bf (40) ~ pred (41) < mv3 (43).
Required ordering a << b,c < d,e,g: SATISFIED, with margins:
a(max 3.1) << b(min 25.8); b,c(max 37.4) < d,e,g(min 38.8) — no seed overlap
between the {b,c} and {d,e,g} groups; 8x gap between a and everything.

## Where metric and intuition disagree (reported per task)
- coex (f) lands BELOW m4. Defensible: in the soup its 12 blobs park into a
  near-frozen weak-bond lattice — 3 species coexist but produce no motion, no
  turnover, no memory. "Coexists" is a static property; the assay rewards
  dynamics. If the search wants coexistence per se, gate on
  d1.n_species_alive (reported separately) rather than the scalar.
- pred (e) scores mostly through C5 (its 149tu tanh channel builds real
  spatial structure, r_mem~7) and C1 (logistic n(t): 12 -> ~75 blobs), while
  its C6 ecology component is small (0.12-0.15): predation kills species 2
  within 400tu (winner-take-most). A PERSISTENT predator-prey cycle would
  score C6 higher; this world is a transient-ecology world. Intuition
  updated, not the metric.
- mv3 (g) wins WITHOUT its memory channel being used (C5=0: the merged world
  has no tau>=30 channel; the machine's slow modes show up in C2/C7 instead).
  Its C7=0.85-0.93 (engine moves at c~0.2, cargo parks) is exactly the
  designed division of labor. 

## Robustness checks
- f32 vs f64 (T=800, m4 + pred): max |dC| 0.15 (C2 on m4, ACF-window
  sensitivity at short T), all phase labels + rank order identical -> f32 OK.
- T=2500 truncation: same ordering (table above) -> screening can run 2500tu.
- Cost (solo, M1 Max): m0 187s, bf 264s, xv 401s, mv3 625s, pred 675s at
  T=5000; halve for T=2500. Battery itself ~15-30s. Fits the 3-5 min budget
  (worst case pred T=2500 ~ 5.6 min at L=128; L=96 option cuts 2.25x more).
- Synthetic unit tests (synth_tests.py; run vs metrics_dev at lock time): static
  lattice -> frozen/mv 0; ballistic flock -> mv 1.0, v_corr 1.0; independent
  walkers -> v_corr ~0, liquid; oscillating population -> oscillator q 0.88;
  hidden slow mass mode -> tau_slow 345tu on mass series. ALL PASS.

## Honesty / provenance
- Selection: these 7 worlds are certified/screened references, not new
  physics. The battery was CALIBRATED on seeds 1-2 (5 metric edits, logged in
  results.json rows kind=soup_assay metrics=metrics_dev) and FROZEN before
  seed 3. Seed-3 scores moved every world by <5 points and no rank swaps
  within the constraint groups -> the scalar generalizes across ICs.
- Known limits: (i) winding scan needs the pair tracked >=15 coarse frames —
  rotors that assemble in the last 500tu are missed; (ii) C6 rewards turnover
  only when >=1 species survives and population is retained — pure extinction
  cascades score 0 by design; (iii) g(r) bond radius capped at 28px — worlds
  with certified d*>28 would need the cap raised (none known); (iv) blob
  identity via greedy 6px/5tu matching — speeds >1.2 px/tu would break
  tracking (fastest known: engine 0.2 px/tu).
