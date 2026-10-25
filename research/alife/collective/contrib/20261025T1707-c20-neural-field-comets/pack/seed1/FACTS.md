# Evidence pack: neural-field (seed 1)

- world: `../../world.py`, family `neural-field`
- parent: None; mutation: new class: Amari neural field with an oscillatory Laing-Troy kernel and linear adaptation
- run: 201 frames x 30 steps x dt 0.1 = time 600; grid [128, 128]; wall 4s; status ok
- command: `python -m labkit.run collective/contrib/20261025T1707-c20-neural-field-comets/world.py --out collective/contrib/20261025T1707-c20-neural-field-comets/pack --seeds 0 1 --no-movie`
- segmentation: matter > 0.50 of robust range [0.0, 1.0], min area 6 px

## Measurements
- components: final 21, mean 21.9, max 68; occupancy final 0.09
- tracks: 166; persistent (alive >= 50% of run): 9; longest 174 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 7.12 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [21, 21, 21], H1 [0, 0, 0]
- motion: 64 long-lived tracks moved >= 1 body length; max speed 0.536/time; max body lengths 30.9
- replication (lineage window K = 20 frames = time 60, default): splits 41, persistent splits 13 (0 more failed only because the siblings re-merged within K), max generation 3, merges 16, merge/split ratio 0.39, nucleations 0
- channel total drift (end/start - 1): [1.0, None, -0.3818]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 76 at frame 114: holes 0, rim-vs-core 0.25, rim-vs-outside 0.90, heterogeneity 0.16; core [0.938, 0.597, 1.0] rim [0.706, 0.523, 0.937]
  - track 51 at frame 86: holes 0, rim-vs-core 0.29, rim-vs-outside 0.89, heterogeneity 0.16; core [0.936, 0.608, 1.0] rim [0.68, 0.517, 0.911]
  - track 80 at frame 124: holes 0, rim-vs-core 0.24, rim-vs-outside 0.94, heterogeneity 0.15; core [0.896, 0.585, 1.0] rim [0.688, 0.472, 0.943]
  - track 137 at frame 163: holes 0, rim-vs-core 0.16, rim-vs-outside 1.03, heterogeneity 0.14; core [0.948, 0.459, 1.0] rim [0.795, 0.447, 0.975]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 128 components >= 12 px at frames [34, 67, 101, 133, 166, 200]):
  - radial activity u: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.78, rim/outside 2.68 (aggregate of 128 individuals; 0/128 membrane-like individually; rim level 0.68)
  - radial adaptation a: peak at rho=0.25 (OUTSIDE the peak band 0.5-1.5), rim/core 0.85, rim/outside 1.85 (aggregate of 128 individuals; 4/128 membrane-like individually; rim level 0.517)
  - radial firing f(u): peak at rho=0.25 (OUTSIDE the peak band 0.5-1.5), rim/core 0.808, rim/outside 16.4 (aggregate of 128 individuals; 3/128 membrane-like individually; rim level 0.737)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #76 (t=342, R_eq 3.52): none; #51 (t=258, R_eq 2.93): none; #80 (t=372, R_eq 4.18): none; #137 (t=489, R_eq 7.09): none

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 6 of 128 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
