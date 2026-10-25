# Evidence pack: pdrop (seed 3)

- world: `../../world.py`, family `hybrid-particle-field`
- parent: threads/active-droplets/worlds/ad2-catalysts; mutation: catalyst fields -> identity-carrying Brownian particles with a heritable rate, gated by droplet material
- run: 81 frames x 250 steps x dt 0.5 = time 10000; grid [128, 128]; wall 237s; status ok
- command: `python -m labkit.run collective/contrib/20261025T1730-c13-review-pdrop/world.py --out collective/contrib/20261025T1730-c13-review-pdrop/rerun/seed3 --seeds 3 --spf 250 --frames 80 --no-movie`
- segmentation: matter > 0.46 of robust range [-1.0297, 1.2316], min area 6 px

## Measurements
- components: final 99, mean 97.9, max 107; occupancy final 0.30
- tracks: 158; persistent (alive >= 50% of run): 100; longest 80 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 9.29 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [99, 99, 99], H1 [1, 0, 0]
- motion: 0 long-lived tracks moved >= 1 body length; max speed 0/time; max body lengths 0.9
- replication (lineage window K = 20 frames = time 2500, default): splits 9, persistent splits 2 (0 more failed only because the siblings re-merged within K), max generation 1, merges 25, merge/split ratio 2.78, nucleations 115
- channel total drift (end/start - 1): [-0.03, -0.6771, 1.5519, -0.2707]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 1 at frame 41: holes 0, rim-vs-core 0.26, rim-vs-outside 0.56, heterogeneity 0.10; core [0.935, 0.055, 0.767, 1.0] rim [0.756, 0.123, 0.598, 1.0]
  - track 2 at frame 41: holes 0, rim-vs-core 0.24, rim-vs-outside 0.61, heterogeneity 0.10; core [0.915, 0.058, 0.873, 1.0] rim [0.777, 0.103, 0.685, 1.0]
  - track 3 at frame 41: holes 0, rim-vs-core 0.46, rim-vs-outside 0.41, heterogeneity 0.10; core [0.928, 0.046, 0.846, 1.0] rim [0.649, 0.156, 0.498, 1.0]
  - track 152 at frame 47: holes 0, rim-vs-core 0.21, rim-vs-outside 0.60, heterogeneity 0.11; core [0.911, 0.059, 0.779, 1.0] rim [0.766, 0.11, 0.64, 1.0]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 598 components >= 12 px at frames [13, 27, 40, 53, 67, 80]):
  - radial phi (droplet material): peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.889, rim/outside 11.9 (aggregate of 598 individuals; 0/598 membrane-like individually; rim level 0.874)
  - radial u (fuel): peak at rho=1.85 (OUTSIDE the peak band 0.5-1.5), rim/core 15, rim/outside 0.839 (aggregate of 598 individuals; 0/598 membrane-like individually; rim level 0.282)
  - radial K particles: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.81, rim/outside 13 (aggregate of 598 individuals; 0/598 membrane-like individually; rim level 0.724)
  - radial mean rate / 2: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 1, rim/outside 2.61 (aggregate of 598 individuals; 0/598 membrane-like individually; rim level 1)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #1 (t=5125, R_eq 3.7): none; #2 (t=5125, R_eq 3.34): none; #3 (t=5125, R_eq 3.91): none; #152 (t=5875, R_eq 3.87): none

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, particles.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
