# Evidence pack: pps (seed 5)

- world: `../../../20261026T0215-c29-pps-lineage/world.py`, family `particle`
- parent: None; mutation: new class: Schmickl's Primordial Particle System, published parameters
- run: 201 frames x 150 steps x dt 1.0 = time 30000; grid [125, 125]; wall 109s; status ok
- command: `python -m labkit.run collective/contrib/20261026T0215-c29-pps-lineage/world.py --out collective/contrib/20261026T0230-c30-review-pps-lineage/rerun/seed5 --seeds 5 --no-movie`
- segmentation: matter > 0.04 of robust range [0.0, 9.375], min area 6 px

## Measurements
- components: final 55, mean 34.0, max 78; occupancy final 0.19
- tracks: 2130; persistent (alive >= 50% of run): 1; longest 111 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 1.93 (1 = constant size)
- enclosures: components with a hole mean 0.28, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [85, 72, 62], H1 [1, 0, 0]
- motion: 9 long-lived tracks moved >= 1 body length; max speed 0.00209/time; max body lengths 1.5
- replication (lineage window K = 20 frames = time 3000, default): splits 762, persistent splits 1 (0 more failed only because the siblings re-merged within K), max generation 1, merges 721, merge/split ratio 0.946, nucleations 1
- channel total drift (end/start - 1): [0.0, None, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 661 at frame 131: holes 0, rim-vs-core 0.33, rim-vs-outside 0.01, heterogeneity 0.22; core [0.252, 0.048, 0.23] rim [0.008, 0.0, 0.009]
  - track 614 at frame 121: holes 0, rim-vs-core 0.38, rim-vs-outside 0.03, heterogeneity 0.24; core [0.26, 0.091, 0.265] rim [0.0, 0.0, 0.0]
  - track 585 at frame 116: holes 0, rim-vs-core 0.41, rim-vs-outside 0.04, heterogeneity 0.23; core [0.272, 0.048, 0.302] rim [0.0, 0.0, 0.0]
  - track 1856 at frame 190: holes 0, rim-vs-core 0.40, rim-vs-outside 0.02, heterogeneity 0.18; core [0.27, 0.0, 0.296] rim [0.0, 0.0, 0.0]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 231 components >= 12 px at frames [34, 67, 101, 133, 166, 200]):
  - radial particles: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.476, rim/outside 2.96 (aggregate of 231 individuals; 48/231 membrane-like individually; rim level 0.116)
  - radial cell N>35: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.171, rim/outside 1.42 (aggregate of 231 individuals; 40/231 membrane-like individually; rim level 0.0063)
  - radial ring 15<N<=35: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.509, rim/outside 5.47 (aggregate of 231 individuals; 53/231 membrane-like individually; rim level 0.122)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #661 (t=19650, R_eq 3.52): ['ring 15<N<=35']; #614 (t=18150, R_eq 3.57): ['ring 15<N<=35']; #585 (t=17400, R_eq 3.52): none; #1856 (t=28500, R_eq 2.65): none

## Warnings
- radial: 3 of 231 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, particles.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
