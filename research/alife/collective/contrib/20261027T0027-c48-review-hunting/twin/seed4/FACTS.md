# Evidence pack: driven-condensate-prey-predator (seed 4)

- world: `../../../20261026T2103-c46-hunting-ecology-claim/world.py`, family `active-emulsion`
- parent: collective/contrib/20261026T1302-c42-foodchain-both-divide-claim; mutation: prey condensate whose miscibility gap is opened only by its own fuel-driven catalysis product (active chi); prey matter recycled from predator waste, not made from fuel
- run: 121 frames x 500 steps x dt 0.2 = time 12000; grid [256, 256]; wall 1599s; status ok
- command: `python -m labkit.run collective/contrib/20261026T2103-c46-hunting-ecology-claim/world.py --out collective/contrib/20261027T0027-c48-review-hunting/twin/seed4 --seeds 4 --size 256 256 --frames 120 --lineage-k 5 --no-movie`
- segmentation: matter > 0.50 of robust range [0.1168, 0.8775], min area 6 px

## Measurements
- components: final 87, mean 59.8, max 87; occupancy final 0.15
- tracks: 118; persistent (alive >= 50% of run): 56; longest 118 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 38.71 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [96, 89, 87], H1 [0, 0, 0]
- motion: 1 long-lived tracks moved >= 1 body length; max speed 0.00107/time; max body lengths 1.1
- replication (lineage window K = 5 frames = time 500, --lineage-k): splits 31, persistent splits 30 (0 more failed only because the siblings re-merged within K), max generation 1, merges 0, merge/split ratio 0, nucleations 56
- channel total drift (end/start - 1): [0.0, None, -0.5545, -0.5143]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 5 at frame 62: holes 0, rim-vs-core 0.28, rim-vs-outside 0.55, heterogeneity 0.08; core [0.938, 0.0, 0.024, 0.87] rim [0.727, 0.0, 0.101, 0.706]
  - track 10 at frame 63: holes 0, rim-vs-core 0.25, rim-vs-outside 0.51, heterogeneity 0.07; core [0.918, 0.0, 0.016, 0.813] rim [0.715, 0.0, 0.1, 0.685]
  - track 11 at frame 63: holes 0, rim-vs-core 0.26, rim-vs-outside 0.51, heterogeneity 0.07; core [0.912, 0.0, 0.016, 0.805] rim [0.704, 0.0, 0.102, 0.672]
  - track 56 at frame 96: holes 0, rim-vs-core 0.40, rim-vs-outside 0.32, heterogeneity 0.08; core [0.925, 0.0, 0.067, 0.931] rim [0.646, 0.0, 0.139, 0.656]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 393 components >= 12 px at frames [20, 40, 61, 80, 100, 120]):
  - radial prey a: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.879, rim/outside 16.4 (aggregate of 393 individuals; 0/393 membrane-like individually; rim level 0.811)
  - radial predator b: flat profile (no radial structure; level 0; aggregate of 393 individuals)
  - radial fuel F: peak at rho=2.45 (OUTSIDE the peak band 0.5-1.5), rim/core 9.41, rim/outside 0.663 (aggregate of 393 individuals; 0/393 membrane-like individually; rim level 0.229)
  - radial product p: peak at rho=0.25 (OUTSIDE the peak band 0.5-1.5), rim/core 0.927, rim/outside 17 (aggregate of 393 individuals; 1/393 membrane-like individually; rim level 0.782)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #5 (t=6200, R_eq 7): none; #10 (t=6300, R_eq 7.14): none; #11 (t=6300, R_eq 7.33): none; #56 (t=9600, R_eq 5.23): none
- species `prey` (channels ['prey a'], own threshold): components final 87, mean 60.4, max 87; tracks 118, persistent 56; splits 31, persistent splits 29 (K=5), max generation 1, merges 0, merge/split 0; moving tracks 1
- species `predator` (channels ['predator b'], own threshold): components final 0, mean 0.0, max 0; tracks 0, persistent 0; splits 0, persistent splits 0 (K=5), max generation 0, merges 0, merge/split n/a; moving tracks 0

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 2 of 393 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
