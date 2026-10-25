# Evidence pack: neural-field-dep (seed 3)

- world: `../../c20nfd/world.py`, family `neural-field`
- parent: None; mutation: c20 neural-field comets plus synaptic depression: the coupling output is scaled by a resource r that firing depletes and that recovers on time tr
- run: 201 frames x 50 steps x dt 0.1 = time 1000; grid [128, 128]; wall 8s; status ok
- command: `python -m labkit.run /tmp/c20nfd/world.py --out /tmp/c20jit/theta0.42 --seeds 3 --spf 50 --no-movie`
- segmentation: matter > 0.50 of robust range [0.0, 1.0], min area 6 px

## Measurements
- components: final 25, mean 24.4, max 73; occupancy final 0.06
- tracks: 423; persistent (alive >= 50% of run): 0; longest 100 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 0.00 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [26, 25, 25], H1 [0, 0, 0]
- motion: 79 long-lived tracks moved >= 1 body length; max speed 0.605/time; max body lengths 31.8
- replication (lineage window K = 20 frames = time 100, default): splits 155, persistent splits 19 (0 more failed only because the siblings re-merged within K), max generation 6, merges 39, merge/split ratio 0.252, nucleations 7
- channel total drift (end/start - 1): [-1.0, None, -0.7012, -0.1339]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 244 at frame 92: holes 0, rim-vs-core 0.25, rim-vs-outside 0.93, heterogeneity 0.17; core [0.938, 0.579, 1.0, 0.454] rim [0.703, 0.517, 0.945, 0.509]
  - track 14 at frame 45: holes 0, rim-vs-core 0.28, rim-vs-outside 0.89, heterogeneity 0.17; core [0.923, 0.613, 1.0, 0.264] rim [0.682, 0.518, 0.941, 0.36]
  - track 288 at frame 114: holes 0, rim-vs-core 0.29, rim-vs-outside 0.87, heterogeneity 0.17; core [0.936, 0.602, 1.0, 0.311] rim [0.69, 0.484, 0.899, 0.298]
  - track 402 at frame 188: holes 0, rim-vs-core 0.16, rim-vs-outside 1.05, heterogeneity 0.17; core [0.942, 0.506, 1.0, 0.477] rim [0.801, 0.486, 0.968, 0.54]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 135 components >= 12 px at frames [34, 67, 101, 133, 166, 200]):
  - radial activity u: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.78, rim/outside 2.94 (aggregate of 135 individuals; 0/135 membrane-like individually; rim level 0.702)
  - radial adaptation a: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.883, rim/outside 2 (aggregate of 135 individuals; 6/135 membrane-like individually; rim level 0.547)
  - radial firing f(u): peak at rho=0.25 (OUTSIDE the peak band 0.5-1.5), rim/core 0.815, rim/outside 23.2 (aggregate of 135 individuals; 1/135 membrane-like individually; rim level 0.77)
  - radial synaptic resource r: peak at rho=2.45 (OUTSIDE the peak band 0.5-1.5), rim/core 1.46, rim/outside 0.839 (aggregate of 135 individuals; 5/135 membrane-like individually; rim level 0.447)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #244 (t=460, R_eq 3.99): none; #14 (t=225, R_eq 2.99): none; #288 (t=570, R_eq 3.57): none; #402 (t=940, R_eq 6.48, ring): none

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 4 of 135 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
