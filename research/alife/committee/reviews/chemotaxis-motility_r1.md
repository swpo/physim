# Review: chemotaxis-motility, sprint 1 (2026-10-24)

**Decision: CONTINUE** (promise 7/10). **Headline:** a slow self-secreted repellent gives the lab's only *spontaneous* populations of self-propelled individuals. kstrail is a numerically validated L4b[L2], and ecology reaches L5[L2] with low confidence, because the effect of predation on prey changed sign in matched reruns. Reproduction is the next rung: make a fed swimmer divide.

## Consensus

| world | judged rung | conf. | key observation | pack |
|---|---|---|---|---|
| kstrail | **L4b[L2]**; L3 Weak | high | seed1 tracks.png #15: one polar crescent from t≈132 to 600, ~14.7 BL, straightness 0.99. The chi_h=0 ablation gives static spots. Passes the dt/2 pack and the skeptic's 2x-resolution rerun (body size and speed within ~10%), with no heading lock. Formation reproduces on seed 11 (3 judges). The swimmer phase coarsens away by t=1800. | threads/chemotaxis-motility/packs/kstrail |
| ecology | **L5[L2]** | low | Prey-predator pairs in every frame after t≈220 in 4 seeds, pairing 0.93-0.96 against null 0.30-0.37. With k=0 the predators fall 93-95% (seed 0 at 160², seed 11 at 128²). At matched controls the prey do *better* with predators (-7% vs -35% total; 12.4 vs 8.3 bodies). The report's "-24%" is unmatched. The predator is an obligate escort or parasite, not a demonstrated predator. There are no cycles. | threads/chemotaxis-motility/packs/ecology |
| toxforage | **L4b[L2]**; L4c Weak (near-Supported); L4a Weak | medium | Biologist's fork (seed 11, 128²): with n=0 at t=500, all bodies are dead by +200 t; with kd=0 they form one sea by +300 t. This is individual-level dependence plus size bounding, but on one seed only (capped Weak). With r=0 the population thins to 4 swimmers, which live on residual food. | threads/chemotaxis-motility/packs/toxforage_abl_r0 |
| pursuit | **L4b[L2]**; L5 Weak | high | Chaser-in-the-concave-rear composites, contact 0.76-0.91 against null 0.27-0.31. A clean 2x2 ablation shows that pursuit binds and evasion shapes the bond. Species are conserved, so populations cannot change. | threads/chemotaxis-motility/packs/pursuit |

## Judges

**Biologist (promise 7).** Saw a genuine self-propelled body with front-back polarity created by its own secretion: a chemical comet, not a cell. All three candidates repeat the Orbium-control rung, but the bodies form spontaneously. The biologist's starvation fork (`judge-scratch/.../starve_toxforage.png`) is the strongest new evidence this round. I examined it: three rows show the fed control, a vanishing starved population, and a toxin-free sea. I upheld the *observation* but kept L4c at Weak, because the rubric caps single-seed evidence at Weak from L3 up and the skeptic's r=0 objection remains (residual food sustains swimmers). Three seeds of the same fork would settle it. The biologist granted ecology L5 as "grazing by an obligate rider".

**Skeptic (promise 6).** Did the most valuable rerun. kstrail at 2x resolution kept the route, body size and speed, and headings show no grid lock (<cos 4θ> = -0.20±0.12). This makes kstrail the best-validated motility result in the lab. Their matched seed-11 ecology pair (k=0.2 vs k=0) reversed the sign of the prey effect. I checked their FACTS: prey totals were -6.7% with predation and -35% without. The curator found the same independently. The skeptic rated L5 Weak because predator dependence is built into the equations. I side with the biologist and curator. The rubric's L5 text is met: a repeatable binding interaction changes both populations, across 2 seeds and 2 grids. Confidence is low, the rung is provisional on the decomposition below, and the "predation" label is withdrawn.

