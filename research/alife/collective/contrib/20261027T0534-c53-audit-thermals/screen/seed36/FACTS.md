# Evidence pack: reacting-thermals (seed 36)

- world: `../../../20261027T0040-c49-reacting-thermals-claim/world.py`, family `reactive-convection`
- parent: None; mutation: -
- run: 201 frames x 25 steps x dt 0.04 = time 200; grid [128, 128]; wall 14s; status ok
- command: `python -m labkit.run collective/contrib/20261027T0040-c49-reacting-thermals-claim/world.py --out collective/contrib/c53-audit-work/screen --seeds 35 36 37 38 39 40 41 42 43 44 45 46 --frames 200 --spf 25 --no-movie`
- segmentation: matter > 0.35 of robust range [0.0, 0.7116], min area 6 px

## Measurements
- components: final 7, mean 6.6, max 42; occupancy final 0.01
- tracks: 131; persistent (alive >= 50% of run): 3; longest 161 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 9.83 (1 = constant size)
- enclosures: components with a hole mean 0.07, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [10, 8, 7], H1 [0, 0, 0]
- motion: 15 long-lived tracks moved >= 1 body length; max speed 0.917/time; max body lengths 22.8
- replication (lineage window K = 20 frames = time 20, default): splits 37, persistent splits 3 (0 more failed only because the siblings re-merged within K), max generation 1, merges 7, merge/split ratio 0.189, nucleations 19
- channel total drift (end/start - 1): [-0.9379, -0.124, None, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 108 at frame 121: holes 0, rim-vs-core 0.26, rim-vs-outside 0.59, heterogeneity 0.14; core [0.774, 0.269, 0.218, 0.966] rim [0.597, 0.296, 0.289, 0.788]
  - track 110 at frame 104: holes 0, rim-vs-core 0.23, rim-vs-outside 0.50, heterogeneity 0.17; core [0.738, 0.201, 0.374, 0.848] rim [0.574, 0.253, 0.412, 0.696]
  - track 111 at frame 121: holes 0, rim-vs-core 0.24, rim-vs-outside 0.47, heterogeneity 0.16; core [0.707, 0.212, 0.528, 0.824] rim [0.55, 0.269, 0.623, 0.68]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 20 components >= 12 px at frames [34, 67, 101, 133, 166, 200]):
  - radial heat T: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.841, rim/outside 5.2 (aggregate of 20 individuals; 0/20 membrane-like individually; rim level 0.482)
  - radial fuel Y: peak at rho=2.45 (OUTSIDE the peak band 0.5-1.5), rim/core 1.76, rim/outside 0.754 (aggregate of 20 individuals; 0/20 membrane-like individually; rim level 0.372)
  - radial vorticity: peak at rho=1.45 (in the peak band 0.5-1.5), rim/core 1.09, rim/outside 1.04 (aggregate of 20 individuals; 4/20 membrane-like individually; rim level 0.46)
  - radial burn r: peak at rho=0.35 (OUTSIDE the peak band 0.5-1.5), rim/core 0.887, rim/outside 6.11 (aggregate of 20 individuals; 1/20 membrane-like individually; rim level 0.553)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #108 (t=121, R_eq 2.39): ['vorticity']; #110 (t=104, R_eq 2.52): none; #111 (t=121, R_eq 2.59): none; #114 (t=148, R_eq 1.69): none

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 4 of 20 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
