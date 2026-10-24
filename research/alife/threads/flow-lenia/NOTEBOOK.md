# flow-lenia notebook

Sprint 1 started 2026-10-24 14:28 UTC.

## E1. Reference Flow-Lenia re-implementation (`worlds/fl_base`)
numpy port of Plantec et al. 2023 (priors from erwanplantec/FlowLenia): k=10 kernels, kernel radius
(R+15)r, Sobel gradients, alpha=clip((A_c/C)^2), reintegration tracking with sigma=0.65, dd=5, dt=0.2,
periodic. Scatter implementation: every source cell spreads its mass over the 3x3 cells its 1.3-wide
square can touch (np.bincount). 128^2, C=1: 400 steps in 3.5 s.
- **Mass conservation: drift 2-4e-12 after 600 steps for every rule tried** (24 rules, C=1 and C=3).
- C=1, 16 random rules, one 40x40 noise patch (screens/base_r*.png): every rule gives ONE bounded
  body; 14/16 are static, radially symmetric "cells": ring + core (r5, r15), nested rings (r13), ring
  with a dotted interior lattice (r0, r11), rim + internal "organelles" (r2). r8: asymmetric body that
  slowly drifts/reshapes; r12: breaks into ~10 small blobs (debris-sized). No gliders.
- C=3, 12 random rules (screens/c3_r*.png): bounded bodies with **channel layering**: e.g. r0 =
  cyan interior with a dot lattice, orange rim ring, magenta dotted outer halo; r9 = concentric
  magenta/cyan/orange shells; r1 magenta membrane around a cyan core. Again mostly static. r2, r7
  begin to rotate / break symmetry late (t>400).
- Reading: mass conservation + the alpha term (pressure when crowded) gives sharp bounded bodies
  for almost any rule: boundedness is cheap in Flow-Lenia; motion is not (a centred symmetric patch
  gives a symmetric body).

## E2. Many bodies: smaller kernels (R_scale 0.4), 6 noise patches (screens/pop_r*.png)
C=3, 128^2, 1000 steps. Each patch condenses into its own layered body; overlapping patches give
elongated bodies. Mostly static. r7: an elongated body splits into 2-3 round bodies by t~600 (one
split event, mass is fixed so it cannot repeat). r8: blobs crumble into ~50 small membrane-bound
cells (cyan rim, pink core). r3/r6: bodies plus a shed cloud of dots.
- Reading: with mass conserved, a body above a preferred mass splits; below it, nothing can grow.
  Division can therefore happen at most once per unit of initial mass -> need a matter source.

## E3. Metabolism with a conserved total (`worlds/fl_food`)
New operator: food phi (diffuses, does not flow). eat = k_eat*phi*q/(1+q), q=(A_sum/K)^n, distributed
over channels in proportion to A_c; every channel decays to food at k_dec=0.002. sum(A)+sum(phi)
conserved to 8e-12 (checked over 1500 steps).
- n=1 (linear uptake), food0=0.3 (screens/food_r*.png, packs/scr_food_r0): matter x4.6.
  r0: the 3 founding cells grow, **divide** (t~140-190 in pack time) and turn into ~12 motile
  "comet" cells with food-depletion wakes. BUT the faint halo the cells shed becomes a
  space-filling lattice of matter dots that also eats ("grey goo"): a sea of matter in the
  background (channel A0 x6.6). r6: labyrinth (L1). r8: blobs crumble to motile particles with
  wakes, number decays as food is used up.
- n=3, K=0.3 (Hill uptake: only dense matter eats) (screens/foodH_r*.png, foodH3_*): the r8 sea is
  gone. r8 becomes a population of **worm-like chains with a cyan sheath around a bead core** that
  grow, break and merge; they stay where food is depleted and leave food-rich patches. r0 still
  makes the background dot lattice (its shed dots are dense enough to pass the Hill gate): negative.

