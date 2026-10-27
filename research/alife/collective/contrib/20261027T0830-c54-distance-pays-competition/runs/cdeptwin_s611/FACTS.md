# Evidence pack: active-nematic-marangoni-distance-pays (seed 611)

- world: `../../../w2/world.py`, family `active-nematic`
- parent: collective/contrib/20261027T0000-c50-marangoni-spread-loop1/world.py; mutation: three heritable surfactant kinds with Marangoni coefficients 20/40/60 (majority-feedback production), in-run mutation between neighbouring kinds, trait-blind turnover
- run: 401 frames x 100 steps x dt 0.05 = time 2000; grid [128, 128]; wall 944s; status ok
- command: `python -m labkit.run /tmp/claude-0/c54/w2/world.py --out /tmp/claude-0/c54/runs/cdeptwin/seed611 --seeds 611 --size 128 128 --frames 400 --no-movie`
- segmentation: matter > 0.65 of robust range [-1.0042, 0.5526], min area 6 px

## Measurements
- components: final 14, mean 11.0, max 16; occupancy final 0.03
- tracks: 86; persistent (alive >= 50% of run): 0; longest 181 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 0.00 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [14, 14, 14], H1 [1, 0, 0]
- motion: 50 long-lived tracks moved >= 1 body length; max speed 0.388/time; max body lengths 13.6
- replication (lineage window K = 20 frames = time 100, default): splits 34, persistent splits 18 (0 more failed only because the siblings re-merged within K), max generation 6, merges 10, merge/split ratio 0.294, nucleations 8
- channel total drift (end/start - 1): [-0.9596, -0.7763, None, 11.7811, -0.9972, -0.3391]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 42 at frame 296: holes 0, rim-vs-core 0.58, rim-vs-outside 0.35, heterogeneity 0.09; core [0.973, 0.842, 0.02, 0.417, 0.0, 1.0] rim [0.808, 0.564, 0.044, 0.894, 0.001, 1.0]
  - track 3 at frame 97: holes 0, rim-vs-core 0.61, rim-vs-outside 0.41, heterogeneity 0.11; core [0.981, 0.954, 0.017, 0.429, 0.039, 1.0] rim [0.809, 0.657, 0.038, 0.933, 0.101, 1.0]
  - track 40 at frame 266: holes 0, rim-vs-core 0.47, rim-vs-outside 0.40, heterogeneity 0.09; core [0.954, 0.935, 0.019, 0.398, 0.0, 1.0] rim [0.773, 0.659, 0.034, 0.734, 0.001, 1.0]
  - track 80 at frame 383: holes 0, rim-vs-core 0.67, rim-vs-outside 0.32, heterogeneity 0.12; core [0.977, 0.71, 0.225, 0.354, 0.005, 0.833] rim [0.821, 0.458, 0.55, 0.854, 0.012, 0.833]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 71 components >= 12 px at frames [67, 134, 202, 266, 333, 400]):
  - radial phi (droplet): peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.837, rim/outside 3.14 (aggregate of 71 individuals; 0/71 membrane-like individually; rim level 0.788)
  - radial order |Q|: peak at rho=0.25 (OUTSIDE the peak band 0.5-1.5), rim/core 0.774, rim/outside 9.88 (aggregate of 71 individuals; 0/71 membrane-like individually; rim level 0.644)
  - radial s0 (mar 20): peak at rho=0.85 (in the peak band 0.5-1.5), rim/core 1.49, rim/outside 2.45 (aggregate of 71 individuals; 32/71 membrane-like individually; rim level 0.107)
  - radial s1 (mar 40): peak at rho=0.55 (in the peak band 0.5-1.5), rim/core 1.39, rim/outside 3.41 (aggregate of 71 individuals; 43/71 membrane-like individually; rim level 0.6)
  - radial s2 (mar 60): peak at rho=0.75 (in the peak band 0.5-1.5), rim/core 1.67, rim/outside 1.61 (aggregate of 71 individuals; 12/71 membrane-like individually; rim level 0.0712)  MEMBRANE-LIKE
  - radial chemostat target phi_b(x,t): peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.984, rim/outside 1.01 (aggregate of 71 individuals; 0/71 membrane-like individually; rim level 0.934)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): s2 (mar 60)
- membrane-like channels per top track at mid-life: #42 (t=1480, R_eq 4.3): none; #3 (t=485, R_eq 3.74): ['s1 (mar 40)', 's2 (mar 60)']; #40 (t=1330, R_eq 3.91): ['s1 (mar 40)']; #80 (t=1915, R_eq 2.39): ['s0 (mar 20)', 's1 (mar 40)', 's2 (mar 60)']

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 1 of 71 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
