# Evidence pack: phoretic-colloids (seed 0)

- world: `../world.py`, family `phoretic-colloids`
- parent: None; mutation: -
- run: 401 frames x 1 steps x dt 0.5 = time 200; grid [128, 128]; wall 110s; status ok
- command: `python -m labkit.run collective/contrib/wip-c33/world.py --out collective/contrib/wip-c33/pack_dthalf --seeds 0 --frames 400 --no-movie`
- segmentation: matter > 0.35 of robust range [0.0, 1.5814], min area 6 px

## Measurements
- components: final 16, mean 23.6, max 42; occupancy final 0.08
- tracks: 237; persistent (alive >= 50% of run): 10; longest 333 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 6.83 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [21, 20, 14], H1 [0, 0, 0]
- motion: 45 long-lived tracks moved >= 1 body length; max speed 0.351/time; max body lengths 5.4
- replication (lineage window K = 20 frames = time 10, default): splits 10, persistent splits 4 (0 more failed only because the siblings re-merged within K), max generation 2, merges 39, merge/split ratio 3.9, nucleations 178
- channel total drift (end/start - 1): [0.0, 0.0, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 78 at frame 235: holes 0, rim-vs-core 0.23, rim-vs-outside 0.27, heterogeneity 0.14; core [0.663, 0.556, 0.324] rim [0.505, 0.393, 0.293]
  - track 8 at frame 195: holes 0, rim-vs-core 0.31, rim-vs-outside 0.27, heterogeneity 0.15; core [0.714, 0.465, 0.495] rim [0.492, 0.269, 0.418]
  - track 99 at frame 229: holes 0, rim-vs-core 0.39, rim-vs-outside 0.34, heterogeneity 0.17; core [0.793, 0.399, 0.615] rim [0.431, 0.491, 0.496]
  - track 183 at frame 329: holes 0, rim-vs-core 0.24, rim-vs-outside 0.28, heterogeneity 0.11; core [0.758, 0.311, 0.457] rim [0.528, 0.283, 0.398]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 121 components >= 12 px at frames [67, 134, 202, 266, 333, 400]):
  - radial A density: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.786, rim/outside 14.2 (aggregate of 121 individuals; 3/121 membrane-like individually; rim level 0.628)
  - radial B density: peak at rho=0.45 (OUTSIDE the peak band 0.5-1.5), rim/core 1.01, rim/outside 13 (aggregate of 121 individuals; 40/121 membrane-like individually; rim level 0.438)
  - radial chemicals (sum): peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.811, rim/outside 2.56 (aggregate of 121 individuals; 0/121 membrane-like individually; rim level 0.575)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #78 (t=117.5, R_eq 2.03): none; #8 (t=97.5, R_eq 3.24): none; #99 (t=114.5, R_eq 3.91): ['B density']; #183 (t=164.5, R_eq 2.76): none

## Warnings
- radial: 1 of 121 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, particles.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
