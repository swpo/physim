# Evidence pack: active-nematic-marangoni-distance-pays (seed 620)

- world: `../../../w2/world.py`, family `active-nematic`
- parent: collective/contrib/20261027T0000-c50-marangoni-spread-loop1/world.py; mutation: three heritable surfactant kinds with Marangoni coefficients 20/40/60 (majority-feedback production), in-run mutation between neighbouring kinds, trait-blind turnover
- run: 401 frames x 100 steps x dt 0.05 = time 2000; grid [128, 128]; wall 980s; status ok
- command: `python -m labkit.run /tmp/claude-0/c54/w2/world.py --out /tmp/claude-0/c54/runs/m60dep/seed620 --seeds 620 --size 128 128 --frames 400 --no-movie`
- segmentation: matter > 0.67 of robust range [-1.0198, 0.5043], min area 6 px

## Measurements
- components: final 11, mean 5.8, max 11; occupancy final 0.02
- tracks: 60; persistent (alive >= 50% of run): 0; longest 131 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 0.00 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [1, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [11, 11, 9], H1 [1, 0, 0]
- motion: 35 long-lived tracks moved >= 1 body length; max speed 0.675/time; max body lengths 16.9
- replication (lineage window K = 20 frames = time 100, default): splits 27, persistent splits 19 (0 more failed only because the siblings re-merged within K), max generation 6, merges 3, merge/split ratio 0.111, nucleations 3
- channel total drift (end/start - 1): [-0.7937, -0.8509, None, None, 4.6326, -0.2473]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 32 at frame 303: holes 0, rim-vs-core 0.57, rim-vs-outside 0.44, heterogeneity 0.11; core [0.996, 0.959, 0.142, 0.142, 0.552, 1.0] rim [0.871, 0.652, 0.273, 0.273, 0.982, 1.0]
  - track 7 at frame 111: holes 0, rim-vs-core 0.55, rim-vs-outside 0.47, heterogeneity 0.12; core [0.994, 0.974, 0.233, 0.233, 0.407, 1.0] rim [0.856, 0.778, 0.427, 0.427, 0.819, 1.0]
  - track 8 at frame 111: holes 0, rim-vs-core 0.56, rim-vs-outside 0.46, heterogeneity 0.12; core [0.995, 0.961, 0.143, 0.143, 0.497, 1.0] rim [0.869, 0.716, 0.256, 0.256, 0.964, 1.0]
  - track 48 at frame 383: holes 0, rim-vs-core 0.55, rim-vs-outside 0.43, heterogeneity 0.11; core [1.0, 0.982, 0.171, 0.171, 0.517, 0.833] rim [0.869, 0.693, 0.31, 0.31, 0.92, 0.833]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 40 components >= 12 px at frames [67, 134, 202, 266, 333, 400]):
  - radial phi (droplet): peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.855, rim/outside 2.89 (aggregate of 40 individuals; 0/40 membrane-like individually; rim level 0.836)
  - radial order |Q|: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.832, rim/outside 9.74 (aggregate of 40 individuals; 2/40 membrane-like individually; rim level 0.72)
  - radial s0 (mar 20): peak at rho=0.55 (in the peak band 0.5-1.5), rim/core 1.24, rim/outside 3.49 (aggregate of 40 individuals; 24/40 membrane-like individually; rim level 0.286)
  - radial s1 (mar 40): peak at rho=0.55 (in the peak band 0.5-1.5), rim/core 1.24, rim/outside 3.49 (aggregate of 40 individuals; 24/40 membrane-like individually; rim level 0.286)
  - radial s2 (mar 60): peak at rho=0.55 (in the peak band 0.5-1.5), rim/core 1.49, rim/outside 3.52 (aggregate of 40 individuals; 25/40 membrane-like individually; rim level 0.742)
  - radial chemostat target phi_b(x,t): peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.99, rim/outside 1.04 (aggregate of 40 individuals; 0/40 membrane-like individually; rim level 0.918)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #32 (t=1515, R_eq 3.14): ['s0 (mar 20)', 's1 (mar 40)']; #7 (t=555, R_eq 3.52): ['s0 (mar 20)', 's1 (mar 40)', 's2 (mar 60)']; #8 (t=555, R_eq 3.43): ['s0 (mar 20)', 's1 (mar 40)', 's2 (mar 60)']; #48 (t=1915, R_eq 3.29): ['s0 (mar 20)', 's1 (mar 40)', 's2 (mar 60)']

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
