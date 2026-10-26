# Evidence pack: phoretic-colloids (seed 3)

- world: `../../world.py`, family `phoretic-colloids`
- parent: None; mutation: -
- run: 401 frames x 1 steps x dt 0.5 = time 200; grid [128, 128]; wall 35s; status ok
- command: `python -m labkit.run collective/contrib/20261026T0315-c32-review-janus/world.py --out collective/contrib/20261026T0315-c32-review-janus/pack --seeds 2 3 --frames 400 --no-movie`
- segmentation: matter > 0.35 of robust range [0.0, 1.6845], min area 6 px

## Measurements
- components: final 16, mean 21.9, max 37; occupancy final 0.08
- tracks: 197; persistent (alive >= 50% of run): 7; longest 345 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 7.83 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [24, 19, 12], H1 [0, 0, 0]
- motion: 41 long-lived tracks moved >= 1 body length; max speed 0.414/time; max body lengths 6.3
- replication (lineage window K = 20 frames = time 10, default): splits 14, persistent splits 5 (0 more failed only because the siblings re-merged within K), max generation 2, merges 38, merge/split ratio 2.71, nucleations 130
- channel total drift (end/start - 1): [0.0, 0.0, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 38 at frame 229: holes 0, rim-vs-core 0.26, rim-vs-outside 0.31, heterogeneity 0.14; core [0.766, 0.409, 0.56] rim [0.537, 0.348, 0.455]
  - track 53 at frame 222: holes 0, rim-vs-core 0.37, rim-vs-outside 0.25, heterogeneity 0.18; core [0.418, 0.723, 0.388] rim [0.494, 0.366, 0.359]
  - track 69 at frame 218: holes 0, rim-vs-core 0.34, rim-vs-outside 0.33, heterogeneity 0.18; core [0.702, 0.687, 0.773] rim [0.473, 0.504, 0.594]
  - track 176 at frame 356: holes 0, rim-vs-core 0.26, rim-vs-outside 0.30, heterogeneity 0.08; core [0.897, 0.019, 0.369] rim [0.65, 0.063, 0.321]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 121 components >= 12 px at frames [67, 134, 202, 266, 333, 400]):
  - radial A density: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.827, rim/outside 12.1 (aggregate of 121 individuals; 5/121 membrane-like individually; rim level 0.653)
  - radial B density: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.946, rim/outside 11.1 (aggregate of 121 individuals; 43/121 membrane-like individually; rim level 0.4)
  - radial chemicals (sum): peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.822, rim/outside 2.5 (aggregate of 121 individuals; 0/121 membrane-like individually; rim level 0.544)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #38 (t=114.5, R_eq 3.74): none; #53 (t=111, R_eq 2.52): ['A density']; #69 (t=109, R_eq 5.17): none; #176 (t=178, R_eq 2.46): ['B density']

## Warnings
- none

## Files
sheet.png, particles.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
