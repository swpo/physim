# Autopoiesis, sprint 1 report

## 1. Headline

**Phase protocells.** The membrane is an Allen-Cahn domain wall whose inside phase is held up
by links that the cell's own catalyst makes, so the wall is always closed. From smoothed noise,
walled cells self-assemble. They have a catalyst core and a link shell (with wall adsorption,
the links form a material layer at the wall). They repair 35% wounds, divide by central
starvation (up to 6 generations), and fill the domain. The base world behaves the same over 3
seeds, ±10% jitter, dt/2 and 2x resolution. Removing any one link of the loop kills every individual: the
mobility gating, the link→phase tilt, or the phase itself. Four variants extend it:
- **Heredity:** two heritable catalyst kinds with point mutation give a faster mutant lineage
  that sweeps the population (3/3 seeds; a neutral mutant never establishes in 3/3).
- **Parasites:** a link-less selfish mutant is purged below a threshold advantage and drives the
  population extinct above it.
- **Continuous trait:** with a heritable growth-rate trait, lineages started above and below
  evolve toward an intermediate optimum (3+3 seeds), a balance between within-cell and
  between-cell selection.
- **Swimming:** with phoretic drift, a lone cell breaks symmetry into a self-propelled crescent
  swimmer (about 18 body lengths). Near the threshold, swimmers also divide (a swim/divide cycle).

## 2. Claims

| world | claimed | strongest evidence | known weaknesses |
|---|---|---|---|
| `phase_protocell_noise` | **L6[L3]**, L4a, L4c | `packs/phase_protocell_noise/seed{0,1,2}`: noise → 22-24 blobs (t=350) → 11-19 survivors (t=650) → 42-43 cells (t=8000), 28-32 persistent splits, gen 3-4 | Wall channel = 4φ(1-φ), a domain wall rather than a molecule (see phase_membrane). The noise IC has K everywhere. Metabolism ablation via feed only (F ≤ 0.005 → extinction). |
| `phase_protocell` | L6[L3], L4a | `packs/phase_protocell/seed{0,1,2}` (4 planted blobs, no walls planted): 36-43 cells, gen 2-5; S-depleted core, K core, L-rich shell, 2-px wall (`screens/pp6_chan.png`). Damage: `packs/phase_protocell_damage`, `screens/damage_strip.png`: wall arc + 36% of a cell cut at t=1500; both pieces reseal in 100-250 time units and keep dividing | Division is multiple fission of a starving disk (horseshoe → 3-4 pieces), akin to Gray-Scott mitosis inside a wall. |
| `phase_membrane` | **L3** (material membrane), L4a, L6 Weak, L5 Weak | `packs/phase_membrane/seed{0,1,2}`: links adsorb to the wall (drift χ up ∇[4φ(1-φ)]) and form a ring at 3-4x the interior level, zero outside (`screens/pm2_chan.png`). Damage at t=2000 (35%): re-walled with a full link ring by t≈2100 and regrown by t≈2350 (`screens/pm_damage_strip.png`). ±10% jitter of χ, F, θ: 6-28 bounded cells | Fewer persistent splits (gen 2-3). Cells also die and fuse (merges 7-12). χ ≥ 5 → sea or extinction. |
| `phase_swim` | **L4b[L3] Weak** | `packs/phase_swim/seed{0,1,2}`: per-cell phoretic drift μ⟨∇S⟩. A lone round cell is still until t≈1200, then swims as a crescent with a depletion wake at 0.10-0.11 px per time unit, 17.7-18.5 body lengths. μ=1 still, μ ≥ 2 swims (a threshold); μ=0 is the static parent; jitter of μ and F keeps swimming | Heading is locked to lattice directions (upwind anisotropy). The swimmer grows into an arc: shape is not preserved and it does not divide. The operator uses a per-cell label (nonlocal). |
| `phase_swimdiv` | **L4b + L6 [L3] Weak** (swim/divide cycle) | `packs/phase_swimdiv/seed{0,1,2}` (μ=1.5, near threshold): 1 cell → 4 (t≈2400). The daughters swim apart as crescents with wakes, grow and divide again, giving 6-12 motile cells at t=8000; 17-24 tracks moved ≥ 1 body length, up to 5-8 body lengths (sheet t=2400-8000) | Labkit tracks break for moving cells, so persistent splits read only 1-4 (gen 1-3). Judge reproduction from the sheet. The first division is 4-fold symmetric from a round ancestor. Same lattice-heading caveat as phase_swim. |
| `phase_kinds` | **L7[L3] Weak** | `packs/phase_kinds/seed{0,1,2}/kinds.png`: K2 (c2 = 0.3 vs 0.2, same link output) arises by ~10 point mutations, breeds true and replaces K1 (49 → 0 K1 cells, 28-33 K2 cells) in 3/3 seeds; gen 5-6. Controls: neutral mutant (c2 = c1) never forms a cell, 51-52 K1 cells at t=32k in 3/3 seeds. No mutation: 52 cells, stable | Two kinds only; one-way mutation written in as a rule. |
| `phase_kinds_parasite` | L7 (cell-level selection), Weak | `packs/phase_kinds_parasite/seed{0,1,2}`: link-less K2 (c2 = 0.3) → infected cells die, population extinct by t≈25k in 3/3 seeds. Screens: c2 = 0.24 purged (3/3 seeds, 38-51 cells at t=32k); c2 = 0.27 collapses | Why uninfected cells also die is a hypothesis (infected cells hog substrate). |
| `phase_trait` + `phase_trait_c20` | L7[L3] Weak (continuous trait, stabilizing selection) | `screens/trait_convergence.png`, `packs/phase_trait*/seed{0,1,2}`: catalyst carries a heritable growth rate c (faster c → fewer links); ±0.1 point mutations. Over 48k time units, 3/3 lineages started at c=0.20 fall to 0.179-0.182 and 3/3 started at c=0.15 rise to 0.155-0.165: selection toward an intermediate c from both sides. Cells with high c lose their walls and die | Not yet converged. Mutation is a written-in rule. Trait variance inside a cell blends away, so the effective unit of selection is the cell. Trait is not visible in sheet.png (see the plot). |
| `scl_lattice` | L3 Weak (planted); L4a **Contradicted** for 30% wounds | `packs/scl_lattice/seed{0,1,2}`: planted link ring maintained 3000 sweeps by decay + splice; `screens/scl_damage_strip.png`: the wound never closes | Closure only 67-76% of the time; the catalyst sometimes escapes. |