**Curator (promise 7).** Rated this the lab's only source of spontaneous motile *populations*, with ecology the most PhySim-ready world (field, bodies, pairs, species). Novelty is moderate. Self-trail propulsion is the known drift bifurcation of spots with a slow inhibitor (Krischer & Mikhailov 1994), and non-reciprocal chaser-fleer pairs (Soto & Golestanian 2014; Agudo-Canalejo & Golestanian 2019) and pursuit-evasion (Tsyganov et al. 2003) are also known. None of these is in LITERATURE.md. Beyond-diffusion leverage is still unshown for kstrail: no Laplacian-only control was run.

## Next sprint

**Main experiment: make a fed trail swimmer reproduce (L6).**
(a) Run a toxforage life-history assay. Seed one crescent at 256² on uniform food, sweep r over 0.03, 0.06, 0.1 and 0.2, and run for at least 2000 t with a per-body budget (uptake vs toxin loss). Report the outcome: steady size, division, or bloat.
(b) Your negatives predict bloat. If so, add a fission route and ablate it as the control. The preferred route is active-droplets' core starvation: make growth need a nutrient whose penetration length is smaller than the body radius, so a grown body hollows into the ring you already see and ruptures into two crescents. An AMB+ or nonlocal area constraint is the fallback.
(c) Pass criteria, from noise on 3 seeds, using prey-channel lineage: at least 2 generations of crescent → 2 crescents, offspring within ~30% of the parent's size, and no divisions in the ablated control.

**Secondary goals**
1. **Ecology decomposition** on one grid (192²), t=1000, 3 seeds, with species-aware tracking. Arms: full; k=0; a non-consuming escort (k=0, predator death off); chi_y=0; prey alone. This settles the sign of the effect on prey and whether binding is required for predator persistence.
2. **L4c:** run the n=0 starvation fork as labkit packs on 3 seeds, plus one dt/2 check of a kinetic world. Note whether clipping rho changes mass.
3. **Beyond-diffusion control:** a Laplacian-only slow-inhibitor RD with the same timescales. Do travelling spots form from noise, and do they bind? Add the four references above to LITERATURE §2.6.

Tooling allowance is minimal: per-channel `matter`, time from the run's own dt, and damage of a median body. Do not spend the sprint on labkit.

## Cross-pollination

- **Out:**
  - **autopoiesis:** a van Leer MUSCL face flux plus body radius ≥6 px fixed diagonal snapping here, and phase_swim reports lattice-locked headings.
  - **active-droplets:** add a slow self-repellent to the dividing ad5 droplets to get motile heritable individuals.
  - **lenia-multichannel and flow-lenia:** non-reciprocal cross-taxis as a predation channel between kinds.
- **In:**
  - core-starvation fission (active-droplets `ad1-fuel`; autopoiesis `phase_swimdiv`);
  - maintenance cost for cycles (lenia-multichannel `mcfd-MIRd`);
  - Hill-gated uptake (flow-lenia `fl_forager`).

## Rubric issues

1. **L4c** does not say *which* ablation counts. Removing a supply (r=0) is not removing a resource that is already there. Proposal: an abrupt removal at a fork, with the fed control alongside, death of individuals rather than thinning of the population, and at least 2 seeds.
2. **L5** "changes population dynamics" needs a *matched* ablation (same grid, duration and seeds, at least 2 seeds) and the sign of the effect on each partner. Here an unmatched comparison gave the wrong sign.
3. **L2**'s "tracked through most of the run" fails for colliding swimmer populations, where bodies are plainly discrete but identities churn. Allow body lifetime between collisions to be much longer than formation time, judged from images.
4. **labkit:**
   - the time axis uses META dt;
   - persistent_area_ratio counts nucleation growth;
   - multi-channel matter fuses species;
   - `--damage` hits the largest clump.
   Judges should also set PYTHONDONTWRITEBYTECODE=1, because a run wrote `__pycache__` into the read-only mirror.
