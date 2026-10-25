# Evidence pack: active-gel-fed-comets-twin (seed 0)

- world: `../../world_twin_global.py`, family `active-gel`
- parent: none (new class); mutation: new class: advection of stress generator and regulator by a contractile active-gel flow
- run: 201 frames x 100 steps x dt 0.01 = time 200; grid [128, 128]; wall 55s; status ok
- command: `python -m labkit.run collective/contrib/20261025T1046-c09-active-gel-bd-twin/world_twin_global.py --out collective/contrib/20261025T1046-c09-active-gel-bd-twin/pack_global --seeds 0 1 --frames 200 --no-movie`
- segmentation: matter > 0.31 of robust range [0.0, 3.1869], min area 6 px

## Measurements
- components: final 1, mean 5.5, max 41; occupancy final 0.00
- tracks: 190; persistent (alive >= 50% of run): 0; longest 85 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 0.00 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [1, 1, 1], H1 [0, 0, 0]
- motion: 5 long-lived tracks moved >= 1 body length; max speed 2.95/time; max body lengths 10.0
- replication (lineage window K = 20 frames = time 20, default): splits 73, persistent splits 0 (0 more failed only because the siblings re-merged within K), max generation 0, merges 0, merge/split ratio 0, nucleations 44
- channel total drift (end/start - 1): [-0.9808, -0.7877, -0.0841]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 189 at frame 158: holes 0, rim-vs-core 0.25, rim-vs-outside 0.17, heterogeneity 0.09; core [0.749, 0.228, 0.26] rim [0.51, 0.213, 0.325]
  - track 178 at frame 77: holes 0, rim-vs-core 0.38, rim-vs-outside 0.43, heterogeneity 0.12; core [0.995, 0.578, 0.219] rim [0.63, 0.545, 0.316]
  - track 177 at frame 69: holes 0, rim-vs-core 0.38, rim-vs-outside 0.34, heterogeneity 0.11; core [0.932, 0.727, 0.124] rim [0.57, 0.684, 0.221]
  - track 27 at frame 18: holes 0, rim-vs-core 0.36, rim-vs-outside 0.33, heterogeneity 0.10; core [0.937, 0.925, 0.028] rim [0.581, 0.896, 0.077]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 18 components >= 12 px at frames [34, 67, 101, 133, 166, 200]):
  - radial generator a: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.846, rim/outside 6.63 (aggregate of 18 individuals; 0/18 membrane-like individually; rim level 0.697)
  - radial regulator b: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.981, rim/outside 1.04 (aggregate of 18 individuals; 0/18 membrane-like individually; rim level 0.689)
  - radial substrate s: peak at rho=2.35 (OUTSIDE the peak band 0.5-1.5), rim/core 2.15, rim/outside 0.779 (aggregate of 18 individuals; 0/18 membrane-like individually; rim level 0.175)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #189 (t=158, R_eq 4.58): none; #178 (t=77, R_eq 6.08): none; #177 (t=69, R_eq 7.46): none; #27 (t=18, R_eq 6.38): none

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