## E4. Random-rule search for self-propelled bodies (scripts/motion_search.py, screens/mot/)
One 20x20 noise patch, 96^2, R_scale 0.4, 800 steps; ~60 C=2 rules (r200-259) and 7 C=3 rules.
C=2 is much richer than C=3 at this scale. Hits (looked at every image of the top 12):
- r202: the patch breaks into ~7 small crescent gliders (orange cap, cyan body) that persist and
  travel far. **Chosen for the forager line.**
- r226: several morphs at once (ring with nucleus, two-dot cell, crescent), all moving.
- r253: two bilateral gliders; r201: a symmetric body that bends into a moving chevron;
  r206: slow bilateral crawler; r208: a big cell with an orange "handle" and cyan internal lobes.
- r257: one rule, **two coexisting morphs** (orange rings, cyan ellipses) from one patch.
- r232, r222: the body crumbles into 6-8 small round cells.
- Most C=3 rules at R_scale 0.4 stay one static body. COM travel of total mass is a poor screen
  with several bodies (they cancel); images were needed.

## E5. Gliders + food = foragers that divide (`worlds/fl_forager`, packs/scr_forager)
fl_food operator on rule C2_r202, food0=0.1, Hill uptake n=3, K=0.3, k_eat 0.05, k_dec 0.002.
- food0 0.3: gliders eat, grow and become a space-filling foam of nucleated cells (screens/glfood_a,
  pretty but a sea). food0 0.06: only 2-3 gliders survive (screens/glfood_f0.06).
- food0 0.1: 1 patch -> 3 gliders -> grow -> elongate -> **split**; ~12-15 crescent gliders at t=800,
  each leaving a dark food-depletion wake. matter still rising slowly at the end (x5-8 per channel).
- tracking needed an absolute threshold (0.15); labkit ignored META["threshold"] (bug, fixed in a
  separate commit 80b2742). With it: 139 tracks, 49 splits, 40 merges, 2 persistent splits, max
  generation 2. Gliders collide and merge often, which resets tracks; lineage.png is a staircase.

## E6. Heredity: parameter localization on the forager (`worlds/fl_forager_evo`)
Every cell carries (m, s, h) of all 10 kernels, mixed by stochastic sampling (one incoming parcel
wins per cell, p ~ mass). Two founders on the same kernels: founder 0 = rule 202, founder 1 =
rule 202 with (m,s,h) * exp(0.25 N(0,1)) (founder_seed). Two patches of each. Rendering: matter
split by nearest founder (orange = kind0, cyan = kind1).
- founder_seed 2 (screens/evo_fs2): kind1 (cyan, ring/ellipse morphs) displaces kind0 (orange
  crescents): by t=4000 almost all bodies are cyan.
- founder_seed 1 (screens/evo_fs1): both kinds persist to t=4000 with distinct morphologies.
- 18 ms/step at 128^2 (sampling uses a lexsort), so 4000 steps ~ 75-170 s.

## E7. Forager ablations and 3-seed pack (packs/fl_forager, screens/abl_forager_*)
- **No food (k_eat=0)**: gliders shrink and dissolve by t~250 (1300 steps); all matter returns to
  food. -> the bodies depend on uptake (metabolism, L4c ablation).
- Linear uptake (n=1): only a few large gliders + faint diffuse matter (worse).
- packs/fl_forager seeds 0-2 (4000 steps, 128^2): 1 patch -> 10-14 gliders, **0 nucleations in every
  seed** (every body descends from the patch by division), 40-49 splits, 29-40 merges, max generation
  1-2 by the labkit tracker. Food falls to ~50% and the population levels off.
- scripts/division_chain.py: clean divisions (both daughters live >= 10 frames 1-to-1): 18/22/13 per
  seed; two-generation chains 0/3/1. packs/fl_forager/seed1/divisions.png shows patch -> split ->
  daughter divides again (f49), and an elongated body dividing (f65) whose daughter divides (f136).
  Daughters are the same kind of crescent/ring glider, but morphology is somewhat variable
  (crescent, C-ring with a nucleus, small ring).

