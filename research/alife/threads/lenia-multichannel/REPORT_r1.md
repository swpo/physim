# lenia-multichannel: Sprint 1 report

## 1. Headline

**Chan's multi-channel replicators get a metabolism, and the result is a consumer-resource
cycle.** The mutation is that matter can only be built from a regrowing, diffusing food field.
- Structured cells (white core, orange cap, dotted magenta halo) still divide for 4+
  generations, but now as a colony front that eats into fresh food and leaves a starved interior.
- Without regrowth they go extinct.
- With regrowth they either crash, or fill the space and turn into a "dormant" lattice that stops
  eating. Jammed cells have no matter turnover, so they cost nothing.
- **Adding a maintenance cost (all matter decays and must be rebuilt from food) removes the free
  dormancy and gives sustained population-food oscillations.** Over 14000 steps the cell count
  cycles 19→7→15→7→18→2→12 with food in antiphase, and cells keep dividing and dying.
- The same metabolism makes a shelled glider pay for its motion: it starves when regrowth stops.
- Starving cells switch phenotype: a cyan core inside an orange ring.

Separately, 2 of 420 random kernel graphs (both 2-channel) **spontaneously** make membrane-bounded
cells from noise. The ablations show why: the shell sits at a set distance from the core, and the
core and shell depend on each other.

## 2. Claims

Packs are in `packs/<id>/seed{0,1,2}`, all with 3 seeds. "Planted" means Chan's creature was placed
by hand.

