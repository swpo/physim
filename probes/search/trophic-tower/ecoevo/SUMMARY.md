# ECO-EVOLUTIONARY TOWER — heritable predator attack G on the certified teacup
**Verdict: L4 EXISTS as a robust evolutionary attractor with two clean response
curves, BUT the 4-layer tower FAILS G1 — maintained genotype variance destroys the
L1–L3 teacup coherence underneath it. Primary deliverable is this mapped negative.**

## Physics added (ecoevo_core.py)
- Genotype field G (per cell): predator intake f2 = (G·a2)H / (1+(G·b2)H) — G scales
  ATTACK RATE at fixed handling time (diminishing returns at high G).
- ONE linear price (E2-rent style): d2_eff = d2 + c·(G−1). G=1 reproduces certified TC*.
- Particulate copy inheritance: births add biomass to P and Q=P·G with the LOCAL
  parental G (no averaging at reproduction); mixing is biomass-weighted transport of
  Q=P·G; mutation = per-cell random walk (step m per sqrt(tu), every 10 ticks),
  clipped to [0.25, 4]. Demographic noise carries local genotype. Selection is NOT
  coded — only differential biomass growth. Base ecology = certified TC*.

## What we found (results.json: 64 entries, 63 runs + gradient map; all logged)
### 1. Emergent selection & interior attractor G* (evolution of restraint)
- <G> relaxes to the SAME G* from above and below (e1: G0=1.5 vs 0.6 agree to ±0.001
  at all 8 (c,m) points) and from G0=3.0 and 0.3. No runaway, no freezing.
- Frozen-gradient map (36 uniform-G ecologies, biomass-weighted marginal invasion
  gradient): s(G) crosses zero at finite G, moving down with price c — independent
  confirmation that the attractor is eco-feedback-made, not an artifact.
- Realized G* is a mutation-selection balance: G*(m) = 0.50→0.59→0.76→1.06 for
  m=0.06→0.25 (greedy mutants transiently boom in H-rich phases; larger mutational
  variance samples them more, pulling the biomass-weighted mean up).

### 2. G3 response curves — both smooth and monotone (PASS)
- **G* vs price c** (m=0.15, 2 seeds, seed spread ±0.02):
  c: 0.005→0.774, 0.0075→0.756, 0.010→0.742, 0.0125→0.729, 0.015→0.719.
  Same monotone-decreasing shape independently at m=0.1 and m=0.2 (e1 grid).
- **G* vs mutation m** (c=0.0075, 2 seeds): 0.06→0.495, 0.1→0.594, 0.15→0.756,
  0.25→1.056. Monotone increasing.
- Variance maintenance (E-track gate): sd(G) ≈ 1.3·m (0.084…0.316), stable over
  400k-tick runs — mutation-selection balance holds; evolution never freezes (PASS).

### 3. L4 timescale & top law (MARGINAL)
- Displacement protocol (G0=1.5 → G*≈0.75, c=0.0075, m=0.15, 400k ticks = 20k tu):
  tau4 = 1664, 1626, 1870 tu across 3 seeds (t_conv ≈ 3600–4300 tu),
  sep(L4/L3) = tau4/T3 ≈ 9–11x (PASS ≥5x). From below the approach is fast and
  asymmetric (tau ≈ 60–90 tu) — selection against prudence is much stronger than
  against greed; the "slow layer" statement holds only for the greedy side.
- Simple-law fit quality on log|gap|: r2 = 0.949, 0.849, 0.763 (3 seeds from above),
  0.936 (from below): 2–3/4 at the 0.85 bar, median 0.849 — **G2-L4 borderline FAIL
  by the strict gate**, though the attractor itself is extremely reproducible.
- No entrainment to T3: plateau <G> wander has no ACF peak at T3 (entrained=False in
  all runs; detrended cross-corr |r|≈0.5 at ~100-tu lag but no locked period).

