# Evidence pack: fl_shell2 (seed 6)

- world: `../../world.py`, family `flow-lenia`
- parent: flow-lenia/fl_food (rule from motion search screens/mot/C2_r202); mutation: fl_forager plus a set-point shell channel S (r-two56 k4 idea) that feeds back on the matter growth field through a disk kernel (r-two56 k5 idea), h5 0.3
- run: 401 frames x 10 steps x dt 0.2 = time 800; grid [128, 128]; wall 70s; status ok
- command: `python -m labkit.run world.py --out pack --seeds 6 7 --frames 400 --no-movie`
- segmentation: matter > 0.08 of robust range [0.0, 1.9503], min area 6 px

## Measurements
- components: final 13, mean 6.2, max 14; occupancy final 0.09
- tracks: 184; persistent (alive >= 50% of run): 1; longest 257 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 4.52 (1 = constant size)
- enclosures: components with a hole mean 0.02, final 0; holes at thresholds 0.2/0.35/0.5 final [2, 4, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [19, 17, 13], H1 [4, 3, 0]
- motion: 32 long-lived tracks moved >= 1 body length; max speed 0.961/time; max body lengths 17.5
- replication (lineage window K = 20 frames = time 40, default): splits 66, persistent splits 3 (0 more failed only because the siblings re-merged within K), max generation 2, merges 54, merge/split ratio 0.818, nucleations 1
- channel total drift (end/start - 1): [5.6456, 5.9977, -0.5292, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 3 at frame 148: holes 0, rim-vs-core 0.37, rim-vs-outside 0.22, heterogeneity 0.22; core [0.381, 0.371, 0.29, 0.0] rim [0.189, 0.078, 0.394, 0.0]
  - track 4 at frame 101: holes 0, rim-vs-core 0.33, rim-vs-outside 0.26, heterogeneity 0.21; core [0.345, 0.378, 0.276, 0.0] rim [0.219, 0.086, 0.365, 0.0]
  - track 2 at frame 91: holes 0, rim-vs-core 0.34, rim-vs-outside 0.40, heterogeneity 0.23; core [0.31, 0.474, 0.383, 0.0] rim [0.309, 0.137, 0.39, 0.0]
  - track 154 at frame 387: holes 0, rim-vs-core 0.25, rim-vs-outside 0.19, heterogeneity 0.17; core [0.269, 0.35, 0.039, 0.0] rim [0.138, 0.137, 0.052, 0.0]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 40 components >= 12 px at frames [67, 134, 202, 266, 333, 400]):
  - radial A0: peak at rho=0.55 (in the peak band 0.5-1.5), rim/core 1.36, rim/outside 19.3 (aggregate of 40 individuals; 20/40 membrane-like individually; rim level 0.317)
  - radial A1: peak at rho=0.45 (OUTSIDE the peak band 0.5-1.5), rim/core 0.926, rim/outside 20.8 (aggregate of 40 individuals; 10/40 membrane-like individually; rim level 0.302)
  - radial food: peak at rho=2.45 (OUTSIDE the peak band 0.5-1.5), rim/core 1.8, rim/outside 0.815 (aggregate of 40 individuals; 0/40 membrane-like individually; rim level 0.18)
  - radial S: peak at rho=1.75 (OUTSIDE the peak band 0.5-1.5), rim/core 1.35, rim/outside 0.361 (aggregate of 40 individuals; 3/40 membrane-like individually; rim level 0.114)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #3 (t=296, R_eq 8.9): ['A1']; #4 (t=202, R_eq 6.98): ['A0']; #2 (t=182, R_eq 7.05): ['A0']; #154 (t=774, R_eq 5.44): ['A0']

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 1 of 40 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
