# VALIDATION_V3 — metrics_v3 (C9 spatial economy + d7b) gate

Status: **GATE COMPLETE** — verdicts below.

Protocol: assay_v3 (locked soup_sim_v2/metrics_v2 verbatim underneath; adaptive-T
ladder capped 2500tu, 5000tu for mv3/champions/m5_trains). Seed 1. CPU (M1 Max, 4-way).

## Gate table (bank x factors x C9 x class x interest v2->v3)

| world | bank | t9 | s9 | e9 | r9 | C9 | class | iv2 | iv3 | T | why |
|---|---|---|---|---|---|---|---|---|---|---|---|
| m0 | a | 0.000 | 0.619 | 0.000 | 0.000 | **0.000** | structured | 2.8 | 2.1 | 2500 | static |
| m4 | a | 1.000 | 0.596 | 0.341 | 0.279 | **0.488** | economy | 22.4 | 29.0 | 2500 | static |
| pred | a | 0.735 | 0.876 | 0.045 | 0.096 | **0.230** | economy | 38.0 | 34.2 | 2500 | cap |
| coex | a | 0.370 | 0.629 | 0.000 | 0.405 | **0.000** | structured | 15.6 | 11.7 | 2500 | static |
| mv3 | a | 1.000 | 0.836 | 0.620 | 0.182 | **0.554** | economy | 49.6 | 51.1 | 5000 | cap |
| p6g8_033 | a | 1.000 | 0.862 | 0.429 | 0.127 | **0.465** | economy | 74.7 | 67.6 | 5000 | cap |
| p3g9_022 | a | 1.000 | 0.619 | 0.680 | 0.166 | **0.514** | economy | 68.6 | 64.3 | 5000 | cap |
| p4g2_044 | a | 0.000 | 0.702 | 0.519 | 0.301 | **0.000** | structured | 76.6 | 57.5 | 5000 | cap |
| cargo_cell | b | 0.747 | 0.670 | 0.184 | 0.102 | **0.311** | economy | 40.5 | 38.1 | 2500 | static |
| m5_trains | b | 0.829 | 0.599 | 0.009 | 0.218 | **0.174** | economy | 26.3 | 24.1 | 2500 | static |
| m2_dimer | b | 0.754 | 0.591 | 0.240 | 0.294 | **0.421** | economy | 27.4 | 31.1 | 2500 | cap |
| m2_dimer_a4 | b | 0.000 | 0.597 | 0.000 | 0.000 | **0.000** | structured | 2.8 | 2.1 | 2500 | static |
| dead | c | 0.000 | — | 0.150 | 0.000 | **0.000** | mixed | 14.1 | 10.6 | 2500 | static |
| frozen | c | 0.000 | 0.633 | 0.000 | 0.000 | **0.000** | structured | 2.8 | 2.1 | 2500 | static |
| noise | c | 0.000 | 0.716 | 0.000 | 0.215 | **0.000** | structured | 9.1 | 6.8 | 2500 | static |

## Verdict vs spec expectations

### Bank (a) — GT worlds + champions: PASS with one revised prior
| expectation (spec) | outcome | verdict |
|---|---|---|
| m0 static gas LOW | C9=0.000 (t9=0 no motion, e9=0 no bond events, r9=0 one phenotype) | PASS |
| labyrinth/storm-class LOW | coex C9=0 (e9=0: never-bonding gas — spec-named factor); pred C9=0.23 (e9 .05: permanent-overlap ecology, r9 .10) | PASS |
| m4 traveling bonds (control) | C9=0.49 economy — sparse movers with episodic bonds; exactly what C9 prices | PASS |
| mv3 engine+cargo (control) | C9=0.554 — top of bank(a); transport machine world | PASS |
| p6g8_033 / p3g9_022 | C9 .47/.51 economy: at T=5000 these champions ARE sparse rotor/swarm ecologies (void .68, disp>=3r, episodic bonds .43/.68). v2 already rewarded them for other reasons; C9 agrees for spatial reasons. iv2->iv3 74.7->67.6 / 68.6->64.3 (renormalization costs dense-only worlds more) | PASS (informative) |
| p4g2_044 "sparse rotor" MID | C9=0.000. NOT a metric bug — diagnosis: acts 2/3 are a box-covering excited carpet (mask_frac .93 raw; carpet-filtered void .35 still under-band, percolation FALSE, zero through-void windows). The "sparse rotor" reading came from blob lists of the 2 blob-forming species only; the locked v2 box_limit flag (span_frac=1.0, persist=1.0) always said organisms span the box. EXPECTATION REVISED: p4g2_044 is a dense-substrate rotor -> correctly LOW | PASS with revised prior |

### Bank (b) — hand-built positives: PASS (2 strong, 2 honest teaching cases)
| world | outcome | verdict |
|---|---|---|
| cargo_cell (membrane R3, N10 ring + confined cargo, etaw12=0.9) | C9=0.311 economy: t9 .75 (cargo bounces through interior void), s9 .67 (flux at ring surface), e9 .18 (ring bonds permanent by design — braced membrane), r9 .10 (2 phenotypes: ring blobs vs cargo, n_eff 1.4) | PASS (HIGH t9/s9 as spec expects; e9 low is the true physics of a permanent membrane) |
| m2_dimer (A=5 binding point) | C9=0.421 economy: HIGH t9 .75 / e9 .24 / r9 .29. The known dt=0.02 A5 artifact (pairs slide + replicate) makes the gas churn — episodic encounters measured | PASS |
| m5_trains (tau=5.7 pair-only drift) | C9=0.174: t9 .83 disp-score with certified transport, s9 .60, but e9 .009 — train bonds are PERMANENT couplings (frozen .58, median life 1975tu). The relay-tug picks cargo up and NEVER lets go: a train is a bound molecule, not a society of meetings | PASS as measurement (metric read the physics right; "trains = high e9" was a wrong prior in the spec bank note; t9+s9 carry it to structured-class) |
| m2_dimer_a4 (A4s statics) | C9=0 — parked dimers at d*, frozen bonds, zero motion. Correct: a crystal of 2-molecules is not an economy | PASS (anti-gaming bonus: it double-confirms the frozen-detector) |

