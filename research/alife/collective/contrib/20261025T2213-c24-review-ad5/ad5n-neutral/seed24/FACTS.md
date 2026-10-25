# Evidence pack: ad5n-neutral (seed 24)

- world: `../../../../../threads/active-droplets/worlds/ad5n-neutral/world.py`, family `phase-field`
- parent: ad5-evolve; mutation: neutral control: all four alleles have the same catalytic rate k=0.13
- run: 201 frames x 200 steps x dt 0.5 = time 20000; grid [128, 128]; wall 311s; status ok
- command: `python -m labkit.run threads/active-droplets/worlds/ad5n-neutral/world.py --out collective/contrib/20261025T2213-c24-review-ad5/ad5n-neutral/seed24 --seeds 24 --frames 200 --no-movie`
- segmentation: matter > 0.43 of robust range [-1.0636, 1.4188], min area 6 px

## Measurements
- components: final 9, mean 8.2, max 9; occupancy final 0.11
- tracks: 14; persistent (alive >= 50% of run): 9; longest 194 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 2.17 (1 = constant size)
- enclosures: components with a hole mean 0.06, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [9, 9, 9], H1 [0, 0, 0]
- motion: 4 long-lived tracks moved >= 1 body length; max speed 0.00121/time; max body lengths 1.4
- replication (lineage window K = 20 frames = time 2000, default): splits 5, persistent splits 5 (0 more failed only because the siblings re-merged within K), max generation 2, merges 0, merge/split ratio 0, nucleations 0
- channel total drift (end/start - 1): [0.0935, -0.5635, 1.6339, None, None, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 4 at frame 104: holes 0, rim-vs-core 0.37, rim-vs-outside 0.75, heterogeneity 0.07; core [0.974, 0.029, 0.959, 0.0, 0.0, 0.0] rim [0.763, 0.11, 0.672, 0.0, 0.0, 0.0]
  - track 6 at frame 114: holes 0, rim-vs-core 0.43, rim-vs-outside 0.68, heterogeneity 0.07; core [0.961, 0.032, 0.953, 0.0, 0.0, 0.0] rim [0.716, 0.124, 0.616, 0.0, 0.0, 0.0]
  - track 7 at frame 114: holes 0, rim-vs-core 0.38, rim-vs-outside 0.82, heterogeneity 0.14; core [0.961, 0.032, 0.532, 0.842, 0.0, 0.0] rim [0.83, 0.084, 0.545, 0.485, 0.0, 0.0]
  - track 12 at frame 123: holes 0, rim-vs-core 0.43, rim-vs-outside 0.69, heterogeneity 0.07; core [0.963, 0.03, 0.958, 0.0, 0.0, 0.0] rim [0.718, 0.124, 0.62, 0.0, 0.0, 0.0]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 52 components >= 12 px at frames [34, 67, 101, 133, 166, 200]):
  - radial phi (droplet material): peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.947, rim/outside 65.4 (aggregate of 52 individuals; 0/52 membrane-like individually; rim level 0.935)
  - radial u (fuel): peak at rho=2.45 (OUTSIDE the peak band 0.5-1.5), rim/core 17.1, rim/outside 0.692 (aggregate of 52 individuals; 0/52 membrane-like individually; rim level 0.233)
  - radial a0: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.9, rim/outside 62.4 (aggregate of 52 individuals; 0/52 membrane-like individually; rim level 0.739)
  - radial a1: peak at rho=0.25 (OUTSIDE the peak band 0.5-1.5), rim/core 0.966, rim/outside 9.9 (aggregate of 52 individuals; 0/52 membrane-like individually; rim level 0.0901)
  - radial a2: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.888, rim/outside 9.33 (aggregate of 52 individuals; 0/52 membrane-like individually; rim level 0.0901)
  - radial a3: peak at rho=0.25 (OUTSIDE the peak band 0.5-1.5), rim/core 0.975, rim/outside 11.4 (aggregate of 52 individuals; 0/52 membrane-like individually; rim level 0.106)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #4 (t=10400, R_eq 7.72): none; #6 (t=11400, R_eq 8.2): none; #7 (t=11400, R_eq 7.84): none; #12 (t=12300, R_eq 8.29): none

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
