# Evidence pack: reacting-thermals (seed 0)

- world: `../world.py`, family `reactive-convection`
- parent: None; mutation: -
- run: 801 frames x 25 steps x dt 0.04 = time 800; grid [128, 128]; wall 87s; status ok
- command: `python -m labkit.run collective/contrib/20261027T0209-c49-thermals-flow-heredity/world.py --out collective/contrib/20261027T0209-c49-thermals-flow-heredity/pack_eps0.1 --seeds 0 --frames 800 --spf 25 --no-movie`
- segmentation: matter > 0.33 of robust range [0.0, 0.7562], min area 6 px

## Measurements
- components: final 23, mean 16.3, max 43; occupancy final 0.02
- tracks: 634; persistent (alive >= 50% of run): 0; longest 237 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 0.00 (1 = constant size)
- enclosures: components with a hole mean 0.02, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [37, 33, 25], H1 [0, 0, 0]
- motion: 217 long-lived tracks moved >= 1 body length; max speed 1.16/time; max body lengths 28.2
- replication (lineage window K = 20 frames = time 20, default): splits 135, persistent splits 36 (0 more failed only because the siblings re-merged within K), max generation 6, merges 24, merge/split ratio 0.178, nucleations 310
- channel total drift (end/start - 1): [-0.874, -0.3508, None, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 139 at frame 383: holes 0, rim-vs-core 0.16, rim-vs-outside 0.46, heterogeneity 0.06; core [0.924, 0.093, 0.058, 1.0] rim [0.774, 0.136, 0.051, 0.973]
  - track 153 at frame 350: holes 0, rim-vs-core 0.20, rim-vs-outside 0.61, heterogeneity 0.07; core [0.97, 0.004, 1.0, 0.039] rim [0.791, 0.051, 0.925, 0.029]
  - track 177 at frame 363: holes 0, rim-vs-core 0.23, rim-vs-outside 0.56, heterogeneity 0.09; core [0.938, 0.026, 0.949, 0.093] rim [0.751, 0.089, 0.831, 0.078]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 77 components >= 12 px at frames [134, 269, 403, 531, 666, 800]):
  - radial heat T: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.913, rim/outside 5.78 (aggregate of 77 individuals; 0/77 membrane-like individually; rim level 0.715)
  - radial fuel Y: peak at rho=2.45 (OUTSIDE the peak band 0.5-1.5), rim/core 4.52, rim/outside 0.607 (aggregate of 77 individuals; 0/77 membrane-like individually; rim level 0.197)
  - radial label a: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.887, rim/outside 4.93 (aggregate of 77 individuals; 2/77 membrane-like individually; rim level 0.567)
  - radial label b: peak at rho=0.25 (OUTSIDE the peak band 0.5-1.5), rim/core 1.04, rim/outside 3.79 (aggregate of 77 individuals; 4/77 membrane-like individually; rim level 0.258)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #139 (t=383, R_eq 2.33): none; #153 (t=350, R_eq 2.46): ['label b']; #338 (t=578, R_eq 1.87): none; #177 (t=363, R_eq 2.46): none

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 3 of 77 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