## E8. Two-kind competition (evo/fs1.png, evo/fs2.png; 6000 steps, seeds 0-2)
Total matter saturates near 1500 (food ~750): a closed resource. In 5/6 runs one kind ends with >85%
of the matter (competitive exclusion); fs1 seed 0 still coexists. But the winner depends on the seed
(fs1: kind1 wins 2/3; fs2: kind0 wins 2/3), so these runs do not separate selection from drift.
fs2 seed 1: the winning kind1 makes ~50 small bodies vs ~15 for kind0: body size is heritable
with the parameters.

## E9. Mutation with genotype ids (`worlds/fl_forager_mut`, evo/mut_muller.png)
One founder; with probability 0.003 per step a disk of radius 12 around a mass-weighted random cell
(about one body) gets (m,s,h) *= exp(0.15 N); every genotype id inside gets a new child id (parent
table). Sampling transport keeps P and id exactly paired, so genotypes are discrete and heritable.
8000 steps: 62 mutations, phylogeny depth 7; at the end the root holds 36% of the matter, and
derived genotypes at depth 2-4 hold the rest (top: id 36 depth 4, 19%). Many lineages go extinct.
Needs the neutral control (same events, mut_size 0) before any selection claim.

## E10. Layered cells (`worlds/fl_cells`, packs/fl_cells, packs/fl_cells_damage)
C=3 rule 0 at R_scale 0.4, 6 noise patches. Every patch condenses (t<16) into a cell with three
radial layers in different channels: cyan core, thin continuous orange ring, magenta outer crown of
beads. 5-9 persistent tracks per seed, live the whole run, constant size. Two overlapping patches
make a stable elongated two-nucleus cell; in seed 1 two touching cells fuse into one at t~240.
- Damage (packs/fl_cells_damage, seeds 0-2, 38-44% of the largest body erased at t=120): the body
  re-forms core/ring/crown within ~40-90 time units, smaller (mass is lost). Undamaged controls =
  packs/fl_cells same seeds.
- Ablations (screens/abl_cells_*): no pressure term (theta=1000, alpha~0): bodies stay bounded but the
  continuous ring breaks into dots and the core clumps -> the -grad(A) pressure makes the smooth
  membrane. sigma 0.45: smaller dotted cells. **dt halved (0.1, 2x steps): core/ring/halo layering
  is kept but the beaded crown becomes a smooth halo** -> the beads are a dt-dependent feature.

## E11. Numerical / robustness checks on the forager
- dt halved (0.1) with all metabolic rates halved (same physical time): gliders form, forage and
  multiply to ~20 (screens/abl_forager_dthalf.png). Survives.
- +-10% on food0, k_eat, k_dec, D_food, K_eat (screens/jit_forager_*.png): same behaviour; at +10%
  some bodies overgrow into large static target-ring cells.

## E12. Neutral control for mutation (evo/mut_neutral*.png)
Same seed, same mutation events (rng draws identical), mut_size 0: 74 neutral "mutations", phylogeny
depth 7, final root share 9% vs 36% with real mutations; mean matter-weighted depth 2.9 vs 1.7.
Clade turnover is at least as large without any parameter change -> the genealogy of the real run
is consistent with drift; if anything real mutations are purged (root keeps more). No positive
selection detected (one paired run; needs replicates).

## E13. One rule, two morphs, food (`worlds/fl_morph257`, evo/morph257_s0.png)
Rule C2_r257 in the forager world: 1 patch -> ~25 bodies of two morphs: pure-A0 rings ("O") and
pure-A1 crescents ("C"); body composition is strongly bimodal. 30 clean divisions in 6000 steps:
20 are O+C composites coming apart into one O and one C (binding/unbinding, an interaction), pure O
parents gave O+O 4/5 times, pure C gave C+C 1/1. Caveat: uptake is proportional to A_c, so a pure
body can only make its own channel: composition heredity is built into the metabolism operator.

