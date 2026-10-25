# Evidence pack: neural-field-dep (seed 7)

- world: `../world.py`, family `neural-field`
- parent: None; mutation: c20 neural-field comets plus synaptic depression: the coupling output is scaled by a resource r that firing depletes and that recovers on time tr
- run: 201 frames x 30 steps x dt 0.1 = time 600; grid [128, 128]; wall 3s; status ok
- command: `python -m labkit.run world.py --out kd0.045 --seeds 7 --no-movie`
- segmentation: matter > 0.50 of robust range [0.0, 1.0], min area 6 px

## Measurements
- components: final 39, mean 44.0, max 72; occupancy final 0.11
- tracks: 684; persistent (alive >= 50% of run): 1; longest 102 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 6.00 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [39, 39, 39], H1 [0, 0, 0]
- motion: 137 long-lived tracks moved >= 1 body length; max speed 0.598/time; max body lengths 22.3
- replication (lineage window K = 20 frames = time 60, default): splits 261, persistent splits 27 (0 more failed only because the siblings re-merged within K), max generation 4, merges 99, merge/split ratio 0.379, nucleations 6
- channel total drift (end/start - 1): [1.0, None, -0.4238, -0.1937]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 483 at frame 150: holes 0, rim-vs-core 0.25, rim-vs-outside 0.82, heterogeneity 0.17; core [0.931, 0.549, 1.0, 0.402] rim [0.712, 0.481, 0.906, 0.397]
  - track 514 at frame 156: holes 0, rim-vs-core 0.26, rim-vs-outside 0.82, heterogeneity 0.17; core [0.903, 0.522, 1.0, 0.448] rim [0.674, 0.465, 0.896, 0.48]
  - track 463 at frame 136: holes 0, rim-vs-core 0.31, rim-vs-outside 0.89, heterogeneity 0.17; core [0.899, 0.654, 1.0, 0.31] rim [0.666, 0.501, 0.919, 0.402]
  - track 557 at frame 165: holes 0, rim-vs-core 0.32, rim-vs-outside 0.88, heterogeneity 0.18; core [0.934, 0.7, 1.0, 0.397] rim [0.757, 0.478, 0.925, 0.523]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 253 components >= 12 px at frames [34, 67, 101, 133, 166, 200]):
  - radial activity u: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.795, rim/outside 2.9 (aggregate of 253 individuals; 0/253 membrane-like individually; rim level 0.7)
  - radial adaptation a: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.892, rim/outside 1.91 (aggregate of 253 individuals; 9/253 membrane-like individually; rim level 0.534)
  - radial firing f(u): peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.853, rim/outside 28.3 (aggregate of 253 individuals; 3/253 membrane-like individually; rim level 0.803)
  - radial synaptic resource r: peak at rho=2.25 (OUTSIDE the peak band 0.5-1.5), rim/core 1.44, rim/outside 0.904 (aggregate of 253 individuals; 15/253 membrane-like individually; rim level 0.399)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #483 (t=450, R_eq 2.71): none; #514 (t=468, R_eq 4.22): none; #463 (t=408, R_eq 3.39): none; #557 (t=495, R_eq 3.83): none

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 9 of 253 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
