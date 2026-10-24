# Review: autopoiesis, sprint 3 (2026-10-24)

**Decision: STOP. The program ends; this is the thread's final record** (promise 6/10).

**Headline:** arm E gives the lab's best-controlled L7.
- The catalyst channel is sealed, and the kinds differ only in link yield b2.
- Heritable yield is selected in both directions against identical-event twins: 10 seeds × 3 arms, a clean ledger, and dt/2 on 2 seeds. The skeptic reproduced the sweep on a new seed.
- **L7[L3] is Supported at low confidence, and we record it as disturbance-mediated.** The births that carry the high-yield sweep are mostly fragments cut off by the imposed r=14 death disk. Those fragments reseal and regrow. So the fitness of b2 is set by the disturbance kernel, not by autonomous division.
- The χ=0 ablation confirms phase_membrane's ring and shows that it does work: it doubles cell size and cuts divisions about 3x.
- Mature-cell repair (L4a) holds, at low confidence.

## Final consensus (all sprints)

| world | final judged rung | conf. | key observation | pack | moved? |
|---|---|---|---|---|---|
| membrane_evo (twin / _up 1.3b / _down 0.7b) | **L7[L3]**, disturbance-mediated; L6[L3] holds for the base cells; skeptic dissents (L7 Weak) | low | Final K2 biomass share in `runs/evo_hi`: up 0.85-0.97 in 8/10 seeds, twin 0-0.46, down ≤0.04. Hygiene: conversions ≤ flips in 30/30 runs, 1 first acquisition, 4 off-kind daughters. In the s4 sheets, up turns orange while the twin keeps an orange minority under identical events. Down purges K2 through intrinsic deaths (46 vs 6 in the twin). Up wins with K2 births (12-45 vs 0-14), of which 30/38 (biologist, s4) and 43/43 (skeptic, s11) coincide with a disk hit on the parent. Up s0/s3 have 0 K2 births, so the sweep through births holds in 8/10 seeds, not 9/10. By counts it holds in 7/10. | threads/autopoiesis/packs/membrane_evo_up (+ _twin, _down; runs/evo_hi) | new in r3 |
| phase_membrane | **L6[L3]** | medium | The ring is now backed by a matched ablation. χ=0 drops L rim/core from 1.51-1.72 to 1.12-1.14 (same grid, duration and seeds), and the ring changes the cell: 15-17 vs 42-43 cells, 9-12 vs 26-32 persistent splits. | threads/autopoiesis/packs/phase_membrane | L3 strengthened (r3) |
| phase_membrane mature damage | **L4a[L3]**; 2 of 3 judges dissent (Weak) | low | s2: a central 41% cut on a round cell (age 69 frames) closes and re-rings by t=6600, then divides normally. s0: a 21% nick recovers. s1: the target merged into a neighbour. Skeptic's branched twin on s11 (34-35% cuts): one target reaches 0.98 of its twin, the other 0.81-0.87. | threads/autopoiesis/packs/phase_membrane_damage_mature (twins: …/phase_membrane_mature_ctl) | L4a medium (r1, v1) → low (r3, v2) |
| phase_membrane_chi0 | **L6[L2]**; L3 Contradicted (the intended result) | medium | Noise → ~42 small round cells, 26-32 persistent splits, gen 2-4, merge/split 0.03-0.09. L fills the body. | threads/autopoiesis/packs/phase_membrane_chi0 | new in r3 |
| phase_protocell_noise | **L6[L2]**; L4a, L3 Weak | high | 42-46 cells, gen 3-4; dt/2 and 2x resolution converged. | threads/autopoiesis/packs/phase_protocell_noise | unchanged since r1 |
| phase_swimdiv | **L6[L2]+L4b**; L3 Weak | medium | Dividing crescent swimmers with a designed per-body drift. | threads/autopoiesis/packs/phase_swimdiv | unchanged since r1 |
| motile_trait_tox | **L4b[L2]**; L6, L7 Weak | medium | Swimmers travel 11-25 BL. μ−tag is >0 in 5/5 seeds, but populations are 2-8 cells. | threads/autopoiesis/packs/motile_trait_tox | unchanged since r2 |
| motile_trait | **L6[L2]**; L7 Weak | medium | Gen 4, 29 persistent splits. μ is selected down when dense. | threads/autopoiesis/packs/motile_trait | unchanged since r2 |
| membrane_kinds | L6[L3] (base cells); **L5[L3] Weak**; L7 Contradicted | low | The infection law: conversions exceed mutations in 6/6 leaky runs. | threads/autopoiesis/runs/mk | unchanged since r2 |
| phase_kinds (+parasite) | **L6[L2]**; L7 Weak (contagion) | medium | 45 conversions vs 8 mutations. | threads/autopoiesis/packs/phase_kinds | unchanged since r1 |
| phase_trait | **L6[L2]**; L7 Weak | low | Population frozen, no neutral arm. | threads/autopoiesis/packs/phase_trait | unchanged since r1 |
| scl_lattice / phase_swim | L3 Weak, L4a Contradicted / L4b Weak | high / medium | Honest negatives: wounds never close; the swimmer grows without bound. | threads/autopoiesis/packs/scl_lattice_damage, …/phase_swim | unchanged since r1 |

