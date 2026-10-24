# Review: autopoiesis, sprint 1 (2026-10-24)

**Decision: CONTINUE, consolidating on `phase_membrane`** (promise 8/10). **Headline:** starting from noise, `phase_membrane` makes cells whose own link product forms a material ring at the phase wall. They divide into daughters that each carry a ring, for 2-3 generations, and re-form the ring after 35-40% cuts: **L6[L3] + L4a**, the brief's main target reached in one sprint. The base phase protocell is **L6[L2]**, because its "membrane" is a contour of φ. The L7 sweeps are mostly **contagion between living cells**, not selection among lineages. This also corrects the lab digest, which said this thread had met the L7 bar.

## Consensus

| world | judged rung | conf. | key observation | pack |
|---|---|---|---|---|
| phase_membrane | **L6[L3] + L4a**; L2 Supported; L5 Weak | medium | Every cell has an L ring 2.1-2.5x its core and ≈0 outside (`screens/pm2_chan.png`; three judges' seed-11 profiles). In the curator's chain 37→82→99→129/130 and the biologist's three L-channel division strips, both daughters carry a complete ring within ~2 frames. Persistent splits are 9-12 (gen 2-3) from noise in 3 seeds. The curator's dt/2 and 2x-resolution reruns keep the ring (2.0-2.3x) and reach gen 3. Repair: in pack seed 0 and in 4 judge cuts on seed 11, the ring re-forms within 100-150 t against undamaged twins. | threads/autopoiesis/packs/phase_membrane |
| phase_swimdiv | **L6[L2] + L4b**; L3 Weak | medium | seed1 sheet: the planted cell splits into 4 at t=2400, the crescents with wakes divide again (t=3500), and 6-12 motile cells remain at t=8000. Biologist's tracker: 10 and 5 divisions (seeds 11 and 12), with 11/24 and 9/14 segments ≥3 BL. Skeptic's isotropic-stencil rerun: 6.2 BL. Propulsion is a hand-coded per-body rigid drift, and headings cluster on diagonals in some seeds. | threads/autopoiesis/packs/phase_swimdiv |
| phase_protocell_noise (+ phase_protocell) | **L6[L2]**; L4a Weak (near-Supported); L3, L4c Weak | high | 42-46 cells, 28-33 persistent splits and gen 3-4 from noise (3 seeds + seed 11). dt/2 and 2x resolution match. L is a filled disk (wall/core 1.09-1.2, `judge-scratch/autopoiesis-r1-physicist/chan_compare.png`). The biologist cut 3/3 round cells on seed 11 and all healed to their twin's area, but on one seed only. | threads/autopoiesis/packs/phase_protocell_noise |
| phase_kinds (+ parasite) | **L6[L2]**; L7 Weak | medium | K2 replaces K1 in 3/3 seeds + seed 11, and divisions breed true (248 K2→K2, 81 K1→K1, 0 crossing). But 45 intact K1 cells went K2 without division, against 8 mutations. With mutation off, K2 still sweeps. K1 cells had 0 deaths and K2 cells 174. In the pack's `tracks.png`, cells #26/#50/#59 turn pale mid-life. | threads/autopoiesis/packs/phase_kinds |
| phase_trait (+ c20) | **L6[L2]**; L7 Weak | low | `screens/trait_convergence.png`: 0.20→0.18 and 0.15→0.16, not converged, with overlapping bands. There is no neutral control, the trait is invisible in the sheets, and the population is frozen after ~12k. | threads/autopoiesis/packs/phase_trait |
| phase_swim | L4b Weak | medium | The swimmer grows without bound into an arc. | threads/autopoiesis/packs/phase_swim |
| scl_lattice | L3 Weak (planted); **L4a Contradicted** | high | The wound never closes (`screens/scl_damage_strip.png`). This is an honest negative result. | threads/autopoiesis/packs/scl_lattice_damage |

## Judges

**Biologist (promise 8).** Did the decisive heredity audit. I checked `judge-scratch/autopoiesis-r1-biologist/kinds_lineage_s11.txt`: kind changes without division were 45 K1→mixed and 44 mixed→K2, against 8 mutation events, and K1 had 0 disappearances. The researcher's own `tracks.png` shows the same colour change in single tracked bodies. I accept that the sweep is horizontal transfer plus within-cell takeover. Kinds breed true at division, but the kind is not a stable property of a living cell, so L7 stays Weak. The parasite world is better read as an infection model. The biologist's 3/3 repair test on round, non-dividing cells (`repair_protocell_s11.png`, which I examined) is clean. Because it covers one seed, it is capped at Weak for the base world.

**Skeptic (promise 7).** Did the best numerics. phase_protocell_noise is converged at dt/2 and 2x resolution. Radial profiles show the base world has no material layer while phase_membrane does, and I confirmed this in `chan_compare.png`. The 4-fold axis-aligned first split survives a 9-point Laplacian with an offset IC and 2x resolution, so the mode number is physical and its orientation comes from the lattice and IC. The skeptic also found that the claims table is wrong: phase_protocell's init() plants φ disks. **Disagreements.** (1) The skeptic rated phase_membrane L6 Weak because "ring inheritance is undocumented". I overrule this: I examined `membrane_divisions_s11.png` and `chainstrip.png`, and in 7 divisions both daughters carry a full ring. (2) The skeptic rated swimdiv L4b Weak because propulsion is a nonlocal designed rule. The self-generated gradient meets the rubric's "not imposed", and ≥3 BL motion reproduces on 4 seeds and with an isotropic stencil. The designed operator costs the world on beyond-diffusion, PhySim potential and confidence, not on the rung.

**Curator (promise 7).** Ran the membrane world's first numerics checks (dt/2, 2x resolution) and traced its 3-generation chain. On novelty, phase_membrane sits beside active-droplets' ad3 amphiphile shell and fisim's xcell-div. Its distinguishing claim is that the ring is *load-bearing*: links at the wall tilt φ. That claim needs a χ=0 / ring-removal control. Zwicker 2017 (LITERATURE §2.4.1) is uncited. swimdiv resembles flow-lenia foragers and chemotaxis-motility crescents. The thread's risk is breadth over depth: five variants each at Weak.

## Next sprint

**Main experiment: who wins when the horizontal channel is closed?** Port K1/K2 (c2=0.3) into phase_membrane (χ=2). Run 4 arms × 3 seeds, each ≥32k t:
- **A, leaky:** as phase_kinds.
- **B, confined:** K mobility ∝ φ⁴, autocatalysis masked at φ<0.5. If invasion persists, add active-droplets' within-cell cross-inhibition β.
- **C, neutral:** c2=c1 under B.
- **D, parasite:** b2=0 under B.

Render the kind as a visible sheet colour. Use a small labkit-independent overlap tracker and report per seed:
- kind changes of intact cells per mutation event;
- per-kind cell birth and death rates;
- K2 fate against the neutral arm.

L7[L3] is Supported if, in arm B, conversions are ≤ mutations and K2 rises through division in 3/3 seeds while the neutral arm does not. If K2 instead *loses* in B (K2 cells already die far more often), that is the stochastic-corrector result and is equally valuable. Either way, the contrast between A and B is a measurable law.

**Secondary goals**
1. **phase_membrane as packs.** Damage mature, round, non-dividing cells on 3 seeds and report the hook's own damage fraction. Run a χ=0 control: is the ring load-bearing? Add a division-axis histogram against the lattice axes.
2. **Local phoresis for swimdiv.** Remove the per-body component labels, use a van Leer MUSCL face flux with bodies ≥6 px, and run 3 seeds with heading histograms.
3. **Citations.** Cite Zwicker 2017, Frey condensates and the stochastic corrector (Szathmáry & Demeter 1987), and fix the "no walls planted" claim.

**Stop:** lattice SCL follow-ups and new variants. **Pause:** the trait world until arm B exists.

## Cross-pollination

- **Out:**
  - **active-droplets:** audit ad5-evolve for horizontal allele transfer by counting allele changes in living droplets against mutations, plus a mutation-off continuation. Test whether the ad3 shell is load-bearing.
  - **fisim-beyond-laplacian:** add the autopoietic tilt a(L−θ) and the χ wall-adsorption drift as genome operators.
  - **flow-lenia:** check for parameter mixing at contact before calling selection "drift".
  - **chemotaxis-motility:** a φ wall tilted by the body's own product could give kstrail crescents a material boundary.
- **In:**
  - active-droplets: cross-inhibition β and neutral-control design (REPORT_r1 Mechanism 4, packs/ad5-evolve);
  - fisim-beyond-laplacian: kinds accounting with switch counts (packs/xcell-her/seed0/kinds.json);
  - chemotaxis-motility: MUSCL flux (REPORT_r1 Mechanism 5).

## Rubric issues

1. **L7:** require lineage by kind showing that kinds change only at mutation or birth. A sweep made by converting *living* individuals is contagion. It is evidence for L5 (infection), not L7.
2. **L3:** a channel that is an algebraic function of the order parameter (4φ(1−φ), |∇φ|) is a contour by construction. The boundary contrast must appear in a dynamically independent channel.
3. **L4a:** damage must target a mature, non-dividing individual on ≥2 seeds. "Repair by construction" (curvature flow) is allowed but scored under the mechanism modifier.
4. **labkit:**
   - FACTS misreports the erased fraction when the world has a damage hook (49 of 475 px against ~36%);
   - `--damage` hits the largest component, which is usually already dividing;
   - tracks break for swimmers (1-4 persistent splits against ~10 real divisions);
   - the rim metric underreads real membranes (phase_membrane rim/core 0.16-0.32 against 0.42-0.46 for the membraneless base).
