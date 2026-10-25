# Evidence pack: fl_shell2 (seed 41)

- world: `../../world_h5_0.py`, family `flow-lenia`
- parent: flow-lenia/fl_food (rule from motion search screens/mot/C2_r202); mutation: fl_forager plus a set-point shell channel S (r-two56 k4 idea) that feeds back on the matter growth field through a disk kernel (r-two56 k5 idea), h5 0.3
- run: 401 frames x 10 steps x dt 0.2 = time 800; grid [128, 128]; wall 93s; status ok
- command: `python -m labkit.run collective/contrib/20261025T2140-c25-review-flshell2/world_h5_0.py --out collective/contrib/20261025T2140-c25-review-flshell2/control_h5_0 --seeds 41 42 --frames 400 --no-movie`
- segmentation: matter > 0.07 of robust range [0.0, 2.0963], min area 6 px

## Measurements
- components: final 15, mean 7.2, max 16; occupancy final 0.10
- tracks: 154; persistent (alive >= 50% of run): 0; longest 158 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 0.00 (1 = constant size)
- enclosures: components with a hole mean 0.02, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 3, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [30, 22, 15], H1 [8, 1, 0]
- motion: 36 long-lived tracks moved >= 1 body length; max speed 0.866/time; max body lengths 10.0
- replication (lineage window K = 20 frames = time 40, default): splits 57, persistent splits 8 (0 more failed only because the siblings re-merged within K), max generation 4, merges 44, merge/split ratio 0.772, nucleations 0
- channel total drift (end/start - 1): [4.0074, 8.0619, -0.5354, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 37 at frame 292: holes 0, rim-vs-core 0.30, rim-vs-outside 0.28, heterogeneity 0.19; core [0.345, 0.352, 0.035, 0.0] rim [0.058, 0.268, 0.053, 0.0]
  - track 2 at frame 81: holes 0, rim-vs-core 0.31, rim-vs-outside 0.34, heterogeneity 0.23; core [0.348, 0.395, 0.359, 0.0] rim [0.274, 0.111, 0.462, 0.0]
  - track 1 at frame 74: holes 0, rim-vs-core 0.36, rim-vs-outside 0.24, heterogeneity 0.23; core [0.386, 0.347, 0.354, 0.0] rim [0.157, 0.125, 0.517, 0.0]
  - track 121 at frame 376: holes 0, rim-vs-core 0.34, rim-vs-outside 0.27, heterogeneity 0.22; core [0.205, 0.472, 0.036, 0.049] rim [0.225, 0.13, 0.028, 0.08]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 53 components >= 12 px at frames [67, 134, 202, 266, 333, 400]):
  - radial A0: peak at rho=0.45 (OUTSIDE the peak band 0.5-1.5), rim/core 0.931, rim/outside 19.4 (aggregate of 53 individuals; 25/53 membrane-like individually; rim level 0.274)
  - radial A1: peak at rho=0.55 (in the peak band 0.5-1.5), rim/core 2.12, rim/outside 26.8 (aggregate of 53 individuals; 38/53 membrane-like individually; rim level 0.357)  MEMBRANE-LIKE
  - radial food: peak at rho=2.45 (OUTSIDE the peak band 0.5-1.5), rim/core 2, rim/outside 0.824 (aggregate of 53 individuals; 0/53 membrane-like individually; rim level 0.167)
  - radial S: peak at rho=1.75 (OUTSIDE the peak band 0.5-1.5), rim/core 1.03, rim/outside 0.171 (aggregate of 53 individuals; 3/53 membrane-like individually; rim level 0.0564)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): A1
- membrane-like channels per top track at mid-life: #37 (t=584, R_eq 7.82): ['A1']; #2 (t=162, R_eq 7.18): ['A0']; #1 (t=148, R_eq 8.81): ['A1']; #121 (t=752, R_eq 4.48): none

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 2 of 53 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
