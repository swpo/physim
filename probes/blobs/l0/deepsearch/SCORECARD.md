# SCORECARD — l0-deepsearch (phase 5b: complexity-driven MAP-Elites)

MISSION ANSWERED: sustained selection FOR the audited interest scalar
(metrics_v1, locked) discovers emergent behavior that random/jitter sampling
did NOT find — including a 4-species rotor ecology and a 75-point world that
beats every ground truth by +75% at the full T=5000 protocol.

## Loop-validation gates (both PASS)
1. Archive grows: 14 cells (gen-0 seeds+GT) -> 35 cells (gen-6).
   28/35 cells are NOT in the 7-ground-truth cell set.
2. Evolved candidates beat their seeds:
   - ds3_017 (merge_slow_tanh, I=72.7 screen / 75.1 CONFIRM) from parents
     46.8 + 11.1 — child >> both parents, and > best GT (mv3 42.9) by +75%.
   - ds3_014 (merge_cross_edge, 68.8 / 57.3 confirm) opens 4|rotor|liquid|m1
     from a 3-species parent (66.5) + engine_10748 block.
   - ds5_003 (mutate on ds3_017) 73.7 — the ratchet continues 4 gens deep.

## Gen-over-gen trajectory (24 children/gen, T=2500 screens, seed 1)
| gen | mean I | max I | new cells | events (new/imp/held/dead) |
|-----|--------|-------|-----------|-----------------------------|
| 0*  | 29.9   | 66.5  | 14        | 14/7/11/3   (*35 evals: 7 GT + 8 elites + 20 jitters) |
| 1   | 33.6   | 53.7  | 6         | 6/5/8/5     |
| 2   | 34.8   | 57.0  | 2         | 2/4/11/7    |
| 3   | 38.4   | 72.7  | 9         | (ingested by racing tick; 8 first-gen + 5 improved) |
| 4   | 41.7   | 62.7  | 2         | 2/4/10/8    |
| 5   | 44.6   | 73.7  | 2         | 2/5/13/4    |
| 6   | 44.4   | 68.6  | 0         | 0/0/20/4    |
Mean interest climbs MONOTONICALLY g0-g5 (+49%); g6 plateaus (saturation of
this seed neighborhood at local budget — honest limit, see pod plan).

## T=5000 confirms (16 runs; rank-stability of the screen)
All 9 top holders confirmed. Highlights (screen -> confirm, cell):
  ds3_017 72.7 -> 75.1 (3|mobile|liquid|m1, STABLE) — best world in program
  ds4_020 62.7 -> 62.4 (2|mobile|liquid|m1, stable)
  ds3_001 61.9 -> 58.3 (1|mobile|liquid|m1, stable)
  ds3_014 68.8 -> 57.3 (4|rotor|liquid|m1, STABLE 4-species rotor)
  ds4_001 55.2 -> 56.5 (3|mobile|liquid|m0, stable)
  ds4_006 43.3 -> 49.7 (4|mobile|liquid|m0, stable)
  ds3_019 44.3 -> 45.8 (3|rotor|liquid|m0, stable)
Softeners: g0_jit_11 66.5 -> 51.6 (churn normalizes over longer window);
ds2_005 38.5 -> 31.8 with drift->still label relax (only cell-drift case).
Screen is rank-stable at the top; T=2500 screening mode VALIDATED for search.

