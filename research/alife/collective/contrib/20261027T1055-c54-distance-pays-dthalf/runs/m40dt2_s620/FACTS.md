# Evidence pack: active-nematic-marangoni-distance-pays (seed 620)

- world: `../../../w2/world.py`, family `active-nematic`
- parent: collective/contrib/20261027T0000-c50-marangoni-spread-loop1/world.py; mutation: three heritable surfactant kinds with Marangoni coefficients 20/40/60 (majority-feedback production), in-run mutation between neighbouring kinds, trait-blind turnover
- run: 401 frames x 200 steps x dt 0.05 = time 4000; grid [128, 128]; wall 2022s; status ok
- command: `python -m labkit.run /tmp/claude-0/c54/w2/world.py --out /tmp/claude-0/c54/runs/m40dt2/seed620 --seeds 620 --size 128 128 --frames 400 --spf 200 --no-movie`
- segmentation: matter > 0.67 of robust range [-1.0144, 0.499], min area 6 px

## Measurements
- components: final 5, mean 2.8, max 7; occupancy final 0.01
- tracks: 36; persistent (alive >= 50% of run): 0; longest 106 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 0.00 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [5, 5, 5], H1 [1, 0, 0]
- motion: 24 long-lived tracks moved >= 1 body length; max speed 0.256/time; max body lengths 8.9
- replication (lineage window K = 20 frames = time 200, default): splits 14, persistent splits 9 (0 more failed only because the siblings re-merged within K), max generation 6, merges 4, merge/split ratio 0.286, nucleations 4
- channel total drift (end/start - 1): [-0.7642, -0.905, None, 1.3903, None, -0.2128]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 20 at frame 212: holes 0, rim-vs-core 0.50, rim-vs-outside 0.45, heterogeneity 0.09; core [1.0, 1.0, 0.129, 0.546, 0.129, 1.0] rim [0.969, 0.935, 0.274, 0.994, 0.274, 1.0]
  - track 16 at frame 128: holes 0, rim-vs-core 0.57, rim-vs-outside 0.50, heterogeneity 0.10; core [1.0, 1.0, 0.123, 0.488, 0.123, 0.833] rim [0.969, 0.884, 0.279, 1.0, 0.279, 0.833]
  - track 4 at frame 57: holes 0, rim-vs-core 0.55, rim-vs-outside 0.41, heterogeneity 0.12; core [1.0, 0.98, 0.248, 0.558, 0.248, 1.0] rim [0.951, 0.842, 0.466, 0.985, 0.466, 1.0]
  - track 28 at frame 366: holes 0, rim-vs-core 0.54, rim-vs-outside 0.47, heterogeneity 0.09; core [1.0, 1.0, 0.153, 0.475, 0.153, 1.0] rim [0.966, 0.938, 0.282, 0.982, 0.282, 1.0]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 18 components >= 12 px at frames [67, 134, 202, 266, 333, 400]):
  - radial phi (droplet): peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.919, rim/outside 2.81 (aggregate of 18 individuals; 0/18 membrane-like individually; rim level 0.91)
  - radial order |Q|: peak at rho=0.25 (OUTSIDE the peak band 0.5-1.5), rim/core 0.978, rim/outside 7.67 (aggregate of 18 individuals; 1/18 membrane-like individually; rim level 0.911)
  - radial s0 (mar 20): peak at rho=0.75 (in the peak band 0.5-1.5), rim/core 1.41, rim/outside 2.78 (aggregate of 18 individuals; 12/18 membrane-like individually; rim level 0.448)
  - radial s1 (mar 40): peak at rho=0.75 (in the peak band 0.5-1.5), rim/core 1.4, rim/outside 3.73 (aggregate of 18 individuals; 10/18 membrane-like individually; rim level 0.841)
  - radial s2 (mar 60): peak at rho=0.75 (in the peak band 0.5-1.5), rim/core 1.41, rim/outside 2.78 (aggregate of 18 individuals; 12/18 membrane-like individually; rim level 0.448)
  - radial chemostat target phi_b(x,t): peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.989, rim/outside 1.04 (aggregate of 18 individuals; 0/18 membrane-like individually; rim level 0.892)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #20 (t=2120, R_eq 3.83): none; #16 (t=1280, R_eq 3.19): ['s0 (mar 20)', 's1 (mar 40)', 's2 (mar 60)']; #4 (t=570, R_eq 5.05): none; #28 (t=3660, R_eq 3.39): ['s0 (mar 20)', 's1 (mar 40)', 's2 (mar 60)']

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
