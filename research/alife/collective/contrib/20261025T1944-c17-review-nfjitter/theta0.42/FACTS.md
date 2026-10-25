# Evidence pack: neural-field-dep (seed 7)

- world: `../world.py`, family `neural-field`
- parent: None; mutation: c20 neural-field comets plus synaptic depression: the coupling output is scaled by a resource r that firing depletes and that recovers on time tr
- run: 201 frames x 30 steps x dt 0.1 = time 600; grid [128, 128]; wall 3s; status ok
- command: `python -m labkit.run world.py --out theta0.42 --seeds 7 --no-movie`
- segmentation: matter > 0.50 of robust range [0.0, 1.0], min area 6 px

## Measurements
- components: final 19, mean 26.1, max 64; occupancy final 0.06
- tracks: 321; persistent (alive >= 50% of run): 1; longest 174 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 5.12 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [20, 19, 19], H1 [0, 0, 0]
- motion: 99 long-lived tracks moved >= 1 body length; max speed 0.611/time; max body lengths 36.4
- replication (lineage window K = 20 frames = time 60, default): splits 116, persistent splits 24 (0 more failed only because the siblings re-merged within K), max generation 5, merges 31, merge/split ratio 0.267, nucleations 2
- channel total drift (end/start - 1): [1.0, None, -0.6784, -0.1152]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 173 at frame 114: holes 0, rim-vs-core 0.26, rim-vs-outside 0.89, heterogeneity 0.17; core [0.927, 0.481, 1.0, 0.395] rim [0.689, 0.45, 0.918, 0.449]
  - track 169 at frame 74: holes 0, rim-vs-core 0.24, rim-vs-outside 0.86, heterogeneity 0.18; core [0.957, 0.529, 1.0, 0.435] rim [0.736, 0.473, 0.943, 0.5]
  - track 166 at frame 71: holes 0, rim-vs-core 0.25, rim-vs-outside 0.89, heterogeneity 0.17; core [0.927, 0.555, 1.0, 0.336] rim [0.697, 0.493, 0.934, 0.398]
  - track 270 at frame 163: holes 0, rim-vs-core 0.25, rim-vs-outside 0.87, heterogeneity 0.18; core [0.909, 0.525, 1.0, 0.445] rim [0.683, 0.477, 0.902, 0.466]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 157 components >= 12 px at frames [34, 67, 101, 133, 166, 200]):
  - radial activity u: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.791, rim/outside 3.05 (aggregate of 157 individuals; 0/157 membrane-like individually; rim level 0.721)
  - radial adaptation a: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.87, rim/outside 1.95 (aggregate of 157 individuals; 6/157 membrane-like individually; rim level 0.53)
  - radial firing f(u): peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.86, rim/outside 28.1 (aggregate of 157 individuals; 0/157 membrane-like individually; rim level 0.821)
  - radial synaptic resource r: peak at rho=2.35 (OUTSIDE the peak band 0.5-1.5), rim/core 1.44, rim/outside 0.873 (aggregate of 157 individuals; 8/157 membrane-like individually; rim level 0.449)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #173 (t=342, R_eq 4.18): none; #169 (t=222, R_eq 3.66): none; #166 (t=213, R_eq 3.43): none; #270 (t=489, R_eq 4.79): none

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 1 of 157 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
