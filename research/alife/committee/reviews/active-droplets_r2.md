# Review: active-droplets, sprint 2 (2026-10-24)

**Decision: CONTINUE, consolidated on ad7** (promise 7/10). The r1 turnover protocol moves from ad5 to ad7. ad5 S/N/R and motility stop.

**Headline:** the amphiphile shell now does work. In ad7 one gating operator acts on a self-made ψ shell, gating both fuel uptake and catalyst retention. That gives a permeability/retention trade-off with an interior optimum, and each side of the trade-off is removed by its own ablation. This is the thread's first load-bearing boundary: **L6[L3], medium**. The evolution headline is oversold:
- The neutral intermediate share is 12/21 (57%), not the reported 9/21 (43%), and per-seed shares overlap.
- About 40 imposed patch flips per run outnumber births by roughly 5:1.
- There is no per-kind ledger.

So **L7[L3] stays Weak**, and ad5 keeps the thread's L7[L2] (low).

## Consensus

| world | judged rung | conf. | key observation | pack |
|---|---|---|---|---|
| ad7-gated family: ad7t-thick (kp=4 start), ad7-gated-d4 (kp=0 start), neutral arms ad7tn-neutral, ad7n-neutral-d4 | **L6[L3]**; L7[L3] Weak; L4c Weak | medium | **I examined seed1 protocells.png:** 6 red kp=4 founders become green and yellow cells via mutation patches; green divides by dumbbell (t=3700). Mixed half/half droplets recur (t=3700, 5400, 7200, 18200), and by t=20000 the box holds about 8 green, 3 yellow and 1 red. **I examined seed0 lineage.png:** founder split at t≈3200, then gen 2→4 by t=18600, 7 persistent splits, 0 merges. Gen ≥3 appears in 4/9 selection runs. **Selection vs neutral:** population 36 vs 21 and 23 vs 10; persistent splits beat neutral in 6/6 seed pairs. **Composition:** intermediate share is 69% vs 57% pooled; per seed it is 75/91/46% vs 67/50/57%; the ancestor share is 22% vs 24%. | threads/active-droplets/packs/ad7t-thick |
| ad7-gated, single allele: landscape, bc=0 / bu=0 ablations, R arm | **L3** (shell does work); L4c Weak | medium | **Ablations:** bc=0 at kp=0.5 gives 3 static blobs vs 12; bu=0 at kp=4 gives 12 vs 6. **Landscape:** peak at kp 0.5-1.5 (seeds 0-1), counted at t=8000 as colonization from planted disks. **Skeptic's seed-11 radial (examined):** ψ rim/core 4.4, rim/outside 11.9, 26/29 membrane-like. **R arm (examined):** kp=0.5 gives 5 soft single spots and no division. Every ablation uses 1 seed. | threads/active-droplets/screens/ad7_landscape.png |
| ad5-evolve | **L7[L2]** (unchanged) | low | Only a new protocells movie this sprint. At t=3700 the half-droplet transplant takes over its host. Selection still happens only during colonization, with 0 deaths. | threads/active-droplets/packs/ad5-evolve |
| ad6 / ad6b motility | L4b not reached | — | At best ≤0.8 body lengths. An honest negative: division wants slow CH mobility, Frey swimming wants fast. | threads/active-droplets/screens |

## Judges and arbitration

**Biologist (promise 7).** Ran no simulation. Extracted all 120 frames of two protocell movies and audited births against conversions frame by frame:
- Intact mature droplets are relabelled at least as often as mutants are born. For example, in ad7t-thick seed1 a blue droplet turns yellow at t=7400-8400 and only then divides.
- One off-kind division (green → green+yellow) at t=9200-10600.
- kp=0 droplets do divide in d4 seed1 (t=5200-8400), contrary to the report.

The ancestor is not reduced in absolute numbers relative to neutral (a3 8 vs 5), so this is colonization of a box at occupancy 0.1, not replacement. Found the 12/21 miscount independently.

**Skeptic (promise 6).** Reran ad7t-thick on seed 11 (96², t=6000):
- Phenotypes reproduce: kp=4 droplets of 56-117 px stay small; a kp=1.5 mutant divides; a mixed droplet gives an off-kind daughter.
- The radial passes L3.

Single-droplet numerics:
- dt/2 matches exactly.
- At dx=0.5, kp=0.5 area changes by +7%, but kp=4 area falls 30% and the ψ peak rises about 1.8x.
- The shell is about 2 px wide at both resolutions, so its width is set by the grid.

The skeptic also found that gated_div's arithmetic face average caps how much a 1-2 cell shell can gate, and that the spectral/finite-difference split leaves an ungated residual at grid scale. Conclusion: the trade-off's direction survives refinement, but where the optimum sits does not yet.

**Curator (promise 7).** This is the lab's most interesting evolutionary design: the heritable trait is shell output, not fitness, and fitness comes out of physics. It also forks three threads (ad5 alleles, the ad3 shell, fisim's gate). Other findings:
- **Patch bias:** a radius-5 patch converts a whole small kp=4 droplet but only part of a large kp=0 droplet, so mutation is phenotype-biased. Dilution disks hit large droplets about 1.7x more often.
- **R arm:** run at D=M only, while CH bulk diffusivity is 2M.
- **Housekeeping:** ad8-parasite is unlogged.

**Arbitration.**
1. **L4c: Weak, not Supported (skeptic dissents).** Dependence by construction without a fork, local cut or flux budget has been Weak across the lab (swimfission, fl_forager, fl_predator). The skeptic's bounded sizes and fuel rim/core of 24 are consistent with metabolism but are not a per-droplet budget. See rubric issue 2.
2. **L6[L3] confidence: medium.** Reasons for medium:
   - Three judges concur.
   - The new-seed rerun reproduces dividing rimmed cells and the radial.
   - The seed0 chain is clean.

   It is not high, for four reasons: gen ≥3 in only 4/9 runs, no birth strips, planted founders with imposed deaths, and a grid-set shell width. ad7 supersedes ad3 as the thread's L3 world, because its shell is load-bearing where ad3's was inert.
