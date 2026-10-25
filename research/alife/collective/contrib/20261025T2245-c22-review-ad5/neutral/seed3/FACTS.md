# Evidence pack: ad5n-neutral (seed 3)

- world: `../../../../../../threads/active-droplets/worlds/ad5n-neutral/world.py`, family `phase-field`
- parent: ad5-evolve; mutation: neutral control: all four alleles have the same catalytic rate k=0.13
- run: 201 frames x 200 steps x dt 0.5 = time 20000; grid [128, 128]; wall 179s; status ok
- command: `python -m labkit.run threads/active-droplets/worlds/ad5n-neutral/world.py --out collective/contrib/wip-c22/rev_ad5/neutral/seed3 --seeds 3 --frames 200 --no-movie`
- segmentation: matter > 0.43 of robust range [-1.0624, 1.4228], min area 6 px

## Measurements
- components: final 10, mean 9.1, max 10; occupancy final 0.11
- tracks: 17; persistent (alive >= 50% of run): 10; longest 201 frames; alive start-to-end: 1
- size of persistent tracks: max/min area ratio 2.81 (1 = constant size)
- enclosures: components with a hole mean 0.07, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [10, 10, 10], H1 [0, 0, 0]
- motion: 2 long-lived tracks moved >= 1 body length; max speed 0.00107/time; max body lengths 1.2
- replication (lineage window K = 20 frames = time 2000, default): splits 5, persistent splits 4 (0 more failed only because the siblings re-merged within K), max generation 1, merges 1, merge/split ratio 0.2, nucleations 0
- channel total drift (end/start - 1): [0.09, -0.5768, 0.8558, None, None, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 3 at frame 101: holes 0, rim-vs-core 0.35, rim-vs-outside 0.65, heterogeneity 0.08; core [0.96, 0.04, 0.571, 0.002, 0.0, 1.0] rim [0.696, 0.13, 0.362, 0.001, 0.0, 0.987]
  - track 8 at frame 103: holes 0, rim-vs-core 0.44, rim-vs-outside 0.68, heterogeneity 0.07; core [0.97, 0.036, 0.934, 0.015, 0.0, 0.0] rim [0.708, 0.12, 0.595, 0.011, 0.0, 0.0]
  - track 9 at frame 116: holes 0, rim-vs-core 0.44, rim-vs-outside 0.68, heterogeneity 0.07; core [0.97, 0.035, 0.948, 0.0, 0.0, 0.0] rim [0.705, 0.119, 0.603, 0.0, 0.0, 0.0]
  - track 10 at frame 116: holes 0, rim-vs-core 0.26, rim-vs-outside 0.84, heterogeneity 0.07; core [0.957, 0.035, 0.943, 0.0, 0.0, 0.0] rim [0.803, 0.086, 0.738, 0.0, 0.0, 0.0]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 57 components >= 12 px at frames [34, 67, 101, 133, 166, 200]):
  - radial phi (droplet material): peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.938, rim/outside 63.1 (aggregate of 57 individuals; 0/57 membrane-like individually; rim level 0.924)
  - radial u (fuel): peak at rho=2.45 (OUTSIDE the peak band 0.5-1.5), rim/core 15.9, rim/outside 0.696 (aggregate of 57 individuals; 0/57 membrane-like individually; rim level 0.223)
  - radial a0: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.888, rim/outside 52.5 (aggregate of 57 individuals; 0/57 membrane-like individually; rim level 0.658)
  - radial a1: peak at rho=0.35 (OUTSIDE the peak band 0.5-1.5), rim/core 0.981, rim/outside 15.6 (aggregate of 57 individuals; 0/57 membrane-like individually; rim level 0.148)
  - radial a2: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.994, rim/outside 10.6 (aggregate of 57 individuals; 0/57 membrane-like individually; rim level 0.0979)
  - radial a3: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.929, rim/outside 5.67 (aggregate of 57 individuals; 0/57 membrane-like individually; rim level 0.0488)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #3 (t=10100, R_eq 8): none; #8 (t=10300, R_eq 7.51): none; #9 (t=11600, R_eq 7.48): none; #10 (t=11600, R_eq 7.88): none

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
