# Evidence pack: active-nematic-marangoni-spread (seed 521)

- world: `../../../20261027T0000-c50-marangoni-spread-loop1/world.py`, family `active-nematic`
- parent: collective/contrib/20261026T0505-c34-nematic-marangoni/world.py; mutation: three heritable surfactant kinds with Marangoni coefficients 20/40/60 (majority-feedback production), in-run mutation between neighbouring kinds, trait-blind turnover
- run: 401 frames x 100 steps x dt 0.05 = time 2000; grid [128, 128]; wall 860s; status ok
- command: `python -m labkit.run collective/contrib/20261027T0000-c50-marangoni-spread-loop1/world.py --out collective/contrib/c57-w10/Efast/seed521 --seeds 521 --size 128 128 --frames 400 --no-movie`
- segmentation: matter > 0.62 of robust range [-0.9537, 0.573], min area 6 px

## Measurements
- components: final 13, mean 14.7, max 24; occupancy final 0.03
- tracks: 149; persistent (alive >= 50% of run): 3; longest 243 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 14.33 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [14, 13, 13], H1 [0, 0, 0]
- motion: 77 long-lived tracks moved >= 1 body length; max speed 0.43/time; max body lengths 13.0
- replication (lineage window K = 20 frames = time 100, default): splits 59, persistent splits 35 (0 more failed only because the siblings re-merged within K), max generation 6, merges 23, merge/split ratio 0.39, nucleations 9
- channel total drift (end/start - 1): [-0.7243, -0.7453, None, 4.8269, None, -0.1463]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 72 at frame 259: holes 0, rim-vs-core 0.57, rim-vs-outside 0.38, heterogeneity 0.10; core [0.958, 0.909, 0.021, 0.331, 0.0, 1.0] rim [0.757, 0.548, 0.053, 0.717, 0.0, 1.0]
  - track 71 at frame 255: holes 0, rim-vs-core 0.54, rim-vs-outside 0.39, heterogeneity 0.09; core [0.969, 0.938, 0.01, 0.351, 0.0, 1.0] rim [0.794, 0.625, 0.028, 0.757, 0.001, 1.0]
  - track 22 at frame 158: holes 0, rim-vs-core 0.54, rim-vs-outside 0.36, heterogeneity 0.09; core [0.948, 0.812, 0.002, 0.419, 0.009, 1.0] rim [0.763, 0.523, 0.004, 0.829, 0.021, 1.0]
  - track 118 at frame 316: holes 0, rim-vs-core 0.54, rim-vs-outside 0.32, heterogeneity 0.09; core [0.949, 0.777, 0.008, 0.411, 0.0, 1.0] rim [0.76, 0.484, 0.016, 0.824, 0.0, 1.0]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 94 components >= 12 px at frames [67, 134, 202, 266, 333, 400]):
  - radial phi (droplet): peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.815, rim/outside 3.46 (aggregate of 94 individuals; 0/94 membrane-like individually; rim level 0.757)
  - radial order |Q|: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.75, rim/outside 9.18 (aggregate of 94 individuals; 4/94 membrane-like individually; rim level 0.578)
  - radial s0 (mar 20): peak at rho=0.65 (in the peak band 0.5-1.5), rim/core 1.5, rim/outside 3.06 (aggregate of 94 individuals; 38/94 membrane-like individually; rim level 0.188)  MEMBRANE-LIKE
  - radial s1 (mar 40): peak at rho=0.65 (in the peak band 0.5-1.5), rim/core 1.5, rim/outside 3.31 (aggregate of 94 individuals; 54/94 membrane-like individually; rim level 0.449)
  - radial s2 (mar 60): peak at rho=0.55 (in the peak band 0.5-1.5), rim/core 1.24, rim/outside 2.45 (aggregate of 94 individuals; 17/94 membrane-like individually; rim level 0.0911)
  - radial chemostat target phi_b(x,t): peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.995, rim/outside 1.01 (aggregate of 94 individuals; 1/94 membrane-like individually; rim level 0.951)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): s0 (mar 20)
- membrane-like channels per top track at mid-life: #72 (t=1295, R_eq 3.34): ['s0 (mar 20)', 's1 (mar 40)']; #71 (t=1275, R_eq 3.61): ['s0 (mar 20)', 's1 (mar 40)']; #22 (t=790, R_eq 4.11): none; #118 (t=1580, R_eq 3.99): none

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 3 of 94 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
