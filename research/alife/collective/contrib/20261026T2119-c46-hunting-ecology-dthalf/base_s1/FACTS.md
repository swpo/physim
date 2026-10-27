# Evidence pack: driven-condensate-prey-predator (seed 1)

- world: `../../world3.py`, family `active-emulsion`
- parent: collective/contrib/20261026T1302-c42-foodchain-both-divide-claim; mutation: prey condensate whose miscibility gap is opened only by its own fuel-driven catalysis product (active chi); prey matter recycled from predator waste, not made from fuel
- run: 121 frames x 500 steps x dt 0.2 = time 12000; grid [128, 128]; wall 375s; status ok
- command: `python -m labkit.run collective/work_c46/world3.py --out collective/work_c46/lk/c_s1 --seeds 1 --frames 120 --lineage-k 5 --no-movie`
- segmentation: matter > 0.36 of robust range [0.1369, 1.1323], min area 6 px

## Measurements
- components: final 12, mean 12.6, max 20; occupancy final 0.10
- tracks: 46; persistent (alive >= 50% of run): 5; longest 84 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 59.38 (1 = constant size)
- enclosures: components with a hole mean 0.01, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [17, 13, 11], H1 [0, 0, 0]
- motion: 0 long-lived tracks moved >= 1 body length; max speed 0/time; max body lengths 0.6
- replication (lineage window K = 5 frames = time 500, --lineage-k): splits 9, persistent splits 6 (0 more failed only because the siblings re-merged within K), max generation 1, merges 0, merge/split ratio 0, nucleations 28
- channel total drift (end/start - 1): [-0.1081, None, -0.4673, -0.5772]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 14 at frame 75: holes 0, rim-vs-core 0.10, rim-vs-outside 0.63, heterogeneity 0.08; core [0.816, 0.0, 0.002, 0.65] rim [0.76, 0.0, 0.073, 0.703]
  - track 16 at frame 81: holes 0, rim-vs-core 0.20, rim-vs-outside 0.52, heterogeneity 0.07; core [0.91, 0.0, 0.012, 0.788] rim [0.74, 0.0, 0.096, 0.715]
  - track 24 at frame 87: holes 0, rim-vs-core 0.28, rim-vs-outside 0.54, heterogeneity 0.08; core [0.952, 0.0, 0.019, 0.872] rim [0.741, 0.0, 0.086, 0.702]
  - track 13 at frame 43: holes 0, rim-vs-core 0.32, rim-vs-outside 0.30, heterogeneity 0.05; core [0.009, 0.946, 0.525, 0.009] rim [0.019, 0.624, 0.523, 0.016]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 75 components >= 12 px at frames [20, 40, 61, 80, 100, 120]):
  - radial prey a: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.884, rim/outside 6.78 (aggregate of 75 individuals; 7/75 membrane-like individually; rim level 0.529)
  - radial predator b: peak at rho=0.25 (OUTSIDE the peak band 0.5-1.5), rim/core 0.949, rim/outside 7.68 (aggregate of 75 individuals; 4/75 membrane-like individually; rim level 0.294)
  - radial fuel F: peak at rho=2.35 (OUTSIDE the peak band 0.5-1.5), rim/core 1.79, rim/outside 0.832 (aggregate of 75 individuals; 0/75 membrane-like individually; rim level 0.341)
  - radial product p: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.938, rim/outside 7.83 (aggregate of 75 individuals; 8/75 membrane-like individually; rim level 0.517)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #14 (t=7500, R_eq 10.42): ['product p']; #16 (t=8100, R_eq 8.21): none; #24 (t=8700, R_eq 7.38): none; #13 (t=4300, R_eq 2.59): none
- species `prey` (channels ['prey a'], own threshold): components final 5, mean 8.7, max 14; tracks 63, persistent 5; splits 18, persistent splits 0 (K=5), max generation 0, merges 0, merge/split 0; moving tracks 3
- species `predator` (channels ['predator b'], own threshold): components final 9, mean 5.8, max 13; tracks 43, persistent 0; splits 9, persistent splits 5 (K=5), max generation 1, merges 0, merge/split 0; moving tracks 0

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 5 of 75 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
