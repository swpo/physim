# Evidence pack: fch-pchemoton-slowDK0.00005 (seed 9)

- world: `../../20261025T2100-c27-review-fch-chemoton/world_slowDK0.00005.py`, family `fch-bilayer`
- parent: collective/contrib/20261025T0651-c02-fch-noise-sighting/world.py; mutation: add a fed precursor, a bilayer-gated Gray-Scott-like catalyst that makes amphiphile, and amphiphile decay
- run: 201 frames x 300 steps x dt 0.01 = time 600; grid [192, 192]; wall 457s; status ok
- command: `python -m labkit.run collective/contrib/20261025T2100-c27-review-fch-chemoton/world_slowDK0.00005.py --out collective/contrib/20261025T2156-c21-review-fch-gate/slowDK0.00005 --seeds 9 --no-movie`
- segmentation: matter > 0.32 of robust range [-0.02, 1.93], min area 6 px

## Measurements
- components: final 3, mean 3.0, max 3; occupancy final 0.05
- tracks: 3; persistent (alive >= 50% of run): 3; longest 200 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 3.60 (1 = constant size)
- enclosures: components with a hole mean 2.76, final 3; holes at thresholds 0.2/0.35/0.5 final [3, 3, 3]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [5, 3, 3], H1 [3, 3, 3]
- motion: 0 long-lived tracks moved >= 1 body length; max speed 0/time; max body lengths 0.3
- replication (lineage window K = 20 frames = time 60, default): splits 0, persistent splits 0 (0 more failed only because the siblings re-merged within K), max generation 0, merges 0, merge/split ratio n/a, nucleations 3
- channel total drift (end/start - 1): [-0.5447, -0.8885, -0.2508]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 0 at frame 101: holes 1, rim-vs-core 0.14, rim-vs-outside 0.49, heterogeneity 0.10; core [0.854, 0.077, 0.07] rim [0.72, 0.084, 0.029]
  - track 1 at frame 101: holes 1, rim-vs-core 0.15, rim-vs-outside 0.46, heterogeneity 0.10; core [0.845, 0.077, 0.057] rim [0.701, 0.086, 0.036]
  - track 2 at frame 101: holes 1, rim-vs-core 0.19, rim-vs-outside 0.46, heterogeneity 0.10; core [0.887, 0.086, 0.007] rim [0.706, 0.074, 0.05]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 18 components >= 12 px at frames [34, 67, 101, 133, 166, 200]):
  - radial amphiphile u+1: peak at rho=0.75 (in the peak band 0.5-1.5), rim/core 2.34, rim/outside 21.7 (aggregate of 18 individuals; 15/18 membrane-like individually; rim level 0.691)  MEMBRANE-LIKE
  - radial precursor P: peak at rho=0.25 (OUTSIDE the peak band 0.5-1.5), rim/core 0.978, rim/outside 1.01 (aggregate of 18 individuals; 0/18 membrane-like individually; rim level 0.0795)
  - radial catalyst K: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 1.14, rim/outside 1.14 (aggregate of 18 individuals; 4/18 membrane-like individually; rim level 0.0471)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): amphiphile u+1
- membrane-like channels per top track at mid-life: #0 (t=303, R_eq 14.19, ring): ['amphiphile u+1']; #1 (t=303, R_eq 14.56, ring): ['amphiphile u+1']; #2 (t=303, R_eq 14.73, ring): none

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 16 of 18 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
