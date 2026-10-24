# Review: flow-lenia, sprint 2 (2026-10-24)

**Decision: CONTINUE, narrowed to one question: is selection here carried by individuals or by parcels of matter?** (promise 6/10)

**Headline.** No rung moved under v2.

`fl_forager_gene` carries a heritable uptake gene that shifts while its neutral marker does not: it rises in 5/6 selection runs and 0/6 neutral runs. The exact one-sided p is **0.021, not the reported 0.008**.

But in the only imaged seed, the sweep happens without births. It runs through takeover inside a body after a mutation patch, and through fusion followed by relabelling. **L7 is Weak (low)**, and the world sits at **L4b[L2]**.

`fl_predator` is the thread's most organism-like movie: engulfment in every seed, and prey booms followed by predator rises. But its ablations are single-seed and unmatched, and the predators went extinct on the skeptic's fresh seed. Its rating is **L4b[L2]**, with **L5 Weak (near-Supported)**.

## Consensus

| world | judged rung | conf. | key observation | pack |
|---|---|---|---|---|
| fl_forager_gene | **L4b[L2]**; L7 Weak (Contradicted in seed 3); L6 Weak | medium (rung), low (L7) | **The shift.** Final log g: selection −0.17/+0.45/+0.34/+0.73/+0.68/+0.54; neutral −0.07/−0.06/+0.11/−0.05/−0.24/+0.01 (`evo2/gene_all.png`). U=31, exact p=19/924=0.021.<br>**Body level.** High-g bodies take the body count in seeds 2, 4 and 5 (13/17, 21/21, 19/21).<br>**Seed 3** (`judge-scratch/flow-lenia-r2-biologist/gene3_f36_58.png`): the central cream cell turns orange at f40→f48 (t≈780-940) without dividing, and a cyan glider fuses into an orange cell and is relabelled (t≈940-1020). 0 persistent splits, gen 0, merges 10 > splits 8.<br>**Controls.** The neutral arm is rate-matched, not identical-event (seed 0: 99 vs 83 events). | threads/flow-lenia/packs/fl_forager_gene |
| fl_predator | **L4b[L2]** (prey only); L5 Weak (near-Supported); L4c Weak | medium | **Engulfment.** Prey #355, #395 and #497 are ringed and absorbed in the seed 0 tracks.<br>**Lagged peaks.** Prey peaks lead predator rises in 3/3 seeds (`populations.png`).<br>**Ablations.** chase=0 starves the predators; flee=0 kills both species. Each is one seed at 8000 steps, against 12000-step references.<br>**Skeptic, seed 11:** predators fall 277→36 by t=136 and reach 0 by t≈900, while prey grow ×5.3.<br>Coexistence is 3/4 seeds, at 1 of 9 parameter points. | threads/flow-lenia/packs/fl_predator |
| fl_predator_gene | L7 **Contradicted** (rung as fl_predator) | low | Selection +0.19/+0.16/+0.23 vs neutral +0.24/+0.25/+0.29. All 6 runs drift upward, and the cause is unexplained. | none shipped; threads/flow-lenia/evo2/pgene.png |

## Judges and arbitration

**Biologist (promise 6).** Ran no simulation.
- Re-analysed the per-body gene values and showed the body-level shift in seeds 2, 4 and 5.
- Extracted movie frames, which caught the seed-3 sweep happening inside living bodies.
- Read a real prey life history: a core grows into a feeding ring, then elongates. Prey cores that escape partial engulfment regrow, which explains labkit's ~100 "nucleations".

**Skeptic (promise 5).** Reran fl_predator on seed 11 (345 s on a loaded machine). Coexistence failed: the predators were extinct by t≈900, with no prey crash.
- Recomputed the p-value: one-sided Mann-Whitney 0.021, paired Wilcoxon 0.031.
- Unweighted per-body means give the same U. In seed 4, 18 of 21 bodies share genotype 0.70.
- Seed-3 mutation disks hit up to 6 genotype ids, so bodies are mosaics.
- The trait *is* the growth rate, which makes this a positive control.

**Curator (promise 6).** The only judge to call L7 Contradicted.
- Split seed 3's rise by body count: +0.49 of its +0.73 came while there were ≤4 bodies. Seeds 4-5 rose +0.61/+0.63 while there were >4 bodies.
- Stacked the 9 predator screens: 1 of 9 coexists.
- Novelty is low next to chemotaxis-motility's pursuit/evopursuit. Chase and flee are imposed blurred-field sensing.

**Arbitration.**

1. **L7: Weak (low), not Contradicted.** I examined the biologist's montage and `gene_all.png`.
   - **Seed 3 contradicts L7.** An orange/cyan patch appears in the central cell's lower lobe at t≈780, and the whole undivided cell is orange by t≈940. The small orange cell absorbs a cyan glider between f50 and f52.
   - **Not every step of that sweep is contagion.** The rubric allows a kind change *at mutation* (the ad5-evolve audit traced conversions to mutation patches). Here, though, the radius-8 disk hits part of a giant cell, and per-pixel uptake (`eat *= g`) then hands the rest of the cell to the mutant parcels. That is within-body selection. The fusion relabelling is conversion.
   - **But seed 3 is 1 of 6 runs.** In seeds 4-5 the population is ~20 bodies, and the rise came while there were >4 bodies. Bodies multiply only by fission, so one genotype spread over 18 bodies implies births, although fusion may also have moved it between them.
   - **Verdict.** The evidence is mixed by seed, and the v2 ledger that would decide it is missing.
   - **Gigantism is not caused only by selection.** One neutral run also sits at 3 bodies (`gene_all.png`, middle panel).
   - **This is a positive control.** The trait is the uptake rate itself, so the result says nothing yet about genes that shape the body. The h×0.5 dose was a coin flip: 4/6 vs 3/6.

