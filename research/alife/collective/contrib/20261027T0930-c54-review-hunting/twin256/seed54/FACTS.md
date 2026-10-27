# Evidence pack: driven-condensate-prey-predator (seed 54)

- world: `../../../20261026T2103-c46-hunting-ecology-claim/world.py`, family `active-emulsion`
- parent: collective/contrib/20261026T1302-c42-foodchain-both-divide-claim; mutation: prey condensate whose miscibility gap is opened only by its own fuel-driven catalysis product (active chi); prey matter recycled from predator waste, not made from fuel
- run: 121 frames x 500 steps x dt 0.2 = time 12000; grid [256, 256]; wall 1506s; status ok
- command: `python -m labkit.run collective/contrib/20261026T2103-c46-hunting-ecology-claim/world.py --out collective/contrib/20261027T0930-c54-review-hunting/twin256/seed54 --seeds 54 --size 256 256 --frames 120 --lineage-k 5 --no-movie`
- segmentation: matter > 0.50 of robust range [0.118, 0.8791], min area 6 px

## Measurements
- components: final 78, mean 61.3, max 78; occupancy final 0.15
- tracks: 93; persistent (alive >= 50% of run): 63; longest 119 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 30.00 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [88, 82, 78], H1 [0, 0, 0]
- motion: 1 long-lived tracks moved >= 1 body length; max speed 0.0012/time; max body lengths 1.2
- replication (lineage window K = 5 frames = time 500, --lineage-k): splits 15, persistent splits 13 (0 more failed only because the siblings re-merged within K), max generation 1, merges 0, merge/split ratio 0, nucleations 63
- channel total drift (end/start - 1): [0.0, None, -0.5471, -0.5136]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 0 at frame 62: holes 0, rim-vs-core 0.27, rim-vs-outside 0.53, heterogeneity 0.07; core [0.929, 0.0, 0.023, 0.852] rim [0.717, 0.0, 0.109, 0.703]
  - track 1 at frame 62: holes 0, rim-vs-core 0.29, rim-vs-outside 0.55, heterogeneity 0.07; core [0.953, 0.0, 0.023, 0.887] rim [0.734, 0.0, 0.108, 0.72]
  - track 2 at frame 62: holes 0, rim-vs-core 0.28, rim-vs-outside 0.53, heterogeneity 0.08; core [0.931, 0.0, 0.022, 0.847] rim [0.713, 0.0, 0.099, 0.682]
  - track 63 at frame 102: holes 0, rim-vs-core 0.39, rim-vs-outside 0.32, heterogeneity 0.08; core [0.925, 0.0, 0.056, 0.91] rim [0.648, 0.0, 0.135, 0.65]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 398 components >= 12 px at frames [20, 40, 61, 80, 100, 120]):
  - radial prey a: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.888, rim/outside 19.9 (aggregate of 398 individuals; 0/398 membrane-like individually; rim level 0.832)
  - radial predator b: flat profile (no radial structure; level 0; aggregate of 398 individuals)
  - radial fuel F: peak at rho=2.45 (OUTSIDE the peak band 0.5-1.5), rim/core 10.5, rim/outside 0.662 (aggregate of 398 individuals; 0/398 membrane-like individually; rim level 0.234)
  - radial product p: peak at rho=0.35 (OUTSIDE the peak band 0.5-1.5), rim/core 0.941, rim/outside 20.1 (aggregate of 398 individuals; 1/398 membrane-like individually; rim level 0.804)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #0 (t=6200, R_eq 6.98): none; #1 (t=6200, R_eq 6.38): none; #2 (t=6200, R_eq 6.98): none; #63 (t=10200, R_eq 5.64): none
- species `prey` (channels ['prey a'], own threshold): components final 78, mean 62.4, max 78; tracks 93, persistent 63; splits 15, persistent splits 12 (K=5), max generation 1, merges 0, merge/split 0; moving tracks 0
- species `predator` (channels ['predator b'], own threshold): components final 0, mean 0.0, max 0; tracks 0, persistent 0; splits 0, persistent splits 0 (K=5), max generation 0, merges 0, merge/split n/a; moving tracks 0

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 1 of 398 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
