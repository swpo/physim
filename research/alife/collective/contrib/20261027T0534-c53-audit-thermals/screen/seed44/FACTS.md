# Evidence pack: reacting-thermals (seed 44)

- world: `../../../20261027T0040-c49-reacting-thermals-claim/world.py`, family `reactive-convection`
- parent: None; mutation: -
- run: 201 frames x 25 steps x dt 0.04 = time 200; grid [128, 128]; wall 14s; status ok
- command: `python -m labkit.run collective/contrib/20261027T0040-c49-reacting-thermals-claim/world.py --out collective/contrib/c53-audit-work/screen --seeds 35 36 37 38 39 40 41 42 43 44 45 46 --frames 200 --spf 25 --no-movie`
- segmentation: matter > 0.34 of robust range [0.0, 0.7255], min area 6 px

## Measurements
- components: final 18, mean 10.5, max 42; occupancy final 0.02
- tracks: 166; persistent (alive >= 50% of run): 0; longest 100 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 0.00 (1 = constant size)
- enclosures: components with a hole mean 0.08, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [24, 20, 19], H1 [0, 0, 0]
- motion: 35 long-lived tracks moved >= 1 body length; max speed 0.843/time; max body lengths 12.7
- replication (lineage window K = 20 frames = time 20, default): splits 45, persistent splits 10 (0 more failed only because the siblings re-merged within K), max generation 3, merges 6, merge/split ratio 0.133, nucleations 24
- channel total drift (end/start - 1): [-0.8708, -0.2534, None, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 119 at frame 151: holes 0, rim-vs-core 0.24, rim-vs-outside 0.46, heterogeneity 0.11; core [0.738, 0.237, 0.518, 0.885] rim [0.58, 0.269, 0.494, 0.716]
  - track 122 at frame 153: holes 0, rim-vs-core 0.31, rim-vs-outside 0.51, heterogeneity 0.14; core [0.758, 0.248, 0.318, 0.917] rim [0.556, 0.279, 0.381, 0.688]
  - track 120 at frame 141: holes 0, rim-vs-core 0.25, rim-vs-outside 0.49, heterogeneity 0.15; core [0.747, 0.21, 0.546, 0.833] rim [0.557, 0.27, 0.528, 0.682]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 54 components >= 12 px at frames [34, 67, 101, 133, 166, 200]):
  - radial heat T: peak at rho=0.35 (OUTSIDE the peak band 0.5-1.5), rim/core 0.848, rim/outside 4.54 (aggregate of 54 individuals; 1/54 membrane-like individually; rim level 0.458)
  - radial fuel Y: peak at rho=2.45 (OUTSIDE the peak band 0.5-1.5), rim/core 1.65, rim/outside 0.774 (aggregate of 54 individuals; 0/54 membrane-like individually; rim level 0.368)
  - radial vorticity: peak at rho=1.05 (in the peak band 0.5-1.5), rim/core 1.12, rim/outside 1.05 (aggregate of 54 individuals; 7/54 membrane-like individually; rim level 0.49)
  - radial burn r: peak at rho=0.35 (OUTSIDE the peak band 0.5-1.5), rim/core 0.892, rim/outside 5.28 (aggregate of 54 individuals; 4/54 membrane-like individually; rim level 0.516)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #119 (t=151, R_eq 2.59): none; #122 (t=153, R_eq 3.04): none; #120 (t=141, R_eq 2.82): none; #148 (t=190, R_eq 2.99, ring): none

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 7 of 54 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