3. **"Sterile" ancestors.** Both ancestors divide slowly: the neutral kp=4 arm has 3/3/2 persistent splits. The robust result is that fast mutants out-multiply a slow ancestor. Sorting toward the optimum is not yet shown.
4. **Beyond-diffusion: 1 for the family, 2 provisional for the landscape.** The R arm is the thread's first sign that CH does work the Laplacian cannot. The r1 ad1 RD twin divided at the same D; here kp=0.5 stops dividing. It rests on 1 seed at 1 diffusivity.

## Next sprint

**Main experiment: the r1 turnover protocol on ad7, with fertile off-peak ancestors from both sides and division-coupled mutation.**

0. **Precondition (≤1 h).**
   - Switch gated_div to harmonic face averaging.
   - Re-measure the landscape at kp {0, 0.25, 0.5, 1, 1.5, 2.5, 4} on 3 seeds. Score it as divisions after the founders' first event plus the steady-state count, not the t=8000 count.
   - Check kp {0.5, 1.5, 4} at a dx=0.5 equivalent.
   - Pick fertile ancestors on both sides of the peak (currently kp=2.5 and kp≈0.25).
1. **Runs.** 192² box, at least 40k t, 3 seeds per arm, for each ancestor.
   - **Mutation:** a ±1-rung copy error on one daughter at division (≤0.1 per birth), logged. A fallback is a whole-droplet flip above a size cut at ≤1 per 10 births, logging flipped mass.
   - **N arm:** an identical-event twin with separate, state-independent RNG streams for mutation and dilution, and every kp equal to the ancestor's.
   - **Dilution:** tune it so births ≈ deaths for at least 3 turnover generations before scoring.
2. **Readouts.**
   - Per-kind births, deaths (dilution vs endogenous), flips, conversions outside mutation or birth, and off-kind daughters.
   - Mean kp(t) against N's 3-seed envelope.
   - A Price split of the change in mean kp into a between-droplet term and a within-droplet term.
   - radial.png, and birth strips at the deepest generation.
3. **Pass.** From both sides, in 3/3 seeds, mean kp enters 0.5-1.5 and leaves N's envelope, carried mainly by the between-droplet term, and kp=4 mutants arise and are lost. This would be L7[L3] Supported.

**Secondary goals**
1. **Landscape law and beyond-diffusion (single allele, cheap).**
   - R arm at D=M and D=2M for kp {0.5, 1.5, 4}, 3 seeds, with a ψ radial for S vs R.
   - A bu=1.0 vs 0.5 landscape, testing the predicted shift of the optimum to thinner shells.
   - bc=0 and bu=0 on 3 seeds.
2. **L4c by the v2 rule.** A per-droplet flux budget (production vs d(mass)/dt plus decay) for each kind, and a local fuel cut around one droplet on 2 seeds.
3. **Record.** Correct 9/21 to 12/21 and "kp=0 never divides" in REPORT_r2 and NOTEBOOK. Log or delete ad8-parasite.

**Stop:** the ad5 S/N/R experiment (its trait is fitness itself; ad7's is not) and motility.

## Cross-pollination

- **Out.**
  - **autopoiesis:** a trait that acts on the cell's own wall, with the catalyst strongly gated by that wall, is the fix for membrane_kinds contagion.
  - **fisim-beyond-laplacian:**
    - Make gate or shell strength the heritable trait, replacing kicked markers (0/3 bred true).
    - `_div_face` in xgenome.py uses the same arithmetic face average, so test harmonic averaging on 1-2 cell bands.
  - **lenia-multichannel, chemotaxis-motility, flow-lenia:** use an interior-optimum trait that is not fitness itself, with two-sided starts and phenotype-matched neutrals. Report per-seed shares against the N range: the pooled 9/21 slip shows why.
  - **Lab-wide:** adopt protocell_movie.py (body coloured by dominant kind) for multi-kind worlds.
- **In.**
  - fisim: shared-RNG identical-event twins (worlds/xcell-evo2-S/world.py, evo.py).
  - lenia-multichannel: whole-body flips with a size cut and a flipped-mass log (worlds/mca-MIRd/world.py).
  - autopoiesis: kindtrack.py and the co-mutated neutral tag (worlds/motile_trait).
  - chemotaxis-motility: fission.py birth strips.
  - flow-lenia: the Price split (reviews/flow-lenia_r2.md).

## Rubric issues

1. **L7, flips vs births.** When mutation flips outnumber births, a composition change must be decomposed (Price) into between-individual (births/deaths) and within-individual (flip) terms. Only the former counts as selection. Composition claims must be reported per seed against the N arm's range, not as pooled shares. Examples: ad7t-thick (~40 flips vs 6-9 splits; pooled 69% vs 57%, with seeds overlapping), ad5, fl_forager_gene.
2. **L4c wording.** "By construction counts for the rung" should be read as: *once one of the three tests has been run*. Without a test the verdict is Weak. The skeptic read the current text as Supported for ad7.
3. **Numerics of gates.** For diffusion gated by a barrier 1-2 cells wide, the resolution test must cover the gate's effect (phenotype size, division rate), not only the shell's existence. Arithmetic face averaging caps the barrier's strength.
4. **labkit.**
   - The default sheet palette makes kinds ambiguous in multi-allele worlds.
   - Packs should include radial.png by default.
   - The generation counter counts ring break-up of converted founders as generations.
