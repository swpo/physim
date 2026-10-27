# Evidence pack: chiral-eating-flocks (seed 5)

- world: `../../../20261027T0216-c51-chiral-flocks-negative/world.py`, family `polar-active-fluid`
- parent: None; mutation: -
- run: 301 frames x 40 steps x dt 0.25 = time 3000; grid [128, 128]; wall 27s; status ok
- command: `python -m labkit.run collective/contrib/20261027T0216-c51-chiral-flocks-negative/world.py --out collective/contrib/c53-rev-ch/chi03 --seeds 5 6 --frames 300 --spf 40 --no-movie`
- segmentation: matter > 0.35 of robust range [0.0, 0.7612], min area 6 px

## Measurements
- components: final 11, mean 15.0, max 25; occupancy final 0.23
- tracks: 2549; persistent (alive >= 50% of run): 0; longest 9 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 0.00 (1 = constant size)
- enclosures: components with a hole mean 0.08, final 0; holes at thresholds 0.2/0.35/0.5 final [2, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [22, 17, 9], H1 [2, 2, 0]
- motion: 0 long-lived tracks moved >= 1 body length; max speed 0/time; max body lengths 2.3
- replication (lineage window K = 20 frames = time 200, default): splits 907, persistent splits 0 (0 more failed only because the siblings re-merged within K), max generation 0, merges 881, merge/split ratio 0.971, nucleations 38
- channel total drift (end/start - 1): [0.356, -0.4335, -0.3543, -2.1393]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 412 at frame 58: holes 0, rim-vs-core 0.32, rim-vs-outside 0.68, heterogeneity 0.19; core [0.809, 0.069, 0.919, 0.335] rim [0.604, 0.259, 0.801, 0.43]
  - track 1004 at frame 129: holes 0, rim-vs-core 0.11, rim-vs-outside 0.19, heterogeneity 0.05; core [0.521, 0.308, 0.731, 0.083] rim [0.454, 0.351, 0.668, 0.128]
  - track 1032 at frame 134: holes 0, rim-vs-core 0.43, rim-vs-outside 0.42, heterogeneity 0.20; core [0.811, 0.132, 0.894, 0.594] rim [0.512, 0.371, 0.715, 0.526]
  - track 2314 at frame 277: holes 0, rim-vs-core 0.25, rim-vs-outside 0.30, heterogeneity 0.09; core [0.622, 0.234, 0.813, 0.057] rim [0.465, 0.353, 0.683, 0.149]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 81 components >= 12 px at frames [50, 101, 151, 199, 250, 300]):
  - radial density rho: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.908, rim/outside 2.8 (aggregate of 81 individuals; 11/81 membrane-like individually; rim level 0.469)
  - radial food c: peak at rho=2.15 (OUTSIDE the peak band 0.5-1.5), rim/core 2.59, rim/outside 0.83 (aggregate of 81 individuals; 0/81 membrane-like individually; rim level 0.454)
  - radial |p|: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.921, rim/outside 2.92 (aggregate of 81 individuals; 5/81 membrane-like individually; rim level 0.652)
  - radial p_x: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.984, rim/outside 0.997 (aggregate of 81 individuals; 0/81 membrane-like individually; rim level 0.474)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #412 (t=580, R_eq 7.59, ring): none; #1004 (t=1290, R_eq 2.71): none; #1032 (t=1340, R_eq 5.41): none; #2314 (t=2770, R_eq 4.11): none

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 20 of 81 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
