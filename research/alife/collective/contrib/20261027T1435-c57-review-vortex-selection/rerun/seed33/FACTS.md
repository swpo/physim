# Evidence pack: fed-vortices (seed 33)

- world: `../../20261027T0845-c53-fed-vortex-selection-claim/world.py`, family `fed-vortex`
- parent: None; mutation: -
- run: 1501 frames x 150 steps x dt 0.02 = time 4500; grid [128, 128]; wall 888s; status ok
- command: `python -m labkit.run collective/contrib/20261027T0845-c53-fed-vortex-selection-claim/world.py --out collective/contrib/c57-w8/rerun --seeds 33 --frames 1500 --spf 150 --no-movie`
- segmentation: matter > 0.28 of robust range [0.0, 0.2136], min area 6 px

## Measurements
- components: final 35, mean 34.5, max 46; occupancy final 0.23
- tracks: 1739; persistent (alive >= 50% of run): 0; longest 529 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 0.00 (1 = constant size)
- enclosures: components with a hole mean 0.01, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [49, 47, 35], H1 [0, 0, 0]
- motion: 629 long-lived tracks moved >= 1 body length; max speed 0.845/time; max body lengths 85.6
- replication (lineage window K = 20 frames = time 60, default): splits 588, persistent splits 117 (0 more failed only because the siblings re-merged within K), max generation 24, merges 531, merge/split ratio 0.903, nucleations 0
- channel total drift (end/start - 1): [-0.2999, -0.0536, None, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 65 at frame 290: holes 0, rim-vs-core 0.69, rim-vs-outside 0.39, heterogeneity 0.16; core [0.817, 0.157, 0.905, 0.011] rim [0.403, 0.376, 0.394, 0.006]
  - track 8 at frame 214: holes 0, rim-vs-core 0.68, rim-vs-outside 0.35, heterogeneity 0.16; core [0.78, 0.169, 0.89, 0.007] rim [0.375, 0.371, 0.387, 0.004]
  - track 4 at frame 202: holes 0, rim-vs-core 0.67, rim-vs-outside 0.40, heterogeneity 0.15; core [0.798, 0.132, 0.929, 0.001] rim [0.43, 0.374, 0.429, 0.001]
  - track 1698 at frame 1487: holes 0, rim-vs-core 0.65, rim-vs-outside 0.33, heterogeneity 0.17; core [0.813, 0.105, 0.381, 0.692] rim [0.386, 0.301, 0.164, 0.298]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 198 components >= 12 px at frames [252, 504, 756, 996, 1248, 1500]):
  - radial |vorticity|: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.741, rim/outside 7.23 (aggregate of 198 individuals; 8/198 membrane-like individually; rim level 0.558)
  - radial fuel Y: peak at rho=2.25 (OUTSIDE the peak band 0.5-1.5), rim/core 4.72, rim/outside 0.798 (aggregate of 198 individuals; 0/198 membrane-like individually; rim level 0.452)
  - radial label a: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.746, rim/outside 7.61 (aggregate of 198 individuals; 9/198 membrane-like individually; rim level 0.294)
  - radial label b: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.726, rim/outside 7.42 (aggregate of 198 individuals; 10/198 membrane-like individually; rim level 0.422)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #65 (t=870, R_eq 4.44): none; #8 (t=642, R_eq 4.37): none; #4 (t=606, R_eq 4.98): none; #1698 (t=4461, R_eq 4.37): none

## Warnings
- radial: 9 of 198 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