### 4. THE HEADLINE NEGATIVE: evolution dissolves the eco tower below it
- AUDIT-CORRECTED boundary law (results_boundary.json: G0=1.0, c=0.0075, 120k
  ticks, 3 seeds per m; coherent = ecoG1 AND ecoG2):

  | m | sd(G) maintained | coherent | median top r2 |
  |---|---|---|---|
  | 0.02 | 0.028 | 3/3 | 0.96 |
  | 0.04 | 0.057 | 3/3 | 0.95 |
  | 0.06 | 0.086 | 0/3 | 0.77 |
  | 0.09 | 0.125 | 0/3 | 0.72 |
  | 0.12 | 0.157 | 0/3 | 0.62 |
  | 0.15 | 0.194 | 0/3 | 0.61 |

  **The law: the clock survives sd(G) ≤ ~0.06 and dissolves above sd(G)* ≈ 0.07
  (sharp transition between 0.057 and 0.086; top-law r2 decays monotonically with
  sd(G) past the boundary).** At the boundary <G> is still in-window (0.87–0.97),
  so this is a pure variance effect, not a mean shift. Strips: dissolution_boundary.png.
- CORRECTION of the earlier claim "even m=0.02 breaks it": that run started at
  G0=1.5 (mean genotype outside the frozen-G coherent window) — a mean-outside-
  window confound, not variance. At G0=1.0 the m=0.02 and m=0.04 towers are fully
  coherent WITH ongoing evolution (audit seed 71 + our 3 seeds agree). There IS a
  narrow coexistence regime: 4 gated eco layers + live L4 at sd(G) ≤ 0.06 — but the
  interesting evolutionary dynamics (fast selection, tau4 in the thousands of tu,
  strong G3 curves) live at m ≥ 0.1, beyond the dissolution boundary.
- Mechanism (frozen-G scan): the teacup is only coherent for uniform G in
  ≈[0.75, 1.2] (T3 shifts 140→190 across it). Standing spatial variance puts
  neighborhoods at different effective (attack, rent); past sd(G)* local cycles
  detune and the global P clock decoheres. High-variance evolution and macro
  coherence remain incompatible; low-variance evolution coexists with the clock.
- Sweet-spot attempts failed and are logged: rho=0.030 (wider eco margin), logmut
  (multiplicative mutation — runs to G*≈3.2, worse), G*≈1.0 tuning via (c=0.005,
  m=0.22) — all still ecoG1=False.

### 5. No evolutionary suicide anywhere swept
- c ≤ 0.03, m ≤ 0.25, G0 ∈ [0.3, 3]: predators never went extinct. Max-greed start
  G0=3.0 dips meanP to 0.022 then evolves down and RECOVERS (evolutionary rescue).
- c=0 (no price): G* ≈ 0.83–1.07, bounded — the saturating functional response is an
  intrinsic brake on greed (honest caveat: attack-rate evolution at fixed handling
  time cannot runaway; a handling-time or conversion-efficiency genotype might).

## Gate scorecard (4-layer world)
- G1 (4 layers, adjacent ≥5x): **FAIL at the interesting-evolution regime**
  (m ≥ 0.06: eco layers collapse, 0/12 coherent). Coexistence exists at m ≤ 0.04
  (3/3 + 3/3 coherent with live L4), but there tau4 was not separately certified
  (selection is ~sd(G)^2-slow: at m=0.04 the G0=1.5 displacement would need
  >~50k tu runs — beyond G5 budget; recorded as untested, not failed).
- G2 on <G>: **MARGINAL FAIL** — relaxation, r2 median 0.849 (2–3/4 seeds ≥0.85).
- G3: **PASS** — two response curves (G* vs c, G* vs m), both monotone, tight seeds.
- G4: attractor G* robust (4/4 seeds ±0.01; both directions; rho variant) — but the
  gated 4-layer claim fails at G1, so G4 is moot for the tower claim.
- G5: **PASS** — 60–190 s per candidate (400k ticks ≈ 3.3 min worst case), L=64.

## Files
ecoevo_core.py (G-field engine + L4 metrics), gradient_scan.py + gradient_map.json,
sweep_e1/e2/e4/frozenG/rescue/tau4/sweet.py + logs, probe1/diag1, results.json
(everything incl. failures), strips/: response_curves_evo.png, tau4_relaxation.png,
diag_evolved_state.png, diag_RHPG.png, sweet_RHPG.png. Round-1 tower unchanged
in parent dir (frozen-G control reproduces it).

## One-line story
Evolution on this teacup finds a beautiful, price-responsive attractor of restraint —
and the clock beneath it survives only while heritable variance stays below
sd(G)* ≈ 0.07: slow, quiet evolution coexists with the tower; fast, high-variance
evolution dissolves the very oscillator it rides on.
