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
- In ALL 45 evolving runs (m>0), the certified L3 oscillator degrades to an
  irregular switch: eco top fit = switch in 45/45, median r2 0.63 (was 0.93–0.97
  frozen); L2 fast layer measurable in only 2/45; ecoG1 = False in 45/45.
- Even m=0.02 (sdG≈0.03) already breaks ecoG1; m=0 exactly restores the full
  certified tower (control: frozen G=1.0 run → oscillator r2 0.96, ecoG1+ecoG2 PASS).
- Mechanism (supported by the frozen-G scan): the teacup is only coherent for
  uniform G in ≈[0.75, 1.2] (T3 shifts 140→190 across it; outside, no clean
  oscillator). Standing spatial variance sd(G) ≥ ~0.03 puts different neighborhoods
  at different effective (attack, rent) — local cycles detune and the global P
  clock decoheres. **Variance maintenance (needed for evolution to work) and macro
  coherence (needed for the L3 clock) are mutually exclusive in this physics.**
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
- G1 (4 layers, adjacent ≥5x): **FAIL** — L4/L3 separation is 9–11x, but L1–L3
  collapse under evolving G (ecoG1 false in every m>0 run).
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
and pays for it by dissolving the very population clock it rides on: heritable
variance is the currency of adaptation and the poison of macro coherence.
