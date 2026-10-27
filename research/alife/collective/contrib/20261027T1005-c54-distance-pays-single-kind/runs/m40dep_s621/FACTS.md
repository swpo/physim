# Evidence pack: active-nematic-marangoni-distance-pays (seed 621)

- world: `../../../w2/world.py`, family `active-nematic`
- parent: collective/contrib/20261027T0000-c50-marangoni-spread-loop1/world.py; mutation: three heritable surfactant kinds with Marangoni coefficients 20/40/60 (majority-feedback production), in-run mutation between neighbouring kinds, trait-blind turnover
- run: 401 frames x 100 steps x dt 0.05 = time 2000; grid [128, 128]; wall 973s; status ok
- command: `python -m labkit.run /tmp/claude-0/c54/w2/world.py --out /tmp/claude-0/c54/runs/m40dep/seed621 --seeds 621 --size 128 128 --frames 400 --no-movie`
- segmentation: matter > 0.64 of robust range [-1.0016, 0.5575], min area 6 px

## Measurements
- components: final 8, mean 11.9, max 22; occupancy final 0.02
- tracks: 96; persistent (alive >= 50% of run): 0; longest 194 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 0.00 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [9, 9, 8], H1 [0, 0, 0]
- motion: 57 long-lived tracks moved >= 1 body length; max speed 0.481/time; max body lengths 13.1
- replication (lineage window K = 20 frames = time 100, default): splits 37, persistent splits 24 (0 more failed only because the siblings re-merged within K), max generation 5, merges 10, merge/split ratio 0.27, nucleations 12
- channel total drift (end/start - 1): [-0.978, -0.8747, None, 3.5944, None, -0.3981]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 43 at frame 245: holes 0, rim-vs-core 0.56, rim-vs-outside 0.44, heterogeneity 0.09; core [0.993, 0.976, 0.041, 0.21, 0.041, 1.0] rim [0.833, 0.68, 0.108, 0.641, 0.108, 1.0]
  - track 42 at frame 225: holes 0, rim-vs-core 0.61, rim-vs-outside 0.33, heterogeneity 0.11; core [0.965, 0.828, 0.05, 0.507, 0.05, 1.0] rim [0.777, 0.512, 0.103, 0.981, 0.103, 1.0]
  - track 19 at frame 101: holes 0, rim-vs-core 0.54, rim-vs-outside 0.40, heterogeneity 0.09; core [0.968, 0.945, 0.032, 0.375, 0.032, 1.0] rim [0.781, 0.649, 0.06, 0.781, 0.06, 1.0]
  - track 88 at frame 376: holes 0, rim-vs-core 0.57, rim-vs-outside 0.40, heterogeneity 0.09; core [0.98, 0.926, 0.032, 0.28, 0.032, 0.833] rim [0.822, 0.618, 0.072, 0.728, 0.072, 0.833]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 71 components >= 12 px at frames [67, 134, 202, 266, 333, 400]):
  - radial phi (droplet): peak at rho=0.25 (OUTSIDE the peak band 0.5-1.5), rim/core 0.855, rim/outside 3.15 (aggregate of 71 individuals; 0/71 membrane-like individually; rim level 0.803)
  - radial order |Q|: peak at rho=0.25 (OUTSIDE the peak band 0.5-1.5), rim/core 0.785, rim/outside 9.66 (aggregate of 71 individuals; 3/71 membrane-like individually; rim level 0.611)
  - radial s0 (mar 20): peak at rho=0.75 (in the peak band 0.5-1.5), rim/core 1.62, rim/outside 2.73 (aggregate of 71 individuals; 43/71 membrane-like individually; rim level 0.109)  MEMBRANE-LIKE
  - radial s1 (mar 40): peak at rho=0.85 (in the peak band 0.5-1.5), rim/core 1.5, rim/outside 3.58 (aggregate of 71 individuals; 46/71 membrane-like individually; rim level 0.669)  MEMBRANE-LIKE
  - radial s2 (mar 60): peak at rho=0.75 (in the peak band 0.5-1.5), rim/core 1.62, rim/outside 2.73 (aggregate of 71 individuals; 43/71 membrane-like individually; rim level 0.109)  MEMBRANE-LIKE
  - radial chemostat target phi_b(x,t): peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.992, rim/outside 1.01 (aggregate of 71 individuals; 0/71 membrane-like individually; rim level 0.916)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): s0 (mar 20), s1 (mar 40), s2 (mar 60)
- membrane-like channels per top track at mid-life: #43 (t=1225, R_eq 3.14): ['s0 (mar 20)', 's1 (mar 40)', 's2 (mar 60)']; #42 (t=1125, R_eq 4.11): none; #19 (t=505, R_eq 3.74): ['s1 (mar 40)']; #88 (t=1880, R_eq 2.99): ['s0 (mar 20)', 's1 (mar 40)', 's2 (mar 60)']

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 1 of 71 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
