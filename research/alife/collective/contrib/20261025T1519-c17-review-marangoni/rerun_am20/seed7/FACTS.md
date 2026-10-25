# Evidence pack: marangoni-droplets (seed 7)

- world: `../../world.py`, family `phase-field`
- parent: threads/active-droplets/worlds/ad1-fuel; mutation: self-generated Brinkman flow from a fuel-dependent interfacial stress advects droplets and fuel
- run: 201 frames x 200 steps x dt 0.5 = time 20000; grid [128, 128]; wall 278s; status ok
- command: `python -m labkit.run collective/contrib/c17-marangoni-wip/world.py --out collective/contrib/c17-marangoni-wip/rerun_am20/seed7 --seeds 7 --no-movie`
- segmentation: matter > 0.49 of robust range [-1.0486, 1.1121], min area 6 px

## Measurements
- components: final 4, mean 1.1, max 4; occupancy final 0.07
- tracks: 8; persistent (alive >= 50% of run): 1; longest 189 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 3.00 (1 = constant size)
- enclosures: components with a hole mean 0.93, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [4, 4, 4], H1 [1, 0, 0]
- motion: 0 long-lived tracks moved >= 1 body length; max speed 0/time; max body lengths 0.3
- replication (lineage window K = 20 frames = time 2000, default): splits 2, persistent splits 0 (0 more failed only because the siblings re-merged within K), max generation 0, merges 1, merge/split ratio 0.5, nucleations 0
- channel total drift (end/start - 1): [0.051, -0.3625, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 3 at frame 197: holes 0, rim-vs-core 0.20, rim-vs-outside 0.51, heterogeneity 0.08; core [0.915, 0.015, 0.171] rim [0.748, 0.109, 0.132]
  - track 4 at frame 197: holes 0, rim-vs-core 0.36, rim-vs-outside 0.53, heterogeneity 0.17; core [0.913, 0.016, 0.603] rim [0.744, 0.111, 0.299]
  - track 6 at frame 198: holes 0, rim-vs-core 0.19, rim-vs-outside 0.51, heterogeneity 0.08; core [0.914, 0.014, 0.181] rim [0.75, 0.106, 0.141]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 9 components >= 12 px at frames [34, 67, 101, 133, 166, 200]):
  - radial phi (droplet material): peak at rho=0.75 (in the peak band 0.5-1.5), rim/core 1.1, rim/outside 4.88 (aggregate of 9 individuals; 3/9 membrane-like individually; rim level 0.428)
  - radial u (fuel): peak at rho=2.45 (OUTSIDE the peak band 0.5-1.5), rim/core 1.09, rim/outside 0.439 (aggregate of 9 individuals; 0/9 membrane-like individually; rim level 0.155)
  - radial |v| (flow speed): peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.869, rim/outside 2.88 (aggregate of 9 individuals; 3/9 membrane-like individually; rim level 0.124)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #2 (t=9700, R_eq 19.29, ring): ['phi (droplet material)', '|v| (flow speed)']; #3 (t=19700, R_eq 9.67): none; #4 (t=19700, R_eq 9.71): none; #6 (t=19800, R_eq 9.62): none

## Warnings
- radial: 5 of 9 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
