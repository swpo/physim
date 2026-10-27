# Evidence pack: driven-condensate-prey-predator (seed 7)

- world: `../../../../../home/user/physim/research/alife/collective/contrib/20261026T2103-c46-hunting-ecology-claim/world.py`, family `active-emulsion`
- parent: collective/contrib/20261026T1302-c42-foodchain-both-divide-claim; mutation: prey condensate whose miscibility gap is opened only by its own fuel-driven catalysis product (active chi); prey matter recycled from predator waste, not made from fuel
- run: 121 frames x 500 steps x dt 0.2 = time 12000; grid [256, 256]; wall 1834s; status ok
- command: `python -m labkit.run collective/contrib/20261026T2103-c46-hunting-ecology-claim/world.py --out /tmp/claude-0/hu/twin/seed7 --seeds 7 --size 256 256 --frames 120 --lineage-k 5 --no-movie`
- segmentation: matter > 0.50 of robust range [0.1176, 0.8797], min area 6 px

## Measurements
- components: final 86, mean 57.7, max 86; occupancy final 0.15
- tracks: 116; persistent (alive >= 50% of run): 56; longest 119 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 48.17 (1 = constant size)
- enclosures: components with a hole mean 0.17, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [96, 89, 85], H1 [0, 0, 0]
- motion: 2 long-lived tracks moved >= 1 body length; max speed 0.00114/time; max body lengths 1.1
- replication (lineage window K = 5 frames = time 500, --lineage-k): splits 30, persistent splits 27 (0 more failed only because the siblings re-merged within K), max generation 2, merges 0, merge/split ratio 0, nucleations 56
- channel total drift (end/start - 1): [-0.0, None, -0.5498, -0.5127]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 0 at frame 62: holes 0, rim-vs-core 0.25, rim-vs-outside 0.52, heterogeneity 0.08; core [0.906, 0.0, 0.015, 0.805] rim [0.707, 0.0, 0.089, 0.665]
  - track 5 at frame 62: holes 0, rim-vs-core 0.39, rim-vs-outside 0.31, heterogeneity 0.08; core [0.918, 0.0, 0.055, 0.9] rim [0.644, 0.0, 0.129, 0.64]
  - track 7 at frame 62: holes 0, rim-vs-core 0.32, rim-vs-outside 0.55, heterogeneity 0.08; core [0.957, 0.0, 0.026, 0.905] rim [0.719, 0.0, 0.107, 0.704]
  - track 104 at frame 115: holes 0, rim-vs-core 0.39, rim-vs-outside 0.32, heterogeneity 0.09; core [0.92, 0.0, 0.066, 0.922] rim [0.643, 0.0, 0.139, 0.656]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 379 components >= 12 px at frames [20, 40, 61, 80, 100, 120]):
  - radial prey a: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.882, rim/outside 16.2 (aggregate of 379 individuals; 3/379 membrane-like individually; rim level 0.805)
  - radial predator b: flat profile (no radial structure; level 0; aggregate of 379 individuals)
  - radial fuel F: peak at rho=2.45 (OUTSIDE the peak band 0.5-1.5), rim/core 8.69, rim/outside 0.664 (aggregate of 379 individuals; 0/379 membrane-like individually; rim level 0.228)
  - radial product p: peak at rho=0.25 (OUTSIDE the peak band 0.5-1.5), rim/core 0.926, rim/outside 16.4 (aggregate of 379 individuals; 4/379 membrane-like individually; rim level 0.778)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #0 (t=6200, R_eq 8.63): none; #5 (t=6200, R_eq 5.53): none; #7 (t=6200, R_eq 6.05): none; #104 (t=11500, R_eq 5.29): none
- species `prey` (channels ['prey a'], own threshold): components final 85, mean 58.3, max 85; tracks 114, persistent 56; splits 29, persistent splits 27 (K=5), max generation 2, merges 0, merge/split 0; moving tracks 0
- species `predator` (channels ['predator b'], own threshold): components final 0, mean 0.0, max 0; tracks 0, persistent 0; splits 0, persistent splits 0 (K=5), max generation 0, merges 0, merge/split n/a; moving tracks 0

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 4 of 379 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
