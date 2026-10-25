# Evidence pack: neural-field-dep (seed 7)

- world: `../world.py`, family `neural-field`
- parent: None; mutation: c20 neural-field comets plus synaptic depression: the coupling output is scaled by a resource r that firing depletes and that recovers on time tr
- run: 201 frames x 30 steps x dt 0.1 = time 600; grid [128, 128]; wall 3s; status ok
- command: `python -m labkit.run world.py --out base --seeds 7 --no-movie`
- segmentation: matter > 0.50 of robust range [0.0, 1.0], min area 6 px

## Measurements
- components: final 34, mean 42.1, max 69; occupancy final 0.10
- tracks: 617; persistent (alive >= 50% of run): 3; longest 120 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 8.55 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [34, 34, 34], H1 [0, 0, 0]
- motion: 142 long-lived tracks moved >= 1 body length; max speed 0.61/time; max body lengths 34.7
- replication (lineage window K = 20 frames = time 60, default): splits 235, persistent splits 32 (0 more failed only because the siblings re-merged within K), max generation 5, merges 87, merge/split ratio 0.37, nucleations 6
- channel total drift (end/start - 1): [1.0, None, -0.5009, -0.1874]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 432 at frame 141: holes 0, rim-vs-core 0.28, rim-vs-outside 0.83, heterogeneity 0.17; core [0.913, 0.519, 1.0, 0.256] rim [0.669, 0.446, 0.882, 0.268]
  - track 444 at frame 143: holes 0, rim-vs-core 0.30, rim-vs-outside 0.82, heterogeneity 0.17; core [0.906, 0.537, 1.0, 0.268] rim [0.658, 0.447, 0.861, 0.319]
  - track 283 at frame 76: holes 0, rim-vs-core 0.27, rim-vs-outside 0.82, heterogeneity 0.15; core [0.884, 0.525, 1.0, 0.165] rim [0.673, 0.429, 0.906, 0.272]
  - track 528 at frame 158: holes 0, rim-vs-core 0.27, rim-vs-outside 0.83, heterogeneity 0.18; core [0.902, 0.541, 1.0, 0.356] rim [0.674, 0.446, 0.897, 0.377]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 240 components >= 12 px at frames [34, 67, 101, 133, 166, 200]):
  - radial activity u: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.802, rim/outside 3.03 (aggregate of 240 individuals; 0/240 membrane-like individually; rim level 0.725)
  - radial adaptation a: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.887, rim/outside 1.95 (aggregate of 240 individuals; 6/240 membrane-like individually; rim level 0.553)
  - radial firing f(u): peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.893, rim/outside 34.1 (aggregate of 240 individuals; 2/240 membrane-like individually; rim level 0.86)
  - radial synaptic resource r: peak at rho=2.25 (OUTSIDE the peak band 0.5-1.5), rim/core 1.52, rim/outside 0.895 (aggregate of 240 individuals; 9/240 membrane-like individually; rim level 0.41)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #432 (t=423, R_eq 2.88): ['synaptic resource r']; #444 (t=429, R_eq 2.93): none; #283 (t=228, R_eq 3.29): none; #528 (t=474, R_eq 3.99): none

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 4 of 240 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
