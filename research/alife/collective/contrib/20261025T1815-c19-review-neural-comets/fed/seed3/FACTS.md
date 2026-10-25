# Evidence pack: neural-field-dep-fork (seed 3)

- world: `../../../20261025T1733-c20-neural-comets-metabolic-claim/world.py`, family `neural-field`
- parent: None; mutation: c20 neural-field comets plus synaptic depression: the coupling output is scaled by a resource r that firing depletes and that recovers on time tr
- run: 201 frames x 50 steps x dt 0.1 = time 1000; grid [128, 128]; wall 5s; status ok
- command: `python -m labkit.run collective/contrib/20261025T1733-c20-neural-comets-metabolic-claim/world.py --out collective/contrib/20261025T1815-c19-review-neural-comets/fed/seed3 --seeds 3 --spf 50 --no-movie`
- segmentation: matter > 0.50 of robust range [0.0, 1.0], min area 6 px

## Measurements
- components: final 36, mean 39.2, max 73; occupancy final 0.09
- tracks: 831; persistent (alive >= 50% of run): 1; longest 108 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 6.12 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [36, 36, 36], H1 [0, 0, 0]
- motion: 96 long-lived tracks moved >= 1 body length; max speed 0.595/time; max body lengths 33.7
- replication (lineage window K = 20 frames = time 100, default): splits 329, persistent splits 15 (0 more failed only because the siblings re-merged within K), max generation 3, merges 98, merge/split ratio 0.298, nucleations 9
- channel total drift (end/start - 1): [-1.0, None, -0.5781, -0.1801]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 383 at frame 106: holes 0, rim-vs-core 0.24, rim-vs-outside 0.89, heterogeneity 0.15; core [0.929, 0.579, 1.0, 0.369] rim [0.711, 0.517, 0.929, 0.405]
  - track 314 at frame 76: holes 0, rim-vs-core 0.28, rim-vs-outside 0.86, heterogeneity 0.16; core [0.891, 0.537, 1.0, 0.225] rim [0.651, 0.46, 0.885, 0.247]
  - track 563 at frame 146: holes 0, rim-vs-core 0.24, rim-vs-outside 0.85, heterogeneity 0.14; core [0.891, 0.6, 1.0, 0.181] rim [0.686, 0.513, 0.944, 0.257]
  - track 685 at frame 176: holes 0, rim-vs-core 0.24, rim-vs-outside 0.87, heterogeneity 0.15; core [0.932, 0.617, 1.0, 0.41] rim [0.718, 0.537, 0.978, 0.473]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 212 components >= 12 px at frames [34, 67, 101, 133, 166, 200]):
  - radial activity u: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.796, rim/outside 2.97 (aggregate of 212 individuals; 0/212 membrane-like individually; rim level 0.71)
  - radial adaptation a: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.838, rim/outside 1.89 (aggregate of 212 individuals; 4/212 membrane-like individually; rim level 0.526)
  - radial firing f(u): peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.863, rim/outside 29.4 (aggregate of 212 individuals; 1/212 membrane-like individually; rim level 0.822)
  - radial synaptic resource r: peak at rho=2.35 (OUTSIDE the peak band 0.5-1.5), rim/core 1.48, rim/outside 0.865 (aggregate of 212 individuals; 6/212 membrane-like individually; rim level 0.409)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #383 (t=530, R_eq 3.09): none; #314 (t=380, R_eq 3.04): none; #563 (t=730, R_eq 2.93): none; #685 (t=880, R_eq 3.57): none

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 5 of 212 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
