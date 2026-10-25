# Evidence pack: act-cpm (seed 0)

- world: `../../world.py`, family `cellular-potts`
- parent: None; mutation: new class: Cellular Potts model with the Act (actin activity memory) term of Niculescu et al. 2015, cells planted as 3x3 seeds
- run: 201 frames x 10 steps x dt 1.0 = time 2000; grid [128, 128]; wall 3s; status ok
- command: `python -m labkit.run collective/contrib/wip-c27m/world.py --out collective/contrib/wip-c27m/pack --seeds 0 1 --frames 200 --no-movie`
- segmentation: matter > 0.50 of robust range [0.0, 1.0], min area 6 px

## Measurements
- components: final 40, mean 40.1, max 42; occupancy final 0.24
- tracks: 186; persistent (alive >= 50% of run): 27; longest 200 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 1.75 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [40, 40, 40], H1 [0, 0, 0]
- motion: 96 long-lived tracks moved >= 1 body length; max speed 0.219/time; max body lengths 25.3
- replication (lineage window K = 20 frames = time 200, default): splits 63, persistent splits 13 (0 more failed only because the siblings re-merged within K), max generation 2, merges 46, merge/split ratio 0.73, nucleations 42
- channel total drift (end/start - 1): [96.35, 9.5658, 4.575]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 17 at frame 101: holes 0, rim-vs-core 0.14, rim-vs-outside 1.42, heterogeneity 0.09; core [1.0, 0.107, 0.0] rim [1.0, 0.245, 0.0]
  - track 22 at frame 101: holes 0, rim-vs-core 0.06, rim-vs-outside 1.42, heterogeneity 0.10; core [1.0, 0.341, 0.0] rim [1.0, 0.403, 0.0]
  - track 30 at frame 101: holes 0, rim-vs-core 0.02, rim-vs-outside 1.43, heterogeneity 0.10; core [1.0, 0.259, 0.0] rim [1.0, 0.237, 0.0]
  - track 115 at frame 161: holes 0, rim-vs-core 0.16, rim-vs-outside 1.43, heterogeneity 0.10; core [1.0, 0.207, 0.0] rim [1.0, 0.37, 0.0]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 240 components >= 12 px at frames [34, 67, 101, 133, 166, 200]):
  - radial cell (sigma > 0): peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.776, rim/outside 2.55 (aggregate of 240 individuals; 0/240 membrane-like individually; rim level 0.752)
  - radial activity act/max: peak at rho=0.95 (in the peak band 0.5-1.5), rim/core 2.24, rim/outside 2.06 (aggregate of 240 individuals; 172/240 membrane-like individually; rim level 0.307)  MEMBRANE-LIKE
  - radial cell boundary: peak at rho=1.05 (in the peak band 0.5-1.5), rim/core 9.14, rim/outside 2 (aggregate of 240 individuals; 225/240 membrane-like individually; rim level 0.299)  MEMBRANE-LIKE
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): activity act/max, cell boundary
- membrane-like channels per top track at mid-life: #17 (t=1010, R_eq 5.59): ['activity act/max', 'cell boundary']; #22 (t=1010, R_eq 5.67): ['activity act/max', 'cell boundary']; #30 (t=1010, R_eq 5.59): ['activity act/max', 'cell boundary']; #115 (t=1610, R_eq 5.61): ['activity act/max', 'cell boundary']

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 2 of 240 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
