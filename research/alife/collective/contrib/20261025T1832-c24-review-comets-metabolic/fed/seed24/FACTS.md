# Evidence pack: neural-field-dep-fork (seed 24)

- world: `../../../20261025T1733-c20-neural-comets-metabolic-claim/world.py`, family `neural-field`
- parent: None; mutation: c20 neural-field comets plus synaptic depression: the coupling output is scaled by a resource r that firing depletes and that recovers on time tr
- run: 201 frames x 50 steps x dt 0.1 = time 1000; grid [128, 128]; wall 8s; status ok
- command: `python -m labkit.run collective/contrib/20261025T1733-c20-neural-comets-metabolic-claim/world.py --out collective/contrib/20261025T1832-c24-review-comets-metabolic/fed/seed24 --seeds 24 --spf 50 --no-movie`
- segmentation: matter > 0.50 of robust range [0.0, 1.0], min area 6 px

## Measurements
- components: final 31, mean 38.6, max 70; occupancy final 0.09
- tracks: 681; persistent (alive >= 50% of run): 1; longest 141 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 4.71 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [31, 31, 31], H1 [0, 0, 0]
- motion: 124 long-lived tracks moved >= 1 body length; max speed 0.607/time; max body lengths 62.1
- replication (lineage window K = 20 frames = time 100, default): splits 274, persistent splits 17 (0 more failed only because the siblings re-merged within K), max generation 3, merges 63, merge/split ratio 0.23, nucleations 12
- channel total drift (end/start - 1): [-1.0, None, -0.5865, -0.1755]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 374 at frame 131: holes 0, rim-vs-core 0.25, rim-vs-outside 0.88, heterogeneity 0.17; core [0.915, 0.464, 1.0, 0.282] rim [0.688, 0.422, 0.929, 0.344]
  - track 231 at frame 62: holes 0, rim-vs-core 0.27, rim-vs-outside 0.90, heterogeneity 0.14; core [0.923, 0.629, 1.0, 0.356] rim [0.702, 0.513, 0.965, 0.453]
  - track 353 at frame 92: holes 0, rim-vs-core 0.25, rim-vs-outside 0.86, heterogeneity 0.16; core [0.868, 0.496, 1.0, 0.318] rim [0.663, 0.428, 0.9, 0.381]
  - track 634 at frame 180: holes 0, rim-vs-core 0.24, rim-vs-outside 0.84, heterogeneity 0.16; core [0.93, 0.57, 1.0, 0.434] rim [0.71, 0.515, 0.945, 0.468]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 216 components >= 12 px at frames [34, 67, 101, 133, 166, 200]):
  - radial activity u: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.798, rim/outside 2.93 (aggregate of 216 individuals; 0/216 membrane-like individually; rim level 0.707)
  - radial adaptation a: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.883, rim/outside 1.97 (aggregate of 216 individuals; 6/216 membrane-like individually; rim level 0.543)
  - radial firing f(u): peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.851, rim/outside 25.4 (aggregate of 216 individuals; 3/216 membrane-like individually; rim level 0.808)
  - radial synaptic resource r: peak at rho=2.35 (OUTSIDE the peak band 0.5-1.5), rim/core 1.42, rim/outside 0.868 (aggregate of 216 individuals; 14/216 membrane-like individually; rim level 0.407)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #374 (t=655, R_eq 3.43): none; #231 (t=310, R_eq 2.93): none; #353 (t=460, R_eq 4.03): none; #634 (t=900, R_eq 3.83): none

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 4 of 216 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
