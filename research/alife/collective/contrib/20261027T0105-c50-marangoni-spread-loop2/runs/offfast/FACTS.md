# Evidence pack: active-nematic-marangoni-spread (seed 501)

- world: `../../../world.py`, family `active-nematic`
- parent: collective/contrib/20261026T0505-c34-nematic-marangoni/world.py; mutation: three heritable surfactant kinds with Marangoni coefficients 20/40/60 (majority-feedback production), in-run mutation between neighbouring kinds, trait-blind turnover
- run: 401 frames x 100 steps x dt 0.05 = time 2000; grid [128, 128]; wall 1053s; status ok
- command: `python -m labkit.run /tmp/claude-0/sp/world.py --out /tmp/claude-0/sp/runs/offfast/seed501 --seeds 501 --size 128 128 --frames 400 --no-movie`
- segmentation: matter > 0.62 of robust range [-0.9404, 0.57], min area 6 px

## Measurements
- components: final 4, mean 8.5, max 18; occupancy final 0.01
- tracks: 79; persistent (alive >= 50% of run): 0; longest 137 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 0.00 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [5, 5, 4], H1 [0, 0, 0]
- motion: 32 long-lived tracks moved >= 1 body length; max speed 0.0842/time; max body lengths 3.0
- replication (lineage window K = 20 frames = time 100, default): splits 33, persistent splits 18 (0 more failed only because the siblings re-merged within K), max generation 4, merges 4, merge/split ratio 0.121, nucleations 9
- channel total drift (end/start - 1): [-0.6769, -0.9251, None, 0.0754, None, 0.0]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 52 at frame 232: holes 0, rim-vs-core 0.60, rim-vs-outside 0.42, heterogeneity 0.09; core [0.988, 0.971, 0.001, 0.008, 0.46, 1.0] rim [0.846, 0.738, 0.001, 0.025, 0.99, 1.0]
  - track 21 at frame 121: holes 0, rim-vs-core 0.49, rim-vs-outside 0.36, heterogeneity 0.10; core [0.976, 0.919, 0.141, 0.403, 0.0, 1.0] rim [0.812, 0.654, 0.319, 0.734, 0.001, 1.0]
  - track 42 at frame 182: holes 0, rim-vs-core 0.39, rim-vs-outside 0.32, heterogeneity 0.11; core [0.959, 0.699, 0.001, 0.559, 0.0, 0.944] rim [0.819, 0.535, 0.002, 0.881, 0.0, 0.889]
  - track 71 at frame 353: holes 0, rim-vs-core 0.49, rim-vs-outside 0.43, heterogeneity 0.09; core [0.979, 0.973, 0.012, 0.378, 0.019, 1.0] rim [0.789, 0.701, 0.027, 0.738, 0.043, 1.0]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 48 components >= 12 px at frames [67, 134, 202, 266, 333, 400]):
  - radial phi (droplet): peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.846, rim/outside 3.21 (aggregate of 48 individuals; 0/48 membrane-like individually; rim level 0.772)
  - radial order |Q|: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.83, rim/outside 6.92 (aggregate of 48 individuals; 2/48 membrane-like individually; rim level 0.673)
  - radial s0 (mar 20): peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.86, rim/outside 1.91 (aggregate of 48 individuals; 11/48 membrane-like individually; rim level 0.0839)
  - radial s1 (mar 40): peak at rho=0.75 (in the peak band 0.5-1.5), rim/core 1.41, rim/outside 2.94 (aggregate of 48 individuals; 27/48 membrane-like individually; rim level 0.504)
  - radial s2 (mar 60): peak at rho=0.55 (in the peak band 0.5-1.5), rim/core 1.22, rim/outside 2.72 (aggregate of 48 individuals; 13/48 membrane-like individually; rim level 0.187)
  - radial chemostat target phi_b(x,t): peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 1.02, rim/outside 1.05 (aggregate of 48 individuals; 1/48 membrane-like individually; rim level 0.995)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #52 (t=1160, R_eq 2.93): ['s1 (mar 40)', 's2 (mar 60)']; #21 (t=605, R_eq 3.52): ['s0 (mar 20)', 's1 (mar 40)']; #42 (t=910, R_eq 3.78): none; #71 (t=1765, R_eq 3.39): ['s0 (mar 20)', 's1 (mar 40)', 's2 (mar 60)']

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 2 of 48 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
