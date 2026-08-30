# ASSAY_V2_API — contract for evolve-v2 (LOCKED 2026-02-25)

Status: LOCKED (metrics_v2.py + assay_v2.py frozen after seeds-1-2 validation;
seed-3 out-of-sample confirms; see VALIDATION_V2.md).

## a) Entrypoint: GENOME-IN. The assay owns sim + adaptive-T internally.
```python
sys.path.insert(0, ".../probes/blobs/l0/complexity")
import assay_v2
out = assay_v2.run_assay(genome_dict, seed=1, L=128.0,
                         workers=2, results_path=None,  # None = no row append
                         tag="ds2_007", save_npz=None)  # path or None
```
- Runs soup chunks T0=2500 with continuation (soup_sim_v2, numerics verbatim,
  bitwise-identical to one long run) and decides EXTEND(x2)/STOP after each
  chunk; cap T=20000.
- You stop calling soup_sim yourself: pass genome+seed only.
- `results_path`: pass your results_v2.json to get an appended row
  (kind="assay_v2"); default None so nothing collides.
- Recompute path also exists: `metrics_v2.full_battery(rec, genome=g)` scores
  any saved soup record (genome optional; without it, genome-coupling gates
  degrade gracefully to behavior-only).

## b) Return dict (top-level keys)
- `interest` float — THE scalar (v2 weights, components C1..C8).
- `C` dict — C1_popdyn, C2_timescale, C3_motion, C4_graph, C5_memory,
  C6_ecology, C7_roles, C8_succession (all [0,1]).
- `D` dict — full descriptors d1..d7 (v1-compatible d1-d6 layout preserved;
  new fields listed in (c); d7 = interaction matrix block).
- `horizon` dict — T_used, why_stopped ("static"|"converged"|"cap"|"blowup"|
  "all_dead"), n_extensions, criteria fired per decision point,
  interest_trajectory [(T, interest), ...].
- `flags` dict — box_limit (bool, max organism span > 0.6*L), box_span_frac.
- `summary` — lean row (assay_v2.lean_summary(out)) sized for archive storage.

## c) Cell-key fields intended for MAP-Elites (all inside out["D"]/out["C"])
- `D["d7"]["n_species_int"]` float — interaction-weighted species count
  (M1 gate: alive species weighted by max pairwise interaction strength;
  passengers ~0; first alive species free, so min 1.0 when anything lives;
  direct genome path (K or bilinear) w=1.0, mediated shared-channel w=0.5,
  behavioral |xcorr|*3 capped 1). Suggested bin: round() capped at 4 -> {1..4}.
- `D["d1"]["org_model"]` — population-model class fit on ORGANISM count
  (connected structures, not segments): constant|relaxation|switch|oscillator
  (+ `org_growth` bool: organisms grew >=1.5x). Suggested bin: growth?
  "grow" : org_model.
- `D["d1"]["n_stages"]` int — M5 succession: count of well-separated
  (>=500tu) per-species saturation epochs. Suggested bin: {0-1, 2, >=3}.
- `D["d1"]["turnover_best"]` — best sliding 2000tu-window turnover (adaptive-T
  safe; plain `turnover` is the v1 whole-window rate).
- motion/phase: unchanged v1 semantics (`D["d4"]["moving_frac"]`,
  `D["d5"]["winding_max"]`, `D["d5"]["phase"]`) — your existing
  motion_class() keeps working.
- `D["d6"]["mem_grade"]` — 0 none | 1 write-only structure | 2 READ memory
  (K-column or bilinear-vertex read, the ds3_014 lesson). Suggested bin as-is.
- Both counts exposed: `D["d1"]["n_end"]` (blobs/segments, v1-compat) and
  `D["d1"]["n_org_end"]` (organisms).

## d) Adaptive-T: YES, assay decides internally.
Ladder: 2500 -> 5000 -> 10000 -> 20000 (x2, hard cap 20000; chunks are
continuations, no re-simulation). EXTEND iff ANY of:
 (a) slow channel (tau>=30) still trending (charging/discharging) over last
     25% window;
 (b) any species organism-count trend nonzero (robust slope) over last 25%;
 (c) coarse-observable ACF not converged (tau_slow > window/5) — this
     criterion alone grants AT MOST ONE doubling (stationary-slow worlds must
     stay cheap; trend criteria (a,b) can chain to cap).
Score is computed at final T; `horizon` explains the decision trail.
Blowup/all-dead exit immediately with v1 semantics.

## Multi-seed / confirm runs: floor t0 at the incumbent's T_used
Different seeds fire the extend criteria at different chunk boundaries; a
confirm seed run at default t0=2500 can stop "static" BEFORE the behavior
that made seed 1 extend has assembled (live example from evolve-v2: ds3_014
seed1 74.2@5000; naive seed2 37.1@2500 "static"; with t0 floored at the
incumbent's T_used it confirms at 49.5). Rule for confirm/elite multi-seed
evals: pass `t0=<incumbent horizon.T_used>` to run_assay (kwarg already in
the locked signature). Scores at different T_used are comparable BY DESIGN
(windowed rate metrics + structure metrics on full record), but the DECISION
to stop must not be made on a shorter window than the incumbent earned.

## Error contract: catch exceptions on all_dead-before-burn records
Root cause (verified): a subcritical genome (alive fields, ZERO blobs ever)
takes soup_sim's all_dead exit at ~405tu < BURN=500, so the post-burn window
is EMPTY and locked metrics_v1.d2_timescales crashes (np.polyfit "expected
non-empty vector") inside full_battery — run_assay propagates it. A
full-length zero-blob record does NOT crash (scores 0.0). Hits ~1-5% of
random immigrants (evolve-v2 measurement). Callers must wrap run_assay in
try/except and score such candidates status="no_blobs", interest 0 (the
evolve-v2 adapter does this). A guard belongs in metrics_v3, not in a locked
module.

## Cost expectations (M1 Max, solo)
Static/boring worlds: one chunk = v1 T2500 cost + ~20-40s battery per decision.
Median over static ground truths validated <= 1.5x v1 T2500 (a lock gate).
Rich growing worlds pay for what they show (ds3_014 -> >=10000tu by design).
