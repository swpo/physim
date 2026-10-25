# Evidence pack: marangoni-droplets (seed 1)

- world: `../../world.py`, family `phase-field`
- parent: threads/active-droplets/worlds/ad1-fuel; mutation: self-generated Brinkman flow from a fuel-dependent interfacial stress advects droplets and fuel
- run: 201 frames x 200 steps x dt 0.5 = time 20000; grid [128, 128]; wall 269s; status ok
- command: `python -m labkit.run collective/contrib/20261025T0946-c01-marangoni-droplets/world.py --out collective/contrib/20261025T0946-c01-marangoni-droplets/pack_a0 --seeds 0 1 --no-movie`
- segmentation: matter > 0.45 of robust range [-1.0481, 1.2682], min area 6 px

## Measurements
- components: final 14, mean 10.6, max 14; occupancy final 0.11
- tracks: 26; persistent (alive >= 50% of run): 14; longest 164 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 1.61 (1 = constant size)
- enclosures: components with a hole mean 0.15, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [14, 14, 14], H1 [0, 0, 0]
- motion: 10 long-lived tracks moved >= 1 body length; max speed 0.00323/time; max body lengths 1.5
- replication (lineage window K = 20 frames = time 2000, default): splits 12, persistent splits 12 (0 more failed only because the siblings re-merged within K), max generation 3, merges 0, merge/split ratio 0, nucleations 0
- channel total drift (end/start - 1): [0.1576, -0.6218, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 10 at frame 119: holes 0, rim-vs-core 0.14, rim-vs-outside 0.62, heterogeneity 0.08; core [0.966, 0.031, 0.198] rim [0.828, 0.061, 0.197]
  - track 11 at frame 119: holes 0, rim-vs-core 0.26, rim-vs-outside 0.53, heterogeneity 0.09; core [0.978, 0.025, 0.181] rim [0.724, 0.086, 0.19]
  - track 14 at frame 134: holes 0, rim-vs-core 0.23, rim-vs-outside 0.53, heterogeneity 0.09; core [0.963, 0.021, 0.254] rim [0.745, 0.09, 0.245]
  - track 15 at frame 134: holes 0, rim-vs-core 0.24, rim-vs-outside 0.53, heterogeneity 0.07; core [0.979, 0.023, 0.064] rim [0.744, 0.084, 0.07]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 70 components >= 12 px at frames [34, 67, 101, 133, 166, 200]):
  - radial phi (droplet material): peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.946, rim/outside 47.2 (aggregate of 70 individuals; 0/70 membrane-like individually; rim level 0.908)
  - radial u (fuel): peak at rho=2.45 (OUTSIDE the peak band 0.5-1.5), rim/core 11.8, rim/outside 0.68 (aggregate of 70 individuals; 0/70 membrane-like individually; rim level 0.171)
  - radial |v| (flow speed): peak at rho=0.65 (in the peak band 0.5-1.5), rim/core 1.32, rim/outside 3.33 (aggregate of 70 individuals; 42/70 membrane-like individually; rim level 0.261)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #10 (t=11900, R_eq 6.15): ['|v| (flow speed)']; #11 (t=11900, R_eq 6.23): ['|v| (flow speed)']; #14 (t=13400, R_eq 7): ['|v| (flow speed)']; #15 (t=13400, R_eq 6.28): none

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
