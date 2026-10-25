# Evidence pack: neural-field-dep-fork (seed 3)

- world: `../../../20261025T1733-c20-neural-comets-metabolic-claim/world.py`, family `neural-field`
- parent: None; mutation: c20 neural-field comets plus synaptic depression: the coupling output is scaled by a resource r that firing depletes and that recovers on time tr
- run: 201 frames x 50 steps x dt 0.1 = time 1000; grid [128, 128]; wall 6s; status ok
- command: `python -m labkit.run collective/contrib/20261025T1733-c20-neural-comets-metabolic-claim/world.py --out collective/contrib/20261025T1815-c19-review-neural-comets/cut_left/seed3 --seeds 3 --spf 50 --no-movie`
- segmentation: matter > 0.50 of robust range [0.0, 1.0], min area 6 px

## Measurements
- components: final 17, mean 28.9, max 73; occupancy final 0.04
- tracks: 679; persistent (alive >= 50% of run): 0; longest 88 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 0.00 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [17, 17, 16], H1 [0, 0, 0]
- motion: 65 long-lived tracks moved >= 1 body length; max speed 0.597/time; max body lengths 33.5
- replication (lineage window K = 20 frames = time 100, default): splits 265, persistent splits 10 (0 more failed only because the siblings re-merged within K), max generation 3, merges 73, merge/split ratio 0.275, nucleations 9
- channel total drift (end/start - 1): [-1.0, None, -0.8149, -0.2705]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 314 at frame 77: holes 0, rim-vs-core 0.29, rim-vs-outside 0.86, heterogeneity 0.15; core [0.937, 0.519, 1.0, 0.437] rim [0.691, 0.397, 0.923, 0.458]
  - track 327 at frame 69: holes 0, rim-vs-core 0.27, rim-vs-outside 0.87, heterogeneity 0.16; core [0.917, 0.539, 1.0, 0.478] rim [0.691, 0.455, 0.897, 0.54]
  - track 383 at frame 82: holes 0, rim-vs-core 0.22, rim-vs-outside 0.89, heterogeneity 0.12; core [0.955, 0.584, 1.0, 0.501] rim [0.747, 0.535, 0.988, 0.538]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 149 components >= 12 px at frames [34, 67, 101, 133, 166, 200]):
  - radial activity u: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.797, rim/outside 2.97 (aggregate of 149 individuals; 1/149 membrane-like individually; rim level 0.712)
  - radial adaptation a: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.872, rim/outside 1.96 (aggregate of 149 individuals; 5/149 membrane-like individually; rim level 0.548)
  - radial firing f(u): peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.854, rim/outside 28.3 (aggregate of 149 individuals; 2/149 membrane-like individually; rim level 0.812)
  - radial synaptic resource r: peak at rho=2.35 (OUTSIDE the peak band 0.5-1.5), rim/core 1.21, rim/outside 0.92 (aggregate of 149 individuals; 3/149 membrane-like individually; rim level 0.54)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #314 (t=385, R_eq 2.99): none; #327 (t=345, R_eq 2.88): none; #383 (t=410, R_eq 3.04): none; #623 (t=825, R_eq 2.11): ['synaptic resource r']

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 3 of 149 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
