# Evidence pack: fed-vortices (seed 1)

- world: `../../world.py`, family `fed-vortex`
- parent: None; mutation: -
- run: 1501 frames x 150 steps x dt 0.02 = time 4500; grid [128, 128]; wall 867s; status ok
- command: `python -m labkit.run collective/contrib/c53-fvh/world.py --out collective/contrib/c53-fvh/pack_sel --seeds 1 2 --frames 1500 --spf 150 --no-movie`
- segmentation: matter > 0.28 of robust range [0.0, 0.2142], min area 6 px

## Measurements
- components: final 33, mean 35.6, max 49; occupancy final 0.23
- tracks: 1793; persistent (alive >= 50% of run): 0; longest 599 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 0.00 (1 = constant size)
- enclosures: components with a hole mean 0.02, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [47, 42, 37], H1 [0, 0, 0]
- motion: 669 long-lived tracks moved >= 1 body length; max speed 0.923/time; max body lengths 42.9
- replication (lineage window K = 20 frames = time 60, default): splits 605, persistent splits 118 (0 more failed only because the siblings re-merged within K), max generation 21, merges 551, merge/split ratio 0.911, nucleations 0
- channel total drift (end/start - 1): [-0.2963, -0.0428, None, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 20 at frame 303: holes 0, rim-vs-core 0.68, rim-vs-outside 0.36, heterogeneity 0.16; core [0.764, 0.144, 0.896, 0.011] rim [0.39, 0.381, 0.38, 0.005]
  - track 22 at frame 252: holes 0, rim-vs-core 0.66, rim-vs-outside 0.37, heterogeneity 0.15; core [0.749, 0.14, 0.907, 0.004] rim [0.394, 0.369, 0.405, 0.003]
  - track 73 at frame 227: holes 0, rim-vs-core 0.66, rim-vs-outside 0.37, heterogeneity 0.15; core [0.763, 0.182, 0.881, 0.007] rim [0.386, 0.355, 0.369, 0.005]
  - track 1696 at frame 1475: holes 0, rim-vs-core 0.64, rim-vs-outside 0.36, heterogeneity 0.17; core [0.86, 0.136, 0.363, 0.649] rim [0.411, 0.311, 0.16, 0.285]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 208 components >= 12 px at frames [252, 504, 756, 996, 1248, 1500]):
  - radial |vorticity|: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.729, rim/outside 7.95 (aggregate of 208 individuals; 7/208 membrane-like individually; rim level 0.569)
  - radial fuel Y: peak at rho=2.25 (OUTSIDE the peak band 0.5-1.5), rim/core 5.03, rim/outside 0.804 (aggregate of 208 individuals; 0/208 membrane-like individually; rim level 0.45)
  - radial label a: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.772, rim/outside 8.83 (aggregate of 208 individuals; 13/208 membrane-like individually; rim level 0.283)
  - radial label b: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.707, rim/outside 7.51 (aggregate of 208 individuals; 9/208 membrane-like individually; rim level 0.4)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #20 (t=909, R_eq 5.2): none; #22 (t=756, R_eq 5.26): none; #73 (t=681, R_eq 4.92): none; #1696 (t=4425, R_eq 3.48): none

## Warnings
- radial: 13 of 208 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
