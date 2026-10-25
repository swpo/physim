# Evidence pack: fch-pchemoton-slowDK0.00005 (seed 13)

- world: `../world_slowDK0.00005.py`, family `fch-bilayer`
- parent: collective/contrib/20261025T0651-c02-fch-noise-sighting/world.py; mutation: add a fed precursor, a bilayer-gated Gray-Scott-like catalyst that makes amphiphile, and amphiphile decay
- run: 201 frames x 300 steps x dt 0.01 = time 600; grid [192, 192]; wall 356s; status ok
- command: `python -m labkit.run collective/contrib/wip-c27c/world_slowDK0.00005.py --out collective/contrib/wip-c27c/slowDK0.00005_s13 --seeds 13 --frames 200 --no-movie`
- segmentation: matter > 0.31 of robust range [-0.0202, 1.9889], min area 6 px

## Measurements
- components: final 3, mean 2.7, max 3; occupancy final 0.05
- tracks: 7; persistent (alive >= 50% of run): 3; longest 200 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 4.48 (1 = constant size)
- enclosures: components with a hole mean 1.79, final 2; holes at thresholds 0.2/0.35/0.5 final [1, 2, 1]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [4, 3, 2], H1 [3, 3, 1]
- motion: 0 long-lived tracks moved >= 1 body length; max speed 0/time; max body lengths 0.1
- replication (lineage window K = 20 frames = time 60, default): splits 2, persistent splits 1 (0 more failed only because the siblings re-merged within K), max generation 1, merges 1, merge/split ratio 0.5, nucleations 2
- channel total drift (end/start - 1): [-0.5453, -0.8886, -0.2528]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 0 at frame 101: holes 1, rim-vs-core 0.17, rim-vs-outside 0.50, heterogeneity 0.10; core [0.899, 0.067, 0.066] rim [0.735, 0.078, 0.036]
  - track 5 at frame 131: holes 0, rim-vs-core 0.14, rim-vs-outside 0.42, heterogeneity 0.10; core [0.857, 0.075, 0.038] rim [0.716, 0.077, 0.045]
  - track 6 at frame 131: holes 1, rim-vs-core 0.18, rim-vs-outside 0.15, heterogeneity 0.09; core [0.744, 0.068, 0.081] rim [0.576, 0.084, 0.013]
  - track 4 at frame 40: holes 7, rim-vs-core 0.05, rim-vs-outside 0.47, heterogeneity 0.10; core [0.647, 0.079, 0.028] rim [0.69, 0.078, 0.046]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 17 components >= 12 px at frames [34, 67, 101, 133, 166, 200]):
  - radial amphiphile u+1: peak at rho=0.55 (in the peak band 0.5-1.5), rim/core 1.26, rim/outside 3.02 (aggregate of 17 individuals; 6/17 membrane-like individually; rim level 0.63)
  - radial precursor P: peak at rho=0.85 (in the peak band 0.5-1.5), rim/core 1.06, rim/outside 1.03 (aggregate of 17 individuals; 0/17 membrane-like individually; rim level 0.0804)
  - radial catalyst K: peak at rho=0.55 (in the peak band 0.5-1.5), rim/core 1.24, rim/outside 1.05 (aggregate of 17 individuals; 5/17 membrane-like individually; rim level 0.0452)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #0 (t=303, R_eq 14.64, ring): ['amphiphile u+1']; #5 (t=393, R_eq 18.05, ring): none; #6 (t=393, R_eq 11.42, ring): ['catalyst K']; #4 (t=120, R_eq 24.65): none

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 14 of 17 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
