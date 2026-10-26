# Evidence pack: sh-spots-inhibitor (seed 1)

- world: `../../world.py`, family `swift-hohenberg`
- parent: None; mutation: Swift-Hohenberg (quadratic-cubic) localized states plus a slow linear inhibitor for a drift bifurcation; new class
- run: 201 frames x 50 steps x dt 0.1 = time 1000; grid [256, 256]; wall 276s; status ok
- command: `python -m labkit.run collective/contrib/wip-c37/sh/world.py --out collective/contrib/wip-c37/sh/packB --seeds 0 1 --frames 200 --no-movie`
- segmentation: matter > 0.39 of robust range [-0.324, 1.5419], min area 6 px

## Measurements
- components: final 20, mean 33.5, max 478; occupancy final 0.01
- tracks: 641; persistent (alive >= 50% of run): 17; longest 201 frames; alive start-to-end: 5
- size of persistent tracks: max/min area ratio 6.57 (1 = constant size)
- enclosures: components with a hole mean 0.02, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [21, 20, 20], H1 [8, 0, 0]
- motion: 20 long-lived tracks moved >= 1 body length; max speed 0.267/time; max body lengths 46.5
- replication (lineage window K = 20 frames = time 100, default): splits 121, persistent splits 0 (0 more failed only because the siblings re-merged within K), max generation 0, merges 14, merge/split ratio 0.116, nucleations 114
- channel total drift (end/start - 1): [1.2283, None, -0.0716]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 12 at frame 101: holes 0, rim-vs-core 0.38, rim-vs-outside 0.35, heterogeneity 0.19; core [0.97, 0.775, 0.2] rim [0.679, 0.56, 0.305]
  - track 68 at frame 101: holes 0, rim-vs-core 0.40, rim-vs-outside 0.35, heterogeneity 0.18; core [0.96, 0.793, 0.104] rim [0.635, 0.571, 0.199]
  - track 102 at frame 101: holes 0, rim-vs-core 0.37, rim-vs-outside 0.33, heterogeneity 0.17; core [0.958, 0.771, 0.021] rim [0.67, 0.552, 0.083]
  - track 128 at frame 101: holes 0, rim-vs-core 0.40, rim-vs-outside 0.37, heterogeneity 0.17; core [0.97, 0.843, 0.022] rim [0.684, 0.571, 0.087]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 107 components >= 12 px at frames [34, 67, 101, 133, 166, 200]):
  - radial u (SH field): peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.903, rim/outside 16.8 (aggregate of 107 individuals; 0/107 membrane-like individually; rim level 0.902)
  - radial v (slow inhibitor): peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.758, rim/outside 6.03 (aggregate of 107 individuals; 0/107 membrane-like individually; rim level 0.705)
  - radial R (resource): peak at rho=2.45 (OUTSIDE the peak band 0.5-1.5), rim/core 4.08, rim/outside 0.747 (aggregate of 107 individuals; 0/107 membrane-like individually; rim level 0.244)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #12 (t=505, R_eq 3.39): none; #68 (t=505, R_eq 3.39): none; #102 (t=505, R_eq 3.24): none; #128 (t=505, R_eq 3.24): none

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
