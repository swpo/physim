# Evidence pack: neural-field-dep (seed 11)

- world: `../../../20261025T1721-c20-neural-comets-depression-claim/world.py`, family `neural-field`
- parent: None; mutation: c20 neural-field comets plus synaptic depression: the coupling output is scaled by a resource r that firing depletes and that recovers on time tr
- run: 201 frames x 30 steps x dt 0.1 = time 600; grid [128, 128]; wall 4s; status ok
- command: `python -m labkit.run collective/contrib/20261025T1721-c20-neural-comets-depression-claim/world.py --out collective/contrib/20261025T1757-c21-review-comets-depression/rerun --seeds 11 12 --no-movie`
- segmentation: matter > 0.50 of robust range [0.0, 1.0], min area 6 px

## Measurements
- components: final 26, mean 40.4, max 71; occupancy final 0.08
- tracks: 599; persistent (alive >= 50% of run): 2; longest 136 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 7.23 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [26, 26, 26], H1 [0, 0, 0]
- motion: 126 long-lived tracks moved >= 1 body length; max speed 0.604/time; max body lengths 26.9
- replication (lineage window K = 20 frames = time 60, default): splits 226, persistent splits 42 (0 more failed only because the siblings re-merged within K), max generation 9, merges 82, merge/split ratio 0.363, nucleations 3
- channel total drift (end/start - 1): [-1.0, None, -0.6294, -0.1674]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 353 at frame 133: holes 0, rim-vs-core 0.23, rim-vs-outside 0.89, heterogeneity 0.17; core [0.9, 0.501, 1.0, 0.456] rim [0.692, 0.457, 0.929, 0.501]
  - track 123 at frame 62: holes 0, rim-vs-core 0.23, rim-vs-outside 0.87, heterogeneity 0.16; core [0.896, 0.552, 1.0, 0.407] rim [0.691, 0.502, 0.936, 0.464]
  - track 347 at frame 109: holes 0, rim-vs-core 0.22, rim-vs-outside 0.88, heterogeneity 0.16; core [0.892, 0.525, 1.0, 0.296] rim [0.687, 0.462, 0.95, 0.334]
  - track 526 at frame 178: holes 0, rim-vs-core 0.27, rim-vs-outside 0.87, heterogeneity 0.17; core [0.91, 0.539, 1.0, 0.215] rim [0.674, 0.434, 0.915, 0.244]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 218 components >= 12 px at frames [34, 67, 101, 133, 166, 200]):
  - radial activity u: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.788, rim/outside 2.9 (aggregate of 218 individuals; 0/218 membrane-like individually; rim level 0.696)
  - radial adaptation a: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.878, rim/outside 1.95 (aggregate of 218 individuals; 5/218 membrane-like individually; rim level 0.554)
  - radial firing f(u): peak at rho=0.25 (OUTSIDE the peak band 0.5-1.5), rim/core 0.86, rim/outside 28.4 (aggregate of 218 individuals; 2/218 membrane-like individually; rim level 0.814)
  - radial synaptic resource r: peak at rho=2.45 (OUTSIDE the peak band 0.5-1.5), rim/core 1.57, rim/outside 0.89 (aggregate of 218 individuals; 11/218 membrane-like individually; rim level 0.414)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #353 (t=399, R_eq 5.23): none; #123 (t=186, R_eq 3.99): none; #347 (t=327, R_eq 3.57): none; #526 (t=534, R_eq 3.19): none

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 6 of 218 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
