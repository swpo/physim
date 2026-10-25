# Evidence pack: neural-field-dep-fork (seed 4)

- world: `../../../20261025T1733-c20-neural-comets-metabolic-claim/world.py`, family `neural-field`
- parent: None; mutation: c20 neural-field comets plus synaptic depression: the coupling output is scaled by a resource r that firing depletes and that recovers on time tr
- run: 201 frames x 50 steps x dt 0.1 = time 1000; grid [128, 128]; wall 5s; status ok
- command: `python -m labkit.run collective/contrib/20261025T1733-c20-neural-comets-metabolic-claim/world.py --out collective/contrib/20261025T1815-c19-review-neural-comets/cut_left/seed4 --seeds 4 --spf 50 --no-movie`
- segmentation: matter > 0.50 of robust range [0.0, 1.0], min area 6 px

## Measurements
- components: final 14, mean 30.8, max 73; occupancy final 0.05
- tracks: 659; persistent (alive >= 50% of run): 0; longest 74 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 0.00 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [14, 14, 14], H1 [0, 0, 0]
- motion: 78 long-lived tracks moved >= 1 body length; max speed 0.593/time; max body lengths 31.6
- replication (lineage window K = 20 frames = time 100, default): splits 262, persistent splits 21 (0 more failed only because the siblings re-merged within K), max generation 5, merges 61, merge/split ratio 0.233, nucleations 8
- channel total drift (end/start - 1): [-1.0, None, -0.7965, -0.2758]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 450 at frame 104: holes 0, rim-vs-core 0.21, rim-vs-outside 0.85, heterogeneity 0.15; core [0.913, 0.556, 1.0, 0.489] rim [0.72, 0.511, 0.931, 0.507]
  - track 563 at frame 148: holes 0, rim-vs-core 0.26, rim-vs-outside 0.84, heterogeneity 0.17; core [0.96, 0.627, 1.0, 0.605] rim [0.731, 0.524, 0.926, 0.633]
  - track 600 at frame 170: holes 0, rim-vs-core 0.24, rim-vs-outside 0.86, heterogeneity 0.14; core [0.926, 0.553, 1.0, 0.349] rim [0.71, 0.483, 0.941, 0.399]
  - track 605 at frame 165: holes 0, rim-vs-core 0.27, rim-vs-outside 0.87, heterogeneity 0.18; core [0.96, 0.464, 1.0, 0.559] rim [0.707, 0.404, 0.939, 0.594]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 166 components >= 12 px at frames [34, 67, 101, 133, 166, 200]):
  - radial activity u: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.796, rim/outside 3.03 (aggregate of 166 individuals; 0/166 membrane-like individually; rim level 0.709)
  - radial adaptation a: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.858, rim/outside 1.97 (aggregate of 166 individuals; 4/166 membrane-like individually; rim level 0.544)
  - radial firing f(u): peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.862, rim/outside 26.7 (aggregate of 166 individuals; 1/166 membrane-like individually; rim level 0.814)
  - radial synaptic resource r: peak at rho=2.25 (OUTSIDE the peak band 0.5-1.5), rim/core 1.23, rim/outside 0.93 (aggregate of 166 individuals; 1/166 membrane-like individually; rim level 0.549)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #450 (t=520, R_eq 3.61): none; #563 (t=740, R_eq 3.52): none; #600 (t=850, R_eq 2.93): none; #605 (t=825, R_eq 3.19): ['adaptation a']

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 4 of 166 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
