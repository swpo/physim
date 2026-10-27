# Evidence pack: active-nematic-marangoni-spread (seed 520)

- world: `../../../20261027T0000-c50-marangoni-spread-loop1/world.py`, family `active-nematic`
- parent: collective/contrib/20261026T0505-c34-nematic-marangoni/world.py; mutation: three heritable surfactant kinds with Marangoni coefficients 20/40/60 (majority-feedback production), in-run mutation between neighbouring kinds, trait-blind turnover
- run: 401 frames x 100 steps x dt 0.05 = time 2000; grid [128, 128]; wall 894s; status ok
- command: `python -m labkit.run collective/contrib/20261027T0000-c50-marangoni-spread-loop1/world.py --out collective/contrib/c57-w7/twin/seed520 --seeds 520 --size 128 128 --frames 400 --no-movie`
- segmentation: matter > 0.64 of robust range [-0.9975, 0.5581], min area 6 px

## Measurements
- components: final 11, mean 13.9, max 27; occupancy final 0.03
- tracks: 131; persistent (alive >= 50% of run): 1; longest 266 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 9.22 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [13, 12, 11], H1 [0, 0, 0]
- motion: 82 long-lived tracks moved >= 1 body length; max speed 0.301/time; max body lengths 10.5
- replication (lineage window K = 20 frames = time 100, default): splits 47, persistent splits 27 (0 more failed only because the siblings re-merged within K), max generation 6, merges 21, merge/split ratio 0.447, nucleations 16
- channel total drift (end/start - 1): [-0.7972, -0.7923, None, 4.0222, None, -0.1729]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 7 at frame 145: holes 0, rim-vs-core 0.45, rim-vs-outside 0.36, heterogeneity 0.10; core [0.929, 0.76, 0.001, 0.544, 0.021, 1.0] rim [0.794, 0.505, 0.002, 0.89, 0.038, 1.0]
  - track 22 at frame 128: holes 0, rim-vs-core 0.56, rim-vs-outside 0.31, heterogeneity 0.11; core [0.966, 0.595, 0.009, 0.45, 0.003, 1.0] rim [0.78, 0.393, 0.023, 0.933, 0.008, 1.0]
  - track 70 at frame 215: holes 0, rim-vs-core 0.64, rim-vs-outside 0.38, heterogeneity 0.11; core [0.969, 0.863, 0.0, 0.434, 0.021, 1.0] rim [0.792, 0.525, 0.001, 0.953, 0.056, 1.0]
  - track 125 at frame 387: holes 0, rim-vs-core 0.62, rim-vs-outside 0.40, heterogeneity 0.09; core [0.984, 0.937, 0.008, 0.25, 0.003, 1.0] rim [0.816, 0.581, 0.027, 0.732, 0.009, 1.0]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 79 components >= 12 px at frames [67, 134, 202, 266, 333, 400]):
  - radial phi (droplet): peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.814, rim/outside 3.01 (aggregate of 79 individuals; 0/79 membrane-like individually; rim level 0.745)
  - radial order |Q|: peak at rho=0.25 (OUTSIDE the peak band 0.5-1.5), rim/core 0.778, rim/outside 8.4 (aggregate of 79 individuals; 3/79 membrane-like individually; rim level 0.55)
  - radial s0 (mar 20): peak at rho=0.65 (in the peak band 0.5-1.5), rim/core 1.93, rim/outside 2.48 (aggregate of 79 individuals; 18/79 membrane-like individually; rim level 0.0897)  MEMBRANE-LIKE
  - radial s1 (mar 40): peak at rho=0.55 (in the peak band 0.5-1.5), rim/core 1.22, rim/outside 3.17 (aggregate of 79 individuals; 34/79 membrane-like individually; rim level 0.406)
  - radial s2 (mar 60): peak at rho=0.55 (in the peak band 0.5-1.5), rim/core 1.22, rim/outside 3.02 (aggregate of 79 individuals; 30/79 membrane-like individually; rim level 0.251)
  - radial chemostat target phi_b(x,t): peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 1.01, rim/outside 1.03 (aggregate of 79 individuals; 0/79 membrane-like individually; rim level 0.987)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): s0 (mar 20)
- membrane-like channels per top track at mid-life: #7 (t=725, R_eq 4.69): ['order |Q|']; #22 (t=640, R_eq 4.58): none; #70 (t=1075, R_eq 3.24): ['s1 (mar 40)', 's2 (mar 60)']; #125 (t=1935, R_eq 2.88): ['s0 (mar 20)', 's1 (mar 40)', 's2 (mar 60)']

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 1 of 79 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
