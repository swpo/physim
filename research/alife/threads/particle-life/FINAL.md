# particle-life: final summary (sprints 1-3)

## Best worlds and the committee's consensus rungs

| world | what it is | consensus rung (committee r1/r2) | main caveat |
|---|---|---|---|
| `sporecell` (S1) | particle life with a stiff core, plus a closed chemistry: food F, catalytic core C, membrane M induced by food contact | **L2** (high); L3, L4a and L4c Weak; L6[L2] Weak | Rings are a reversible food-contact label and vanish when food is depleted. Spore release was a time-step instability (below). |
| `sporecell2` / `-sel` (S2) | adds majority-vote conformity (cells are pure, so a spore is a genetic bottleneck) and two kinds that differ in catalysis rate | L2; L7[L2] Weak | The sweep is fixed during colonization and fails at a 1.2× advantage, at dt=0.015 or 0.01, and on seed 11. |
| `sporecell2` + lysis (S2) | contact predation between kinds | **L5[L2] Supported** (low), on the dt=0.02 map only | Rare predators lose (a priority effect), so the interaction cannot evolve. |
| `sporecell2`, gate β=1 (S2) | food mobility gated by membrane density (forked from the lab's gated-mobility convergence) | L2; L3, L4a and L6[L2] Weak; L6[L3] Contradicted | Daughters are bare. |
| `plife-m2` (S1) | a random particle-life matrix: concentric type shells | L3, as a calibration (known result) | |
| `sporecell3` (S3) | sporecell2-sel with a step-safe integrator and explicit spore-release routes | see REPORT_r3 | |

## Mechanisms that worked (with ablations)

- **Closed particle chemistry gives reproduction through propagules.**
  - Catalysis F→C needs a C within 0.5, so cells cannot nucleate spontaneously and every new cell descends from shed matter.
  - Particle identity then gives exact matter provenance. No field thread has this.
  - The ablation k_cat=0 means no cells at all; switching catalysis off mid-run makes cells shrink at the decay rate.
- **Majority-vote conformity makes cells pure and kinds breed true.**
  - Without it (S1), mutants spread inside cells: purity 0.55–0.75, and kinds did not breed true.
  - With it, purity is 0.99–1.00 and 64/66 daughters of kind-1 parents are kind 1. The vote is what turns a single spore into a genetic bottleneck.
- **Contact killing creates a priority effect.**
  - With lysis the worse grazer holds territory on 3/3 seeds. In the ablation without lysis it is excluded.
  - Seeded at 15%, it loses on 3/3 seeds, as predicted. Frequency-dependent interactions need a front, and a rare mutant never builds one.
- **Core stiffness sets the cell scale.** A soft core (rep=1) collapses clusters to points; a stiff one (rep=10) gives cells about one interaction range across.
- **A long-range repulsion shell (B) sets territory and freezes turnover.** It is not needed for reproduction.

## Mechanisms that failed

- **Spore emission was a numerical artifact.**
  - At dt=0.02 the stiff core overshoots once cells pass about 70 particles. Free spores go 127 → 40 → 6 as dt halves twice.
  - Neither core noise nor a softer core fixed it. With a step-safe integrator, spontaneous release essentially disappears (sprint 3).
  - Lesson: **check dt-convergence of the reproduction event itself, before anything else.**
- **Every membrane rule tried is a label, not a material.**
  - The neighbour-count and geometric rules make dead or all-membrane cells.
  - The food-contact rule makes rings that vanish when food is depleted.
  - The turnover screen (deaths through dilution or decay cost) found no setting with a stationary population and rings on ≥80% of cells. Rings need free food, and a food-limited population consumes it.
- **Gating food mobility at the membrane** keeps the rings, but it also starves the core. Cells die at any maintenance cost above k_dec=0.01.
- **No motility:** designed chase matrices segregate the types instead.
- **Periodic Particle Lenia** from uniform noise gives foam or lattices, never separate cells.

## What transfers to PhySim worlds

1. **Identity-carrying matter with catalytic inheritance.** A conserved, labelled matter channel gives exact lineage and provenance for free: a hidden law an agent could discover.
2. **Majority-vote conformity** is a cheap, local operator that makes individuals genetically coherent. It applies to any multi-type field or particle world.
3. **Contact killing gives a frequency-dependent advantage, hence bistable territories.** That is a measurable, multi-level law.
4. **The method rule:** a discovery world needs the reproduction event to converge in dt. Step-safe integration (bounded displacement per step) should be the default for stiff particle systems.

## What a next lab should try

- A **material** membrane: M made from food by C, slow to decay, adhesive to C and repelling F, so the rings survive starvation.
- **Fission by an explicit physical route** (SALR or a surface-tension instability), verified to converge in dt.
- Identical-event twin arms throughout (all RNG draws unconditional) and merge-aware lineage from day one.

## Showcase movie

`movies/showcase.mp4`: see the caption at the end of REPORT_r3.md and below.
