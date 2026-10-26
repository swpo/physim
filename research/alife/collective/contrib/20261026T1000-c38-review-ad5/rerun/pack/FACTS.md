# Evidence pack: ad5-evolve (seed 21)

- world: `../../../../../threads/active-droplets/worlds/ad5-evolve/world.py`, family `phase-field`
- parent: ad2-catalysts; mutation: N catalyst alleles with different rates, rare local mutation patches, random dilution disks
- run: 201 frames x 200 steps x dt 0.5 = time 20000; grid [128, 128]; wall 318s; status ok
- command: `python -m labkit.run threads/active-droplets/worlds/ad5-evolve/world.py --out collective/contrib/20261026T1000-c38-review-ad5/rerun/pack --seeds 21 --frames 200 --no-movie`
- segmentation: matter > 0.42 of robust range [-1.0661, 1.4506], min area 6 px

## Measurements
- components: final 10, mean 8.4, max 10; occupancy final 0.11
- tracks: 16; persistent (alive >= 50% of run): 7; longest 201 frames; alive start-to-end: 2
- size of persistent tracks: max/min area ratio 2.77 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [10, 10, 10], H1 [0, 0, 0]
- motion: 2 long-lived tracks moved >= 1 body length; max speed 0.00157/time; max body lengths 1.3
- replication (lineage window K = 20 frames = time 2000, default): splits 5, persistent splits 5 (0 more failed only because the siblings re-merged within K), max generation 2, merges 0, merge/split ratio 0, nucleations 0
- channel total drift (end/start - 1): [0.0894, -0.5745, -0.6066, None, None, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 4 at frame 101: holes 0, rim-vs-core 0.44, rim-vs-outside 0.69, heterogeneity 0.07; core [0.97, 0.144, 0.951, 0.0, 0.0, 0.0] rim [0.705, 0.209, 0.61, 0.0, 0.0, 0.0]
  - track 5 at frame 101: holes 0, rim-vs-core 0.41, rim-vs-outside 0.71, heterogeneity 0.07; core [0.952, 0.051, 0.0, 0.995, 0.0, 0.0] rim [0.7, 0.149, 0.0, 0.686, 0.0, 0.0]
  - track 6 at frame 119: holes 0, rim-vs-core 0.45, rim-vs-outside 0.67, heterogeneity 0.07; core [0.966, 0.111, 0.965, 0.0, 0.0, 0.0] rim [0.696, 0.203, 0.617, 0.0, 0.0, 0.0]
  - track 10 at frame 141: holes 0, rim-vs-core 0.34, rim-vs-outside 0.77, heterogeneity 0.07; core [0.958, 0.021, 0.0, 0.0, 0.96, 0.01] rim [0.766, 0.089, 0.0, 0.0, 0.694, 0.008]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 51 components >= 12 px at frames [34, 67, 101, 133, 166, 200]):
  - radial phi (droplet material): peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.932, rim/outside 60.2 (aggregate of 51 individuals; 0/51 membrane-like individually; rim level 0.896)
  - radial u (fuel): peak at rho=2.45 (OUTSIDE the peak band 0.5-1.5), rim/core 5.55, rim/outside 0.711 (aggregate of 51 individuals; 0/51 membrane-like individually; rim level 0.249)
  - radial a0 (k=0.10): peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.903, rim/outside 30.6 (aggregate of 51 individuals; 0/51 membrane-like individually; rim level 0.325)
  - radial a1 (k=0.12): peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.982, rim/outside 17.9 (aggregate of 51 individuals; 0/51 membrane-like individually; rim level 0.172)
  - radial a2 (k=0.14): peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.878, rim/outside 28.4 (aggregate of 51 individuals; 0/51 membrane-like individually; rim level 0.29)
  - radial a3 (k=0.16): peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.938, rim/outside 13 (aggregate of 51 individuals; 1/51 membrane-like individually; rim level 0.124)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #4 (t=10100, R_eq 6.21): none; #5 (t=10100, R_eq 8.31): none; #6 (t=11900, R_eq 7.76): none; #10 (t=14100, R_eq 7.86): none

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
