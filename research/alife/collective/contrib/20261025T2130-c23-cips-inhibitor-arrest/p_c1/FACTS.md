# Evidence pack: cips-inhib (seed 1)

- world: `../world_inh.py`, family `catalysis-induced-phase-separation`
- parent: collective/contrib/20261025T1650-c00-q-cips-fuel-limited-condensates; mutation: adds an inhibitor I made by catalysis that slows catalysis (cat / (1 + I/KI)) and decays slowly: core inhibition of large droplets as a size-control route that keeps the enzyme conserved
- run: 301 frames x 100 steps x dt 0.1 = time 3000; grid [128, 128]; wall 60s; status ok
- command: `python -m labkit.run collective/contrib/20261025T2130-c23-cips-inhibitor-arrest/world.py --out collective/contrib/20261025T2130-c23-cips-inhibitor-arrest/p_c1 --seeds 1 --frames 300 --size 128 128 --no-movie`
- segmentation: matter > 0.51 of robust range [0.0019, 0.9857], min area 6 px

## Measurements
- components: final 36, mean 27.9, max 41; occupancy final 0.13
- tracks: 45; persistent (alive >= 50% of run): 36; longest 237 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 16.67 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [36, 36, 36], H1 [0, 0, 0]
- motion: 0 long-lived tracks moved >= 1 body length; max speed 0/time; max body lengths 0.6
- replication (lineage window K = 20 frames = time 200, default): splits 0, persistent splits 0 (0 more failed only because the siblings re-merged within K), max generation 0, merges 3, merge/split ratio n/a, nucleations 42
- channel total drift (end/start - 1): [-0.0, -0.5695, 0.3926, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 0 at frame 184: holes 0, rim-vs-core 0.37, rim-vs-outside 0.41, heterogeneity 0.10; core [0.956, 0.905, 0.147, 0.915] rim [0.709, 0.703, 0.306, 0.802]
  - track 1 at frame 184: holes 0, rim-vs-core 0.39, rim-vs-outside 0.41, heterogeneity 0.11; core [0.957, 0.92, 0.126, 0.923] rim [0.707, 0.713, 0.299, 0.798]
  - track 2 at frame 187: holes 0, rim-vs-core 0.33, rim-vs-outside 0.40, heterogeneity 0.09; core [0.95, 0.882, 0.189, 0.882] rim [0.729, 0.703, 0.324, 0.786]
  - track 3 at frame 187: holes 0, rim-vs-core 0.35, rim-vs-outside 0.41, heterogeneity 0.10; core [0.951, 0.892, 0.172, 0.896] rim [0.711, 0.701, 0.318, 0.792]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 186 components >= 12 px at frames [101, 151, 199, 250, 300]):
  - radial e: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.926, rim/outside 27.9 (aggregate of 186 individuals; 0/186 membrane-like individually; rim level 0.911)
  - radial p: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.876, rim/outside 4.46 (aggregate of 186 individuals; 0/186 membrane-like individually; rim level 0.836)
  - radial F: peak at rho=2.45 (OUTSIDE the peak band 0.5-1.5), rim/core 4.89, rim/outside 0.682 (aggregate of 186 individuals; 0/186 membrane-like individually; rim level 0.488)
  - radial I: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.928, rim/outside 1.72 (aggregate of 186 individuals; 0/186 membrane-like individually; rim level 0.89)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #0 (t=1840, R_eq 4.41): none; #1 (t=1840, R_eq 4.69): none; #2 (t=1870, R_eq 3.95): none; #3 (t=1870, R_eq 4.18): none

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
