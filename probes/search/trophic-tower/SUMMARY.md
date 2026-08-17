# TROPHIC TOWER — R -> H -> P reaction–diffusion food chain
**Verdict: PASS (all gates G1–G5).** A 3-level Rosenzweig–MacArthur / Hastings–Powell
chain on a 64x64 torus, searched in Hopf-anchored theory coordinates, has a robust
window where the world self-organizes into a **three-timescale tower** whose top law
is a clean global predator oscillator (r2 ~ 0.93–0.97) with period set by the
predator's metabolic price: **T3 ≈ 5.8 / rho** (T3·rho = 5.65–5.94 across the sweep).

## Mechanism
- dR/dt = R(1−R) − a1·R/(1+b1·R)·H + DR·lap(R)   (logistic grass)
- dH/dt = [a1·R/(1+b1·R) − d1]·H − a2·H/(1+b2·H)·P + DH·lap(H)  (grazer)
- dP/dt = [a2·H/(1+b2·H) − d2]·P + DP·lap(P)   (predator)
- small demographic noise nu·sqrt(X)·xi on H,P every 10 ticks; floor 1e-9 (rare-immigration);
  Euler dt=0.05, 1 tick = 0.05 tu. No scripted events, no imposed clock anywhere.
The R–H pair sits past its Hopf point (mu1<1) -> fast local limit cycle (L1/L2);
the P level rides on the time-AVERAGED H like a slow LV mode -> slow global cycle (L3).
Space + saturation keep the fast layer desynchronized into patches instead of a
global flash (mean-field 0-D comparison at the same params: switch r2=0.76, ragged
q=0.76 — the lattice CLEANS the top law, it does not merely copy the ODE).

## Theory coordinates (what we swept, 9 dims)
sigma1=b1 (grazer saturation), mu1=R*/R_Hopf (<1 = past Hopf), d1 (grazer turnover),
sigma2=b2, eta2=H*/H_free (predator efficiency), rho=d2/d1 (timescale ratio),
DH, Delta=DP/DH (pursuit ratio), nu (demographic noise).

## Best candidate TC* (tcstar.json)
sigma1=4.5, mu1=0.4, d1=0.4, sigma2=2.0, eta2=0.44, rho=0.034, DH=0.05, Delta=4, nu=0.03
(raw: a1=4.37 b1=4.5 d1=0.4 a2=0.121 b2=2.0 d2=0.0136 DR=0.01 DH=0.05 DP=0.2)

## Hierarchy (layer -> variable -> scale), measured at TC*, L=64
| layer | variable | scale | how measured |
|---|---|---|---|
| L1 fast | pixel R falling edge (front transit), front width ~3 px | tau1 ≈ 4.9 tu | 70->30% crossing stats on 8 probe pixels |
| L2 meso | 4x4-block H boom–bust; patch mosaic lambda ≈ 26–28 px | T2 ≈ 26 tu | band-limited ACF period per block (24 blocks, frac ≥ 0.5) |
| L3 top | mean P over map (global) | T3 ≈ 166 tu | compact_top_fit oscillator |
Separations: T2/tau1 = 5.2–5.7x, T3/T2 = 6.4x (both ≥ 5x); product tau1->T3 = 34x.
Patchiness: spatial CV(H) ≈ 0.5–0.6, ~7–14 patches. n_cycles ≈ 11 in a 56k-tick run.

## Gate results
- **G1 PASS**: 3 measurable layers, adjacent separations ≥5x (5.2–5.7 and 6.4).
- **G2 PASS**: top fit oscillator r2 = 0.93–0.97, n_cycles ≈ 11 (≥5), q ≈ 0.9.
- **G3 PASS**: response curve of T3 vs rho (5 values x 2 seeds), smooth & monotone:
  rho: 0.026->224, 0.030->194, 0.034->166, 0.038->155, 0.042->141 tu; fit T3 ∝ rho^-0.95
  (inverse law, T3·rho ≈ 5.8, i.e. period ≈ 5.8 predator mean lifetimes; ODE analogy
  says slow LV frequency ~ sqrt(d2·gain), so a slightly sub-linear exponent is honest).
  Secondary curve: T3 rises with eta2 (163->183 over 0.40->0.46), monotone.
- **G4 PASS**: seeds 4/4 BOTH at TC*; jitter ±10% on all 9 searched params:
  10/12 BOTH across two independent 6-draw batches (failures degrade to switch-top,
  never explode); L=96 2/2 PASS with identical T3.
- **G5 PASS**: 56k ticks @ L=64 = 2800 tu ≈ 11 full top cycles; runtime ~9 s/candidate
  on one core (report: 6–15 s incl. measurement; far under 3 min).

## Bonus scoring
- Patch-size distribution: alpha ≈ 1.4–1.5 over **2.6–3.2 decades** (n≈2–6k patches,
  KS 0.09–0.13) — genuine broadband mosaic at L2 (crude MLE; not a criticality claim).
- Visual drama: three-color pursuit mosaics; space–time plots show fast traveling
  H-waves nested inside slow global P-breathing (strips/tcstar_*.png).
- Real-world analogue: lynx–hare / plankton bloom cycles (honest: parameters not
  calibrated to data; analogy is structural).

## Honest negatives / caveats (deliverables)
1. **Most of the searched volume fails.** Stage-1 (36 cands, d1=0.6 corner): fast and
   slow layers merge (T3/T2 = 1); the "teacup" needs rho ≤ ~0.05 AND eta2 in a narrow
   band (~0.42–0.48 at sigma1=4.5). Below eta2≈0.42 the H-min dives (extinction risk);
   above ~0.48 the slow mode loses coherence (switch-top, r2~0.7).
2. **Full 3-frequency teacup (distinct L2 patch clock at every pixel all the time) is
   partially intermittent**: T2 block-cycle fraction ~0.5–0.8, fast amplitude ~60–70%
   of block variance. We measure T2 as median over blocks; single-block stats are noisy.
3. rho ≥ 0.05 with eta2≈0.45: slow mode swallows the fast one (single global cycle,
   G1 fails — the s1/s3 sweeps document this ridge).
4. sigma2 ≥ 2.5 at the good spot kills the slow coherence (deeper predator saturation
   -> boom–bust switch, not oscillator). sigma2=2.0 is part of the recipe.
5. Warm start matters (settle-order lesson): cold random inits spend ~700 tu on a
   predator ramp; we ODE-warm-start (same physics) and still cut the first 35%.
6. nu≈0.02–0.03 needed: nu ≤ 0.01 lets the fast layer resynchronize globally
   (switch-top); nu ≥ 0.05 blurs L2. Demographic-noise window is real but forgiving.
7. Anti-imposition check: no top-level clock exists in the code; T3 emerges and obeys
   T3 ∝ rho^-0.95 while T2 (~26 tu) and tau1 (~4.9 tu) stay nearly fixed — three
   independently moving scales, computed not imposed.

## Engine-integration sketch
World needs: 3 float fields (R,H,P) on the existing torus lattice; per-field diffusion
(DR,DH,DP); local Holling-II couplings (4 mults, 2 divs per cell); sqrt-noise on H,P;
floor+cap clamps. Params: a1,b1,d1,a2,b2,d2,DR,DH,DP,nu (10 scalars). Natural film
channels: (R,H,P) -> (G,B,R). Probe hooks: mean fields, 4x4 block means, patch labels.

## Files
- trophic_core.py (engine + all metrics), sweep_stage{1,1b,2,3,4,5,6}.py, sweep_map.py,
  certify{,2,3}.py, results.json (292 runs, 215 unique candidates, failures included),
  results_*.json per stage, strips/*.png, tcstar.json.
