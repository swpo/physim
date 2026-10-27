# Evidence pack: active-nematic-marangoni-distance-pays (seed 611)

- world: `../../../w2/world.py`, family `active-nematic`
- parent: collective/contrib/20261027T0000-c50-marangoni-spread-loop1/world.py; mutation: three heritable surfactant kinds with Marangoni coefficients 20/40/60 (majority-feedback production), in-run mutation between neighbouring kinds, trait-blind turnover
- run: 401 frames x 100 steps x dt 0.05 = time 2000; grid [128, 128]; wall 970s; status ok
- command: `python -m labkit.run /tmp/claude-0/c54/w2/world.py --out /tmp/claude-0/c54/runs/cE/seed611 --seeds 611 --size 128 128 --frames 400 --no-movie`
- segmentation: matter > 0.65 of robust range [-1.0016, 0.5498], min area 6 px

## Measurements
- components: final 13, mean 14.2, max 23; occupancy final 0.04
- tracks: 175; persistent (alive >= 50% of run): 0; longest 172 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 0.00 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [14, 13, 13], H1 [1, 0, 0]
- motion: 89 long-lived tracks moved >= 1 body length; max speed 0.507/time; max body lengths 15.2
- replication (lineage window K = 20 frames = time 100, default): splits 66, persistent splits 30 (0 more failed only because the siblings re-merged within K), max generation 6, merges 33, merge/split ratio 0.5, nucleations 8
- channel total drift (end/start - 1): [-0.9183, -0.7741, None, 11.4189, 4.3681, -0.3088]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 84 at frame 309: holes 0, rim-vs-core 0.60, rim-vs-outside 0.40, heterogeneity 0.10; core [0.969, 0.928, 0.037, 0.423, 0.006, 1.0] rim [0.799, 0.641, 0.083, 0.919, 0.016, 1.0]
  - track 85 at frame 296: holes 0, rim-vs-core 0.51, rim-vs-outside 0.30, heterogeneity 0.09; core [0.944, 0.621, 0.032, 0.518, 0.007, 1.0] rim [0.775, 0.411, 0.063, 0.947, 0.015, 1.0]
  - track 34 at frame 131: holes 0, rim-vs-core 0.52, rim-vs-outside 0.35, heterogeneity 0.09; core [0.956, 0.898, 0.016, 0.374, 0.003, 1.0] rim [0.778, 0.589, 0.031, 0.748, 0.006, 1.0]
  - track 127 at frame 323: holes 0, rim-vs-core 0.63, rim-vs-outside 0.32, heterogeneity 0.11; core [0.956, 0.747, 0.025, 0.028, 0.538, 1.0] rim [0.762, 0.351, 0.051, 0.067, 0.992, 1.0]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 86 components >= 12 px at frames [67, 134, 202, 266, 333, 400]):
  - radial phi (droplet): peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.824, rim/outside 2.88 (aggregate of 86 individuals; 0/86 membrane-like individually; rim level 0.74)
  - radial order |Q|: peak at rho=0.25 (OUTSIDE the peak band 0.5-1.5), rim/core 0.785, rim/outside 7.77 (aggregate of 86 individuals; 5/86 membrane-like individually; rim level 0.533)
  - radial s0 (mar 20): peak at rho=0.65 (in the peak band 0.5-1.5), rim/core 1.24, rim/outside 1.8 (aggregate of 86 individuals; 26/86 membrane-like individually; rim level 0.0637)
  - radial s1 (mar 40): peak at rho=0.65 (in the peak band 0.5-1.5), rim/core 1.18, rim/outside 3.18 (aggregate of 86 individuals; 40/86 membrane-like individually; rim level 0.501)
  - radial s2 (mar 60): peak at rho=0.45 (OUTSIDE the peak band 0.5-1.5), rim/core 1.37, rim/outside 3.02 (aggregate of 86 individuals; 22/86 membrane-like individually; rim level 0.164)
  - radial chemostat target phi_b(x,t): peak at rho=1.75 (OUTSIDE the peak band 0.5-1.5), rim/core 1, rim/outside 0.997 (aggregate of 86 individuals; 0/86 membrane-like individually; rim level 0.988)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #84 (t=1545, R_eq 3.78): ['s0 (mar 20)', 's1 (mar 40)']; #85 (t=1480, R_eq 4.55): none; #34 (t=655, R_eq 3.57): ['s1 (mar 40)']; #127 (t=1615, R_eq 2.99): ['s0 (mar 20)', 's1 (mar 40)', 's2 (mar 60)']

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 3 of 86 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
