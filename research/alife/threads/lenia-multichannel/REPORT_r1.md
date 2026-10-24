# lenia-multichannel: Sprint 1 report

## 1. Headline

**A build-from-food metabolism turns Chan's multi-channel replicators into food-limited
colonies.** In this metabolism, matter can only be built from a regrowing, diffusing food field;
decay dissipates. Structured cells (white core, orange cap, dotted magenta halo) divide
for 4+ generations. As a colony they form an expanding front that eats into fresh food and
leaves a starved interior. Population size and fate follow the food supply: extinction with no
regrowth, boom and bust at low supply, a persistent colony at middle supply, and at high supply a
space-limited "dormant" lattice of cells that stops eating. The same coupling makes a shelled
glider pay for its motion, and it starves when regrowth stops. The rule is unchanged where food
is plentiful, so it adds metabolism to any Lenia world without retuning the creatures.
Separately, about 1 in 200 random 2-channel kernel graphs **spontaneously** makes membrane-bounded
cells from noise. The ablations show the mechanism: the core and the shell depend on each other.

## 2. Claims

Packs are in `packs/<id>/seed{0,1,2}`, all with 3 seeds. "Planted" means Chan's creature was placed
by hand.

| world | claimed rung | strongest evidence | known weaknesses |
|---|---|---|---|
| `mcf-MIRd` (MIRd+ #1130 + food) | **L6[L3?] + L4c + L5** (metabolism-limited replication, competition for food shapes population dynamics) | `packs/mcf-MIRd/seed*/sheet.png`: the colony front and depleted interior from t≈100. timeseries: boom to ~40 cells at t≈200, decline to 11-16 by t=400. Ablation `packs/mcf-MIRd-norefill` (rho=0): boom to ~10 cells, then extinct in 3/3 seeds (seed0 at t≈230) while mean food is still ~0.4. Supply sweep in `screens/mcf-MIRd_rho*.png`. No-food control `packs/mc-MIRd`: 16-17 persistent splits, generation 4, ~40 cells fill the grid by t=200 | Planted creature (Chan's). L3 is weak: cell parts (core/cap/halo) are visible on the sheets, but labkit tracks only the core channel, so rim metrics don't see the halo. Long-term fate at rho=0.01 not settled (rho=0.005 went extinct by step 5000 at 128²). The lineage tracker sees few persistent splits once cells crowd together |
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
- labkit tracking breaks on creatures that shed shell debris or touch through halos (any split
  above 10% overlap ends a track). We worked around it with the `matter` channel choice. This is
  not a labkit bug, so labkit is unchanged.

## 5. Next sprint

1. **Heredity on the replicating, food-limited line:** localize one or two kernel parameters
   per cell (a parameter field carried with matter, in the style of Flow-Lenia), so that daughters
   inherit them with small mutations. Then let food competition select (target L7). The two-species
   ecology is the stepping stone: run proper packs with equal starts, and test competitive
   exclusion against coexistence across supply rates.
2. **Spontaneous replicators:** mutate r-two56 toward fission (core-splitting
   cross-inhibition, two-peaked growth on k0) and screen 2-channel graphs with a replication
   filter. Spontaneous shelled replicators would combine both lines.
3. **Numerics:** dt and R sweeps for mcf-MIRd and mcf-fastcell (mc-MIRd replication already
   survives dt/2), and a less discretization-sensitive variant of r-two56 (larger R, soft clip).
4. Needs: nothing new. A labkit option to keep a track through small debris splits would help
   every Lenia thread.
