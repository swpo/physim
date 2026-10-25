# Evidence pack: neural-field (seed 0)

- world: `../../world.py`, family `neural-field`
- parent: None; mutation: new class: Amari neural field with an oscillatory Laing-Troy kernel and linear adaptation
- run: 201 frames x 30 steps x dt 0.1 = time 600; grid [128, 128]; wall 4s; status ok
- command: `python -m labkit.run collective/contrib/20261025T1707-c20-neural-field-comets/world.py --out collective/contrib/20261025T1707-c20-neural-field-comets/pack --seeds 0 1 --no-movie`
- segmentation: matter > 0.50 of robust range [0.0, 1.0], min area 6 px

## Measurements
- components: final 16, mean 18.9, max 72; occupancy final 0.05
- tracks: 162; persistent (alive >= 50% of run): 7; longest 175 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 23.27 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [16, 16, 16], H1 [0, 0, 0]
- motion: 55 long-lived tracks moved >= 1 body length; max speed 0.484/time; max body lengths 32.3
- replication (lineage window K = 20 frames = time 60, default): splits 39, persistent splits 12 (0 more failed only because the siblings re-merged within K), max generation 5, merges 15, merge/split ratio 0.385, nucleations 0
- channel total drift (end/start - 1): [-1.0, None, -0.6954]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 85 at frame 114: holes 0, rim-vs-core 0.23, rim-vs-outside 0.97, heterogeneity 0.14; core [0.968, 0.627, 1.0] rim [0.747, 0.562, 0.972]
  - track 109 at frame 139: holes 0, rim-vs-core 0.23, rim-vs-outside 0.96, heterogeneity 0.15; core [0.931, 0.525, 1.0] rim [0.711, 0.491, 0.945]
  - track 36 at frame 61: holes 0, rim-vs-core 0.22, rim-vs-outside 0.91, heterogeneity 0.15; core [0.964, 0.642, 1.0] rim [0.779, 0.521, 0.977]
  - track 154 at frame 183: holes 0, rim-vs-core 0.21, rim-vs-outside 0.97, heterogeneity 0.14; core [0.949, 0.554, 1.0] rim [0.749, 0.501, 0.973]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 105 components >= 12 px at frames [34, 67, 101, 133, 166, 200]):
  - radial activity u: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.782, rim/outside 2.59 (aggregate of 105 individuals; 0/105 membrane-like individually; rim level 0.664)
  - radial adaptation a: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.904, rim/outside 1.94 (aggregate of 105 individuals; 4/105 membrane-like individually; rim level 0.543)
  - radial firing f(u): peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.783, rim/outside 14.1 (aggregate of 105 individuals; 2/105 membrane-like individually; rim level 0.701)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #85 (t=342, R_eq 3.29): none; #109 (t=417, R_eq 5.11): none; #36 (t=183, R_eq 3.52): none; #154 (t=549, R_eq 4.15): none

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 3 of 105 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
