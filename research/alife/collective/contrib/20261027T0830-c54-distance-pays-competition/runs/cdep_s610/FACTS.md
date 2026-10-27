# Evidence pack: active-nematic-marangoni-distance-pays (seed 610)

- world: `../../../w2/world.py`, family `active-nematic`
- parent: collective/contrib/20261027T0000-c50-marangoni-spread-loop1/world.py; mutation: three heritable surfactant kinds with Marangoni coefficients 20/40/60 (majority-feedback production), in-run mutation between neighbouring kinds, trait-blind turnover
- run: 401 frames x 100 steps x dt 0.05 = time 2000; grid [128, 128]; wall 939s; status ok
- command: `python -m labkit.run /tmp/claude-0/c54/w2/world.py --out /tmp/claude-0/c54/runs/cdep/seed610 --seeds 610 --size 128 128 --frames 400 --no-movie`
- segmentation: matter > 0.65 of robust range [-0.9858, 0.5414], min area 6 px

## Measurements
- components: final 10, mean 12.2, max 19; occupancy final 0.03
- tracks: 96; persistent (alive >= 50% of run): 1; longest 202 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 11.33 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [10, 10, 10], H1 [0, 0, 0]
- motion: 61 long-lived tracks moved >= 1 body length; max speed 0.487/time; max body lengths 16.4
- replication (lineage window K = 20 frames = time 100, default): splits 38, persistent splits 21 (0 more failed only because the siblings re-merged within K), max generation 5, merges 14, merge/split ratio 0.368, nucleations 7
- channel total drift (end/start - 1): [-0.8432, -0.8263, None, 7.8356, 3.287, -0.2542]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 4 at frame 118: holes 0, rim-vs-core 0.46, rim-vs-outside 0.25, heterogeneity 0.10; core [0.95, 0.544, 0.028, 0.011, 0.567, 1.0] rim [0.805, 0.325, 0.047, 0.021, 0.939, 1.0]
  - track 13 at frame 128: holes 0, rim-vs-core 0.50, rim-vs-outside 0.33, heterogeneity 0.10; core [0.961, 0.694, 0.026, 0.004, 0.529, 1.0] rim [0.795, 0.446, 0.046, 0.009, 0.932, 1.0]
  - track 58 at frame 309: holes 0, rim-vs-core 0.55, rim-vs-outside 0.41, heterogeneity 0.10; core [0.977, 0.966, 0.066, 0.36, 0.006, 1.0] rim [0.794, 0.678, 0.134, 0.788, 0.014, 1.0]
  - track 80 at frame 353: holes 0, rim-vs-core 0.63, rim-vs-outside 0.37, heterogeneity 0.11; core [0.968, 0.81, 0.033, 0.013, 0.398, 0.833] rim [0.794, 0.44, 0.067, 0.024, 0.883, 0.833]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 78 components >= 12 px at frames [67, 134, 202, 266, 333, 400]):
  - radial phi (droplet): peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.847, rim/outside 3.24 (aggregate of 78 individuals; 0/78 membrane-like individually; rim level 0.801)
  - radial order |Q|: peak at rho=0.25 (OUTSIDE the peak band 0.5-1.5), rim/core 0.784, rim/outside 10.3 (aggregate of 78 individuals; 4/78 membrane-like individually; rim level 0.616)
  - radial s0 (mar 20): peak at rho=0.55 (in the peak band 0.5-1.5), rim/core 1.21, rim/outside 2.53 (aggregate of 78 individuals; 42/78 membrane-like individually; rim level 0.114)
  - radial s1 (mar 40): peak at rho=0.55 (in the peak band 0.5-1.5), rim/core 1.45, rim/outside 3.3 (aggregate of 78 individuals; 41/78 membrane-like individually; rim level 0.32)
  - radial s2 (mar 60): peak at rho=0.75 (in the peak band 0.5-1.5), rim/core 1.45, rim/outside 3.58 (aggregate of 78 individuals; 43/78 membrane-like individually; rim level 0.43)
  - radial chemostat target phi_b(x,t): peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.996, rim/outside 1.01 (aggregate of 78 individuals; 0/78 membrane-like individually; rim level 0.922)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #4 (t=590, R_eq 4.26, ring): ['order |Q|']; #13 (t=640, R_eq 4.11): none; #58 (t=1545, R_eq 3.48): ['s0 (mar 20)', 's1 (mar 40)']; #80 (t=1765, R_eq 2.99): ['s0 (mar 20)', 's1 (mar 40)', 's2 (mar 60)']

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 1 of 78 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
