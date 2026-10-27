# Evidence pack: driven-condensate-prey-predator (seed 13)

- world: `../../20261026T2103-c46-hunting-ecology-claim/world.py`, family `active-emulsion`
- parent: collective/contrib/20261026T1302-c42-foodchain-both-divide-claim; mutation: prey condensate whose miscibility gap is opened only by its own fuel-driven catalysis product (active chi); prey matter recycled from predator waste, not made from fuel
- run: 121 frames x 500 steps x dt 0.2 = time 12000; grid [256, 256]; wall 1086s; status ok
- command: `python -m labkit.run collective/contrib/20261026T2103-c46-hunting-ecology-claim/world.py --out collective/contrib/20261027T0217-c51-review-hunting/twin256 --seeds 13 --size 256 256 --frames 120 --lineage-k 5 --no-movie`
- segmentation: matter > 0.50 of robust range [0.1172, 0.8771], min area 6 px

## Measurements
- components: final 79, mean 56.2, max 79; occupancy final 0.15
- tracks: 103; persistent (alive >= 50% of run): 55; longest 119 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 38.83 (1 = constant size)
- enclosures: components with a hole mean 0.25, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [92, 84, 79], H1 [0, 0, 0]
- motion: 2 long-lived tracks moved >= 1 body length; max speed 0.00105/time; max body lengths 1.0
- replication (lineage window K = 5 frames = time 500, --lineage-k): splits 24, persistent splits 24 (0 more failed only because the siblings re-merged within K), max generation 2, merges 0, merge/split ratio 0, nucleations 55
- channel total drift (end/start - 1): [0.0, None, -0.5499, -0.5139]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 2 at frame 62: holes 0, rim-vs-core 0.32, rim-vs-outside 0.56, heterogeneity 0.08; core [0.957, 0.0, 0.027, 0.898] rim [0.719, 0.0, 0.113, 0.706]
  - track 3 at frame 62: holes 0, rim-vs-core 0.27, rim-vs-outside 0.54, heterogeneity 0.07; core [0.937, 0.0, 0.021, 0.851] rim [0.731, 0.0, 0.101, 0.703]
  - track 4 at frame 62: holes 0, rim-vs-core 0.28, rim-vs-outside 0.52, heterogeneity 0.08; core [0.924, 0.0, 0.021, 0.833] rim [0.707, 0.0, 0.104, 0.679]
  - track 99 at frame 118: holes 0, rim-vs-core 0.39, rim-vs-outside 0.32, heterogeneity 0.09; core [0.92, 0.0, 0.066, 0.914] rim [0.639, 0.0, 0.143, 0.652]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 363 components >= 12 px at frames [20, 40, 61, 80, 100, 120]):
  - radial prey a: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.879, rim/outside 15.9 (aggregate of 363 individuals; 2/363 membrane-like individually; rim level 0.797)
  - radial predator b: flat profile (no radial structure; level 0; aggregate of 363 individuals)
  - radial fuel F: peak at rho=2.45 (OUTSIDE the peak band 0.5-1.5), rim/core 8.78, rim/outside 0.66 (aggregate of 363 individuals; 0/363 membrane-like individually; rim level 0.233)
  - radial product p: peak at rho=0.25 (OUTSIDE the peak band 0.5-1.5), rim/core 0.929, rim/outside 16.1 (aggregate of 363 individuals; 2/363 membrane-like individually; rim level 0.763)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #2 (t=6200, R_eq 6.31): none; #3 (t=6200, R_eq 6.89): none; #4 (t=6200, R_eq 7.16): none; #99 (t=11800, R_eq 5.67): none
- species `prey` (channels ['prey a'], own threshold): components final 79, mean 57.0, max 79; tracks 103, persistent 55; splits 24, persistent splits 22 (K=5), max generation 1, merges 0, merge/split 0; moving tracks 0
- species `predator` (channels ['predator b'], own threshold): components final 0, mean 0.0, max 0; tracks 0, persistent 0; splits 0, persistent splits 0 (K=5), max generation 0, merges 0, merge/split n/a; moving tracks 0

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 4 of 363 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
