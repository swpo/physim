# Evidence pack: neural-field-dep-graded-fork (seed 24)

- world: `../../world_graded.py`, family `neural-field`
- parent: None; mutation: c20 neural-field comets plus synaptic depression: the coupling output is scaled by a resource r that firing depletes and that recovers on time tr
- run: 201 frames x 50 steps x dt 0.1 = time 1000; grid [128, 128]; wall 8s; status ok
- command: `python -m labkit.run collective/contrib/20261025T1832-c24-review-comets-metabolic/world_graded.py --out collective/contrib/20261025T1832-c24-review-comets-metabolic/tr_x2/seed24 --seeds 24 --spf 50 --no-movie`
- segmentation: matter > 0.50 of robust range [0.0, 1.0], min area 6 px

## Measurements
- components: final 17, mean 35.2, max 70; occupancy final 0.05
- tracks: 584; persistent (alive >= 50% of run): 4; longest 126 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 15.50 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [17, 17, 17], H1 [0, 0, 0]
- motion: 108 long-lived tracks moved >= 1 body length; max speed 0.579/time; max body lengths 54.5
- replication (lineage window K = 20 frames = time 100, default): splits 234, persistent splits 20 (0 more failed only because the siblings re-merged within K), max generation 3, merges 48, merge/split ratio 0.205, nucleations 11
- channel total drift (end/start - 1): [-1.0, None, -0.7645, -0.178]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 231 at frame 77: holes 0, rim-vs-core 0.20, rim-vs-outside 0.92, heterogeneity 0.16; core [0.908, 0.511, 1.0, 0.46] rim [0.719, 0.47, 0.943, 0.494]
  - track 353 at frame 116: holes 0, rim-vs-core 0.26, rim-vs-outside 0.86, heterogeneity 0.13; core [0.877, 0.548, 1.0, 0.105] rim [0.678, 0.445, 0.957, 0.218]
  - track 381 at frame 119: holes 0, rim-vs-core 0.29, rim-vs-outside 0.78, heterogeneity 0.16; core [0.85, 0.558, 1.0, 0.211] rim [0.636, 0.492, 0.834, 0.283]
  - track 554 at frame 183: holes 0, rim-vs-core 0.24, rim-vs-outside 0.87, heterogeneity 0.14; core [0.883, 0.591, 1.0, 0.146] rim [0.689, 0.528, 0.938, 0.247]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 198 components >= 12 px at frames [34, 67, 101, 133, 166, 200]):
  - radial activity u: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.807, rim/outside 3.09 (aggregate of 198 individuals; 0/198 membrane-like individually; rim level 0.733)
  - radial adaptation a: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.882, rim/outside 2.07 (aggregate of 198 individuals; 5/198 membrane-like individually; rim level 0.559)
  - radial firing f(u): peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.891, rim/outside 32.8 (aggregate of 198 individuals; 2/198 membrane-like individually; rim level 0.858)
  - radial synaptic resource r: peak at rho=2.45 (OUTSIDE the peak band 0.5-1.5), rim/core 1.39, rim/outside 0.856 (aggregate of 198 individuals; 7/198 membrane-like individually; rim level 0.402)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #231 (t=385, R_eq 4.69): none; #353 (t=580, R_eq 2.88): none; #381 (t=595, R_eq 2.93): none; #554 (t=915, R_eq 3.39): none

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 4 of 198 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
