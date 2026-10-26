# Evidence pack: ad5-evolve (seed 25)

- world: `../../../../../threads/active-droplets/worlds/ad5-evolve/world.py`, family `phase-field`
- parent: ad2-catalysts; mutation: N catalyst alleles with different rates, rare local mutation patches, random dilution disks
- run: 201 frames x 200 steps x dt 0.5 = time 20000; grid [128, 128]; wall 314s; status ok
- command: `python -m labkit.run threads/active-droplets/worlds/ad5-evolve/world.py --out collective/contrib/20261025T2213-c24-review-ad5/ad5-evolve/seed25 --seeds 25 --frames 200 --no-movie`
- segmentation: matter > 0.42 of robust range [-1.0677, 1.4492], min area 6 px

## Measurements
- components: final 11, mean 7.8, max 11; occupancy final 0.11
- tracks: 16; persistent (alive >= 50% of run): 7; longest 201 frames; alive start-to-end: 4
- size of persistent tracks: max/min area ratio 4.54 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [11, 11, 11], H1 [0, 0, 0]
- motion: 1 long-lived tracks moved >= 1 body length; max speed 0.00132/time; max body lengths 1.1
- replication (lineage window K = 20 frames = time 2000, default): splits 5, persistent splits 5 (0 more failed only because the siblings re-merged within K), max generation 3, merges 0, merge/split ratio 0, nucleations 0
- channel total drift (end/start - 1): [0.0874, -0.57, -0.3124, None, None, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 0 at frame 101: holes 0, rim-vs-core 0.21, rim-vs-outside 0.78, heterogeneity 0.07; core [0.939, 0.078, 0.727, 0.0, 0.0, 0.276] rim [0.801, 0.127, 0.584, 0.0, 0.0, 0.22]
  - track 1 at frame 101: holes 0, rim-vs-core 0.46, rim-vs-outside 0.67, heterogeneity 0.07; core [0.964, 0.105, 0.959, 0.0, 0.0, 0.0] rim [0.688, 0.202, 0.604, 0.0, 0.0, 0.0]
  - track 3 at frame 101: holes 0, rim-vs-core 0.43, rim-vs-outside 0.67, heterogeneity 0.07; core [0.952, 0.022, 0.024, 0.0, 0.943, 0.0] rim [0.706, 0.108, 0.017, 0.0, 0.604, 0.0]
  - track 12 at frame 185: holes 0, rim-vs-core 0.29, rim-vs-outside 0.67, heterogeneity 0.05; core [0.955, 0.057, 0.0, 1.0, 0.0, 0.311] rim [0.693, 0.126, 0.0, 1.0, 0.0, 0.206]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 49 components >= 12 px at frames [34, 67, 101, 133, 166, 200]):
  - radial phi (droplet material): peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.945, rim/outside 55.1 (aggregate of 49 individuals; 0/49 membrane-like individually; rim level 0.918)
  - radial u (fuel): peak at rho=2.45 (OUTSIDE the peak band 0.5-1.5), rim/core 6.04, rim/outside 0.709 (aggregate of 49 individuals; 0/49 membrane-like individually; rim level 0.256)
  - radial a0 (k=0.10): peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.918, rim/outside 40.7 (aggregate of 49 individuals; 0/49 membrane-like individually; rim level 0.416)
  - radial a1 (k=0.12): peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.949, rim/outside 8.61 (aggregate of 49 individuals; 0/49 membrane-like individually; rim level 0.0828)
  - radial a2 (k=0.14): peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.892, rim/outside 28.3 (aggregate of 49 individuals; 0/49 membrane-like individually; rim level 0.329)
  - radial a3 (k=0.16): peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.914, rim/outside 13.7 (aggregate of 49 individuals; 0/49 membrane-like individually; rim level 0.135)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #0 (t=10100, R_eq 8.48): none; #1 (t=10100, R_eq 8.12): none; #3 (t=10100, R_eq 8.04): none; #12 (t=18500, R_eq 6.63): none

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