## E14. Founder tournament at 96^2 (evo/t96_fs*.log, 3000 steps, 10 seeds per pair)
Winner = kind with more matter at the end. fs1: kind0 7/10 (at 128^2 it was kind1 2/3).
(more pairs below when finished)
fs2: kind0 6/10 at 96^2 (6/9 at 128^2; pooled 12/19, one-sided binomial p~0.18). When kind1 wins it
holds its matter in 2-3x more bodies (10-14 vs 1-3 kind0 bodies at similar mass): body size breeds
true with the parameters even though fitness is not detectably different.

## E15. Layered cells + food (screens/cellfood_*.png)
fl_food on the fl_cells rule (C=3 rule 0) with a steeper gate (n=4, K=0.6): no grey goo at food0
0.15. Cells eat and elongate into rods with an axial core (cellfood_a, 4000 steps); with k_dec x2
they stay round. food0 0.2 for 10000 steps (cellfood_long): a cell grows into a multi-compartment
"morula" (~6 internal compartments with their own rings, t~5500), then breaks up into ~100 small
orange dots that tile the domain (L1 sea by t~8000). Sporulation-like, but the offspring are not
the parent kind: negative for L6[L3] so far, the most interesting lead for sprint 2.

## E16. Lower food for cleaner forager lineages (food0 0.075, seed 1, 6000 steps; not kept)
7 gliders at the end, 24 splits / 18 merges, 14 clean divisions, 0 two-generation chains. Fewer
bodies does not stop the split/merge churn: daughters usually re-merge or collide before dividing.

## E17. Layered cells + food as a pack (`worlds/fl_cells_food`, packs/fl_cells_food)
A full sequence over 10000 steps: layered cell -> binucleate (t~270-440) -> the composition shifts
to orange -> multi-compartment "morula" (6-8 ringed compartments, t~1040-1200) -> releases dozens of
small ring "spores" (t~1300-1480) and shrinks to a small ringed cell -> the spores tile the domain.
The composition shift happens because the three channels move with different flows and uptake is
proportional to A_c, so the channel that grows fastest takes over.
- Mutation `eat_split=[.34,.33,.33]` (new matter made in fixed channel proportions;
  screens/cellfood_split.png, 8000 steps): no morula and no spores. The cells keep the
  core/ring/crown layering while growing slowly into long rods. A 20000-step run with food0 0.3 is
  in screens/cellfood_split_long.png (see report).
- cellfood_split_long (food0 0.3, 20000 steps): the cells grow into a layered tube that wraps the
  periodic domain; there are internal "nuclei" but no division. Negative.

## E18. fl_morph257 pack (packs/fl_morph257, 6000 steps)
The patch sorts into orange rings and cyan crescents (0 nucleations; 13 bodies at the end).
Crescents often cup a ring (composites). t~790-1100: a big cyan ring closes around 1-2 orange cells
(a vesicle with inclusions), then opens again (t~1150). Interaction motif for sprint 2.

## E14 (final). Founder tournament, 96^2, 3000 steps, 10 seeds per pair
kind0 : kind1 wins = fs1 7:3, fs2 6:4, fs3 3:7, fs4 6:4. 40 runs, nothing distinguishable from a
coin flip (best 7/10, one-sided p~0.17). Exclusion (one kind >80% of matter) in most runs. Reading:
with sampling transport and 25% (m,s,h) differences, competition outcome is set by stochastic
history (which bodies collide/merge first), not by the parameters. Sprint 2 needs either larger
effects (different kernels, speed) or a mixing rule that lets fitter matter win at contacts.
Sprint 1 ended 16:19 UTC.

# Sprint 2 (started 16:37 UTC)

Committee digest read. Lab convergences: gated mobility for containment; consumed resource plus
maintenance cost; L7 bar = variation arising in the run + neutral control at the same mutation
rate + >= 3 seeds. Challenge: fork a mechanism from another thread.

