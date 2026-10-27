# Evidence pack: active-nematic-marangoni-distance-pays (seed 601)

- world: `../../../../../../home/user/physim/research/alife/collective/contrib/20261027T0540-c54-distance-pays-loop1/world.py`, family `active-nematic`
- parent: collective/contrib/20261027T0000-c50-marangoni-spread-loop1/world.py; mutation: three heritable surfactant kinds with Marangoni coefficients 20/40/60 (majority-feedback production), in-run mutation between neighbouring kinds, trait-blind turnover
- run: 401 frames x 100 steps x dt 0.05 = time 2000; grid [128, 128]; wall 892s; status ok
- command: `python -m labkit.run collective/contrib/20261027T0540-c54-distance-pays-loop1/world.py --out /tmp/claude-0/c54/runs/glob/seed601 --seeds 601 --size 128 128 --frames 400 --no-movie`
- segmentation: matter > 0.65 of robust range [-1.0153, 0.5548], min area 6 px

## Measurements
- components: final 12, mean 10.7, max 18; occupancy final 0.03
- tracks: 78; persistent (alive >= 50% of run): 4; longest 326 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 11.50 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [12, 12, 11], H1 [0, 0, 0]
- motion: 47 long-lived tracks moved >= 1 body length; max speed 0.311/time; max body lengths 12.4
- replication (lineage window K = 20 frames = time 100, default): splits 28, persistent splits 20 (0 more failed only because the siblings re-merged within K), max generation 5, merges 10, merge/split ratio 0.357, nucleations 12
- channel total drift (end/start - 1): [-0.6594, -0.7464, None, 3.6384, None, -0.1535]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 15 at frame 188: holes 0, rim-vs-core 0.51, rim-vs-outside 0.41, heterogeneity 0.10; core [0.975, 0.965, 0.635, 0.011, 0.006, 0.976] rim [0.787, 0.672, 1.0, 0.035, 0.016, 0.976]
  - track 27 at frame 165: holes 0, rim-vs-core 0.42, rim-vs-outside 0.46, heterogeneity 0.11; core [0.955, 0.704, 0.0, 0.519, 0.0, 0.988] rim [0.834, 0.534, 0.001, 0.885, 0.001, 0.988]
  - track 8 at frame 131: holes 0, rim-vs-core 0.60, rim-vs-outside 0.37, heterogeneity 0.10; core [0.964, 0.874, 0.013, 0.477, 0.0, 0.976] rim [0.787, 0.573, 0.03, 0.965, 0.001, 0.976]
  - track 66 at frame 383: holes 0, rim-vs-core 0.45, rim-vs-outside 0.37, heterogeneity 0.08; core [0.957, 0.948, 0.011, 0.36, 0.0, 0.94] rim [0.795, 0.669, 0.026, 0.676, 0.001, 0.94]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 66 components >= 12 px at frames [67, 134, 202, 266, 333, 400]):
  - radial phi (droplet): peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.849, rim/outside 3.11 (aggregate of 66 individuals; 0/66 membrane-like individually; rim level 0.792)
  - radial order |Q|: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.874, rim/outside 9.46 (aggregate of 66 individuals; 5/66 membrane-like individually; rim level 0.627)
  - radial s0 (mar 20): peak at rho=0.85 (in the peak band 0.5-1.5), rim/core 1.6, rim/outside 2.57 (aggregate of 66 individuals; 18/66 membrane-like individually; rim level 0.139)  MEMBRANE-LIKE
  - radial s1 (mar 40): peak at rho=0.65 (in the peak band 0.5-1.5), rim/core 1.23, rim/outside 3.29 (aggregate of 66 individuals; 32/66 membrane-like individually; rim level 0.522)
  - radial s2 (mar 60): peak at rho=0.85 (in the peak band 0.5-1.5), rim/core 1.54, rim/outside 1.64 (aggregate of 66 individuals; 11/66 membrane-like individually; rim level 0.0964)  MEMBRANE-LIKE
  - radial chemostat target phi_b(x,t): peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 1, rim/outside 1.01 (aggregate of 66 individuals; 0/66 membrane-like individually; rim level 0.958)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): s0 (mar 20), s2 (mar 60)
- membrane-like channels per top track at mid-life: #15 (t=940, R_eq 3.34): ['s0 (mar 20)', 's1 (mar 40)', 's2 (mar 60)']; #27 (t=825, R_eq 2.99): ['s1 (mar 40)']; #8 (t=655, R_eq 4.07): ['s1 (mar 40)']; #66 (t=1915, R_eq 3.83): none

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
