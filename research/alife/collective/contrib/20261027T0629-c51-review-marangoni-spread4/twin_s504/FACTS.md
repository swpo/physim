# Evidence pack: active-nematic-marangoni-spread (seed 504)

- world: `../../20261027T0000-c50-marangoni-spread-loop1/world.py`, family `active-nematic`
- parent: collective/contrib/20261026T0505-c34-nematic-marangoni/world.py; mutation: three heritable surfactant kinds with Marangoni coefficients 20/40/60 (majority-feedback production), in-run mutation between neighbouring kinds, trait-blind turnover
- run: 401 frames x 100 steps x dt 0.05 = time 2000; grid [128, 128]; wall 714s; status ok
- command: `python -m labkit.run collective/contrib/20261027T0000-c50-marangoni-spread-loop1/world.py --out collective/contrib/20261027T0629-c51-review-marangoni-spread4/twin_s504 --seeds 504 --size 128 128 --frames 400 --no-movie`
- segmentation: matter > 0.64 of robust range [-0.9976, 0.5585], min area 6 px

## Measurements
- components: final 11, mean 14.9, max 24; occupancy final 0.04
- tracks: 120; persistent (alive >= 50% of run): 4; longest 259 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 6.88 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [12, 11, 11], H1 [1, 0, 0]
- motion: 77 long-lived tracks moved >= 1 body length; max speed 0.391/time; max body lengths 15.2
- replication (lineage window K = 20 frames = time 100, default): splits 48, persistent splits 34 (0 more failed only because the siblings re-merged within K), max generation 8, merges 17, merge/split ratio 0.354, nucleations 7
- channel total drift (end/start - 1): [-0.7786, -0.7634, None, 3.3839, None, -0.1427]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 22 at frame 178: holes 0, rim-vs-core 0.52, rim-vs-outside 0.27, heterogeneity 0.18; core [0.938, 0.617, 0.007, 0.525, 0.081, 0.789] rim [0.774, 0.415, 0.015, 0.958, 0.161, 0.696]
  - track 50 at frame 252: holes 0, rim-vs-core 0.46, rim-vs-outside 0.36, heterogeneity 0.09; core [0.964, 0.897, 0.007, 0.017, 0.715, 1.0] rim [0.79, 0.584, 0.016, 0.048, 1.0, 1.0]
  - track 71 at frame 296: holes 0, rim-vs-core 0.53, rim-vs-outside 0.28, heterogeneity 0.09; core [0.95, 0.732, 0.005, 0.432, 0.01, 1.0] rim [0.77, 0.449, 0.01, 0.842, 0.022, 1.0]
  - track 110 at frame 370: holes 0, rim-vs-core 0.44, rim-vs-outside 0.37, heterogeneity 0.10; core [0.966, 0.622, 0.477, 0.033, 0.001, 1.0] rim [0.817, 0.472, 0.863, 0.084, 0.001, 1.0]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 88 components >= 12 px at frames [67, 134, 202, 266, 333, 400]):
  - radial phi (droplet): peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.813, rim/outside 2.88 (aggregate of 88 individuals; 0/88 membrane-like individually; rim level 0.724)
  - radial order |Q|: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.776, rim/outside 7.59 (aggregate of 88 individuals; 3/88 membrane-like individually; rim level 0.537)
  - radial s0 (mar 20): peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.949, rim/outside 2.79 (aggregate of 88 individuals; 22/88 membrane-like individually; rim level 0.155)
  - radial s1 (mar 40): peak at rho=0.65 (in the peak band 0.5-1.5), rim/core 1.2, rim/outside 3.23 (aggregate of 88 individuals; 40/88 membrane-like individually; rim level 0.458)
  - radial s2 (mar 60): peak at rho=0.65 (in the peak band 0.5-1.5), rim/core 1.63, rim/outside 2.41 (aggregate of 88 individuals; 14/88 membrane-like individually; rim level 0.0836)  MEMBRANE-LIKE
  - radial chemostat target phi_b(x,t): peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 1, rim/outside 1.02 (aggregate of 88 individuals; 0/88 membrane-like individually; rim level 0.998)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): s2 (mar 60)
- membrane-like channels per top track at mid-life: #22 (t=890, R_eq 3.66): none; #50 (t=1260, R_eq 3.66): ['s1 (mar 40)']; #71 (t=1480, R_eq 3.7): ['s1 (mar 40)']; #110 (t=1850, R_eq 4.26): ['order |Q|', 's1 (mar 40)']

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 2 of 88 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
