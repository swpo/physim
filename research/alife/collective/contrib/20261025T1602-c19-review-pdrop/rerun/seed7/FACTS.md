# Evidence pack: pdrop (seed 7)

- world: `../../../20261025T1408-c14-pdrop-arrested/world.py`, family `hybrid-particle-field`
- parent: threads/active-droplets/worlds/ad2-catalysts; mutation: catalyst fields -> identity-carrying Brownian particles with a heritable rate, gated by droplet material
- run: 81 frames x 250 steps x dt 0.5 = time 10000; grid [128, 128]; wall 300s; status ok
- command: `python -m labkit.run collective/contrib/20261025T1408-c14-pdrop-arrested/world.py --out collective/contrib/20261025T1602-c19-review-pdrop/rerun/seed7 --seeds 7 --frames 80 --spf 250 --no-movie`
- segmentation: matter > 0.46 of robust range [-1.0306, 1.2316], min area 6 px

## Measurements
- components: final 100, mean 97.9, max 110; occupancy final 0.30
- tracks: 154; persistent (alive >= 50% of run): 100; longest 80 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 9.17 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [100, 100, 100], H1 [6, 0, 0]
- motion: 0 long-lived tracks moved >= 1 body length; max speed 0/time; max body lengths 0.7
- replication (lineage window K = 20 frames = time 2500, default): splits 7, persistent splits 2 (0 more failed only because the siblings re-merged within K), max generation 1, merges 23, merge/split ratio 3.29, nucleations 117
- channel total drift (end/start - 1): [-0.0268, -0.677, 1.5572, -0.2666]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 0 at frame 41: holes 0, rim-vs-core 0.43, rim-vs-outside 0.43, heterogeneity 0.10; core [0.925, 0.06, 0.813, 1.0] rim [0.648, 0.155, 0.497, 1.0]
  - track 1 at frame 41: holes 0, rim-vs-core 0.41, rim-vs-outside 0.42, heterogeneity 0.10; core [0.932, 0.045, 0.829, 1.0] rim [0.667, 0.153, 0.531, 1.0]
  - track 3 at frame 41: holes 0, rim-vs-core 0.46, rim-vs-outside 0.41, heterogeneity 0.10; core [0.927, 0.054, 0.773, 1.0] rim [0.635, 0.177, 0.437, 1.0]
  - track 148 at frame 46: holes 0, rim-vs-core 0.39, rim-vs-outside 0.42, heterogeneity 0.09; core [0.931, 0.051, 0.777, 1.0] rim [0.668, 0.16, 0.511, 1.0]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 599 components >= 12 px at frames [13, 27, 40, 53, 67, 80]):
  - radial phi (droplet material): peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.887, rim/outside 11.8 (aggregate of 599 individuals; 0/599 membrane-like individually; rim level 0.874)
  - radial u (fuel): peak at rho=1.85 (OUTSIDE the peak band 0.5-1.5), rim/core 15.1, rim/outside 0.839 (aggregate of 599 individuals; 0/599 membrane-like individually; rim level 0.282)
  - radial K particles: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.813, rim/outside 12.9 (aggregate of 599 individuals; 0/599 membrane-like individually; rim level 0.724)
  - radial mean rate / 2: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 1, rim/outside 2.58 (aggregate of 599 individuals; 0/599 membrane-like individually; rim level 1)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #0 (t=5125, R_eq 3.39): none; #1 (t=5125, R_eq 3.95): none; #3 (t=5125, R_eq 4.22): none; #148 (t=5750, R_eq 3.95): none

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, particles.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