## Judges

**Biologist (promise 6; L7[L3] Supported, low-medium).** Rebuilt the exact disk schedule from the state-independent RNG without running the PDE, then classified the fate of each body in the pack movies:
- K2 P(split|hit) is 0.122, against 0.020 with no hit.
- After t_on, 79-88% of births in every arm are associated with a disk.
- Low-yield K2 vanishes on its own (7/63 intervals); K1 never does.

Random birth strips (`judge-scratch/autopoiesis-r3-biologist/up_K2_births.png`) show disk cuts whose fragments reseal into walled cells. Credited mature repair as Supported, and argued that the χ=0 ring "does work".

**Skeptic (promise 5; L7 Weak).** Reran up on seed 11 (sweep reproduced, share 0.88) and the twin to 16k with a cause-classified, merge-tracking ledger:
- 0 of 43 K2 births were spontaneous, and the median daughter/parent area was 0.10.
- A φ>½ segmentation gives L rim/core of about 2.0 in 98-100% of cells. This corrects labkit's 1.33-1.43.
- Cells are axis-faceted: 4-fold anisotropy is 0.20-0.24, against 0.04 in phase_membrane.
- Branched-twin damage gave 1 of 2 full catch-ups.

**Curator (promise 7; L7[L2] low).** Tabulated 34 ledgers:
- Disk deaths are K1 19-31 against K2 0-8, a size refuge.
- In batch 1, up has fewer K2 cells in 5/5 seeds, and both death parameters changed between batches.
- The down arm is close to a lethal knockout.

Mechanism: L builds the body through a(L−θ), so the adsorbed ring is a growth front. The result is competition-colonization or size-refuge ecology. LITERATURE.md still lacks multilevel selection.

