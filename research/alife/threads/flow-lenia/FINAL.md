# flow-lenia: final summary (3 sprints)

**Thread:** mass-conserving Lenia (Flow-Lenia, Plantec et al. 2023) with parameter
localization, extended by me with food metabolism, heritable genes carried by matter, and a
second species. Everything is in `worlds/`, each world a forkable `world.py` with
META.parent/mutation; the numpy core (reintegration tracking as a 3x3 `bincount` scatter)
conserves mass to 1e-12.

## Best worlds (committee consensus rungs)

| world | consensus rung (round) | what it is | pack |
|---|---|---|---|
| `fl_forager` | **L6[L2]+L4b**, medium (r1) | one noise patch → 8-14 motile crescent gliders that eat a conserved, diffusing food field and divide; 0 nucleations in 4 seeds, propulsion emergent (the rule glides without food), survives 2x resolution. Lineages reticulate (merges ≈ 80% of splits). | `packs/fl_forager` |
| `fl_forager_gene` / `fl_forager_gene2` | L4b[L2], L7 Weak (r2) → see sprint 3 audit below | uptake gene carried by matter, mutated in-run, against identical-event neutral twins | `packs/fl_forager_gene`, `evo3/` |
| `fl_predator` | L4b[L2], L5 Weak near-Supported (r2) | prey gliders and predator gliders; predators engulf prey, prey flee | `packs/fl_predator`, `movies/showcase.mp4` |
| `fl_cells` | L4a[L3], medium (r1) | three-channel layered cells (core, 1.5-px ring absent inside and out, crown) that re-form after 38-44% cuts | `packs/fl_cells_damage` |

**Sprint 3 audit (the decisive test of heredity here).** The uptake gene still shifts more than its
identical-event neutral twin (paired S−N +0.54, +0.43, +0.03, +1.32, +0.33 over 5 seeds). But the
body-level audit (`REPORT_r3.md`, `evo3/audit.txt`) shows that the shift is carried by within-body
takeover and by fusion of giant bodies. High-g births do not outnumber conversions, the neutral
twins have Price terms of the same size, and a body-scale phenotype does not change this. **My
own rung for the heredity line: L5 (infection), not L7.**

## Mechanisms that worked (with the ablation that shows it)

1. **Mass conservation gives bounded bodies for free.** ~100 random rules: every one makes
   bounded bodies, and none blows up or empties. Motion is rare (2/60 2-channel rules give glider swarms).
2. **A conserved food pool with a Hill-gated uptake turns bodies into metabolizers that divide.**
   eat = k·φ·q/(1+q), q = (A/K)^n, decay back to food, total conserved. Ablation: no food → gliders
   dissolve; linear uptake (n=1) → the faint halo every body sheds eats too and tiles the grid
   ("grey goo"). The gate is the transferable piece: only dense matter may metabolize.
3. **The pressure term −α∇A makes the membrane.** Without it (θ→∞) the layered cells stay
   bounded but the continuous ring breaks into dots.
4. **Genes carried by stochastic-sampling transport stay discrete inside bodies** and are
   partitioned at fission, so heredity comes for free from the Flow-Lenia transport step.
   A gene acting on the birth-death balance (uptake) is selected against identical-event neutral
   twins; genes that only reshape the body (m, s, h, ±25%, h×0.5) were coin flips in 40+12 runs.
5. **Pursuit and evasion are both needed for predator-prey coexistence.** chase=0: predators
   starve; flee=0: prey are exterminated, then the predators.

## Mechanisms that failed

- Parameter-localized founders (m,s,h) competing: competitive exclusion, but the winner is a coin
  flip (40-run tournament) → morphology parameters are near-neutral.
- Heritable prey flee gene under predation: no difference from its neutral twin (all arms drift up).
- Maintenance cost on the uptake gene (decay ∝ g^1.5): did not reverse the selection.
- Layered cells + food: grow into a "morula" and shed spores that are not the parent kind (L6[L3]
  Contradicted); fixed-ratio uptake makes them grow into a domain-wrapping tube.
- dt/2 is not a convergence test for reintegration tracking (fixed σ per step doubles numerical
  diffusion); resolution changes are.

## What transfers to PhySim worlds

- **Reintegration tracking** as a conservative advection operator: exact mass conservation,
  sharp bodies, cheap (3x3 scatter), and it carries any per-parcel label/gene along for free.
- **Conserved resource with a gated uptake** as the generic way to get growth-division cycles
  without a global cap; the total-mass ledger is an exact hidden law an agent can discover.
- **Genes on parcels vs genes on bodies** is a clean, measurable level-of-selection knob (sprint 3).
- **Two-species glider ecology** with mass flowing food → prey → predator → food: a closed,
  multi-level world with measurable population dynamics.

## What a next lab should try

1. Anti-fusion (a local term that keeps bodies from merging) so that lineages become trees.
2. Make sensing world-made: a secreted, diffusing signal instead of imposed blurred-field chase/flee.
3. Heritable genes that act on *body-level* traits (speed, size set-point) with the body-scale
   phenotype operator, to get L7 for organized, motile individuals rather than a growth-rate gene.
4. Larger domains (≥256²) for predator-prey: coexistence was a knife edge at 128².

## Showcase movie

`movies/showcase.mp4` (3.8 MB, 301 frames, 192², t = 0…2400, fixed colour scales; frames in
`movies/showcase_sheet.png`). **Predator-prey Flow-Lenia.**
- Two glider species run under the same mass-conserving Flow-Lenia rule (rule C2_r202) in separate channel pairs.
- Cyan prey gliders eat a diffusing food field (magenta) and divide. They leave dark depletion wakes and flee a blurred image of the predators.
- Orange predators are drawn up a blurred image of the prey. They absorb the prey mass they overlap and decay back into food, so the total mass is conserved.
- Prey multiply from two noise patches to a crowd of ~30 by t≈800. The predators then grow and run them down (engulfments are visible as orange rings closing on cyan gliders), and the prey decline.
- Predators nearly die out (minimum matter 11) but persist. The prey recover to a second peak at t≈2200.
- One seed is shown. At 128², coexistence held in 3 of 4 seeds.
