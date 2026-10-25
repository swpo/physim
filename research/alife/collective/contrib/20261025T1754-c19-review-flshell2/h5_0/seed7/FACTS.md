# Evidence pack: fl_shell2 (seed 7)

- world: `../../../20261025T1748-c18-flshell2-metabolic-cell-claim/world.py`, family `flow-lenia`
- parent: flow-lenia/fl_food (rule from motion search screens/mot/C2_r202); mutation: fl_forager plus a set-point shell channel S (r-two56 k4 idea) that feeds back on the matter growth field through a disk kernel (r-two56 k5 idea), h5 0.3
- run: 401 frames x 10 steps x dt 0.2 = time 800; grid [128, 128]; wall 87s; status ok
- command: `python -m labkit.run collective/contrib/20261025T1748-c18-flshell2-metabolic-cell-claim/world.py --out collective/contrib/20261025T1754-c19-review-flshell2/h5_0/seed7 --seeds 7 --frames 400 --no-movie`
- segmentation: matter > 0.07 of robust range [0.0, 2.1011], min area 6 px

## Measurements
- components: final 14, mean 8.0, max 17; occupancy final 0.10
- tracks: 204; persistent (alive >= 50% of run): 0; longest 128 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 0.00 (1 = constant size)
- enclosures: components with a hole mean 0.06, final 1; holes at thresholds 0.2/0.35/0.5 final [3, 1, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [28, 19, 15], H1 [10, 3, 0]
- motion: 46 long-lived tracks moved >= 1 body length; max speed 0.936/time; max body lengths 12.9
- replication (lineage window K = 20 frames = time 40, default): splits 71, persistent splits 9 (0 more failed only because the siblings re-merged within K), max generation 5, merges 60, merge/split ratio 0.845, nucleations 0
- channel total drift (end/start - 1): [4.4199, 7.8047, -0.5314, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 107 at frame 339: holes 0, rim-vs-core 0.42, rim-vs-outside 0.13, heterogeneity 0.18; core [0.306, 0.41, 0.073, 0.0] rim [0.134, 0.027, 0.087, 0.0]
  - track 99 at frame 326: holes 0, rim-vs-core 0.34, rim-vs-outside 0.08, heterogeneity 0.16; core [0.247, 0.337, 0.052, 0.0] rim [0.033, 0.073, 0.053, 0.0]
  - track 1 at frame 81: holes 0, rim-vs-core 0.38, rim-vs-outside 0.27, heterogeneity 0.23; core [0.455, 0.356, 0.425, 0.0] rim [0.224, 0.08, 0.561, 0.0]
  - track 156 at frame 353: holes 0, rim-vs-core 0.61, rim-vs-outside 0.05, heterogeneity 0.28; core [0.376, 0.428, 0.047, 0.322] rim [0.023, 0.044, 0.031, 0.0]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 54 components >= 12 px at frames [67, 134, 202, 266, 333, 400]):
  - radial A0: peak at rho=0.45 (OUTSIDE the peak band 0.5-1.5), rim/core 1.25, rim/outside 17.9 (aggregate of 54 individuals; 28/54 membrane-like individually; rim level 0.302)
  - radial A1: peak at rho=0.55 (in the peak band 0.5-1.5), rim/core 2.01, rim/outside 27 (aggregate of 54 individuals; 41/54 membrane-like individually; rim level 0.375)  MEMBRANE-LIKE
  - radial food: peak at rho=2.45 (OUTSIDE the peak band 0.5-1.5), rim/core 2.11, rim/outside 0.812 (aggregate of 54 individuals; 0/54 membrane-like individually; rim level 0.179)
  - radial S: peak at rho=1.75 (OUTSIDE the peak band 0.5-1.5), rim/core 0.972, rim/outside 0.174 (aggregate of 54 individuals; 2/54 membrane-like individually; rim level 0.0603)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): A1
- membrane-like channels per top track at mid-life: #107 (t=678, R_eq 4.82): none; #99 (t=652, R_eq 5.32): ['A0', 'A1']; #1 (t=162, R_eq 7.29): ['A0']; #156 (t=706, R_eq 4.22): none

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 3 of 54 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
