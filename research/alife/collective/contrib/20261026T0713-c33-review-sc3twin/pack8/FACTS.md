# Evidence pack: sporecell3-det (seed 8)

- world: `../../../../threads/particle-life/worlds/sporecell3-det/world.py`, family `particle`
- parent: sporecell3; mutation: promoted gate settings: surface detachment k_det=0.05 for particles with < 60 matter neighbours (dt-converged release route)
- run: 201 frames x 50 steps x dt 0.02 = time 200; grid [128, 128]; wall 709s; status ok
- command: `python -m labkit.run threads/particle-life/worlds/sporecell3-det/world.py --out collective/contrib/wip-c33-s3/pack8 --seeds 8 --no-movie`
- segmentation: matter > 0.35 of robust range [0.0, 6.6571], min area 6 px

## Measurements
- components: final 13, mean 9.4, max 13; occupancy final 0.03
- tracks: 16; persistent (alive >= 50% of run): 13; longest 167 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 7.50 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [26, 15, 13], H1 [0, 0, 0]
- motion: 4 long-lived tracks moved >= 1 body length; max speed 0.101/time; max body lengths 2.3
- replication (lineage window K = 20 frames = time 20, default): splits 0, persistent splits 0 (0 more failed only because the siblings re-merged within K), max generation 0, merges 0, merge/split ratio n/a, nucleations 16
- channel total drift (end/start - 1): [-0.9025, 89.0526, None, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 0 at frame 118: holes 0, rim-vs-core 0.32, rim-vs-outside 0.34, heterogeneity 0.04; core [0.001, 0.0, 0.0, 0.988] rim [0.005, 0.0, 0.0, 0.673]
  - track 1 at frame 121: holes 0, rim-vs-core 0.33, rim-vs-outside 0.32, heterogeneity 0.05; core [0.002, 0.0, 0.0, 0.986] rim [0.012, 0.0, 0.0, 0.654]
  - track 2 at frame 121: holes 0, rim-vs-core 0.31, rim-vs-outside 0.30, heterogeneity 0.04; core [0.001, 0.0, 0.0, 0.986] rim [0.004, 0.0, 0.0, 0.672]
  - track 3 at frame 123: holes 0, rim-vs-core 0.29, rim-vs-outside 0.32, heterogeneity 0.04; core [0.001, 0.0, 0.0, 0.981] rim [0.005, 0.0, 0.0, 0.691]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 61 components >= 12 px at frames [67, 101, 133, 166, 200]):
  - radial F food: peak at rho=2.45 (OUTSIDE the peak band 0.5-1.5), rim/core 1.79, rim/outside 0.533 (aggregate of 61 individuals; 2/61 membrane-like individually; rim level 0.0269)
  - radial C0 core kind 0: peak at rho=0.45 (OUTSIDE the peak band 0.5-1.5), rim/core 1.21, rim/outside 5.29 (aggregate of 61 individuals; 0/61 membrane-like individually; rim level 0.508)
  - radial M membrane: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 1.04, rim/outside 1.14 (aggregate of 61 individuals; 0/61 membrane-like individually; rim level 0.0014)
  - radial C1 core kind 1: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.88, rim/outside 28.6 (aggregate of 61 individuals; 0/61 membrane-like individually; rim level 0.513)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #0 (t=118, R_eq 4.15): none; #1 (t=121, R_eq 3.99): none; #2 (t=121, R_eq 3.61): none; #3 (t=123, R_eq 3.83): none

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, particles.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
