# Evidence pack: active-nematic-marangoni-distance-pays (seed 602)

- world: `../../../../../../home/user/physim/research/alife/collective/contrib/20261027T0540-c54-distance-pays-loop1/world.py`, family `active-nematic`
- parent: collective/contrib/20261027T0000-c50-marangoni-spread-loop1/world.py; mutation: three heritable surfactant kinds with Marangoni coefficients 20/40/60 (majority-feedback production), in-run mutation between neighbouring kinds, trait-blind turnover
- run: 401 frames x 100 steps x dt 0.05 = time 2000; grid [128, 128]; wall 899s; status ok
- command: `python -m labkit.run collective/contrib/20261027T0540-c54-distance-pays-loop1/world.py --out /tmp/claude-0/c54/runs/twin/seed602 --seeds 602 --size 128 128 --frames 400 --no-movie`
- segmentation: matter > 0.65 of robust range [-1.0033, 0.5433], min area 6 px

## Measurements
- components: final 7, mean 7.9, max 14; occupancy final 0.02
- tracks: 61; persistent (alive >= 50% of run): 1; longest 286 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 6.50 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [8, 7, 7], H1 [1, 0, 0]
- motion: 48 long-lived tracks moved >= 1 body length; max speed 0.533/time; max body lengths 12.7
- replication (lineage window K = 20 frames = time 100, default): splits 28, persistent splits 21 (0 more failed only because the siblings re-merged within K), max generation 7, merges 3, merge/split ratio 0.107, nucleations 2
- channel total drift (end/start - 1): [-0.9447, -0.8923, None, 2.4861, None, -0.3357]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 17 at frame 222: holes 0, rim-vs-core 0.61, rim-vs-outside 0.35, heterogeneity 0.10; core [0.987, 0.809, 0.016, 0.424, 0.005, 1.0] rim [0.819, 0.523, 0.045, 0.938, 0.015, 1.0]
  - track 25 at frame 222: holes 0, rim-vs-core 0.47, rim-vs-outside 0.34, heterogeneity 0.12; core [0.996, 0.493, 0.132, 0.019, 0.614, 1.0] rim [0.861, 0.333, 0.405, 0.045, 0.932, 1.0]
  - track 23 at frame 212: holes 0, rim-vs-core 0.70, rim-vs-outside 0.40, heterogeneity 0.12; core [0.991, 0.943, 0.006, 0.337, 0.08, 1.0] rim [0.836, 0.555, 0.019, 0.877, 0.229, 1.0]
  - track 55 at frame 383: holes 0, rim-vs-core 0.54, rim-vs-outside 0.42, heterogeneity 0.10; core [0.981, 0.966, 0.0, 0.452, 0.001, 0.986] rim [0.823, 0.727, 0.0, 0.914, 0.003, 0.97]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 48 components >= 12 px at frames [67, 134, 202, 266, 333, 400]):
  - radial phi (droplet): peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.868, rim/outside 3.04 (aggregate of 48 individuals; 0/48 membrane-like individually; rim level 0.799)
  - radial order |Q|: peak at rho=0.25 (OUTSIDE the peak band 0.5-1.5), rim/core 0.829, rim/outside 8.34 (aggregate of 48 individuals; 4/48 membrane-like individually; rim level 0.62)
  - radial s0 (mar 20): peak at rho=0.35 (OUTSIDE the peak band 0.5-1.5), rim/core 1.25, rim/outside 1.41 (aggregate of 48 individuals; 11/48 membrane-like individually; rim level 0.0846)
  - radial s1 (mar 40): peak at rho=0.85 (in the peak band 0.5-1.5), rim/core 1.3, rim/outside 3.52 (aggregate of 48 individuals; 26/48 membrane-like individually; rim level 0.54)
  - radial s2 (mar 60): peak at rho=0.65 (in the peak band 0.5-1.5), rim/core 1.43, rim/outside 2.31 (aggregate of 48 individuals; 16/48 membrane-like individually; rim level 0.173)
  - radial chemostat target phi_b(x,t): peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 1, rim/outside 1.05 (aggregate of 48 individuals; 0/48 membrane-like individually; rim level 0.959)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #17 (t=1110, R_eq 4.33): none; #25 (t=1110, R_eq 2.59): ['s0 (mar 20)', 's1 (mar 40)', 's2 (mar 60)']; #23 (t=1060, R_eq 2.65): ['s0 (mar 20)', 's1 (mar 40)', 's2 (mar 60)']; #55 (t=1915, R_eq 4.07): none

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 2 of 48 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
