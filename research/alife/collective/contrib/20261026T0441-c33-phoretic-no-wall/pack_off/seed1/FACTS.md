# Evidence pack: phoretic-colloids (seed 1)

- world: `../../world.py`, family `phoretic-colloids`
- parent: None; mutation: -
- run: 801 frames x 1 steps x dt 0.5 = time 400; grid [128, 128]; wall 115s; status ok
- command: `python -m labkit.run collective/contrib/wip-c33-nuc/world.py --out collective/contrib/wip-c33-nuc/pack_off --seeds 0 1 --frames 800 --no-movie`
- segmentation: matter > 0.35 of robust range [0.0, 2.1662], min area 6 px

## Measurements
- components: final 8, mean 10.2, max 21; occupancy final 0.04
- tracks: 102; persistent (alive >= 50% of run): 5; longest 589 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 5.83 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [13, 11, 5], H1 [0, 0, 0]
- motion: 31 long-lived tracks moved >= 1 body length; max speed 0.404/time; max body lengths 8.7
- replication (lineage window K = 20 frames = time 10, default): splits 6, persistent splits 3 (0 more failed only because the siblings re-merged within K), max generation 2, merges 20, merge/split ratio 3.33, nucleations 70
- channel total drift (end/start - 1): [0.0, 0.0, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 59 at frame 457: holes 0, rim-vs-core 0.25, rim-vs-outside 0.21, heterogeneity 0.11; core [0.787, 0.182, 0.352] rim [0.604, 0.35, 0.317]
  - track 72 at frame 511: holes 0, rim-vs-core 0.31, rim-vs-outside 0.28, heterogeneity 0.13; core [0.902, 0.118, 0.568] rim [0.618, 0.187, 0.465]
  - track 35 at frame 350: holes 0, rim-vs-core 0.15, rim-vs-outside 0.24, heterogeneity 0.12; core [0.735, 0.269, 0.386] rim [0.603, 0.314, 0.342]
  - track 95 at frame 766: holes 0, rim-vs-core 0.05, rim-vs-outside 0.16, heterogeneity 0.11; core [0.606, 0.22, 0.344] rim [0.569, 0.199, 0.315]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 59 components >= 12 px at frames [134, 269, 403, 531, 666, 800]):
  - radial A density: peak at rho=0.35 (OUTSIDE the peak band 0.5-1.5), rim/core 0.923, rim/outside 17.4 (aggregate of 59 individuals; 4/59 membrane-like individually; rim level 0.698)
  - radial B density: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.831, rim/outside 13 (aggregate of 59 individuals; 32/59 membrane-like individually; rim level 0.331)
  - radial chemicals (sum): peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.821, rim/outside 2.46 (aggregate of 59 individuals; 0/59 membrane-like individually; rim level 0.503)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #59 (t=228.5, R_eq 2.59): ['B density']; #72 (t=255.5, R_eq 4.26): ['B density']; #35 (t=175, R_eq 2.93): ['B density']; #95 (t=383, R_eq 2.39): ['B density']

## Warnings
- radial: 1 of 59 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, particles.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
