# Evidence pack: pdrop (seed 8)

- world: `../../../20261025T1408-c14-pdrop-arrested/world.py`, family `hybrid-particle-field`
- parent: threads/active-droplets/worlds/ad2-catalysts; mutation: catalyst fields -> identity-carrying Brownian particles with a heritable rate, gated by droplet material
- run: 161 frames x 500 steps x dt 0.5 = time 40000; grid [128, 128]; wall 1167s; status ok
- command: `python -m labkit.run collective/contrib/20261025T1408-c14-pdrop-arrested/world.py --out collective/contrib/20261025T1602-c19-review-pdrop/long/seed8 --seeds 8 --frames 160 --spf 500 --no-movie`
- segmentation: matter > 0.45 of robust range [-1.0258, 1.2295], min area 6 px

## Measurements
- components: final 100, mean 99.5, max 112; occupancy final 0.30
- tracks: 151; persistent (alive >= 50% of run): 100; longest 160 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 4.64 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [100, 100, 100], H1 [1, 0, 0]
- motion: 1 long-lived tracks moved >= 1 body length; max speed 0.000177/time; max body lengths 1.0
- replication (lineage window K = 20 frames = time 5000, default): splits 6, persistent splits 2 (0 more failed only because the siblings re-merged within K), max generation 1, merges 21, merge/split ratio 3.5, nucleations 118
- channel total drift (end/start - 1): [-0.0142, -0.6808, 1.5624, -0.2651]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 0 at frame 81: holes 0, rim-vs-core 0.22, rim-vs-outside 0.59, heterogeneity 0.10; core [0.917, 0.061, 0.79, 1.0] rim [0.768, 0.113, 0.638, 1.0]
  - track 1 at frame 81: holes 0, rim-vs-core 0.30, rim-vs-outside 0.56, heterogeneity 0.10; core [0.941, 0.046, 0.815, 1.0] rim [0.737, 0.124, 0.606, 1.0]
  - track 2 at frame 81: holes 0, rim-vs-core 0.23, rim-vs-outside 0.60, heterogeneity 0.10; core [0.91, 0.056, 0.801, 1.0] rim [0.764, 0.112, 0.628, 1.0]
  - track 146 at frame 86: holes 0, rim-vs-core 0.39, rim-vs-outside 0.41, heterogeneity 0.09; core [0.922, 0.063, 0.711, 1.0] rim [0.639, 0.177, 0.467, 1.0]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 600 components >= 12 px at frames [27, 54, 81, 106, 133, 160]):
  - radial phi (droplet material): peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.897, rim/outside 16.3 (aggregate of 600 individuals; 0/600 membrane-like individually; rim level 0.89)
  - radial u (fuel): peak at rho=1.85 (OUTSIDE the peak band 0.5-1.5), rim/core 18.1, rim/outside 0.839 (aggregate of 600 individuals; 0/600 membrane-like individually; rim level 0.285)
  - radial K particles: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.822, rim/outside 17.6 (aggregate of 600 individuals; 0/600 membrane-like individually; rim level 0.738)
  - radial mean rate / 2: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 1, rim/outside 3.02 (aggregate of 600 individuals; 0/600 membrane-like individually; rim level 1)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #0 (t=20250, R_eq 3.74): none; #1 (t=20250, R_eq 3.78): none; #2 (t=20250, R_eq 4.3): none; #146 (t=21500, R_eq 4.15): none

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, particles.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
