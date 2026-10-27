# Evidence pack: active-nematic-marangoni-distance-pays (seed 601)

- world: `../../../../../../home/user/physim/research/alife/collective/contrib/20261027T0540-c54-distance-pays-loop1/world.py`, family `active-nematic`
- parent: collective/contrib/20261027T0000-c50-marangoni-spread-loop1/world.py; mutation: three heritable surfactant kinds with Marangoni coefficients 20/40/60 (majority-feedback production), in-run mutation between neighbouring kinds, trait-blind turnover
- run: 401 frames x 100 steps x dt 0.05 = time 2000; grid [128, 128]; wall 904s; status ok
- command: `python -m labkit.run collective/contrib/20261027T0540-c54-distance-pays-loop1/world.py --out /tmp/claude-0/c54/runs/twin/seed601 --seeds 601 --size 128 128 --frames 400 --no-movie`
- segmentation: matter > 0.64 of robust range [-1.0038, 0.5547], min area 6 px

## Measurements
- components: final 14, mean 10.1, max 21; occupancy final 0.03
- tracks: 83; persistent (alive >= 50% of run): 2; longest 208 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 3.46 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [14, 14, 14], H1 [0, 0, 0]
- motion: 48 long-lived tracks moved >= 1 body length; max speed 0.448/time; max body lengths 14.4
- replication (lineage window K = 20 frames = time 100, default): splits 34, persistent splits 21 (0 more failed only because the siblings re-merged within K), max generation 4, merges 2, merge/split ratio 0.059, nucleations 12
- channel total drift (end/start - 1): [-0.6384, -0.7525, None, 2.9516, None, -0.1444]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 41 at frame 276: holes 0, rim-vs-core 0.64, rim-vs-outside 0.37, heterogeneity 0.15; core [0.985, 0.793, 0.006, 0.432, 0.292, 1.0] rim [0.799, 0.541, 0.015, 0.983, 0.357, 1.0]
  - track 43 at frame 282: holes 0, rim-vs-core 0.28, rim-vs-outside 0.32, heterogeneity 0.06; core [0.981, 0.711, 0.008, 0.011, 1.0, 1.0] rim [0.801, 0.492, 0.02, 0.027, 1.0, 1.0]
  - track 48 at frame 299: holes 0, rim-vs-core 0.60, rim-vs-outside 0.31, heterogeneity 0.13; core [0.98, 0.651, 0.004, 0.45, 0.107, 1.0] rim [0.803, 0.415, 0.009, 0.949, 0.247, 1.0]
  - track 61 at frame 306: holes 0, rim-vs-core 0.69, rim-vs-outside 0.39, heterogeneity 0.11; core [0.988, 0.937, 0.003, 0.4, 0.019, 0.833] rim [0.793, 0.521, 0.008, 0.918, 0.05, 0.833]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 63 components >= 12 px at frames [67, 134, 202, 266, 333, 400]):
  - radial phi (droplet): peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.846, rim/outside 3.11 (aggregate of 63 individuals; 0/63 membrane-like individually; rim level 0.787)
  - radial order |Q|: peak at rho=0.25 (OUTSIDE the peak band 0.5-1.5), rim/core 0.79, rim/outside 9.27 (aggregate of 63 individuals; 1/63 membrane-like individually; rim level 0.628)
  - radial s0 (mar 20): peak at rho=0.65 (in the peak band 0.5-1.5), rim/core 1.38, rim/outside 2.82 (aggregate of 63 individuals; 17/63 membrane-like individually; rim level 0.182)
  - radial s1 (mar 40): peak at rho=0.65 (in the peak band 0.5-1.5), rim/core 1.38, rim/outside 3.42 (aggregate of 63 individuals; 34/63 membrane-like individually; rim level 0.516)
  - radial s2 (mar 60): peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 1.07, rim/outside 1.57 (aggregate of 63 individuals; 8/63 membrane-like individually; rim level 0.0738)
  - radial chemostat target phi_b(x,t): peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.99, rim/outside 1.03 (aggregate of 63 individuals; 0/63 membrane-like individually; rim level 0.937)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #41 (t=1380, R_eq 4.85): none; #43 (t=1410, R_eq 4.44): none; #48 (t=1495, R_eq 4.11): ['s2 (mar 60)']; #61 (t=1530, R_eq 3.09): ['s0 (mar 20)', 's1 (mar 40)', 's2 (mar 60)']

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 2 of 63 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
