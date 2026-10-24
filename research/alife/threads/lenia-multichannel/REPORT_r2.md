# lenia-multichannel: Sprint 2 report

## 1. Headline

**The cycling, food-limited Lenia replicators now carry a heritable trait, and selection against
neutral control is visible at the cell level.** The mechanism is forked from active-droplets'
body-confined alleles. Matter built inside a cell copies the trait of the cell it grows from, and
rare cell-scale replication errors change it.
- When harmful mutations cost food yield, harmful lineages are purged: 3/497 harmful cells
  vs 48/474 in the neutral control, 6+6 seeds.
- In the neutral twin (same seed, same mutation sequence) a harmful lineage can take over the whole
  population by drift.
- A planted two-kind competition breeds true and is decided by yield only when yield matters.
- An ecological finding: *beneficial* mutations tip the population out of its turnover cycle into
  a fed, static lattice, which stops selection. Evolving efficiency switches the ecology off.

The striking movie for this thread is `movies/mcg_selection_vs_neutral_seed0.mp4`: selection (left)
vs neutral (right), same seed and same mutations. The left colony reddens as harmful variants are
purged; the right one is taken over by a blue harmful lineage.

## 2. Claims

| world | claimed rung | strongest evidence | known weaknesses |
|---|---|---|---|
| `mcg-MIRd` (+ `mcg-MIRd-neutral`) | **L7[L3?]** (variation arising, breeds true, purifying selection vs a neutral control) | `screens/mcg_purifying_mu012.png`: 3 selection vs 3 neutral seeds, 160², 10000 steps. Harmful cells (g<-0.2) in the second half: 0/86, 1/73, 0/97 vs 29/56, 0/86, 5/95. The same design at MU 0.004 gave 1/75, 1/74, 0/92 vs 0/56, 1/86, 13/95 (NOTEBOOK H5). Mean g ratchets up under selection (+0.40 to +0.51) but not in neutral (-0.33 to +0.38). `screens/mcg_purifying_neutral_seed0.png` and the movie: a blue low-g lineage fixes by drift in neutral seed 0. The ecology keeps cycling in all runs. Packs: `packs/mcg-MIRd`, `packs/mcg-MIRd-neutral` | The trait is continuous and its fitness effect is designed (yield = Y·e^{min(g,0)}). Selection is purifying, not adaptive. With ~10-20 cells, drift is strong: 1 of 3 neutral seeds at each rate shows few harmful cells. The trait blurs at cell contacts. Planted Chan creature |
| `mcg-MIRd`, competition assay | **L7 support** (two kinds breed true; differential persistence only under selection) | `screens/mcg_competition_cycling.png`, 3+3 seeds, 128², 12000 steps. The kind with 26% lower yield falls 0.50→0.07 by step 2000 and to 0.01-0.05 after (3/3). Neutral frequencies drift to 0.04, ~0.2 and 0.92 | The kinds were planted. 2 of 3 neutral populations went extinct near step 12000 (128² fragility) |
| `mcg-MIRd` with beneficial mutations | ecological result, not a rung | `screens/mcg_yield_selection_vs_neutral.png` (3+3): every selection run ends as a fed static lattice (30-35 cells, food ~0.6), and every neutral run keeps cycling (5-22 cells) | Mean g barely differs: the base point sits at the cycle/lattice boundary |

## 3. Mechanisms learned

- **Heredity by growth.** In Chan's Lenia matter never moves, it is built and destroyed. Daughters
  inherit if built matter copies the mass-weighted, locally blurred trait of existing matter. One
  Gaussian blur of g·M per step is enough: kinds stay pure through divisions (H3: traits remain
  exactly 0 and 0.5).
- **Selection needs turnover, and Lenia shuts turnover off.** A confluent Lenia tissue is a fixed
  point with no matter turnover. Once cells reach it they stop eating, dying and dividing, and kind
  frequencies freeze at their colonization values (H3). Selection works only in the
  consumer-resource cycle (decay 0.03), where crashes keep killing cells and survivors recolonize.
- **Evolution can switch off its own ecology.** Higher yield acts like a lower maintenance cost,
  and the base point is close to the cycle/lattice boundary (decay 0.025 gives a lattice). So
  beneficial mutants push the population into the static lattice, and evolution stops. Purifying
  selection keeps the cycle. Prediction: adaptive evolution needs a trait whose benefit does not
  lower the effective maintenance cost, for example a trade-off, or a larger grid where local
  cycles are out of phase.
- **Mutation must act at the scale of a cell**, as active-droplets found. Small disks (r=5,
  DELTA 0.3) moved cell means by only ~0.04. Disks covering a core (r=8, DELTA 0.5) give
  distinguishable kinds.

## 4. Negative results

- The two-sided yield gene gives no measurable trait difference between selection and neutral:
  the ecology freezes before selection acts.
- A trade-off trait (yield and decay both scaled by e^g) also tips 3/3 selection runs into the
  lattice, with no trait difference from neutral (H9).
- Parameter-localized trait (kernel growth centres shifted by g): one run, mean g rose to +0.6 and
  then the population collapsed. Within the neutral range; exploratory (H8).
- Competition at decay 0.04: the neutral baseline goes extinct by step 3300 (3/3), and the
  selection runs freeze into a mixed lattice.
- MU 0.004 is too little variation for a clear purifying signal: 13 of the 14 harmful neutral
  cells came from one seed.

## 5. Next sprint

1. **Adaptive (not only purifying) selection while keeping turnover.** Give the trait a trade-off,
   that cannot reach confluence. Yield against maintenance cost failed (H9). Two options: penalise
   jamming directly, for example decay that rises with local crowding, or use 192²+ grids, where
   the cycle damps into a noisy steady state with continual turnover. GENE_MODE "m" (localized
   kernel parameters) is implemented and needs 3+3 seeds.
2. **Heritable morphology.** Localize a kernel parameter so that kinds differ in shape or division
   mode (dynamic phenotype, endogenous fitness): a step toward L8.
3. **Spontaneous replicators** remain open (0/150 in sprint 1).
