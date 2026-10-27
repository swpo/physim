# Evidence pack: active-nematic-marangoni-ladder (seed 101)

- world: `../../../world.py`, family `active-nematic`
- parent: collective/contrib/20261026T0505-c34-nematic-marangoni/world.py; mutation: three heritable surfactant kinds with Marangoni coefficients 20/40/60 (majority-feedback production), in-run mutation between neighbouring kinds, trait-blind turnover
- run: 401 frames x 100 steps x dt 0.05 = time 2000; grid [128, 128]; wall 861s; status ok
- command: `python -m labkit.run /tmp/claude-0/ld/world.py --out /tmp/claude-0/ld/runs/twin/seed101 --seeds 101 --size 128 128 --frames 400 --no-movie`
- segmentation: matter > 0.59 of robust range [-0.8271, 0.5741], min area 6 px

## Measurements
- components: final 18, mean 20.0, max 29; occupancy final 0.07
- tracks: 286; persistent (alive >= 50% of run): 0; longest 176 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 0.00 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [24, 18, 18], H1 [1, 0, 0]
- motion: 138 long-lived tracks moved >= 1 body length; max speed 0.328/time; max body lengths 8.1
- replication (lineage window K = 20 frames = time 100, default): splits 124, persistent splits 63 (0 more failed only because the siblings re-merged within K), max generation 10, merges 27, merge/split ratio 0.218, nucleations 8
- channel total drift (end/start - 1): [-0.4916, -0.5714, 5.6155, 2.8205, 1.7983]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 117 at frame 262: holes 0, rim-vs-core 0.58, rim-vs-outside 0.36, heterogeneity 0.12; core [0.949, 0.84, 0.428, 0.015, 0.022] rim [0.763, 0.541, 0.892, 0.042, 0.049]
  - track 53 at frame 145: holes 0, rim-vs-core 0.60, rim-vs-outside 0.39, heterogeneity 0.12; core [0.95, 0.875, 0.013, 0.002, 0.427] rim [0.756, 0.572, 0.033, 0.005, 0.909]
  - track 144 at frame 269: holes 0, rim-vs-core 0.59, rim-vs-outside 0.35, heterogeneity 0.12; core [0.953, 0.7, 0.48, 0.007, 0.006] rim [0.745, 0.453, 0.968, 0.015, 0.016]
  - track 262 at frame 383: holes 0, rim-vs-core 0.67, rim-vs-outside 0.36, heterogeneity 0.14; core [0.953, 0.785, 0.391, 0.011, 0.035] rim [0.758, 0.437, 0.92, 0.03, 0.1]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 131 components >= 12 px at frames [67, 134, 202, 266, 333, 400]):
  - radial phi (droplet): peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.788, rim/outside 4.21 (aggregate of 131 individuals; 0/131 membrane-like individually; rim level 0.687)
  - radial order |Q|: peak at rho=0.25 (OUTSIDE the peak band 0.5-1.5), rim/core 0.784, rim/outside 7.82 (aggregate of 131 individuals; 11/131 membrane-like individually; rim level 0.526)
  - radial s0 (mar 20): peak at rho=0.75 (in the peak band 0.5-1.5), rim/core 1.21, rim/outside 2.95 (aggregate of 131 individuals; 42/131 membrane-like individually; rim level 0.292)
  - radial s1 (mar 40): peak at rho=0.55 (in the peak band 0.5-1.5), rim/core 1.23, rim/outside 2.9 (aggregate of 131 individuals; 34/131 membrane-like individually; rim level 0.172)
  - radial s2 (mar 60): peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 1.1, rim/outside 2.88 (aggregate of 131 individuals; 39/131 membrane-like individually; rim level 0.216)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #117 (t=1310, R_eq 3.66): ['s0 (mar 20)', 's1 (mar 40)', 's2 (mar 60)']; #53 (t=725, R_eq 3.61): ['s0 (mar 20)', 's2 (mar 60)']; #144 (t=1345, R_eq 4.62): none; #262 (t=1915, R_eq 2.88): ['s0 (mar 20)', 's1 (mar 40)', 's2 (mar 60)']

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 6 of 131 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
