# Evidence pack: ad5-evolve (seed 7)

- world: `../../../../threads/active-droplets/worlds/ad5-evolve/world.py`, family `phase-field`
- parent: ad2-catalysts; mutation: N catalyst alleles with different rates, rare local mutation patches, random dilution disks
- run: 201 frames x 200 steps x dt 0.5 = time 20000; grid [128, 128]; wall 305s; status ok
- command: `python -m labkit.run threads/active-droplets/worlds/ad5-evolve/world.py --out collective/contrib/wip-c33-ad5/pack7 --seeds 7 --frames 200 --no-movie`
- segmentation: matter > 0.42 of robust range [-1.0665, 1.4537], min area 6 px

## Measurements
- components: final 10, mean 7.3, max 10; occupancy final 0.11
- tracks: 15; persistent (alive >= 50% of run): 8; longest 201 frames; alive start-to-end: 1
- size of persistent tracks: max/min area ratio 2.61 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [10, 10, 10], H1 [0, 0, 0]
- motion: 4 long-lived tracks moved >= 1 body length; max speed 0.00159/time; max body lengths 1.6
- replication (lineage window K = 20 frames = time 2000, default): splits 5, persistent splits 5 (0 more failed only because the siblings re-merged within K), max generation 2, merges 0, merge/split ratio 0, nucleations 0
- channel total drift (end/start - 1): [0.085, -0.5624, -0.4131, None, None, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 3 at frame 101: holes 0, rim-vs-core 0.45, rim-vs-outside 0.67, heterogeneity 0.07; core [0.953, 0.076, 0.943, 0.0, 0.0, 0.071] rim [0.69, 0.188, 0.594, 0.0, 0.0, 0.05]
  - track 2 at frame 81: holes 0, rim-vs-core 0.36, rim-vs-outside 0.60, heterogeneity 0.07; core [0.959, 0.046, 0.439, 0.014, 0.485, 0.0] rim [0.702, 0.146, 0.279, 0.009, 0.31, 0.0]
  - track 5 at frame 123: holes 0, rim-vs-core 0.42, rim-vs-outside 0.69, heterogeneity 0.07; core [0.972, 0.098, 0.956, 0.0, 0.0, 0.0] rim [0.722, 0.184, 0.629, 0.0, 0.0, 0.0]
  - track 7 at frame 143: holes 0, rim-vs-core 0.46, rim-vs-outside 0.67, heterogeneity 0.07; core [0.946, 0.013, 0.0, 0.0, 0.942, 0.169] rim [0.682, 0.097, 0.0, 0.0, 0.582, 0.116]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 47 components >= 12 px at frames [34, 67, 101, 133, 166, 200]):
  - radial phi (droplet material): peak at rho=0.25 (OUTSIDE the peak band 0.5-1.5), rim/core 0.943, rim/outside 56.8 (aggregate of 47 individuals; 0/47 membrane-like individually; rim level 0.921)
  - radial u (fuel): peak at rho=2.45 (OUTSIDE the peak band 0.5-1.5), rim/core 7.87, rim/outside 0.7 (aggregate of 47 individuals; 0/47 membrane-like individually; rim level 0.251)
  - radial a0 (k=0.10): peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.913, rim/outside 36.4 (aggregate of 47 individuals; 0/47 membrane-like individually; rim level 0.394)
  - radial a1 (k=0.12): peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.907, rim/outside 19.3 (aggregate of 47 individuals; 0/47 membrane-like individually; rim level 0.201)
  - radial a2 (k=0.14): peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.928, rim/outside 24.1 (aggregate of 47 individuals; 0/47 membrane-like individually; rim level 0.247)
  - radial a3 (k=0.16): peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.963, rim/outside 13.6 (aggregate of 47 individuals; 0/47 membrane-like individually; rim level 0.136)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #3 (t=10100, R_eq 8.74): none; #2 (t=8100, R_eq 8.23): none; #5 (t=12300, R_eq 7.38): none; #7 (t=14300, R_eq 8.37): none

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
