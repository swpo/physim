# Evidence pack: kstrail-rd-twin-global (seed 1)

- world: `../../twin_global.py`, family `chemotaxis`
- parent: kstrail; mutation: taxis flux replaced by a local mass-conserving reaction (Laplacian-only twin)
- run: 201 frames x 60 steps x dt 0.05 = time 600; grid [192, 192]; wall 26s; status ok
- command: `python -m labkit.run collective/contrib/20261025T0632-c01-kstrail-rd-twin/twin_global.py --out collective/contrib/20261025T0632-c01-kstrail-rd-twin/pack_global --seeds 0 1 --no-movie`
- segmentation: matter > 0.35 of robust range [0.0, 1.0], min area 6 px

## Measurements
- components: final 1, mean 1.2, max 7; occupancy final 0.05
- tracks: 9; persistent (alive >= 50% of run): 1; longest 190 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 1.13 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [1, 1, 1], H1 [0, 0, 0]
- motion: 1 long-lived tracks moved >= 1 body length; max speed 0.493/time; max body lengths 6.4
- replication (lineage window K = 20 frames = time 60, default): splits 0, persistent splits 0 (0 more failed only because the siblings re-merged within K), max generation 0, merges 2, merge/split ratio n/a, nucleations 7
- channel total drift (end/start - 1): [-0.0, -0.0, 0.0]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 8 at frame 106: holes 0, rim-vs-core 0.41, rim-vs-outside 0.92, heterogeneity 0.21; core [1.0, 0.894, 0.817] rim [0.861, 0.601, 0.568]
  - track 7 at frame 8: holes 0, rim-vs-core 0.37, rim-vs-outside 0.70, heterogeneity 0.16; core [0.998, 0.622, 0.54] rim [0.726, 0.429, 0.378]
  - track 4 at frame 7: holes 0, rim-vs-core 0.38, rim-vs-outside 0.68, heterogeneity 0.15; core [0.997, 0.575, 0.482] rim [0.719, 0.385, 0.309]
  - track 6 at frame 7: holes 0, rim-vs-core 0.44, rim-vs-outside 0.77, heterogeneity 0.16; core [0.999, 0.617, 0.527] rim [0.778, 0.371, 0.24]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 6 components >= 12 px at frames [34, 67, 101, 133, 166, 200]):
  - radial rho: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.999, rim/outside 101 (aggregate of 6 individuals; 0/6 membrane-like individually; rim level 0.999)
  - radial a: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.855, rim/outside 27.8 (aggregate of 6 individuals; 0/6 membrane-like individually; rim level 0.827)
  - radial h: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.858, rim/outside 28.4 (aggregate of 6 individuals; 0/6 membrane-like individually; rim level 0.752)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #8 (t=318, R_eq 24.68): none; #7 (t=24, R_eq 12.85): none; #4 (t=21, R_eq 13.16): none; #6 (t=21, R_eq 16.64): none

## Warnings
- none

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
