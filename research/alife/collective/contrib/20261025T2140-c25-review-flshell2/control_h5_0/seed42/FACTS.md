# Evidence pack: fl_shell2 (seed 42)

- world: `../../world_h5_0.py`, family `flow-lenia`
- parent: flow-lenia/fl_food (rule from motion search screens/mot/C2_r202); mutation: fl_forager plus a set-point shell channel S (r-two56 k4 idea) that feeds back on the matter growth field through a disk kernel (r-two56 k5 idea), h5 0.3
- run: 401 frames x 10 steps x dt 0.2 = time 800; grid [128, 128]; wall 77s; status ok
- command: `python -m labkit.run collective/contrib/20261025T2140-c25-review-flshell2/world_h5_0.py --out collective/contrib/20261025T2140-c25-review-flshell2/control_h5_0 --seeds 41 42 --frames 400 --no-movie`
- segmentation: matter > 0.08 of robust range [0.0, 1.9662], min area 6 px

## Measurements
- components: final 8, mean 5.8, max 11; occupancy final 0.09
- tracks: 67; persistent (alive >= 50% of run): 2; longest 272 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 2.32 (1 = constant size)
- enclosures: components with a hole mean 0.01, final 1; holes at thresholds 0.2/0.35/0.5 final [2, 2, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [21, 10, 9], H1 [10, 4, 1]
- motion: 25 long-lived tracks moved >= 1 body length; max speed 0.682/time; max body lengths 9.4
- replication (lineage window K = 20 frames = time 40, default): splits 23, persistent splits 6 (0 more failed only because the siblings re-merged within K), max generation 5, merges 18, merge/split ratio 0.783, nucleations 0
- channel total drift (end/start - 1): [3.6682, 8.292, -0.5015, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 10 at frame 259: holes 0, rim-vs-core 0.17, rim-vs-outside 0.29, heterogeneity 0.18; core [0.207, 0.391, 0.016, 0.0] rim [0.15, 0.237, 0.043, 0.0]
  - track 11 at frame 229: holes 0, rim-vs-core 0.32, rim-vs-outside 0.26, heterogeneity 0.20; core [0.333, 0.366, 0.058, 0.0] rim [0.051, 0.234, 0.138, 0.0]
  - track 38 at frame 339: holes 0, rim-vs-core 0.46, rim-vs-outside 0.06, heterogeneity 0.17; core [0.307, 0.407, 0.043, 0.0] rim [0.058, 0.024, 0.054, 0.0]
  - track 63 at frame 387: holes 0, rim-vs-core 0.41, rim-vs-outside 0.06, heterogeneity 0.18; core [0.294, 0.369, 0.05, 0.0] rim [0.029, 0.057, 0.064, 0.0]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 35 components >= 12 px at frames [67, 134, 202, 266, 333, 400]):
  - radial A0: peak at rho=0.35 (OUTSIDE the peak band 0.5-1.5), rim/core 0.678, rim/outside 23 (aggregate of 35 individuals; 14/35 membrane-like individually; rim level 0.233)
  - radial A1: peak at rho=0.75 (in the peak band 0.5-1.5), rim/core 2.66, rim/outside 32.4 (aggregate of 35 individuals; 28/35 membrane-like individually; rim level 0.384)  MEMBRANE-LIKE
  - radial food: peak at rho=2.45 (OUTSIDE the peak band 0.5-1.5), rim/core 2.51, rim/outside 0.769 (aggregate of 35 individuals; 0/35 membrane-like individually; rim level 0.238)
  - radial S: peak at rho=1.65 (OUTSIDE the peak band 0.5-1.5), rim/core 1.75, rim/outside 0.268 (aggregate of 35 individuals; 3/35 membrane-like individually; rim level 0.0702)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): A1
- membrane-like channels per top track at mid-life: #10 (t=518, R_eq 9.66): ['A1']; #11 (t=458, R_eq 7.31): ['A1']; #38 (t=678, R_eq 4.95): ['A0', 'A1']; #63 (t=774, R_eq 5.56): ['A0', 'A1']

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 1 of 35 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
