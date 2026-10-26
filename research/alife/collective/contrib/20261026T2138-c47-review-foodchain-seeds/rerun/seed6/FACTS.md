# Evidence pack: condensate-food-chain (seed 6)

- world: `../../../20261026T1302-c42-foodchain-both-divide-claim/world.py`, family `active-emulsion`
- parent: threads/active-droplets/worlds/ad1-fuel; mutation: two immiscible autocatalytic condensates in a closed chain: prey made from fuel, predator made from prey material; decay -> waste -> fuel
- run: 121 frames x 200 steps x dt 0.5 = time 12000; grid [128, 128]; wall 158s; status ok
- command: `python -m labkit.run collective/contrib/20261026T1302-c42-foodchain-both-divide-claim/world.py --out collective/contrib/20261026T2138-c47-review-foodchain-seeds/rerun/seed6 --seeds 6 --size 128 128 --frames 120 --lineage-k 5 --no-movie`
- segmentation: matter > 0.35 of robust range [0.0355, 1.3116], min area 6 px

## Measurements
- components: final 34, mean 35.5, max 67; occupancy final 0.22
- tracks: 494; persistent (alive >= 50% of run): 0; longest 39 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 0.00 (1 = constant size)
- enclosures: components with a hole mean 2.09, final 1; holes at thresholds 0.2/0.35/0.5 final [1, 1, 2]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [40, 33, 24], H1 [2, 1, 0]
- motion: 3 long-lived tracks moved >= 1 body length; max speed 0.00728/time; max body lengths 1.2
- replication (lineage window K = 5 frames = time 500, --lineage-k): splits 151, persistent splits 73 (0 more failed only because the siblings re-merged within K), max generation 6, merges 44, merge/split ratio 0.291, nucleations 64
- channel total drift (end/start - 1): [-0.4121, 3.1688, -0.3818, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 75 at frame 21: holes 0, rim-vs-core 0.24, rim-vs-outside 0.24, heterogeneity 0.05; core [0.004, 0.843, 0.703, 0.114] rim [0.015, 0.599, 0.697, 0.114]
  - track 367 at frame 98: holes 0, rim-vs-core 0.24, rim-vs-outside 0.26, heterogeneity 0.05; core [0.005, 0.828, 0.667, 0.205] rim [0.015, 0.583, 0.667, 0.202]
  - track 110 at frame 19: holes 0, rim-vs-core 0.30, rim-vs-outside 0.52, heterogeneity 0.08; core [0.924, 0.034, 0.035, 0.895] rim [0.645, 0.024, 0.122, 0.81]
  - track 357 at frame 85: holes 0, rim-vs-core 0.23, rim-vs-outside 0.25, heterogeneity 0.04; core [0.007, 0.819, 0.705, 0.108] rim [0.018, 0.587, 0.704, 0.107]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 181 components >= 12 px at frames [20, 40, 61, 80, 100, 120]):
  - radial prey a: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.959, rim/outside 3.4 (aggregate of 181 individuals; 18/181 membrane-like individually; rim level 0.254)
  - radial predator b: peak at rho=0.25 (OUTSIDE the peak band 0.5-1.5), rim/core 1.04, rim/outside 5.22 (aggregate of 181 individuals; 25/181 membrane-like individually; rim level 0.486)
  - radial fuel u: peak at rho=1.85 (OUTSIDE the peak band 0.5-1.5), rim/core 1.22, rim/outside 0.958 (aggregate of 181 individuals; 0/181 membrane-like individually; rim level 0.512)
  - radial waste w: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.906, rim/outside 1.26 (aggregate of 181 individuals; 0/181 membrane-like individually; rim level 0.402)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #75 (t=2100, R_eq 5.59): none; #367 (t=9800, R_eq 5.73): none; #110 (t=1900, R_eq 6.75): none; #357 (t=8500, R_eq 3.24): none
- species `prey` (channels ['prey a'], own threshold): components final 10, mean 13.9, max 60; tracks 298, persistent 0; splits 78, persistent splits 21 (K=5), max generation 5, merges 7, merge/split 0.09; moving tracks 3
- species `predator` (channels ['predator b'], own threshold): components final 25, mean 25.0, max 34; tracks 341, persistent 0; splits 87, persistent splits 38 (K=5), max generation 2, merges 22, merge/split 0.253; moving tracks 16

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 28 of 181 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
