# Evidence pack: active-nematic-marangoni-distance-pays (seed 621)

- world: `../../../w2/world.py`, family `active-nematic`
- parent: collective/contrib/20261027T0000-c50-marangoni-spread-loop1/world.py; mutation: three heritable surfactant kinds with Marangoni coefficients 20/40/60 (majority-feedback production), in-run mutation between neighbouring kinds, trait-blind turnover
- run: 401 frames x 100 steps x dt 0.05 = time 2000; grid [128, 128]; wall 969s; status ok
- command: `python -m labkit.run /tmp/claude-0/c54/w2/world.py --out /tmp/claude-0/c54/runs/m60dep/seed621 --seeds 621 --size 128 128 --frames 400 --no-movie`
- segmentation: matter > 0.66 of robust range [-0.9997, 0.5197], min area 6 px

## Measurements
- components: final 5, mean 10.3, max 21; occupancy final 0.01
- tracks: 105; persistent (alive >= 50% of run): 0; longest 179 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 0.00 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [5, 5, 5], H1 [0, 0, 0]
- motion: 63 long-lived tracks moved >= 1 body length; max speed 0.464/time; max body lengths 14.0
- replication (lineage window K = 20 frames = time 100, default): splits 39, persistent splits 25 (0 more failed only because the siblings re-merged within K), max generation 7, merges 14, merge/split ratio 0.359, nucleations 12
- channel total drift (end/start - 1): [-0.983, -0.9367, None, None, 2.133, -0.397]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 32 at frame 138: holes 0, rim-vs-core 0.35, rim-vs-outside 0.43, heterogeneity 0.09; core [0.964, 0.934, 0.059, 0.059, 0.473, 1.0] rim [0.838, 0.775, 0.092, 0.092, 0.76, 1.0]
  - track 66 at frame 289: holes 0, rim-vs-core 0.50, rim-vs-outside 0.42, heterogeneity 0.10; core [0.984, 0.943, 0.075, 0.075, 0.328, 1.0] rim [0.838, 0.674, 0.136, 0.136, 0.707, 1.0]
  - track 19 at frame 87: holes 0, rim-vs-core 0.52, rim-vs-outside 0.40, heterogeneity 0.10; core [0.965, 0.933, 0.056, 0.056, 0.544, 1.0] rim [0.806, 0.643, 0.098, 0.098, 0.935, 1.0]
  - track 92 at frame 380: holes 0, rim-vs-core 0.56, rim-vs-outside 0.39, heterogeneity 0.11; core [0.977, 0.87, 0.046, 0.046, 0.47, 0.914] rim [0.804, 0.582, 0.082, 0.082, 0.916, 0.917]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 59 components >= 12 px at frames [67, 134, 202, 266, 333, 400]):
  - radial phi (droplet): peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.851, rim/outside 2.99 (aggregate of 59 individuals; 0/59 membrane-like individually; rim level 0.805)
  - radial order |Q|: peak at rho=0.25 (OUTSIDE the peak band 0.5-1.5), rim/core 0.766, rim/outside 9.08 (aggregate of 59 individuals; 3/59 membrane-like individually; rim level 0.604)
  - radial s0 (mar 20): peak at rho=0.85 (in the peak band 0.5-1.5), rim/core 1.46, rim/outside 3.02 (aggregate of 59 individuals; 32/59 membrane-like individually; rim level 0.103)
  - radial s1 (mar 40): peak at rho=0.85 (in the peak band 0.5-1.5), rim/core 1.46, rim/outside 3.02 (aggregate of 59 individuals; 32/59 membrane-like individually; rim level 0.103)
  - radial s2 (mar 60): peak at rho=0.65 (in the peak band 0.5-1.5), rim/core 1.39, rim/outside 3.49 (aggregate of 59 individuals; 35/59 membrane-like individually; rim level 0.707)
  - radial chemostat target phi_b(x,t): peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 1.01, rim/outside 1.02 (aggregate of 59 individuals; 0/59 membrane-like individually; rim level 0.918)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #32 (t=690, R_eq 4.37): none; #66 (t=1445, R_eq 3.09): ['s0 (mar 20)', 's1 (mar 40)', 's2 (mar 60)']; #19 (t=435, R_eq 4.15): none; #92 (t=1900, R_eq 4.33): none

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
