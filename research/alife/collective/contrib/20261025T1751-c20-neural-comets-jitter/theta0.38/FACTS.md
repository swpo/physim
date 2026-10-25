# Evidence pack: neural-field-dep (seed 3)

- world: `../../c20nfd/world.py`, family `neural-field`
- parent: None; mutation: c20 neural-field comets plus synaptic depression: the coupling output is scaled by a resource r that firing depletes and that recovers on time tr
- run: 201 frames x 50 steps x dt 0.1 = time 1000; grid [128, 128]; wall 8s; status ok
- command: `python -m labkit.run /tmp/c20nfd/world.py --out /tmp/c20jit/theta0.38 --seeds 3 --spf 50 --no-movie`
- segmentation: matter > 0.50 of robust range [0.0, 1.0], min area 6 px

## Measurements
- components: final 46, mean 49.7, max 82; occupancy final 0.13
- tracks: 1241; persistent (alive >= 50% of run): 0; longest 60 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 0.00 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [48, 48, 47], H1 [0, 0, 0]
- motion: 125 long-lived tracks moved >= 1 body length; max speed 0.606/time; max body lengths 26.1
- replication (lineage window K = 20 frames = time 100, default): splits 499, persistent splits 27 (0 more failed only because the siblings re-merged within K), max generation 5, merges 159, merge/split ratio 0.319, nucleations 8
- channel total drift (end/start - 1): [-1.0, None, -0.4502, -0.2401]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 931 at frame 160: holes 0, rim-vs-core 0.25, rim-vs-outside 0.89, heterogeneity 0.15; core [0.907, 0.48, 1.0, 0.247] rim [0.671, 0.436, 0.943, 0.277]
  - track 996 at frame 175: holes 0, rim-vs-core 0.28, rim-vs-outside 0.87, heterogeneity 0.17; core [0.946, 0.542, 1.0, 0.405] rim [0.698, 0.45, 0.939, 0.46]
  - track 295 at frame 37: holes 0, rim-vs-core 0.24, rim-vs-outside 0.83, heterogeneity 0.15; core [0.893, 0.47, 1.0, 0.166] rim [0.677, 0.431, 0.933, 0.23]
  - track 989 at frame 161: holes 0, rim-vs-core 0.20, rim-vs-outside 0.90, heterogeneity 0.14; core [0.865, 0.491, 1.0, 0.275] rim [0.679, 0.449, 0.946, 0.328]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 283 components >= 12 px at frames [34, 67, 101, 133, 166, 200]):
  - radial activity u: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.798, rim/outside 2.94 (aggregate of 283 individuals; 0/283 membrane-like individually; rim level 0.701)
  - radial adaptation a: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.873, rim/outside 1.92 (aggregate of 283 individuals; 8/283 membrane-like individually; rim level 0.542)
  - radial firing f(u): peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.849, rim/outside 29.8 (aggregate of 283 individuals; 4/283 membrane-like individually; rim level 0.806)
  - radial synaptic resource r: peak at rho=2.35 (OUTSIDE the peak band 0.5-1.5), rim/core 1.54, rim/outside 0.89 (aggregate of 283 individuals; 7/283 membrane-like individually; rim level 0.37)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #931 (t=800, R_eq 3.24): none; #996 (t=875, R_eq 3.61): none; #295 (t=185, R_eq 2.99): none; #989 (t=805, R_eq 4.62): none

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 7 of 283 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
