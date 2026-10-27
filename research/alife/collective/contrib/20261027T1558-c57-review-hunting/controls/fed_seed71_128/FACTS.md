# Evidence pack: driven-condensate-prey-predator (seed 71)

- world: `../../20261026T2103-c46-hunting-ecology-claim/world.py`, family `active-emulsion`
- parent: collective/contrib/20261026T1302-c42-foodchain-both-divide-claim; mutation: prey condensate whose miscibility gap is opened only by its own fuel-driven catalysis product (active chi); prey matter recycled from predator waste, not made from fuel
- run: 76 frames x 500 steps x dt 0.2 = time 7500; grid [128, 128]; wall 262s; status ok
- command: `python -m labkit.run collective/contrib/20261026T2103-c46-hunting-ecology-claim/world.py --out collective/contrib/c57-w11/fed128 --seeds 71 --frames 75 --lineage-k 5 --no-movie`
- segmentation: matter > 0.35 of robust range [0.1419, 1.1626], min area 6 px

## Measurements
- components: final 17, mean 16.1, max 29; occupancy final 0.11
- tracks: 38; persistent (alive >= 50% of run): 13; longest 62 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 21.50 (1 = constant size)
- enclosures: components with a hole mean 0.08, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [20, 18, 15], H1 [0, 0, 0]
- motion: 0 long-lived tracks moved >= 1 body length; max speed 0/time; max body lengths 0.5
- replication (lineage window K = 5 frames = time 500, --lineage-k): splits 3, persistent splits 0 (0 more failed only because the siblings re-merged within K), max generation 0, merges 0, merge/split ratio 0, nucleations 32
- channel total drift (end/start - 1): [-0.088, None, -0.483, -0.5691]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 0 at frame 33: holes 0, rim-vs-core 0.28, rim-vs-outside 0.24, heterogeneity 0.04; core [0.0, 0.856, 0.546, 0.0] rim [0.005, 0.577, 0.539, 0.005]
  - track 2 at frame 33: holes 0, rim-vs-core 0.32, rim-vs-outside 0.25, heterogeneity 0.05; core [0.0, 0.884, 0.538, 0.0] rim [0.004, 0.567, 0.53, 0.003]
  - track 4 at frame 37: holes 0, rim-vs-core 0.33, rim-vs-outside 0.28, heterogeneity 0.05; core [0.0, 0.932, 0.53, 0.0] rim [0.007, 0.602, 0.526, 0.006]
  - track 1 at frame 32: holes 0, rim-vs-core 0.30, rim-vs-outside 0.23, heterogeneity 0.04; core [0.0, 0.878, 0.532, 0.0] rim [0.001, 0.58, 0.525, 0.001]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 97 components >= 12 px at frames [12, 25, 38, 50, 62, 75]):
  - radial prey a: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.822, rim/outside 4.5 (aggregate of 97 individuals; 3/97 membrane-like individually; rim level 0.416)
  - radial predator b: peak at rho=0.25 (OUTSIDE the peak band 0.5-1.5), rim/core 0.953, rim/outside 12.3 (aggregate of 97 individuals; 0/97 membrane-like individually; rim level 0.438)
  - radial fuel F: peak at rho=2.45 (OUTSIDE the peak band 0.5-1.5), rim/core 1.38, rim/outside 0.904 (aggregate of 97 individuals; 0/97 membrane-like individually; rim level 0.356)
  - radial product p: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.863, rim/outside 5.06 (aggregate of 97 individuals; 3/97 membrane-like individually; rim level 0.414)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #0 (t=3300, R_eq 4.3): none; #2 (t=3300, R_eq 4.3): none; #4 (t=3700, R_eq 3.52): none; #1 (t=3200, R_eq 4.07): none
- species `prey` (channels ['prey a'], own threshold): components final 9, mean 9.7, max 19; tracks 54, persistent 1; splits 10, persistent splits 0 (K=5), max generation 0, merges 0, merge/split 0; moving tracks 3
- species `predator` (channels ['predator b'], own threshold): components final 9, mean 8.8, max 17; tracks 30, persistent 8; splits 3, persistent splits 0 (K=5), max generation 0, merges 0, merge/split 0; moving tracks 0

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
