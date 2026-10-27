# Evidence pack: active-nematic-marangoni-distance-pays (seed 620)

- world: `../../../w2/world.py`, family `active-nematic`
- parent: collective/contrib/20261027T0000-c50-marangoni-spread-loop1/world.py; mutation: three heritable surfactant kinds with Marangoni coefficients 20/40/60 (majority-feedback production), in-run mutation between neighbouring kinds, trait-blind turnover
- run: 401 frames x 100 steps x dt 0.05 = time 2000; grid [128, 128]; wall 1002s; status ok
- command: `python -m labkit.run /tmp/claude-0/c54/w2/world.py --out /tmp/claude-0/c54/runs/m40E/seed620 --seeds 620 --size 128 128 --frames 400 --no-movie`
- segmentation: matter > 0.65 of robust range [-1.0179, 0.5363], min area 6 px

## Measurements
- components: final 14, mean 8.0, max 14; occupancy final 0.04
- tracks: 94; persistent (alive >= 50% of run): 0; longest 139 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 0.00 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [16, 14, 13], H1 [1, 0, 0]
- motion: 52 long-lived tracks moved >= 1 body length; max speed 0.315/time; max body lengths 11.0
- replication (lineage window K = 20 frames = time 100, default): splits 40, persistent splits 25 (0 more failed only because the siblings re-merged within K), max generation 8, merges 11, merge/split ratio 0.275, nucleations 3
- channel total drift (end/start - 1): [-0.721, -0.7175, None, 7.9489, None, -0.1831]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 34 at frame 239: holes 0, rim-vs-core 0.60, rim-vs-outside 0.36, heterogeneity 0.11; core [0.971, 0.86, 0.058, 0.495, 0.058, 1.0] rim [0.788, 0.523, 0.108, 0.948, 0.108, 1.0]
  - track 46 at frame 299: holes 0, rim-vs-core 0.67, rim-vs-outside 0.39, heterogeneity 0.12; core [0.979, 0.9, 0.09, 0.343, 0.09, 1.0] rim [0.827, 0.552, 0.218, 0.859, 0.218, 1.0]
  - track 55 at frame 346: holes 0, rim-vs-core 0.59, rim-vs-outside 0.41, heterogeneity 0.11; core [0.984, 0.953, 0.1, 0.326, 0.1, 1.0] rim [0.806, 0.63, 0.193, 0.763, 0.193, 1.0]
  - track 84 at frame 390: holes 0, rim-vs-core 0.67, rim-vs-outside 0.32, heterogeneity 0.16; core [0.97, 0.674, 0.248, 0.482, 0.248, 1.0] rim [0.79, 0.438, 0.527, 0.929, 0.527, 1.0]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 55 components >= 12 px at frames [67, 134, 202, 266, 333, 400]):
  - radial phi (droplet): peak at rho=0.25 (OUTSIDE the peak band 0.5-1.5), rim/core 0.814, rim/outside 2.71 (aggregate of 55 individuals; 0/55 membrane-like individually; rim level 0.745)
  - radial order |Q|: peak at rho=0.25 (OUTSIDE the peak band 0.5-1.5), rim/core 0.782, rim/outside 7.45 (aggregate of 55 individuals; 4/55 membrane-like individually; rim level 0.576)
  - radial s0 (mar 20): peak at rho=0.65 (in the peak band 0.5-1.5), rim/core 1.16, rim/outside 2.7 (aggregate of 55 individuals; 23/55 membrane-like individually; rim level 0.141)
  - radial s1 (mar 40): peak at rho=0.65 (in the peak band 0.5-1.5), rim/core 1.28, rim/outside 3.24 (aggregate of 55 individuals; 25/55 membrane-like individually; rim level 0.641)
  - radial s2 (mar 60): peak at rho=0.65 (in the peak band 0.5-1.5), rim/core 1.16, rim/outside 2.7 (aggregate of 55 individuals; 23/55 membrane-like individually; rim level 0.141)
  - radial chemostat target phi_b(x,t): peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 1, rim/outside 1.02 (aggregate of 55 individuals; 0/55 membrane-like individually; rim level 1)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #34 (t=1195, R_eq 3.83): ['s0 (mar 20)', 's1 (mar 40)', 's2 (mar 60)']; #46 (t=1495, R_eq 2.99): ['s0 (mar 20)', 's1 (mar 40)', 's2 (mar 60)']; #55 (t=1730, R_eq 3.34): ['s0 (mar 20)', 's1 (mar 40)', 's2 (mar 60)']; #84 (t=1950, R_eq 4.92): none

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 2 of 55 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
