# Evidence pack: kstrail-rd-twin-noh (seed 7)

- world: `../../20261025T0632-c01-kstrail-rd-twin/twin_noh.py`, family `chemotaxis`
- parent: kstrail; mutation: taxis flux replaced by a local mass-conserving reaction (Laplacian-only twin)
- run: 201 frames x 60 steps x dt 0.05 = time 600; grid [192, 192]; wall 67s; status ok
- command: `python -m labkit.run collective/contrib/20261025T0632-c01-kstrail-rd-twin/twin_noh.py --out collective/contrib/20261025T0835-c07-review-c01-twin/rerun_noh --seeds 7 --no-movie`
- segmentation: matter > 0.35 of robust range [0.0, 1.0], min area 6 px

## Measurements
- components: final 1, mean 11.2, max 34; occupancy final 0.05
- tracks: 37; persistent (alive >= 50% of run): 4; longest 187 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 38.10 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [11, 2, 1], H1 [0, 0, 0]
- motion: 0 long-lived tracks moved >= 1 body length; max speed 0/time; max body lengths 0.6
- replication (lineage window K = 20 frames = time 60, default): splits 0, persistent splits 0 (0 more failed only because the siblings re-merged within K), max generation 0, merges 2, merge/split ratio n/a, nucleations 35
- channel total drift (end/start - 1): [0.0, 0.0, 0.0]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 20 at frame 106: holes 0, rim-vs-core 0.49, rim-vs-outside 0.72, heterogeneity 0.17; core [0.994, 0.651, 0.892] rim [0.7, 0.453, 0.558]
  - track 36 at frame 114: holes 0, rim-vs-core 0.49, rim-vs-outside 0.97, heterogeneity 0.18; core [1.0, 0.918, 0.969] rim [0.808, 0.607, 0.638]
  - track 16 at frame 74: holes 0, rim-vs-core 0.48, rim-vs-outside 0.50, heterogeneity 0.15; core [0.954, 0.427, 0.729] rim [0.589, 0.315, 0.442]
  - track 35 at frame 72: holes 0, rim-vs-core 0.29, rim-vs-outside 0.71, heterogeneity 0.15; core [0.951, 0.444, 0.776] rim [0.729, 0.373, 0.601]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 58 components >= 12 px at frames [34, 67, 101, 133, 166, 200]):
  - radial rho: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.827, rim/outside 15.7 (aggregate of 58 individuals; 0/58 membrane-like individually; rim level 0.732)
  - radial a: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.773, rim/outside 3.62 (aggregate of 58 individuals; 0/58 membrane-like individually; rim level 0.316)
  - radial h: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.782, rim/outside 7.19 (aggregate of 58 individuals; 0/58 membrane-like individually; rim level 0.549)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #20 (t=318, R_eq 10.94): none; #36 (t=342, R_eq 19.75): none; #16 (t=222, R_eq 7.11): none; #35 (t=216, R_eq 7.33): none

## Warnings
- none

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
