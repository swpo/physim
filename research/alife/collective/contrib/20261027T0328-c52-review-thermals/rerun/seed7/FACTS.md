# Evidence pack: reacting-thermals (seed 7)

- world: `../../../20261027T0040-c49-reacting-thermals-claim/world.py`, family `reactive-convection`
- parent: None; mutation: -
- run: 601 frames x 25 steps x dt 0.04 = time 600; grid [128, 128]; wall 42s; status ok
- command: `python -m labkit.run collective/contrib/20261027T0040-c49-reacting-thermals-claim/world.py --out collective/contrib/20261027T0328-c52-review-thermals/rerun/seed7 --seeds 7 --frames 600 --spf 25 --no-movie`
- segmentation: matter > 0.36 of robust range [0.0, 0.7037], min area 6 px

## Measurements
- components: final 18, mean 17.3, max 44; occupancy final 0.02
- tracks: 444; persistent (alive >= 50% of run): 0; longest 236 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 0.00 (1 = constant size)
- enclosures: components with a hole mean 0.02, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [31, 26, 20], H1 [0, 0, 0]
- motion: 167 long-lived tracks moved >= 1 body length; max speed 1.21/time; max body lengths 29.6
- replication (lineage window K = 20 frames = time 20, default): splits 102, persistent splits 34 (0 more failed only because the siblings re-merged within K), max generation 7, merges 19, merge/split ratio 0.186, nucleations 189
- channel total drift (end/start - 1): [-0.8488, -0.3205, None, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 147 at frame 272: holes 0, rim-vs-core 0.30, rim-vs-outside 0.56, heterogeneity 0.15; core [0.916, 0.07, 0.523, 0.955] rim [0.707, 0.111, 0.485, 0.754]
  - track 208 at frame 373: holes 0, rim-vs-core 0.26, rim-vs-outside 0.64, heterogeneity 0.18; core [0.941, 0.04, 0.459, 0.954] rim [0.739, 0.112, 0.44, 0.802]
  - track 383 at frame 560: holes 0, rim-vs-core 0.28, rim-vs-outside 0.65, heterogeneity 0.16; core [0.99, 0.037, 0.521, 0.994] rim [0.77, 0.093, 0.51, 0.826]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 85 components >= 12 px at frames [101, 202, 303, 398, 499, 600]):
  - radial heat T: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.872, rim/outside 5.34 (aggregate of 85 individuals; 2/85 membrane-like individually; rim level 0.659)
  - radial fuel Y: peak at rho=2.45 (OUTSIDE the peak band 0.5-1.5), rim/core 4.49, rim/outside 0.621 (aggregate of 85 individuals; 0/85 membrane-like individually; rim level 0.212)
  - radial vorticity: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 1.03, rim/outside 1.08 (aggregate of 85 individuals; 18/85 membrane-like individually; rim level 0.499)
  - radial burn r: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.908, rim/outside 6.43 (aggregate of 85 individuals; 6/85 membrane-like individually; rim level 0.66)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #147 (t=272, R_eq 2.33): none; #142 (t=227, R_eq 1.78): none; #208 (t=373, R_eq 2.71): none; #383 (t=560, R_eq 2.46): none

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 6 of 85 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
