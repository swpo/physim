# Evidence pack: neural-field-dep (seed 7)

- world: `../world.py`, family `neural-field`
- parent: None; mutation: c20 neural-field comets plus synaptic depression: the coupling output is scaled by a resource r that firing depletes and that recovers on time tr
- run: 201 frames x 100 steps x dt 0.05 (--dt; world META dt 0.1) = time 1000; grid [128, 128]; wall 16s; status ok
- command: `python -m labkit.run /root/rev5/world.py --out /root/rev5/dt2 --seeds 7 --spf 100 --dt 0.05 --no-movie`
- segmentation: matter > 0.50 of robust range [0.0, 1.0], min area 6 px

## Measurements
- components: final 40, mean 39.5, max 69; occupancy final 0.10
- tracks: 872; persistent (alive >= 50% of run): 0; longest 96 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 0.00 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [40, 40, 40], H1 [0, 0, 0]
- motion: 107 long-lived tracks moved >= 1 body length; max speed 0.617/time; max body lengths 40.6
- replication (lineage window K = 20 frames = time 100, default): splits 357, persistent splits 16 (0 more failed only because the siblings re-merged within K), max generation 4, merges 91, merge/split ratio 0.255, nucleations 9
- channel total drift (end/start - 1): [1.0, None, -0.4925, -0.1888]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 498 at frame 131: holes 0, rim-vs-core 0.25, rim-vs-outside 0.88, heterogeneity 0.15; core [0.939, 0.601, 1.0, 0.329] rim [0.718, 0.523, 0.975, 0.416]
  - track 286 at frame 64: holes 0, rim-vs-core 0.24, rim-vs-outside 0.91, heterogeneity 0.16; core [0.918, 0.529, 1.0, 0.419] rim [0.691, 0.497, 0.935, 0.443]
  - track 657 at frame 168: holes 0, rim-vs-core 0.34, rim-vs-outside 0.83, heterogeneity 0.19; core [0.901, 0.585, 1.0, 0.341] rim [0.648, 0.461, 0.851, 0.458]
  - track 693 at frame 173: holes 0, rim-vs-core 0.27, rim-vs-outside 0.83, heterogeneity 0.16; core [0.933, 0.527, 1.0, 0.28] rim [0.699, 0.431, 0.936, 0.337]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 227 components >= 12 px at frames [34, 67, 101, 133, 166, 200]):
  - radial activity u: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.779, rim/outside 2.92 (aggregate of 227 individuals; 0/227 membrane-like individually; rim level 0.7)
  - radial adaptation a: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.873, rim/outside 1.96 (aggregate of 227 individuals; 6/227 membrane-like individually; rim level 0.544)
  - radial firing f(u): peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.819, rim/outside 25.4 (aggregate of 227 individuals; 0/227 membrane-like individually; rim level 0.792)
  - radial synaptic resource r: peak at rho=2.45 (OUTSIDE the peak band 0.5-1.5), rim/core 1.49, rim/outside 0.878 (aggregate of 227 individuals; 8/227 membrane-like individually; rim level 0.423)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #498 (t=655, R_eq 2.99): none; #286 (t=320, R_eq 4.33): none; #657 (t=840, R_eq 3.24): none; #693 (t=865, R_eq 3.19): none

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- --dt 0.05 only relabels time (world META dt 0.1): the world's integration step is unchanged, so this run is NOT a dt/2 (or any time-step) test; change the world's own step for that

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
