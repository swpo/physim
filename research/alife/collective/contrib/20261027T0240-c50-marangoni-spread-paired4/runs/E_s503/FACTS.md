# Evidence pack: active-nematic-marangoni-spread (seed 503)

- world: `../../../world.py`, family `active-nematic`
- parent: collective/contrib/20261026T0505-c34-nematic-marangoni/world.py; mutation: three heritable surfactant kinds with Marangoni coefficients 20/40/60 (majority-feedback production), in-run mutation between neighbouring kinds, trait-blind turnover
- run: 401 frames x 100 steps x dt 0.05 = time 2000; grid [128, 128]; wall 1077s; status ok
- command: `python -m labkit.run /tmp/claude-0/sp/world.py --out /tmp/claude-0/sp/runs/E/seed503 --seeds 503 --size 128 128 --frames 400 --no-movie`
- segmentation: matter > 0.65 of robust range [-1.0174, 0.5462], min area 6 px

## Measurements
- components: final 6, mean 10.0, max 21; occupancy final 0.02
- tracks: 110; persistent (alive >= 50% of run): 1; longest 331 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 10.86 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [1, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [7, 6, 6], H1 [0, 0, 0]
- motion: 52 long-lived tracks moved >= 1 body length; max speed 0.615/time; max body lengths 12.3
- replication (lineage window K = 20 frames = time 100, default): splits 44, persistent splits 18 (0 more failed only because the siblings re-merged within K), max generation 4, merges 14, merge/split ratio 0.318, nucleations 12
- channel total drift (end/start - 1): [-0.8133, -0.8363, None, 1.8512, None, -0.2625]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 13 at frame 188: holes 0, rim-vs-core 0.59, rim-vs-outside 0.35, heterogeneity 0.10; core [0.973, 0.893, 0.0, 0.492, 0.01, 1.0] rim [0.805, 0.589, 0.0, 0.969, 0.025, 1.0]
  - track 28 at frame 118: holes 0, rim-vs-core 0.49, rim-vs-outside 0.37, heterogeneity 0.09; core [0.946, 0.875, 0.0, 0.016, 0.533, 1.0] rim [0.783, 0.607, 0.0, 0.031, 0.913, 1.0]
  - track 65 at frame 323: holes 0, rim-vs-core 0.56, rim-vs-outside 0.33, heterogeneity 0.10; core [0.968, 0.864, 0.012, 0.441, 0.018, 1.0] rim [0.794, 0.553, 0.028, 0.866, 0.043, 1.0]
  - track 48 at frame 235: holes 0, rim-vs-core 0.51, rim-vs-outside 0.29, heterogeneity 0.10; core [0.958, 0.587, 0.0, 0.017, 0.575, 1.0] rim [0.775, 0.335, 0.001, 0.039, 0.981, 1.0]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 61 components >= 12 px at frames [67, 134, 202, 266, 333, 400]):
  - radial phi (droplet): peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.834, rim/outside 2.94 (aggregate of 61 individuals; 0/61 membrane-like individually; rim level 0.777)
  - radial order |Q|: peak at rho=0.25 (OUTSIDE the peak band 0.5-1.5), rim/core 0.826, rim/outside 8.99 (aggregate of 61 individuals; 7/61 membrane-like individually; rim level 0.605)
  - radial s0 (mar 20): peak at rho=0.65 (in the peak band 0.5-1.5), rim/core 1.28, rim/outside 2 (aggregate of 61 individuals; 9/61 membrane-like individually; rim level 0.106)
  - radial s1 (mar 40): peak at rho=0.75 (in the peak band 0.5-1.5), rim/core 1.36, rim/outside 3.1 (aggregate of 61 individuals; 24/61 membrane-like individually; rim level 0.376)
  - radial s2 (mar 60): peak at rho=0.65 (in the peak band 0.5-1.5), rim/core 1.15, rim/outside 2.97 (aggregate of 61 individuals; 24/61 membrane-like individually; rim level 0.288)
  - radial chemostat target phi_b(x,t): peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 1, rim/outside 1.04 (aggregate of 61 individuals; 0/61 membrane-like individually; rim level 1)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #13 (t=940, R_eq 4.26): none; #28 (t=590, R_eq 4.37): none; #65 (t=1615, R_eq 4.03): none; #48 (t=1175, R_eq 4.15): none

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 1 of 61 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
