# Evidence pack: active-nematic-marangoni-spread (seed 521)

- world: `../../../20261027T0000-c50-marangoni-spread-loop1/world.py`, family `active-nematic`
- parent: collective/contrib/20261026T0505-c34-nematic-marangoni/world.py; mutation: three heritable surfactant kinds with Marangoni coefficients 20/40/60 (majority-feedback production), in-run mutation between neighbouring kinds, trait-blind turnover
- run: 401 frames x 100 steps x dt 0.05 = time 2000; grid [128, 128]; wall 852s; status ok
- command: `python -m labkit.run collective/contrib/20261027T0000-c50-marangoni-spread-loop1/world.py --out collective/contrib/c57-w10/twinfast/seed521 --seeds 521 --size 128 128 --frames 400 --no-movie`
- segmentation: matter > 0.63 of robust range [-0.9526, 0.5593], min area 6 px

## Measurements
- components: final 13, mean 15.7, max 24; occupancy final 0.05
- tracks: 153; persistent (alive >= 50% of run): 2; longest 291 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 9.50 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [16, 13, 13], H1 [1, 0, 0]
- motion: 91 long-lived tracks moved >= 1 body length; max speed 0.421/time; max body lengths 12.3
- replication (lineage window K = 20 frames = time 100, default): splits 59, persistent splits 32 (0 more failed only because the siblings re-merged within K), max generation 5, merges 25, merge/split ratio 0.424, nucleations 9
- channel total drift (end/start - 1): [-0.7243, -0.6824, None, 3.4439, None, -0.1463]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 13 at frame 178: holes 0, rim-vs-core 0.55, rim-vs-outside 0.34, heterogeneity 0.09; core [0.946, 0.802, 0.009, 0.433, 0.012, 1.0] rim [0.745, 0.486, 0.021, 0.833, 0.027, 1.0]
  - track 8 at frame 128: holes 0, rim-vs-core 0.45, rim-vs-outside 0.35, heterogeneity 0.10; core [0.962, 0.547, 0.003, 0.498, 0.016, 1.0] rim [0.812, 0.395, 0.007, 0.893, 0.033, 1.0]
  - track 30 at frame 165: holes 0, rim-vs-core 0.59, rim-vs-outside 0.35, heterogeneity 0.10; core [0.963, 0.806, 0.016, 0.434, 0.01, 1.0] rim [0.782, 0.525, 0.038, 0.92, 0.025, 1.0]
  - track 141 at frame 376: holes 0, rim-vs-core 0.54, rim-vs-outside 0.33, heterogeneity 0.09; core [0.953, 0.812, 0.437, 0.004, 0.0, 1.0] rim [0.772, 0.531, 0.866, 0.009, 0.001, 1.0]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 98 components >= 12 px at frames [67, 134, 202, 266, 333, 400]):
  - radial phi (droplet): peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.816, rim/outside 3.35 (aggregate of 98 individuals; 0/98 membrane-like individually; rim level 0.738)
  - radial order |Q|: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.775, rim/outside 8.66 (aggregate of 98 individuals; 7/98 membrane-like individually; rim level 0.559)
  - radial s0 (mar 20): peak at rho=0.55 (in the peak band 0.5-1.5), rim/core 1.31, rim/outside 3.03 (aggregate of 98 individuals; 41/98 membrane-like individually; rim level 0.23)
  - radial s1 (mar 40): peak at rho=0.55 (in the peak band 0.5-1.5), rim/core 1.22, rim/outside 3.15 (aggregate of 98 individuals; 44/98 membrane-like individually; rim level 0.347)
  - radial s2 (mar 60): peak at rho=0.65 (in the peak band 0.5-1.5), rim/core 1.39, rim/outside 2.73 (aggregate of 98 individuals; 27/98 membrane-like individually; rim level 0.129)
  - radial chemostat target phi_b(x,t): peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.998, rim/outside 1.02 (aggregate of 98 individuals; 0/98 membrane-like individually; rim level 0.986)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #13 (t=890, R_eq 4.3): none; #8 (t=640, R_eq 4.26): ['order |Q|']; #30 (t=825, R_eq 4.37): none; #141 (t=1880, R_eq 4.03): none

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 4 of 98 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
