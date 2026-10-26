# Does the swim-far minority of the Marangoni rods persist through lineages?

Operator-run analysis (an agent scout, then a red-team critic). Scripts and outputs are in files/.

# Persistence of the swim-3-rod-lengths trait in c34's Marangoni rods: lineage scout

**Bottom line:** the minority does not persist by inheritance. A rod that swims 3 of its own lengths before dividing does not pass that on: across 102 dividing tracks, parent and offspring displacement show no measurable link. The swim-far rods keep reappearing in each run because of how each cycle plays out, and a run only ever sees 1-2 generations, because division almost stops once the population fills up around frame 100. Speed is selected for (faster rods leave more descendants). But faster rods also grow faster and divide sooner, so the distance covered per cycle stays near 1.4 rod lengths.

## Data and definitions
- **Runs:** 7 in total. The existing frames for seeds 51 and 52 and the 1.5x-grid run, plus 4 new unchanged runs on seeds 61-64. The new runs took about 37 minutes, one at a time. Nothing under research/alife or in the git repository was changed, and `git status` is clean.
- **Dividing track:** born by a split and ending in a split into at least 2 daughters that each live 20 or more frames.
- **D:** net displacement over the cycle divided by the track's median 4 sqrt(lambda_max), in rod lengths.
- **Time correction:** every trait is corrected for its run's rise-and-fall over time before comparing relatives. Parent-offspring and sister tests are compared against random unrelated pairs matched in time, and also in time plus place.

**Counts:** 102 dividing tracks. D has median 1.42 (IQR 0.84-1.87). 5 tracks reach 3 or more, on 4 of 7 runs, all of them new seeds: seed 61 #20 at 3.23, seed 62 #30 at 4.67 and #19 at 3.16, seed 63 #11 at 4.18, seed 64 #15 at 4.45. Seeds 51, 52 and the 1.5x run have none.
- Counted the claim's way (nucleation-born dividers included, mean 4 sqrt(lambda_max)), the rate is 5 of 156.
- Seeds 61-64 against the older runs is 5 of 61 versus 0 of 41 (Fisher p 0.08), so the higher rate on the new seeds is not significant.

## (1) Heritability
| Test | n | Result | Against the nulls |
|---|---|---|---|
| D on D, parent and child both dividing | 25 offspring of 21 parents | slope +0.22 [-0.61, +1.44], r +0.16 [-0.30, +0.55] | not above (null +0.08) |
| Speed, both dividing | 25 offspring | slope +0.29 [+0.06, +0.57] | fully explained by timing (time null +0.33, P = 0.70) |
| Speed, all split-born daughters | 357 offspring of 186 parents | slope +0.04 [-0.04, +0.11] | null +0.01 |
| Speed, leading-side daughters only | 173 | slope +0.11 [-0.02, +0.25] | above both nulls, P ≈ 0.01 |
| Speed, trailing-side daughters only | 184 | slope -0.02 | none |

- **Sisters:** speed in the first 15 frames is strongly anti-correlated, ICC -0.38 [-0.48, -0.26] against a null of about 0. The daughter born on the parent's leading side is faster by +0.048 [+0.030, +0.065] (about 0.5 SD), in 115 of 187 pairs (p = 0.002), and keeps the parent's heading (cos +0.32 versus -0.12). Over whole lives, sisters are no more alike than unrelated pairs (D: -0.04; speed: -0.05).
- **Top-quartile parents:** their daughters are no faster than the rest (+0.005 [-0.009, +0.021], SD 0.070). For D, 6 children of 5 top parents sit at +0.52 [-0.25, +1.31], which is not significant.
- **Lineages:**
  - Only 3 grandparent-parent-child chains of dividing tracks exist, all on seed 64 (2.34 → 2.08 → 1.71, 1.69 → 1.61 → 0.29, 1.69 → 1.42 → 0.86).
  - Over 226 broader chains, the grandparent-grandchild speed correlation is +0.07 [-0.05, +0.19].
  - Along leading-daughter lines (54 chains): grandparent-grandchild +0.12 [-0.12, +0.36], parent-child +0.23.
- **The passers' own families:**
  - 3 of 5 had a nucleation-born parent that barely moved (D 0.10-0.52), and 4 of 5 are trailing-side daughters.
  - Of their 10 daughters, 1 divides (D 0.94). 2 swim 3 or more lengths but merge or reach the run's end.

