# Evidence pack: condensate-food-chain (seed 0)

- world: `../../../../../../../../home/user/physim/research/alife/collective/contrib/20261026T0413-c36-food-chain-predation-claim/world.py`, family `active-emulsion`
- parent: threads/active-droplets/worlds/ad1-fuel; mutation: two immiscible autocatalytic condensates in a closed chain: prey made from fuel, predator made from prey material; decay -> waste -> fuel
- run: 101 frames x 200 steps x dt 0.5 = time 10000; grid [384, 384]; wall 1560s; status ok
- command: `python -m labkit.run collective/contrib/20261026T0413-c36-food-chain-predation-claim/world.py --out /tmp/claude-0/-home-user-physim/60e094ad-5b43-583e-8321-7611b63df58f/scratchpad/fc/big/s0 --seeds 0 --frames 100 --size 384 384 --no-movie`
- segmentation: matter > 0.35 of robust range [0.0092, 1.2734], min area 7 px

## Measurements
- components: final 405, mean 364.0, max 446; occupancy final 0.31
- tracks: 1769; persistent (alive >= 50% of run): 352; longest 101 frames; alive start-to-end: 4
- size of persistent tracks: max/min area ratio 9.26 (1 = constant size)
- enclosures: components with a hole mean 0.76, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [406, 405, 405], H1 [0, 0, 0]
- motion: 12 long-lived tracks moved >= 1 body length; max speed 0.00967/time; max body lengths 1.4
- replication (lineage window K = 20 frames = time 2000, default): splits 472, persistent splits 162 (0 more failed only because the siblings re-merged within K), max generation 5, merges 155, merge/split ratio 0.328, nucleations 68
- channel total drift (end/start - 1): [0.3092, -0.9995, -0.7335, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 77 at frame 50: holes 0, rim-vs-core 0.33, rim-vs-outside 0.51, heterogeneity 0.07; core [0.952, 0.0, 0.026, 0.961] rim [0.636, 0.0, 0.079, 0.898]
  - track 89 at frame 50: holes 0, rim-vs-core 0.32, rim-vs-outside 0.51, heterogeneity 0.07; core [0.95, 0.0, 0.026, 0.962] rim [0.636, 0.0, 0.078, 0.898]
  - track 107 at frame 50: holes 0, rim-vs-core 0.30, rim-vs-outside 0.53, heterogeneity 0.06; core [0.951, 0.0, 0.025, 0.965] rim [0.666, 0.0, 0.076, 0.902]
  - track 1743 at frame 86: holes 0, rim-vs-core 0.37, rim-vs-outside 0.32, heterogeneity 0.06; core [0.906, 0.0, 0.041, 0.943] rim [0.538, 0.0, 0.086, 0.891]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 2171 components >= 14 px at frames [17, 33, 50, 67, 83, 100]):
  - radial prey a: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.907, rim/outside 16.8 (aggregate of 2171 individuals; 13/2171 membrane-like individually; rim level 0.862)
  - radial predator b: peak at rho=0.55 (in the peak band 0.5-1.5), rim/core 1.06, rim/outside 1.28 (aggregate of 2171 individuals; 9/2171 membrane-like individually; rim level 0.012)
  - radial fuel u: peak at rho=1.75 (OUTSIDE the peak band 0.5-1.5), rim/core 5.89, rim/outside 0.872 (aggregate of 2171 individuals; 0/2171 membrane-like individually; rim level 0.135)
  - radial waste w: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.951, rim/outside 1.17 (aggregate of 2171 individuals; 0/2171 membrane-like individually; rim level 0.928)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #77 (t=5000, R_eq 6.21): none; #89 (t=5000, R_eq 6.21): none; #107 (t=5000, R_eq 6.18): none; #1743 (t=8600, R_eq 5.67): none
- species `prey` (channels ['prey a'], own threshold): components final 405, mean 352.5, max 447; tracks 1384, persistent 352; splits 348, persistent splits 162 (K=20), max generation 5, merges 96, merge/split 0.276; moving tracks 12
- species `predator` (channels ['predator b'], own threshold): components final 0, mean 22.5, max 176; tracks 509, persistent 0; splits 127, persistent splits 0 (K=20), max generation 0, merges 35, merge/split 0.276; moving tracks 2

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 15 of 2171 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
