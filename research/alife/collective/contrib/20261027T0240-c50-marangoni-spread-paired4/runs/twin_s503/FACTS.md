# Evidence pack: active-nematic-marangoni-spread (seed 503)

- world: `../../../world.py`, family `active-nematic`
- parent: collective/contrib/20261026T0505-c34-nematic-marangoni/world.py; mutation: three heritable surfactant kinds with Marangoni coefficients 20/40/60 (majority-feedback production), in-run mutation between neighbouring kinds, trait-blind turnover
- run: 401 frames x 100 steps x dt 0.05 = time 2000; grid [128, 128]; wall 1076s; status ok
- command: `python -m labkit.run /tmp/claude-0/sp/world.py --out /tmp/claude-0/sp/runs/twin/seed503 --seeds 503 --size 128 128 --frames 400 --no-movie`
- segmentation: matter > 0.65 of robust range [-1.0188, 0.5451], min area 6 px

## Measurements
- components: final 7, mean 10.0, max 19; occupancy final 0.03
- tracks: 86; persistent (alive >= 50% of run): 1; longest 257 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 9.83 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [8, 8, 7], H1 [0, 0, 0]
- motion: 52 long-lived tracks moved >= 1 body length; max speed 0.512/time; max body lengths 21.7
- replication (lineage window K = 20 frames = time 100, default): splits 32, persistent splits 18 (0 more failed only because the siblings re-merged within K), max generation 6, merges 10, merge/split ratio 0.312, nucleations 12
- channel total drift (end/start - 1): [-0.8133, -0.8242, None, 0.7873, None, -0.2625]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 4 at frame 141: holes 0, rim-vs-core 0.74, rim-vs-outside 0.39, heterogeneity 0.11; core [0.995, 0.934, 0.0, 0.283, 0.021, 1.0] rim [0.825, 0.517, 0.0, 0.865, 0.064, 1.0]
  - track 61 at frame 323: holes 0, rim-vs-core 0.47, rim-vs-outside 0.32, heterogeneity 0.09; core [0.946, 0.729, 0.0, 0.548, 0.011, 1.0] rim [0.787, 0.513, 0.001, 0.937, 0.022, 1.0]
  - track 63 at frame 336: holes 0, rim-vs-core 0.38, rim-vs-outside 0.38, heterogeneity 0.06; core [0.965, 0.921, 1.0, 0.023, 0.013, 1.0] rim [0.778, 0.593, 1.0, 0.055, 0.029, 1.0]
  - track 13 at frame 87: holes 0, rim-vs-core 0.59, rim-vs-outside 0.30, heterogeneity 0.11; core [0.978, 0.618, 0.004, 0.476, 0.015, 1.0] rim [0.798, 0.379, 0.012, 0.986, 0.04, 1.0]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 56 components >= 12 px at frames [67, 134, 202, 266, 333, 400]):
  - radial phi (droplet): peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.837, rim/outside 2.86 (aggregate of 56 individuals; 0/56 membrane-like individually; rim level 0.744)
  - radial order |Q|: peak at rho=0.35 (OUTSIDE the peak band 0.5-1.5), rim/core 0.828, rim/outside 7.68 (aggregate of 56 individuals; 2/56 membrane-like individually; rim level 0.557)
  - radial s0 (mar 20): peak at rho=0.75 (in the peak band 0.5-1.5), rim/core 1.19, rim/outside 1.6 (aggregate of 56 individuals; 10/56 membrane-like individually; rim level 0.101)
  - radial s1 (mar 40): peak at rho=0.65 (in the peak band 0.5-1.5), rim/core 1.18, rim/outside 3.26 (aggregate of 56 individuals; 21/56 membrane-like individually; rim level 0.402)
  - radial s2 (mar 60): peak at rho=0.75 (in the peak band 0.5-1.5), rim/core 1.12, rim/outside 2.98 (aggregate of 56 individuals; 19/56 membrane-like individually; rim level 0.267)
  - radial chemostat target phi_b(x,t): peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.987, rim/outside 1.02 (aggregate of 56 individuals; 1/56 membrane-like individually; rim level 0.972)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #4 (t=705, R_eq 2.71): ['s1 (mar 40)', 's2 (mar 60)']; #61 (t=1615, R_eq 4.95): none; #63 (t=1680, R_eq 3.48): ['s1 (mar 40)', 's2 (mar 60)']; #13 (t=435, R_eq 4.15): ['order |Q|', 's2 (mar 60)']

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 3 of 56 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
