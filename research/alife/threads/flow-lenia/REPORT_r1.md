# flow-lenia: sprint 1 report

## 1. Headline

**Adding a conserved food field to Flow-Lenia turns gliders found by random rule search into foragers
that eat, grow and divide.** One 12x12 noise patch becomes 10-14 motile crescent gliders. All 3 seeds
have 0 nucleations, so every body descends from the patch by division. Each glider leaves a
food-depletion wake. Without food the gliders dissolve. The behaviour survives halving dt and ±10%
changes to every metabolic rate. Heritable parameter variants of these foragers compete to exclusion
for the shared food, but this sprint could **not** tell selection from drift (section 4).

Implementation (`worlds/fl_base`): a numpy port of Flow-Lenia. It uses reference priors, Sobel
gradients, `alpha = clip((A_c/C)^2)`, and reintegration tracking done as a 3x3 scatter with
`np.bincount`. Mass drift is 1e-12 to 3e-11 over 2000-4000 steps for every rule tried (~100 rules).
Matter plus food is conserved to 8e-12.

## 2. Claims

| world | claimed rung | strongest evidence (pack, time) | known weaknesses |
|---|---|---|---|
| `fl_forager` (rule C2_r202 + food) | **L6[L2]**, with L4b (motion) and L4c (metabolism) | `packs/fl_forager/seed{0,1,2}` sheet.png: 1 patch → 3 gliders (t≈40) → ~12 (t=800). 0 nucleations, 40-49 splits per seed. `seed1/divisions.png`: parent → division (f5) → daughter divides again (f49); an elongated body divides (f65) and its daughter divides (f136). Moving tracks travel 7-11 body lengths. No-food ablation: all gliders gone by t≈250 (`screens/abl_forager_nofood.png`). | Gliders collide and merge often, so labkit lineages are shallow (max gen 1-2; 2-generation chains: 0/3/1 per seed). Daughter morphology varies (crescent, C-ring, small ring). Division with food is reported in the Flow-Lenia paper (Fig. 6f), so novelty lies in the specific operator (Hill-gated uptake from a conserved, diffusing pool) and in the motile foragers. |
| `fl_cells` (C=3 rule 0) | **L3**, with L4a (repair) | `packs/fl_cells/seed{0,1,2}`: each noise patch condenses into a cell with a cyan core, a thin continuous orange ring and a magenta outer crown. The three layers are in different channels and persist the whole run at constant size (tracks.png). `packs/fl_cells_damage/seed{0,1,2}`: 38-44% of the largest body erased at t=120; core, ring and crown re-form within ~40-100 time units (seed 2: the damaged 3-lobed body briefly falls apart into 3 sub-cells, then re-forms one 2-nucleus cell). The undamaged control is the same seed in `fl_cells`. | Static, no motion; cells that touch fuse (seed 1 t≈240, seed 2 t≈250). Formed from random patches, but each patch gives exactly one cell. **The beaded crown disappears at dt/2** (it becomes a smooth halo); the core/ring/halo layering survives. One rule. |
| `fl_forager_evo` (2 founders, localized m,s,h) | **L5** (competition for a resource). L7 **not supported** | `evo/fs1.png`, `evo/fs2.png`: total matter saturates at ~1500 (food-limited), and in 5/6 runs one kind ends with >85% (exclusion). The kinds breed true with distinct morphology: in fs2 seed 1, kind1 makes ~50 small bodies, kind0 rings (`packs/fl_forager_evo` sheet). | Which kind wins depends on the seed: 4 pairs × 10 seeds at 96² give 7/3, 6/4, 3/7, 6/4. Exclusion is real; selection is not detected. The founders were planted by me. |
| `fl_forager_mut` (one founder + mutation, genotype ids) | L7 candidate, **Weak/not supported** | `evo/mut_muller.png`: 62 mutations, phylogeny depth 7, and new heritable morphologies appear mid-run (`packs/fl_forager_mut` sheet: a lineage of compact solid bodies, a large target-ring cell). | Neutral control with the same events and no parameter change (`evo/mut_neutral_muller.png`) shows as much clade turnover (root share 9% vs 36%). The genealogy is consistent with drift. One run each. |
| `fl_cells_food` (layered cells + food) | L1 at the end; an L6[L3] lead | `packs/fl_cells_food` sheet: a layered cell eats, turns binucleate (t≈270-440), reorganizes into a multi-compartment "morula" of 6-8 ringed compartments (t≈1040-1200), releases dozens of small ring "spores" (t≈1300-1480) and shrinks back to one small ringed cell. The spores then tile the domain (t≈2000). | One seed. The spores are not the parent kind, and the run ends in a sea. Channel composition drifts during growth. |
| `fl_morph257` (one rule, two morphs + food) | L5 (binding/unbinding, engulfment), Weak | `packs/fl_morph257` sheet: one patch sorts into orange rings and cyan crescents that multiply (0 nucleations). Crescents often cup a ring. At t≈790-1100 a large cyan ring encloses 1-2 orange cells (a vesicle), then reopens (t≈1150). `evo/morph257_s0.png`: body composition is bimodal (pure A0 rings / pure A1 crescents). Of 30 clean divisions, 20 are A0+A1 composites splitting into one of each; pure parents divide true 5/6. | One seed. Uptake is proportional to A_c, so composition heredity is partly built into the operator. |

