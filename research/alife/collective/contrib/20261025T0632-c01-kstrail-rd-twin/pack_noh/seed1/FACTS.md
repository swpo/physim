# Evidence pack: kstrail-rd-twin-noh (seed 1)

- world: `../../twin_noh.py`, family `chemotaxis`
- parent: kstrail; mutation: taxis flux replaced by a local mass-conserving reaction (Laplacian-only twin)
- run: 201 frames x 60 steps x dt 0.05 = time 600; grid [192, 192]; wall 50s; status ok
- command: `python -m labkit.run collective/contrib/20261025T0632-c01-kstrail-rd-twin/twin_noh.py --out collective/contrib/20261025T0632-c01-kstrail-rd-twin/pack_noh --seeds 0 1 --no-movie`
- segmentation: matter > 0.35 of robust range [0.0, 1.0], min area 6 px

## Measurements
- components: final 1, mean 9.2, max 35; occupancy final 0.05
- tracks: 38; persistent (alive >= 50% of run): 2; longest 162 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 34.70 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [1, 1, 1], H1 [0, 0, 0]
- motion: 1 long-lived tracks moved >= 1 body length; max speed 0.0358/time; max body lengths 1.2
- replication (lineage window K = 20 frames = time 60, default): splits 0, persistent splits 0 (0 more failed only because the siblings re-merged within K), max generation 0, merges 2, merge/split ratio n/a, nucleations 36
- channel total drift (end/start - 1): [0.0, -0.0, 0.0]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 37 at frame 119: holes 0, rim-vs-core 0.45, rim-vs-outside 1.01, heterogeneity 0.17; core [1.0, 0.925, 0.979] rim [0.83, 0.626, 0.69]
  - track 20 at frame 86: holes 0, rim-vs-core 0.48, rim-vs-outside 0.72, heterogeneity 0.17; core [0.994, 0.614, 0.889] rim [0.691, 0.428, 0.56]
  - track 10 at frame 57: holes 0, rim-vs-core 0.46, rim-vs-outside 0.49, heterogeneity 0.14; core [0.945, 0.388, 0.734] rim [0.581, 0.292, 0.465]
  - track 7 at frame 55: holes 0, rim-vs-core 0.47, rim-vs-outside 0.49, heterogeneity 0.14; core [0.948, 0.396, 0.741] rim [0.584, 0.296, 0.467]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 48 components >= 12 px at frames [34, 67, 101, 133, 166, 200]):
  - radial rho: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.827, rim/outside 15.4 (aggregate of 48 individuals; 0/48 membrane-like individually; rim level 0.72)
  - radial a: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.776, rim/outside 3.71 (aggregate of 48 individuals; 0/48 membrane-like individually; rim level 0.308)
  - radial h: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.788, rim/outside 7.14 (aggregate of 48 individuals; 0/48 membrane-like individually; rim level 0.54)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #37 (t=357, R_eq 21.48): none; #20 (t=258, R_eq 10.51): none; #10 (t=171, R_eq 6.6): none; #7 (t=165, R_eq 6.75): none

## Warnings
- none

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
