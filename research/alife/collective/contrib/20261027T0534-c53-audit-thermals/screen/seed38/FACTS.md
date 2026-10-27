# Evidence pack: reacting-thermals (seed 38)

- world: `../../../20261027T0040-c49-reacting-thermals-claim/world.py`, family `reactive-convection`
- parent: None; mutation: -
- run: 201 frames x 25 steps x dt 0.04 = time 200; grid [128, 128]; wall 14s; status ok
- command: `python -m labkit.run collective/contrib/20261027T0040-c49-reacting-thermals-claim/world.py --out collective/contrib/c53-audit-work/screen --seeds 35 36 37 38 39 40 41 42 43 44 45 46 --frames 200 --spf 25 --no-movie`
- segmentation: matter > 0.33 of robust range [0.0, 0.7545], min area 6 px

## Measurements
- components: final 9, mean 6.1, max 46; occupancy final 0.02
- tracks: 124; persistent (alive >= 50% of run): 1; longest 110 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 5.67 (1 = constant size)
- enclosures: components with a hole mean 0.08, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [11, 10, 8], H1 [0, 0, 0]
- motion: 19 long-lived tracks moved >= 1 body length; max speed 0.957/time; max body lengths 10.3
- replication (lineage window K = 20 frames = time 20, default): splits 37, persistent splits 6 (0 more failed only because the siblings re-merged within K), max generation 2, merges 5, merge/split ratio 0.135, nucleations 9
- channel total drift (end/start - 1): [-0.9214, -0.1403, None, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 111 at frame 158: holes 0, rim-vs-core 0.20, rim-vs-outside 0.48, heterogeneity 0.12; core [0.664, 0.259, 0.592, 0.842] rim [0.54, 0.287, 0.609, 0.69]
  - track 113 at frame 160: holes 0, rim-vs-core 0.17, rim-vs-outside 0.44, heterogeneity 0.15; core [0.675, 0.212, 0.474, 0.767] rim [0.556, 0.248, 0.484, 0.656]
  - track 115 at frame 178: holes 0, rim-vs-core 0.31, rim-vs-outside 0.45, heterogeneity 0.13; core [0.734, 0.241, 0.334, 0.89] rim [0.546, 0.263, 0.424, 0.663]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 26 components >= 12 px at frames [67, 101, 133, 166, 200]):
  - radial heat T: peak at rho=0.25 (OUTSIDE the peak band 0.5-1.5), rim/core 0.833, rim/outside 4.88 (aggregate of 26 individuals; 1/26 membrane-like individually; rim level 0.451)
  - radial fuel Y: peak at rho=2.45 (OUTSIDE the peak band 0.5-1.5), rim/core 1.67, rim/outside 0.738 (aggregate of 26 individuals; 0/26 membrane-like individually; rim level 0.37)
  - radial vorticity: peak at rho=1.05 (in the peak band 0.5-1.5), rim/core 1.14, rim/outside 1.08 (aggregate of 26 individuals; 4/26 membrane-like individually; rim level 0.496)
  - radial burn r: peak at rho=0.25 (OUTSIDE the peak band 0.5-1.5), rim/core 0.867, rim/outside 5.5 (aggregate of 26 individuals; 2/26 membrane-like individually; rim level 0.509)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #96 (t=67, R_eq 2.03): ['vorticity']; #111 (t=158, R_eq 2.33): ['vorticity']; #113 (t=160, R_eq 3.34): none; #115 (t=178, R_eq 3.61): none

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 2 of 26 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
