# lenia-multichannel: Sprint 2 report

The committee's r1 review arrived mid-sprint (~17:45, sprint start 16:37). I re-planned to its main
experiment for the last ~40 minutes. The work done before the review follows below it.

## 1. Headline

**The committee's L7 test on the food-limited MIRd+ replicator fails: new alleles arise but never
take hold.** Setup: discrete alleles carried by matter (kernel-weighted majority inheritance, never
averaged), whole-cell mutation, nothing planted, S vs N arms, 3 seeds each, 192², t=2000.
- Heredity of the resident allele is near perfect: 2932/2933 divisions breed true, 1 conversion vs
  18 mutations, <0.25% impure cell samples.
- But all 18 allele-1 lineages are lost in both arms, typically within 500-1500 steps (peak share
  0.14/0.18/0.05 under S vs 0.14/0.02/0.02 under N, paired seeds).
- At 10x the mutation rate (30 mutations per run, 1 seed per arm), allele-1 cells divided only 2-3
  times and kept the allele in 1 of 5 divisions. Mean allele-1 share was 0.005 in both arms.
- So minority alleles neither persist nor breed true. The likely causes are population size (5-30
  cells with crashes to 3-7) and swamping of mutant cells by the majority at contacts.

Before the review I had shown purifying selection with a *continuous*, blurred trait (mcg-MIRd:
harmful cells 3/497 vs 48/474 neutral, 6+6 seeds, and a selection|neutral movie). The committee's
discrete-majority design rules out that averaging. Under it, the evidence for heritable kinds at the
cell level is negative.

## 2. Claims

| world | claimed rung | strongest evidence | known weaknesses |
|---|---|---|---|
| `mca-MIRd` (committee design; EFF=0.15 S vs EFF=0 N) | **L7 Contradicted** for this design. Resident heredity Supported (2932/2933 true divisions, 1 conversion vs 18 mutations) | `screens/mca_alleles_S_vs_N.png` (3+3 seeds, 192², 20000 steps): allele-1 share spikes after each mutation and returns to 0 in both arms. Audit data in `screen_data/mca/*.json`. 10x-rate pair: NOTEBOOK A2 | Spec mutation rate gives only 2-4 events per run. True-division counts are dominated by allele-0 parents. The allele-1 division audit (5 events) exists only for the 10x pair. No labkit packs: time ran out |

### Earlier sprint-2 work (before the review): continuous trait, mcg-MIRd

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
- Crowding-dependent maintenance (one seed): the selection run still settles to a steady ~20
  cells; inconclusive (H10).
- Parameter-localized trait (kernel growth centres shifted by g): one run, mean g rose to +0.6 and
  then the population collapsed. Within the neutral range; exploratory (H8).
- Competition at decay 0.04: the neutral baseline goes extinct by step 3300 (3/3), and the
  selection runs freeze into a mixed lattice.
- MU 0.004 is too little variation for a clear purifying signal: 13 of the 14 harmful neutral
  cells came from one seed.

## 5. Next sprint

1. **Find out why minority alleles fail.** Check whether mutant cells are swamped at contacts
   (majority kernel over neighbours' halos) or whether this is plain drift: run larger populations
   (256²), restrict the majority to the cell's own core (A0) mass, and seed one mutant at a fixed
   time across 10+ replicate seeds to measure fixation probability against the drift expectation
   1/N.
2. **Committee secondary items not done this sprint:** whether the cycle is real (256² and dt/2
   using the N series, which are now available in `screen_data/mca`), and r-two56 on
   build-from-food plus decay.
3. If heredity holds in step 1, repeat the S/N test with ≥3 seeds and labkit packs, and add allele
   colours to the sheets.
