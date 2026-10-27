# Evidence pack: active-nematic-marangoni-spread (seed 501)

- world: `../../../world.py`, family `active-nematic`
- parent: collective/contrib/20261026T0505-c34-nematic-marangoni/world.py; mutation: three heritable surfactant kinds with Marangoni coefficients 20/40/60 (majority-feedback production), in-run mutation between neighbouring kinds, trait-blind turnover
- run: 401 frames x 100 steps x dt 0.05 = time 2000; grid [128, 128]; wall 1046s; status ok
- command: `python -m labkit.run /tmp/claude-0/sp/world.py --out /tmp/claude-0/sp/runs/E/seed501 --seeds 501 --size 128 128 --frames 400 --no-movie`
- segmentation: matter > 0.65 of robust range [-1.0276, 0.5453], min area 6 px

## Measurements
- components: final 8, mean 10.8, max 18; occupancy final 0.03
- tracks: 107; persistent (alive >= 50% of run): 1; longest 201 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 2.80 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [9, 8, 7], H1 [0, 0, 0]
- motion: 62 long-lived tracks moved >= 1 body length; max speed 0.387/time; max body lengths 19.1
- replication (lineage window K = 20 frames = time 100, default): splits 39, persistent splits 19 (0 more failed only because the siblings re-merged within K), max generation 5, merges 19, merge/split ratio 0.487, nucleations 10
- channel total drift (end/start - 1): [-0.9065, -0.8423, None, 1.2979, None, -0.2938]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 38 at frame 195: holes 0, rim-vs-core 0.59, rim-vs-outside 0.33, heterogeneity 0.11; core [0.973, 0.694, 0.004, 0.448, 0.007, 1.0] rim [0.791, 0.424, 0.01, 0.945, 0.02, 1.0]
  - track 37 at frame 158: holes 0, rim-vs-core 0.57, rim-vs-outside 0.39, heterogeneity 0.14; core [0.975, 0.876, 0.012, 0.417, 0.007, 0.972] rim [0.806, 0.613, 0.034, 0.886, 0.017, 0.875]
  - track 48 at frame 192: holes 0, rim-vs-core 0.50, rim-vs-outside 0.32, heterogeneity 0.10; core [0.961, 0.738, 0.0, 0.019, 0.566, 1.0] rim [0.815, 0.464, 0.0, 0.044, 0.962, 1.0]
  - track 93 at frame 360: holes 0, rim-vs-core 0.63, rim-vs-outside 0.37, heterogeneity 0.11; core [0.967, 0.799, 0.014, 0.463, 0.014, 1.0] rim [0.791, 0.453, 0.031, 0.956, 0.035, 1.0]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 69 components >= 12 px at frames [67, 134, 202, 266, 333, 400]):
  - radial phi (droplet): peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.842, rim/outside 2.92 (aggregate of 69 individuals; 0/69 membrane-like individually; rim level 0.78)
  - radial order |Q|: peak at rho=0.25 (OUTSIDE the peak band 0.5-1.5), rim/core 0.796, rim/outside 9.29 (aggregate of 69 individuals; 5/69 membrane-like individually; rim level 0.6)
  - radial s0 (mar 20): peak at rho=0.65 (in the peak band 0.5-1.5), rim/core 1.15, rim/outside 2.46 (aggregate of 69 individuals; 11/69 membrane-like individually; rim level 0.0877)
  - radial s1 (mar 40): peak at rho=0.75 (in the peak band 0.5-1.5), rim/core 1.29, rim/outside 3.29 (aggregate of 69 individuals; 27/69 membrane-like individually; rim level 0.43)
  - radial s2 (mar 60): peak at rho=0.65 (in the peak band 0.5-1.5), rim/core 1.25, rim/outside 2.87 (aggregate of 69 individuals; 21/69 membrane-like individually; rim level 0.237)
  - radial chemostat target phi_b(x,t): peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 1, rim/outside 1.03 (aggregate of 69 individuals; 0/69 membrane-like individually; rim level 1)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #38 (t=975, R_eq 4.51): none; #37 (t=790, R_eq 4.92): none; #48 (t=960, R_eq 3.95): none; #93 (t=1800, R_eq 3.04): ['s0 (mar 20)', 's1 (mar 40)', 's2 (mar 60)']

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 1 of 69 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
