# Evidence pack: active-nematic-marangoni-spread (seed 504)

- world: `../../20261027T0000-c50-marangoni-spread-loop1/world.py`, family `active-nematic`
- parent: collective/contrib/20261026T0505-c34-nematic-marangoni/world.py; mutation: three heritable surfactant kinds with Marangoni coefficients 20/40/60 (majority-feedback production), in-run mutation between neighbouring kinds, trait-blind turnover
- run: 401 frames x 100 steps x dt 0.05 = time 2000; grid [128, 128]; wall 717s; status ok
- command: `python -m labkit.run collective/contrib/20261027T0000-c50-marangoni-spread-loop1/world.py --out collective/contrib/20261027T0629-c51-review-marangoni-spread4/E_s504 --seeds 504 --size 128 128 --frames 400 --no-movie`
- segmentation: matter > 0.63 of robust range [-0.997, 0.574], min area 6 px

## Measurements
- components: final 13, mean 13.3, max 22; occupancy final 0.03
- tracks: 137; persistent (alive >= 50% of run): 0; longest 186 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 0.00 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [13, 13, 12], H1 [1, 0, 0]
- motion: 67 long-lived tracks moved >= 1 body length; max speed 0.395/time; max body lengths 18.8
- replication (lineage window K = 20 frames = time 100, default): splits 54, persistent splits 27 (0 more failed only because the siblings re-merged within K), max generation 7, merges 24, merge/split ratio 0.444, nucleations 7
- channel total drift (end/start - 1): [-0.7786, -0.7835, None, 4.5856, None, -0.1427]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 86 at frame 309: holes 0, rim-vs-core 0.56, rim-vs-outside 0.32, heterogeneity 0.12; core [0.963, 0.661, 0.001, 0.418, 0.003, 1.0] rim [0.792, 0.443, 0.003, 0.906, 0.008, 1.0]
  - track 59 at frame 198: holes 0, rim-vs-core 0.61, rim-vs-outside 0.46, heterogeneity 0.10; core [0.977, 0.954, 0.323, 0.007, 0.001, 1.0] rim [0.816, 0.744, 0.868, 0.023, 0.005, 1.0]
  - track 101 at frame 329: holes 0, rim-vs-core 0.55, rim-vs-outside 0.33, heterogeneity 0.09; core [0.954, 0.769, 0.0, 0.482, 0.001, 1.0] rim [0.782, 0.517, 0.001, 0.94, 0.001, 1.0]
  - track 120 at frame 339: holes 0, rim-vs-core 0.55, rim-vs-outside 0.37, heterogeneity 0.10; core [0.958, 0.892, 0.002, 0.405, 0.0, 1.0] rim [0.785, 0.582, 0.005, 0.825, 0.001, 1.0]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 83 components >= 12 px at frames [67, 134, 202, 266, 333, 400]):
  - radial phi (droplet): peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.822, rim/outside 3.06 (aggregate of 83 individuals; 0/83 membrane-like individually; rim level 0.75)
  - radial order |Q|: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.764, rim/outside 8.79 (aggregate of 83 individuals; 3/83 membrane-like individually; rim level 0.576)
  - radial s0 (mar 20): peak at rho=0.85 (in the peak band 0.5-1.5), rim/core 1.61, rim/outside 2.86 (aggregate of 83 individuals; 21/83 membrane-like individually; rim level 0.139)  MEMBRANE-LIKE
  - radial s1 (mar 40): peak at rho=0.65 (in the peak band 0.5-1.5), rim/core 1.32, rim/outside 3.46 (aggregate of 83 individuals; 42/83 membrane-like individually; rim level 0.529)
  - radial s2 (mar 60): peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.968, rim/outside 1.95 (aggregate of 83 individuals; 13/83 membrane-like individually; rim level 0.06)
  - radial chemostat target phi_b(x,t): peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 1, rim/outside 1.01 (aggregate of 83 individuals; 0/83 membrane-like individually; rim level 0.992)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): s0 (mar 20)
- membrane-like channels per top track at mid-life: #86 (t=1545, R_eq 4.3): ['s1 (mar 40)']; #59 (t=990, R_eq 3.57): ['s0 (mar 20)', 's1 (mar 40)']; #101 (t=1645, R_eq 4.11): none; #120 (t=1695, R_eq 3.66): ['s1 (mar 40)']

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 2 of 83 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