| world | claimed rung | strongest evidence | known weaknesses |
|---|---|---|---|
| `mcfd-MIRd` (MIRd+ #1130 + food + maintenance decay 0.03) | **L6[L3?] + L4c + L5** (sustained consumer-resource cycle with ongoing division and death) | `screens/mcfd-MIRd_decay0.03_14000steps.png` (128², seed 1): 3+ population cycles over 14000 steps. `packs/mcfd-MIRd/seed*/timeseries.png` (3 seeds, 14000 steps = t 1400): all 3 seeds persist (3-10 cells at the end, 25-28 at peaks). Matter and food oscillate in antiphase; seed2 shows 4 cycles with period ≈380 time units. The sheets show division, starving phenotypes and food wells. Comparison: decay 0.01 gives a static fed lattice (`screens/mcfd-MIRd_decay0.01_128.png`); decay 0 gives dormancy or extinction (rows below) | Planted Chan creature. One grid size (128²). Cycle period and amplitude not yet measured across seeds or parameters. Tracking sees divisions only as long as cells stay apart |
| `mcf-MIRd` (MIRd+ #1130 + food) | **L6[L3?] + L4c + L5** (metabolism-limited replication, competition for food shapes population dynamics) | `packs/mcf-MIRd/seed*/sheet.png`: the colony front and depleted interior from t≈100. timeseries: boom to ~40 cells at t≈200, decline to 11-16 by t=400. Ablation `packs/mcf-MIRd-norefill` (rho=0): boom to ~10 cells, then extinct in 3/3 seeds (seed0 at t≈230) while mean food is still ~0.4. Supply sweep in `screens/mcf-MIRd_rho*.png`. No-food control `packs/mc-MIRd`: 16-17 persistent splits, generation 4, ~40 cells fill the grid by t=200 | Planted creature (Chan's). Without decay there is no dynamic steady state: at rho=0.01 it is extinct by step ~4500 at 128², and at 192² extinct after two growing boom-bust cycles (step ~11300; `screens/mcf-MIRd_192_20000steps_cycles.png`). At rho ≥ 0.0125 or D=8 the cells form a dormant lattice. L3 is weak: cell parts (core/cap/halo) are visible on the sheets, but labkit tracks only the core channel, so rim metrics don't see the halo. The lineage tracker sees few persistent splits once cells crowd together |
| `mcf-fastcell` (*fast cell* + food, Y=5) | **L4b[L3] + L4c** | `packs/mcf-fastcell/seed0/sheet.png`: 4 cyan-shelled gliders with orange/magenta cores forage for t=300 and leave dark food trails. Ablation `packs/mcf-fastcell-norefill`: gliders die one by one, 0-1 left by t=255-300 (seed0 timeseries). Starvation threshold: mean food ~0.3-0.35 (NOTEBOOK M4) | Planted known creature. L3 is from Chan's division of labour. Shell-only debris makes tracking fragile (we track the core channels) |
| `r-two56` (random 2-channel rule) | **L3, spontaneous** | `packs/r-two56/seed*/sheet.png`: in all 3 seeds the noise forms a tissue with a two-layer rim, and 4-8 cells pinch off: white centre, cyan core, orange spiky shell. tracks.png: cells are stable t=20-100. FACTS: rim-vs-core 0.5-0.75, rim-vs-outside 0.46-0.53 | **Numerics weak**: cells die off slowly at dt/2, and R=15 kills them. ±10% jitter of all 18 parameters keeps the behaviour in only 1 of 5 draws. **L4a fails**: shell-side cuts up to 20% regrow, 30% kills, any core damage kills (`screens/r-two56_damage_side_vs_core.png`). Stationary, no division |
| `r-two-s1-85` (random) | L3 spontaneous (tissue) | `packs/r-two-s1-85/seed1/sheet.png`: about 30 shelled cells packed into a frozen tissue | Static. Lineage "splits" are flickering bridges, not division |
| `r-two-s1-60` (random) | L4b[L2] spontaneous + L5 (weak: crowding arrest) | `packs/r-two-s1-60/seed0/sheet.png`: about 45 individuals. Static "bricks" inside the crowd, C-shaped gliders leave from its edge (15-26 moving tracks). A brick planted alone becomes a glider | The second channel is dispensable: replacing the orange→cyan kernel by a constant keeps the gliders. The glider is effectively single-channel Lenia |
| `eco-MIRd-Rplus` (two species, shared food) | L5 preliminary (coexistence under competition) | `screens/eco-MIRd-Rplus_*.png`: an MIRd+ enclave (3-6 cells) persists inside an R+ population (~35-50 cells) for 4000 steps. Monocultures for comparison. Pack `packs/eco-MIRd-Rplus` | One quick seed at 128². R+ is planted as a cluster, so the start is unequal. No variation, so this is not L7 |

**Fraction of random graphs giving individuals** (S1+S3, 420 rules, R=10, 96², from noise):
discrete individuals in ~10/420 (2.4%). Shelled core+shell cells in 2/420, both from the
2-channel family. By family: the full 15-kernel Chan template gives 3/60 classifier hits and is
72% dead. Sparser graphs (two-channel, star, cycle) are viable far more often. Most classifier
"individuals" are frozen dot lattices that fill the seeded square.

## 3. Mechanisms learned

- **The membrane is a distance set point, and the cell is a mutual dependence (r-two56,
  `screens/r-two56_ablations.png`).** Kernel k4 (core→shell) lets the shell grow only where the
  ring-sensed core density is about 0.23, which is a band at a fixed distance from the core.
  Removing k4 gives an orange sea. k5 (shell→core) feeds the core: removing it, or replacing it
  by a constant, kills the core. k0 (narrow core self-kernel) limits size: without it the cells
  grow into endless bilayer worms, and with a weakened k0 (h0 ≤ 0.33) they become expanding hollow
  vesicles that shed cells. **Prediction checked:** the same constant-k5 test on r-two-s1-60
  leaves its gliders intact, so its second channel does no structural work.
- **Build-from-food metabolism (M2-M5, R3).** It charges only matter *turnover*: positive growth is
  capped by local food, and decay dissipates. Three consequences:
  1. Static cells never eat: food returns to 1.0 around r-two56 cells.
  2. Moving or dividing creatures pay in proportion to their turnover, so the glider needs Y≥5
     and dies when mean food falls below ~0.3.
  3. Jammed cells (confluent MIRd+ at rho=0.02, the crowd bricks in r-two-s1-60) become inert.
  4. So whether a population cycles depends on whether dormancy is free. A maintenance decay
     μ·A that must be rebuilt from food turns dormancy (μ=0) into a fed static lattice (μ=0.01)
     and then into sustained oscillations (μ=0.03). Without μ, a larger grid allows one recovery
     cycle before extinction (192²), while 128² dies at the first crash.

  A gated metabolism (growth × F) destroys Chan creatures even at F≈0.93 (negative result).
- **Replication seen in labkit needs care.** A single planted creature on a torus gives identical
  seeds, because 90° rotations are exact symmetries; we add 5% multiplicative jitter. Dotted
  halos fuse neighbouring cells, so we track the core channel only.

## 4. Negative results

- Gated food (positive growth × F^1, eating, starvation) kills *mIRde* for every setting tried.
- Food on *mIRde* (a slow replicator that tends to re-merge): marginal. Extinct in 2/3 seeds
  at 192².
- No binary fission of r-two56 cells under the k0 weight or set-point mutations: a single planted
  cell is unchanged for h0 ∈ [0.1, 0.41] and m0 ∈ [0.13, 0.19].
- The full random 15-kernel graph is mostly dead (43/60). The designed "shell" family (outer-ring
  feed + shell inhibits core) produced rings, hollow loops and lattices, but no persistent
  shelled cells.
- Some random rules make individuals from one noise seed and a sea from another (two-s1#66).
- Spontaneous replication screen (150 2-channel rules, small seed patch): 0 cell replicators. 6
  are expanding dot lattices that tile space from a front, and 1 makes C-shaped gliders. The
  C-glider is a recurring attractor of 2-channel rules.
- labkit tracking breaks on creatures that shed shell debris or touch through halos (any split
  above 10% overlap ends a track). We worked around it with the `matter` channel choice. This is
  not a labkit bug, so labkit is unchanged.

## 5. Next sprint

1. **Characterise the cycle** (period and amplitude against rho, μ, D and grid size, with 3 seeds),
   and check the reported dt/2 and R robustness on mcfd-MIRd.
2. **Heredity on the cycling line:** localize one or two kernel parameters
   per cell (a parameter field carried with matter, in the style of Flow-Lenia), so that daughters
   inherit them with small mutations. Then let food competition select (target L7). The two-species
   ecology is the stepping stone: run proper packs with equal starts, and test competitive
   exclusion against coexistence across supply rates.
3. **Spontaneous replicators:** mutate r-two56 toward fission (core-splitting
   cross-inhibition, two-peaked growth on k0). The first replication screen (150 rules) found only
   expanding dot lattices. Spontaneous shelled replicators would combine both lines.
4. **Numerics:** dt and R sweeps for mcf-MIRd and mcf-fastcell (mc-MIRd replication already
   survives dt/2), and a less discretization-sensitive variant of r-two56 (larger R, soft clip).
5. Needs: nothing new. A labkit option to keep a track through small debris splits would help
   every Lenia thread.
