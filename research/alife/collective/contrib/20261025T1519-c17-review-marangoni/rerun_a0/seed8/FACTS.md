# Evidence pack: marangoni-droplets (seed 8)

- world: `../../world.py`, family `phase-field`
- parent: threads/active-droplets/worlds/ad1-fuel; mutation: self-generated Brinkman flow from a fuel-dependent interfacial stress advects droplets and fuel
- run: 201 frames x 200 steps x dt 0.5 = time 20000; grid [128, 128]; wall 277s; status ok
- command: `python -m labkit.run collective/contrib/c17-marangoni-wip/world.py --out collective/contrib/c17-marangoni-wip/rerun_a0/seed8 --seeds 8 --no-movie`
- segmentation: matter > 0.44 of robust range [-1.0536, 1.3161], min area 6 px

## Measurements
- components: final 2, mean 2.0, max 2; occupancy final 0.09
- tracks: 2; persistent (alive >= 50% of run): 2; longest 201 frames; alive start-to-end: 2
- size of persistent tracks: max/min area ratio 7.05 (1 = constant size)
- enclosures: components with a hole mean 0.06, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [4, 2, 2], H1 [0, 0, 0]
- motion: 0 long-lived tracks moved >= 1 body length; max speed 0/time; max body lengths 0.5
- replication (lineage window K = 20 frames = time 2000, default): splits 0, persistent splits 0 (0 more failed only because the siblings re-merged within K), max generation 0, merges 0, merge/split ratio n/a, nucleations 0
- channel total drift (end/start - 1): [0.0872, -0.4822, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 0 at frame 101: holes 0, rim-vs-core 0.58, rim-vs-outside 0.72, heterogeneity 0.17; core [0.923, 0.003, 0.931] rim [0.811, 0.066, 0.361]
  - track 1 at frame 101: holes 0, rim-vs-core 0.59, rim-vs-outside 0.71, heterogeneity 0.17; core [0.938, 0.004, 0.908] rim [0.801, 0.07, 0.335]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 12 components >= 12 px at frames [34, 67, 101, 133, 166, 200]):
  - radial phi (droplet material): peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.408, rim/outside 2.14 (aggregate of 12 individuals; 0/12 membrane-like individually; rim level 0.233)
  - radial u (fuel): peak at rho=2.45 (OUTSIDE the peak band 0.5-1.5), rim/core 3.49, rim/outside 0.771 (aggregate of 12 individuals; 0/12 membrane-like individually; rim level 0.306)
  - radial |v| (flow speed): peak at rho=2.05 (OUTSIDE the peak band 0.5-1.5), rim/core 1.15, rim/outside 0.94 (aggregate of 12 individuals; 0/12 membrane-like individually; rim level 0.139)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #0 (t=10100, R_eq 14.88): none; #1 (t=10100, R_eq 14.92): none

## Warnings
- radial: 2 of 12 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
