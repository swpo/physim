# Evidence pack: marangoni-droplets (seed 2)

- world: `../../world.py`, family `phase-field`
- parent: threads/active-droplets/worlds/ad1-fuel; mutation: self-generated Brinkman flow from a fuel-dependent interfacial stress advects droplets and fuel
- run: 201 frames x 200 steps x dt 0.5 = time 20000; grid [128, 128]; wall 283s; status ok
- command: `python -m labkit.run collective/contrib/20261025T1410-c13-review-marangoni/world.py --out collective/contrib/20261025T1410-c13-review-marangoni/rerun_a0/seed2 --seeds 2 --no-movie`
- segmentation: matter > 0.45 of robust range [-1.0484, 1.2719], min area 6 px

## Measurements
- components: final 16, mean 11.0, max 16; occupancy final 0.12
- tracks: 30; persistent (alive >= 50% of run): 8; longest 156 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 1.49 (1 = constant size)
- enclosures: components with a hole mean 0.07, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [16, 16, 16], H1 [0, 0, 0]
- motion: 6 long-lived tracks moved >= 1 body length; max speed 0.00318/time; max body lengths 1.4
- replication (lineage window K = 20 frames = time 2000, default): splits 14, persistent splits 10 (0 more failed only because the siblings re-merged within K), max generation 2, merges 0, merge/split ratio 0, nucleations 0
- channel total drift (end/start - 1): [0.1643, -0.6351, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 12 at frame 123: holes 0, rim-vs-core 0.24, rim-vs-outside 0.53, heterogeneity 0.08; core [0.976, 0.022, 0.104] rim [0.742, 0.081, 0.11]
  - track 13 at frame 123: holes 0, rim-vs-core 0.25, rim-vs-outside 0.53, heterogeneity 0.08; core [0.975, 0.023, 0.102] rim [0.736, 0.082, 0.106]
  - track 15 at frame 133: holes 0, rim-vs-core 0.16, rim-vs-outside 0.62, heterogeneity 0.09; core [0.966, 0.024, 0.183] rim [0.807, 0.063, 0.189]
  - track 22 at frame 158: holes 0, rim-vs-core 0.23, rim-vs-outside 0.53, heterogeneity 0.08; core [0.972, 0.02, 0.117] rim [0.746, 0.083, 0.12]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 74 components >= 12 px at frames [34, 67, 101, 133, 166, 200]):
  - radial phi (droplet material): peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.932, rim/outside 47.3 (aggregate of 74 individuals; 0/74 membrane-like individually; rim level 0.91)
  - radial u (fuel): peak at rho=2.45 (OUTSIDE the peak band 0.5-1.5), rim/core 13.8, rim/outside 0.684 (aggregate of 74 individuals; 0/74 membrane-like individually; rim level 0.166)
  - radial |v| (flow speed): peak at rho=0.55 (in the peak band 0.5-1.5), rim/core 1.17, rim/outside 3.28 (aggregate of 74 individuals; 43/74 membrane-like individually; rim level 0.235)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #12 (t=12300, R_eq 6.1): ['|v| (flow speed)']; #13 (t=12300, R_eq 6.13): ['|v| (flow speed)']; #15 (t=13300, R_eq 6.58): ['|v| (flow speed)']; #22 (t=15800, R_eq 6.43): ['|v| (flow speed)']

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
