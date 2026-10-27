# Evidence pack: reacting-thermals (seed 0)

- world: `../world.py`, family `reactive-convection`
- parent: None; mutation: -
- run: 601 frames x 50 steps x dt 0.02 (--dt; world META dt 0.04) = time 600; grid [128, 128]; wall 114s; status ok
- command: `python -m labkit.run collective/contrib/20261027T0040-c49-reacting-thermals-claim/world.py --out collective/contrib/20261027T0040-c49-reacting-thermals-claim/pack_dthalf --seeds 0 --frames 600 --spf 50 --dt 0.02 --no-movie`
- segmentation: matter > 0.33 of robust range [0.0, 0.7534], min area 6 px

## Measurements
- components: final 28, mean 14.2, max 44; occupancy final 0.02
- tracks: 372; persistent (alive >= 50% of run): 0; longest 190 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 0.00 (1 = constant size)
- enclosures: components with a hole mean 0.02, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [33, 32, 30], H1 [0, 0, 0]
- motion: 135 long-lived tracks moved >= 1 body length; max speed 1.24/time; max body lengths 25.5
- replication (lineage window K = 20 frames = time 20, default): splits 85, persistent splits 29 (0 more failed only because the siblings re-merged within K), max generation 7, merges 13, merge/split ratio 0.153, nucleations 152
- channel total drift (end/start - 1): [-0.871, -0.336, None, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 134 at frame 358: holes 0, rim-vs-core 0.23, rim-vs-outside 0.52, heterogeneity 0.14; core [0.889, 0.098, 0.376, 0.936] rim [0.724, 0.128, 0.376, 0.774]
  - track 123 at frame 282: holes 0, rim-vs-core 0.22, rim-vs-outside 0.52, heterogeneity 0.15; core [0.842, 0.08, 0.404, 0.875] rim [0.689, 0.126, 0.487, 0.747]
  - track 168 at frame 424: holes 0, rim-vs-core 0.31, rim-vs-outside 0.64, heterogeneity 0.15; core [0.95, 0.094, 0.228, 0.965] rim [0.696, 0.161, 0.274, 0.799]
  - track 234 at frame 509: holes 0, rim-vs-core 0.18, rim-vs-outside 0.43, heterogeneity 0.15; core [0.857, 0.067, 0.351, 0.856] rim [0.716, 0.113, 0.383, 0.76]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 72 components >= 12 px at frames [101, 202, 303, 398, 499, 600]):
  - radial heat T: peak at rho=0.35 (OUTSIDE the peak band 0.5-1.5), rim/core 0.892, rim/outside 5.15 (aggregate of 72 individuals; 1/72 membrane-like individually; rim level 0.633)
  - radial fuel Y: peak at rho=2.45 (OUTSIDE the peak band 0.5-1.5), rim/core 2.67, rim/outside 0.68 (aggregate of 72 individuals; 0/72 membrane-like individually; rim level 0.255)
  - radial vorticity: peak at rho=0.65 (in the peak band 0.5-1.5), rim/core 1.07, rim/outside 1.05 (aggregate of 72 individuals; 16/72 membrane-like individually; rim level 0.474)
  - radial burn r: peak at rho=0.35 (OUTSIDE the peak band 0.5-1.5), rim/core 0.943, rim/outside 6.22 (aggregate of 72 individuals; 5/72 membrane-like individually; rim level 0.66)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #134 (t=358, R_eq 3.19): none; #123 (t=282, R_eq 3.04): ['burn r']; #168 (t=424, R_eq 2.39): none; #234 (t=509, R_eq 2.39): none

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- --dt 0.02 only relabels time (world META dt 0.04): the world's integration step is unchanged, so this run is NOT a dt/2 (or any time-step) test; change the world's own step for that
- radial: 10 of 72 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
