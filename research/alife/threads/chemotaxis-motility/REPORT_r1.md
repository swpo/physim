# REPORT r1: chemotaxis-motility

## Headline
**A slow, self-secreted repellent turns Keller-Segel aggregates into self-propelled crescent swimmers that form
from noise.** I built three worlds on this one operator. In the first, two species pursue each other and lock
into chaser-and-fleer pairs. In the second, the repellent is toxic waste and the swimmers live on a regrowing
nutrient, so a population with turnover persists only while the food regrows. The third combines both into a
predator-prey ecology that coexists stably for t = 2000. Removing the trail kills motility in every world.

## Claims
| world | claimed rung | strongest evidence | known weaknesses |
|---|---|---|---|
| `kstrail` | **L4b[L2]**; L3 Weak | `packs/kstrail/seed1` tracks.png #15: one polar crescent from t=132 to 600. All 3 seeds have 22-25 tracks moving ≥ 1 body length (max 23 body lengths). Formation route spot → expanding ring → rupture → crescent (seed0 #0, `kstrail_dthalf`). Spontaneous from noise. | Collisions merge swimmers. **Swimmers are transient**: `packs/kstrail_long` (t=1800) coarsens 14 → 2 bodies, ending as 2 immotile saturated aggregates. L3 "front/back differentiation" is only rho-crescent ahead + h cloud behind, a soft field. Not a membrane. |
| `pursuit` | **L5[L2]** (pursuit → bound composites) | `packs/pursuit/seed0` sheet t ≥ 300: predators (orange) sit in the concave rear of prey crescents (cyan) and the pair travels together. `pairing.py`: predator bodies touching prey 0.86/0.91/0.76 (null 0.27-0.31). | No population dynamics (no kinetics). The labkit tracker merges the pair into one component, so track and lineage numbers do not see the two species. |
| `toxforage` | **L4c[L2]** + L4b; L4a Weak | `packs/toxforage` (3 seeds, t=1200): 9-14 swimmers, mass stationary at 1.0-1.9x initial. Ablation r=0 (`toxforage_abl_r0`): mass → 0.14 and bodies 11 → 4, still falling. Single-swimmer damage (40-47% erased, `screens/damage1_toxforage*.png`): it re-forms a polar crescent within ~15 t and is back to control size by ~50 t (seeds 0 and 2). | Individuals live ~300-500 t inside constant turnover (no track spans the run). Growth/death is balanced at the population level, and a "metabolism" of single bodies is not separated from merge/split exchange. Repair tested only on 3 bodies, with no labkit-native pack. |
| `ecology` | **L5[L2]** (predation changes populations) | `packs/ecology` (3 seeds, t=1000): ~22 prey and ~19 predator bodies coexist; 93-96% of predators are on a prey. Ablation k=0: predators -95% and prey +1%, against prey -24% with predation. `ecology_long_160` (t=2000): stable coexistence. | **No sustained predator-prey cycles**, only one damped overshoot. Pairs dominate, so "populations" of the two species co-move. Body counts come from `species.py`, not labkit lineage. |

## Mechanisms learned (with ablations)
1. **Propulsion = self-repulsion from a slower field.** a (fast, short) holds the body together, while h (slow decay, small diffusion)
   accumulates where the body has been. A stationary body sits on a symmetric h hill, which is unstable, and after
   displacement the hill is behind it. Ablation chi_h=0 (`kstrail_abl_noh`): 30-60 static round spots, ≤ 2.5 body lengths,
   0 splits. Window: chi_h ≈ 4-6.5 at chi_a 24. Above it the system is a turbulent sea; below it, static spots.
2. **Only unsaturated bodies swim.** With volume filling, large bodies form rho=1 plateaus, the gradient of h across them
   vanishes, and they stop. Low total mass (rho0 0.05) keeps bodies small, which is why swimmers coexist with occasional
   immotile clumps. *Prediction for other threads:* any self-propulsion that relies on a gradient across the body fails
   at saturation, so size control is a precondition for motility.
3. **Pursuit binds; evasion shapes the bond.** Pursuit-only (chi_x=0): predators are carried inside prey (contact 0.99).
   Evasion-only (chi_y=0): contact at chance (0.58 vs null 0.58). Both: predators lock into the crescent's concave rear (0.86).
4. **Toxic trail couples metabolism to motility.** With waste toxicity kd·h·rho, a stationary body poisons itself. toxtrail
   chi_h=0 ablation: static spots shrink and half vanish (43 → 20 bodies), then stabilise at a small size, so the
   prediction "static dies" holds only partly. With nutrient-limited growth (toxforage), clumps formed in
   collisions are poisoned and re-shed swimmers, which is the source of turnover. **Toxicity is the size control that keeps the
   swimmer phase alive**: mass-conserving kstrail coarsens to 2 immotile blobs by t=1800 (`kstrail_long`), while toxforage keeps 6-7
   swimmers to t=1500 (`toxforage_long_128`).
5. **Numerics matter for direction.** At body radius ~3 px, first-order (and even MUSCL) upwinding pulled headings to the grid
   diagonals: a single swimmer seeded at 20° turned to 45°, and one at 0° died (`dirtest`). After doubling all lengths (body radius ~6 px) plus
   a van Leer MUSCL volume-filling flux, headings stay at 0° and wander without snapping. dt halving (`kstrail_dthalf`) gives the same
   picture. ±10% jitter of chi_a, chi_h and rho0 keeps swimmers in all 6 variants.

## Negative results
- Cell-centred volume-filling factor + clipping lost 80% of the conserved mass. Use face fluxes v·rho_up·(1−rho_down).
- Chemotaxis up a consumed nutrient (`forager`, scale 1): a static lattice when the nutrient diffuses fast, extinction when it is slow. The (1−rho) growth factor
  starves dense bodies. Cubic pressure instead of volume filling gives round bodies but goes unstable (NaN) explicitly.
- Kinetics active from t=0 (Allee growth) kill everything before swimmers condense. Fix: switch kinetics on at t_on=150.
- Nutrient-limited swimmers with r=0.01 decline slowly in all seeds. r ≥ 0.06 is needed for a stationary population.
- Prey growth without toxicity leads to swimmers growing into large immotile amoeboid blobs (no fission).
- Mass-conserving trail swimmers (kstrail) do not last: they coarsen into immotile aggregates by t~1800.
- Predator-prey kinetics give stable coexistence, not oscillations, in every run so far.
- Novelty caveat: self-propulsion by self-generated chemorepellent trails is known for single particles (e.g. "autochemotactic"
  walkers and active droplets). What I have not seen in our LITERATURE.md is the field version with formation from noise, pursuit pairs and
  toxic-trail metabolism.

## Next sprint plan
1. **Reproduction (L6)**: make growth-driven fission reliable. Idea: size-dependent rupture via the ring instability (static bodies already
   hollow into rings that break into crescents). Add an Aranson-style nonlocal area constraint or an AMB+-like size selection so a
   grown body splits into two same-size swimmers, then check lineage over ≥ 2 generations.
2. **Cycles (L5 → richer ecology)**: break the 1:1 pair lock (predator handling time or satiation, prey escape bursts, larger domain 256²)
   to get sustained oscillations carried by individuals. Add per-species tracking (a `matter` hook per species, or my own tracker).
3. **Heredity seed**: give each swimmer a heritable parameter (e.g. a chi_h tag carried as a passive concentration field) and see
   whether fast or slow swimmers win under predation.
4. Needs: a labkit option to track one channel (species) at a time, and to damage a median body instead of the largest.
