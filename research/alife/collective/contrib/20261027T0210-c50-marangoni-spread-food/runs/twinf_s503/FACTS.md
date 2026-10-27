# Evidence pack: active-nematic-marangoni-spread-food (seed 503)

- world: `../../../world.py`, family `active-nematic`
- parent: collective/contrib/20261026T0505-c34-nematic-marangoni/world.py; mutation: three heritable surfactant kinds with Marangoni coefficients 20/40/60 (majority-feedback production), in-run mutation between neighbouring kinds, trait-blind turnover
- run: 401 frames x 100 steps x dt 0.05 = time 2000; grid [128, 128]; wall 1078s; status ok
- command: `python -m labkit.run /tmp/claude-0/sp3/world.py --out /tmp/claude-0/sp3/runs/twinf/seed503 --seeds 503 --size 128 128 --frames 400 --no-movie`
- segmentation: matter > 0.66 of robust range [-1.0542, 0.5322], min area 6 px

## Measurements
- components: final 2, mean 6.6, max 17; occupancy final 0.00
- tracks: 82; persistent (alive >= 50% of run): 0; longest 182 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 0.00 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [1, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [2, 2, 2], H1 [0, 0, 0]
- motion: 37 long-lived tracks moved >= 1 body length; max speed 0.338/time; max body lengths 7.4
- replication (lineage window K = 20 frames = time 100, default): splits 31, persistent splits 17 (0 more failed only because the siblings re-merged within K), max generation 7, merges 10, merge/split ratio 0.323, nucleations 9
- channel total drift (end/start - 1): [-0.8047, -0.9763, None, -0.7933, None, -0.2625, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 47 at frame 225: holes 0, rim-vs-core 0.53, rim-vs-outside 0.42, heterogeneity 0.08; core [0.98, 0.952, 0.0, 0.463, 0.0, 1.0, 0.0] rim [0.814, 0.702, 0.0, 0.895, 0.0, 1.0, 0.0]
  - track 35 at frame 182: holes 0, rim-vs-core 0.48, rim-vs-outside 0.32, heterogeneity 0.15; core [0.972, 0.788, 0.0, 0.681, 0.025, 1.0, 0.6] rim [0.822, 0.464, 0.0, 1.0, 0.067, 1.0, 0.619]
  - track 3 at frame 61: holes 0, rim-vs-core 0.36, rim-vs-outside 0.47, heterogeneity 0.07; core [0.99, 0.97, 0.003, 0.026, 0.702, 1.0, 0.0] rim [0.857, 0.767, 0.006, 0.059, 0.963, 1.0, 0.0]
  - track 72 at frame 339: holes 0, rim-vs-core 0.55, rim-vs-outside 0.41, heterogeneity 0.08; core [0.991, 0.982, 0.0, 0.462, 0.022, 1.0, 0.0] rim [0.849, 0.759, 0.001, 0.941, 0.055, 1.0, 0.0]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 40 components >= 12 px at frames [67, 134, 202, 266, 333, 400]):
  - radial phi (droplet): peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.846, rim/outside 2.69 (aggregate of 40 individuals; 0/40 membrane-like individually; rim level 0.781)
  - radial order |Q|: peak at rho=0.35 (OUTSIDE the peak band 0.5-1.5), rim/core 0.799, rim/outside 8.08 (aggregate of 40 individuals; 2/40 membrane-like individually; rim level 0.576)
  - radial s0 (mar 20): peak at rho=0.75 (in the peak band 0.5-1.5), rim/core 1.77, rim/outside 2.65 (aggregate of 40 individuals; 7/40 membrane-like individually; rim level 0.205)  MEMBRANE-LIKE
  - radial s1 (mar 40): peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 1.09, rim/outside 3.28 (aggregate of 40 individuals; 14/40 membrane-like individually; rim level 0.43)
  - radial s2 (mar 60): peak at rho=0.55 (in the peak band 0.5-1.5), rim/core 1.07, rim/outside 2.72 (aggregate of 40 individuals; 11/40 membrane-like individually; rim level 0.231)
  - radial chemostat target phi_b(x,t): peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.997, rim/outside 1.06 (aggregate of 40 individuals; 1/40 membrane-like individually; rim level 0.993)
  - radial food patch: peak at rho=2.15 (OUTSIDE the peak band 0.5-1.5), rim/core 2.43, rim/outside 1.11 (aggregate of 40 individuals; 2/40 membrane-like individually; rim level 0.043)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): s0 (mar 20)
- membrane-like channels per top track at mid-life: #47 (t=1125, R_eq 3.7): none; #35 (t=910, R_eq 3.39): none; #3 (t=305, R_eq 3.83): none; #72 (t=1695, R_eq 3.57): ['s1 (mar 40)', 's2 (mar 60)']

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 2 of 40 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
