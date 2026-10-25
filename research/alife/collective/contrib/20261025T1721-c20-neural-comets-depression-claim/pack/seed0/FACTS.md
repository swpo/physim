# Evidence pack: neural-field-dep (seed 0)

- world: `../../world.py`, family `neural-field`
- parent: None; mutation: c20 neural-field comets plus synaptic depression: the coupling output is scaled by a resource r that firing depletes and that recovers on time tr
- run: 201 frames x 50 steps x dt 0.1 = time 1000; grid [128, 128]; wall 9s; status ok
- command: `python -m labkit.run /tmp/c20nfd/world.py --out /tmp/c20nfd/pack --seeds 0 1 2 --spf 50 --no-movie`
- segmentation: matter > 0.50 of robust range [0.0, 1.0], min area 6 px

## Measurements
- components: final 37, mean 38.0, max 69; occupancy final 0.11
- tracks: 631; persistent (alive >= 50% of run): 1; longest 102 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 5.82 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [37, 37, 37], H1 [0, 0, 0]
- motion: 127 long-lived tracks moved >= 1 body length; max speed 0.6/time; max body lengths 40.8
- replication (lineage window K = 20 frames = time 100, default): splits 249, persistent splits 29 (0 more failed only because the siblings re-merged within K), max generation 6, merges 64, merge/split ratio 0.257, nucleations 8
- channel total drift (end/start - 1): [-1.0, None, -0.5329, -0.1974]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 444 at frame 150: holes 0, rim-vs-core 0.28, rim-vs-outside 0.86, heterogeneity 0.17; core [0.888, 0.513, 1.0, 0.268] rim [0.664, 0.411, 0.885, 0.318]
  - track 253 at frame 59: holes 0, rim-vs-core 0.28, rim-vs-outside 0.88, heterogeneity 0.17; core [0.917, 0.501, 1.0, 0.358] rim [0.668, 0.45, 0.894, 0.394]
  - track 433 at frame 133: holes 0, rim-vs-core 0.30, rim-vs-outside 0.96, heterogeneity 0.18; core [0.943, 0.597, 1.0, 0.463] rim [0.748, 0.413, 0.937, 0.57]
  - track 546 at frame 173: holes 0, rim-vs-core 0.28, rim-vs-outside 0.90, heterogeneity 0.16; core [0.9, 0.466, 1.0, 0.215] rim [0.651, 0.43, 0.89, 0.25]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 213 components >= 12 px at frames [34, 67, 101, 133, 166, 200]):
  - radial activity u: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.788, rim/outside 2.92 (aggregate of 213 individuals; 0/213 membrane-like individually; rim level 0.697)
  - radial adaptation a: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.903, rim/outside 1.96 (aggregate of 213 individuals; 8/213 membrane-like individually; rim level 0.549)
  - radial firing f(u): peak at rho=0.25 (OUTSIDE the peak band 0.5-1.5), rim/core 0.841, rim/outside 25 (aggregate of 213 individuals; 2/213 membrane-like individually; rim level 0.792)
  - radial synaptic resource r: peak at rho=2.35 (OUTSIDE the peak band 0.5-1.5), rim/core 1.44, rim/outside 0.881 (aggregate of 213 individuals; 12/213 membrane-like individually; rim level 0.409)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #444 (t=750, R_eq 3.91): none; #253 (t=295, R_eq 4.07): none; #433 (t=665, R_eq 3.95): none; #546 (t=865, R_eq 3.43): none

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 5 of 213 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