## 3. Mechanisms learned (with ablations)

- **Mass conservation makes bounded bodies cheap but motion and growth rare.** Of 16 C=1 and 12 C=3 random rules, all formed one bounded body per patch and almost all were static and radially symmetric (`screens/base_*`, `screens/c3_*`). At R_scale 0.4, 2-channel rules are far more often motile than 3-channel ones: 2 of ~60 C2 rules made glider swarms (r202, r226) and several made crawlers, while 0 of 7 C3 rules did.
- **A closed body cannot reproduce repeatedly.** Fixed mass means one division at most. Food conversion (`eat = k·phi·q/(1+q)`, `q=(A/K)^n`) plus decay back to food gives a birth-death balance with a conserved total. **The Hill gate (n=3) is essential**: with linear uptake (n=1), the faint halo every body sheds starts eating too and becomes a space-filling lattice of matter (`packs/scr_food_r0`, "grey goo").
- **Membrane = the pressure term.** Removing the `-alpha·grad(A)` term (theta=1000) keeps the cells bounded, but the continuous ring breaks into dots (`screens/abl_cells_nopressure.png`).
- **The food field turns bodies into foragers.** Food diffuses but does not flow. Gliders therefore carve depletion wakes and cannot graze their own trail. The population levels off when food reaches ~50%.

## 4. Negative results

- Linear uptake (n=1): grey goo for rule 0; rule 202 gives fewer, larger gliders plus diffuse matter.
- Too much food (food0 0.3): gliders overgrow into a space-filling foam of nucleated cells (L1 sea).
- Selection: **4 founder pairs × 10 seeds at 96²** (`evo/t96_fs*.log`) gave kind0 7/3, 6/4, 3/7 and 6/4 wins. At 128², pair 1 went 1/2 and pair 2 6/9. No pair has a consistent winner (the best is 7/10, p≈0.17), and the mutation genealogy matched a neutral control. Exclusion happened, so the dynamics are close to neutral for (m,s,h) changes of 15-25%.
- Layered cells with fixed-ratio uptake (`eat_split`) keep their layers but grow into a tube that wraps the domain at food0 0.3 (`screens/cellfood_split_long.png`). They never divide.
- A lower food level (0.075) gives fewer gliders but the same split/merge churn and no clean 2-generation chains.
- Center-of-mass travel is a useless screen when there are several bodies, because their motions cancel. The images were needed.
- labkit bug fixed in its own commit (80b2742): `run_pack` ignored `META["threshold"]`, which world.py documents. Thin crescent bodies flickered between 1 and 3 components without it.

## 5. Next sprint

1. **Selection that works.** Measure fitness directly: run head-to-head competitions in 20+ seeds at 96², with larger founder differences and with h (speed) only. Add a negotiation-style mixing rule (Michel et al.: the parcel with the higher local growth wins). The literature reports that averaging and passive sampling give almost no evolutionary activity.
2. **Cleaner reproduction evidence.** Lower glider density or add mild repulsion between bodies so lineages are not cut by collisions. Run a longer dt/2 pack.
3. **Combine the lines.** The layered-cell rule in the food world already grows, compartmentalizes and sporulates (`fl_cells_food`). Next, tune it (decay, uptake gate, per-channel uptake) so that the spores grow back into layered cells: a life cycle and L6[L3]. Fork from lenia-multichannel if their membrane rules are better.
4. Needs: nothing new. A 2x faster RT (the sampling transport costs 18 ms/step) would make 20-seed tournaments affordable.
