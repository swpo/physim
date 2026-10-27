# Evidence pack: reacting-thermals (seed 35)

- world: `../../../20261027T0040-c49-reacting-thermals-claim/world.py`, family `reactive-convection`
- parent: None; mutation: -
- run: 201 frames x 25 steps x dt 0.04 = time 200; grid [128, 128]; wall 13s; status ok
- command: `python -m labkit.run collective/contrib/20261027T0040-c49-reacting-thermals-claim/world.py --out collective/contrib/c53-audit-work/screen --seeds 35 36 37 38 39 40 41 42 43 44 45 46 --frames 200 --spf 25 --no-movie`
- segmentation: matter > 0.34 of robust range [0.0, 0.7398], min area 6 px

## Measurements
- components: final 14, mean 8.6, max 42; occupancy final 0.02
- tracks: 144; persistent (alive >= 50% of run): 0; longest 91 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 0.00 (1 = constant size)
- enclosures: components with a hole mean 0.04, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [15, 15, 14], H1 [0, 0, 0]
- motion: 29 long-lived tracks moved >= 1 body length; max speed 0.86/time; max body lengths 13.3
- replication (lineage window K = 20 frames = time 20, default): splits 41, persistent splits 8 (0 more failed only because the siblings re-merged within K), max generation 2, merges 9, merge/split ratio 0.22, nucleations 18
- channel total drift (end/start - 1): [-0.905, -0.2099, None, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 46 at frame 55: holes 0, rim-vs-core 0.22, rim-vs-outside 0.42, heterogeneity 0.13; core [0.697, 0.233, 0.56, 0.818] rim [0.548, 0.273, 0.615, 0.667]
  - track 103 at frame 64: holes 0, rim-vs-core 0.25, rim-vs-outside 0.54, heterogeneity 0.14; core [0.713, 0.255, 0.594, 0.881] rim [0.552, 0.294, 0.527, 0.706]
  - track 113 at frame 143: holes 0, rim-vs-core 0.22, rim-vs-outside 0.43, heterogeneity 0.16; core [0.704, 0.212, 0.425, 0.778] rim [0.538, 0.267, 0.467, 0.648]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 43 components >= 12 px at frames [34, 67, 101, 133, 166, 200]):
  - radial heat T: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.865, rim/outside 5.12 (aggregate of 43 individuals; 0/43 membrane-like individually; rim level 0.464)
  - radial fuel Y: peak at rho=2.45 (OUTSIDE the peak band 0.5-1.5), rim/core 1.64, rim/outside 0.762 (aggregate of 43 individuals; 0/43 membrane-like individually; rim level 0.387)
  - radial vorticity: peak at rho=1.45 (in the peak band 0.5-1.5), rim/core 1.12, rim/outside 1.07 (aggregate of 43 individuals; 11/43 membrane-like individually; rim level 0.486)
  - radial burn r: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.911, rim/outside 5.96 (aggregate of 43 individuals; 2/43 membrane-like individually; rim level 0.53)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #46 (t=55, R_eq 2.03): none; #103 (t=64, R_eq 2.46): none; #113 (t=143, R_eq 2.93): ['vorticity']; #125 (t=176, R_eq 2.46): none

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 4 of 43 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
