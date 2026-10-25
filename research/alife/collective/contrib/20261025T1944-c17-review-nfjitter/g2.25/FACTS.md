# Evidence pack: neural-field-dep (seed 7)

- world: `../world.py`, family `neural-field`
- parent: None; mutation: c20 neural-field comets plus synaptic depression: the coupling output is scaled by a resource r that firing depletes and that recovers on time tr
- run: 201 frames x 30 steps x dt 0.1 = time 600; grid [128, 128]; wall 3s; status ok
- command: `python -m labkit.run world.py --out g2.25 --seeds 7 --no-movie`
- segmentation: matter > 0.50 of robust range [0.0, 1.0], min area 6 px

## Measurements
- components: final 41, mean 43.1, max 73; occupancy final 0.11
- tracks: 619; persistent (alive >= 50% of run): 1; longest 102 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 3.54 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [41, 41, 41], H1 [0, 0, 0]
- motion: 151 long-lived tracks moved >= 1 body length; max speed 0.633/time; max body lengths 20.5
- replication (lineage window K = 20 frames = time 60, default): splits 243, persistent splits 23 (0 more failed only because the siblings re-merged within K), max generation 5, merges 73, merge/split ratio 0.3, nucleations 6
- channel total drift (end/start - 1): [1.0, None, -0.444, -0.1924]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 210 at frame 69: holes 0, rim-vs-core 0.27, rim-vs-outside 0.88, heterogeneity 0.17; core [0.896, 0.554, 1.0, 0.268] rim [0.655, 0.5, 0.91, 0.305]
  - track 456 at frame 158: holes 0, rim-vs-core 0.20, rim-vs-outside 0.86, heterogeneity 0.15; core [0.866, 0.542, 1.0, 0.413] rim [0.683, 0.498, 0.95, 0.438]
  - track 20 at frame 42: holes 0, rim-vs-core 0.29, rim-vs-outside 0.86, heterogeneity 0.16; core [0.923, 0.593, 1.0, 0.35] rim [0.67, 0.491, 0.91, 0.353]
  - track 590 at frame 190: holes 0, rim-vs-core 0.26, rim-vs-outside 0.85, heterogeneity 0.16; core [0.89, 0.522, 1.0, 0.343] rim [0.657, 0.458, 0.896, 0.344]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 253 components >= 12 px at frames [34, 67, 101, 133, 166, 200]):
  - radial activity u: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.792, rim/outside 3.06 (aggregate of 253 individuals; 0/253 membrane-like individually; rim level 0.703)
  - radial adaptation a: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.895, rim/outside 1.97 (aggregate of 253 individuals; 10/253 membrane-like individually; rim level 0.558)
  - radial firing f(u): peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.862, rim/outside 31.8 (aggregate of 253 individuals; 3/253 membrane-like individually; rim level 0.822)
  - radial synaptic resource r: peak at rho=2.35 (OUTSIDE the peak band 0.5-1.5), rim/core 1.5, rim/outside 0.863 (aggregate of 253 individuals; 14/253 membrane-like individually; rim level 0.404)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #210 (t=207, R_eq 3.24): none; #456 (t=474, R_eq 4.03): none; #20 (t=126, R_eq 3.09): none; #590 (t=570, R_eq 4.33): none

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 7 of 253 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
