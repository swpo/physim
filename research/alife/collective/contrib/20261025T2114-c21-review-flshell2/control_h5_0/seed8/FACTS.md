# Evidence pack: fl_shell2 (seed 8)

- world: `../../../20261025T1748-c18-flshell2-metabolic-cell-claim/world.py`, family `flow-lenia`
- parent: flow-lenia/fl_food (rule from motion search screens/mot/C2_r202); mutation: fl_forager plus a set-point shell channel S (r-two56 k4 idea) that feeds back on the matter growth field through a disk kernel (r-two56 k5 idea), h5 0.3
- run: 401 frames x 10 steps x dt 0.2 = time 800; grid [128, 128]; wall 71s; status ok
- command: `python -m labkit.run collective/contrib/20261025T1748-c18-flshell2-metabolic-cell-claim/world.py --out collective/contrib/20261025T2114-c21-review-flshell2/control_h5_0 --seeds 7 8 --frames 400 --no-movie`
- segmentation: matter > 0.07 of robust range [0.0, 2.0216], min area 6 px

## Measurements
- components: final 10, mean 6.2, max 10; occupancy final 0.09
- tracks: 80; persistent (alive >= 50% of run): 0; longest 122 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 0.00 (1 = constant size)
- enclosures: components with a hole mean 0.11, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 7, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [20, 12, 10], H1 [13, 6, 0]
- motion: 26 long-lived tracks moved >= 1 body length; max speed 0.631/time; max body lengths 12.4
- replication (lineage window K = 20 frames = time 40, default): splits 29, persistent splits 7 (0 more failed only because the siblings re-merged within K), max generation 4, merges 20, merge/split ratio 0.69, nucleations 0
- channel total drift (end/start - 1): [4.0238, 7.1348, -0.4891, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 44 at frame 339: holes 0, rim-vs-core 0.34, rim-vs-outside 0.22, heterogeneity 0.19; core [0.337, 0.334, 0.025, 0.0] rim [0.017, 0.214, 0.04, 0.0]
  - track 4 at frame 67: holes 0, rim-vs-core 0.35, rim-vs-outside 0.25, heterogeneity 0.23; core [0.348, 0.378, 0.326, 0.0] rim [0.186, 0.098, 0.468, 0.0]
  - track 34 at frame 279: holes 0, rim-vs-core 0.45, rim-vs-outside 0.09, heterogeneity 0.17; core [0.266, 0.421, 0.134, 0.0] rim [0.089, 0.015, 0.17, 0.0]
  - track 6 at frame 67: holes 0, rim-vs-core 0.34, rim-vs-outside 0.30, heterogeneity 0.23; core [0.333, 0.402, 0.279, 0.0] rim [0.224, 0.112, 0.42, 0.0]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 42 components >= 12 px at frames [67, 134, 202, 266, 333, 400]):
  - radial A0: peak at rho=0.35 (OUTSIDE the peak band 0.5-1.5), rim/core 0.52, rim/outside 20.2 (aggregate of 42 individuals; 15/42 membrane-like individually; rim level 0.222)
  - radial A1: peak at rho=0.75 (in the peak band 0.5-1.5), rim/core 3.06, rim/outside 26 (aggregate of 42 individuals; 34/42 membrane-like individually; rim level 0.401)  MEMBRANE-LIKE
  - radial food: peak at rho=2.45 (OUTSIDE the peak band 0.5-1.5), rim/core 2.31, rim/outside 0.781 (aggregate of 42 individuals; 0/42 membrane-like individually; rim level 0.238)
  - radial S: peak at rho=1.55 (OUTSIDE the peak band 0.5-1.5), rim/core 1.06, rim/outside 0.156 (aggregate of 42 individuals; 2/42 membrane-like individually; rim level 0.0374)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): A1
- membrane-like channels per top track at mid-life: #44 (t=678, R_eq 7.84): ['A1']; #4 (t=134, R_eq 7.27): ['A0']; #34 (t=558, R_eq 5.17): ['A0', 'A1']; #6 (t=134, R_eq 6.79): ['A0']

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
