# Evidence pack: nrch (seed 6)

- world: `../../world.py`, family `active-emulsion`
- parent: None; mutation: reference: nonreciprocal Cahn-Hilliard (Brauns-Marchetti 2024), phi phase-separating, psi diffusive
- run: 241 frames x 500 steps x dt 0.05 = time 6000; grid [192, 192]; wall 1047s; status ok
- command: `python -m labkit.run collective/contrib/20261025T1254-c12-review-crystal-growth/world.py --out collective/contrib/20261025T1254-c12-review-crystal-growth/net_prod/seed6 --seeds 6 --frames 240 --spf 500 --lineage-k 40 --no-movie`
- segmentation: matter > 0.50 of robust range [-0.9221, 0.9352], min area 6 px

## Measurements
- components: final 23, mean 23.0, max 41; occupancy final 0.27
- tracks: 347; persistent (alive >= 50% of run): 23; longest 214 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 4.67 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [23, 23, 23], H1 [0, 0, 0]
- motion: 23 long-lived tracks moved >= 1 body length; max speed 0.273/time; max body lengths 72.8
- replication (lineage window K = 40 frames = time 1000, --lineage-k): splits 93, persistent splits 2 (0 more failed only because the siblings re-merged within K), max generation 1, merges 83, merge/split ratio 0.892, nucleations 97
- channel total drift (end/start - 1): [0.1589, 95.0]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 259 at frame 135: holes 0, rim-vs-core 0.26, rim-vs-outside 0.35, heterogeneity 0.20; core [0.917, 0.369] rim [0.655, 0.411]
  - track 263 at frame 135: holes 0, rim-vs-core 0.26, rim-vs-outside 0.37, heterogeneity 0.20; core [0.931, 0.392] rim [0.675, 0.409]
  - track 268 at frame 135: holes 0, rim-vs-core 0.27, rim-vs-outside 0.35, heterogeneity 0.20; core [0.926, 0.44] rim [0.661, 0.43]
  - track 328 at frame 143: holes 0, rim-vs-core 0.26, rim-vs-outside 0.35, heterogeneity 0.19; core [0.917, 0.343] rim [0.663, 0.398]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 138 components >= 12 px at frames [40, 81, 121, 159, 200, 240]):
  - radial phi: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.819, rim/outside 7.14 (aggregate of 138 individuals; 0/138 membrane-like individually; rim level 0.796)
  - radial psi: peak at rho=1.65 (OUTSIDE the peak band 0.5-1.5), rim/core 1.25, rim/outside 0.944 (aggregate of 138 individuals; 0/138 membrane-like individually; rim level 0.563)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #259 (t=3375, R_eq 12.02): none; #263 (t=3375, R_eq 12.09): none; #268 (t=3375, R_eq 11.69): none; #328 (t=3575, R_eq 10.14): none

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
