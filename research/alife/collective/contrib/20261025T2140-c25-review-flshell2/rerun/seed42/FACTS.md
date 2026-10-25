# Evidence pack: fl_shell2 (seed 42)

- world: `../../../20261025T1748-c18-flshell2-metabolic-cell-claim/world.py`, family `flow-lenia`
- parent: flow-lenia/fl_food (rule from motion search screens/mot/C2_r202); mutation: fl_forager plus a set-point shell channel S (r-two56 k4 idea) that feeds back on the matter growth field through a disk kernel (r-two56 k5 idea), h5 0.3
- run: 401 frames x 10 steps x dt 0.2 = time 800; grid [128, 128]; wall 81s; status ok
- command: `python -m labkit.run collective/contrib/20261025T1748-c18-flshell2-metabolic-cell-claim/world.py --out collective/contrib/20261025T2140-c25-review-flshell2/rerun --seeds 41 42 --frames 400 --no-movie`
- segmentation: matter > 0.08 of robust range [0.0, 1.9972], min area 6 px

## Measurements
- components: final 9, mean 7.0, max 17; occupancy final 0.09
- tracks: 176; persistent (alive >= 50% of run): 0; longest 126 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 0.00 (1 = constant size)
- enclosures: components with a hole mean 0.02, final 1; holes at thresholds 0.2/0.35/0.5 final [4, 3, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [21, 18, 12], H1 [5, 4, 0]
- motion: 45 long-lived tracks moved >= 1 body length; max speed 1.04/time; max body lengths 10.4
- replication (lineage window K = 20 frames = time 40, default): splits 63, persistent splits 8 (0 more failed only because the siblings re-merged within K), max generation 6, merges 49, merge/split ratio 0.778, nucleations 3
- channel total drift (end/start - 1): [6.0253, 6.8483, -0.5434, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 13 at frame 212: holes 0, rim-vs-core 0.44, rim-vs-outside 0.05, heterogeneity 0.20; core [0.304, 0.376, 0.135, 0.0] rim [0.027, 0.041, 0.174, 0.0]
  - track 12 at frame 185: holes 0, rim-vs-core 0.40, rim-vs-outside 0.07, heterogeneity 0.18; core [0.254, 0.385, 0.206, 0.0] rim [0.029, 0.058, 0.266, 0.0]
  - track 1 at frame 64: holes 0, rim-vs-core 0.33, rim-vs-outside 0.34, heterogeneity 0.23; core [0.509, 0.308, 0.338, 0.0] rim [0.218, 0.189, 0.445, 0.0]
  - track 144 at frame 380: holes 0, rim-vs-core 0.42, rim-vs-outside 0.06, heterogeneity 0.19; core [0.316, 0.351, 0.028, 0.049] rim [0.048, 0.032, 0.02, 0.0]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 46 components >= 12 px at frames [67, 134, 202, 266, 333, 400]):
  - radial A0: peak at rho=0.55 (in the peak band 0.5-1.5), rim/core 1.31, rim/outside 15.7 (aggregate of 46 individuals; 20/46 membrane-like individually; rim level 0.295)
  - radial A1: peak at rho=0.45 (OUTSIDE the peak band 0.5-1.5), rim/core 1.04, rim/outside 21.6 (aggregate of 46 individuals; 13/46 membrane-like individually; rim level 0.311)
  - radial food: peak at rho=2.35 (OUTSIDE the peak band 0.5-1.5), rim/core 1.93, rim/outside 0.836 (aggregate of 46 individuals; 0/46 membrane-like individually; rim level 0.191)
  - radial S: peak at rho=1.65 (OUTSIDE the peak band 0.5-1.5), rim/core 1.85, rim/outside 0.415 (aggregate of 46 individuals; 3/46 membrane-like individually; rim level 0.122)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #13 (t=424, R_eq 5.56): ['A0', 'A1']; #12 (t=370, R_eq 5.23): ['A0', 'A1']; #1 (t=128, R_eq 8.16): none; #144 (t=760, R_eq 4.58): ['A1']

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 1 of 46 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
