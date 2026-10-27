# Evidence pack: reacting-thermals (seed 1)

- world: `../../world.py`, family `reactive-convection`
- parent: None; mutation: -
- run: 601 frames x 25 steps x dt 0.04 = time 600; grid [128, 128]; wall 59s; status ok
- command: `python -m labkit.run collective/contrib/20261027T0040-c49-reacting-thermals-claim/world.py --out collective/contrib/20261027T0040-c49-reacting-thermals-claim/pack --seeds 0 1 2 --frames 600 --spf 25 --no-movie`
- segmentation: matter > 0.41 of robust range [0.0, 0.611], min area 6 px

## Measurements
- components: final 20, mean 14.8, max 47; occupancy final 0.02
- tracks: 475; persistent (alive >= 50% of run): 0; longest 179 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 0.00 (1 = constant size)
- enclosures: components with a hole mean 0.02, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [30, 28, 23], H1 [0, 0, 0]
- motion: 136 long-lived tracks moved >= 1 body length; max speed 1.5/time; max body lengths 24.3
- replication (lineage window K = 20 frames = time 20, default): splits 112, persistent splits 21 (0 more failed only because the siblings re-merged within K), max generation 5, merges 27, merge/split ratio 0.241, nucleations 198
- channel total drift (end/start - 1): [-0.839, -0.3242, None, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 127 at frame 192: holes 0, rim-vs-core 0.27, rim-vs-outside 0.70, heterogeneity 0.16; core [0.989, 0.032, 0.381, 0.98] rim [0.794, 0.09, 0.464, 0.827]
  - track 132 at frame 197: holes 0, rim-vs-core 0.19, rim-vs-outside 0.47, heterogeneity 0.14; core [0.875, 0.023, 0.448, 0.846] rim [0.726, 0.076, 0.472, 0.741]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 69 components >= 12 px at frames [101, 202, 303, 398, 499, 600]):
  - radial heat T: peak at rho=0.25 (OUTSIDE the peak band 0.5-1.5), rim/core 0.926, rim/outside 5.59 (aggregate of 69 individuals; 2/69 membrane-like individually; rim level 0.664)
  - radial fuel Y: peak at rho=2.45 (OUTSIDE the peak band 0.5-1.5), rim/core 4.37, rim/outside 0.626 (aggregate of 69 individuals; 0/69 membrane-like individually; rim level 0.226)
  - radial vorticity: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 1.07, rim/outside 1.1 (aggregate of 69 individuals; 12/69 membrane-like individually; rim level 0.507)
  - radial burn r: peak at rho=0.25 (OUTSIDE the peak band 0.5-1.5), rim/core 0.971, rim/outside 6.47 (aggregate of 69 individuals; 8/69 membrane-like individually; rim level 0.655)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #127 (t=192, R_eq 3.39): none; #132 (t=197, R_eq 3.24): ['burn r']; #167 (t=348, R_eq 2.39): ['vorticity']; #263 (t=429, R_eq 1.69): ['vorticity']

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 13 of 69 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
