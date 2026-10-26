# Evidence pack: ad5n-neutral (seed 7)

- world: `../../../../../threads/active-droplets/worlds/ad5n-neutral/world.py`, family `phase-field`
- parent: ad5-evolve; mutation: neutral control: all four alleles have the same catalytic rate k=0.13
- run: 201 frames x 200 steps x dt 0.5 = time 20000; grid [128, 128]; wall 181s; status ok
- command: `python -m labkit.run threads/active-droplets/worlds/ad5n-neutral/world.py --out collective/contrib/_c26work/rev7/neutral --seeds 7 --frames 200 --no-movie`
- segmentation: matter > 0.43 of robust range [-1.0656, 1.4367], min area 6 px

## Measurements
- components: final 10, mean 8.6, max 11; occupancy final 0.11
- tracks: 19; persistent (alive >= 50% of run): 9; longest 195 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 2.93 (1 = constant size)
- enclosures: components with a hole mean 0.05, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [10, 10, 10], H1 [0, 0, 0]
- motion: 4 long-lived tracks moved >= 1 body length; max speed 0.00246/time; max body lengths 1.3
- replication (lineage window K = 20 frames = time 2000, default): splits 7, persistent splits 6 (0 more failed only because the siblings re-merged within K), max generation 2, merges 0, merge/split ratio 0, nucleations 0
- channel total drift (end/start - 1): [0.087, -0.5625, 0.5561, None, None, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 5 at frame 104: holes 0, rim-vs-core 0.31, rim-vs-outside 0.79, heterogeneity 0.06; core [0.968, 0.036, 0.0, 0.0, 1.0, 0.0] rim [0.71, 0.117, 0.0, 0.0, 0.844, 0.0]
  - track 6 at frame 104: holes 0, rim-vs-core 0.25, rim-vs-outside 0.87, heterogeneity 0.07; core [0.955, 0.047, 0.0, 0.989, 0.0, 0.0] rim [0.803, 0.085, 0.0, 0.789, 0.0, 0.0]
  - track 3 at frame 76: holes 0, rim-vs-core 0.40, rim-vs-outside 0.64, heterogeneity 0.07; core [0.943, 0.029, 0.829, 0.127, 0.0, 0.002] rim [0.703, 0.133, 0.523, 0.088, 0.0, 0.001]
  - track 15 at frame 171: holes 0, rim-vs-core 0.41, rim-vs-outside 0.69, heterogeneity 0.07; core [0.973, 0.05, 0.942, 0.0, 0.0, 0.0] rim [0.724, 0.116, 0.617, 0.0, 0.0, 0.0]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 54 components >= 12 px at frames [34, 67, 101, 133, 166, 200]):
  - radial phi (droplet material): peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.927, rim/outside 53.9 (aggregate of 54 individuals; 0/54 membrane-like individually; rim level 0.901)
  - radial u (fuel): peak at rho=2.45 (OUTSIDE the peak band 0.5-1.5), rim/core 13.6, rim/outside 0.693 (aggregate of 54 individuals; 0/54 membrane-like individually; rim level 0.221)
  - radial a0: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.875, rim/outside 42.9 (aggregate of 54 individuals; 0/54 membrane-like individually; rim level 0.545)
  - radial a1: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.939, rim/outside 17.6 (aggregate of 54 individuals; 0/54 membrane-like individually; rim level 0.174)
  - radial a2: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.971, rim/outside 11 (aggregate of 54 individuals; 0/54 membrane-like individually; rim level 0.107)
  - radial a3: peak at rho=0.25 (OUTSIDE the peak band 0.5-1.5), rim/core 0.976, rim/outside 9.74 (aggregate of 54 individuals; 0/54 membrane-like individually; rim level 0.0883)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #5 (t=10400, R_eq 7.31): none; #6 (t=10400, R_eq 7.29): none; #3 (t=7600, R_eq 8.97): none; #15 (t=17100, R_eq 6.43): none

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