## S2-E1. Heritable uptake gene (`worlds/fl_forager_gene`), forked protocol
Fork: the "heritable rate allele carried by the body, mutated during the run, plus a neutral
control" protocol of active-droplets/ad5-evolve and autopoiesis/phase_trait, ported into the
forager. Every parcel carries log g (eat *= g) and a genotype id, moved with the matter by the
same stochastic sampling as sprint 1. Mutation: with p=0.004/step, a radius-8 disk around a
mass-weighted random cell (about one body) gets log g += N(0, 0.2), one draw per event. Neutral
control: gene_active=False, so the same mutation process runs but g has no effect (a marker).
- 3 seeds x 8000 steps + 3 seeds x 12000 steps per condition (evo2/gene_all.png).
  Final matter-weighted mean log g. Selection: -0.17, +0.34, +0.45 (8k); +0.73, +0.68, +0.54 (12k).
  Neutral: -0.07, -0.06, +0.11 (8k); -0.05, -0.24, +0.01 (12k). Mann-Whitney U = 31/36,
  one-sided p~0.008. The selection trajectories rise steadily; the neutral ones wander around 0.
- Phenotype (packs/fl_forager_gene/seed3 sheet): the high-g (orange) lineages that win overgrow
  into a few large, slow multi-ring cells. The small, low-g (cyan) gliders disappear. Selection
  for uptake drives gigantism and loss of motility in this seed; seeds 4-5 kept ~20 bodies.
- One selection seed (0) went down (-0.17): the population fell to 3-7 bodies, so drift dominates.

## S2-E2. Predator-prey Flow-Lenia (`worlds/fl_predator`)
Two glider species, both with rule C2_r202, in separate channel pairs with their own pressure
term. Prey eat food (Hill uptake). Predator matter converts the prey matter it overlaps (kill =
k_pred·prey·q_pred/(1+q_pred), mass-conserving) and decays to food at 0.003. Chase:
U_pred += chase·blur12(prey). Flee: U_prey -= flee·blur12(pred). Total mass is conserved to 6e-13.
- Screens (screens/pred_*.png): chase 2 -> the predator cannot find prey and dies. chase 30,
  k_pred 0.05 -> prey exterminated by t~1800, then the predators starve (total extinction).
  Weak predators die early. **flee 60 with chase 20, k_pred 0.03: coexistence.**
- packs/fl_predator seed0-2 (12000 steps): coexistence in 3/3. Prey go through 2-3 boom-and-crash
  cycles (to ~3.6x, crashing when predators peak), and predator matter tracks prey with a lag
  (packs/fl_predator/populations.png). Minimum predator matter 25-57, minimum prey 182-283.
- Ablations (8000 steps): chase=0 -> predators starve by t~2700 and prey persist alone. flee=0 ->
  prey exterminated, then predators die (extinction). Coexistence needs pursuit AND evasion.

## S2-E3. Heritable prey flee gene under predation (`worlds/fl_predator_gene`, evo2/pgene.png)
The prey carry log f (flee *= f), transported with prey matter by sampling. Mutation p=0.004/step,
N(0, 0.3). 8000 steps, 3+3 seeds. Selection: +0.19, +0.16, +0.23. Neutral: +0.24, +0.25, +0.29.
No difference. All 6 drift up, controls included: an unexplained bias (the uptake-gene controls
centre on 0). Coexistence held in all 6 runs. Negative / inconclusive.

## S2-E4. Maintenance cost on the uptake gene (cost 1.5: decay *= g^1.5; evo2/gene_cost.log)
Prediction from R* (break-even food = k_dec g^0.5 / k_eat): mean log g should fall. Result after
8000 steps: +0.14, -0.23, +0.32. Not supported; the outcome looks like the no-cost runs. Selection
on g probably acts through growth during colonization, not through the steady-state food level.
Sprint 2 ended ~18:25 UTC.

## Corrections after the sprint 1 review (append-only; the earlier entries stand as written)
- E13/E18: in fl_morph257, channel A0 renders **cyan**, not orange (labkit palette: channel 0 is
  cyan, channel 1 orange). So "pure A0 rings" are the cyan bodies; the O/C labels are by
  composition, not colour.
