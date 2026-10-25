# Evidence pack: fl_shell2 (seed 12)

- world: `../../world.py`, family `flow-lenia`
- parent: flow-lenia/fl_food (rule from motion search screens/mot/C2_r202); mutation: fl_forager plus a set-point shell channel S (r-two56 k4 idea) that feeds back on the matter growth field through a disk kernel (r-two56 k5 idea), h5 0.3
- run: 401 frames x 10 steps x dt 0.2 = time 800; grid [128, 128]; wall 55s; status ok
- command: `python -m labkit.run collective/contrib/wip-c27d/world.py --out collective/contrib/wip-c27d/rerun --seeds 11 12 --frames 400 --no-movie`
- segmentation: matter > 0.07 of robust range [0.0, 2.1077], min area 6 px

## Measurements
- components: final 13, mean 9.8, max 18; occupancy final 0.10
- tracks: 211; persistent (alive >= 50% of run): 0; longest 181 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 0.00 (1 = constant size)
- enclosures: components with a hole mean 0.01, final 0; holes at thresholds 0.2/0.35/0.5 final [3, 7, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [30, 20, 15], H1 [12, 4, 1]
- motion: 56 long-lived tracks moved >= 1 body length; max speed 0.887/time; max body lengths 13.0
- replication (lineage window K = 20 frames = time 40, default): splits 72, persistent splits 8 (0 more failed only because the siblings re-merged within K), max generation 4, merges 62, merge/split ratio 0.861, nucleations 3
- channel total drift (end/start - 1): [5.2531, 6.854, -0.5459, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 54 at frame 313: holes 0, rim-vs-core 0.46, rim-vs-outside 0.05, heterogeneity 0.18; core [0.291, 0.397, 0.078, 0.0] rim [0.045, 0.013, 0.08, 0.0]
  - track 17 at frame 198: holes 0, rim-vs-core 0.34, rim-vs-outside 0.25, heterogeneity 0.20; core [0.358, 0.302, 0.204, 0.0] rim [0.034, 0.241, 0.292, 0.0]
  - track 14 at frame 151: holes 0, rim-vs-core 0.25, rim-vs-outside 0.23, heterogeneity 0.18; core [0.259, 0.337, 0.229, 0.0] rim [0.06, 0.208, 0.304, 0.0]
  - track 194 at frame 387: holes 0, rim-vs-core 0.44, rim-vs-outside 0.05, heterogeneity 0.18; core [0.325, 0.365, 0.029, 0.0] rim [0.048, 0.016, 0.02, 0.0]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 68 components >= 12 px at frames [67, 134, 202, 266, 333, 400]):
  - radial A0: peak at rho=0.55 (in the peak band 0.5-1.5), rim/core 1.48, rim/outside 25.1 (aggregate of 68 individuals; 32/68 membrane-like individually; rim level 0.323)
  - radial A1: peak at rho=0.45 (OUTSIDE the peak band 0.5-1.5), rim/core 1.24, rim/outside 27.2 (aggregate of 68 individuals; 31/68 membrane-like individually; rim level 0.34)
  - radial food: peak at rho=2.35 (OUTSIDE the peak band 0.5-1.5), rim/core 1.71, rim/outside 0.838 (aggregate of 68 individuals; 0/68 membrane-like individually; rim level 0.196)
  - radial S: peak at rho=1.75 (OUTSIDE the peak band 0.5-1.5), rim/core 0.756, rim/outside 0.191 (aggregate of 68 individuals; 1/68 membrane-like individually; rim level 0.0754)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #54 (t=626, R_eq 5.14): ['A0', 'A1']; #17 (t=396, R_eq 5.53): ['A1']; #14 (t=302, R_eq 5.64): ['A1']; #194 (t=774, R_eq 5.01): ['A0', 'A1']

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 1 of 68 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
