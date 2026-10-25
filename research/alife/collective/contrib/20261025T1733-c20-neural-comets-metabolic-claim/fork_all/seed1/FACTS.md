# Evidence pack: neural-field-dep-fork (seed 1)

- world: `../../world_fork.py`, family `neural-field`
- parent: None; mutation: c20 neural-field comets plus synaptic depression: the coupling output is scaled by a resource r that firing depletes and that recovers on time tr
- run: 201 frames x 50 steps x dt 0.1 = time 1000; grid [128, 128]; wall 9s; status ok
- command: `python -m labkit.run /tmp/c20nfe/world_fork.py --out /tmp/c20nfe/cut_all --seeds 0 1 --spf 50 --no-movie`
- segmentation: matter > 0.50 of robust range [0.0, 1.0], min area 6 px

## Measurements
- components: final 0, mean 24.3, max 70; occupancy final 0.00
- tracks: 555; persistent (alive >= 50% of run): 0; longest 62 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 0.00 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [51, 24, 3], H1 [40, 6, 0]
- motion: 66 long-lived tracks moved >= 1 body length; max speed 0.569/time; max body lengths 25.6
- replication (lineage window K = 20 frames = time 100, default): splits 211, persistent splits 11 (0 more failed only because the siblings re-merged within K), max generation 3, merges 58, merge/split ratio 0.275, nucleations 6
- channel total drift (end/start - 1): [1.0, None, -0.9983, -0.3313]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 268 at frame 50: holes 0, rim-vs-core 0.26, rim-vs-outside 0.91, heterogeneity 0.16; core [0.956, 0.568, 1.0, 0.516] rim [0.706, 0.516, 0.939, 0.498]
  - track 365 at frame 79: holes 0, rim-vs-core 0.26, rim-vs-outside 0.88, heterogeneity 0.15; core [0.961, 0.566, 1.0, 0.546] rim [0.724, 0.488, 0.939, 0.576]
  - track 254 at frame 45: holes 0, rim-vs-core 0.22, rim-vs-outside 0.87, heterogeneity 0.15; core [0.944, 0.529, 1.0, 0.551] rim [0.737, 0.488, 0.943, 0.58]
  - track 512 at frame 106: holes 0, rim-vs-core 0.28, rim-vs-outside 0.85, heterogeneity 0.17; core [0.915, 0.541, 1.0, 0.397] rim [0.665, 0.475, 0.883, 0.402]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 115 components >= 12 px at frames [34, 67, 101]):
  - radial activity u: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.792, rim/outside 3.22 (aggregate of 115 individuals; 0/115 membrane-like individually; rim level 0.727)
  - radial adaptation a: peak at rho=0.35 (OUTSIDE the peak band 0.5-1.5), rim/core 0.848, rim/outside 1.97 (aggregate of 115 individuals; 3/115 membrane-like individually; rim level 0.544)
  - radial firing f(u): peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.86, rim/outside 35.1 (aggregate of 115 individuals; 0/115 membrane-like individually; rim level 0.835)
  - radial synaptic resource r: peak at rho=2.45 (OUTSIDE the peak band 0.5-1.5), rim/core 1.25, rim/outside 0.9 (aggregate of 115 individuals; 0/115 membrane-like individually; rim level 0.527)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #268 (t=250, R_eq 3.48): none; #365 (t=395, R_eq 3.61): none; #254 (t=225, R_eq 4.18): none; #512 (t=530, R_eq 3.09): none

## Warnings
- no components at the end: matter died out or fell below threshold
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 1 of 115 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
