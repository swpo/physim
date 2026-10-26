# Evidence pack: condensate-food-chain (seed 47)

- world: `../../../20261026T1302-c42-foodchain-both-divide-claim/world.py`, family `active-emulsion`
- parent: threads/active-droplets/worlds/ad1-fuel; mutation: two immiscible autocatalytic condensates in a closed chain: prey made from fuel, predator made from prey material; decay -> waste -> fuel
- run: 81 frames x 200 steps x dt 0.5 = time 8000; grid [128, 128]; wall 102s; status ok
- command: `python -m labkit.run collective/contrib/20261026T1302-c42-foodchain-both-divide-claim/world.py --out collective/contrib/20261026T1721-c45-review-foodchain/efork/seed47 --seeds 47 --size 128 128 --frames 80 --lineage-k 5 --no-movie`
- segmentation: matter > 0.35 of robust range [0.0004, 1.313], min area 6 px

## Measurements
- components: final 0, mean 28.5, max 61; occupancy final 0.00
- tracks: 305; persistent (alive >= 50% of run): 0; longest 36 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 0.00 (1 = constant size)
- enclosures: components with a hole mean 1.53, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [2, 2, 1], H1 [1, 0, 0]
- motion: 0 long-lived tracks moved >= 1 body length; max speed 0/time; max body lengths 0.9
- replication (lineage window K = 5 frames = time 500, --lineage-k): splits 83, persistent splits 24 (0 more failed only because the siblings re-merged within K), max generation 2, merges 32, merge/split ratio 0.386, nucleations 32
- channel total drift (end/start - 1): [-1.0, -0.9888, -1.0, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 76 at frame 19: holes 0, rim-vs-core 0.29, rim-vs-outside 0.25, heterogeneity 0.04; core [0.012, 0.857, 0.806, 0.435] rim [0.027, 0.563, 0.801, 0.435]
  - track 101 at frame 19: holes 0, rim-vs-core 0.29, rim-vs-outside 0.27, heterogeneity 0.05; core [0.012, 0.86, 0.758, 0.451] rim [0.024, 0.57, 0.756, 0.451]
  - track 103 at frame 19: holes 0, rim-vs-core 0.41, rim-vs-outside 0.38, heterogeneity 0.20; core [0.221, 0.812, 0.384, 0.725] rim [0.289, 0.408, 0.404, 0.711]
  - track 197 at frame 37: holes 0, rim-vs-core 0.31, rim-vs-outside 0.27, heterogeneity 0.05; core [0.011, 0.879, 0.771, 0.452] rim [0.026, 0.574, 0.768, 0.451]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 120 components >= 12 px at frames [13, 27, 40, 53]):
  - radial prey a: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 1.02, rim/outside 2.79 (aggregate of 120 individuals; 12/120 membrane-like individually; rim level 0.225)
  - radial predator b: peak at rho=0.45 (OUTSIDE the peak band 0.5-1.5), rim/core 0.953, rim/outside 5.43 (aggregate of 120 individuals; 13/120 membrane-like individually; rim level 0.52)
  - radial fuel u: peak at rho=2.15 (OUTSIDE the peak band 0.5-1.5), rim/core 1.13, rim/outside 0.971 (aggregate of 120 individuals; 0/120 membrane-like individually; rim level 0.604)
  - radial waste w: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.96, rim/outside 1.08 (aggregate of 120 individuals; 0/120 membrane-like individually; rim level 0.612)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #76 (t=1900, R_eq 5.7): none; #101 (t=1900, R_eq 4.51): none; #103 (t=1900, R_eq 7.05): ['prey a']; #197 (t=3700, R_eq 4.72): none
- species `prey` (channels ['prey a'], own threshold): components final 0, mean 10.5, max 60; tracks 185, persistent 0; splits 40, persistent splits 2 (K=5), max generation 1, merges 7, merge/split 0.175; moving tracks 2
- species `predator` (channels ['predator b'], own threshold): components final 0, mean 20.8, max 34; tracks 198, persistent 1; splits 51, persistent splits 14 (K=5), max generation 2, merges 9, merge/split 0.176; moving tracks 11

## Warnings
- no components at the end: matter died out or fell below threshold
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 15 of 120 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
