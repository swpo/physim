# Evidence pack: active-nematic-marangoni-distance-pays (seed 600)

- world: `../../../../../../home/user/physim/research/alife/collective/contrib/20261027T0540-c54-distance-pays-loop1/world.py`, family `active-nematic`
- parent: collective/contrib/20261027T0000-c50-marangoni-spread-loop1/world.py; mutation: three heritable surfactant kinds with Marangoni coefficients 20/40/60 (majority-feedback production), in-run mutation between neighbouring kinds, trait-blind turnover
- run: 401 frames x 100 steps x dt 0.05 = time 2000; grid [128, 128]; wall 867s; status ok
- command: `python -m labkit.run collective/contrib/20261027T0540-c54-distance-pays-loop1/world.py --out /tmp/claude-0/c54/runs/twin/seed600 --seeds 600 --size 128 128 --frames 400 --no-movie`
- segmentation: matter > 0.64 of robust range [-1.0027, 0.5523], min area 6 px

## Measurements
- components: final 8, mean 9.9, max 15; occupancy final 0.02
- tracks: 77; persistent (alive >= 50% of run): 0; longest 195 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 0.00 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [8, 8, 8], H1 [0, 0, 0]
- motion: 45 long-lived tracks moved >= 1 body length; max speed 0.432/time; max body lengths 9.6
- replication (lineage window K = 20 frames = time 100, default): splits 33, persistent splits 21 (0 more failed only because the siblings re-merged within K), max generation 6, merges 6, merge/split ratio 0.182, nucleations 5
- channel total drift (end/start - 1): [-0.8601, -0.9015, None, 2.2068, None, -0.2229]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 21 at frame 192: holes 0, rim-vs-core 0.60, rim-vs-outside 0.39, heterogeneity 0.10; core [0.977, 0.887, 0.004, 0.428, 0.0, 1.0] rim [0.806, 0.59, 0.01, 0.922, 0.0, 1.0]
  - track 27 at frame 242: holes 0, rim-vs-core 0.67, rim-vs-outside 0.40, heterogeneity 0.11; core [0.975, 0.927, 0.005, 0.421, 0.0, 1.0] rim [0.771, 0.546, 0.01, 0.931, 0.0, 1.0]
  - track 29 at frame 222: holes 0, rim-vs-core 0.62, rim-vs-outside 0.41, heterogeneity 0.10; core [0.978, 0.941, 0.003, 0.389, 0.0, 1.0] rim [0.788, 0.597, 0.007, 0.867, 0.0, 1.0]
  - track 71 at frame 387: holes 0, rim-vs-core 0.70, rim-vs-outside 0.39, heterogeneity 0.11; core [0.997, 0.932, 0.003, 0.26, 0.098, 0.833] rim [0.835, 0.547, 0.007, 0.764, 0.336, 0.833]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 62 components >= 12 px at frames [67, 134, 202, 266, 333, 400]):
  - radial phi (droplet): peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.85, rim/outside 3.18 (aggregate of 62 individuals; 0/62 membrane-like individually; rim level 0.807)
  - radial order |Q|: peak at rho=0.25 (OUTSIDE the peak band 0.5-1.5), rim/core 0.83, rim/outside 9.9 (aggregate of 62 individuals; 5/62 membrane-like individually; rim level 0.626)
  - radial s0 (mar 20): peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 1.22, rim/outside 2.08 (aggregate of 62 individuals; 13/62 membrane-like individually; rim level 0.0881)
  - radial s1 (mar 40): peak at rho=0.65 (in the peak band 0.5-1.5), rim/core 1.45, rim/outside 3.82 (aggregate of 62 individuals; 40/62 membrane-like individually; rim level 0.613)
  - radial s2 (mar 60): peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 1.42, rim/outside 1.89 (aggregate of 62 individuals; 11/62 membrane-like individually; rim level 0.128)
  - radial chemostat target phi_b(x,t): peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.988, rim/outside 1.04 (aggregate of 62 individuals; 0/62 membrane-like individually; rim level 0.936)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #21 (t=960, R_eq 4.11): none; #27 (t=1210, R_eq 3.34): ['s1 (mar 40)']; #29 (t=1110, R_eq 3.34): ['s1 (mar 40)']; #71 (t=1935, R_eq 2.65): ['s1 (mar 40)', 's2 (mar 60)']

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 1 of 62 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
