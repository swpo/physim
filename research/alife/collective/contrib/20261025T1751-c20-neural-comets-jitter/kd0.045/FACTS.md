# Evidence pack: neural-field-dep (seed 3)

- world: `../../c20nfd/world.py`, family `neural-field`
- parent: None; mutation: c20 neural-field comets plus synaptic depression: the coupling output is scaled by a resource r that firing depletes and that recovers on time tr
- run: 201 frames x 50 steps x dt 0.1 = time 1000; grid [128, 128]; wall 8s; status ok
- command: `python -m labkit.run /tmp/c20nfd/world.py --out /tmp/c20jit/kd0.045 --seeds 3 --spf 50 --no-movie`
- segmentation: matter > 0.50 of robust range [0.0, 1.0], min area 6 px

## Measurements
- components: final 40, mean 45.2, max 74; occupancy final 0.11
- tracks: 1040; persistent (alive >= 50% of run): 0; longest 94 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 0.00 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [42, 41, 39], H1 [0, 0, 0]
- motion: 113 long-lived tracks moved >= 1 body length; max speed 0.566/time; max body lengths 33.5
- replication (lineage window K = 20 frames = time 100, default): splits 420, persistent splits 22 (0 more failed only because the siblings re-merged within K), max generation 5, merges 132, merge/split ratio 0.314, nucleations 6
- channel total drift (end/start - 1): [-1.0, None, -0.5261, -0.1961]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 388 at frame 84: holes 0, rim-vs-core 0.30, rim-vs-outside 0.86, heterogeneity 0.17; core [0.887, 0.544, 1.0, 0.292] rim [0.653, 0.427, 0.888, 0.377]
  - track 370 at frame 74: holes 0, rim-vs-core 0.26, rim-vs-outside 0.87, heterogeneity 0.15; core [0.904, 0.622, 1.0, 0.303] rim [0.686, 0.533, 0.927, 0.371]
  - track 449 at frame 89: holes 0, rim-vs-core 0.26, rim-vs-outside 0.86, heterogeneity 0.18; core [0.901, 0.463, 1.0, 0.322] rim [0.666, 0.446, 0.896, 0.344]
  - track 924 at frame 187: holes 0, rim-vs-core 0.27, rim-vs-outside 0.78, heterogeneity 0.17; core [0.909, 0.502, 1.0, 0.229] rim [0.683, 0.418, 0.899, 0.292]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 254 components >= 12 px at frames [34, 67, 101, 133, 166, 200]):
  - radial activity u: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.79, rim/outside 2.93 (aggregate of 254 individuals; 0/254 membrane-like individually; rim level 0.703)
  - radial adaptation a: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.887, rim/outside 1.99 (aggregate of 254 individuals; 5/254 membrane-like individually; rim level 0.556)
  - radial firing f(u): peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.853, rim/outside 28.9 (aggregate of 254 individuals; 2/254 membrane-like individually; rim level 0.819)
  - radial synaptic resource r: peak at rho=2.45 (OUTSIDE the peak band 0.5-1.5), rim/core 1.45, rim/outside 0.862 (aggregate of 254 individuals; 12/254 membrane-like individually; rim level 0.382)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #388 (t=420, R_eq 3.39): none; #370 (t=370, R_eq 2.93): none; #449 (t=445, R_eq 3.7): none; #924 (t=935, R_eq 3.61): none

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 3 of 254 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
