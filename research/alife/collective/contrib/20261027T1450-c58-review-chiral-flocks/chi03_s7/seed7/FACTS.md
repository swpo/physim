# Evidence pack: chiral-eating-flocks (seed 7)

- world: `../../../20261027T0216-c51-chiral-flocks-negative/world.py`, family `polar-active-fluid`
- parent: None; mutation: -
- run: 301 frames x 40 steps x dt 0.25 = time 3000; grid [128, 128]; wall 28s; status ok
- command: `python -m labkit.run collective/contrib/20261027T0216-c51-chiral-flocks-negative/world.py --out collective/contrib/20261027T1450-c58-review-chiral-flocks/chi03_s7 --seeds 7 8 --frames 300 --spf 40 --threshold 0.45 --no-movie`
- segmentation: matter > 0.59 of robust range [0.0, 0.7598], min area 6 px

## Measurements
- components: final 20, mean 18.1, max 27; occupancy final 0.07
- tracks: 1774; persistent (alive >= 50% of run): 0; longest 20 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 0.00 (1 = constant size)
- enclosures: components with a hole mean 0.05, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [24, 18, 11], H1 [2, 0, 0]
- motion: 1 long-lived tracks moved >= 1 body length; max speed 0.239/time; max body lengths 6.9
- replication (lineage window K = 20 frames = time 200, default): splits 327, persistent splits 0 (0 more failed only because the siblings re-merged within K), max generation 0, merges 243, merge/split ratio 0.743, nucleations 851
- channel total drift (end/start - 1): [0.7193, -0.4342, -0.368, -0.3178]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 236 at frame 48: holes 0, rim-vs-core 0.13, rim-vs-outside 0.28, heterogeneity 0.06; core [0.877, 0.057, 0.952, 0.0] rim [0.778, 0.14, 0.919, 0.004]
  - track 822 at frame 149: holes 0, rim-vs-core 0.25, rim-vs-outside 0.24, heterogeneity 0.08; core [0.941, 0.021, 0.969, 0.027] rim [0.728, 0.092, 0.877, 0.072]
  - track 1468 at frame 252: holes 0, rim-vs-core 0.11, rim-vs-outside 0.25, heterogeneity 0.10; core [0.863, 0.072, 0.953, 0.62] rim [0.779, 0.138, 0.923, 0.59]
  - track 1659 at frame 285: holes 0, rim-vs-core 0.13, rim-vs-outside 0.25, heterogeneity 0.11; core [0.881, 0.077, 0.955, 0.444] rim [0.776, 0.133, 0.919, 0.467]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 97 components >= 12 px at frames [50, 101, 151, 199, 250, 300]):
  - radial density rho: peak at rho=0.25 (OUTSIDE the peak band 0.5-1.5), rim/core 0.952, rim/outside 2.26 (aggregate of 97 individuals; 4/97 membrane-like individually; rim level 0.683)
  - radial food c: peak at rho=2.45 (OUTSIDE the peak band 0.5-1.5), rim/core 3.83, rim/outside 0.705 (aggregate of 97 individuals; 0/97 membrane-like individually; rim level 0.283)
  - radial |p|: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.983, rim/outside 1.87 (aggregate of 97 individuals; 2/97 membrane-like individually; rim level 0.844)
  - radial p_x: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.979, rim/outside 0.998 (aggregate of 97 individuals; 0/97 membrane-like individually; rim level 0.457)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #236 (t=480, R_eq 3.43): none; #822 (t=1490, R_eq 4.11): none; #1468 (t=2520, R_eq 3.43): none; #1659 (t=2850, R_eq 3.95): none

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 19 of 97 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
