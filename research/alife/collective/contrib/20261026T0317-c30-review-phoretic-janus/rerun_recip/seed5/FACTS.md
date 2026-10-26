# Evidence pack: phoretic-colloids (seed 5)

- world: `../../../20261026T0254-c33-phoretic-janus-claim/world.py`, family `phoretic-colloids`
- parent: None; mutation: -
- run: 401 frames x 1 steps x dt 0.5 = time 200; grid [128, 128]; wall 56s; status ok
- command: `python -m labkit.run collective/contrib/20261026T0254-c33-phoretic-janus-claim/world.py --out collective/contrib/20261026T0317-c30-review-phoretic-janus/rerun_recip --seeds 4 5 --frames 400 --no-movie`
- segmentation: matter > 0.35 of robust range [0.0, 1.8972], min area 6 px

## Measurements
- components: final 17, mean 25.5, max 39; occupancy final 0.07
- tracks: 155; persistent (alive >= 50% of run): 19; longest 374 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 9.67 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [17, 16, 12], H1 [0, 0, 0]
- motion: 19 long-lived tracks moved >= 1 body length; max speed 0.135/time; max body lengths 3.2
- replication (lineage window K = 20 frames = time 10, default): splits 0, persistent splits 0 (0 more failed only because the siblings re-merged within K), max generation 0, merges 30, merge/split ratio n/a, nucleations 125
- channel total drift (end/start - 1): [0.0, 0.0, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 13 at frame 215: holes 0, rim-vs-core 0.33, rim-vs-outside 0.30, heterogeneity 0.13; core [0.832, 0.341, 0.551] rim [0.549, 0.476, 0.46]
  - track 35 at frame 222: holes 0, rim-vs-core 0.33, rim-vs-outside 0.36, heterogeneity 0.17; core [0.801, 0.699, 0.736] rim [0.542, 0.563, 0.593]
  - track 93 at frame 235: holes 0, rim-vs-core 0.13, rim-vs-outside 0.30, heterogeneity 0.10; core [0.582, 0.689, 0.414] rim [0.506, 0.593, 0.366]
  - track 21 at frame 198: holes 0, rim-vs-core 0.25, rim-vs-outside 0.35, heterogeneity 0.12; core [0.658, 0.791, 0.47] rim [0.459, 0.657, 0.405]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 134 components >= 12 px at frames [67, 134, 202, 266, 333, 400]):
  - radial A density: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.826, rim/outside 18.8 (aggregate of 134 individuals; 0/134 membrane-like individually; rim level 0.703)
  - radial B density: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.932, rim/outside 15.4 (aggregate of 134 individuals; 28/134 membrane-like individually; rim level 0.566)
  - radial chemicals (sum): peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.833, rim/outside 2.69 (aggregate of 134 individuals; 0/134 membrane-like individually; rim level 0.607)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #13 (t=107.5, R_eq 3.24): ['B density']; #35 (t=111, R_eq 4.07): none; #93 (t=117.5, R_eq 2.39): none; #21 (t=99, R_eq 2.76): none

## Warnings
- none

## Files
sheet.png, particles.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