- E6: the kind names are swapped. In the evo renders kind0 (founder) is cyan and kind1 (variant)
  orange. The text of E6 says the opposite.
- E12: the "identical-event" neutral twin is not identical: it had 74 events vs 62, because the
  event times come from the same rng, whose stream diverges once the dynamics differ.

## S2-E5. Committee main experiment, cut-down first pass (review reached this session 18:23)
fl_forager_evo with `h_factor`: the variant differs from the founder only in localized h. Arms:
h x0.5 and a same-founder neutral arm (h x1.0001, so the kinds stay distinguishable). 96^2,
3000 steps, 6 seeds each, stochastic sampling only. Negotiation not run yet.
Result (evo2/dose_*.log; kind1 = variant). h x0.5: variant/founder matter 99/1020, 736/339,
542/571, 1049/69, 559/558, 565/516, so the variant has the majority in 4/6 (two of those are 50:50).
The variant always makes more, smaller bodies (8-15 vs 0-11). Neutral (x1.0001): kind1 majority
3/6. Even halving h is not a clear fitness difference under sampling: the coin-flip outcome the
committee named as "redesign heredity first", though only for one rule and 6 seeds. Contrast with
S2-E1: the uptake gene acts on the birth-death balance directly and IS selected (p~0.008).

# Sprint 3 (final; started 19:36 UTC)

## Corrections after the sprint 2 review
- S2-E1: Mann-Whitney U = 31/36 gives an exact one-sided p of 19/924 = **0.021**, not 0.008.
  REPORT_r2 is corrected.
- S2-E1: the neutral arm was rate-matched, not identical-event (seed 0: 99 vs 83 events).
  Fixed in fl_forager_gene2: mutation times, location quantiles and effect draws come from their
  own RNG stream, so S and N share every event time and draw.
- S2-E2: ablation times were given in steps. In t (dt = 0.2): predators starve by t~540
  (chase=0), and extinction comes by t~540 (flee=0).
- labkit v0.2 dropped the META["threshold"] fix again; re-applied in its own commit (03676da).

## S3-E1. Level-of-selection audit (`worlds/fl_forager_gene2`, scripts/record_gene.py, audit_gene.py)
Arms (128^2, 12000 steps): S (gene, per-parcel uptake), N (identical-event neutral twin: same
event times, location quantiles and effects from rng_mut), S_body (uptake uses
g_eff = blur5(A g)/blur5(A), so parcels within a body share one rate). N_body is not run: with
the gene inactive, body_pheno has nothing to act on, so N_body is bit-identical to N (checked on
seed 0: -0.008 for both).
Snapshots every 20 steps. Bodies are periodic components of blur1(A) > 0.15. Main parent =
largest overlap. Price split per interval (exact identity, checked: the terms sum to the total):
between-body (growth, fission and death of bodies), within-body (1-parent children), fusion
(>=2-parent children). "Persistent" fission = >= 2 daughters that each continue 1-to-1 for
>= 10 intervals (200 steps). The raw labkit-style generation counts (40-49) are flicker.
Results so far are in evo3/audit*.json and the REPORT_r3 table.
- Seed 0: S +0.527 = between +0.689, within +0.472, fusion -0.634. 18 bodies, all high-g, at the
  end. Visually (evo3/sheet_S_s0.png) a gradual sweep of small orange gliders through ~20 motile
  gliders. Twin N -0.008 (between -0.233, within +0.031, fusion +0.195: noise of order 0.2).
- Seed 1: S +0.582 = between +0.256, within +0.526, fusion -0.199. 1 body at the end.
  evo3/sheet_S_s1.png: orange gliders appear and multiply (t~312-416), grow into multi-ring
  giants, fuse, and absorb the last pale cell (t~1880): gigantism, then within-body dominance.
- S_body seed 0: +0.559, but 2 bodies at the end (within +0.51 dominates). The body-scale
  phenotype does not prevent gigantism.
- Seed 2: S -0.198 vs N -0.224. The twins end nearly identical: in this seed selection did
  nothing measurable.
