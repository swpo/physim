# Evidence pack: sh-spots-inhibitor (seed 11)

- world: `../../../world_kick.py`, family `swift-hohenberg`
- parent: None; mutation: Swift-Hohenberg (quadratic-cubic) localized states plus a slow linear inhibitor for a drift bifurcation; new class
- run: 81 frames x 50 steps x dt 0.1 = time 400; grid [128, 128]; wall 15s; status ok
- command: `python -m labkit.run collective/contrib/20261026T1200-c41-review-sh-delay/world_kick.py --out collective/contrib/20261026T1200-c41-review-sh-delay/rerun/kick_pyr_km03_t10 --seeds 11 12 --frames 80 --no-movie`
- segmentation: matter > 0.39 of robust range [-0.6312, 2.0313], min area 6 px

## Measurements
- components: final 88, mean 62.4, max 115; occupancy final 0.42
- tracks: 248; persistent (alive >= 50% of run): 44; longest 64 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 10.65 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [82, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [99, 89, 88], H1 [67, 0, 0]
- motion: 96 long-lived tracks moved >= 1 body length; max speed 0.286/time; max body lengths 10.1
- replication (lineage window K = 20 frames = time 100, default): splits 36, persistent splits 4 (0 more failed only because the siblings re-merged within K), max generation 1, merges 60, merge/split ratio 1.67, nucleations 115
- channel total drift (end/start - 1): [191.0602, 191.1819, 0.0]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 2 at frame 49: holes 0, rim-vs-core 0.38, rim-vs-outside 0.29, heterogeneity 0.15; core [0.843, 0.713, 0.0] rim [0.539, 0.48, 0.0]
  - track 4 at frame 49: holes 0, rim-vs-core 0.25, rim-vs-outside 0.65, heterogeneity 0.14; core [0.908, 0.719, 0.0] rim [0.697, 0.585, 0.0]
  - track 5 at frame 50: holes 0, rim-vs-core 0.32, rim-vs-outside 0.47, heterogeneity 0.14; core [0.874, 0.697, 0.0] rim [0.601, 0.531, 0.0]
  - track 6 at frame 50: holes 0, rim-vs-core 0.29, rim-vs-outside 0.54, heterogeneity 0.14; core [0.902, 0.702, 0.0] rim [0.65, 0.564, 0.0]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 413 components >= 12 px at frames [13, 27, 40, 53, 67, 80]):
  - radial u (SH field): peak at rho=0.25 (OUTSIDE the peak band 0.5-1.5), rim/core 0.755, rim/outside 3.23 (aggregate of 413 individuals; 0/413 membrane-like individually; rim level 0.664)
  - radial v (slow inhibitor): peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.769, rim/outside 2.54 (aggregate of 413 individuals; 2/413 membrane-like individually; rim level 0.575)
  - radial R (resource): flat profile (no radial structure; level 0; aggregate of 413 individuals)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #2 (t=245, R_eq 3.52): none; #4 (t=245, R_eq 10.79, ring): none; #5 (t=250, R_eq 8.37): none; #6 (t=250, R_eq 7.9): none

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 19 of 413 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
