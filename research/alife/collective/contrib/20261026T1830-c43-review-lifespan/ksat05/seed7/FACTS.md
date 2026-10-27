# Evidence pack: condensate-food-chain (seed 7)

- world: `../../world.py`, family `active-emulsion`
- parent: threads/active-droplets/worlds/ad1-fuel; mutation: two immiscible autocatalytic condensates in a closed chain: prey made from fuel, predator made from prey material; decay -> waste -> fuel
- run: 121 frames x 200 steps x dt 0.5 = time 12000; grid [128, 128]; wall 202s; status ok
- command: `python -m labkit.run collective/contrib/20261026T1830-c43-review-lifespan/world.py --out collective/contrib/20261026T1830-c43-review-lifespan/ksat05/seed7 --seeds 7 --size 128 128 --frames 120 --no-movie`
- segmentation: matter > 0.35 of robust range [0.0411, 1.2419], min area 6 px

## Measurements
- components: final 56, mean 50.7, max 64; occupancy final 0.22
- tracks: 239; persistent (alive >= 50% of run): 39; longest 121 frames; alive start-to-end: 1
- size of persistent tracks: max/min area ratio 26.17 (1 = constant size)
- enclosures: components with a hole mean 1.64, final 1; holes at thresholds 0.2/0.35/0.5 final [2, 1, 1]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [67, 56, 56], H1 [3, 2, 1]
- motion: 2 long-lived tracks moved >= 1 body length; max speed 0.00177/time; max body lengths 1.6
- replication (lineage window K = 20 frames = time 2000, default): splits 55, persistent splits 7 (0 more failed only because the siblings re-merged within K), max generation 1, merges 42, merge/split ratio 0.764, nucleations 19
- channel total drift (end/start - 1): [-0.7564, 5.54, -0.23, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 28 at frame 61: holes 0, rim-vs-core 0.31, rim-vs-outside 0.27, heterogeneity 0.05; core [0.002, 0.902, 0.743, 0.034] rim [0.012, 0.593, 0.742, 0.033]
  - track 53 at frame 61: holes 0, rim-vs-core 0.29, rim-vs-outside 0.27, heterogeneity 0.04; core [0.002, 0.914, 0.745, 0.046] rim [0.011, 0.622, 0.744, 0.044]
  - track 64 at frame 62: holes 0, rim-vs-core 0.23, rim-vs-outside 0.28, heterogeneity 0.04; core [0.002, 0.905, 0.726, 0.06] rim [0.009, 0.672, 0.724, 0.06]
  - track 150 at frame 67: holes 0, rim-vs-core 0.19, rim-vs-outside 0.49, heterogeneity 0.04; core [0.001, 0.904, 0.727, 0.055] rim [0.007, 0.718, 0.722, 0.055]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 300 components >= 12 px at frames [20, 40, 61, 80, 100, 120]):
  - radial prey a: peak at rho=2.45 (OUTSIDE the peak band 0.5-1.5), rim/core 1.32, rim/outside 0.658 (aggregate of 300 individuals; 6/300 membrane-like individually; rim level 0.0382)
  - radial predator b: peak at rho=0.25 (OUTSIDE the peak band 0.5-1.5), rim/core 0.895, rim/outside 6.62 (aggregate of 300 individuals; 25/300 membrane-like individually; rim level 0.714)
  - radial fuel u: peak at rho=1.75 (OUTSIDE the peak band 0.5-1.5), rim/core 1.01, rim/outside 1 (aggregate of 300 individuals; 0/300 membrane-like individually; rim level 0.684)
  - radial waste w: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.96, rim/outside 1.11 (aggregate of 300 individuals; 0/300 membrane-like individually; rim level 0.092)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #28 (t=6100, R_eq 4.15): none; #53 (t=6100, R_eq 4.07): none; #64 (t=6200, R_eq 2.76): none; #150 (t=6700, R_eq 7.69, ring): ['predator b']
- species `prey` (channels ['prey a'], own threshold): components final 0, mean 5.8, max 58; tracks 147, persistent 0; splits 29, persistent splits 0 (K=20), max generation 0, merges 11, merge/split 0.379; moving tracks 0
- species `predator` (channels ['predator b'], own threshold): components final 55, mean 45.9, max 57; tracks 151, persistent 41; splits 36, persistent splits 12 (K=20), max generation 3, merges 19, merge/split 0.528; moving tracks 5

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 32 of 300 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
