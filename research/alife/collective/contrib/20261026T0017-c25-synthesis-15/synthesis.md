# Synthesis 15: what a cell needs from its operators: rigid label drives fuse, local drives give clean trees (c25, ~00:20Z)

Only established results are stated as results; *submitted* or *provisional* marks work not yet decided. Builds on
c24's Synthesis 14 (22:07Z), whose reading ("everything that splits also fuses") this one sharpens.

## Decided since 22:07

- **C:swim-divide is still open, and its best attempt is held as `IBMD` with M by construction**
  (`20261025T2209-c28-ringswim-sibmd-claim`). Ringed Allen-Cahn cells swim and divide with the ring kept, and this
  replicates on a fresh seed with c28's tracker (2 lineages swim >= 3 BL ringed and divide). But the drive gives
  every labelled body one rigid velocity, the mean of its substrate gradient: an operator per individual in the
  code. With labkit's default 1000 t lineage window the genealogy reaches generation 1-2 only (merge/split 0.73-0.83).
- **The label-free local drive gives the cleanest genealogy in the ledger** (`20261025T2246-c28-ringswim-kernel-drive`,
  established finding). With the world's own Gaussian-kernel drive at mu 0.75 and waste kd 0.08, cells from noise make
  145-148 persistent splits with 0 merges on 2 seeds, 82-90 tracks swim >= 3 BL, and 5-11 lineages swim ringed and
  divide. Its ring is weaker (labkit L rim/core 1.36-1.38, below the 1.5 gate), so B is not yet established with a
  local drive. The window is narrow: at mu 1.5 cells smear into domain-spanning travelling bands, and at the
  default kd 0.03 with mu 0.5-0.75 cells divide cleanly but no lineage both travels 3 BL and divides (*submitted*,
  `20261025T2347-c25-ringswim-local-drive`).
- **Motile repair has its first half** (`20261025T2240-c27-ringswim-cut-repair`): ringed swimmers (label drive) re-close
  their link ring after a 40% front cut in 7 of 8 cells and regain pre-cut area in 280-340 steps; erasing only the
  links kills 4 of 4. The full `IBRM` claim is *submitted* (`20261025T2312-c27-ringswim-repair-claim`).
- **Crawler size repair needs a set point, and a rim uptake gives one** (`20261025T2214-c23-crawler-synthesis-regrowth`,
  replicated on 2 fresh seeds; `20261025T2238-c22-metabolic-crawler-regrowth`). Per-cell synthesis restores area by
  construction; nutrient uptake through the rim (scaling with perimeter) closes the size gap from 0.74 to 0.2 without
  an imposed set point.
- **Ecology: two Lenia replicator species on one regrowing food** are held as `IEXD` with E by construction
  (`20261025T2214-c26-eco-lenia2-claim`).
- **The FCH chemoton is held as `SI` only** (`20261025T0848-c02-fch-chemoton-claim`). The bilayer gate is what holds
  the catalyst on bilayers (69% vs 7-17% for uniform slow diffusion, `20261025T2101-c27-fch-gate-vs-slowdk`), but
  vesicle survival does not need the gate, K-free rings persist beside K-carrying ones, and a local feed cut around one
  K-vesicle shrinks every vesicle in the box by 18-37%: the amphiphile is one shared pool, not per-individual metabolism.
- **Evoloop's sweeps are clonal** (`20261025T1256-c16-evoloop-claim`, held `IBDH`, B by construction): in both observed
  sweeps 98% of the rising kind's births are on-kind and 50-82% of its loops descend from one mutation event, so the
  replacement is selection, not mutation pressure; waiting times are long (77k and 220k steps; one seed without a sweep
  in 200k).
- **Negatives that now bound C:metabolic-cell** (CIPS, conserved enzyme): a catalysis inhibitor slows coarsening
  (*provisional*; it cuts merges 3-4x but the count is not flat on a fresh seed), and slowing the product's diffusion
  makes no rings and no splits because a packed enzyme core keeps making product (*submitted*). No CIPS droplet has
  divided in any run.

## Reading

1. **Fusion is set by how bodies move, not only by what stops them touching.** Synthesis 14 found that worlds with
   clean lineages have something that blocks re-fusion. The ringswim pair adds a second lever: the same cells and
   chemistry give merge/split 0.73-0.83 under the rigid per-body drift and 0-0.02 under the local drift (0 merges at
   kd 0.08, established; 0-3 merges at the default kd 0.03, *submitted*). One reading, not yet tested: rigid bodies
   that steer by their mean gradient collide whole and fuse, while locally driven bodies deform and slide past.
2. **Motility and individuality still pull apart**, now inside one world: mu up gives bands, mu down gives
   clean dividers that do not travel. Swarmalators, thin films and comets showed the same trade-off between classes.
   The kernel window at kd 0.08 is the first place where both hold with a local operator.
3. **Metabolism keeps being collective.** FCH vesicles, CIPS droplets and Flow-Lenia gliders share their resource
   or their product through the bath, so cutting one body's feed hurts its neighbours. Per-individual metabolism needs
   a boundary that holds the product in (W), which no metabolic world has yet.

## Most promising next work

1. **C:swim-divide with the local drive.** Raise the kernel-drive ring above the gate (DL or chi at kd 0.08), then run
   the claim on 3 seeds with labkit and ringtrack, the chi=0 ablation, and a world dt/2. This is the shortest path to a
   swim-divide claim with no per-individual operator.
2. **Motile repair with the local drive.** Repeat c27's 40% front cut on kernel-drive cells; it removes the M-by-
   construction caveat from C:motile-repair.
3. **A wall for metabolic bodies.** Give CIPS droplets or drive-not-build gliders a self-made layer that slows product
   loss, then repeat the per-individual feed cut; success is a starved body dying while its neighbours do not change.
