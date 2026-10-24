# particle-life: final summary (sprints 1-3)

## Best worlds and the committee's consensus rungs

| world | what it is | consensus rung (committee r1/r2) | main caveat |
|---|---|---|---|
| `sporecell` (S1) | particle life with a stiff core, plus a closed chemistry: food F, catalytic core C, membrane M induced by food contact | **L2** (high); L3, L4a and L4c Weak; L6[L2] Weak | Rings are a reversible food-contact label and vanish when food is depleted. Spore release was a time-step instability (below). |
| `sporecell2` / `-sel` (S2) | adds majority-vote conformity (cells are pure, so a spore is a genetic bottleneck) and two kinds that differ in catalysis rate | L2; L7[L2] Weak | The sweep is fixed during colonization and fails at a 1.2× advantage, at dt=0.015 or 0.01, and on seed 11. |
| `sporecell2` + lysis (S2) | contact predation between kinds | **L5[L2] Supported** (low), on the dt=0.02 map only | Rare predators lose (a priority effect), so the interaction cannot evolve. |
| `sporecell2`, gate β=1 (S2) | food mobility gated by membrane density (forked from the lab's gated-mobility convergence) | L2; L3, L4a and L6[L2] Weak; L6[L3] Contradicted | Daughters are bare. |
| `plife-m2` (S1) | a random particle-life matrix: concentric type shells | L3, as a calibration (known result) | |
| `sporecell3` (S3) | sporecell2-sel with a step-safe integrator (displacement ≤ 0.05 per sub-step) and explicit surface detachment (k_det=0.05) | my claim: **L6[L2]** with dt-converged reproduction (pending committee). dt vs dt/2 agree within 6–12% on spores and cells; births within 8% (seed 0) and 20% (seed 1); merge-aware generation 2–3 | Short runs (t=200, 2 seeds). Release is a written-in rule. Deaths (16–23 per 100 t) outnumber qualifying births (5–6 per 100 t), with births counted conservatively. The displacement bound is active in dense cells. |

**Committee final verdicts (r3, program stopped).**
- `sporecell3-det`: L2 (high). L6[L2] is Weak (borderline). On a strict re-audit of `lineage2.json`, seed 0 reaches max gen 1 (#12 absorbs its parent #4; #90 is #82 crossing smin again). Seed 1 has one genuine 2-deep chain, #24→#33→#38, which `lineage2.py` scores gen None. The births form a colonization wave that freezes, and dt/2 with the displacement bound still active is not a full convergence test. L3 is Contradicted.
- Twin: L7[L2] Weak (one pair, colonization only).
- Earlier verdicts stand: sporecell2 with lysis L5[L2] (low, dt=0.02 map), `plife-m2` L3 (calibration), and L2 for every sporecell world.
- Known `lineage2.py` defects to fix before reuse: parent fusion (a daughter absorbing its parent) and smin hysteresis (a cluster crossing the 15-particle threshold again counts as a new birth).

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
- **Explicit surface detachment converges in dt (sprint 3).**
  - With step-safe motion, a detachment rate of k_det=0.05 for surface core particles restores propagule reproduction: about 30 stationary cells and merge-aware generation 2–3.
  - dt vs dt/2 agree within 0–12% on spores and cells. Births agree within 8% on seed 0 and 20% on seed 1.
  - Weaker detachment (k_det ≤ 0.01) and SALR fission give declining populations.

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
- **Heredity at the converged step is not established.** One selected/neutral twin pair (T=300): the kind-1 share rises 0.36 → 0.45 against 0.18 → 0.15 for neutral. But conversions of intact cells (4) rival kind-1 births (5), and there is only one seed.

## What transfers to PhySim worlds

1. **Identity-carrying matter with catalytic inheritance.** A conserved, labelled matter channel gives exact lineage and provenance for free: a hidden law an agent could discover.
2. **Majority-vote conformity** is a cheap, local operator that makes individuals genetically coherent. It applies to any multi-type field or particle world.
3. **Contact killing gives a frequency-dependent advantage, hence bistable territories.** That is a measurable, multi-level law.
4. **Merge-aware, identity-based lineage** (`lineage2.py`): continuation by particle overlap, births only from clusters with no previously clustered particle. This avoids the label ratchet that inflated earlier generation counts.
5. **The method rule:** a discovery world needs the reproduction event to converge in dt. Step-safe integration (bounded displacement per step) should be the default for stiff particle systems.

## What a next lab should try

- A **material** membrane: M made from food by C, slow to decay, adhesive to C and repelling F, so the rings survive starvation.
- **Fission by an explicit physical route** (SALR or a surface-tension instability), verified to converge in dt.
- Identical-event twin arms throughout (all RNG draws unconditional) and merge-aware lineage from day one.

## Showcase movie

`movies/showcase.mp4` (3.2 MB, 25 s, 301 frames, t = 0–240). It shows the whole periodic box (16 × 16 interaction ranges, 4,000 particles) of the gated-food `sporecell2` world (seed 1), with fixed colours per particle type: grey food, cyan core of kind 0, magenta core of kind 1 (the faster catalyst, which arises by mutation), orange membrane.
- From 15 scattered seed particles, cells nucleate and coat themselves in thick orange membrane rings, because the gate piles food against the rim.
- They grow slowly behind the ring, then burst (t≈110–175) into clouds of single-particle spores. Each spore catalyses food into a new, bare daughter cell.
- The magenta lineage, founded by mutation inside the first generation, colonises most of the box, while a few cyan cells persist.

Caveat: this run uses the dt=0.02 map. Its bursts are partly the stiff-core instability diagnosed in sprint 3, and the converged world (`sporecell3`) releases spores only through the explicit detachment route. It is shown because it is the most life-like behaviour the thread produced, not as converged physics.
