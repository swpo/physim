# Evidence pack: active-nematic-marangoni-distance-pays (seed 601)

- world: `../../../../../../home/user/physim/research/alife/collective/contrib/20261027T0540-c54-distance-pays-loop1/world.py`, family `active-nematic`
- parent: collective/contrib/20261027T0000-c50-marangoni-spread-loop1/world.py; mutation: three heritable surfactant kinds with Marangoni coefficients 20/40/60 (majority-feedback production), in-run mutation between neighbouring kinds, trait-blind turnover
- run: 401 frames x 100 steps x dt 0.05 = time 2000; grid [128, 128]; wall 892s; status ok
- command: `python -m labkit.run collective/contrib/20261027T0540-c54-distance-pays-loop1/world.py --out /tmp/claude-0/c54/runs/E/seed601 --seeds 601 --size 128 128 --frames 400 --no-movie`
- segmentation: matter > 0.64 of robust range [-1.0024, 0.5562], min area 6 px

## Measurements
- components: final 17, mean 12.9, max 24; occupancy final 0.06
- tracks: 135; persistent (alive >= 50% of run): 3; longest 303 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 7.00 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [19, 17, 17], H1 [2, 0, 0]
- motion: 61 long-lived tracks moved >= 1 body length; max speed 0.41/time; max body lengths 14.7
- replication (lineage window K = 20 frames = time 100, default): splits 52, persistent splits 22 (0 more failed only because the siblings re-merged within K), max generation 5, merges 19, merge/split ratio 0.365, nucleations 12
- channel total drift (end/start - 1): [-0.5756, -0.5834, None, 8.0568, None, -0.0764]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 16 at frame 178: holes 0, rim-vs-core 0.48, rim-vs-outside 0.43, heterogeneity 0.09; core [0.962, 0.938, 0.003, 0.398, 0.0, 1.0] rim [0.801, 0.658, 0.007, 0.756, 0.0, 1.0]
  - track 34 at frame 188: holes 0, rim-vs-core 0.62, rim-vs-outside 0.39, heterogeneity 0.11; core [0.969, 0.884, 0.002, 0.425, 0.0, 1.0] rim [0.79, 0.589, 0.005, 0.941, 0.0, 1.0]
  - track 39 at frame 168: holes 0, rim-vs-core 0.63, rim-vs-outside 0.40, heterogeneity 0.10; core [0.976, 0.95, 0.0, 0.362, 0.0, 1.0] rim [0.79, 0.6, 0.001, 0.853, 0.0, 1.0]
  - track 113 at frame 376: holes 0, rim-vs-core 0.51, rim-vs-outside 0.34, heterogeneity 0.09; core [0.954, 0.782, 0.0, 0.422, 0.024, 1.0] rim [0.776, 0.513, 0.001, 0.813, 0.053, 1.0]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 83 components >= 12 px at frames [67, 134, 202, 266, 333, 400]):
  - radial phi (droplet): peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.815, rim/outside 2.93 (aggregate of 83 individuals; 0/83 membrane-like individually; rim level 0.742)
  - radial order |Q|: peak at rho=0.25 (OUTSIDE the peak band 0.5-1.5), rim/core 0.779, rim/outside 8.37 (aggregate of 83 individuals; 6/83 membrane-like individually; rim level 0.577)
  - radial s0 (mar 20): peak at rho=0.55 (in the peak band 0.5-1.5), rim/core 1.14, rim/outside 1.76 (aggregate of 83 individuals; 17/83 membrane-like individually; rim level 0.085)
  - radial s1 (mar 40): peak at rho=0.55 (in the peak band 0.5-1.5), rim/core 1.17, rim/outside 3.08 (aggregate of 83 individuals; 37/83 membrane-like individually; rim level 0.504)
  - radial s2 (mar 60): peak at rho=0.45 (OUTSIDE the peak band 0.5-1.5), rim/core 1.03, rim/outside 2.41 (aggregate of 83 individuals; 9/83 membrane-like individually; rim level 0.106)
  - radial chemostat target phi_b(x,t): peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 1, rim/outside 1.02 (aggregate of 83 individuals; 0/83 membrane-like individually; rim level 1)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #16 (t=890, R_eq 3.78): none; #34 (t=940, R_eq 4.3): none; #39 (t=840, R_eq 3.52): ['s1 (mar 40)']; #113 (t=1880, R_eq 4.37): none

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 2 of 83 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
