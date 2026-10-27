# Evidence pack: active-nematic-marangoni-distance-pays (seed 602)

- world: `../../../../../../home/user/physim/research/alife/collective/contrib/20261027T0540-c54-distance-pays-loop1/world.py`, family `active-nematic`
- parent: collective/contrib/20261027T0000-c50-marangoni-spread-loop1/world.py; mutation: three heritable surfactant kinds with Marangoni coefficients 20/40/60 (majority-feedback production), in-run mutation between neighbouring kinds, trait-blind turnover
- run: 401 frames x 100 steps x dt 0.05 = time 2000; grid [128, 128]; wall 909s; status ok
- command: `python -m labkit.run collective/contrib/20261027T0540-c54-distance-pays-loop1/world.py --out /tmp/claude-0/c54/runs/glob/seed602 --seeds 602 --size 128 128 --frames 400 --no-movie`
- segmentation: matter > 0.65 of robust range [-1.0086, 0.5406], min area 6 px

## Measurements
- components: final 7, mean 7.7, max 14; occupancy final 0.02
- tracks: 57; persistent (alive >= 50% of run): 2; longest 234 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 11.14 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [7, 7, 7], H1 [1, 0, 0]
- motion: 40 long-lived tracks moved >= 1 body length; max speed 0.424/time; max body lengths 16.7
- replication (lineage window K = 20 frames = time 100, default): splits 25, persistent splits 21 (0 more failed only because the siblings re-merged within K), max generation 6, merges 5, merge/split ratio 0.2, nucleations 2
- channel total drift (end/start - 1): [-0.96, -0.8582, None, 0.7046, None, -0.3668]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 14 at frame 178: holes 0, rim-vs-core 0.59, rim-vs-outside 0.38, heterogeneity 0.10; core [0.975, 0.91, 0.001, 0.463, 0.0, 0.952] rim [0.801, 0.598, 0.002, 0.938, 0.001, 0.952]
  - track 11 at frame 158: holes 0, rim-vs-core 0.55, rim-vs-outside 0.37, heterogeneity 0.12; core [0.973, 0.803, 0.099, 0.542, 0.001, 0.952] rim [0.808, 0.56, 0.288, 0.973, 0.001, 0.952]
  - track 21 at frame 182: holes 0, rim-vs-core 0.57, rim-vs-outside 0.41, heterogeneity 0.10; core [0.981, 0.96, 0.029, 0.392, 0.0, 0.952] rim [0.811, 0.663, 0.075, 0.841, 0.0, 0.952]
  - track 46 at frame 383: holes 0, rim-vs-core 0.26, rim-vs-outside 0.42, heterogeneity 0.05; core [0.967, 0.914, 0.031, 0.006, 1.0, 0.964] rim [0.842, 0.691, 0.063, 0.011, 1.0, 0.964]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 51 components >= 12 px at frames [67, 134, 202, 266, 333, 400]):
  - radial phi (droplet): peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.852, rim/outside 3.02 (aggregate of 51 individuals; 0/51 membrane-like individually; rim level 0.788)
  - radial order |Q|: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.808, rim/outside 9.01 (aggregate of 51 individuals; 3/51 membrane-like individually; rim level 0.645)
  - radial s0 (mar 20): peak at rho=0.25 (OUTSIDE the peak band 0.5-1.5), rim/core 1.23, rim/outside 1.66 (aggregate of 51 individuals; 10/51 membrane-like individually; rim level 0.142)
  - radial s1 (mar 40): peak at rho=0.55 (in the peak band 0.5-1.5), rim/core 1.22, rim/outside 3.28 (aggregate of 51 individuals; 27/51 membrane-like individually; rim level 0.558)
  - radial s2 (mar 60): peak at rho=0.75 (in the peak band 0.5-1.5), rim/core 1.33, rim/outside 1.52 (aggregate of 51 individuals; 9/51 membrane-like individually; rim level 0.129)
  - radial chemostat target phi_b(x,t): peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.996, rim/outside 1.05 (aggregate of 51 individuals; 0/51 membrane-like individually; rim level 0.964)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #14 (t=890, R_eq 4.18): ['s1 (mar 40)']; #11 (t=790, R_eq 4.15): ['s0 (mar 20)']; #21 (t=910, R_eq 3.43): ['s0 (mar 20)', 's1 (mar 40)']; #46 (t=1915, R_eq 3.57): ['s0 (mar 20)']

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 2 of 51 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
