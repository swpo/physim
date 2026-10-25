# Evidence pack: neural-field (seed 7)

- world: `../world.py`, family `neural-field`
- parent: None; mutation: new class: Amari neural field with an oscillatory Laing-Troy kernel and linear adaptation
- run: 201 frames x 50 steps x dt 0.1 = time 1000; grid [128, 128]; wall 12s; status ok
- command: `python -m labkit.run /root/rev6/world.py --out /root/rev6/rerun --seeds 7 --spf 50 --no-movie`
- segmentation: matter > 0.50 of robust range [0.0, 1.0], min area 6 px

## Measurements
- components: final 10, mean 11.4, max 56; occupancy final 0.13
- tracks: 73; persistent (alive >= 50% of run): 10; longest 201 frames; alive start-to-end: 3
- size of persistent tracks: max/min area ratio 72.00 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [10, 10, 10], H1 [0, 0, 0]
- motion: 18 long-lived tracks moved >= 1 body length; max speed 0.48/time; max body lengths 77.2
- replication (lineage window K = 20 frames = time 100, default): splits 9, persistent splits 2 (0 more failed only because the siblings re-merged within K), max generation 1, merges 2, merge/split ratio 0.222, nucleations 0
- channel total drift (end/start - 1): [1.0, None, -0.161]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 35 at frame 101: holes 0, rim-vs-core 0.22, rim-vs-outside 0.92, heterogeneity 0.13; core [0.977, 0.704, 1.0] rim [0.776, 0.619, 0.974]
  - track 69 at frame 121: holes 0, rim-vs-core 0.26, rim-vs-outside 0.87, heterogeneity 0.17; core [0.957, 0.613, 1.0] rim [0.722, 0.543, 0.925]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 64 components >= 12 px at frames [34, 67, 101, 133, 166, 200]):
  - radial activity u: peak at rho=0.25 (OUTSIDE the peak band 0.5-1.5), rim/core 0.853, rim/outside 2.25 (aggregate of 64 individuals; 0/64 membrane-like individually; rim level 0.642)
  - radial adaptation a: peak at rho=0.25 (OUTSIDE the peak band 0.5-1.5), rim/core 0.952, rim/outside 1.63 (aggregate of 64 individuals; 1/64 membrane-like individually; rim level 0.536)
  - radial firing f(u): peak at rho=0.25 (OUTSIDE the peak band 0.5-1.5), rim/core 0.858, rim/outside 8.72 (aggregate of 64 individuals; 5/64 membrane-like individually; rim level 0.624)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #5 (t=505, R_eq 15.82, ring): none; #35 (t=505, R_eq 3.09): none; #48 (t=505, R_eq 13.32, ring): none; #69 (t=605, R_eq 3.43): none

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 12 of 64 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
