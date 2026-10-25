# Evidence pack: neural-field-dep-graded-fork (seed 24)

- world: `../../world_graded.py`, family `neural-field`
- parent: None; mutation: c20 neural-field comets plus synaptic depression: the coupling output is scaled by a resource r that firing depletes and that recovers on time tr
- run: 201 frames x 50 steps x dt 0.1 = time 1000; grid [128, 128]; wall 8s; status ok
- command: `python -m labkit.run collective/contrib/20261025T1832-c24-review-comets-metabolic/world_graded.py --out collective/contrib/20261025T1832-c24-review-comets-metabolic/tr_x4/seed24 --seeds 24 --spf 50 --no-movie`
- segmentation: matter > 0.50 of robust range [0.0, 1.0], min area 6 px

## Measurements
- components: final 7, mean 26.1, max 70; occupancy final 0.05
- tracks: 519; persistent (alive >= 50% of run): 1; longest 105 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 7.75 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [7, 7, 7], H1 [0, 0, 0]
- motion: 74 long-lived tracks moved >= 1 body length; max speed 0.579/time; max body lengths 31.7
- replication (lineage window K = 20 frames = time 100, default): splits 202, persistent splits 12 (0 more failed only because the siblings re-merged within K), max generation 2, merges 46, merge/split ratio 0.228, nucleations 12
- channel total drift (end/start - 1): [-1.0, None, -0.7761, -0.2149]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 231 at frame 67: holes 0, rim-vs-core 0.28, rim-vs-outside 0.87, heterogeneity 0.17; core [0.906, 0.579, 1.0, 0.376] rim [0.678, 0.476, 0.927, 0.464]
  - track 481 at frame 143: holes 0, rim-vs-core 0.27, rim-vs-outside 0.76, heterogeneity 0.16; core [0.876, 0.615, 1.0, 0.113] rim [0.691, 0.528, 0.898, 0.254]
  - track 353 at frame 87: holes 0, rim-vs-core 0.31, rim-vs-outside 0.85, heterogeneity 0.17; core [0.931, 0.537, 1.0, 0.356] rim [0.67, 0.421, 0.889, 0.372]
  - track 290 at frame 64: holes 0, rim-vs-core 0.32, rim-vs-outside 0.86, heterogeneity 0.17; core [0.931, 0.548, 1.0, 0.32] rim [0.674, 0.429, 0.887, 0.405]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 138 components >= 12 px at frames [34, 67, 101, 133, 166, 200]):
  - radial activity u: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.799, rim/outside 3.1 (aggregate of 138 individuals; 0/138 membrane-like individually; rim level 0.726)
  - radial adaptation a: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.847, rim/outside 2.03 (aggregate of 138 individuals; 4/138 membrane-like individually; rim level 0.537)
  - radial firing f(u): peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.856, rim/outside 28 (aggregate of 138 individuals; 0/138 membrane-like individually; rim level 0.82)
  - radial synaptic resource r: peak at rho=2.45 (OUTSIDE the peak band 0.5-1.5), rim/core 1.39, rim/outside 0.874 (aggregate of 138 individuals; 6/138 membrane-like individually; rim level 0.417)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #231 (t=335, R_eq 3.52): none; #481 (t=715, R_eq 2.71): none; #353 (t=435, R_eq 3.04): none; #290 (t=320, R_eq 3.14): none

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 2 of 138 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
