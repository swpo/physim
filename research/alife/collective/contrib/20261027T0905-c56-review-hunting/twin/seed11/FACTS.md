# Evidence pack: driven-condensate-prey-predator (seed 11)

- world: `../../../collective/contrib/20261026T2103-c46-hunting-ecology-claim/world.py`, family `active-emulsion`
- parent: collective/contrib/20261026T1302-c42-foodchain-both-divide-claim; mutation: prey condensate whose miscibility gap is opened only by its own fuel-driven catalysis product (active chi); prey matter recycled from predator waste, not made from fuel
- run: 121 frames x 500 steps x dt 0.2 = time 12000; grid [256, 256]; wall 1353s; status ok
- command: `python -m labkit.run collective/contrib/20261026T2103-c46-hunting-ecology-claim/world.py --out c56work/rv/twin256 --seeds 11 --size 256 256 --frames 120 --lineage-k 5 --no-movie`
- segmentation: matter > 0.50 of robust range [0.1176, 0.8782], min area 6 px

## Measurements
- components: final 79, mean 53.5, max 79; occupancy final 0.15
- tracks: 109; persistent (alive >= 50% of run): 51; longest 119 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 37.67 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [92, 84, 79], H1 [0, 0, 0]
- motion: 1 long-lived tracks moved >= 1 body length; max speed 0.00107/time; max body lengths 1.1
- replication (lineage window K = 5 frames = time 500, --lineage-k): splits 28, persistent splits 23 (0 more failed only because the siblings re-merged within K), max generation 2, merges 1, merge/split ratio 0.036, nucleations 52
- channel total drift (end/start - 1): [-0.0, None, -0.5478, -0.5132]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 1 at frame 62: holes 0, rim-vs-core 0.28, rim-vs-outside 0.53, heterogeneity 0.08; core [0.933, 0.0, 0.028, 0.869] rim [0.723, 0.0, 0.107, 0.708]
  - track 2 at frame 62: holes 0, rim-vs-core 0.19, rim-vs-outside 0.61, heterogeneity 0.07; core [0.932, 0.0, 0.026, 0.853] rim [0.786, 0.0, 0.076, 0.739]
  - track 10 at frame 62: holes 0, rim-vs-core 0.26, rim-vs-outside 0.52, heterogeneity 0.07; core [0.921, 0.0, 0.019, 0.825] rim [0.719, 0.0, 0.102, 0.693]
  - track 97 at frame 117: holes 0, rim-vs-core 0.39, rim-vs-outside 0.31, heterogeneity 0.08; core [0.912, 0.0, 0.056, 0.891] rim [0.631, 0.0, 0.137, 0.635]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 348 components >= 12 px at frames [20, 40, 61, 80, 100, 120]):
  - radial prey a: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.879, rim/outside 14.8 (aggregate of 348 individuals; 3/348 membrane-like individually; rim level 0.786)
  - radial predator b: flat profile (no radial structure; level 0; aggregate of 348 individuals)
  - radial fuel F: peak at rho=2.45 (OUTSIDE the peak band 0.5-1.5), rim/core 7.94, rim/outside 0.664 (aggregate of 348 individuals; 0/348 membrane-like individually; rim level 0.231)
  - radial product p: peak at rho=0.25 (OUTSIDE the peak band 0.5-1.5), rim/core 0.925, rim/outside 14.8 (aggregate of 348 individuals; 9/348 membrane-like individually; rim level 0.754)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #1 (t=6200, R_eq 6.6): none; #2 (t=6200, R_eq 6.77): none; #10 (t=6200, R_eq 7.11): none; #97 (t=11700, R_eq 5.94): none
- species `prey` (channels ['prey a'], own threshold): components final 78, mean 54.0, max 78; tracks 108, persistent 51; splits 27, persistent splits 23 (K=5), max generation 2, merges 1, merge/split 0.037; moving tracks 1
- species `predator` (channels ['predator b'], own threshold): components final 0, mean 0.0, max 0; tracks 0, persistent 0; splits 0, persistent splits 0 (K=5), max generation 0, merges 0, merge/split n/a; moving tracks 0

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 9 of 348 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
