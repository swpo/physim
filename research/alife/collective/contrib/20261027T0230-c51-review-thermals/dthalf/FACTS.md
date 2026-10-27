# Evidence pack: reacting-thermals (seed 9)

- world: `../../20261027T0040-c49-reacting-thermals-claim/world.py`, family `reactive-convection`
- parent: None; mutation: -
- run: 601 frames x 50 steps x dt 0.02 (--dt; world META dt 0.04) = time 600; grid [128, 128]; wall 72s; status ok
- command: `python -m labkit.run collective/contrib/20261027T0040-c49-reacting-thermals-claim/world.py --out collective/contrib/20261027T0230-c51-review-thermals/dthalf --seeds 9 --frames 600 --spf 50 --dt 0.02 --no-movie`
- segmentation: matter > 0.37 of robust range [0.0, 0.6696], min area 6 px

## Measurements
- components: final 25, mean 12.0, max 40; occupancy final 0.02
- tracks: 379; persistent (alive >= 50% of run): 0; longest 248 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 0.00 (1 = constant size)
- enclosures: components with a hole mean 0.02, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [32, 29, 26], H1 [0, 0, 0]
- motion: 122 long-lived tracks moved >= 1 body length; max speed 0.992/time; max body lengths 34.2
- replication (lineage window K = 20 frames = time 20, default): splits 91, persistent splits 25 (0 more failed only because the siblings re-merged within K), max generation 7, merges 19, merge/split ratio 0.209, nucleations 141
- channel total drift (end/start - 1): [-0.8513, -0.3212, None, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 162 at frame 464: holes 0, rim-vs-core 0.20, rim-vs-outside 0.63, heterogeneity 0.14; core [0.971, 0.061, 0.651, 0.984] rim [0.816, 0.112, 0.655, 0.86]
  - track 209 at frame 469: holes 0, rim-vs-core 0.21, rim-vs-outside 0.49, heterogeneity 0.11; core [0.857, 0.079, 0.359, 0.91] rim [0.715, 0.116, 0.435, 0.775]
  - track 208 at frame 459: holes 0, rim-vs-core 0.29, rim-vs-outside 0.52, heterogeneity 0.15; core [0.93, 0.07, 0.546, 0.955] rim [0.713, 0.122, 0.477, 0.78]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 64 components >= 12 px at frames [101, 202, 303, 398, 499, 600]):
  - radial heat T: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.877, rim/outside 4.97 (aggregate of 64 individuals; 0/64 membrane-like individually; rim level 0.637)
  - radial fuel Y: peak at rho=2.45 (OUTSIDE the peak band 0.5-1.5), rim/core 3.06, rim/outside 0.634 (aggregate of 64 individuals; 0/64 membrane-like individually; rim level 0.232)
  - radial vorticity: peak at rho=0.95 (in the peak band 0.5-1.5), rim/core 1.09, rim/outside 1.09 (aggregate of 64 individuals; 20/64 membrane-like individually; rim level 0.499)
  - radial burn r: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.915, rim/outside 5.81 (aggregate of 64 individuals; 7/64 membrane-like individually; rim level 0.647)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #162 (t=464, R_eq 2.03): none; #209 (t=469, R_eq 2.46): none; #208 (t=459, R_eq 2.39): none; #261 (t=504, R_eq 1.78): ['vorticity']

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- --dt 0.02 only relabels time (world META dt 0.04): the world's integration step is unchanged, so this run is NOT a dt/2 (or any time-step) test; change the world's own step for that
- radial: 7 of 64 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