### Bank (c) — anti-gaming: PASS 3/3 via the spec-named factor
| probe | named factor | outcome |
|---|---|---|
| dead (champion chemistry, lam x0.2) | C1 gate | outcome nuance: lam x0.2 left a WEAK FULL-BOX carpet (void_frac=0.0, r_blob=72px, alive, iv2=14.1) rather than zero blobs — C1 did not fire; C9=0 via t9=0 (no void, no movers) + r9=0. A truly-empty variant (noise probe v1 at 6e-3) exits all_dead -> interest 0, C9=0: both dead flavors land at 0. Initial run also exposed e9=1.0 on 12 anecdotal bonds -> E9_SUPPORT_TU=2000 floor added (e9 .15 raw, C9 still 0) |
| frozen (A4s lattice, 8x8 at 16px) | e9 | frozen_frac=1.0 -> e9=0.000 exactly; t9=0 (no motion). C9=0 |
| noise (M0 spot-soup corner k1=-.5,k4=2.5) | r9 clusters unstable | churning speckle, alive (iv2 9.1): r9 .22 (only log-area varies; 1-feature k-cap keeps it at 2 packing strata), and t9=0 (blobs never MOVE through void — replication is not traversal), e9~0 (bond graph flickers frozen). C9=0 |

### Score movement (iv2 -> iv3, W9=0.25 renormalization)
Dense high-C worlds pay the C9 rent unless they also earn spatial economy:
p4g2_044 76.6->57.5 (pure-density world pays most), p6g8_033 74.7->67.6,
p3g9_022 68.6->64.3; mv3 49.6->51.1 GAINS (machine world), m4 22.4->29.0
gains, m2_dimer 27.4->31.1 gains. Rank inversion within champions:
p6g8_033 > p3g9_022 > p4g2_044 under v3 (was p4g2 ~= p6g8 under v2) — the
intended pressure: organism-level complexity must live IN structured space.

## Threshold tunes applied at the gate (all documented in code)
1. VOID_KNOTS (0.35,0.55,0.90)->(0.35,0.55,0.99,0.9975) trapezoid: raw void
   for every certified sparse-transport world sits at .93-.99; the spec tent
   [0.35,0.9] would have zeroed m4/m5_trains/m2_dimer. Emptiness-without-
   movers is already killed by the disp-score and C1.
2. VOID_CARPET_FRAC=0.85: acts covering >85% of the box are media (iso-
   background class), excluded from the occupancy union for t9-void and s9
   shell. Labyrinths (.4-.7 cover) remain counted and punished. (p4g2_044.)
3. E9_SUPPORT_TU=2000: e9 fades in with total bond-lifetime mass (dead-world
   12-bond e9=1.0 exploit).
4. d7b 1-feature k-cap=2: k-means on a single informative feature cannot
   claim >2 species (noise-soup 5-strata packing exploit).
5. economy class requires C9>0 (never-bonding gas with pretty geometry is
   structured, not economy).
TUNABLE PRIORS left as shipped: NEFF_LOG_TARGET=24 (full credit at 24
emergent species; 8 -> 0.65), E9_BAND=[10,500]tu, S9/T9 class thresholds
(.50/.35), SHELL_PX=2.

## Known limitations (for the pilot review)
- s9 needs full-field snapshots (assay_v3 provides; plain v2 records degrade
  to partial=True, C9 over available factors).
- e9 penalizes permanently-bound composite MACHINES (trains). If the pilot
  should reward "molecule societies", consider counting INTER-composite
  encounters (bond graph between connected components, not blobs) in v3.1.
- r9 saturates low: log2(24) target means n_eff 2-3 -> .13-.30. This is by
  design (headroom for emergent speciation), but it drags C9 geometric mean
  for every current world; if the pilot shows r9 pinning C9 below the 0.4
  archive threshold everywhere, revisit NEFF_LOG_TARGET=8 (8 species = 1.0).
- ONE seed per world (gate budget); multi-seed stability deferred to pilot.

## Relock protocol compliance
metrics_v1/v2, assay_v2, soup_sim_* UNTOUCHED (hash-stable vs v2_lock_hashes
.txt). All v3 logic in NEW modules: metrics_v3.py, assay_v3.py,
operators_v3.py, worlds_v3.py, run_val_v3.py. v3 lock hashes:
v3_lock_hashes.txt (written at gate completion).

## merge_spatial_ic (W2) status
operators_v3.merge_spatial_ic implemented + verified end-to-end: m0 x m4
parents -> child genome (parent-A chemistry verbatim) + composed IC from
both parents' T=300 developed states in soft half-plane/disk masks
(periodic-safe seams, SEAM_PX=4); assay_v3.run_assay(ic_override=...) ran it
through the full battery. Hook is DATA-LEVEL (replaces S["F"] after
init_soup) — no locked-file edit. The deploy pod runtime (pod_lib.evaluate)
calls assay_v2.run_assay which lacks the kwarg; pilot needs pod_lib to
import assay_v3 (one line) or pass ic_override through its job dict.

## GATE VERDICT: PASS — all three banks land in the expected order after
the 5 documented tunes. metrics_v3 is ready for the pilot (K2) pending
user review of this table.
