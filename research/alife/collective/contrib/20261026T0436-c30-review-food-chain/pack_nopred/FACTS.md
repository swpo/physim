# Evidence pack: condensate-food-chain (seed 4)

- world: `../../20261026T0413-c36-food-chain-predation-claim/world.py`, family `active-emulsion`
- parent: threads/active-droplets/worlds/ad1-fuel; mutation: two immiscible autocatalytic condensates in a closed chain: prey made from fuel, predator made from prey material; decay -> waste -> fuel
- run: 101 frames x 200 steps x dt 0.5 = time 10000; grid [256, 256]; wall 566s; status ok
- command: `python -m labkit.run collective/contrib/20261026T0413-c36-food-chain-predation-claim/world.py --out collective/contrib/20261026T0436-c30-review-food-chain/pack_nopred --seeds 4 --frames 100 --no-movie`
- segmentation: matter > 0.35 of robust range [0.0092, 1.2168], min area 6 px

## Measurements
- components: final 222, mean 222.0, max 229; occupancy final 0.32
- tracks: 524; persistent (alive >= 50% of run): 223; longest 101 frames; alive start-to-end: 18
- size of persistent tracks: max/min area ratio 21.70 (1 = constant size)
- enclosures: components with a hole mean 0.05, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [222, 222, 222], H1 [0, 0, 0]
- motion: 0 long-lived tracks moved >= 1 body length; max speed 0/time; max body lengths 0.9
- replication (lineage window K = 20 frames = time 2000, default): splits 79, persistent splits 7 (0 more failed only because the siblings re-merged within K), max generation 1, merges 37, merge/split ratio 0.468, nucleations 42
- channel total drift (end/start - 1): [0.2798, None, -0.7379, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 7 at frame 50: holes 0, rim-vs-core 0.43, rim-vs-outside 0.30, heterogeneity 0.08; core [0.887, 0.0, 0.036, 0.897] rim [0.477, 0.0, 0.079, 0.768]
  - track 40 at frame 50: holes 0, rim-vs-core 0.34, rim-vs-outside 0.54, heterogeneity 0.08; core [0.948, 0.0, 0.018, 0.955] rim [0.652, 0.0, 0.067, 0.805]
  - track 43 at frame 50: holes 0, rim-vs-core 0.41, rim-vs-outside 0.31, heterogeneity 0.08; core [0.895, 0.0, 0.034, 0.902] rim [0.505, 0.0, 0.077, 0.773]
  - track 510 at frame 54: holes 0, rim-vs-core 0.40, rim-vs-outside 0.31, heterogeneity 0.07; core [0.901, 0.0, 0.032, 0.909] rim [0.528, 0.0, 0.076, 0.775]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 1338 components >= 12 px at frames [17, 33, 50, 67, 83, 100]):
  - radial prey a: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.888, rim/outside 18.8 (aggregate of 1338 individuals; 0/1338 membrane-like individually; rim level 0.88)
  - radial predator b: peak at rho=1.75 (OUTSIDE the peak band 0.5-1.5), rim/core 1.07, rim/outside 0.225 (aggregate of 1338 individuals; 0/1338 membrane-like individually; rim level 0.0007)
  - radial fuel u: peak at rho=1.75 (OUTSIDE the peak band 0.5-1.5), rim/core 5.97, rim/outside 0.888 (aggregate of 1338 individuals; 0/1338 membrane-like individually; rim level 0.112)
  - radial waste w: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.899, rim/outside 1.44 (aggregate of 1338 individuals; 0/1338 membrane-like individually; rim level 0.869)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #7 (t=5000, R_eq 5.59): none; #40 (t=5000, R_eq 6.1): none; #43 (t=5000, R_eq 5.59): none; #510 (t=5400, R_eq 5.67): none
- species `prey` (channels ['prey a'], own threshold): components final 222, mean 222.0, max 229; tracks 524, persistent 223; splits 80, persistent splits 7 (K=20), max generation 1, merges 38, merge/split 0.475; moving tracks 0
- species `predator` (channels ['predator b'], own threshold): components final 0, mean 4.4, max 138; tracks 306, persistent 0; splits 75, persistent splits 0 (K=20), max generation 0, merges 4, merge/split 0.053; moving tracks 0

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
