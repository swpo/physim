# Evidence pack: active-nematic-marangoni-distance-pays (seed 610)

- world: `../../../w2/world.py`, family `active-nematic`
- parent: collective/contrib/20261027T0000-c50-marangoni-spread-loop1/world.py; mutation: three heritable surfactant kinds with Marangoni coefficients 20/40/60 (majority-feedback production), in-run mutation between neighbouring kinds, trait-blind turnover
- run: 401 frames x 100 steps x dt 0.05 = time 2000; grid [128, 128]; wall 933s; status ok
- command: `python -m labkit.run /tmp/claude-0/c54/w2/world.py --out /tmp/claude-0/c54/runs/cdeptwin/seed610 --seeds 610 --size 128 128 --frames 400 --no-movie`
- segmentation: matter > 0.64 of robust range [-0.9892, 0.5595], min area 6 px

## Measurements
- components: final 8, mean 12.9, max 22; occupancy final 0.02
- tracks: 83; persistent (alive >= 50% of run): 2; longest 269 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 4.00 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [8, 8, 8], H1 [0, 0, 0]
- motion: 57 long-lived tracks moved >= 1 body length; max speed 0.23/time; max body lengths 16.4
- replication (lineage window K = 20 frames = time 100, default): splits 34, persistent splits 21 (0 more failed only because the siblings re-merged within K), max generation 4, merges 6, merge/split ratio 0.176, nucleations 9
- channel total drift (end/start - 1): [-0.8698, -0.876, None, 1.1146, 5.8516, -0.2652]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 23 at frame 188: holes 0, rim-vs-core 0.68, rim-vs-outside 0.36, heterogeneity 0.11; core [0.97, 0.876, 0.047, 0.002, 0.407, 0.833] rim [0.755, 0.446, 0.097, 0.004, 0.891, 0.833]
  - track 36 at frame 249: holes 0, rim-vs-core 0.52, rim-vs-outside 0.31, heterogeneity 0.11; core [0.956, 0.635, 0.012, 0.001, 0.459, 0.971] rim [0.781, 0.437, 0.023, 0.001, 0.904, 0.961]
  - track 13 at frame 128: holes 0, rim-vs-core 0.48, rim-vs-outside 0.37, heterogeneity 0.09; core [0.952, 0.855, 0.026, 0.007, 0.408, 1.0] rim [0.789, 0.603, 0.052, 0.015, 0.78, 1.0]
  - track 42 at frame 225: holes 0, rim-vs-core 0.55, rim-vs-outside 0.41, heterogeneity 0.09; core [0.981, 0.953, 0.02, 0.0, 0.308, 1.0] rim [0.809, 0.667, 0.046, 0.001, 0.742, 1.0]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 80 components >= 12 px at frames [67, 134, 202, 266, 333, 400]):
  - radial phi (droplet): peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.828, rim/outside 3.24 (aggregate of 80 individuals; 0/80 membrane-like individually; rim level 0.778)
  - radial order |Q|: peak at rho=0.25 (OUTSIDE the peak band 0.5-1.5), rim/core 0.759, rim/outside 9.8 (aggregate of 80 individuals; 3/80 membrane-like individually; rim level 0.606)
  - radial s0 (mar 20): peak at rho=0.75 (in the peak band 0.5-1.5), rim/core 1.24, rim/outside 2.8 (aggregate of 80 individuals; 45/80 membrane-like individually; rim level 0.089)
  - radial s1 (mar 40): peak at rho=0.65 (in the peak band 0.5-1.5), rim/core 1.28, rim/outside 2.87 (aggregate of 80 individuals; 31/80 membrane-like individually; rim level 0.129)
  - radial s2 (mar 60): peak at rho=0.65 (in the peak band 0.5-1.5), rim/core 1.51, rim/outside 3.66 (aggregate of 80 individuals; 51/80 membrane-like individually; rim level 0.589)  MEMBRANE-LIKE
  - radial chemostat target phi_b(x,t): peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.984, rim/outside 1.01 (aggregate of 80 individuals; 0/80 membrane-like individually; rim level 0.93)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): s2 (mar 60)
- membrane-like channels per top track at mid-life: #23 (t=940, R_eq 3.09): ['s0 (mar 20)', 's2 (mar 60)']; #36 (t=1245, R_eq 4.65): none; #13 (t=640, R_eq 4.37): none; #42 (t=1125, R_eq 3.43): ['s0 (mar 20)', 's2 (mar 60)']

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 1 of 80 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
