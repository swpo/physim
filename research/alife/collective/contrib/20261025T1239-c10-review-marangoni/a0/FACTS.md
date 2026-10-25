# Evidence pack: marangoni-droplets (seed 7)

- world: `../../20261025T0946-c01-marangoni-droplets/world.py`, family `phase-field`
- parent: threads/active-droplets/worlds/ad1-fuel; mutation: self-generated Brinkman flow from a fuel-dependent interfacial stress advects droplets and fuel
- run: 201 frames x 200 steps x dt 0.5 = time 20000; grid [128, 128]; wall 346s; status ok
- command: `python -m labkit.run collective/contrib/20261025T0946-c01-marangoni-droplets/world.py --out collective/contrib/20261025T1239-c10-review-marangoni/a0 --seeds 7 --no-movie`
- segmentation: matter > 0.45 of robust range [-1.0483, 1.2751], min area 6 px

## Measurements
- components: final 16, mean 11.1, max 16; occupancy final 0.11
- tracks: 30; persistent (alive >= 50% of run): 12; longest 112 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 1.39 (1 = constant size)
- enclosures: components with a hole mean 0.01, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [16, 16, 16], H1 [0, 0, 0]
- motion: 10 long-lived tracks moved >= 1 body length; max speed 0.00346/time; max body lengths 1.4
- replication (lineage window K = 20 frames = time 2000, default): splits 14, persistent splits 14 (0 more failed only because the siblings re-merged within K), max generation 3, merges 0, merge/split ratio 0, nucleations 0
- channel total drift (end/start - 1): [0.1644, -0.6351, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 14 at frame 145: holes 0, rim-vs-core 0.19, rim-vs-outside 0.58, heterogeneity 0.07; core [0.977, 0.018, 0.077] rim [0.793, 0.068, 0.095]
  - track 15 at frame 145: holes 0, rim-vs-core 0.32, rim-vs-outside 0.32, heterogeneity 0.07; core [0.935, 0.038, 0.046] rim [0.618, 0.095, 0.049]
  - track 16 at frame 145: holes 0, rim-vs-core 0.32, rim-vs-outside 0.31, heterogeneity 0.07; core [0.938, 0.038, 0.045] rim [0.625, 0.095, 0.049]
  - track 17 at frame 145: holes 0, rim-vs-core 0.25, rim-vs-outside 0.53, heterogeneity 0.07; core [0.971, 0.021, 0.086] rim [0.733, 0.083, 0.091]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 76 components >= 12 px at frames [34, 67, 101, 133, 166, 200]):
  - radial phi (droplet material): peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.948, rim/outside 47.5 (aggregate of 76 individuals; 0/76 membrane-like individually; rim level 0.923)
  - radial u (fuel): peak at rho=2.45 (OUTSIDE the peak band 0.5-1.5), rim/core 12.1, rim/outside 0.686 (aggregate of 76 individuals; 0/76 membrane-like individually; rim level 0.162)
  - radial |v| (flow speed): peak at rho=0.45 (OUTSIDE the peak band 0.5-1.5), rim/core 0.987, rim/outside 3.04 (aggregate of 76 individuals; 35/76 membrane-like individually; rim level 0.16)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #14 (t=14500, R_eq 6.31): ['|v| (flow speed)']; #15 (t=14500, R_eq 5.97): ['|v| (flow speed)']; #16 (t=14500, R_eq 5.94): ['|v| (flow speed)']; #17 (t=14500, R_eq 6.33): ['|v| (flow speed)']

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
