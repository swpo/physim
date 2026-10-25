# Evidence pack: fl_forager_mut (seed 6)

- world: `../../../../../../threads/flow-lenia/worlds/fl_forager_mut/world.py`, family `flow-lenia`
- parent: flow-lenia/fl_forager_evo; mutation: one founder; rare body-scale mutations of (m,s,h) create new genotypes (ids + parent table carried with matter)
- run: 401 frames x 20 steps x dt 0.2 = time 1600; grid [128, 128]; wall 506s; status ok
- command: `python -m labkit.run threads/flow-lenia/worlds/fl_forager_mut/world.py --out collective/contrib/20261025T2335-c23-review-flfmut/rerun/seed6 --seeds 6 --frames 400 --spf 20 --no-movie`
- segmentation: matter > 0.07 of robust range [0.0, 2.2754], min area 6 px

## Measurements
- components: final 9, mean 9.7, max 14; occupancy final 0.10
- tracks: 498; persistent (alive >= 50% of run): 0; longest 67 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 0.00 (1 = constant size)
- enclosures: components with a hole mean 0.10, final 0; holes at thresholds 0.2/0.35/0.5 final [4, 4, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [20, 12, 9], H1 [11, 5, 0]
- motion: 50 long-lived tracks moved >= 1 body length; max speed 0.947/time; max body lengths 14.1
- replication (lineage window K = 20 frames = time 80, default): splits 172, persistent splits 1 (0 more failed only because the siblings re-merged within K), max generation 1, merges 160, merge/split ratio 0.93, nucleations 6
- channel total drift (end/start - 1): [0.5701, None, None, -0.556]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 228 at frame 262: holes 0, rim-vs-core 0.55, rim-vs-outside 0.07, heterogeneity 0.08; core [0.0, 0.0, 0.617, 0.055] rim [0.0, 0.0, 0.065, 0.04]
  - track 37 at frame 91: holes 0, rim-vs-core 0.43, rim-vs-outside 0.17, heterogeneity 0.10; core [0.592, 0.0, 0.0, 0.164] rim [0.168, 0.0, 0.0, 0.206]
  - track 156 at frame 195: holes 0, rim-vs-core 0.29, rim-vs-outside 0.26, heterogeneity 0.09; core [0.0, 0.0, 0.546, 0.022] rim [0.0, 0.0, 0.256, 0.027]
  - track 364 at frame 350: holes 0, rim-vs-core 0.61, rim-vs-outside 0.06, heterogeneity 0.09; core [0.0, 0.0, 0.674, 0.048] rim [0.0, 0.0, 0.06, 0.038]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 60 components >= 12 px at frames [67, 134, 202, 266, 333, 400]):
  - radial gid%3=0: peak at rho=0.45 (OUTSIDE the peak band 0.5-1.5), rim/core 1.05, rim/outside 13.2 (aggregate of 60 individuals; 15/60 membrane-like individually; rim level 0.204)
  - radial gid%3=1: peak at rho=0.45 (OUTSIDE the peak band 0.5-1.5), rim/core 1.16, rim/outside 9.46 (aggregate of 60 individuals; 9/60 membrane-like individually; rim level 0.149)
  - radial gid%3=2: peak at rho=0.35 (OUTSIDE the peak band 0.5-1.5), rim/core 0.868, rim/outside 10.9 (aggregate of 60 individuals; 8/60 membrane-like individually; rim level 0.218)
  - radial food: peak at rho=2.45 (OUTSIDE the peak band 0.5-1.5), rim/core 1.25, rim/outside 0.848 (aggregate of 60 individuals; 0/60 membrane-like individually; rim level 0.096)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #228 (t=1048, R_eq 4.82): none; #37 (t=364, R_eq 5.47): ['gid%3=0']; #156 (t=780, R_eq 7.96): none; #364 (t=1400, R_eq 5.2): none

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 3 of 60 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
