# Evidence pack: reacting-thermals (seed 46)

- world: `../../../20261027T0040-c49-reacting-thermals-claim/world.py`, family `reactive-convection`
- parent: None; mutation: -
- run: 201 frames x 25 steps x dt 0.04 = time 200; grid [128, 128]; wall 14s; status ok
- command: `python -m labkit.run collective/contrib/20261027T0040-c49-reacting-thermals-claim/world.py --out collective/contrib/c53-audit-work/screen --seeds 35 36 37 38 39 40 41 42 43 44 45 46 --frames 200 --spf 25 --no-movie`
- segmentation: matter > 0.34 of robust range [0.0, 0.73], min area 6 px

## Measurements
- components: final 14, mean 5.9, max 42; occupancy final 0.02
- tracks: 118; persistent (alive >= 50% of run): 1; longest 141 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 7.57 (1 = constant size)
- enclosures: components with a hole mean 0.07, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [14, 13, 11], H1 [0, 0, 0]
- motion: 16 long-lived tracks moved >= 1 body length; max speed 1.01/time; max body lengths 11.7
- replication (lineage window K = 20 frames = time 20, default): splits 34, persistent splits 6 (0 more failed only because the siblings re-merged within K), max generation 3, merges 6, merge/split ratio 0.176, nucleations 8
- channel total drift (end/start - 1): [-0.9183, -0.1595, None, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 95 at frame 121: holes 0, rim-vs-core 0.28, rim-vs-outside 0.48, heterogeneity 0.15; core [0.696, 0.24, 0.531, 0.851] rim [0.511, 0.282, 0.535, 0.643]
  - track 94 at frame 87: holes 0, rim-vs-core 0.26, rim-vs-outside 0.55, heterogeneity 0.17; core [0.724, 0.235, 0.345, 0.868] rim [0.537, 0.297, 0.343, 0.704]
  - track 99 at frame 161: holes 0, rim-vs-core 0.27, rim-vs-outside 0.57, heterogeneity 0.19; core [0.751, 0.216, 0.403, 0.868] rim [0.548, 0.293, 0.433, 0.718]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 33 components >= 12 px at frames [34, 67, 101, 133, 166, 200]):
  - radial heat T: peak at rho=0.35 (OUTSIDE the peak band 0.5-1.5), rim/core 0.882, rim/outside 5.03 (aggregate of 33 individuals; 1/33 membrane-like individually; rim level 0.463)
  - radial fuel Y: peak at rho=2.45 (OUTSIDE the peak band 0.5-1.5), rim/core 1.65, rim/outside 0.76 (aggregate of 33 individuals; 0/33 membrane-like individually; rim level 0.384)
  - radial vorticity: peak at rho=0.65 (in the peak band 0.5-1.5), rim/core 1.11, rim/outside 1.09 (aggregate of 33 individuals; 6/33 membrane-like individually; rim level 0.495)
  - radial burn r: peak at rho=0.35 (OUTSIDE the peak band 0.5-1.5), rim/core 0.928, rim/outside 5.8 (aggregate of 33 individuals; 2/33 membrane-like individually; rim level 0.552)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #95 (t=121, R_eq 3.43): none; #94 (t=87, R_eq 2.52): ['vorticity']; #99 (t=161, R_eq 3.39): none; #104 (t=188, R_eq 1.87): ['vorticity']

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 1 of 33 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
