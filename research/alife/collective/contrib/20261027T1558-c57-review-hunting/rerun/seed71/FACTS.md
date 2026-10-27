# Evidence pack: driven-condensate-prey-predator (seed 71)

- world: `../../20261026T2103-c46-hunting-ecology-claim/world.py`, family `active-emulsion`
- parent: collective/contrib/20261026T1302-c42-foodchain-both-divide-claim; mutation: prey condensate whose miscibility gap is opened only by its own fuel-driven catalysis product (active chi); prey matter recycled from predator waste, not made from fuel
- run: 121 frames x 500 steps x dt 0.2 = time 12000; grid [256, 256]; wall 1793s; status ok
- command: `python -m labkit.run collective/contrib/20261026T2103-c46-hunting-ecology-claim/world.py --out collective/contrib/c57-w11/rerun --seeds 71 --size 256 256 --frames 120 --lineage-k 5 --no-movie`
- segmentation: matter > 0.35 of robust range [0.1427, 1.1733], min area 6 px

## Measurements
- components: final 50, mean 65.4, max 122; occupancy final 0.06
- tracks: 238; persistent (alive >= 50% of run): 22; longest 87 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 43.62 (1 = constant size)
- enclosures: components with a hole mean 0.11, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [59, 47, 35], H1 [0, 0, 0]
- motion: 1 long-lived tracks moved >= 1 body length; max speed 0.00135/time; max body lengths 1.1
- replication (lineage window K = 5 frames = time 500, --lineage-k): splits 41, persistent splits 22 (0 more failed only because the siblings re-merged within K), max generation 3, merges 0, merge/split ratio 0, nucleations 155
- channel total drift (end/start - 1): [-0.0668, None, -0.4993, -0.5583]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 60 at frame 78: holes 0, rim-vs-core 0.25, rim-vs-outside 0.48, heterogeneity 0.08; core [0.928, 0.0, 0.007, 0.799] rim [0.727, 0.0, 0.063, 0.656]
  - track 61 at frame 78: holes 0, rim-vs-core 0.26, rim-vs-outside 0.52, heterogeneity 0.07; core [0.942, 0.0, 0.01, 0.83] rim [0.749, 0.0, 0.057, 0.668]
  - track 70 at frame 81: holes 0, rim-vs-core 0.25, rim-vs-outside 0.46, heterogeneity 0.07; core [0.925, 0.0, 0.005, 0.789] rim [0.723, 0.0, 0.06, 0.645]
  - track 186 at frame 108: holes 0, rim-vs-core 0.27, rim-vs-outside 0.27, heterogeneity 0.04; core [0.022, 0.863, 0.54, 0.024] rim [0.03, 0.593, 0.538, 0.03]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 369 components >= 12 px at frames [20, 40, 61, 80, 100, 120]):
  - radial prey a: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.79, rim/outside 4.61 (aggregate of 369 individuals; 14/369 membrane-like individually; rim level 0.404)
  - radial predator b: peak at rho=0.25 (OUTSIDE the peak band 0.5-1.5), rim/core 0.933, rim/outside 8.81 (aggregate of 369 individuals; 6/369 membrane-like individually; rim level 0.411)
  - radial fuel F: peak at rho=2.45 (OUTSIDE the peak band 0.5-1.5), rim/core 1.52, rim/outside 0.899 (aggregate of 369 individuals; 0/369 membrane-like individually; rim level 0.375)
  - radial product p: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.833, rim/outside 5.21 (aggregate of 369 individuals; 15/369 membrane-like individually; rim level 0.396)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #60 (t=7800, R_eq 8.67): none; #61 (t=7800, R_eq 8.37): none; #70 (t=8100, R_eq 7.65): none; #186 (t=10800, R_eq 2.33): none
- species `prey` (channels ['prey a'], own threshold): components final 15, mean 32.9, max 59; tracks 289, persistent 11; splits 63, persistent splits 1 (K=5), max generation 1, merges 1, merge/split 0.016; moving tracks 19
- species `predator` (channels ['predator b'], own threshold): components final 39, mean 40.5, max 72; tracks 230, persistent 0; splits 37, persistent splits 19 (K=5), max generation 2, merges 4, merge/split 0.108; moving tracks 1

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 1 of 369 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
