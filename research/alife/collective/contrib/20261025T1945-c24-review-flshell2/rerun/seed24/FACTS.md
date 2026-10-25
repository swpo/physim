# Evidence pack: fl_shell2 (seed 24)

- world: `../../../20261025T1748-c18-flshell2-metabolic-cell-claim/world.py`, family `flow-lenia`
- parent: flow-lenia/fl_food (rule from motion search screens/mot/C2_r202); mutation: fl_forager plus a set-point shell channel S (r-two56 k4 idea) that feeds back on the matter growth field through a disk kernel (r-two56 k5 idea), h5 0.3
- run: 401 frames x 10 steps x dt 0.2 = time 800; grid [128, 128]; wall 149s; status ok
- command: `python -m labkit.run collective/contrib/20261025T1748-c18-flshell2-metabolic-cell-claim/world.py --out collective/contrib/20261025T1945-c24-review-flshell2/rerun/seed24 --seeds 24 --frames 400 --no-movie`
- segmentation: matter > 0.07 of robust range [0.0, 2.0825], min area 6 px

## Measurements
- components: final 16, mean 8.8, max 17; occupancy final 0.10
- tracks: 182; persistent (alive >= 50% of run): 0; longest 161 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 0.00 (1 = constant size)
- enclosures: components with a hole mean 0.01, final 0; holes at thresholds 0.2/0.35/0.5 final [2, 3, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [30, 20, 15], H1 [6, 1, 0]
- motion: 57 long-lived tracks moved >= 1 body length; max speed 0.87/time; max body lengths 12.2
- replication (lineage window K = 20 frames = time 40, default): splits 64, persistent splits 12 (0 more failed only because the siblings re-merged within K), max generation 6, merges 51, merge/split ratio 0.797, nucleations 3
- channel total drift (end/start - 1): [5.5621, 6.7699, -0.5423, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 3 at frame 91: holes 0, rim-vs-core 0.23, rim-vs-outside 0.40, heterogeneity 0.23; core [0.452, 0.319, 0.316, 0.0] rim [0.248, 0.234, 0.379, 0.0]
  - track 4 at frame 71: holes 0, rim-vs-core 0.33, rim-vs-outside 0.26, heterogeneity 0.22; core [0.37, 0.345, 0.329, 0.0] rim [0.199, 0.097, 0.47, 0.0]
  - track 7 at frame 165: holes 0, rim-vs-core 0.45, rim-vs-outside 0.08, heterogeneity 0.18; core [0.316, 0.398, 0.21, 0.0] rim [0.023, 0.062, 0.273, 0.0]
  - track 126 at frame 366: holes 0, rim-vs-core 0.44, rim-vs-outside 0.05, heterogeneity 0.18; core [0.305, 0.375, 0.074, 0.0] rim [0.028, 0.039, 0.095, 0.0]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 61 components >= 12 px at frames [67, 134, 202, 266, 333, 400]):
  - radial A0: peak at rho=0.55 (in the peak band 0.5-1.5), rim/core 1.36, rim/outside 22.9 (aggregate of 61 individuals; 33/61 membrane-like individually; rim level 0.305)
  - radial A1: peak at rho=0.45 (OUTSIDE the peak band 0.5-1.5), rim/core 1.08, rim/outside 27.2 (aggregate of 61 individuals; 17/61 membrane-like individually; rim level 0.346)
  - radial food: peak at rho=2.45 (OUTSIDE the peak band 0.5-1.5), rim/core 1.89, rim/outside 0.819 (aggregate of 61 individuals; 1/61 membrane-like individually; rim level 0.166)
  - radial S: peak at rho=1.75 (OUTSIDE the peak band 0.5-1.5), rim/core 0.538, rim/outside 0.202 (aggregate of 61 individuals; 1/61 membrane-like individually; rim level 0.0749)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #3 (t=182, R_eq 7.42): ['A0']; #4 (t=142, R_eq 6.63): ['A0']; #7 (t=330, R_eq 4.98): ['A0']; #126 (t=732, R_eq 5.23): ['A0']

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
