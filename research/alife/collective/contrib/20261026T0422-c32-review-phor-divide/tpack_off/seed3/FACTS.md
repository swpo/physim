# Evidence pack: phoretic-colloids (seed 3)

- world: `../../world.py`, family `phoretic-colloids`
- parent: None; mutation: -
- run: 801 frames x 1 steps x dt 0.5 = time 400; grid [128, 128]; wall 70s; status ok
- command: `python -m labkit.run collective/contrib/20261026T0422-c32-review-phor-divide/world.py --out collective/contrib/20261026T0422-c32-review-phor-divide/tpack_off --seeds 2 3 --frames 800 --no-movie`
- segmentation: matter > 0.35 of robust range [0.0, 1.9324], min area 6 px

## Measurements
- components: final 9, mean 14.6, max 28; occupancy final 0.06
- tracks: 164; persistent (alive >= 50% of run): 11; longest 763 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 10.50 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [13, 9, 8], H1 [0, 0, 0]
- motion: 36 long-lived tracks moved >= 1 body length; max speed 0.334/time; max body lengths 11.7
- replication (lineage window K = 20 frames = time 10, default): splits 0, persistent splits 0 (0 more failed only because the siblings re-merged within K), max generation 0, merges 25, merge/split ratio n/a, nucleations 139
- channel total drift (end/start - 1): [0.0, -0.0, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 6 at frame 424: holes 0, rim-vs-core 0.23, rim-vs-outside 0.36, heterogeneity 0.13; core [0.728, 0.545, 0.426] rim [0.507, 0.578, 0.359]
  - track 34 at frame 370: holes 0, rim-vs-core 0.29, rim-vs-outside 0.29, heterogeneity 0.15; core [0.814, 0.363, 0.517] rim [0.553, 0.461, 0.427]
  - track 127 at frame 524: holes 0, rim-vs-core 0.26, rim-vs-outside 0.27, heterogeneity 0.10; core [0.872, 0.19, 0.472] rim [0.621, 0.17, 0.394]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 84 components >= 12 px at frames [134, 269, 403, 531, 666, 800]):
  - radial A density: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.859, rim/outside 18.3 (aggregate of 84 individuals; 0/84 membrane-like individually; rim level 0.716)
  - radial B density: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.895, rim/outside 16.9 (aggregate of 84 individuals; 38/84 membrane-like individually; rim level 0.431)
  - radial chemicals (sum): peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.814, rim/outside 3 (aggregate of 84 individuals; 0/84 membrane-like individually; rim level 0.533)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #6 (t=212, R_eq 3.24): ['B density']; #34 (t=185, R_eq 3.74): ['B density']; #127 (t=262, R_eq 3.43): ['B density']; #50 (t=178, R_eq 2.39): ['B density']

## Warnings
- none

## Files
sheet.png, particles.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
