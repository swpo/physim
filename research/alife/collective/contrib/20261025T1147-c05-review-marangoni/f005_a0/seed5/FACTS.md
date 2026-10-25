# Evidence pack: marangoni-droplets (seed 5)

- world: `../../../../contrib/20261025T0946-c01-marangoni-droplets/world.py`, family `phase-field`
- parent: threads/active-droplets/worlds/ad1-fuel; mutation: self-generated Brinkman flow from a fuel-dependent interfacial stress advects droplets and fuel
- run: 201 frames x 200 steps x dt 0.5 = time 20000; grid [128, 128]; wall 281s; status ok
- command: `python -m labkit.run collective/contrib/20261025T0946-c01-marangoni-droplets/world.py --out collective/work_c05/rev_mg/f005_a0/seed5 --seeds 5 --no-movie`
- segmentation: matter > 0.45 of robust range [-1.0483, 1.2711], min area 6 px

## Measurements
- components: final 16, mean 11.0, max 16; occupancy final 0.12
- tracks: 30; persistent (alive >= 50% of run): 8; longest 146 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 1.38 (1 = constant size)
- enclosures: components with a hole mean 0.06, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [16, 16, 16], H1 [0, 0, 0]
- motion: 8 long-lived tracks moved >= 1 body length; max speed 0.00264/time; max body lengths 1.4
- replication (lineage window K = 20 frames = time 2000, default): splits 14, persistent splits 10 (0 more failed only because the siblings re-merged within K), max generation 2, merges 0, merge/split ratio 0, nucleations 0
- channel total drift (end/start - 1): [0.1641, -0.6347, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 10 at frame 128: holes 0, rim-vs-core 0.23, rim-vs-outside 0.55, heterogeneity 0.08; core [0.978, 0.02, 0.119] rim [0.759, 0.078, 0.132]
  - track 11 at frame 128: holes 0, rim-vs-core 0.23, rim-vs-outside 0.53, heterogeneity 0.08; core [0.976, 0.021, 0.124] rim [0.753, 0.08, 0.133]
  - track 12 at frame 128: holes 0, rim-vs-core 0.19, rim-vs-outside 0.60, heterogeneity 0.11; core [0.964, 0.029, 0.453] rim [0.8, 0.062, 0.362]
  - track 22 at frame 166: holes 0, rim-vs-core 0.30, rim-vs-outside 0.32, heterogeneity 0.07; core [0.938, 0.038, 0.048] rim [0.64, 0.093, 0.052]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 78 components >= 12 px at frames [34, 67, 101, 133, 166, 200]):
  - radial phi (droplet material): peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.948, rim/outside 44.6 (aggregate of 78 individuals; 0/78 membrane-like individually; rim level 0.935)
  - radial u (fuel): peak at rho=2.45 (OUTSIDE the peak band 0.5-1.5), rim/core 13.3, rim/outside 0.693 (aggregate of 78 individuals; 0/78 membrane-like individually; rim level 0.164)
  - radial |v| (flow speed): peak at rho=0.55 (in the peak band 0.5-1.5), rim/core 1.23, rim/outside 2.99 (aggregate of 78 individuals; 47/78 membrane-like individually; rim level 0.207)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #10 (t=12800, R_eq 6.21): ['|v| (flow speed)']; #11 (t=12800, R_eq 6.15): ['|v| (flow speed)']; #12 (t=12800, R_eq 6.7): ['|v| (flow speed)']; #22 (t=16600, R_eq 5.89): none

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
