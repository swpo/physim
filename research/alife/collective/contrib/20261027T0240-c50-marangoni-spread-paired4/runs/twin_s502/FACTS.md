# Evidence pack: active-nematic-marangoni-spread (seed 502)

- world: `../../../world.py`, family `active-nematic`
- parent: collective/contrib/20261026T0505-c34-nematic-marangoni/world.py; mutation: three heritable surfactant kinds with Marangoni coefficients 20/40/60 (majority-feedback production), in-run mutation between neighbouring kinds, trait-blind turnover
- run: 401 frames x 100 steps x dt 0.05 = time 2000; grid [128, 128]; wall 1079s; status ok
- command: `python -m labkit.run /tmp/claude-0/sp/world.py --out /tmp/claude-0/sp/runs/twin/seed502 --seeds 502 --size 128 128 --frames 400 --no-movie`
- segmentation: matter > 0.64 of robust range [-1.0038, 0.5573], min area 6 px

## Measurements
- components: final 14, mean 14.8, max 23; occupancy final 0.04
- tracks: 112; persistent (alive >= 50% of run): 2; longest 242 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 3.44 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [16, 15, 15], H1 [0, 0, 0]
- motion: 69 long-lived tracks moved >= 1 body length; max speed 0.372/time; max body lengths 10.3
- replication (lineage window K = 20 frames = time 100, default): splits 44, persistent splits 30 (0 more failed only because the siblings re-merged within K), max generation 7, merges 16, merge/split ratio 0.364, nucleations 10
- channel total drift (end/start - 1): [-0.9144, -0.7046, None, 5.2532, None, -0.1876]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 23 at frame 165: holes 0, rim-vs-core 0.48, rim-vs-outside 0.28, heterogeneity 0.10; core [0.963, 0.566, 0.607, 0.014, 0.012, 1.0] rim [0.77, 0.358, 0.999, 0.033, 0.03, 1.0]
  - track 22 at frame 155: holes 0, rim-vs-core 0.55, rim-vs-outside 0.39, heterogeneity 0.10; core [0.962, 0.912, 0.002, 0.38, 0.018, 1.0] rim [0.788, 0.627, 0.005, 0.812, 0.042, 1.0]
  - track 27 at frame 131: holes 0, rim-vs-core 0.40, rim-vs-outside 0.29, heterogeneity 0.09; core [0.969, 0.692, 0.009, 0.039, 0.777, 1.0] rim [0.803, 0.414, 0.024, 0.099, 1.0, 1.0]
  - track 87 at frame 356: holes 0, rim-vs-core 0.58, rim-vs-outside 0.32, heterogeneity 0.10; core [0.963, 0.745, 0.006, 0.411, 0.0, 1.0] rim [0.775, 0.466, 0.016, 0.878, 0.001, 1.0]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 92 components >= 12 px at frames [67, 134, 202, 266, 333, 400]):
  - radial phi (droplet): peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.829, rim/outside 3.09 (aggregate of 92 individuals; 0/92 membrane-like individually; rim level 0.76)
  - radial order |Q|: peak at rho=0.25 (OUTSIDE the peak band 0.5-1.5), rim/core 0.798, rim/outside 9.34 (aggregate of 92 individuals; 8/92 membrane-like individually; rim level 0.58)
  - radial s0 (mar 20): peak at rho=0.65 (in the peak band 0.5-1.5), rim/core 1.24, rim/outside 2.87 (aggregate of 92 individuals; 28/92 membrane-like individually; rim level 0.149)
  - radial s1 (mar 40): peak at rho=0.75 (in the peak band 0.5-1.5), rim/core 1.35, rim/outside 3.23 (aggregate of 92 individuals; 50/92 membrane-like individually; rim level 0.463)
  - radial s2 (mar 60): peak at rho=0.55 (in the peak band 0.5-1.5), rim/core 1.06, rim/outside 2.42 (aggregate of 92 individuals; 20/92 membrane-like individually; rim level 0.0949)
  - radial chemostat target phi_b(x,t): peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.998, rim/outside 1.03 (aggregate of 92 individuals; 0/92 membrane-like individually; rim level 0.992)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #23 (t=825, R_eq 4.89): none; #22 (t=775, R_eq 3.7): ['s1 (mar 40)', 's2 (mar 60)']; #27 (t=655, R_eq 4.15): none; #87 (t=1780, R_eq 4.03): ['s0 (mar 20)']

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 3 of 92 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
