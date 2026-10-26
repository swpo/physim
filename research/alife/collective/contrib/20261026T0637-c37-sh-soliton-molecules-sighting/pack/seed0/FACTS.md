# Evidence pack: sh-spots-inhibitor (seed 0)

- world: `../../world.py`, family `swift-hohenberg`
- parent: None; mutation: Swift-Hohenberg (quadratic-cubic) localized states plus a slow linear inhibitor for a drift bifurcation; new class
- run: 201 frames x 50 steps x dt 0.1 = time 1000; grid [256, 256]; wall 261s; status ok
- command: `python -m labkit.run collective/contrib/wip-c37/sh/world.py --out collective/contrib/wip-c37/sh/packB --seeds 0 1 --frames 200 --no-movie`
- segmentation: matter > 0.39 of robust range [-0.3051, 1.5223], min area 6 px

## Measurements
- components: final 11, mean 25.9, max 478; occupancy final 0.01
- tracks: 658; persistent (alive >= 50% of run): 11; longest 201 frames; alive start-to-end: 6
- size of persistent tracks: max/min area ratio 8.00 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [12, 11, 11], H1 [3, 0, 0]
- motion: 11 long-lived tracks moved >= 1 body length; max speed 0.267/time; max body lengths 46.6
- replication (lineage window K = 20 frames = time 100, default): splits 150, persistent splits 0 (0 more failed only because the siblings re-merged within K), max generation 0, merges 12, merge/split ratio 0.08, nucleations 89
- channel total drift (end/start - 1): [-0.5796, None, -0.0419]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 14 at frame 101: holes 0, rim-vs-core 0.42, rim-vs-outside 0.37, heterogeneity 0.19; core [0.98, 0.821, 0.186] rim [0.674, 0.564, 0.302]
  - track 61 at frame 101: holes 0, rim-vs-core 0.41, rim-vs-outside 0.36, heterogeneity 0.17; core [0.987, 0.824, 0.021] rim [0.694, 0.549, 0.084]
  - track 70 at frame 101: holes 0, rim-vs-core 0.37, rim-vs-outside 0.34, heterogeneity 0.16; core [0.974, 0.79, 0.0] rim [0.689, 0.551, 0.012]
  - track 76 at frame 101: holes 0, rim-vs-core 0.39, rim-vs-outside 0.36, heterogeneity 0.17; core [0.984, 0.829, 0.018] rim [0.697, 0.577, 0.081]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 64 components >= 12 px at frames [34, 67, 101, 133, 166, 200]):
  - radial u (SH field): peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.951, rim/outside 19.9 (aggregate of 64 individuals; 0/64 membrane-like individually; rim level 0.95)
  - radial v (slow inhibitor): peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.745, rim/outside 5.88 (aggregate of 64 individuals; 0/64 membrane-like individually; rim level 0.712)
  - radial R (resource): peak at rho=2.45 (OUTSIDE the peak band 0.5-1.5), rim/core 4.42, rim/outside 0.725 (aggregate of 64 individuals; 0/64 membrane-like individually; rim level 0.221)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #14 (t=505, R_eq 3.48): none; #61 (t=505, R_eq 3.29): none; #70 (t=505, R_eq 3.24): none; #76 (t=505, R_eq 3.29): none

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
