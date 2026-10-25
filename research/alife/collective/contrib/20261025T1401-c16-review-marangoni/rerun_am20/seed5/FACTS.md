# Evidence pack: marangoni-droplets (seed 5)

- world: `../../../20261025T0946-c01-marangoni-droplets/world.py`, family `phase-field`
- parent: threads/active-droplets/worlds/ad1-fuel; mutation: self-generated Brinkman flow from a fuel-dependent interfacial stress advects droplets and fuel
- run: 201 frames x 200 steps x dt 0.5 = time 20000; grid [128, 128]; wall 354s; status ok
- command: `python -m labkit.run collective/contrib/20261025T0946-c01-marangoni-droplets/world.py --out collective/contrib/20261025T1401-c16-review-marangoni/rerun_am20/seed5 --seeds 5 --no-movie`
- segmentation: matter > 0.45 of robust range [-1.0482, 1.2637], min area 6 px

## Measurements
- components: final 6, mean 4.1, max 6; occupancy final 0.10
- tracks: 10; persistent (alive >= 50% of run): 6; longest 111 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 1.26 (1 = constant size)
- enclosures: components with a hole mean 0.48, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [12, 6, 6], H1 [1, 0, 0]
- motion: 0 long-lived tracks moved >= 1 body length; max speed 0/time; max body lengths 0.9
- replication (lineage window K = 20 frames = time 2000, default): splits 4, persistent splits 4 (0 more failed only because the siblings re-merged within K), max generation 2, merges 0, merge/split ratio 0, nucleations 0
- channel total drift (end/start - 1): [0.1027, -0.494, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 2 at frame 146: holes 0, rim-vs-core 0.14, rim-vs-outside 0.58, heterogeneity 0.13; core [0.912, 0.033, 0.356] rim [0.779, 0.082, 0.374]
  - track 5 at frame 146: holes 0, rim-vs-core 0.20, rim-vs-outside 0.56, heterogeneity 0.13; core [0.919, 0.034, 0.435] rim [0.767, 0.083, 0.32]
  - track 6 at frame 148: holes 1, rim-vs-core 0.19, rim-vs-outside 0.55, heterogeneity 0.11; core [0.933, 0.032, 0.236] rim [0.758, 0.09, 0.267]
  - track 7 at frame 148: holes 1, rim-vs-core 0.21, rim-vs-outside 0.52, heterogeneity 0.08; core [0.936, 0.038, 0.128] rim [0.737, 0.089, 0.144]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 28 components >= 12 px at frames [34, 67, 101, 133, 166, 200]):
  - radial phi (droplet material): peak at rho=0.55 (in the peak band 0.5-1.5), rim/core 1.18, rim/outside 26 (aggregate of 28 individuals; 6/28 membrane-like individually; rim level 0.8)
  - radial u (fuel): peak at rho=2.45 (OUTSIDE the peak band 0.5-1.5), rim/core 8.23, rim/outside 0.622 (aggregate of 28 individuals; 0/28 membrane-like individually; rim level 0.232)
  - radial |v| (flow speed): peak at rho=0.35 (OUTSIDE the peak band 0.5-1.5), rim/core 0.914, rim/outside 4.09 (aggregate of 28 individuals; 2/28 membrane-like individually; rim level 0.405)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #2 (t=14600, R_eq 9.04): none; #5 (t=14600, R_eq 9.04): none; #6 (t=14800, R_eq 9.13): none; #7 (t=14800, R_eq 8.94, ring): ['phi (droplet material)']

## Warnings
- radial: 4 of 28 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
