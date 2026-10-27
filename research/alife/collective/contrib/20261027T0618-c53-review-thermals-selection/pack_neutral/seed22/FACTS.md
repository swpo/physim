# Evidence pack: reacting-thermals (seed 22)

- world: `../../../20261027T0222-c49-thermals-selection-claim/world.py`, family `reactive-convection`
- parent: None; mutation: -
- run: 1201 frames x 25 steps x dt 0.04 = time 1200; grid [128, 128]; wall 132s; status ok
- command: `python -m labkit.run collective/contrib/20261027T0222-c49-thermals-selection-claim/world.py --out collective/contrib/c53-rev-sel/pack_neutral --seeds 21 22 --frames 1200 --spf 25 --no-movie`
- segmentation: matter > 0.34 of robust range [0.0, 0.7305], min area 6 px

## Measurements
- components: final 23, mean 18.0, max 45; occupancy final 0.02
- tracks: 828; persistent (alive >= 50% of run): 0; longest 301 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 0.00 (1 = constant size)
- enclosures: components with a hole mean 0.02, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [36, 33, 30], H1 [0, 0, 0]
- motion: 346 long-lived tracks moved >= 1 body length; max speed 1.09/time; max body lengths 46.6
- replication (lineage window K = 20 frames = time 20, default): splits 159, persistent splits 56 (0 more failed only because the siblings re-merged within K), max generation 12, merges 16, merge/split ratio 0.101, nucleations 460
- channel total drift (end/start - 1): [-0.8684, -0.3438, None, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 132 at frame 343: holes 0, rim-vs-core 0.21, rim-vs-outside 0.49, heterogeneity 0.09; core [0.953, 0.057, 0.224, 0.936] rim [0.789, 0.074, 0.199, 0.81]
  - track 513 at frame 877: holes 0, rim-vs-core 0.19, rim-vs-outside 0.58, heterogeneity 0.08; core [1.0, 0.014, 1.0, 0.155] rim [0.832, 0.077, 0.954, 0.117]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 75 components >= 12 px at frames [202, 403, 605, 797, 998, 1200]):
  - radial heat T: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.833, rim/outside 5.57 (aggregate of 75 individuals; 0/75 membrane-like individually; rim level 0.691)
  - radial fuel Y: peak at rho=2.45 (OUTSIDE the peak band 0.5-1.5), rim/core 8.6, rim/outside 0.591 (aggregate of 75 individuals; 0/75 membrane-like individually; rim level 0.193)
  - radial label a: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.875, rim/outside 3.99 (aggregate of 75 individuals; 1/75 membrane-like individually; rim level 0.369)
  - radial label b: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.854, rim/outside 4.34 (aggregate of 75 individuals; 0/75 membrane-like individually; rim level 0.489)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #356 (t=766, R_eq 1.95): none; #307 (t=706, R_eq 2.19): none; #132 (t=343, R_eq 2.39): none; #513 (t=877, R_eq 2.26): none

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 4 of 75 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
