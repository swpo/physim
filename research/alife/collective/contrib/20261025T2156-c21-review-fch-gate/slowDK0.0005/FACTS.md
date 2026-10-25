# Evidence pack: fch-pchemoton-slowDK0.0005 (seed 9)

- world: `../../20261025T2100-c27-review-fch-chemoton/world_slowDK0.0005.py`, family `fch-bilayer`
- parent: collective/contrib/20261025T0651-c02-fch-noise-sighting/world.py; mutation: add a fed precursor, a bilayer-gated Gray-Scott-like catalyst that makes amphiphile, and amphiphile decay
- run: 201 frames x 300 steps x dt 0.01 = time 600; grid [192, 192]; wall 439s; status ok
- command: `python -m labkit.run collective/contrib/20261025T2100-c27-review-fch-chemoton/world_slowDK0.0005.py --out collective/contrib/20261025T2156-c21-review-fch-gate/slowDK0.0005 --seeds 9 --no-movie`
- segmentation: matter > 0.31 of robust range [-0.02, 1.9589], min area 6 px

## Measurements
- components: final 4, mean 3.6, max 6; occupancy final 0.12
- tracks: 16; persistent (alive >= 50% of run): 4; longest 200 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 5.51 (1 = constant size)
- enclosures: components with a hole mean 2.75, final 3; holes at thresholds 0.2/0.35/0.5 final [7, 5, 1]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [10, 8, 3], H1 [12, 7, 3]
- motion: 0 long-lived tracks moved >= 1 body length; max speed 0/time; max body lengths 0.3
- replication (lineage window K = 20 frames = time 60, default): splits 5, persistent splits 1 (0 more failed only because the siblings re-merged within K), max generation 1, merges 4, merge/split ratio 0.8, nucleations 3
- channel total drift (end/start - 1): [0.2954, -0.6995, -0.3434]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 2 at frame 101: holes 6, rim-vs-core 0.18, rim-vs-outside 0.50, heterogeneity 0.14; core [0.879, 0.17, 0.216] rim [0.738, 0.235, 0.117]
  - track 9 at frame 109: holes 5, rim-vs-core 0.15, rim-vs-outside 0.48, heterogeneity 0.16; core [0.878, 0.217, 0.206] rim [0.739, 0.221, 0.156]
  - track 14 at frame 148: holes 0, rim-vs-core 0.24, rim-vs-outside 0.45, heterogeneity 0.15; core [0.911, 0.166, 0.334] rim [0.753, 0.191, 0.154]
  - track 15 at frame 148: holes 1, rim-vs-core 0.20, rim-vs-outside 0.21, heterogeneity 0.14; core [0.821, 0.211, 0.137] rim [0.626, 0.205, 0.119]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 22 components >= 12 px at frames [34, 67, 101, 133, 166, 200]):
  - radial amphiphile u+1: peak at rho=0.55 (in the peak band 0.5-1.5), rim/core 1.21, rim/outside 5.14 (aggregate of 22 individuals; 4/22 membrane-like individually; rim level 0.679)
  - radial precursor P: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.878, rim/outside 1.01 (aggregate of 22 individuals; 1/22 membrane-like individually; rim level 0.226)
  - radial catalyst K: peak at rho=0.85 (in the peak band 0.5-1.5), rim/core 1.73, rim/outside 1.08 (aggregate of 22 individuals; 9/22 membrane-like individually; rim level 0.155)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #2 (t=303, R_eq 22.74): none; #9 (t=327, R_eq 21.03): none; #14 (t=444, R_eq 19.23, ring): ['amphiphile u+1', 'catalyst K']; #15 (t=444, R_eq 12.85, ring): ['catalyst K']

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 8 of 22 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
