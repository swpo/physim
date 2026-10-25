# Evidence pack: swimfission-rd-twin (seed 0)

- world: `../../twin_sf.py`, family `chemotaxis`
- parent: toxforage; mutation: shorter cohesion range (Da 4 -> 2): grown swimmers exceed it and divide
- run: 201 frames x 120 steps x dt 0.05 = time 1200; grid [160, 160]; wall 57s; status ok
- command: `python -m labkit.run collective/contrib/20261025T0658-c01-swimfission-rd-twin/twin_sf.py --out collective/contrib/20261025T0658-c01-swimfission-rd-twin/pack --seeds 0 1 --no-movie`
- segmentation: matter > 0.35 of robust range [0.0, 0.9998], min area 6 px

## Measurements
- components: final 9, mean 6.5, max 23; occupancy final 0.06
- tracks: 150; persistent (alive >= 50% of run): 0; longest 71 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 0.00 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [11, 10, 8], H1 [0, 0, 0]
- motion: 13 long-lived tracks moved >= 1 body length; max speed 0.643/time; max body lengths 17.0
- replication (lineage window K = 20 frames = time 120, default): splits 15, persistent splits 0 (0 more failed only because the siblings re-merged within K), max generation 0, merges 11, merge/split ratio 0.733, nucleations 109
- channel total drift (end/start - 1): [0.1735, 0.0592, -0.0182, -0.059]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 103 at frame 119: holes 0, rim-vs-core 0.48, rim-vs-outside 0.72, heterogeneity 0.25; core [0.992, 0.862, 0.689, 0.075] rim [0.675, 0.621, 0.539, 0.307]
  - track 106 at frame 121: holes 0, rim-vs-core 0.35, rim-vs-outside 0.87, heterogeneity 0.24; core [0.994, 0.865, 0.674, 0.059] rim [0.755, 0.699, 0.612, 0.247]
  - track 125 at frame 176: holes 0, rim-vs-core 0.39, rim-vs-outside 0.82, heterogeneity 0.24; core [0.991, 0.86, 0.69, 0.071] rim [0.744, 0.671, 0.557, 0.26]
  - track 107 at frame 114: holes 0, rim-vs-core 0.39, rim-vs-outside 0.84, heterogeneity 0.24; core [0.993, 0.837, 0.646, 0.072] rim [0.738, 0.652, 0.554, 0.283]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 40 components >= 12 px at frames [34, 67, 101, 133, 166, 200]):
  - radial rho: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.699, rim/outside 12.7 (aggregate of 40 individuals; 0/40 membrane-like individually; rim level 0.626)
  - radial a: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.75, rim/outside 3.95 (aggregate of 40 individuals; 0/40 membrane-like individually; rim level 0.454)
  - radial h: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.797, rim/outside 3.38 (aggregate of 40 individuals; 0/40 membrane-like individually; rim level 0.373)
  - radial n: peak at rho=2.45 (OUTSIDE the peak band 0.5-1.5), rim/core 1.56, rim/outside 0.884 (aggregate of 40 individuals; 0/40 membrane-like individually; rim level 0.837)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #103 (t=714, R_eq 11.98): none; #106 (t=726, R_eq 12.85): none; #125 (t=1056, R_eq 13.77): none; #107 (t=684, R_eq 12.4): none

## Warnings
- none

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
