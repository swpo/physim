# Evidence pack: sh-spots-inhibitor (seed 12)

- world: `../../../world_kick.py`, family `swift-hohenberg`
- parent: None; mutation: Swift-Hohenberg (quadratic-cubic) localized states plus a slow linear inhibitor for a drift bifurcation; new class
- run: 81 frames x 50 steps x dt 0.1 = time 400; grid [128, 128]; wall 15s; status ok
- command: `python -m labkit.run collective/contrib/20261026T1200-c41-review-sh-delay/world_kick.py --out collective/contrib/20261026T1200-c41-review-sh-delay/rerun/kick_pyr_km03_t10 --seeds 11 12 --frames 80 --no-movie`
- segmentation: matter > 0.39 of robust range [-0.6314, 2.0235], min area 6 px

## Measurements
- components: final 72, mean 59.8, max 121; occupancy final 0.44
- tracks: 309; persistent (alive >= 50% of run): 34; longest 64 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 14.86 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [59, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [87, 73, 71], H1 [51, 0, 0]
- motion: 78 long-lived tracks moved >= 1 body length; max speed 0.264/time; max body lengths 10.4
- replication (lineage window K = 20 frames = time 100, default): splits 51, persistent splits 1 (0 more failed only because the siblings re-merged within K), max generation 1, merges 86, merge/split ratio 1.69, nucleations 119
- channel total drift (end/start - 1): [199.1466, 199.781, 0.0]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 2 at frame 49: holes 0, rim-vs-core 0.38, rim-vs-outside 0.27, heterogeneity 0.15; core [0.847, 0.719, 0.0] rim [0.543, 0.491, 0.0]
  - track 4 at frame 49: holes 0, rim-vs-core 0.27, rim-vs-outside 0.66, heterogeneity 0.14; core [0.92, 0.727, 0.0] rim [0.691, 0.58, 0.0]
  - track 5 at frame 50: holes 0, rim-vs-core 0.31, rim-vs-outside 0.51, heterogeneity 0.14; core [0.903, 0.699, 0.0] rim [0.63, 0.545, 0.0]
  - track 6 at frame 50: holes 0, rim-vs-core 0.33, rim-vs-outside 0.50, heterogeneity 0.14; core [0.887, 0.711, 0.0] rim [0.607, 0.54, 0.0]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 387 components >= 12 px at frames [13, 27, 40, 53, 67, 80]):
  - radial u (SH field): peak at rho=0.25 (OUTSIDE the peak band 0.5-1.5), rim/core 0.752, rim/outside 3 (aggregate of 387 individuals; 0/387 membrane-like individually; rim level 0.654)
  - radial v (slow inhibitor): peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.773, rim/outside 2.46 (aggregate of 387 individuals; 3/387 membrane-like individually; rim level 0.565)
  - radial R (resource): flat profile (no radial structure; level 0; aggregate of 387 individuals)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #2 (t=245, R_eq 3.48): none; #4 (t=245, R_eq 11.58, ring): none; #5 (t=250, R_eq 6.7): none; #6 (t=250, R_eq 7.2): none

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 19 of 387 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
