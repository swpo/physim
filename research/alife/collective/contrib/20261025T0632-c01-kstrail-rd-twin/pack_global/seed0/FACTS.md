# Evidence pack: kstrail-rd-twin-global (seed 0)

- world: `../../twin_global.py`, family `chemotaxis`
- parent: kstrail; mutation: taxis flux replaced by a local mass-conserving reaction (Laplacian-only twin)
- run: 201 frames x 60 steps x dt 0.05 = time 600; grid [192, 192]; wall 28s; status ok
- command: `python -m labkit.run collective/contrib/20261025T0632-c01-kstrail-rd-twin/twin_global.py --out collective/contrib/20261025T0632-c01-kstrail-rd-twin/pack_global --seeds 0 1 --no-movie`
- segmentation: matter > 0.35 of robust range [0.0, 1.0], min area 6 px

## Measurements
- components: final 1, mean 1.2, max 10; occupancy final 0.05
- tracks: 10; persistent (alive >= 50% of run): 1; longest 199 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 16.43 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [1, 1, 1], H1 [0, 0, 0]
- motion: 1 long-lived tracks moved >= 1 body length; max speed 0.472/time; max body lengths 6.5
- replication (lineage window K = 20 frames = time 60, default): splits 0, persistent splits 0 (0 more failed only because the siblings re-merged within K), max generation 0, merges 0, merge/split ratio n/a, nucleations 10
- channel total drift (end/start - 1): [0.0, 0.0, -0.0]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 1 at frame 101: holes 0, rim-vs-core 0.40, rim-vs-outside 0.94, heterogeneity 0.21; core [1.0, 0.889, 0.808] rim [0.855, 0.599, 0.57]
  - track 0 at frame 8: holes 0, rim-vs-core 0.44, rim-vs-outside 0.77, heterogeneity 0.16; core [0.999, 0.579, 0.559] rim [0.777, 0.36, 0.252]
  - track 3 at frame 7: holes 0, rim-vs-core 0.45, rim-vs-outside 0.46, heterogeneity 0.14; core [0.964, 0.475, 0.494] rim [0.589, 0.33, 0.285]
  - track 4 at frame 7: holes 0, rim-vs-core 0.36, rim-vs-outside 0.67, heterogeneity 0.14; core [0.995, 0.516, 0.496] rim [0.715, 0.366, 0.336]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 6 components >= 12 px at frames [34, 67, 101, 133, 166, 200]):
  - radial rho: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 1, rim/outside 101 (aggregate of 6 individuals; 0/6 membrane-like individually; rim level 1)
  - radial a: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.858, rim/outside 28.9 (aggregate of 6 individuals; 0/6 membrane-like individually; rim level 0.833)
  - radial h: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.858, rim/outside 28.8 (aggregate of 6 individuals; 0/6 membrane-like individually; rim level 0.757)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #1 (t=303, R_eq 24.77): none; #0 (t=24, R_eq 14.03): none; #3 (t=21, R_eq 9.67): none; #4 (t=21, R_eq 10.12): none

## Warnings
- none

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
