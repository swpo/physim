# Evidence pack: active-nematic-marangoni-distance-pays (seed 600)

- world: `../../../../../../home/user/physim/research/alife/collective/contrib/20261027T0540-c54-distance-pays-loop1/world.py`, family `active-nematic`
- parent: collective/contrib/20261027T0000-c50-marangoni-spread-loop1/world.py; mutation: three heritable surfactant kinds with Marangoni coefficients 20/40/60 (majority-feedback production), in-run mutation between neighbouring kinds, trait-blind turnover
- run: 401 frames x 100 steps x dt 0.05 = time 2000; grid [128, 128]; wall 846s; status ok
- command: `python -m labkit.run collective/contrib/20261027T0540-c54-distance-pays-loop1/world.py --out /tmp/claude-0/c54/runs/dep07/seed600 --seeds 600 --size 128 128 --frames 400 --no-movie`
- segmentation: matter > 0.64 of robust range [-1.0042, 0.564], min area 6 px

## Measurements
- components: final 7, mean 10.1, max 16; occupancy final 0.02
- tracks: 78; persistent (alive >= 50% of run): 0; longest 171 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 0.00 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [8, 7, 7], H1 [0, 0, 0]
- motion: 53 long-lived tracks moved >= 1 body length; max speed 0.362/time; max body lengths 14.1
- replication (lineage window K = 20 frames = time 100, default): splits 31, persistent splits 22 (0 more failed only because the siblings re-merged within K), max generation 5, merges 10, merge/split ratio 0.323, nucleations 5
- channel total drift (end/start - 1): [-0.8483, -0.8621, None, 0.4044, None, -0.1929]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 50 at frame 316: holes 0, rim-vs-core 0.50, rim-vs-outside 0.36, heterogeneity 0.10; core [0.963, 0.877, 0.606, 0.015, 0.058, 1.0] rim [0.793, 0.606, 0.988, 0.03, 0.129, 1.0]
  - track 33 at frame 245: holes 0, rim-vs-core 0.50, rim-vs-outside 0.38, heterogeneity 0.12; core [0.971, 0.802, 0.019, 0.519, 0.04, 1.0] rim [0.815, 0.533, 0.039, 0.909, 0.105, 1.0]
  - track 49 at frame 306: holes 0, rim-vs-core 0.64, rim-vs-outside 0.40, heterogeneity 0.11; core [0.985, 0.97, 0.416, 0.022, 0.002, 1.0] rim [0.815, 0.696, 0.964, 0.071, 0.007, 1.0]
  - track 73 at frame 376: holes 0, rim-vs-core 0.63, rim-vs-outside 0.38, heterogeneity 0.11; core [0.978, 0.932, 0.008, 0.415, 0.002, 0.911] rim [0.81, 0.604, 0.02, 0.923, 0.004, 0.917]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 59 components >= 12 px at frames [67, 134, 202, 266, 333, 400]):
  - radial phi (droplet): peak at rho=0.25 (OUTSIDE the peak band 0.5-1.5), rim/core 0.851, rim/outside 3.05 (aggregate of 59 individuals; 0/59 membrane-like individually; rim level 0.787)
  - radial order |Q|: peak at rho=0.25 (OUTSIDE the peak band 0.5-1.5), rim/core 0.802, rim/outside 8.68 (aggregate of 59 individuals; 2/59 membrane-like individually; rim level 0.603)
  - radial s0 (mar 20): peak at rho=0.45 (OUTSIDE the peak band 0.5-1.5), rim/core 1.38, rim/outside 3.13 (aggregate of 59 individuals; 16/59 membrane-like individually; rim level 0.177)
  - radial s1 (mar 40): peak at rho=0.75 (in the peak band 0.5-1.5), rim/core 1.43, rim/outside 3.59 (aggregate of 59 individuals; 30/59 membrane-like individually; rim level 0.493)
  - radial s2 (mar 60): peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.867, rim/outside 1.7 (aggregate of 59 individuals; 11/59 membrane-like individually; rim level 0.102)
  - radial chemostat target phi_b(x,t): peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.994, rim/outside 1.03 (aggregate of 59 individuals; 0/59 membrane-like individually; rim level 0.953)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #50 (t=1580, R_eq 4.65): none; #33 (t=1225, R_eq 4.79): none; #49 (t=1530, R_eq 3.39): ['s0 (mar 20)', 's1 (mar 40)']; #73 (t=1880, R_eq 3.24): ['s0 (mar 20)', 's1 (mar 40)']

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 2 of 59 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
