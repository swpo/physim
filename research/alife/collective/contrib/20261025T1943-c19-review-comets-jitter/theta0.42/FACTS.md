# Evidence pack: neural-field-dep-fork (seed 6)

- world: `../../20261025T1733-c20-neural-comets-metabolic-claim/world.py`, family `neural-field`
- parent: None; mutation: c20 neural-field comets plus synaptic depression: the coupling output is scaled by a resource r that firing depletes and that recovers on time tr
- run: 201 frames x 50 steps x dt 0.1 = time 1000; grid [128, 128]; wall 5s; status ok
- command: `python -m labkit.run collective/contrib/20261025T1733-c20-neural-comets-metabolic-claim/world.py --out collective/contrib/20261025T1943-c19-review-comets-jitter/theta0.42 --seeds 6 --spf 50 --no-movie`
- segmentation: matter > 0.50 of robust range [0.0, 1.0], min area 6 px

## Measurements
- components: final 24, mean 28.9, max 62; occupancy final 0.08
- tracks: 450; persistent (alive >= 50% of run): 1; longest 141 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 8.62 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [24, 24, 24], H1 [0, 0, 0]
- motion: 97 long-lived tracks moved >= 1 body length; max speed 0.568/time; max body lengths 53.1
- replication (lineage window K = 20 frames = time 100, default): splits 165, persistent splits 26 (0 more failed only because the siblings re-merged within K), max generation 5, merges 44, merge/split ratio 0.267, nucleations 9
- channel total drift (end/start - 1): [1.0, None, -0.5952, -0.133]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 122 at frame 79: holes 0, rim-vs-core 0.25, rim-vs-outside 0.87, heterogeneity 0.16; core [0.902, 0.478, 1.0, 0.128] rim [0.684, 0.431, 0.926, 0.209]
  - track 148 at frame 62: holes 0, rim-vs-core 0.24, rim-vs-outside 0.79, heterogeneity 0.18; core [0.921, 0.515, 1.0, 0.379] rim [0.723, 0.448, 0.894, 0.448]
  - track 278 at frame 124: holes 0, rim-vs-core 0.31, rim-vs-outside 0.82, heterogeneity 0.20; core [0.928, 0.518, 1.0, 0.461] rim [0.68, 0.418, 0.867, 0.557]
  - track 421 at frame 190: holes 0, rim-vs-core 0.25, rim-vs-outside 0.88, heterogeneity 0.18; core [0.946, 0.549, 1.0, 0.389] rim [0.719, 0.469, 0.939, 0.404]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 165 components >= 12 px at frames [34, 67, 101, 133, 166, 200]):
  - radial activity u: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.788, rim/outside 3.01 (aggregate of 165 individuals; 0/165 membrane-like individually; rim level 0.714)
  - radial adaptation a: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.867, rim/outside 2.04 (aggregate of 165 individuals; 0/165 membrane-like individually; rim level 0.544)
  - radial firing f(u): peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.832, rim/outside 27.2 (aggregate of 165 individuals; 0/165 membrane-like individually; rim level 0.801)
  - radial synaptic resource r: peak at rho=2.45 (OUTSIDE the peak band 0.5-1.5), rim/core 1.54, rim/outside 0.853 (aggregate of 165 individuals; 3/165 membrane-like individually; rim level 0.455)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #122 (t=395, R_eq 3.14): none; #148 (t=310, R_eq 3.7): none; #278 (t=620, R_eq 3.83): none; #421 (t=950, R_eq 3.43): none

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 3 of 165 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
