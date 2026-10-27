# Evidence pack: driven-condensate-prey-predator (seed 71)

- world: `../../20261026T2103-c46-hunting-ecology-claim/world.py`, family `active-emulsion`
- parent: collective/contrib/20261026T1302-c42-foodchain-both-divide-claim; mutation: prey condensate whose miscibility gap is opened only by its own fuel-driven catalysis product (active chi); prey matter recycled from predator waste, not made from fuel
- run: 121 frames x 500 steps x dt 0.2 = time 12000; grid [256, 256]; wall 1398s; status ok
- command: `python -m labkit.run collective/contrib/20261026T2103-c46-hunting-ecology-claim/world.py --out collective/contrib/c57-w11/twin --seeds 71 --size 256 256 --frames 120 --lineage-k 5 --no-movie`
- segmentation: matter > 0.50 of robust range [0.1162, 0.8789], min area 6 px

## Measurements
- components: final 84, mean 56.9, max 84; occupancy final 0.15
- tracks: 113; persistent (alive >= 50% of run): 55; longest 119 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 41.29 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [93, 91, 84], H1 [0, 0, 0]
- motion: 1 long-lived tracks moved >= 1 body length; max speed 0.00109/time; max body lengths 1.1
- replication (lineage window K = 5 frames = time 500, --lineage-k): splits 29, persistent splits 25 (0 more failed only because the siblings re-merged within K), max generation 1, merges 0, merge/split ratio 0, nucleations 55
- channel total drift (end/start - 1): [0.0, None, -0.5517, -0.5121]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 1 at frame 62: holes 0, rim-vs-core 0.27, rim-vs-outside 0.52, heterogeneity 0.07; core [0.923, 0.0, 0.019, 0.828] rim [0.714, 0.0, 0.095, 0.676]
  - track 6 at frame 62: holes 0, rim-vs-core 0.30, rim-vs-outside 0.55, heterogeneity 0.07; core [0.951, 0.0, 0.023, 0.885] rim [0.727, 0.0, 0.108, 0.711]
  - track 7 at frame 62: holes 0, rim-vs-core 0.28, rim-vs-outside 0.53, heterogeneity 0.07; core [0.923, 0.0, 0.021, 0.834] rim [0.704, 0.0, 0.108, 0.682]
  - track 55 at frame 95: holes 0, rim-vs-core 0.39, rim-vs-outside 0.32, heterogeneity 0.08; core [0.926, 0.0, 0.056, 0.912] rim [0.648, 0.0, 0.14, 0.658]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 375 components >= 12 px at frames [20, 40, 61, 80, 100, 120]):
  - radial prey a: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.876, rim/outside 15.4 (aggregate of 375 individuals; 0/375 membrane-like individually; rim level 0.799)
  - radial predator b: flat profile (no radial structure; level 0; aggregate of 375 individuals)
  - radial fuel F: peak at rho=2.45 (OUTSIDE the peak band 0.5-1.5), rim/core 8.94, rim/outside 0.662 (aggregate of 375 individuals; 0/375 membrane-like individually; rim level 0.231)
  - radial product p: peak at rho=0.25 (OUTSIDE the peak band 0.5-1.5), rim/core 0.924, rim/outside 15.8 (aggregate of 375 individuals; 0/375 membrane-like individually; rim level 0.766)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #1 (t=6200, R_eq 7.11): none; #6 (t=6200, R_eq 6.36): none; #7 (t=6200, R_eq 7.14): none; #55 (t=9500, R_eq 5.86): none
- species `prey` (channels ['prey a'], own threshold): components final 82, mean 57.5, max 82; tracks 109, persistent 55; splits 27, persistent splits 23 (K=5), max generation 1, merges 0, merge/split 0; moving tracks 0
- species `predator` (channels ['predator b'], own threshold): components final 0, mean 0.0, max 0; tracks 0, persistent 0; splits 0, persistent splits 0 (K=5), max generation 0, merges 0, merge/split n/a; moving tracks 0

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 4 of 375 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
