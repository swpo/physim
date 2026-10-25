# Evidence pack: ad5n-neutral (seed 4)

- world: `../../../../../../threads/active-droplets/worlds/ad5n-neutral/world.py`, family `phase-field`
- parent: ad5-evolve; mutation: neutral control: all four alleles have the same catalytic rate k=0.13
- run: 201 frames x 200 steps x dt 0.5 = time 20000; grid [128, 128]; wall 184s; status ok
- command: `python -m labkit.run threads/active-droplets/worlds/ad5n-neutral/world.py --out collective/contrib/wip-c22/rev_ad5/neutral/seed4 --seeds 4 --frames 200 --no-movie`
- segmentation: matter > 0.43 of robust range [-1.0636, 1.4199], min area 6 px

## Measurements
- components: final 9, mean 8.4, max 9; occupancy final 0.11
- tracks: 15; persistent (alive >= 50% of run): 9; longest 201 frames; alive start-to-end: 2
- size of persistent tracks: max/min area ratio 2.12 (1 = constant size)
- enclosures: components with a hole mean 0.01, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [10, 9, 9], H1 [0, 0, 0]
- motion: 3 long-lived tracks moved >= 1 body length; max speed 0.00128/time; max body lengths 1.8
- replication (lineage window K = 20 frames = time 2000, default): splits 4, persistent splits 3 (0 more failed only because the siblings re-merged within K), max generation 1, merges 1, merge/split ratio 0.25, nucleations 0
- channel total drift (end/start - 1): [0.0796, -0.5598, -0.1701, None, None, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 4 at frame 101: holes 0, rim-vs-core 0.36, rim-vs-outside 0.63, heterogeneity 0.13; core [0.967, 0.04, 0.014, 0.0, 0.627, 0.435] rim [0.727, 0.123, 0.01, 0.0, 0.424, 0.281]
  - track 5 at frame 101: holes 0, rim-vs-core 0.42, rim-vs-outside 0.73, heterogeneity 0.07; core [0.972, 0.044, 0.024, 0.999, 0.0, 0.007] rim [0.69, 0.126, 0.016, 0.703, 0.0, 0.005]
  - track 8 at frame 103: holes 0, rim-vs-core 0.40, rim-vs-outside 0.62, heterogeneity 0.08; core [0.967, 0.045, 0.0, 0.177, 0.702, 0.191] rim [0.702, 0.137, 0.0, 0.115, 0.437, 0.126]
  - track 9 at frame 114: holes 0, rim-vs-core 0.43, rim-vs-outside 0.68, heterogeneity 0.07; core [0.958, 0.032, 0.958, 0.0, 0.0, 0.0] rim [0.713, 0.122, 0.622, 0.0, 0.0, 0.0]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 52 components >= 12 px at frames [34, 67, 101, 133, 166, 200]):
  - radial phi (droplet material): peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.941, rim/outside 68 (aggregate of 52 individuals; 0/52 membrane-like individually; rim level 0.918)
  - radial u (fuel): peak at rho=2.45 (OUTSIDE the peak band 0.5-1.5), rim/core 15.5, rim/outside 0.69 (aggregate of 52 individuals; 0/52 membrane-like individually; rim level 0.229)
  - radial a0: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.884, rim/outside 46 (aggregate of 52 individuals; 0/52 membrane-like individually; rim level 0.495)
  - radial a1: peak at rho=0.45 (OUTSIDE the peak band 0.5-1.5), rim/core 0.992, rim/outside 12.8 (aggregate of 52 individuals; 1/52 membrane-like individually; rim level 0.121)
  - radial a2: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.939, rim/outside 17.1 (aggregate of 52 individuals; 0/52 membrane-like individually; rim level 0.163)
  - radial a3: peak at rho=0.35 (OUTSIDE the peak band 0.5-1.5), rim/core 0.983, rim/outside 15.4 (aggregate of 52 individuals; 0/52 membrane-like individually; rim level 0.148)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #4 (t=10100, R_eq 7.48): none; #5 (t=10100, R_eq 7.29): none; #8 (t=10300, R_eq 7.98): none; #9 (t=11400, R_eq 8.48): none

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
