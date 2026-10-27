# Evidence pack: active-nematic-marangoni-distance-pays (seed 600)

- world: `../../../../../../home/user/physim/research/alife/collective/contrib/20261027T0540-c54-distance-pays-loop1/world.py`, family `active-nematic`
- parent: collective/contrib/20261027T0000-c50-marangoni-spread-loop1/world.py; mutation: three heritable surfactant kinds with Marangoni coefficients 20/40/60 (majority-feedback production), in-run mutation between neighbouring kinds, trait-blind turnover
- run: 401 frames x 100 steps x dt 0.05 = time 2000; grid [128, 128]; wall 835s; status ok
- command: `python -m labkit.run collective/contrib/20261027T0540-c54-distance-pays-loop1/world.py --out /tmp/claude-0/c54/runs/E/seed600 --seeds 600 --size 128 128 --frames 400 --no-movie`
- segmentation: matter > 0.64 of robust range [-1.0025, 0.564], min area 6 px

## Measurements
- components: final 9, mean 13.5, max 19; occupancy final 0.03
- tracks: 132; persistent (alive >= 50% of run): 0; longest 182 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 0.00 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [11, 10, 9], H1 [0, 0, 0]
- motion: 68 long-lived tracks moved >= 1 body length; max speed 0.277/time; max body lengths 11.2
- replication (lineage window K = 20 frames = time 100, default): splits 50, persistent splits 27 (0 more failed only because the siblings re-merged within K), max generation 6, merges 27, merge/split ratio 0.54, nucleations 5
- channel total drift (end/start - 1): [-0.8251, -0.7896, None, 3.7391, None, -0.192]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 45 at frame 242: holes 0, rim-vs-core 0.67, rim-vs-outside 0.38, heterogeneity 0.10; core [0.98, 0.955, 0.473, 0.007, 0.001, 1.0] rim [0.789, 0.594, 1.0, 0.025, 0.002, 1.0]
  - track 76 at frame 316: holes 0, rim-vs-core 0.43, rim-vs-outside 0.45, heterogeneity 0.10; core [0.972, 0.984, 0.677, 0.023, 0.041, 1.0] rim [0.787, 0.793, 1.0, 0.061, 0.108, 1.0]
  - track 59 at frame 259: holes 0, rim-vs-core 0.61, rim-vs-outside 0.32, heterogeneity 0.15; core [0.957, 0.56, 0.004, 0.469, 0.006, 1.0] rim [0.758, 0.305, 0.011, 0.95, 0.014, 0.826]
  - track 128 at frame 390: holes 0, rim-vs-core 0.58, rim-vs-outside 0.33, heterogeneity 0.10; core [0.956, 0.715, 0.004, 0.515, 0.014, 1.0] rim [0.776, 0.452, 0.01, 0.994, 0.034, 1.0]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 85 components >= 12 px at frames [67, 134, 202, 266, 333, 400]):
  - radial phi (droplet): peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.815, rim/outside 3.03 (aggregate of 85 individuals; 0/85 membrane-like individually; rim level 0.757)
  - radial order |Q|: peak at rho=0.25 (OUTSIDE the peak band 0.5-1.5), rim/core 0.756, rim/outside 8.89 (aggregate of 85 individuals; 3/85 membrane-like individually; rim level 0.586)
  - radial s0 (mar 20): peak at rho=0.75 (in the peak band 0.5-1.5), rim/core 1.3, rim/outside 2.7 (aggregate of 85 individuals; 21/85 membrane-like individually; rim level 0.116)
  - radial s1 (mar 40): peak at rho=0.75 (in the peak band 0.5-1.5), rim/core 1.43, rim/outside 3.34 (aggregate of 85 individuals; 47/85 membrane-like individually; rim level 0.525)
  - radial s2 (mar 60): peak at rho=0.45 (OUTSIDE the peak band 0.5-1.5), rim/core 1.04, rim/outside 2.39 (aggregate of 85 individuals; 28/85 membrane-like individually; rim level 0.081)
  - radial chemostat target phi_b(x,t): peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 1, rim/outside 1.02 (aggregate of 85 individuals; 1/85 membrane-like individually; rim level 0.995)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #45 (t=1210, R_eq 3.24): ['s0 (mar 20)']; #76 (t=1580, R_eq 4.65): none; #59 (t=1295, R_eq 3.7): ['s1 (mar 40)', 's2 (mar 60)']; #128 (t=1950, R_eq 4.07): none

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 2 of 85 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
