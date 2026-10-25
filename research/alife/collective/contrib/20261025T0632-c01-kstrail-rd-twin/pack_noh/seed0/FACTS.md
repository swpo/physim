# Evidence pack: kstrail-rd-twin-noh (seed 0)

- world: `../../twin_noh.py`, family `chemotaxis`
- parent: kstrail; mutation: taxis flux replaced by a local mass-conserving reaction (Laplacian-only twin)
- run: 201 frames x 60 steps x dt 0.05 = time 600; grid [192, 192]; wall 42s; status ok
- command: `python -m labkit.run collective/contrib/20261025T0632-c01-kstrail-rd-twin/twin_noh.py --out collective/contrib/20261025T0632-c01-kstrail-rd-twin/pack_noh --seeds 0 1 --no-movie`
- segmentation: matter > 0.35 of robust range [0.0, 1.0], min area 6 px

## Measurements
- components: final 2, mean 9.7, max 32; occupancy final 0.05
- tracks: 34; persistent (alive >= 50% of run): 5; longest 190 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 74.44 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [14, 3, 2], H1 [0, 0, 0]
- motion: 0 long-lived tracks moved >= 1 body length; max speed 0/time; max body lengths 0.6
- replication (lineage window K = 20 frames = time 60, default): splits 0, persistent splits 0 (0 more failed only because the siblings re-merged within K), max generation 0, merges 1, merge/split ratio n/a, nucleations 33
- channel total drift (end/start - 1): [-0.0, -0.0, -0.0]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 15 at frame 106: holes 0, rim-vs-core 0.54, rim-vs-outside 0.75, heterogeneity 0.18; core [0.996, 0.853, 0.931] rim [0.7, 0.575, 0.575]
  - track 24 at frame 104: holes 0, rim-vs-core 0.49, rim-vs-outside 0.73, heterogeneity 0.17; core [0.993, 0.739, 0.914] rim [0.7, 0.522, 0.589]
  - track 32 at frame 111: holes 0, rim-vs-core 0.51, rim-vs-outside 0.88, heterogeneity 0.18; core [0.999, 0.927, 0.958] rim [0.764, 0.632, 0.614]
  - track 9 at frame 82: holes 0, rim-vs-core 0.54, rim-vs-outside 0.53, heterogeneity 0.17; core [0.97, 0.632, 0.848] rim [0.587, 0.448, 0.516]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 50 components >= 12 px at frames [34, 67, 101, 133, 166, 200]):
  - radial rho: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.867, rim/outside 18.9 (aggregate of 50 individuals; 0/50 membrane-like individually; rim level 0.79)
  - radial a: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.775, rim/outside 4.72 (aggregate of 50 individuals; 0/50 membrane-like individually; rim level 0.451)
  - radial h: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.8, rim/outside 9.57 (aggregate of 50 individuals; 0/50 membrane-like individually; rim level 0.631)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #15 (t=318, R_eq 12.75): none; #24 (t=312, R_eq 10.14): none; #32 (t=333, R_eq 14.45): none; #9 (t=246, R_eq 8.85): none

## Warnings
- none

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
