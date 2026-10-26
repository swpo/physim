# Evidence pack: fl_forager_mut (seed 5)

- world: `../../../../../../threads/flow-lenia/worlds/fl_forager_mut/world.py`, family `flow-lenia`
- parent: flow-lenia/fl_forager_evo; mutation: one founder; rare body-scale mutations of (m,s,h) create new genotypes (ids + parent table carried with matter)
- run: 401 frames x 20 steps x dt 0.2 = time 1600; grid [128, 128]; wall 457s; status ok
- command: `python -m labkit.run threads/flow-lenia/worlds/fl_forager_mut/world.py --out collective/contrib/20261025T2335-c23-review-flfmut/rerun/seed5 --seeds 5 --frames 400 --spf 20 --no-movie`
- segmentation: matter > 0.07 of robust range [0.0, 2.194], min area 6 px

## Measurements
- components: final 13, mean 9.5, max 18; occupancy final 0.11
- tracks: 385; persistent (alive >= 50% of run): 0; longest 94 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 0.00 (1 = constant size)
- enclosures: components with a hole mean 0.38, final 1; holes at thresholds 0.2/0.35/0.5 final [1, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [23, 17, 12], H1 [2, 0, 0]
- motion: 36 long-lived tracks moved >= 1 body length; max speed 0.678/time; max body lengths 12.9
- replication (lineage window K = 20 frames = time 80, default): splits 130, persistent splits 3 (0 more failed only because the siblings re-merged within K), max generation 2, merges 119, merge/split ratio 0.915, nucleations 17
- channel total drift (end/start - 1): [1.0666, None, None, -0.5495]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 118 at frame 225: holes 0, rim-vs-core 0.39, rim-vs-outside 0.22, heterogeneity 0.09; core [0.632, 0.0, 0.0, 0.082] rim [0.241, 0.0, 0.0, 0.064]
  - track 65 at frame 134: holes 0, rim-vs-core 0.14, rim-vs-outside 0.27, heterogeneity 0.09; core [0.408, 0.0, 0.0, 0.106] rim [0.27, 0.0, 0.0, 0.097]
  - track 67 at frame 151: holes 0, rim-vs-core 0.35, rim-vs-outside 0.26, heterogeneity 0.10; core [0.595, 0.0, 0.0, 0.127] rim [0.253, 0.0, 0.0, 0.2]
  - track 286 at frame 353: holes 0, rim-vs-core 0.46, rim-vs-outside 0.34, heterogeneity 0.10; core [0.0, 0.0, 0.796, 0.077] rim [0.0, 0.0, 0.336, 0.068]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 62 components >= 12 px at frames [67, 134, 202, 266, 333, 400]):
  - radial gid%3=0: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.801, rim/outside 18.5 (aggregate of 62 individuals; 9/62 membrane-like individually; rim level 0.258)
  - radial gid%3=1: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.927, rim/outside 8.22 (aggregate of 62 individuals; 10/62 membrane-like individually; rim level 0.0909)
  - radial gid%3=2: peak at rho=0.25 (OUTSIDE the peak band 0.5-1.5), rim/core 0.883, rim/outside 13.3 (aggregate of 62 individuals; 9/62 membrane-like individually; rim level 0.178)
  - radial food: peak at rho=2.45 (OUTSIDE the peak band 0.5-1.5), rim/core 1.15, rim/outside 0.815 (aggregate of 62 individuals; 0/62 membrane-like individually; rim level 0.122)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #118 (t=900, R_eq 7.09): none; #65 (t=536, R_eq 7.16): none; #67 (t=604, R_eq 6.84): none; #286 (t=1412, R_eq 7.44): none

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 1 of 62 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
