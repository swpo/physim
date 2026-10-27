# Evidence pack: fed-wave-matter (seed 7)

- world: `../../../20261027T0949-c55-schrodinger-poisson-negative/world.py`, family `schrodinger-poisson`
- parent: None; mutation: -
- run: 201 frames x 50 steps x dt 0.2 = time 2000; grid [128, 128]; wall 25s; status ok
- command: `python -m labkit.run collective/contrib/20261027T0949-c55-schrodinger-poisson-negative/world.py --out collective/contrib/20261027T1648-c58-review-sp/packC --seeds 6 7 --frames 200 --spf 50 --no-movie`
- segmentation: matter > 0.08 of robust range [0.0, 3.9689], min area 6 px

## Measurements
- components: final 4, mean 6.7, max 23; occupancy final 0.04
- tracks: 831; persistent (alive >= 50% of run): 0; longest 15 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 0.00 (1 = constant size)
- enclosures: components with a hole mean 0.14, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [3, 3, 1], H1 [0, 0, 0]
- motion: 0 long-lived tracks moved >= 1 body length; max speed 0/time; max body lengths 5.0
- replication (lineage window K = 20 frames = time 200, default): splits 174, persistent splits 0 (0 more failed only because the siblings re-merged within K), max generation 0, merges 191, merge/split ratio 1.1, nucleations 272
- channel total drift (end/start - 1): [-0.9472, -0.0585, None, 0.8581]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 235 at frame 50: holes 0, rim-vs-core 0.52, rim-vs-outside 0.28, heterogeneity 0.18; core [0.751, 0.083, 0.683, 0.227] rim [0.258, 0.216, 0.624, 0.328]
  - track 485 at frame 134: holes 0, rim-vs-core 0.56, rim-vs-outside 0.12, heterogeneity 0.19; core [0.691, 0.186, 0.537, 0.517] rim [0.167, 0.366, 0.485, 0.491]
  - track 319 at frame 82: holes 0, rim-vs-core 0.54, rim-vs-outside 0.15, heterogeneity 0.20; core [0.635, 0.151, 0.538, 0.822] rim [0.189, 0.299, 0.488, 0.553]
  - track 637 at frame 168: holes 0, rim-vs-core 0.55, rim-vs-outside 0.15, heterogeneity 0.18; core [0.671, 0.437, 0.528, 0.801] rim [0.188, 0.531, 0.494, 0.555]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 18 components >= 12 px at frames [34, 67, 101, 133, 166, 200]):
  - radial density |psi|^2: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.545, rim/outside 5 (aggregate of 18 individuals; 1/18 membrane-like individually; rim level 0.274)
  - radial fuel Y: peak at rho=2.45 (OUTSIDE the peak band 0.5-1.5), rim/core 2.03, rim/outside 0.832 (aggregate of 18 individuals; 0/18 membrane-like individually; rim level 0.501)
  - radial potential -V: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.94, rim/outside 1.25 (aggregate of 18 individuals; 0/18 membrane-like individually; rim level 0.745)
  - radial phase cos: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 1.03, rim/outside 1.01 (aggregate of 18 individuals; 0/18 membrane-like individually; rim level 0.465)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #235 (t=500, R_eq 6.13): none; #485 (t=1340, R_eq 5.11): none; #319 (t=820, R_eq 5.89): none; #637 (t=1680, R_eq 4.79): none

## Warnings
- matter fills >80% of the domain at some point: components may be one connected sea
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
