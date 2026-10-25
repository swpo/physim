# Evidence pack: ad5-evolve (seed 24)

- world: `../../../../../threads/active-droplets/worlds/ad5-evolve/world.py`, family `phase-field`
- parent: ad2-catalysts; mutation: N catalyst alleles with different rates, rare local mutation patches, random dilution disks
- run: 201 frames x 200 steps x dt 0.5 = time 20000; grid [128, 128]; wall 311s; status ok
- command: `python -m labkit.run threads/active-droplets/worlds/ad5-evolve/world.py --out collective/contrib/20261025T2213-c24-review-ad5/ad5-evolve/seed24 --seeds 24 --frames 200 --no-movie`
- segmentation: matter > 0.42 of robust range [-1.0677, 1.4521], min area 6 px

## Measurements
- components: final 10, mean 7.5, max 11; occupancy final 0.11
- tracks: 18; persistent (alive >= 50% of run): 5; longest 201 frames; alive start-to-end: 1
- size of persistent tracks: max/min area ratio 2.76 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [10, 10, 10], H1 [0, 0, 0]
- motion: 3 long-lived tracks moved >= 1 body length; max speed 0.00175/time; max body lengths 1.4
- replication (lineage window K = 20 frames = time 2000, default): splits 7, persistent splits 6 (0 more failed only because the siblings re-merged within K), max generation 3, merges 0, merge/split ratio 0, nucleations 0
- channel total drift (end/start - 1): [0.0894, -0.5561, -0.3161, None, None, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 1 at frame 101: holes 0, rim-vs-core 0.44, rim-vs-outside 0.68, heterogeneity 0.07; core [0.965, 0.106, 0.962, 0.0, 0.0, 0.0] rim [0.701, 0.203, 0.619, 0.0, 0.0, 0.0]
  - track 2 at frame 87: holes 0, rim-vs-core 0.41, rim-vs-outside 0.69, heterogeneity 0.07; core [0.957, 0.106, 0.925, 0.081, 0.003, 0.0] rim [0.715, 0.198, 0.607, 0.059, 0.002, 0.0]
  - track 6 at frame 133: holes 0, rim-vs-core 0.43, rim-vs-outside 0.65, heterogeneity 0.08; core [0.967, 0.117, 0.625, 0.7, 0.0, 0.0] rim [0.701, 0.194, 0.394, 0.457, 0.0, 0.0]
  - track 10 at frame 156: holes 0, rim-vs-core 0.35, rim-vs-outside 0.60, heterogeneity 0.13; core [0.951, 0.055, 0.261, 0.413, 0.508, 0.0] rim [0.715, 0.139, 0.193, 0.269, 0.32, 0.0]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 48 components >= 12 px at frames [34, 67, 101, 133, 166, 200]):
  - radial phi (droplet material): peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.94, rim/outside 47 (aggregate of 48 individuals; 0/48 membrane-like individually; rim level 0.913)
  - radial u (fuel): peak at rho=2.45 (OUTSIDE the peak band 0.5-1.5), rim/core 5.52, rim/outside 0.714 (aggregate of 48 individuals; 0/48 membrane-like individually; rim level 0.258)
  - radial a0 (k=0.10): peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.911, rim/outside 37.4 (aggregate of 48 individuals; 0/48 membrane-like individually; rim level 0.43)
  - radial a1 (k=0.12): peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.957, rim/outside 13.1 (aggregate of 48 individuals; 0/48 membrane-like individually; rim level 0.13)
  - radial a2 (k=0.14): peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.908, rim/outside 19.5 (aggregate of 48 individuals; 0/48 membrane-like individually; rim level 0.226)
  - radial a3 (k=0.16): peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.877, rim/outside 14.3 (aggregate of 48 individuals; 0/48 membrane-like individually; rim level 0.158)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #1 (t=10100, R_eq 8.08): none; #2 (t=8700, R_eq 8.35): none; #6 (t=13300, R_eq 6.98): none; #10 (t=15600, R_eq 7.53): none

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
