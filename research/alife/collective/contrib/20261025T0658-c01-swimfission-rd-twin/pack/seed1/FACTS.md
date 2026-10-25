# Evidence pack: swimfission-rd-twin (seed 1)

- world: `../../twin_sf.py`, family `chemotaxis`
- parent: toxforage; mutation: shorter cohesion range (Da 4 -> 2): grown swimmers exceed it and divide
- run: 201 frames x 120 steps x dt 0.05 = time 1200; grid [160, 160]; wall 57s; status ok
- command: `python -m labkit.run collective/contrib/20261025T0658-c01-swimfission-rd-twin/twin_sf.py --out collective/contrib/20261025T0658-c01-swimfission-rd-twin/pack --seeds 0 1 --no-movie`
- segmentation: matter > 0.35 of robust range [0.0, 0.9999], min area 6 px

## Measurements
- components: final 5, mean 6.3, max 24; occupancy final 0.08
- tracks: 147; persistent (alive >= 50% of run): 1; longest 108 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 7.89 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [7, 6, 6], H1 [0, 0, 0]
- motion: 14 long-lived tracks moved >= 1 body length; max speed 0.627/time; max body lengths 13.2
- replication (lineage window K = 20 frames = time 120, default): splits 18, persistent splits 0 (0 more failed only because the siblings re-merged within K), max generation 0, merges 22, merge/split ratio 1.22, nucleations 91
- channel total drift (end/start - 1): [0.5452, 0.5439, 0.5682, -0.0933]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 70 at frame 103: holes 0, rim-vs-core 0.39, rim-vs-outside 0.90, heterogeneity 0.23; core [0.999, 0.92, 0.726, 0.033] rim [0.79, 0.704, 0.577, 0.235]
  - track 65 at frame 69: holes 0, rim-vs-core 0.44, rim-vs-outside 0.52, heterogeneity 0.18; core [0.949, 0.529, 0.388, 0.277] rim [0.6, 0.393, 0.289, 0.495]
  - track 131 at frame 185: holes 0, rim-vs-core 0.48, rim-vs-outside 0.54, heterogeneity 0.21; core [0.966, 0.633, 0.476, 0.192] rim [0.611, 0.456, 0.356, 0.436]
  - track 90 at frame 150: holes 0, rim-vs-core 0.41, rim-vs-outside 0.81, heterogeneity 0.23; core [0.993, 0.767, 0.584, 0.102] rim [0.739, 0.571, 0.461, 0.323]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 31 components >= 12 px at frames [34, 67, 101, 133, 166, 200]):
  - radial rho: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.699, rim/outside 8.37 (aggregate of 31 individuals; 0/31 membrane-like individually; rim level 0.578)
  - radial a: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.771, rim/outside 3.31 (aggregate of 31 individuals; 0/31 membrane-like individually; rim level 0.456)
  - radial h: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.824, rim/outside 2.82 (aggregate of 31 individuals; 1/31 membrane-like individually; rim level 0.385)
  - radial n: peak at rho=2.45 (OUTSIDE the peak band 0.5-1.5), rim/core 1.5, rim/outside 0.883 (aggregate of 31 individuals; 0/31 membrane-like individually; rim level 0.804)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #70 (t=618, R_eq 16.59): none; #65 (t=414, R_eq 6.31): none; #131 (t=1110, R_eq 8.08): none; #90 (t=900, R_eq 10.59): none

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 2 of 31 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
