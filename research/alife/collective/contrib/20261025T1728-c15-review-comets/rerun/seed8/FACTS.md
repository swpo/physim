# Evidence pack: neural-field-dep (seed 8)

- world: `../../world.py`, family `neural-field`
- parent: None; mutation: c20 neural-field comets plus synaptic depression: the coupling output is scaled by a resource r that firing depletes and that recovers on time tr
- run: 201 frames x 50 steps x dt 0.1 = time 1000; grid [128, 128]; wall 7s; status ok
- command: `python -m labkit.run /root/rev5/world.py --out /root/rev5/rerun --seeds 7 8 --spf 50 --no-movie`
- segmentation: matter > 0.50 of robust range [0.0, 1.0], min area 6 px

## Measurements
- components: final 33, mean 39.8, max 69; occupancy final 0.10
- tracks: 643; persistent (alive >= 50% of run): 4; longest 125 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 6.50 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [33, 33, 33], H1 [0, 0, 0]
- motion: 121 long-lived tracks moved >= 1 body length; max speed 0.6/time; max body lengths 57.0
- replication (lineage window K = 20 frames = time 100, default): splits 247, persistent splits 23 (0 more failed only because the siblings re-merged within K), max generation 3, merges 75, merge/split ratio 0.304, nucleations 7
- channel total drift (end/start - 1): [-1.0, None, -0.533, -0.197]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 455 at frame 138: holes 0, rim-vs-core 0.30, rim-vs-outside 0.85, heterogeneity 0.18; core [0.901, 0.47, 1.0, 0.204] rim [0.655, 0.408, 0.87, 0.312]
  - track 485 at frame 139: holes 0, rim-vs-core 0.22, rim-vs-outside 0.92, heterogeneity 0.16; core [0.883, 0.507, 1.0, 0.269] rim [0.679, 0.463, 0.928, 0.309]
  - track 515 at frame 148: holes 0, rim-vs-core 0.22, rim-vs-outside 0.91, heterogeneity 0.15; core [0.887, 0.397, 1.0, 0.294] rim [0.762, 0.556, 0.964, 0.225]
  - track 585 at frame 168: holes 0, rim-vs-core 0.27, rim-vs-outside 0.86, heterogeneity 0.20; core [0.963, 0.477, 1.0, 0.474] rim [0.711, 0.404, 0.926, 0.498]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 215 components >= 12 px at frames [34, 67, 101, 133, 166, 200]):
  - radial activity u: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.778, rim/outside 2.94 (aggregate of 215 individuals; 0/215 membrane-like individually; rim level 0.698)
  - radial adaptation a: peak at rho=0.25 (OUTSIDE the peak band 0.5-1.5), rim/core 0.9, rim/outside 1.93 (aggregate of 215 individuals; 4/215 membrane-like individually; rim level 0.535)
  - radial firing f(u): peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.821, rim/outside 25.8 (aggregate of 215 individuals; 0/215 membrane-like individually; rim level 0.791)
  - radial synaptic resource r: peak at rho=2.45 (OUTSIDE the peak band 0.5-1.5), rim/core 1.41, rim/outside 0.913 (aggregate of 215 individuals; 9/215 membrane-like individually; rim level 0.411)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #455 (t=690, R_eq 3.48): none; #485 (t=695, R_eq 2.88): none; #515 (t=740, R_eq 2.93): none; #585 (t=840, R_eq 3.52): none

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 4 of 215 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
