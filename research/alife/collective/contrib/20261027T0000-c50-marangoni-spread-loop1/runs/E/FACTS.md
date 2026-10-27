# Evidence pack: active-nematic-marangoni-spread (seed 500)

- world: `../../../world.py`, family `active-nematic`
- parent: collective/contrib/20261026T0505-c34-nematic-marangoni/world.py; mutation: three heritable surfactant kinds with Marangoni coefficients 20/40/60 (majority-feedback production), in-run mutation between neighbouring kinds, trait-blind turnover
- run: 401 frames x 100 steps x dt 0.05 = time 2000; grid [128, 128]; wall 752s; status ok
- command: `python -m labkit.run /tmp/claude-0/sp/world.py --out /tmp/claude-0/sp/runs/E/seed500 --seeds 500 --size 128 128 --frames 400 --no-movie`
- segmentation: matter > 0.64 of robust range [-1.0052, 0.5602], min area 6 px

## Measurements
- components: final 7, mean 15.3, max 22; occupancy final 0.02
- tracks: 160; persistent (alive >= 50% of run): 1; longest 212 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 2.69 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [8, 7, 7], H1 [0, 0, 0]
- motion: 85 long-lived tracks moved >= 1 body length; max speed 0.38/time; max body lengths 9.0
- replication (lineage window K = 20 frames = time 100, default): splits 61, persistent splits 31 (0 more failed only because the siblings re-merged within K), max generation 8, merges 31, merge/split ratio 0.508, nucleations 8
- channel total drift (end/start - 1): [-0.8195, -0.8495, None, 3.0082, None, -0.2133]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 14 at frame 134: holes 0, rim-vs-core 0.74, rim-vs-outside 0.40, heterogeneity 0.12; core [0.985, 0.959, 0.001, 0.329, 0.002, 1.0] rim [0.791, 0.589, 0.004, 0.94, 0.003, 1.0]
  - track 93 at frame 306: holes 0, rim-vs-core 0.29, rim-vs-outside 0.27, heterogeneity 0.08; core [0.939, 0.43, 0.001, 0.026, 0.77, 1.0] rim [0.797, 0.255, 0.001, 0.049, 0.952, 1.0]
  - track 96 at frame 306: holes 0, rim-vs-core 0.58, rim-vs-outside 0.30, heterogeneity 0.10; core [0.961, 0.64, 0.0, 0.427, 0.027, 1.0] rim [0.764, 0.372, 0.001, 0.903, 0.063, 1.0]
  - track 146 at frame 370: holes 0, rim-vs-core 0.41, rim-vs-outside 0.42, heterogeneity 0.10; core [0.962, 0.711, 0.002, 0.411, 0.019, 1.0] rim [0.821, 0.589, 0.005, 0.78, 0.034, 1.0]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 96 components >= 12 px at frames [67, 134, 202, 266, 333, 400]):
  - radial phi (droplet): peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.825, rim/outside 3.06 (aggregate of 96 individuals; 0/96 membrane-like individually; rim level 0.76)
  - radial order |Q|: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.773, rim/outside 9.07 (aggregate of 96 individuals; 3/96 membrane-like individually; rim level 0.567)
  - radial s0 (mar 20): peak at rho=0.75 (in the peak band 0.5-1.5), rim/core 1.66, rim/outside 2.67 (aggregate of 96 individuals; 18/96 membrane-like individually; rim level 0.0964)  MEMBRANE-LIKE
  - radial s1 (mar 40): peak at rho=0.55 (in the peak band 0.5-1.5), rim/core 1.29, rim/outside 3.29 (aggregate of 96 individuals; 49/96 membrane-like individually; rim level 0.499)
  - radial s2 (mar 60): peak at rho=0.55 (in the peak band 0.5-1.5), rim/core 1.31, rim/outside 2.81 (aggregate of 96 individuals; 16/96 membrane-like individually; rim level 0.11)
  - radial chemostat target phi_b(x,t): peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.998, rim/outside 1.02 (aggregate of 96 individuals; 0/96 membrane-like individually; rim level 0.998)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): s0 (mar 20)
- membrane-like channels per top track at mid-life: #14 (t=670, R_eq 4.58): ['s1 (mar 40)']; #93 (t=1530, R_eq 3.95): none; #96 (t=1530, R_eq 3.95): ['s1 (mar 40)', 's2 (mar 60)']; #146 (t=1850, R_eq 4.22): none

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 2 of 96 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
