# Evidence pack: neural-field-dep-fork (seed 5)

- world: `../../world.py`, family `neural-field`
- parent: None; mutation: c20 neural-field comets plus synaptic depression: the coupling output is scaled by a resource r that firing depletes and that recovers on time tr
- run: 201 frames x 50 steps x dt 0.1 = time 1000; grid [128, 128]; wall 5s; status ok
- command: `python -m labkit.run world.py --out fork_all --seeds 5 6 --frames 200 --spf 50 --no-movie`
- segmentation: matter > 0.50 of robust range [0.0, 1.0], min area 6 px

## Measurements
- components: final 0, mean 23.0, max 70; occupancy final 0.00
- tracks: 544; persistent (alive >= 50% of run): 0; longest 54 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 0.00 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [50, 24, 5], H1 [39, 11, 0]
- motion: 61 long-lived tracks moved >= 1 body length; max speed 0.582/time; max body lengths 21.7
- replication (lineage window K = 20 frames = time 100, default): splits 218, persistent splits 4 (0 more failed only because the siblings re-merged within K), max generation 2, merges 55, merge/split ratio 0.252, nucleations 5
- channel total drift (end/start - 1): [-1.0, None, -0.9986, -0.3371]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 193 at frame 39: holes 0, rim-vs-core 0.31, rim-vs-outside 0.84, heterogeneity 0.17; core [0.905, 0.605, 1.0, 0.455] rim [0.663, 0.469, 0.873, 0.52]
  - track 359 at frame 79: holes 0, rim-vs-core 0.24, rim-vs-outside 0.85, heterogeneity 0.15; core [0.884, 0.511, 1.0, 0.417] rim [0.68, 0.459, 0.901, 0.476]
  - track 227 at frame 39: holes 0, rim-vs-core 0.25, rim-vs-outside 0.87, heterogeneity 0.17; core [0.896, 0.644, 1.0, 0.421] rim [0.718, 0.515, 0.883, 0.451]
  - track 462 at frame 87: holes 0, rim-vs-core 0.27, rim-vs-outside 0.85, heterogeneity 0.16; core [0.886, 0.529, 1.0, 0.41] rim [0.665, 0.44, 0.877, 0.471]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 112 components >= 12 px at frames [34, 67, 101, 133]):
  - radial activity u: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.79, rim/outside 3.11 (aggregate of 112 individuals; 0/112 membrane-like individually; rim level 0.715)
  - radial adaptation a: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.88, rim/outside 2.11 (aggregate of 112 individuals; 2/112 membrane-like individually; rim level 0.578)
  - radial firing f(u): peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.85, rim/outside 28.5 (aggregate of 112 individuals; 0/112 membrane-like individually; rim level 0.814)
  - radial synaptic resource r: peak at rho=2.45 (OUTSIDE the peak band 0.5-1.5), rim/core 1.28, rim/outside 0.914 (aggregate of 112 individuals; 0/112 membrane-like individually; rim level 0.539)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #193 (t=195, R_eq 3.19): none; #359 (t=395, R_eq 3.91): none; #227 (t=195, R_eq 3.14): none; #462 (t=435, R_eq 3.87): none

## Warnings
- no components at the end: matter died out or fell below threshold
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 2 of 112 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
