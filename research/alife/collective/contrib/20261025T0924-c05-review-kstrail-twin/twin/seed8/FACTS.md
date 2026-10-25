# Evidence pack: kstrail-rd-twin (seed 8)

- world: `../../../../contrib/20261025T0632-c01-kstrail-rd-twin/twin.py`, family `chemotaxis`
- parent: kstrail; mutation: taxis flux replaced by a local mass-conserving reaction (Laplacian-only twin)
- run: 201 frames x 60 steps x dt 0.05 = time 600; grid [192, 192]; wall 124s; status ok
- command: `python -m labkit.run collective/contrib/20261025T0632-c01-kstrail-rd-twin/twin.py --out collective/work_c05/rev_kt/twin/seed8 --seeds 8 --no-movie`
- segmentation: matter > 0.35 of robust range [0.0, 0.8567], min area 6 px

## Measurements
- components: final 9, mean 6.1, max 19; occupancy final 0.05
- tracks: 112; persistent (alive >= 50% of run): 0; longest 61 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 0.00 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [11, 8, 8], H1 [0, 0, 0]
- motion: 19 long-lived tracks moved >= 1 body length; max speed 0.865/time; max body lengths 12.3
- replication (lineage window K = 20 frames = time 60, default): splits 22, persistent splits 1 (0 more failed only because the siblings re-merged within K), max generation 1, merges 16, merge/split ratio 0.727, nucleations 53
- channel total drift (end/start - 1): [0.0, 0.0, 0.0]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 28 at frame 133: holes 0, rim-vs-core 0.17, rim-vs-outside 0.12, heterogeneity 0.10; core [0.707, 0.609, 0.466] rim [0.545, 0.556, 0.433]
  - track 32 at frame 133: holes 0, rim-vs-core 0.22, rim-vs-outside 0.30, heterogeneity 0.12; core [0.814, 0.655, 0.484] rim [0.615, 0.583, 0.436]
  - track 80 at frame 171: holes 0, rim-vs-core 0.35, rim-vs-outside 0.42, heterogeneity 0.21; core [0.973, 0.885, 0.627] rim [0.676, 0.73, 0.523]
  - track 95 at frame 183: holes 0, rim-vs-core 0.18, rim-vs-outside 0.29, heterogeneity 0.11; core [0.792, 0.616, 0.435] rim [0.625, 0.556, 0.396]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 45 components >= 12 px at frames [101, 133, 166, 200]):
  - radial rho: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.708, rim/outside 3.74 (aggregate of 45 individuals; 0/45 membrane-like individually; rim level 0.57)
  - radial a: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.853, rim/outside 1.91 (aggregate of 45 individuals; 0/45 membrane-like individually; rim level 0.624)
  - radial h: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.815, rim/outside 1.64 (aggregate of 45 individuals; 0/45 membrane-like individually; rim level 0.492)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #28 (t=399, R_eq 5.14): none; #32 (t=399, R_eq 7.07): none; #80 (t=513, R_eq 8.85): none; #95 (t=549, R_eq 6.48): none

## Warnings
- none

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
