# Evidence pack: neural-field-dep-fork (seed 6)

- world: `../../20261025T1733-c20-neural-comets-metabolic-claim/world.py`, family `neural-field`
- parent: None; mutation: c20 neural-field comets plus synaptic depression: the coupling output is scaled by a resource r that firing depletes and that recovers on time tr
- run: 201 frames x 50 steps x dt 0.1 = time 1000; grid [128, 128]; wall 5s; status ok
- command: `python -m labkit.run collective/contrib/20261025T1733-c20-neural-comets-metabolic-claim/world.py --out collective/contrib/20261025T1943-c19-review-comets-jitter/kd0.055 --seeds 6 --spf 50 --no-movie`
- segmentation: matter > 0.50 of robust range [0.0, 1.0], min area 6 px

## Measurements
- components: final 33, mean 35.3, max 63; occupancy final 0.09
- tracks: 666; persistent (alive >= 50% of run): 0; longest 78 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 0.00 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [33, 33, 33], H1 [0, 0, 0]
- motion: 102 long-lived tracks moved >= 1 body length; max speed 0.6/time; max body lengths 32.3
- replication (lineage window K = 20 frames = time 100, default): splits 268, persistent splits 20 (0 more failed only because the siblings re-merged within K), max generation 4, merges 64, merge/split ratio 0.239, nucleations 7
- channel total drift (end/start - 1): [1.0, None, -0.5907, -0.1853]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 369 at frame 121: holes 0, rim-vs-core 0.22, rim-vs-outside 0.90, heterogeneity 0.18; core [0.905, 0.538, 1.0, 0.492] rim [0.715, 0.491, 0.915, 0.551]
  - track 299 at frame 91: holes 0, rim-vs-core 0.22, rim-vs-outside 0.90, heterogeneity 0.17; core [0.87, 0.475, 1.0, 0.254] rim [0.677, 0.451, 0.917, 0.293]
  - track 209 at frame 50: holes 0, rim-vs-core 0.21, rim-vs-outside 0.83, heterogeneity 0.14; core [0.898, 0.4, 1.0, 0.321] rim [0.697, 0.377, 0.927, 0.328]
  - track 500 at frame 150: holes 0, rim-vs-core 0.23, rim-vs-outside 0.87, heterogeneity 0.15; core [0.859, 0.575, 1.0, 0.236] rim [0.676, 0.502, 0.923, 0.323]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 191 components >= 12 px at frames [34, 67, 101, 133, 166, 200]):
  - radial activity u: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.776, rim/outside 2.89 (aggregate of 191 individuals; 0/191 membrane-like individually; rim level 0.697)
  - radial adaptation a: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.887, rim/outside 1.97 (aggregate of 191 individuals; 7/191 membrane-like individually; rim level 0.552)
  - radial firing f(u): peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.819, rim/outside 24.6 (aggregate of 191 individuals; 0/191 membrane-like individually; rim level 0.789)
  - radial synaptic resource r: peak at rho=2.45 (OUTSIDE the peak band 0.5-1.5), rim/core 1.46, rim/outside 0.863 (aggregate of 191 individuals; 9/191 membrane-like individually; rim level 0.432)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #369 (t=605, R_eq 5.05): none; #299 (t=455, R_eq 3.66): none; #209 (t=250, R_eq 2.39): none; #500 (t=750, R_eq 3.34): none

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 2 of 191 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
