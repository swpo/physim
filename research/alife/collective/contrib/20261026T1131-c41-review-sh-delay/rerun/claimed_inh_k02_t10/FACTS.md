# Evidence pack: sh-spots-inhibitor (seed 11)

- world: `../../world.py`, family `swift-hohenberg`
- parent: None; mutation: Swift-Hohenberg (quadratic-cubic) localized states plus a slow linear inhibitor for a drift bifurcation; new class
- run: 101 frames x 50 steps x dt 0.1 = time 500; grid [128, 128]; wall 19s; status ok
- command: `python -m labkit.run collective/contrib/20261026T1200-c41-review-sh-delay/world.py --out collective/contrib/20261026T1200-c41-review-sh-delay/rerun/claimed_inh_k02_t10 --seeds 11 --frames 100 --no-movie`
- segmentation: matter > 0.34 of robust range [-0.0548, 1.2702], min area 6 px

## Measurements
- components: final 1, mean 1.0, max 1; occupancy final 0.00
- tracks: 1; persistent (alive >= 50% of run): 1; longest 101 frames; alive start-to-end: 1
- size of persistent tracks: max/min area ratio 1.80 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [2, 1, 1], H1 [0, 0, 0]
- motion: 1 long-lived tracks moved >= 1 body length; max speed 0.113/time; max body lengths 8.3
- replication (lineage window K = 20 frames = time 100, default): splits 0, persistent splits 0 (0 more failed only because the siblings re-merged within K), max generation 0, merges 0, merge/split ratio n/a, nucleations 0
- channel total drift (end/start - 1): [0.2913, None, 0.0]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 0 at frame 50: holes 0, rim-vs-core 0.00, rim-vs-outside 0.50, heterogeneity 0.00; core [1.0, 1.0, 0.0] rim [1.0, 1.0, 0.0]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 6 components >= 12 px at frames [17, 33, 50, 67, 83, 100]):
  - radial u (SH field): peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 1, rim/outside 97.7 (aggregate of 6 individuals; 0/6 membrane-like individually; rim level 1)
  - radial v (slow inhibitor): peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 1, rim/outside 16.5 (aggregate of 6 individuals; 0/6 membrane-like individually; rim level 1)
  - radial R (resource): flat profile (no radial structure; level 0; aggregate of 6 individuals)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #0 (t=250, R_eq 3.87): none

## Warnings
- none

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
