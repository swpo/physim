# Evidence pack: fch-pchemoton-slowDK0.005 (seed 9)

- world: `../../20261025T2100-c27-review-fch-chemoton/world_slowDK0.005.py`, family `fch-bilayer`
- parent: collective/contrib/20261025T0651-c02-fch-noise-sighting/world.py; mutation: add a fed precursor, a bilayer-gated Gray-Scott-like catalyst that makes amphiphile, and amphiphile decay
- run: 201 frames x 300 steps x dt 0.01 = time 600; grid [192, 192]; wall 446s; status ok
- command: `python -m labkit.run collective/contrib/20261025T2100-c27-review-fch-chemoton/world_slowDK0.005.py --out collective/contrib/20261025T2156-c21-review-fch-gate/slowDK0.005 --seeds 9 --no-movie`
- segmentation: matter > 0.31 of robust range [-0.0253, 1.9615], min area 6 px

## Measurements
- components: final 3, mean 3.2, max 7; occupancy final 0.01
- tracks: 28; persistent (alive >= 50% of run): 3; longest 134 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 4.11 (1 = constant size)
- enclosures: components with a hole mean 1.49, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [6, 6, 3], H1 [0, 0, 0]
- motion: 0 long-lived tracks moved >= 1 body length; max speed 0/time; max body lengths 0.1
- replication (lineage window K = 20 frames = time 60, default): splits 8, persistent splits 0 (0 more failed only because the siblings re-merged within K), max generation 0, merges 9, merge/split ratio 1.12, nucleations 3
- channel total drift (end/start - 1): [-0.9904, 1.0, -1.0]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 25 at frame 134: holes 0, rim-vs-core 0.18, rim-vs-outside 0.28, heterogeneity 0.06; core [0.785, 1.0, 0.0] rim [0.603, 1.0, 0.0]
  - track 26 at frame 136: holes 0, rim-vs-core 0.17, rim-vs-outside 0.28, heterogeneity 0.06; core [0.784, 1.0, 0.0] rim [0.61, 1.0, 0.0]
  - track 27 at frame 139: holes 0, rim-vs-core 0.18, rim-vs-outside 0.28, heterogeneity 0.06; core [0.785, 1.0, 0.0] rim [0.606, 1.0, 0.0]
  - track 2 at frame 27: holes 6, rim-vs-core 0.04, rim-vs-outside 0.47, heterogeneity 0.04; core [0.729, 0.763, 0.029] rim [0.685, 0.764, 0.027]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 20 components >= 12 px at frames [34, 67, 101, 133, 166, 200]):
  - radial amphiphile u+1: peak at rho=0.65 (in the peak band 0.5-1.5), rim/core 1.07, rim/outside 7.24 (aggregate of 20 individuals; 3/20 membrane-like individually; rim level 0.662)
  - radial precursor P: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 1, rim/outside 1 (aggregate of 20 individuals; 0/20 membrane-like individually; rim level 0.984)
  - radial catalyst K: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.999, rim/outside 1 (aggregate of 20 individuals; 0/20 membrane-like individually; rim level 0.0006)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #25 (t=402, R_eq 9.46): none; #26 (t=408, R_eq 9.39): none; #27 (t=417, R_eq 9.36): none; #2 (t=81, R_eq 24.53): none

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 5 of 20 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
