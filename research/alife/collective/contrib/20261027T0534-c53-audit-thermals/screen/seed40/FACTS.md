# Evidence pack: reacting-thermals (seed 40)

- world: `../../../20261027T0040-c49-reacting-thermals-claim/world.py`, family `reactive-convection`
- parent: None; mutation: -
- run: 201 frames x 25 steps x dt 0.04 = time 200; grid [128, 128]; wall 14s; status ok
- command: `python -m labkit.run collective/contrib/20261027T0040-c49-reacting-thermals-claim/world.py --out collective/contrib/c53-audit-work/screen --seeds 35 36 37 38 39 40 41 42 43 44 45 46 --frames 200 --spf 25 --no-movie`
- segmentation: matter > 0.33 of robust range [0.0, 0.7625], min area 6 px

## Measurements
- components: final 4, mean 4.1, max 46; occupancy final 0.01
- tracks: 119; persistent (alive >= 50% of run): 0; longest 98 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 0.00 (1 = constant size)
- enclosures: components with a hole mean 0.06, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [5, 4, 4], H1 [0, 0, 0]
- motion: 8 long-lived tracks moved >= 1 body length; max speed 0.687/time; max body lengths 9.1
- replication (lineage window K = 20 frames = time 20, default): splits 35, persistent splits 1 (0 more failed only because the siblings re-merged within K), max generation 1, merges 7, merge/split ratio 0.2, nucleations 8
- channel total drift (end/start - 1): [-0.9625, -0.0763, None, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 113 at frame 111: holes 0, rim-vs-core 0.24, rim-vs-outside 0.43, heterogeneity 0.15; core [0.708, 0.224, 0.579, 0.874] rim [0.551, 0.268, 0.546, 0.704]
  - track 114 at frame 156: holes 0, rim-vs-core 0.19, rim-vs-outside 0.62, heterogeneity 0.19; core [0.762, 0.164, 0.457, 0.812] rim [0.603, 0.251, 0.469, 0.759]
  - track 112 at frame 76: holes 0, rim-vs-core 0.34, rim-vs-outside 0.55, heterogeneity 0.19; core [0.81, 0.213, 0.346, 0.935] rim [0.566, 0.274, 0.425, 0.723]
  - track 115 at frame 180: holes 0, rim-vs-core 0.24, rim-vs-outside 0.48, heterogeneity 0.16; core [0.692, 0.203, 0.434, 0.812] rim [0.533, 0.252, 0.37, 0.652]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 11 components >= 12 px at frames [67, 101, 133, 166, 200]):
  - radial heat T: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.955, rim/outside 5.03 (aggregate of 11 individuals; 1/11 membrane-like individually; rim level 0.498)
  - radial fuel Y: peak at rho=2.35 (OUTSIDE the peak band 0.5-1.5), rim/core 1.78, rim/outside 0.742 (aggregate of 11 individuals; 0/11 membrane-like individually; rim level 0.369)
  - radial vorticity: peak at rho=0.85 (in the peak band 0.5-1.5), rim/core 1.2, rim/outside 1.11 (aggregate of 11 individuals; 3/11 membrane-like individually; rim level 0.484)
  - radial burn r: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 1.09, rim/outside 6.04 (aggregate of 11 individuals; 1/11 membrane-like individually; rim level 0.597)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #113 (t=111, R_eq 2.33): none; #114 (t=156, R_eq 4.03): ['heat T', 'burn r']; #112 (t=76, R_eq 2.33): ['vorticity']; #115 (t=180, R_eq 3.09): none

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 2 of 11 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
