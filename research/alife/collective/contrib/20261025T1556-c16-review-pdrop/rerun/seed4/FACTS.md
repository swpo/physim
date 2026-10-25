# Evidence pack: pdrop (seed 4)

- world: `../../../20261025T1408-c14-pdrop-arrested/world.py`, family `hybrid-particle-field`
- parent: threads/active-droplets/worlds/ad2-catalysts; mutation: catalyst fields -> identity-carrying Brownian particles with a heritable rate, gated by droplet material
- run: 81 frames x 250 steps x dt 0.5 = time 10000; grid [128, 128]; wall 438s; status ok
- command: `python -m labkit.run collective/contrib/20261025T1408-c14-pdrop-arrested/world.py --out collective/contrib/20261025T1556-c16-review-pdrop/rerun/seed4 --seeds 4 --frames 80 --spf 250 --no-movie`
- segmentation: matter > 0.46 of robust range [-1.0284, 1.2313], min area 6 px

## Measurements
- components: final 101, mean 100.0, max 123; occupancy final 0.30
- tracks: 188; persistent (alive >= 50% of run): 101; longest 80 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 9.00 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [101, 101, 101], H1 [1, 0, 0]
- motion: 0 long-lived tracks moved >= 1 body length; max speed 0/time; max body lengths 0.5
- replication (lineage window K = 20 frames = time 2500, default): splits 11, persistent splits 4 (0 more failed only because the siblings re-merged within K), max generation 1, merges 35, merge/split ratio 3.18, nucleations 131
- channel total drift (end/start - 1): [-0.0245, -0.6791, 1.5237, -0.2657]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 1 at frame 41: holes 0, rim-vs-core 0.23, rim-vs-outside 0.60, heterogeneity 0.11; core [0.909, 0.063, 0.764, 1.0] rim [0.75, 0.119, 0.614, 1.0]
  - track 2 at frame 41: holes 0, rim-vs-core 0.37, rim-vs-outside 0.46, heterogeneity 0.10; core [0.931, 0.054, 0.748, 1.0] rim [0.676, 0.159, 0.504, 1.0]
  - track 4 at frame 41: holes 0, rim-vs-core 0.37, rim-vs-outside 0.42, heterogeneity 0.09; core [0.939, 0.05, 0.78, 1.0] rim [0.693, 0.153, 0.524, 1.0]
  - track 176 at frame 47: holes 0, rim-vs-core 0.44, rim-vs-outside 0.41, heterogeneity 0.10; core [0.928, 0.051, 0.791, 1.0] rim [0.639, 0.168, 0.476, 1.0]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 608 components >= 12 px at frames [13, 27, 40, 53, 67, 80]):
  - radial phi (droplet material): peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.886, rim/outside 12.6 (aggregate of 608 individuals; 0/608 membrane-like individually; rim level 0.869)
  - radial u (fuel): peak at rho=1.75 (OUTSIDE the peak band 0.5-1.5), rim/core 14.3, rim/outside 0.841 (aggregate of 608 individuals; 0/608 membrane-like individually; rim level 0.279)
  - radial K particles: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.81, rim/outside 13.7 (aggregate of 608 individuals; 0/608 membrane-like individually; rim level 0.717)
  - radial mean rate / 2: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.999, rim/outside 2.57 (aggregate of 608 individuals; 0/608 membrane-like individually; rim level 0.999)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #1 (t=5125, R_eq 3.99): none; #2 (t=5125, R_eq 4.07): none; #4 (t=5125, R_eq 3.74): none; #176 (t=5875, R_eq 4.07): none

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, particles.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
