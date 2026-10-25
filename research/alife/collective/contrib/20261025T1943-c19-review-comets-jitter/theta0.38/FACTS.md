# Evidence pack: neural-field-dep-fork (seed 6)

- world: `../../20261025T1733-c20-neural-comets-metabolic-claim/world.py`, family `neural-field`
- parent: None; mutation: c20 neural-field comets plus synaptic depression: the coupling output is scaled by a resource r that firing depletes and that recovers on time tr
- run: 201 frames x 50 steps x dt 0.1 = time 1000; grid [128, 128]; wall 5s; status ok
- command: `python -m labkit.run collective/contrib/20261025T1733-c20-neural-comets-metabolic-claim/world.py --out collective/contrib/20261025T1943-c19-review-comets-jitter/theta0.38 --seeds 6 --spf 50 --no-movie`
- segmentation: matter > 0.50 of robust range [0.0, 1.0], min area 6 px

## Measurements
- components: final 54, mean 52.7, max 75; occupancy final 0.12
- tracks: 1279; persistent (alive >= 50% of run): 0; longest 71 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 0.00 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [55, 54, 54], H1 [0, 0, 0]
- motion: 130 long-lived tracks moved >= 1 body length; max speed 0.589/time; max body lengths 24.7
- replication (lineage window K = 20 frames = time 100, default): splits 524, persistent splits 26 (0 more failed only because the siblings re-merged within K), max generation 4, merges 162, merge/split ratio 0.309, nucleations 12
- channel total drift (end/start - 1): [1.0, None, -0.4432, -0.2413]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 459 at frame 79: holes 0, rim-vs-core 0.30, rim-vs-outside 0.84, heterogeneity 0.15; core [0.927, 0.476, 1.0, 0.304] rim [0.67, 0.359, 0.927, 0.383]
  - track 783 at frame 138: holes 0, rim-vs-core 0.25, rim-vs-outside 0.87, heterogeneity 0.15; core [0.899, 0.637, 1.0, 0.268] rim [0.692, 0.522, 0.955, 0.326]
  - track 380 at frame 59: holes 0, rim-vs-core 0.27, rim-vs-outside 0.80, heterogeneity 0.16; core [0.863, 0.599, 1.0, 0.192] rim [0.646, 0.526, 0.872, 0.249]
  - track 1087 at frame 176: holes 0, rim-vs-core 0.25, rim-vs-outside 0.86, heterogeneity 0.15; core [0.902, 0.538, 1.0, 0.256] rim [0.679, 0.475, 0.94, 0.308]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 302 components >= 12 px at frames [34, 67, 101, 133, 166, 200]):
  - radial activity u: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.799, rim/outside 2.99 (aggregate of 302 individuals; 1/302 membrane-like individually; rim level 0.708)
  - radial adaptation a: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.862, rim/outside 1.96 (aggregate of 302 individuals; 8/302 membrane-like individually; rim level 0.545)
  - radial firing f(u): peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.868, rim/outside 32 (aggregate of 302 individuals; 3/302 membrane-like individually; rim level 0.83)
  - radial synaptic resource r: peak at rho=2.25 (OUTSIDE the peak band 0.5-1.5), rim/core 1.53, rim/outside 0.902 (aggregate of 302 individuals; 12/302 membrane-like individually; rim level 0.377)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #459 (t=395, R_eq 3.48): none; #783 (t=690, R_eq 2.76): none; #380 (t=295, R_eq 2.93): none; #1087 (t=880, R_eq 3.29): none

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 6 of 302 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