## What selection found that sampling did not
- 6 four-species cells (4|*) — stage-2/3 sampling+jitter found ZERO 4-species
  worlds (jitter's ceiling was 2-3 coexisting species, evolve/SUMMARY.md).
- 4|rotor|liquid|m1: 4 coexisting species with a persistent heterodimer rotor
  + memory structure (ds3_014 = jittered rail_111_17 x engine_10748 block —
  the block-library mechanism paid off).
- 2|mobile|flicker|m1 and 2|still|flicker|m1: flicker-phase bond dynamics,
  a graph phase NO prior world occupied.
- 9 cells with screen I > 50 (GT max 40.2 at T=2500): all evolved/jittered.
- Top lineage is COMPOSITIONAL: gt_bf mutant (46.8) + weak XV-jitter (11.1)
  under slow_tanh coupling -> 72.7. The weak parent contributed structure,
  not fitness — exactly the open-endedness signature this program sought.

## Operator economics (gens 1-6, 144 screens)
| op               | n  | ok  | archive holders | best I |
|------------------|----|-----|-----------------|--------|
| mutate           | 60 | 54  | 17              | 73.7   |
| merge_cross_edge | 39 | 38  | 8               | 68.8   |
| merge_slow_tanh  | 21 | 18  | 1               | 72.7   |
| merge_share_chan | 24 | 5   | 3               | 54.5   |
Division of labor CONFIRMED at the soup level: merges OPEN new cells
(4-species, flicker, rotor classes; 12/28 new-cell first-touches), mutate
CLIMBS within cells (17 holders, both top scores). share_chan stays fragile
(5/24 funnel-pass — same-vacuum lesson from evolve/ holds).

## Yield + cost (M1 Max, shared with sibling load; 10 cores)
179 screens + 16 confirms + 1 smoke = 196 logged evals, 47.7 core-h total.
Per gen (24 children): 13-25 ks sim wall = 1.5-2.5 h on 4 workers.
Funnel reject rate 13% (24/180 fail_g0a) at ~0 cost; 3 size_cap (breeder
bug, fixed gen-4); 5 all_dead; 0 battery crashes after the early-death guard.
Evals per discovery: 35 evals -> 14 cells (g0 bootstrap); gens 1-6:
144 evals -> 21 new cells + 24 improvements = 3.2 evals/archive event.

## Pod-scaled plan (for controller; 20+ generations)
Local per-child cost: median ~850 core-s (T=2500 screen incl. battery).
On one 32-vCPU CPU pod (prime CLI): pop 48/gen x 20 gens = 960 screens
= ~227 core-h => ~7-8 h wall; + 60 confirms ~ 42 core-h. TOTAL ~1 pod-day.
RECOMMENDED changes at scale (to break the g6 plateau):
  a. immigration: 20% fresh funnel-passed random genomes per gen;
  b. descriptor expansion: add n_act and a C5-memory-grade axis to the key
     (current 4-tuple saturates at ~40 reachable cells);
  c. raise MAX_FIELDS 12->14 with cost-aware sharding (4-act merges were
     the discovery engine but 3 hit the cap);
  d. multi-seed screens (2 seeds/child) for elites before archive insert —
     kills seed-luck holders like g0_jit_11's 66.5->51.6.

## Honest negatives + limits
- g6 added 0 new cells and mean I flatlined: THIS seed family + operator set
  saturates at ~35 cells / I~75 under local budget. Not a failed loop — a
  measured convergence point; scale/immigration is the tested remedy.
- Interest scalar is exploitable by liquid+memory+mobile combos: 8 of top 10
  holders are *|mobile|liquid|m1 variants. MAP-Elites diversity keying
  contained Goodhart collapse (still/frozen/rotor/flicker cells retained),
  but a v2 metric should consider novelty pressure inside cells.
- Confirm coverage: 16/33 non-GT holders; low cells (<I 35) unconfirmed.
- Single-seed screens: cell labels near drift/still and liquid/frozen
  boundaries can flip between seeds (2 observed cases).
- No new physics CLAIMED beyond metric-space discovery: ds3_017/ds3_014
  deserve mechanism autopsies (why does the slow-tanh coupling of a BFIELD
  mutant + dead XV jitter triple the score?) before world-catalog entry.

## Files (probes/blobs/l0/deepsearch/)
ds_lib.py (eval+archive), gen.py (driver), worker.py, seeds/ (8 elites),
jobs/ (7 gens + 2 confirm rounds), results.json (196 rows, full lineage),
archive.json (35 cells + confirm fields), data/state.json (gen stats),
runs/*.npz (164 raw runs), README.md, SCORECARD.md (this file).
