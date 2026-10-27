# Evidence pack: chiral-eating-flocks (seed 6)

- world: `../../../20261027T0216-c51-chiral-flocks-negative/world.py`, family `polar-active-fluid`
- parent: None; mutation: -
- run: 301 frames x 40 steps x dt 0.25 = time 3000; grid [128, 128]; wall 29s; status ok
- command: `python -m labkit.run collective/contrib/20261027T0216-c51-chiral-flocks-negative/world.py --out collective/contrib/c53-rev-ch/chi20 --seeds 5 6 --frames 300 --spf 40 --no-movie`
- segmentation: matter > 0.35 of robust range [0.0, 0.5199], min area 6 px

## Measurements
- components: final 63, mean 53.0, max 63; occupancy final 0.42
- tracks: 428; persistent (alive >= 50% of run): 59; longest 294 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 2.16 (1 = constant size)
- enclosures: components with a hole mean 0.02, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [64, 64, 63], H1 [30, 0, 0]
- motion: 0 long-lived tracks moved >= 1 body length; max speed 0/time; max body lengths 0.7
- replication (lineage window K = 20 frames = time 200, default): splits 135, persistent splits 22 (0 more failed only because the siblings re-merged within K), max generation 4, merges 100, merge/split ratio 0.741, nucleations 3
- channel total drift (end/start - 1): [0.8234, -0.4991, -0.2535, -2.0648]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 66 at frame 154: holes 0, rim-vs-core 0.46, rim-vs-outside 0.30, heterogeneity 0.14; core [0.791, 0.129, 0.841, 0.831] rim [0.504, 0.29, 0.557, 0.691]
  - track 134 at frame 161: holes 0, rim-vs-core 0.46, rim-vs-outside 0.59, heterogeneity 0.14; core [0.848, 0.073, 0.913, 0.06] rim [0.577, 0.266, 0.62, 0.192]
  - track 153 at frame 161: holes 0, rim-vs-core 0.49, rim-vs-outside 0.32, heterogeneity 0.14; core [0.799, 0.124, 0.851, 0.795] rim [0.491, 0.308, 0.53, 0.7]
  - track 418 at frame 222: holes 0, rim-vs-core 0.47, rim-vs-outside 0.31, heterogeneity 0.13; core [0.809, 0.118, 0.86, 0.731] rim [0.503, 0.297, 0.555, 0.664]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 337 components >= 12 px at frames [50, 101, 151, 199, 250, 300]):
  - radial density rho: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.865, rim/outside 2.95 (aggregate of 337 individuals; 0/337 membrane-like individually; rim level 0.751)
  - radial food c: peak at rho=1.55 (OUTSIDE the peak band 0.5-1.5), rim/core 9.56, rim/outside 1.05 (aggregate of 337 individuals; 0/337 membrane-like individually; rim level 0.463)
  - radial |p|: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.858, rim/outside 3.18 (aggregate of 337 individuals; 0/337 membrane-like individually; rim level 0.807)
  - radial p_x: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.992, rim/outside 1.02 (aggregate of 337 individuals; 0/337 membrane-like individually; rim level 0.506)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #66 (t=1540, R_eq 5.23): none; #134 (t=1610, R_eq 6.15): none; #153 (t=1610, R_eq 5.86): none; #418 (t=2220, R_eq 5.7): none

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 4 of 337 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
