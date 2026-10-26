# Evidence pack: sh-spots-inhibitor (seed 4)

- world: `../../../20261026T0847-c37-sh-fission-correction/world.py`, family `swift-hohenberg`
- parent: None; mutation: Swift-Hohenberg (quadratic-cubic) localized states plus a slow linear inhibitor (drift bifurcation, kap*tau=3) and a consumed regrowing resource that sets the local growth rate; new class
- run: 501 frames x 20 steps x dt 0.1 = time 1000; grid [128, 128]; wall 60s; status ok
- command: `python -m labkit.run collective/contrib/20261026T0847-c37-sh-fission-correction/world.py --out collective/contrib/20261026T0955-c38-review-sh-corr/rerun/ar02_seed4 --seeds 4 --frames 500 --spf 20 --no-movie`
- segmentation: matter > 0.40 of robust range [-0.3871, 1.5893], min area 6 px

## Measurements
- components: final 53, mean 54.4, max 118; occupancy final 0.10
- tracks: 210; persistent (alive >= 50% of run): 47; longest 501 frames; alive start-to-end: 8
- size of persistent tracks: max/min area ratio 6.83 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [62, 54, 51], H1 [22, 0, 0]
- motion: 109 long-lived tracks moved >= 1 body length; max speed 0.262/time; max body lengths 44.6
- replication (lineage window K = 20 frames = time 40, default): splits 40, persistent splits 0 (0 more failed only because the siblings re-merged within K), max generation 0, merges 3, merge/split ratio 0.075, nucleations 64
- channel total drift (end/start - 1): [0.5328, None, -0.3005]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 14 at frame 252: holes 0, rim-vs-core 0.36, rim-vs-outside 0.28, heterogeneity 0.15; core [0.857, 0.722, 0.08] rim [0.571, 0.506, 0.137]
  - track 19 at frame 252: holes 0, rim-vs-core 0.36, rim-vs-outside 0.28, heterogeneity 0.17; core [0.853, 0.693, 0.153] rim [0.552, 0.5, 0.221]
  - track 26 at frame 252: holes 0, rim-vs-core 0.36, rim-vs-outside 0.38, heterogeneity 0.15; core [0.896, 0.807, 0.03] rim [0.678, 0.527, 0.076]
  - track 27 at frame 252: holes 0, rim-vs-core 0.33, rim-vs-outside 0.27, heterogeneity 0.15; core [0.862, 0.684, 0.023] rim [0.589, 0.513, 0.076]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 305 components >= 12 px at frames [84, 168, 252, 332, 416, 500]):
  - radial u (SH field): peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.763, rim/outside 9.21 (aggregate of 305 individuals; 0/305 membrane-like individually; rim level 0.741)
  - radial v (slow inhibitor): peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.787, rim/outside 4.21 (aggregate of 305 individuals; 0/305 membrane-like individually; rim level 0.63)
  - radial R (resource): peak at rho=2.45 (OUTSIDE the peak band 0.5-1.5), rim/core 2.68, rim/outside 0.821 (aggregate of 305 individuals; 0/305 membrane-like individually; rim level 0.186)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #14 (t=504, R_eq 3.19): none; #19 (t=504, R_eq 3.29): none; #26 (t=504, R_eq 3.19): none; #27 (t=504, R_eq 3.09): none

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
