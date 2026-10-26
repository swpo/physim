# Evidence pack: ad5-evolve (seed 23)

- world: `../../../../../threads/active-droplets/worlds/ad5-evolve/world.py`, family `phase-field`
- parent: ad2-catalysts; mutation: N catalyst alleles with different rates, rare local mutation patches, random dilution disks
- run: 201 frames x 200 steps x dt 0.5 = time 20000; grid [128, 128]; wall 226s; status ok
- command: `python -m labkit.run threads/active-droplets/worlds/ad5-evolve/world.py --out collective/contrib/c39-rev-ad5-wip/ad5-evolve/seed23 --seeds 23 --frames 200 --no-movie`
- segmentation: matter > 0.42 of robust range [-1.0681, 1.4455], min area 6 px

## Measurements
- components: final 10, mean 6.4, max 10; occupancy final 0.11
- tracks: 15; persistent (alive >= 50% of run): 6; longest 201 frames; alive start-to-end: 3
- size of persistent tracks: max/min area ratio 2.96 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [10, 10, 10], H1 [0, 0, 0]
- motion: 4 long-lived tracks moved >= 1 body length; max speed 0.00209/time; max body lengths 1.6
- replication (lineage window K = 20 frames = time 2000, default): splits 5, persistent splits 3 (0 more failed only because the siblings re-merged within K), max generation 2, merges 0, merge/split ratio 0, nucleations 0
- channel total drift (end/start - 1): [0.08, -0.5463, -0.2477, None, None, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 1 at frame 101: holes 0, rim-vs-core 0.45, rim-vs-outside 0.68, heterogeneity 0.07; core [0.971, 0.089, 0.95, 0.0, 0.0, 0.0] rim [0.703, 0.182, 0.606, 0.0, 0.0, 0.0]
  - track 3 at frame 101: holes 0, rim-vs-core 0.41, rim-vs-outside 0.63, heterogeneity 0.11; core [0.966, 0.065, 0.753, 0.0, 0.295, 0.0] rim [0.701, 0.167, 0.464, 0.0, 0.212, 0.0]
  - track 4 at frame 101: holes 0, rim-vs-core 0.44, rim-vs-outside 0.67, heterogeneity 0.07; core [0.962, 0.072, 0.961, 0.0, 0.0, 0.0] rim [0.71, 0.184, 0.623, 0.0, 0.0, 0.0]
  - track 10 at frame 176: holes 0, rim-vs-core 0.42, rim-vs-outside 0.70, heterogeneity 0.07; core [0.972, 0.046, 0.0, 0.984, 0.0, 0.0] rim [0.714, 0.124, 0.0, 0.656, 0.0, 0.0]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 42 components >= 12 px at frames [34, 67, 101, 133, 166, 200]):
  - radial phi (droplet material): peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.943, rim/outside 44.2 (aggregate of 42 individuals; 0/42 membrane-like individually; rim level 0.923)
  - radial u (fuel): peak at rho=2.45 (OUTSIDE the peak band 0.5-1.5), rim/core 8.21, rim/outside 0.694 (aggregate of 42 individuals; 0/42 membrane-like individually; rim level 0.257)
  - radial a0 (k=0.10): peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.91, rim/outside 39.8 (aggregate of 42 individuals; 0/42 membrane-like individually; rim level 0.505)
  - radial a1 (k=0.12): peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.899, rim/outside 18.1 (aggregate of 42 individuals; 0/42 membrane-like individually; rim level 0.175)
  - radial a2 (k=0.14): peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.984, rim/outside 12.9 (aggregate of 42 individuals; 0/42 membrane-like individually; rim level 0.121)
  - radial a3 (k=0.16): peak at rho=0.45 (OUTSIDE the peak band 0.5-1.5), rim/core 0.999, rim/outside 10.7 (aggregate of 42 individuals; 0/42 membrane-like individually; rim level 0.143)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #1 (t=10100, R_eq 7.69): none; #3 (t=10100, R_eq 8.29): none; #4 (t=10100, R_eq 8.72): none; #10 (t=17600, R_eq 6.91): none

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
