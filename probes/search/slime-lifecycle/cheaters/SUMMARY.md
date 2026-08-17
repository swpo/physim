# CHEATERS — social evolution on the slime lifecycle (Strassmann/Queller problem)

## Verdict (honest, mixed)
The heritable-cooperativeness layer WORKS mechanistically (particulate strain
bins, signal cost, shared benefit, zero fitness functions) and produces the
classic social-evolution phenomenology: **tragedy of the commons, its
cost-dependence, Hamilton-assortment rescue, bistable cooperation, and
mutation-variance balance**. But the hoped-for *stable-polymorphism-with-
clean-relaxation* L4 (regime a as a smooth c*(lam) curve) is **drift-dominated
and bistable** at this world size (N_e ~ 15 mounds), and the evolutionary-
rescue oscillator (regime b) **does not occur** in 61 runs. Gates: G2/G3/G5
pass on the collapse dynamics; G1 (sep>=5x) passes at the canonical point but
narrows at high cost; G4 passes for the lifecycle and for the *regime*, not
for a fixed c*.

## Mechanism added to certified c30 (no fitness function anywhere)
- K=9-11 strain bins c_k in [0,1]; VK[k] biomass fields. Growth at a site is
  allocated ∝ current local composition (clonal copying); mutation mu moves a
  fraction of NEW growth to adjacent bins. NO averaging -> no blending.
- SIGNAL COST: sites with active emitters burn strain biomass exp(-lam_c*c_k)
  per firing tick. Emission strength ∝ cooperator biomass only (Vc): all-
  cheater mounds go silent -> no waves -> no aggregation (public good).
- SHARED BENEFIT: density protection/chemotaxis/dispersal trait-blind.
- ASSORTMENT PHYSICS (required — see negatives): local germination dispersal
  (chi_d=6, Dv_germ=0.14, T_wake=300 instead of the certified global blast)
  + founder bottleneck: each waking mound resamples its composition once from
  Dirichlet(N_f*share), N_f=1.5 (spore-head founder sampling, strain-blind).

## Layer stack at canonical point (lam_c=0.002, mu=0.01)
| layer | variable | timescale | sep |
|---|---|---|---|
| L1 relay waves | fires rhythm | 26 | — |
| L2 aggregation | aggm rise | 220 | 8.5 |
| L3 lifecycle | aggm/hf square wave | 2250-2400 | 10 |
| L4 cooperativeness | <c>(t) relaxation (tragedy) | tau 11k-53k (4 seeds) | 4.7-23x, med 15.6x |
Tick -> L4 span ~ 4 decades. L4 never entrains to L3 (per-cycle wiggle 0.002-
0.02 << collapse amplitude 0.4; wiggle is phasic with famine, as expected —
cost is paid during famines).

## G2 (top law on <c>)
Tragedy collapse = clean relaxation: free-exp fits on collapse windows,
9 fits (lam 0.002-0.004): r2 = 0.70-0.93, median 0.90 (7/9 >= 0.85), c_inf ~
0.0-0.05. In the polymorphic band (jittered canonical) <c> holds a noisy
plateau c* 0.27-0.50 (fit_full: relaxation/constant; no oscillation).

## G3 response curves (both monotone where selection dominates drift)
**(a) collapse half-time vs signal cost** (uniform init, mu=0.01, 3-4 seeds):
| lam_c | 0.002 | 0.003 | 0.004 | 0.008 |
|---|---|---|---|---|
| t_half med | 27725 | 9850 | 8650 | 4200 |
lam*t_half ~ 30-55e-3 (approx 1/lam). Below lam=0.002 drift dominates
(N_e ~ 15 mounds): fate bistable, direction not cost-set — reported, not
counted. **(b) equilibrium sd(c)* vs mutation** (c=1 init, lam=0.002):
| mu | 0.001 | 0.003 | 0.01 | 0.03 | 0.1 |
|---|---|---|---|---|---|
| sd(c)* med | 0.0028 | 0.0048 | 0.0254 | 0.0345 | 0.0452 |
Monotone over 2 decades (~mu^0.6). Variance maintained (sd>0) in every run:
mutation-selection-drift balance verified.

## G4
- Lifecycle robustness: 4/4 jittered runs (all 15 params ±10%, seeds 10-13,
  100k) keep the L3 lifecycle cycling. 4/4 canonical seeds reproduce tragedy
  with t_half 11k-38k.
- L4 caveat: jitter mostly lands on the polymorphic side of the boundary
  (c* 0.27-0.50) while the exact canonical point is tragedy-bound — the
  canonical lam_c=0.002 sits NEAR the boundary. Robust claims: (i) regime
  map, (ii) tragedy law in the selection band, (iii) polymorphism under
  jitter. NOT robust: a fixed c* value.

## Tragedy boundary & rescue (the main scientific deliverables)
- Bands at mu=0.01, canonical movement: lam <= 0.001 drift/bistable
  (cooperative-frozen or drift-collapse, seed-dependent) | lam >= 0.002
  tragedy (all seeds collapse, speed ~ 1/lam).
- Tragedy does NOT kill L3 outright: p_spont pacemakers keep weak mounds
  nucleating, but V drops 3-10x and most seeds end non-aggregating (bare
  R-V relaxation) — "sociality lost, ecology crippled".
- **Assortment is load-bearing (Hamilton verified in the negative)**: with
  the certified c30 global dispersal, cooperation ALWAYS collapses (c* ->
  0.09-0.18 even at lam=0.0005). Local dispersal + founder bottleneck is the
  minimal physics that lets cost-bearing signalers persist at all.
- **Bistability**: at lam=0.002, mu=0.03, hi-assortment init holds c*=0.93
  for 100k while lo-init collapses to 0.13 — threshold public good.

## Negative results (first-class)
1. NO evolutionary-rescue oscillator (regime b) anywhere in 61 runs: after
   collapse, too few mounds and too little variance for cooperator re-bloom;
   rescue would need larger L (bigger mound population) or faster variance
   regeneration.
2. Site-level founder resampling (first design) = too much drift: c*(lam)
   non-monotone; mound-level single-draw sampling is the working design.
3. 30k-tick d<c>/dt slope assays cannot resolve selection below lam~0.002.
4. K=1 emission-calibration control confirmed: <c>=0.5 world emits like
   certified c30 after a_s 1.2->2.4, a_a 0.05->0.10 rescale.

## Files
slime_evo.py (engine), probe_long.py / assay_rates.py / run_assays.sh
(drivers), measure_evo.py, results.json (61 runs classified), strips/
L4_panels.png (tragedy/polymorphism/bistable-hold/no-assortment) and
G3_curves.png, series_*.npz + assay_*.npz (raw).

## Engine-integration note
Adds K biomass planes + 2 params (lam_c, mu) + 3 assortment params (N_f,
chi_d/Dv_germ already in c30's family). Cost ~2x c30 at K=9 (1.3 ms/tick at
64^2). Real-world analogue: Dictyostelium chimeras & csA/fbxA cheater
strains (Strassmann-Queller); named honestly.
