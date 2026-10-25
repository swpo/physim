# Evidence pack: fl_shell2 (seed 9)

- world: `../../world.py`, family `flow-lenia`
- parent: flow-lenia/fl_food (rule from motion search screens/mot/C2_r202); mutation: fl_forager plus a set-point shell channel S (r-two56 k4 idea) that feeds back on the matter growth field through a disk kernel (r-two56 k5 idea), h5 0.3
- run: 401 frames x 10 steps x dt 0.2 = time 800; grid [128, 128]; wall 135s; status ok
- command: `python -m labkit.run /tmp/c20f2/world.py --out /tmp/c20f2/pack --seeds 8 9 --frames 400 --no-movie`
- segmentation: matter > 0.07 of robust range [0.0, 2.0407], min area 6 px

## Measurements
- components: final 13, mean 8.0, max 16; occupancy final 0.09
- tracks: 218; persistent (alive >= 50% of run): 0; longest 146 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 0.00 (1 = constant size)
- enclosures: components with a hole mean 0.02, final 0; holes at thresholds 0.2/0.35/0.5 final [3, 3, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [23, 20, 13], H1 [8, 5, 1]
- motion: 41 long-lived tracks moved >= 1 body length; max speed 1.01/time; max body lengths 14.0
- replication (lineage window K = 20 frames = time 40, default): splits 78, persistent splits 4 (0 more failed only because the siblings re-merged within K), max generation 4, merges 64, merge/split ratio 0.821, nucleations 0
- channel total drift (end/start - 1): [5.4558, 6.3888, -0.5375, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 5 at frame 161: holes 0, rim-vs-core 0.45, rim-vs-outside 0.08, heterogeneity 0.20; core [0.285, 0.397, 0.252, 0.0] rim [0.025, 0.044, 0.346, 0.0]
  - track 3 at frame 74: holes 0, rim-vs-core 0.34, rim-vs-outside 0.26, heterogeneity 0.21; core [0.404, 0.327, 0.26, 0.0] rim [0.174, 0.119, 0.387, 0.0]
  - track 25 at frame 225: holes 0, rim-vs-core 0.45, rim-vs-outside 0.04, heterogeneity 0.19; core [0.283, 0.377, 0.156, 0.0] rim [0.032, 0.012, 0.202, 0.0]
  - track 87 at frame 319: holes 0, rim-vs-core 0.46, rim-vs-outside 0.04, heterogeneity 0.18; core [0.322, 0.378, 0.063, 0.0] rim [0.031, 0.022, 0.074, 0.0]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 57 components >= 12 px at frames [67, 134, 202, 266, 333, 400]):
  - radial A0: peak at rho=0.55 (in the peak band 0.5-1.5), rim/core 1.62, rim/outside 24.6 (aggregate of 57 individuals; 30/57 membrane-like individually; rim level 0.345)  MEMBRANE-LIKE
  - radial A1: peak at rho=0.55 (in the peak band 0.5-1.5), rim/core 1.08, rim/outside 27.5 (aggregate of 57 individuals; 23/57 membrane-like individually; rim level 0.337)
  - radial food: peak at rho=2.45 (OUTSIDE the peak band 0.5-1.5), rim/core 1.73, rim/outside 0.831 (aggregate of 57 individuals; 0/57 membrane-like individually; rim level 0.176)
  - radial S: peak at rho=1.75 (OUTSIDE the peak band 0.5-1.5), rim/core 0.918, rim/outside 0.224 (aggregate of 57 individuals; 0/57 membrane-like individually; rim level 0.073)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): A0
- membrane-like channels per top track at mid-life: #5 (t=322, R_eq 5.61): ['A1']; #3 (t=148, R_eq 6.43): ['A0']; #25 (t=450, R_eq 5.59): ['A0', 'A1']; #87 (t=638, R_eq 4.98): ['A1']

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 2 of 57 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
