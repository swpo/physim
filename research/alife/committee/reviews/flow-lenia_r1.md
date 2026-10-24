# Review: flow-lenia, sprint 1 (2026-10-24)

**Decision: CONTINUE** (promise 7/10). **Headline:** `fl_forager` is a reproduced **L6[L2]+L4b**. Adding Hill-gated uptake from a conserved, non-flowing food pool to a Flow-Lenia rule that already glides produces motile crescents. One noise patch grows into 8-14 of them by fission, with 0 nucleations in 4 seeds, and the skeptic reproduced this on seed 11 and at 2x resolution. `fl_cells` is **L4a[L3]**, and its layering converges under a resolution change. Selection is **not** detectable yet: the 40-run tournament is a coin flip, and the mutation run matches its neutral twin. Sprint 2 must find out whether this substrate can show selection at all.

## Consensus

| world | judged rung | conf. | key observation | pack |
|---|---|---|---|---|
| fl_forager | **L6[L2]+L4b**; L4c, L5, L3 Weak | medium | 0 nucleations in 4 seeds (3 packs plus skeptic seed 11), with 2-generation chains in seed 1 (`seed1/divisions.png`: loop splits at f65, a daughter buds at f136), seed 2 (f15→f74) and seed 11 (#2→#4 at t≈78→#22 at t≈317; labkit gen 3). Crescents keep their shape for ~180 t and travel 7-13.7 BL. The parent rule glides without food (`screens/mot/C2_r202.png`). Merges are ~80% of splits, so the genealogy is reticulate. | threads/flow-lenia/packs/fl_forager |
| fl_cells (+damage) | **L4a[L3]** | medium | A0 core, a 1.5-px A1 ring that is 0 inside and outside, and A2 shells. The radii agree at 2x resolution (`judge-scratch/flow-lenia-r1-skeptic/cells_radial.png`). 38-44% cuts on 3 seeds re-form the ring and crown against undamaged twins. The repaired cell is smaller and has a hollow core. The cells are static, and each planted patch gives one cell. The beaded crown is numerical. | threads/flow-lenia/packs/fl_cells_damage |
| fl_morph257 | **L2**; L5, L4b, L6 Weak | low | Orange A1 rings and cyan A0 crescents sort out from one patch. Cupped pairs last 500-650 t (#206, #302), and a cyan ring encloses orange cells (t≈788-1100). 20/30 composite divisions give one of each. One seed. | threads/flow-lenia/packs/fl_morph257 |
| fl_forager_mut | **L2**; L6, L7 Weak | low | New morphs persist (#64 compact solid body, #91 target cell), but the identical-event neutral twin shows as much turnover (root share 9% vs 36%). 177 splits vs 169 merges, gen 0. One pair. | threads/flow-lenia/packs/fl_forager_mut |
| fl_forager_evo | **L2**; L5 Weak; L7 Contradicted | medium | One kind is excluded in 5/6 runs, but the winner is a coin flip (7:3, 6:4, 3:7, 6:4). There is no monoculture control, and conversions at contact were not counted. | threads/flow-lenia/packs/fl_forager_evo |
| fl_cells_food | **L2** (spot lattice at the end); L3 Weak; L6[L3] Contradicted | medium | Binucleate cell, then a 6-8-compartment "morula" (t≈1040-1200), then A1 dots tile the box. There are 257 nucleations, and A0/A2 are already −99.8%/−97.6%, so the "spores" condense from shed matter. One seed. | threads/flow-lenia/packs/fl_cells_food |

## Judges and arbitration

**Biologist (promise 7).** Gave a careful body-plan reading: an A1 cap with A0 trailing mass, and a figure-8 doubling before division. Rated fl_forager L6 Weak, because fusion nearly equals fission and only ~2 chains are credible. Proposed the thread's best hypothesis: fusion plus parameter mixing makes bodies chimeric and swamps both lineage and selection.

**Skeptic (promise 7).** Ran four reruns:
- seed 11 reproduces fl_forager in full;
- at 2x resolution (R_scale 0.8, flow ×4), fl_forager keeps gliders, wakes and a division, but the crescents turn into speckled ring-in-halo bodies, so shape has not converged;
- fl_cells profiles converge at 2x resolution.

The key methodological finding: reintegration tracking spreads mass with a fixed σ every step, so **dt/2 doubles numerical diffusion and is not a convergence test**. That is why the crown beads vanish at dt/2. The skeptic rated L4a Weak (hollow core).

**Curator (promise 7).** Novelty is modest against Plantec et al. Fig. 6f, Michel et al. and in-lab phase_swimdiv/kstrail. The distinguishing claim to make explicit is that propulsion, growth and division all come from one local rule plus a conserved resource, with no per-body drift. fl_forager is the best PhySim world here. The thread risks breadth: 4 of 6 candidates rest on one seed.

**Disagreements.**
1. *fl_forager L6.* I examined seed1 and seed2 `divisions.png` and the skeptic's seed-11 sheet: a crescent at t=68 is two at t=88, and the population is 8-10 bodies by t=500, all from the patch. **Supported, medium.** Every body descends from the patch by fission (0 nucleations), and 2-generation chains appear in 3 of 4 seeds, one of them an independent judge seed. Daughters are plastic forms of one two-part body plan, which meets "same kind" at [L2]. The biologist's reticulation point stands as the confidence limit.
2. *fl_cells L4a.* In `fl_cells_damage/seed0/sheet.png` the cut 2-nucleus body (t=122) re-forms core, ring and crown by t≈208 and holds them to t=400. This meets the rung on 3 seeds with twins and mature, non-dividing cells. Re-condensation by attractor is scored under mechanism and novelty, not the rung.
3. *fl_forager_evo L4b* (curator: Supported). One seed is capped at Weak.

## Next sprint

**Main experiment: can selection show in this substrate? A dose-response with a positive control under two mixing rules.**
- **Setup:** fl_forager_evo at 96², 3000+ steps as in E14. A founder competes against a variant that differs **only in localized h**, at ×0.9, ×0.75 and ×0.5. A same-founder neutral arm sets the 50% baseline.
- **Mixing rules:** current stochastic sampling vs **negotiation** (Michel et al.; β=100, V = local growth, Q carried with matter; LITERATURE Flow-Lenia section). That is 8 arms × ≥12 seeds, about 1 CPU-hour at E14 cost.
- **Monocultures:** run each variant alone on 3 seeds, so viability and growth are known. This is also the matched L5 test.
- **Report per run:** winner and final share; **conversions of living bodies without division** (the autopoiesis phase_kinds lesson); per-division true-breeding rate.
- **Pass:** win rate rises monotonically with dose, with ≥10/12 at the largest dose under at least one rule, the neutral arm near 6/12, and the sweep carried by divisions rather than conversions.
- **If it passes:** in that rule, run fl_forager_mut with real mutations against identical-event neutral twins (≥5 pairs), and score derived-genotype share and depth.
- **If even ×0.5 is a coin flip under both rules:** mixing erases selection, and heredity must be redesigned before any more mutation runs.

**Secondary goals**
1. **Clean L6 and L4c in fl_forager.** Add one *local* anti-fusion ingredient; no per-body labels. Run 3 seeds × 2000 t with merge-aware lineage. Pass: ≥3 generations of crescent → 2 crescents per seed, daughters within ~30% of the parent's area, merges <25% of splits, 0 nucleations. In a twin of each seed, set k_eat=0 at t=600 (a starvation fork). Say plainly that the food dependence comes from the designed decay k_dec.
2. **fl_morph257 on 3 seeds.** Measure a contact-vs-null rate for cupped pairs and tabulate O→O+O, C→C+C and OC→O+C. If it holds, this is the thread's most novel result and a discoverable law.
3. **Numerics.** Validate the winning arm and fl_forager at R_scale 0.8 with flow ×4 (`judge-scratch/flow-lenia-r1-skeptic/mkres2.py`). Treat RT σ as a model parameter.

**Pause:** fl_cells_food life-cycle tuning, new rule screens, and static-cell variants.

## Cross-pollination

- **Out:**
  - **lenia-multichannel**, which plans to localize kernel parameters: stochastic sampling with 15-25% (m,s,h) changes is near-neutral. Use genotype-id transport and an identical-event neutral twin (`evo/mut_neutral_muller.png`).
  - **chemotaxis-motility**, whose target is dividing fed crescents: food that diffuses but does not flow stops re-grazing, and a conserved matter+food closure gives birth-death balance with no regrowth parameter. Their crescents should elongate and pinch, as in `fl_forager/seed1/divisions.png`.
  - **autopoiesis** and **active-droplets**: replaying the identical mutation event stream with mut_size 0 is a stricter neutral control than matching the rate.
- **In:**
  - autopoiesis: conversion counting (`packs/phase_kinds`);
  - active-droplets: within-body competition β decides whether a mutant can take over a body. Negotiation β plays that role here (`REPORT_r1.md` Mechanism 4, `packs/ad5-evolve` vs `ad5n-neutral`);
  - fisim-beyond-laplacian: per-division kinds accounting (`packs/xcell-her/seed0/kinds.json`);
  - chemotaxis-motility: pursuit cross-taxis between kinds, once selection is detectable.

## Rubric issues

1. **Numerical validity for reintegration transport.** dt halving with a fixed RT σ doubles numerical diffusion. Require a resolution change with kernels and flow scaled (R_scale ×2, flow ×4), or σ scaled with dt.
2. **L6 in fission-fusion populations.** Report the merge/split ratio. Supported needs ≥2-generation chains in ≥2 seeds and 0 or explained nucleations, and confidence is capped at medium when merges exceed 50% of splits. "Same kind" means the same body plan, not the same instantaneous shape.
3. **L4c.** When the researcher adds the maintenance cost (decay), and the rule without it lives indefinitely, the dependence is designed. That still counts for the rung, but it is scored under mechanism.
4. **labkit:**
   - merges end lineages, and generation propagates through merges as the maximum of the parents;
   - persistent_tracks = 0 for discrete motile foragers;
   - the A1 ring in fl_cells is segmented apart from the core, so the rim metrics miss the membrane;
   - static fl_cells seed 0 scores 2 persistent splits;
   - frames.npz is float16, so conservation cannot be audited.
