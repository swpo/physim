# Evidence pack: sh-spots-inhibitor (seed 3)

- world: `../../../20261026T0841-c37-sh-no-fission-negative/world.py`, family `swift-hohenberg`
- parent: None; mutation: Swift-Hohenberg (quadratic-cubic) localized states plus a slow linear inhibitor (drift bifurcation, kap*tau=3) and a consumed regrowing resource that sets the local growth rate; new class
- run: 501 frames x 20 steps x dt 0.1 = time 1000; grid [128, 128]; wall 60s; status ok
- command: `python -m labkit.run collective/contrib/20261026T0841-c37-sh-no-fission-negative/world.py --out collective/contrib/20261026T0945-c38-review-sh/rerun/k1_seed3 --seeds 3 --frames 500 --spf 20 --no-movie`
- segmentation: matter > 0.41 of robust range [-0.4239, 1.6043], min area 6 px

## Measurements
- components: final 125, mean 85.0, max 128; occupancy final 0.22
- tracks: 405; persistent (alive >= 50% of run): 59; longest 500 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 6.67 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [1, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [131, 127, 125], H1 [109, 0, 0]
- motion: 246 long-lived tracks moved >= 1 body length; max speed 0.309/time; max body lengths 48.1
- replication (lineage window K = 20 frames = time 40, default): splits 40, persistent splits 0 (0 more failed only because the siblings re-merged within K), max generation 0, merges 4, merge/split ratio 0.1, nucleations 258
- channel total drift (end/start - 1): [6.778, None, -0.5565]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 83 at frame 252: holes 0, rim-vs-core 0.38, rim-vs-outside 0.27, heterogeneity 0.17; core [0.868, 0.683, 0.244] rim [0.564, 0.475, 0.316]
  - track 132 at frame 256: holes 0, rim-vs-core 0.36, rim-vs-outside 0.26, heterogeneity 0.17; core [0.875, 0.674, 0.196] rim [0.579, 0.485, 0.266]
  - track 138 at frame 256: holes 0, rim-vs-core 0.30, rim-vs-outside 0.26, heterogeneity 0.15; core [0.866, 0.623, 0.026] rim [0.595, 0.501, 0.063]
  - track 191 at frame 261: holes 0, rim-vs-core 0.31, rim-vs-outside 0.24, heterogeneity 0.14; core [0.849, 0.621, 0.068] rim [0.572, 0.492, 0.11]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 528 components >= 12 px at frames [84, 168, 252, 332, 416, 500]):
  - radial u (SH field): peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.771, rim/outside 8.3 (aggregate of 528 individuals; 0/528 membrane-like individually; rim level 0.743)
  - radial v (slow inhibitor): peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.81, rim/outside 2.56 (aggregate of 528 individuals; 1/528 membrane-like individually; rim level 0.578)
  - radial R (resource): peak at rho=2.25 (OUTSIDE the peak band 0.5-1.5), rim/core 2.1, rim/outside 0.865 (aggregate of 528 individuals; 0/528 membrane-like individually; rim level 0.153)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #83 (t=504, R_eq 3.34): none; #132 (t=512, R_eq 3.34): none; #138 (t=512, R_eq 3.09): none; #191 (t=522, R_eq 3.19): none

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