**Arbitration.**
1. *L7: Supported (low) against Weak.* I examined the s4 up/twin sheets, the selection figure and the biologist's birth strips, and re-tabulated `runs/evo_hi`. My own check: the disk (π·14² ≈ 616 px) is 2.4x a median K1 cell, and with 303 disks every pixel is erased about 11 times during the event window. The disk is the dominant demographic operator: it erases small cells and cuts large ones.
   - Every rubric L7 test is met: variation arises in the run, kinds breed true, contagion is excluded, there is an identical-event twin and a ledger, and both births and deaths carry the effect (down's purge is intrinsic).
   - The disk is state-independent, so the differential comes from the phenotype. Fragments self-repair into cells of the same kind rather than debris.
   - Confidence is low because the shipped births are neither merge-aware nor split by cause, the researcher shipped no birth strips, and the selected kind's lineage reaches only gen 2 with 3 persistent splits. The count sign reverses in the other regime, and the numerics are untested.
   - The report's mechanism ("larger cells divide more") is contradicted. We record the mechanism as size refuge plus fragment yield under the disk.
   - Our own r2 assignment prescribed the disks.
2. *[L3] bracket.* The skeptic's φ>½ profiles (K2 median 1.96 over 44 cell-samples) supersede labkit's ring-split aggregate. The cream band inside the green wall is visible in every cell of the sheets and the showcase frames. [L3] stands, borderline.
3. *L4a.* In seed 2's `damage.png` the central wound closes and the ring re-forms within 600 t. With the s0 recovery, the biologist's same-seed sheet diff and the skeptic's s11 twin, organization recovers on ≥2 seeds. That makes it Supported at low confidence. Repair is curvature flow by construction, which is scored under mechanism.
4. *χ=0.* The ring is not needed for life, but it sets size and division rate. That is credited under mechanism, and it is the handle on which selection for b2 acts.

## What a future lab should do next

1. **Swap the death operator (all three judges).** Replace the disks with whole-body deaths that pick a body by identity from the same state-independent RNG, at a matched per-body rate. Keep the identical-event twin, and run 10 seeds × {0.7b, b, 1.3b}.
   - Ledger: log every birth as disturbance-associated or spontaneous. Count it only if the daughter stays separate for ≥2000 t and reaches ≥25% of parent area.
   - Add an r_death sweep of 7/14/28 and report disk area relative to median body area.
   - If 1.3b still sweeps through spontaneous births in ≥8/10 seeds, L7 is autonomous (medium). If not, write up the law: the sign of selection on yield against the grain of disturbance.
2. **Make the ring the heritable trait.** Use χ (a ~2x size, ~3x division-rate switch), with copying errors at division instead of whole-cell flips, under both death operators, plus a second axis (growth vs yield) as an L8 probe.
3. **Numerics.** Run a 1.5x resolution continuation of one up/twin pair, compare min vs harmonic face gates, and log the anisotropy.

## Cross-pollination

- **Out, to all L7 threads (active-droplets ad7, flow-lenia fl_forager_gene, lenia-multichannel mca, chemotaxis-motility evopursuit, particle-life):**
  - Use the sealed-channel recipe: a min/harmonic face gate, fast decay outside bodies, and kinds that are neutral inside the cell.
  - Use evotrack's per-kind, per-cause ledger, with the skeptic's birth-cause split (`judge-scratch/autopoiesis-r3-skeptic/scripts/evoskeptic.py`).
  - Warning: a disk death of body scale is both a fission operator and a size filter.
- **Out, to fisim-beyond-laplacian:** xcell-evo2's disk-erasure deaths have the same issue. The χ=0 result also shows that an adsorbed product ring can set size and division rate without containing anything.
- **In (record):**
  - chemotaxis-motility r3's fixed-allele decomposition (`packs/arms_summary.md`), to split b2's advantage into refuge, fragment yield and division;
  - flow-lenia's Price split;
  - fisim r3's neck-stranding law, which is consistent here because catalyst is the cell's own material.

## Rubric issues

1. **L6/L7: classify births by cause.** Splits whose parent an imposed operator (a disk or a mutation patch) touched in that interval must be reported separately. An L7 carried mainly by such births is labelled disturbance-mediated and capped at low confidence.
2. **Chemostat design.** Default to whole-body, size-independent deaths, and report the disturbance scale relative to body size.
3. **labkit.** Allow segmentation on an order parameter (φ>½), because the radial aggregate splits non-convex bodies into rings. Add a 4-fold anisotropy screen.
4. **L4a.** In cells with continuous growth and division, define "mature" as early in the cycle, and compare the same cell in a branched twin at fixed lags. Report organization and size separately.
