# Evidence pack: active-nematic-marangoni-distance-pays (seed 620)

- world: `../../../w2/world.py`, family `active-nematic`
- parent: collective/contrib/20261027T0000-c50-marangoni-spread-loop1/world.py; mutation: three heritable surfactant kinds with Marangoni coefficients 20/40/60 (majority-feedback production), in-run mutation between neighbouring kinds, trait-blind turnover
- run: 401 frames x 100 steps x dt 0.05 = time 2000; grid [128, 128]; wall 974s; status ok
- command: `python -m labkit.run /tmp/claude-0/c54/w2/world.py --out /tmp/claude-0/c54/runs/m40dep/seed620 --seeds 620 --size 128 128 --frames 400 --no-movie`
- segmentation: matter > 0.66 of robust range [-1.0181, 0.5294], min area 6 px

## Measurements
- components: final 10, mean 5.5, max 10; occupancy final 0.03
- tracks: 45; persistent (alive >= 50% of run): 0; longest 166 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 0.00 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [10, 10, 10], H1 [1, 0, 0]
- motion: 29 long-lived tracks moved >= 1 body length; max speed 0.398/time; max body lengths 14.1
- replication (lineage window K = 20 frames = time 100, default): splits 20, persistent splits 13 (0 more failed only because the siblings re-merged within K), max generation 5, merges 2, merge/split ratio 0.1, nucleations 3
- channel total drift (end/start - 1): [-0.7491, -0.7667, None, 6.0425, None, -0.2087]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 25 at frame 319: holes 0, rim-vs-core 0.57, rim-vs-outside 0.40, heterogeneity 0.15; core [0.994, 0.93, 0.082, 0.46, 0.082, 0.963] rim [0.84, 0.666, 0.154, 0.93, 0.154, 0.885]
  - track 28 at frame 329: holes 0, rim-vs-core 0.54, rim-vs-outside 0.46, heterogeneity 0.11; core [0.996, 0.985, 0.134, 0.356, 0.134, 1.0] rim [0.85, 0.783, 0.265, 0.795, 0.265, 1.0]
  - track 6 at frame 97: holes 0, rim-vs-core 0.60, rim-vs-outside 0.44, heterogeneity 0.11; core [0.997, 0.979, 0.079, 0.446, 0.079, 1.0] rim [0.87, 0.763, 0.175, 0.971, 0.175, 1.0]
  - track 37 at frame 366: holes 0, rim-vs-core 0.52, rim-vs-outside 0.44, heterogeneity 0.11; core [0.991, 0.975, 0.089, 0.458, 0.089, 0.841] rim [0.838, 0.787, 0.169, 0.908, 0.169, 0.854]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 40 components >= 12 px at frames [67, 134, 202, 266, 333, 400]):
  - radial phi (droplet): peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.861, rim/outside 2.86 (aggregate of 40 individuals; 0/40 membrane-like individually; rim level 0.818)
  - radial order |Q|: peak at rho=0.25 (OUTSIDE the peak band 0.5-1.5), rim/core 0.881, rim/outside 8.44 (aggregate of 40 individuals; 1/40 membrane-like individually; rim level 0.718)
  - radial s0 (mar 20): peak at rho=0.55 (in the peak band 0.5-1.5), rim/core 1.21, rim/outside 2 (aggregate of 40 individuals; 21/40 membrane-like individually; rim level 0.28)
  - radial s1 (mar 40): peak at rho=0.65 (in the peak band 0.5-1.5), rim/core 1.34, rim/outside 3.26 (aggregate of 40 individuals; 21/40 membrane-like individually; rim level 0.685)
  - radial s2 (mar 60): peak at rho=0.55 (in the peak band 0.5-1.5), rim/core 1.21, rim/outside 2 (aggregate of 40 individuals; 21/40 membrane-like individually; rim level 0.28)
  - radial chemostat target phi_b(x,t): peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.995, rim/outside 1.02 (aggregate of 40 individuals; 1/40 membrane-like individually; rim level 0.912)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #25 (t=1595, R_eq 4.11): none; #28 (t=1645, R_eq 3.52): ['s0 (mar 20)', 's1 (mar 40)', 's2 (mar 60)']; #6 (t=485, R_eq 3.57): ['s0 (mar 20)', 's1 (mar 40)', 's2 (mar 60)']; #37 (t=1830, R_eq 3.83): ['s0 (mar 20)', 's1 (mar 40)', 's2 (mar 60)']

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 1 of 40 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
