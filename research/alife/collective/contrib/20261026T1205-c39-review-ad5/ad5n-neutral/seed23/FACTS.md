# Evidence pack: ad5n-neutral (seed 23)

- world: `../../../../../threads/active-droplets/worlds/ad5n-neutral/world.py`, family `phase-field`
- parent: ad5-evolve; mutation: neutral control: all four alleles have the same catalytic rate k=0.13
- run: 201 frames x 200 steps x dt 0.5 = time 20000; grid [128, 128]; wall 225s; status ok
- command: `python -m labkit.run threads/active-droplets/worlds/ad5n-neutral/world.py --out collective/contrib/c39-rev-ad5-wip/ad5n-neutral/seed23 --seeds 23 --frames 200 --no-movie`
- segmentation: matter > 0.43 of robust range [-1.0642, 1.4227], min area 6 px

## Measurements
- components: final 10, mean 8.4, max 10; occupancy final 0.11
- tracks: 15; persistent (alive >= 50% of run): 9; longest 201 frames; alive start-to-end: 1
- size of persistent tracks: max/min area ratio 2.38 (1 = constant size)
- enclosures: components with a hole mean 0.02, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [10, 10, 10], H1 [0, 0, 0]
- motion: 4 long-lived tracks moved >= 1 body length; max speed 0.00199/time; max body lengths 2.0
- replication (lineage window K = 20 frames = time 2000, default): splits 5, persistent splits 5 (0 more failed only because the siblings re-merged within K), max generation 2, merges 0, merge/split ratio 0, nucleations 0
- channel total drift (end/start - 1): [0.0938, -0.5733, 1.3063, None, None, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 1 at frame 101: holes 0, rim-vs-core 0.44, rim-vs-outside 0.68, heterogeneity 0.07; core [0.963, 0.032, 0.951, 0.0, 0.0, 0.0] rim [0.702, 0.123, 0.603, 0.0, 0.0, 0.0]
  - track 6 at frame 106: holes 0, rim-vs-core 0.43, rim-vs-outside 0.72, heterogeneity 0.09; core [0.964, 0.035, 0.846, 0.0, 0.566, 0.0] rim [0.72, 0.126, 0.546, 0.0, 0.397, 0.0]
  - track 7 at frame 124: holes 0, rim-vs-core 0.37, rim-vs-outside 0.68, heterogeneity 0.07; core [0.967, 0.039, 0.736, 1.0, 0.0, 0.0] rim [0.722, 0.125, 0.477, 0.993, 0.0, 0.0]
  - track 13 at frame 180: holes 0, rim-vs-core 0.28, rim-vs-outside 0.56, heterogeneity 0.04; core [0.969, 0.038, 0.0, 0.0, 1.0, 0.0] rim [0.699, 0.121, 0.0, 0.0, 1.0, 0.0]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 53 components >= 12 px at frames [34, 67, 101, 133, 166, 200]):
  - radial phi (droplet material): peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.937, rim/outside 66.5 (aggregate of 53 individuals; 0/53 membrane-like individually; rim level 0.921)
  - radial u (fuel): peak at rho=2.45 (OUTSIDE the peak band 0.5-1.5), rim/core 17.4, rim/outside 0.691 (aggregate of 53 individuals; 0/53 membrane-like individually; rim level 0.224)
  - radial a0: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.893, rim/outside 73.3 (aggregate of 53 individuals; 0/53 membrane-like individually; rim level 0.824)
  - radial a1: peak at rho=0.35 (OUTSIDE the peak band 0.5-1.5), rim/core 0.966, rim/outside 6.22 (aggregate of 53 individuals; 0/53 membrane-like individually; rim level 0.0527)
  - radial a2: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.871, rim/outside 7.37 (aggregate of 53 individuals; 0/53 membrane-like individually; rim level 0.0704)
  - radial a3: peak at rho=0.45 (OUTSIDE the peak band 0.5-1.5), rim/core 1, rim/outside 6.37 (aggregate of 53 individuals; 0/53 membrane-like individually; rim level 0.0597)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #1 (t=10100, R_eq 8.02): none; #6 (t=10600, R_eq 8.18): none; #7 (t=12400, R_eq 7.69): none; #13 (t=18000, R_eq 7.46): none

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
