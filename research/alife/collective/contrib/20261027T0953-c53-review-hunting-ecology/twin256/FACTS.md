# Evidence pack: driven-condensate-prey-predator (seed 8)

- world: `../../20261026T2103-c46-hunting-ecology-claim/world.py`, family `active-emulsion`
- parent: collective/contrib/20261026T1302-c42-foodchain-both-divide-claim; mutation: prey condensate whose miscibility gap is opened only by its own fuel-driven catalysis product (active chi); prey matter recycled from predator waste, not made from fuel
- run: 121 frames x 500 steps x dt 0.2 = time 12000; grid [256, 256]; wall 1527s; status ok
- command: `python -m labkit.run collective/contrib/20261026T2103-c46-hunting-ecology-claim/world.py --out collective/contrib/c53-rev-hc/twin256 --seeds 8 --size 256 256 --frames 120 --lineage-k 5 --no-movie`
- segmentation: matter > 0.50 of robust range [0.1179, 0.8805], min area 6 px

## Measurements
- components: final 87, mean 66.2, max 87; occupancy final 0.15
- tracks: 108; persistent (alive >= 50% of run): 66; longest 119 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 30.17 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [100, 92, 86], H1 [0, 0, 0]
- motion: 2 long-lived tracks moved >= 1 body length; max speed 0.00101/time; max body lengths 1.1
- replication (lineage window K = 5 frames = time 500, --lineage-k): splits 21, persistent splits 15 (0 more failed only because the siblings re-merged within K), max generation 1, merges 0, merge/split ratio 0, nucleations 66
- channel total drift (end/start - 1): [0.0, None, -0.5549, -0.5138]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 1 at frame 62: holes 0, rim-vs-core 0.28, rim-vs-outside 0.53, heterogeneity 0.07; core [0.93, 0.0, 0.017, 0.841] rim [0.715, 0.0, 0.101, 0.69]
  - track 2 at frame 62: holes 0, rim-vs-core 0.27, rim-vs-outside 0.53, heterogeneity 0.08; core [0.919, 0.0, 0.018, 0.833] rim [0.71, 0.0, 0.092, 0.674]
  - track 5 at frame 62: holes 0, rim-vs-core 0.31, rim-vs-outside 0.54, heterogeneity 0.08; core [0.948, 0.0, 0.023, 0.888] rim [0.713, 0.0, 0.109, 0.701]
  - track 66 at frame 97: holes 0, rim-vs-core 0.39, rim-vs-outside 0.33, heterogeneity 0.08; core [0.93, 0.0, 0.059, 0.934] rim [0.657, 0.0, 0.139, 0.672]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 428 components >= 12 px at frames [20, 40, 61, 80, 100, 120]):
  - radial prey a: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.877, rim/outside 18.7 (aggregate of 428 individuals; 0/428 membrane-like individually; rim level 0.818)
  - radial predator b: flat profile (no radial structure; level 0; aggregate of 428 individuals)
  - radial fuel F: peak at rho=2.45 (OUTSIDE the peak band 0.5-1.5), rim/core 10.2, rim/outside 0.663 (aggregate of 428 individuals; 0/428 membrane-like individually; rim level 0.227)
  - radial product p: peak at rho=0.25 (OUTSIDE the peak band 0.5-1.5), rim/core 0.922, rim/outside 18.6 (aggregate of 428 individuals; 0/428 membrane-like individually; rim level 0.792)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #1 (t=6200, R_eq 6.79): none; #2 (t=6200, R_eq 7.44): none; #5 (t=6200, R_eq 6.41): none; #66 (t=9700, R_eq 5.53): none
- species `prey` (channels ['prey a'], own threshold): components final 84, mean 67.3, max 84; tracks 103, persistent 66; splits 18, persistent splits 15 (K=5), max generation 1, merges 0, merge/split 0; moving tracks 1
- species `predator` (channels ['predator b'], own threshold): components final 0, mean 0.0, max 0; tracks 0, persistent 0; splits 0, persistent splits 0 (K=5), max generation 0, merges 0, merge/split n/a; moving tracks 0

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 1 of 428 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
