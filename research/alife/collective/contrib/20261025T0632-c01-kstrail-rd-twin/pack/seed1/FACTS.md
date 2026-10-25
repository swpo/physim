# Evidence pack: kstrail-rd-twin (seed 1)

- world: `../../twin.py`, family `chemotaxis`
- parent: kstrail; mutation: taxis flux replaced by a local mass-conserving reaction (Laplacian-only twin)
- run: 201 frames x 60 steps x dt 0.05 = time 600; grid [192, 192]; wall 41s; status ok
- command: `python -m labkit.run collective/contrib/20261025T0632-c01-kstrail-rd-twin/twin.py --out collective/contrib/20261025T0632-c01-kstrail-rd-twin/pack --seeds 0 1 2 --no-movie`
- segmentation: matter > 0.35 of robust range [0.0, 0.7645], min area 6 px

## Measurements
- components: final 10, mean 7.1, max 16; occupancy final 0.06
- tracks: 170; persistent (alive >= 50% of run): 0; longest 63 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 0.00 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [15, 10, 5], H1 [0, 0, 0]
- motion: 21 long-lived tracks moved >= 1 body length; max speed 0.891/time; max body lengths 15.4
- replication (lineage window K = 20 frames = time 60, default): splits 40, persistent splits 0 (0 more failed only because the siblings re-merged within K), max generation 0, merges 21, merge/split ratio 0.525, nucleations 70
- channel total drift (end/start - 1): [0.0, -0.0, 0.0]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 46 at frame 138: holes 0, rim-vs-core 0.14, rim-vs-outside 0.12, heterogeneity 0.08; core [0.688, 0.572, 0.406] rim [0.559, 0.524, 0.368]
  - track 61 at frame 138: holes 0, rim-vs-core 0.05, rim-vs-outside 0.09, heterogeneity 0.05; core [0.594, 0.523, 0.409] rim [0.551, 0.503, 0.395]
  - track 57 at frame 131: holes 0, rim-vs-core 0.34, rim-vs-outside 0.31, heterogeneity 0.16; core [0.87, 0.909, 0.81] rim [0.597, 0.756, 0.669]
  - track 88 at frame 153: holes 0, rim-vs-core 0.37, rim-vs-outside 0.42, heterogeneity 0.21; core [0.986, 0.922, 0.679] rim [0.699, 0.748, 0.522]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 49 components >= 12 px at frames [101, 133, 166, 200]):
  - radial rho: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.739, rim/outside 3.45 (aggregate of 49 individuals; 0/49 membrane-like individually; rim level 0.585)
  - radial a: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.859, rim/outside 1.94 (aggregate of 49 individuals; 0/49 membrane-like individually; rim level 0.67)
  - radial h: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.824, rim/outside 1.74 (aggregate of 49 individuals; 0/49 membrane-like individually; rim level 0.558)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #46 (t=414, R_eq 5.35): none; #61 (t=414, R_eq 5.14): none; #57 (t=393, R_eq 8.33): none; #88 (t=459, R_eq 8.18): none

## Warnings
- none

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
