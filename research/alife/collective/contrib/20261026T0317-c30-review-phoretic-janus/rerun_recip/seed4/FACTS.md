# Evidence pack: phoretic-colloids (seed 4)

- world: `../../../20261026T0254-c33-phoretic-janus-claim/world.py`, family `phoretic-colloids`
- parent: None; mutation: -
- run: 401 frames x 1 steps x dt 0.5 = time 200; grid [128, 128]; wall 58s; status ok
- command: `python -m labkit.run collective/contrib/20261026T0254-c33-phoretic-janus-claim/world.py --out collective/contrib/20261026T0317-c30-review-phoretic-janus/rerun_recip --seeds 4 5 --frames 400 --no-movie`
- segmentation: matter > 0.35 of robust range [0.0, 1.9822], min area 6 px

## Measurements
- components: final 20, mean 22.5, max 37; occupancy final 0.07
- tracks: 153; persistent (alive >= 50% of run): 18; longest 371 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 9.67 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [22, 22, 18], H1 [0, 0, 0]
- motion: 17 long-lived tracks moved >= 1 body length; max speed 0.246/time; max body lengths 2.5
- replication (lineage window K = 20 frames = time 10, default): splits 0, persistent splits 0 (0 more failed only because the siblings re-merged within K), max generation 0, merges 22, merge/split ratio n/a, nucleations 131
- channel total drift (end/start - 1): [0.0, 0.0, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 7 at frame 215: holes 0, rim-vs-core 0.24, rim-vs-outside 0.33, heterogeneity 0.15; core [0.73, 0.703, 0.584] rim [0.572, 0.543, 0.496]
  - track 13 at frame 218: holes 0, rim-vs-core 0.23, rim-vs-outside 0.32, heterogeneity 0.17; core [0.741, 0.548, 0.603] rim [0.539, 0.529, 0.5]
  - track 28 at frame 225: holes 0, rim-vs-core 0.37, rim-vs-outside 0.38, heterogeneity 0.15; core [0.833, 0.661, 0.796] rim [0.589, 0.449, 0.619]
  - track 39 at frame 229: holes 0, rim-vs-core 0.17, rim-vs-outside 0.26, heterogeneity 0.09; core [0.799, 0.334, 0.521] rim [0.646, 0.302, 0.45]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 126 components >= 12 px at frames [67, 134, 202, 266, 333, 400]):
  - radial A density: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.863, rim/outside 18.6 (aggregate of 126 individuals; 0/126 membrane-like individually; rim level 0.747)
  - radial B density: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.86, rim/outside 16.1 (aggregate of 126 individuals; 14/126 membrane-like individually; rim level 0.574)
  - radial chemicals (sum): peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.852, rim/outside 2.82 (aggregate of 126 individuals; 0/126 membrane-like individually; rim level 0.65)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #7 (t=107.5, R_eq 3.19): none; #13 (t=109, R_eq 3.39): ['B density']; #28 (t=112.5, R_eq 4.44): none; #39 (t=114.5, R_eq 2.82): ['B density']

## Warnings
- none

## Files
sheet.png, particles.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
