# Evidence pack: active-nematic-marangoni-distance-pays (seed 600)

- world: `../../../../../../home/user/physim/research/alife/collective/contrib/20261027T0540-c54-distance-pays-loop1/world.py`, family `active-nematic`
- parent: collective/contrib/20261027T0000-c50-marangoni-spread-loop1/world.py; mutation: three heritable surfactant kinds with Marangoni coefficients 20/40/60 (majority-feedback production), in-run mutation between neighbouring kinds, trait-blind turnover
- run: 401 frames x 100 steps x dt 0.05 = time 2000; grid [128, 128]; wall 927s; status ok
- command: `python -m labkit.run collective/contrib/20261027T0540-c54-distance-pays-loop1/world.py --out /tmp/claude-0/c54/runs/off/seed600 --seeds 600 --size 128 128 --frames 400 --no-movie`
- segmentation: matter > 0.66 of robust range [-0.9954, 0.5116], min area 6 px

## Measurements
- components: final 1, mean 4.1, max 10; occupancy final 0.00
- tracks: 30; persistent (alive >= 50% of run): 0; longest 192 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 0.00 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [1, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [2, 1, 1], H1 [0, 0, 0]
- motion: 14 long-lived tracks moved >= 1 body length; max speed 0.0609/time; max body lengths 3.3
- replication (lineage window K = 20 frames = time 100, default): splits 12, persistent splits 9 (0 more failed only because the siblings re-merged within K), max generation 4, merges 1, merge/split ratio 0.083, nucleations 5
- channel total drift (end/start - 1): [-0.8308, -0.9734, None, -0.3772, None, -0.1929]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 19 at frame 239: holes 0, rim-vs-core 0.52, rim-vs-outside 0.42, heterogeneity 0.06; core [1.0, 1.0, 0.002, 0.387, 0.006, 1.0] rim [0.967, 0.961, 0.005, 0.905, 0.019, 1.0]
  - track 9 at frame 104: holes 0, rim-vs-core 0.10, rim-vs-outside 0.45, heterogeneity 0.02; core [1.0, 1.0, 0.006, 0.005, 1.0, 1.0] rim [0.933, 0.927, 0.014, 0.013, 1.0, 1.0]
  - track 15 at frame 175: holes 0, rim-vs-core 0.48, rim-vs-outside 0.43, heterogeneity 0.07; core [1.0, 0.998, 0.007, 0.507, 0.001, 1.0] rim [0.941, 0.897, 0.016, 0.968, 0.003, 1.0]
  - track 25 at frame 360: holes 0, rim-vs-core 0.54, rim-vs-outside 0.42, heterogeneity 0.08; core [1.0, 0.99, 0.001, 0.481, 0.0, 1.0] rim [0.943, 0.762, 0.002, 0.964, 0.001, 1.0]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 24 components >= 12 px at frames [67, 134, 202, 266, 333, 400]):
  - radial phi (droplet): peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.965, rim/outside 3.11 (aggregate of 24 individuals; 0/24 membrane-like individually; rim level 0.958)
  - radial order |Q|: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.941, rim/outside 7.8 (aggregate of 24 individuals; 0/24 membrane-like individually; rim level 0.865)
  - radial s0 (mar 20): peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 1.2, rim/outside 1.52 (aggregate of 24 individuals; 7/24 membrane-like individually; rim level 0.08)
  - radial s1 (mar 40): peak at rho=0.95 (in the peak band 0.5-1.5), rim/core 2.54, rim/outside 3.6 (aggregate of 24 individuals; 19/24 membrane-like individually; rim level 0.742)  MEMBRANE-LIKE
  - radial s2 (mar 60): peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 1.26, rim/outside 1.31 (aggregate of 24 individuals; 6/24 membrane-like individually; rim level 0.2)
  - radial chemostat target phi_b(x,t): peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 1, rim/outside 1.01 (aggregate of 24 individuals; 0/24 membrane-like individually; rim level 0.923)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): s1 (mar 40)
- membrane-like channels per top track at mid-life: #19 (t=1195, R_eq 3.14): ['s1 (mar 40)']; #9 (t=520, R_eq 3.24): ['s0 (mar 20)']; #15 (t=875, R_eq 3.24): ['s1 (mar 40)']; #25 (t=1800, R_eq 2.46): ['s1 (mar 40)']

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
