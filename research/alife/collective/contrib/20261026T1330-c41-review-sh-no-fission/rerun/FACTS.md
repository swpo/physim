# Evidence pack: sh-spots-inhibitor (seed 5)

- world: `../../20261026T0841-c37-sh-no-fission-negative/world.py`, family `swift-hohenberg`
- parent: None; mutation: Swift-Hohenberg (quadratic-cubic) localized states plus a slow linear inhibitor (drift bifurcation, kap*tau=3) and a consumed regrowing resource that sets the local growth rate; new class
- run: 201 frames x 50 steps x dt 0.1 = time 1000; grid [128, 128]; wall 55s; status ok
- command: `python -m labkit.run collective/contrib/20261026T0841-c37-sh-no-fission-negative/world.py --out collective/contrib/20261026T1330-c41-review-sh-no-fission/rerun --seeds 5 --frames 200 --no-movie`
- segmentation: matter > 0.40 of robust range [-0.3877, 1.6004], min area 6 px

## Measurements
- components: final 61, mean 56.0, max 116; occupancy final 0.12
- tracks: 196; persistent (alive >= 50% of run): 54; longest 201 frames; alive start-to-end: 2
- size of persistent tracks: max/min area ratio 5.43 (1 = constant size)
- enclosures: components with a hole mean 0.01, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [71, 61, 61], H1 [30, 0, 0]
- motion: 82 long-lived tracks moved >= 1 body length; max speed 0.266/time; max body lengths 45.2
- replication (lineage window K = 20 frames = time 100, default): splits 34, persistent splits 0 (0 more failed only because the siblings re-merged within K), max generation 0, merges 0, merge/split ratio 0, nucleations 69
- channel total drift (end/start - 1): [0.525, None, -0.3507]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 9 at frame 101: holes 0, rim-vs-core 0.37, rim-vs-outside 0.27, heterogeneity 0.16; core [0.841, 0.705, 0.133] rim [0.544, 0.488, 0.198]
  - track 24 at frame 101: holes 0, rim-vs-core 0.35, rim-vs-outside 0.27, heterogeneity 0.15; core [0.843, 0.697, 0.083] rim [0.558, 0.494, 0.134]
  - track 38 at frame 101: holes 0, rim-vs-core 0.33, rim-vs-outside 0.27, heterogeneity 0.14; core [0.844, 0.712, 0.15] rim [0.57, 0.53, 0.21]
  - track 50 at frame 101: holes 0, rim-vs-core 0.35, rim-vs-outside 0.26, heterogeneity 0.15; core [0.834, 0.658, 0.164] rim [0.54, 0.476, 0.227]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 329 components >= 12 px at frames [34, 67, 101, 133, 166, 200]):
  - radial u (SH field): peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.759, rim/outside 9.1 (aggregate of 329 individuals; 0/329 membrane-like individually; rim level 0.737)
  - radial v (slow inhibitor): peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.795, rim/outside 4.21 (aggregate of 329 individuals; 0/329 membrane-like individually; rim level 0.639)
  - radial R (resource): peak at rho=2.45 (OUTSIDE the peak band 0.5-1.5), rim/core 2.44, rim/outside 0.827 (aggregate of 329 individuals; 0/329 membrane-like individually; rim level 0.195)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #9 (t=505, R_eq 3.34): none; #24 (t=505, R_eq 3.19): none; #38 (t=505, R_eq 3.14): none; #50 (t=505, R_eq 3.34): none

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