## 3. Mechanisms learned (with ablations)

1. **Topological closure.** Lattice and polymer-field membranes failed by opening. A boundary
   that is the level set of an order parameter cannot have a hole, and repair is automatic.
   Transplant recipe for any RD or Lenia chemistry: add φ, gate the mobilities by φ², and tilt
   φ's double well by an internal product.
2. **Autopoietic tilt.** `dφ = Dp∇²φ + rφ(1-φ)(φ - ½ + a(L - θ))`. Only links *at the wall*
   matter, since φ=1 is a fixed point. Ablation a=0: domains shrink and all die by t≈350
   (`packs/phase_protocell_notilt`). Adsorbing links to the wall (χ) makes that dependence
   explicit: a membrane made of the cell's product.
3. **Gated mobility.** gate=0 → all dead by t≈350 (`packs/phase_protocell_nogate`); K ungated →
   dead; φ ≡ 1 → a uniform sea.
4. **Division by central starvation.** S dips at the centre, so L < θ there and the wall pinches
   through. Prediction: bigger cells at higher feed. Area per cell was 71/66/88/405 px at
   F = 0.0054/0.006/0.0066/0.008, which roughly holds. Window: F < 0.005 → extinction,
   F ≥ 0.01 → sea.
5. **Two levels of selection.** Within a cell, the faster catalyst wins. Between cells, a cell
   whose catalyst makes no links loses its wall. A parasite-advantage threshold separates purging
   (0.24) from collapse (≥ 0.27). With a continuous trait the balance sets an optimum c*, and
   the prediction "steeper trade-off → lower c*" holds. End means at t=32k from starts 0.15 / 0.20
   (1 seed each): β=1.5 → 0.182 / 0.202; β=3 → 0.165 / 0.188; β=6 → 0.150 / 0.166.
6. **Autophoretic swimming.** Above a mobility threshold, a cell's symmetric depletion halo is
   unstable and the cell runs away into a crescent swimmer. Moving keeps it fed: at μ=3 it never
   divides, while at μ=1.5 (slower) it still starves centrally, so swimming and division
   alternate. Rigid-body phoresis must label only cell bodies (φ > ½) grown into their own halo.
   Labelling the φ > 0.05 halo merged touching cells into one rigid body and smeared dying cells
   (an artifact, fixed).
7. **Numerics.** Substrate consumption capped at 0.5 S per step. dt/2 matches cell counts to
   3 digits (10/24/36/47). 2x resolution gives 8/10/22/35/49 against 8/10/24/36/47.

## 4. Negative results

- Lattice SCL (numba, McMullin rules + splice): closure 0.2-0.8 over 24 settings x 2 seeds.
  Single-end extension grows inward spurs.
- scl_divide (bond-fluctuation moves, insertion, reconnection fission): the membrane drifts
  inward (production makes holes inside), gap ends separate, and reconnection shatters cells into
  vesicles. Nothing robust in 16 configurations.
- Polymer-field protocell (M forms where |∇L| is large) and Gray-Scott kinetics inside any
  barrier: freeze or die (14 configurations).
- Dense-noise IC: one sea, then synchronous starvation crash (6 configurations).
- Swim + divide: lower feed gives domain-wrapping bands. Swimming plus adsorption gives
  grid-aligned squares that collapse.
- labkit `--damage` puts its disk at the centroid, so it misses the wall of walled cells and is
  misplaced for cells that wrap over the periodic edge. My hooks re-find the cell and cut its
  wall. A rim-centred option in labkit would help.

## 5. Next sprint

1. Pearling or budding division through a wall-tension term that depends on adsorbed links
   (phase_membrane), instead of starvation fission.
2. Continuous trait (`phase_trait`): run to convergence with 3 seeds per β to pin c*(β), then
   add a second trait axis to look for diversification → L7 Supported, a first L8 probe.
3. Local phoresis (wall slip plus a Darcy flow) to remove the per-cell label and the
   lattice-locked heading. Track swimmers' lineages with a labkit-independent tracker.
4. Lattice SCL with chain-based bond inhibition (LITERATURE §2.7.1): a cheap check of whether the
   classic model reaches L4a.
