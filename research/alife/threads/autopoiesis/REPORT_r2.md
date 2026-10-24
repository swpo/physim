# Autopoiesis, sprint 2 report

## 1. Headline

**Motility evolves, and the environment decides its direction.** I forked the
chemotaxis-motility thread's toxic-trail metabolism into my swimming phase protocells. The
catalyst carries a heritable phoretic mobility μ, and a neutral tag with the same mutation rate
and size measures drift. With self-made toxic waste, μ rises in all 5 surviving seeds of 6
(μ − tag = +0.08 to +1.33 at t=48k; every one ends at μ ≥ 1.8): a swimmer leaves its waste
behind. Without waste, μ falls to 1.01-1.22 in all 5 seeds whose populations grow large (neutral
tag mean 1.44), because swimmers divide less. A ±10% toxicity jitter showed what sets the direction: at kd=0.018, μ first rose, then
collapsed (1.73 → 0.82) as one population turned dense (9 → 42 cells). Crowding dilutes the
waste, so the direction of selection follows population density (a regime shift between a
sparse motile and a dense sessile state). These are heritable, motile individuals under
selection that a control separates from drift. Three other forks (local trail propulsion, toxicity-driven rescue, chemotactic
predators) failed for informative reasons.

## 2. Claims

| world | claimed | strongest evidence | known weaknesses |
|---|---|---|---|
| `motile_trait_tox` / `motile_trait` | **L7[L3] + L4b**: selection on a heritable motility trait, against a neutral-tag control | `screens/motility_evolution.png`, `runs/mt6_*.log` (6 seeds per environment, 48k). kd=0.02: μ 1.98/1.85/2.08/2.24/1.81 vs tag 1.09/1.43/0.75/0.95/1.73 (seed 3 extinct by t≈4000). kd=0: μ 1.21/1.01/1.01/1.17/1.22 vs tag 1.39/1.47/1.64/1.18/1.52 (43-52 cells). Packs: `packs/motile_trait_tox` (seed 0), `packs/motile_trait` (seed 1) | Small populations under toxin (2-10 cells), so drift is large: the tag moves by up to 0.75 and fell in 4/5 toxic runs (hitchhiking or drift). μ ended above its start in 5/5, the tag in 1/5. The no-toxin seed 0 goes the other way (μ 2.33, population crash to 3 cells). Labkit's tracker breaks for swimmers (hundreds of "nucleations"), so cell counts come from my φ-labelled counts in the logs. Not robust to −10% toxicity (kd=0.018 shifts to the dense sessile regime, `screens/motility_regime_shift.png`); kd=0.022 and dt/2 keep the result. Mutation is a written-in rule. Phoresis uses a per-cell label (nonlocal). |
| (carried over) `phase_kinds`, `phase_trait` | L7[L3] | sprint 1 packs; neutral controls in 3 seeds | as in sprint 1 |

**Movie:** `packs/motile_trait_tox/movie.mp4`: walled swimmers with waste wakes grow, split and
evolve higher mobility.

## 3. Mechanisms learned

1. **Waste toxicity couples metabolism to motility** (forked from chemotaxis-motility
   toxforage). Pure populations at t=8000: kd=0.01 gives 34 sessile cells vs 8 motile;
   kd=0.015-0.02 gives sessile extinction vs 4-8 motile cells; kd=0.03 kills both. Swimming
   rescues sparse populations from their own waste but costs reproduction when the waste is mild.
   The trait experiment converts this into selection.
2. **A phase-field cell needs a rigid-body drive.** Local flows (−χ∇h, or a Gaussian-smoothed
   version) are read by the Allen-Cahn wall as stretching and tear the cell. Keller-Segel bodies
   survive this because their aggregation term holds them together; ours has none. Per-cell
   (labelled) phoresis works.
3. **Crowding dilutes waste, so density decides.** Under a slow toxicity ramp a dense sessile
   population survives kd=0.02, which kills sparse populations. In the evolution runs the same
   effect gives a regime shift: once a population turns dense, motility is selected against
   (kd=0.018, seed 1). Prediction: a larger domain (more room before crowding) should keep the
   motile regime longer.
4. **Predators that eat substrate cannot hunt.** Moving toward prey means entering the prey's
   depletion halo, and predators starve before contact. A faster catalyst also starves its own
   wall (c2 = 0.3 is not viable alone), which bounds every parasite/predator design.

## 4. Negative results

- `phase_trail` (local self-repellent propulsion, fork of kstrail): cells tear (local flow) or
  are poisoned (trail as wall tilt). No motility.
- `motile_kinds`: no evolutionary rescue at constant kd=0.015 (extinction before t=4000). Under
  a ramp, motile and neutral mutants rise equally (3 cells each).
- `hunters` (fork of the pursuit chemotaxis): predators die on approach at every speed cap. Only
  static predators coexist (25 vs 29 cells).

## 5. Next sprint

1. Motility evolution at larger scale (256², more cells) to shrink drift. Started at μ=3 (no
   toxin), populations stay at 2-4 cells and μ does not decline in 48k (3 seeds, `runs/mthi_*`):
   a sparse motile regime where selection is too slow. Test whether it is a true second
   attractor with larger domains and longer runs.
2. Predation that pays: predators that eat links/catalyst on contact (not substrate), so
   approaching prey is not starvation.
3. Local phoresis with an incompressible interior (Darcy flow inside φ) to drop the label.
