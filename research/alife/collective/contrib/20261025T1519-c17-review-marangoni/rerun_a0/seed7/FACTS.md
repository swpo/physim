# Evidence pack: marangoni-droplets (seed 7)

- world: `../../world.py`, family `phase-field`
- parent: threads/active-droplets/worlds/ad1-fuel; mutation: self-generated Brinkman flow from a fuel-dependent interfacial stress advects droplets and fuel
- run: 201 frames x 200 steps x dt 0.5 = time 20000; grid [128, 128]; wall 271s; status ok
- command: `python -m labkit.run collective/contrib/c17-marangoni-wip/world.py --out collective/contrib/c17-marangoni-wip/rerun_a0/seed7 --seeds 7 --no-movie`
- segmentation: matter > 0.45 of robust range [-1.0485, 1.3056], min area 6 px

## Measurements
- components: final 4, mean 3.6, max 4; occupancy final 0.09
- tracks: 6; persistent (alive >= 50% of run): 4; longest 161 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 1.49 (1 = constant size)
- enclosures: components with a hole mean 0.07, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [8, 4, 4], H1 [0, 0, 0]
- motion: 0 long-lived tracks moved >= 1 body length; max speed 0/time; max body lengths 1.0
- replication (lineage window K = 20 frames = time 2000, default): splits 2, persistent splits 2 (0 more failed only because the siblings re-merged within K), max generation 1, merges 0, merge/split ratio 0, nucleations 0
- channel total drift (end/start - 1): [0.0922, -0.4705, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 2 at frame 121: holes 0, rim-vs-core 0.41, rim-vs-outside 0.63, heterogeneity 0.14; core [0.93, 0.017, 0.796] rim [0.758, 0.091, 0.436]
  - track 3 at frame 121: holes 0, rim-vs-core 0.37, rim-vs-outside 0.62, heterogeneity 0.14; core [0.924, 0.016, 0.789] rim [0.77, 0.089, 0.458]
  - track 4 at frame 121: holes 0, rim-vs-core 0.37, rim-vs-outside 0.62, heterogeneity 0.14; core [0.924, 0.016, 0.79] rim [0.771, 0.089, 0.458]
  - track 5 at frame 121: holes 0, rim-vs-core 0.41, rim-vs-outside 0.63, heterogeneity 0.15; core [0.93, 0.017, 0.796] rim [0.758, 0.091, 0.436]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 22 components >= 12 px at frames [34, 67, 101, 133, 166, 200]):
  - radial phi (droplet material): peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.781, rim/outside 15.1 (aggregate of 22 individuals; 0/22 membrane-like individually; rim level 0.53)
  - radial u (fuel): peak at rho=2.45 (OUTSIDE the peak band 0.5-1.5), rim/core 5.95, rim/outside 0.574 (aggregate of 22 individuals; 0/22 membrane-like individually; rim level 0.237)
  - radial |v| (flow speed): peak at rho=0.35 (OUTSIDE the peak band 0.5-1.5), rim/core 0.995, rim/outside 5.08 (aggregate of 22 individuals; 2/22 membrane-like individually; rim level 0.569)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #2 (t=12100, R_eq 10.85): none; #3 (t=12100, R_eq 10.59): none; #4 (t=12100, R_eq 10.59): none; #5 (t=12100, R_eq 10.85): none

## Warnings
- none

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
