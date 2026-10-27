# Evidence pack: active-nematic-marangoni-spread-food (seed 502)

- world: `../../../world.py`, family `active-nematic`
- parent: collective/contrib/20261026T0505-c34-nematic-marangoni/world.py; mutation: three heritable surfactant kinds with Marangoni coefficients 20/40/60 (majority-feedback production), in-run mutation between neighbouring kinds, trait-blind turnover
- run: 401 frames x 100 steps x dt 0.05 = time 2000; grid [128, 128]; wall 1020s; status ok
- command: `python -m labkit.run /tmp/claude-0/sp3/world.py --out /tmp/claude-0/sp3/runs/Ef/seed502 --seeds 502 --size 128 128 --frames 400 --no-movie`
- segmentation: matter > 0.66 of robust range [-1.0332, 0.5342], min area 6 px

## Measurements
- components: final 8, mean 10.0, max 17; occupancy final 0.02
- tracks: 123; persistent (alive >= 50% of run): 0; longest 135 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 0.00 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [2, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [9, 8, 8], H1 [0, 0, 0]
- motion: 58 long-lived tracks moved >= 1 body length; max speed 0.478/time; max body lengths 8.7
- replication (lineage window K = 20 frames = time 100, default): splits 53, persistent splits 24 (0 more failed only because the siblings re-merged within K), max generation 6, merges 10, merge/split ratio 0.189, nucleations 7
- channel total drift (end/start - 1): [-0.9278, -0.8847, None, -0.6964, None, -0.1876, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 18 at frame 114: holes 0, rim-vs-core 0.59, rim-vs-outside 0.38, heterogeneity 0.09; core [0.976, 0.94, 0.083, 0.467, 0.008, 1.0, 0.0] rim [0.806, 0.659, 0.198, 0.939, 0.019, 1.0, 0.0]
  - track 16 at frame 111: holes 0, rim-vs-core 0.60, rim-vs-outside 0.34, heterogeneity 0.09; core [0.978, 0.854, 0.005, 0.529, 0.009, 1.0, 0.0] rim [0.8, 0.512, 0.012, 0.986, 0.024, 1.0, 0.0]
  - track 68 at frame 323: holes 0, rim-vs-core 0.50, rim-vs-outside 0.37, heterogeneity 0.08; core [0.967, 0.907, 0.0, 0.0, 0.603, 1.0, 0.0] rim [0.808, 0.611, 0.0, 0.001, 0.978, 1.0, 0.0]
  - track 97 at frame 363: holes 0, rim-vs-core 0.49, rim-vs-outside 0.31, heterogeneity 0.08; core [0.966, 0.656, 0.009, 0.0, 0.594, 1.0, 0.0] rim [0.806, 0.397, 0.02, 0.001, 0.978, 1.0, 0.0]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 62 components >= 12 px at frames [67, 134, 202, 266, 333, 400]):
  - radial phi (droplet): peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.83, rim/outside 2.65 (aggregate of 62 individuals; 0/62 membrane-like individually; rim level 0.77)
  - radial order |Q|: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.755, rim/outside 8.6 (aggregate of 62 individuals; 1/62 membrane-like individually; rim level 0.611)
  - radial s0 (mar 20): peak at rho=0.65 (in the peak band 0.5-1.5), rim/core 1.43, rim/outside 1.55 (aggregate of 62 individuals; 9/62 membrane-like individually; rim level 0.0537)
  - radial s1 (mar 40): peak at rho=0.55 (in the peak band 0.5-1.5), rim/core 1.36, rim/outside 3.02 (aggregate of 62 individuals; 23/62 membrane-like individually; rim level 0.353)
  - radial s2 (mar 60): peak at rho=0.65 (in the peak band 0.5-1.5), rim/core 1.28, rim/outside 3.26 (aggregate of 62 individuals; 21/62 membrane-like individually; rim level 0.35)
  - radial chemostat target phi_b(x,t): peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 1, rim/outside 1.02 (aggregate of 62 individuals; 0/62 membrane-like individually; rim level 1)
  - radial food patch: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 1.09, rim/outside 1.1 (aggregate of 62 individuals; 1/62 membrane-like individually; rim level 0.101)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #18 (t=570, R_eq 4.22): ['s0 (mar 20)']; #16 (t=555, R_eq 4.22): none; #68 (t=1615, R_eq 4.41): none; #97 (t=1815, R_eq 3.57): none

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 2 of 62 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
