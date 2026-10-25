# Evidence pack: ad5-evolve (seed 4)

- world: `../../../../../../threads/active-droplets/worlds/ad5-evolve/world.py`, family `phase-field`
- parent: ad2-catalysts; mutation: N catalyst alleles with different rates, rare local mutation patches, random dilution disks
- run: 201 frames x 200 steps x dt 0.5 = time 20000; grid [128, 128]; wall 181s; status ok
- command: `python -m labkit.run threads/active-droplets/worlds/ad5-evolve/world.py --out collective/contrib/wip-c22/rev_ad5/evolve/seed4 --seeds 4 --frames 200 --no-movie`
- segmentation: matter > 0.43 of robust range [-1.0675, 1.4427], min area 6 px

## Measurements
- components: final 12, mean 8.5, max 12; occupancy final 0.12
- tracks: 23; persistent (alive >= 50% of run): 6; longest 201 frames; alive start-to-end: 2
- size of persistent tracks: max/min area ratio 1.97 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [12, 12, 12], H1 [0, 0, 0]
- motion: 5 long-lived tracks moved >= 1 body length; max speed 0.00175/time; max body lengths 1.4
- replication (lineage window K = 20 frames = time 2000, default): splits 8, persistent splits 7 (0 more failed only because the siblings re-merged within K), max generation 3, merges 1, merge/split ratio 0.125, nucleations 0
- channel total drift (end/start - 1): [0.101, -0.6003, -0.8251, None, None, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 4 at frame 101: holes 0, rim-vs-core 0.36, rim-vs-outside 0.62, heterogeneity 0.11; core [0.948, 0.03, 0.0, 0.0, 0.697, 0.253] rim [0.725, 0.115, 0.0, 0.0, 0.441, 0.189]
  - track 5 at frame 101: holes 0, rim-vs-core 0.34, rim-vs-outside 0.59, heterogeneity 0.09; core [0.96, 0.04, 0.0, 0.149, 0.476, 0.33] rim [0.707, 0.124, 0.0, 0.098, 0.301, 0.214]
  - track 8 at frame 104: holes 0, rim-vs-core 0.38, rim-vs-outside 0.62, heterogeneity 0.08; core [0.948, 0.031, 0.0, 0.0, 0.708, 0.233] rim [0.704, 0.122, 0.0, 0.0, 0.449, 0.154]
  - track 17 at frame 185: holes 0, rim-vs-core 0.43, rim-vs-outside 0.68, heterogeneity 0.07; core [0.959, 0.016, 0.0, 0.0, 0.0, 0.965] rim [0.71, 0.09, 0.0, 0.0, 0.0, 0.623]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 52 components >= 12 px at frames [34, 67, 101, 133, 166, 200]):
  - radial phi (droplet material): peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.928, rim/outside 55.1 (aggregate of 52 individuals; 0/52 membrane-like individually; rim level 0.88)
  - radial u (fuel): peak at rho=2.45 (OUTSIDE the peak band 0.5-1.5), rim/core 7.37, rim/outside 0.697 (aggregate of 52 individuals; 0/52 membrane-like individually; rim level 0.23)
  - radial a0 (k=0.10): peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.95, rim/outside 12.1 (aggregate of 52 individuals; 0/52 membrane-like individually; rim level 0.113)
  - radial a1 (k=0.12): peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.96, rim/outside 14.4 (aggregate of 52 individuals; 0/52 membrane-like individually; rim level 0.139)
  - radial a2 (k=0.14): peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.883, rim/outside 37.2 (aggregate of 52 individuals; 0/52 membrane-like individually; rim level 0.396)
  - radial a3 (k=0.16): peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.871, rim/outside 22.8 (aggregate of 52 individuals; 0/52 membrane-like individually; rim level 0.241)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #4 (t=10100, R_eq 8.12): none; #5 (t=10100, R_eq 7.61): none; #8 (t=10400, R_eq 8.31): none; #17 (t=18500, R_eq 7.53): none

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