## (2) What predicts a long swim before dividing
- **D breaks down into four parts:** how straight the path is (54% of the variance [38, 72]), path speed (31%), shorter rod length (12%), and cycle length (2% [-15, +17]).
- **Long cycles do not help on average.** Rods with long cycles are slower (rho -0.49) and meander more (rho -0.77), so cycle length and D are unrelated (rho -0.03).
- **The tail does need a long cycle.** All 5 passers are in the longer half of cycles (5 of 51 versus 0 of 51, Fisher p 0.056); 4 of them are in the top 20% of their run. They differ from other long-cycle rods by keeping their path speed (67th-89th percentile) and being born small (13th-36th percentile).
- **Size at birth:** rho -0.39 [-0.56, -0.19]; in a multiple regression, beta -0.57 [-1.02, -0.16].
- **Ring:** measurable only on the frames where the surfactant channel was saved (120 of 201). In 97% of dividing tracks the surfactant sits at the rear. The more rear-loaded it is, the farther the rod goes (rho -0.55 [-0.68, -0.40], beta -0.86). Within a track, rear-loading tracks speed frame by frame (median r -0.43), so cause and effect cannot be separated. Mean ring strength gives rho -0.40, but it is mixed up with size and time.
- **Null predictors:** local crowding (rho -0.08) and position (cy +0.07, cx -0.17, both CIs span 0) predict nothing.
- **Later-born rods swim less far** (rho -0.31).

## (3) Fitness
- **Faster dividing rods divide sooner** (rho -0.58 [-0.70, -0.42]).
- **Swimming feeds growth:** speed against area gain over the same 15 frames gives rho +0.33 [+0.21, +0.44], n=298.
- **Early speed and fate:** among split-born rods whose fate is known, the fastest quarter divides 51% of the time against 25-32% for the slowest two quarters, and merges 27% against 42-57%. This link disappears for rods living 30 or more frames (r -0.06), so it reflects the fast rods' quick division.
- **Descendants:** living descendants after 40 frames rise with early speed (rho +0.26 [+0.16, +0.36]; fastest quarter 1.31 against 0.87-0.98). After 60 frames the effect is +0.15 [+0.04, +0.26].
- **Far swimmers that don't divide:** 31 split-born rods cover 3 or more lengths over their whole life, but only 5 divide. They live long (median 94 frames), grow little (1.59x against 2.34x for dividers) and are born late (frame 77 against 40).

## (4) Persistence over time
**Per-cycle displacement falls as the run goes on** (grouped by the frame of division):

| Divides in frames | n | Median D | Median cycle (frames) | Median net speed |
|---|---|---|---|---|
| 0-59 | 26 | 1.71 | 22 | 0.246 |
| 60-99 | 34 | 1.30 | 34 | — |
| 100-139 | 21 | 1.13 | — | — |
| 140-180 | 14 | 0.76 | 72 | 0.066 |

Between the two halves the median drops 1.63 → 1.01, a difference of -0.62 [-0.84, -0.21] (Mann-Whitney p 0.047).

**The far tail does not shrink:**
- 3 or more lengths: 2 of 60 → 3 of 35 (Fisher p 0.35).
- 2.5 or more: 5% → 11%.

The late passers were born early (frames 32-65) and had long cycles.

**The population stops reproducing:**
- Bodies level off at about 28-33 by frame 100.
- Splits fall from 7-10 to 0-5 per 20 frames.
- Bath surfactant rises about 8-fold and plateaus.
- Daughters' early speed drops from 0.138 to 0.102 (p 0.002).
- Of 145 rods split-born after frame 100, only 4 divide.

## What this means for your two questions
- **How the minority persists:** not through lineages. The trait is re-drawn every cycle from rods born small in the active phase that happen to get a long cycle without slowing down. The only inherited part is a weak motile polarity handed to the leading daughter, and that daughter divides sooner. 4 of the 5 passers are trailing daughters.
- **An environment where it spreads:** three obstacles show up in the data. These are leads, not tested:
  - There is almost no time for selection: reproduction stops at saturation, so each run is about 2 generations. Removing bodies or matter periodically would keep the population in its growth phase.
  - Selection acts on speed, not on D. Speed buys faster growth and an earlier division, so distance per cycle stays capped. The environment would have to reward displacement itself, for example food that a rod only reaches by travelling, or growth that does not depend on how fast it moves into fresh bath.
  - There is no heritable carrier of a swim-far phenotype. The c34 two-kinds world, with its inherited surfactant kinds, is the existing route to one.

## Files
All in /tmp/claude-0/-home-user-physim/a7c2ec48-e3a6-5436-88da-a7523dbbe428/scratchpad/minority/scout/:
- results.txt — the full analysis output
- checks.txt — passer birth sides, the cycle Fisher test, claim-style counts
- timecourse_all.txt
- extract.py, analyze.py, timecourse.py
- tables/*.json
- seed61/ to seed64/ (frames.npz, FACTS.md) and seed61.log to seed64.log
