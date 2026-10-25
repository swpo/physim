# Evidence pack: pdrop (seed 0)

- world: `../../world.py`, family `hybrid-particle-field`
- parent: threads/active-droplets/worlds/ad2-catalysts; mutation: catalyst fields -> identity-carrying Brownian particles with a heritable rate, gated by droplet material
- run: 81 frames x 250 steps x dt 0.5 = time 10000; grid [128, 128]; wall 313s; status ok
- command: `python -m labkit.run scratch/c14/pdrop/world.py --out scratch/c14/pdrop/pack/seed0 --seeds 0 --frames 80 --spf 250 --no-movie`
- segmentation: matter > 0.45 of robust range [-1.0273, 1.2319], min area 6 px

## Measurements
- components: final 102, mean 102.9, max 125; occupancy final 0.30
- tracks: 162; persistent (alive >= 50% of run): 104; longest 80 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 9.62 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [103, 103, 102], H1 [2, 0, 0]
- motion: 0 long-lived tracks moved >= 1 body length; max speed 0/time; max body lengths 0.7
- replication (lineage window K = 20 frames = time 2500, default): splits 5, persistent splits 3 (0 more failed only because the siblings re-merged within K), max generation 1, merges 26, merge/split ratio 5.2, nucleations 126
- channel total drift (end/start - 1): [-0.0168, -0.6811, 1.5791, -0.259]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 1 at frame 41: holes 0, rim-vs-core 0.41, rim-vs-outside 0.42, heterogeneity 0.10; core [0.934, 0.059, 0.761, 1.0] rim [0.667, 0.16, 0.469, 1.0]
  - track 2 at frame 41: holes 0, rim-vs-core 0.46, rim-vs-outside 0.41, heterogeneity 0.11; core [0.921, 0.055, 0.824, 1.0] rim [0.636, 0.16, 0.482, 1.0]
  - track 5 at frame 41: holes 0, rim-vs-core 0.42, rim-vs-outside 0.42, heterogeneity 0.10; core [0.931, 0.046, 0.827, 1.0] rim [0.657, 0.152, 0.521, 1.0]
  - track 150 at frame 45: holes 0, rim-vs-core 0.48, rim-vs-outside 0.40, heterogeneity 0.11; core [0.918, 0.067, 0.749, 1.0] rim [0.599, 0.188, 0.412, 1.0]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 625 components >= 12 px at frames [13, 27, 40, 53, 67, 80]):
  - radial phi (droplet material): peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.886, rim/outside 12.2 (aggregate of 625 individuals; 0/625 membrane-like individually; rim level 0.869)
  - radial u (fuel): peak at rho=1.75 (OUTSIDE the peak band 0.5-1.5), rim/core 13.6, rim/outside 0.839 (aggregate of 625 individuals; 0/625 membrane-like individually; rim level 0.276)
  - radial K particles: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.807, rim/outside 13.2 (aggregate of 625 individuals; 0/625 membrane-like individually; rim level 0.716)
  - radial mean rate / 2: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 1, rim/outside 2.55 (aggregate of 625 individuals; 0/625 membrane-like individually; rim level 1)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #1 (t=5125, R_eq 3.66): none; #2 (t=5125, R_eq 3.66): none; #5 (t=5125, R_eq 3.78): none; #150 (t=5625, R_eq 3.99): none

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, particles.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