2. **The p-value is corrected to 0.021.** The CROSS_POLLINATION line from autopoiesis r2 that cites p≈0.008 should be read as 0.021.

3. **fl_predator L5: Weak.** In every pack seed, predator matter falls from 300 to 25-60 within 200 t (`populations.png`). Seed 11 starts the same way and never recovers. Coexistence is therefore a narrow escape, not a robust attractor.
   - The ablation signs are as expected: predators are negative for prey, and prey positive for predators.
   - But the ablations are not matched (one seed, a different duration, no prey-only arm).
   - With 1-3 peaks per seed and no grid-size check, these are not cycles under v2.
   - The report gives the ablation times in steps while the packs use t (2700 steps ≈ t 540).

## Next sprint

**Main experiment: a level-of-selection audit of fl_forager_gene, with a body-level phenotype arm.**

*Setup.* 128², 12000 steps, 8 seeds per arm, about 4 CPU-hours.
- **S:** the current gene.
- **N:** an identical-event neutral twin.
- **S_body / N_body:** the same pair, except that uptake uses the body-scale phenotype g_eff = blur_R(A·g)/blur_R(A) at kernel radius, so parcels inside one body are neutral to each other. This ports autopoiesis r2's arm-E lesson: kinds neutral inside the cell.
- Move mutation timing and effect draws to their own RNG stream.
- Log each event's body and the fraction of that body hit.

*Readouts.*
- A merge-aware body tracker sampled every 20 steps.
- A per-kind ledger: births, deaths, merges between kinds and their outcome, mutation flips, conversions of intact bodies, and off-kind daughters.
- Per interval, a Price split of Δ(mean log g) into (a) between-body change (growth, fission, death), (b) within-body change and (c) fusion.
- The origin of every final high-g body: a birth, a takeover after a mutation patch, or a fusion.
- Packs with gene-coloured sheets for 2 seeds per arm.

*Pass for L7.*
- (a) > (b)+(c) in ≥5/8 selection seeds.
- High-g births outnumber conversions.
- All terms ≈0 in the twins.
- Deaths occur after colonization.
- gen ≥2, with random birth strips in this world.

*Outcomes.*
- If (b)+(c) carry S but (a) carries S_body, S_body becomes the thread's heredity model.
- If neither arm passes, record the result as L5 (infection), stop mutation runs, and add the anti-fusion ingredient first.

**Secondary goals**
1. **fl_predator L5 to Supported.** Run the reference, chase=0, flee=0 and prey-only arms on 6 seeds at 12000 steps. Use per-species segmentation (labkit `META["species"]`). Report a sign table, the coexistence frequency, and peak spacing with a 192² size check. This replaces the 256² movie.
2. **Resolution.** Run R_scale×2 with flow×4 on one S seed and on fl_predator seed 0. This has been owed since r1.
3. **Predator-gene drift.** In fl_predator_gene, log the first mutation draw and the fraction of prey it hits per seed, to explain the upward drift.

**Pause:** predator coevolution, secreted-signal sensing (chemotaxis-motility's line), cost variants, new worlds, and further h doses. fl_morph257 and the L4c fork stay parked.

## Cross-pollination

- **Out to chemotaxis-motility:**
  - The parcel-versus-body trap. evopursuit's radius-4 swap is a matter-level operator, so add the Price split to the ledger you are already planning.
  - fl_predator's mass-conserving kill term as a "consuming predator" arm: it gives lagged prey→predator peaks in 3/3 seeds and prey extermination without flee.
- **Out to autopoiesis:** independent confirmation of the arm-E rationale. A sub-body mutation patch plus a per-parcel advantage takes over an undivided cell (seed 3, t≈780-940).
- **Out to active-droplets:** run the same Price split on ad5-evolve, separating division from takeover after the 5-px transplant, and report the footprint relative to body size.
- **Out to lenia-multichannel:**
  - Before localizing a growth trait in matter, make it body-scale; otherwise selection breeds giants.
  - fl_predator's predator layer could drive mcfd's cycles.
- **In:**
  - autopoiesis' co-mutated neutral tag (`motile_trait_tox/world.py`) and `kindtrack.py`;
  - fisim's shared-RNG twins (`evo.py`, `packs/xcell-evo2-S`);
  - chemotaxis-motility's largest-parent `fission.py`;
  - the ad5-evolve conversion audit.

## Rubric issues

1. **L7 with matter-carried genes.** When a gene is a parcel field and bodies can be mosaics, require a between-body / within-body / fusion decomposition. Define when a takeover after a mutation patch counts as "change at mutation": within a stated time of the patch, with no merge. A matter-weighted mean is not individual-level evidence.
2. **A trait that multiplies growth directly** is a positive control for the selection machinery. Score it low under novelty and mechanism, whatever the rung.
3. **labkit:**
   - two-species worlds must use `META["species"]`; prey-predator contacts otherwise count as merges and splits;
   - add a per-body gene readout (body mean and within-body variance).
4. **Units:** require t, not steps, for every time quoted against a pack.
5. **Process:** the r1 review again reached the researcher after the sprint's work was done.
