# Evidence pack: reacting-thermals (seed 3)

- world: `../../20261027T0024-c49-thermals-controls/world.py`, family `reactive-convection`
- parent: None; mutation: -
- run: 2001 frames x 25 steps x dt 0.04 = time 2000; grid [128, 128]; wall 129s; status ok
- command: `python -m labkit.run collective/contrib/20261027T0024-c49-thermals-controls/world.py --out collective/contrib/20261027T0616-c51-review-thermals-controls/pack_long_s3 --seeds 3 --frames 2000 --spf 25 --no-movie`
- segmentation: matter > 0.33 of robust range [0.0, 0.7488], min area 6 px

## Measurements
- components: final 25, mean 21.8, max 42; occupancy final 0.02
- tracks: 1695; persistent (alive >= 50% of run): 0; longest 314 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 0.00 (1 = constant size)
- enclosures: components with a hole mean 0.01, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [30, 27, 24], H1 [0, 0, 0]
- motion: 676 long-lived tracks moved >= 1 body length; max speed 1.25/time; max body lengths 49.0
- replication (lineage window K = 20 frames = time 20, default): splits 271, persistent splits 87 (0 more failed only because the siblings re-merged within K), max generation 7, merges 42, merge/split ratio 0.155, nucleations 1085
- channel total drift (end/start - 1): [-0.8789, -0.318, None, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 993 at frame 1378: holes 0, rim-vs-core 0.19, rim-vs-outside 0.57, heterogeneity 0.16; core [0.934, 0.0, 0.518, 0.904] rim [0.807, 0.04, 0.602, 0.797]
  - track 927 at frame 1261: holes 0, rim-vs-core 0.29, rim-vs-outside 0.51, heterogeneity 0.14; core [0.965, 0.001, 0.507, 0.94] rim [0.766, 0.047, 0.602, 0.759]
  - track 406 at frame 639: holes 0, rim-vs-core 0.18, rim-vs-outside 0.55, heterogeneity 0.17; core [0.926, 0.0, 0.482, 0.863] rim [0.783, 0.036, 0.484, 0.769]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 94 components >= 12 px at frames [336, 672, 1008, 1328, 1664, 2000]):
  - radial heat T: peak at rho=0.25 (OUTSIDE the peak band 0.5-1.5), rim/core 0.898, rim/outside 5.55 (aggregate of 94 individuals; 2/94 membrane-like individually; rim level 0.739)
  - radial fuel Y: peak at rho=2.45 (OUTSIDE the peak band 0.5-1.5), rim/core 10.1, rim/outside 0.564 (aggregate of 94 individuals; 0/94 membrane-like individually; rim level 0.155)
  - radial vorticity: peak at rho=1.25 (in the peak band 0.5-1.5), rim/core 1.1, rim/outside 1.09 (aggregate of 94 individuals; 25/94 membrane-like individually; rim level 0.508)
  - radial burn r: peak at rho=0.25 (OUTSIDE the peak band 0.5-1.5), rim/core 0.928, rim/outside 7.02 (aggregate of 94 individuals; 4/94 membrane-like individually; rim level 0.711)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #993 (t=1378, R_eq 2.26): none; #927 (t=1261, R_eq 2.11): none; #406 (t=639, R_eq 2.39): ['vorticity']; #1282 (t=1714, R_eq 1.69): none

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 7 of 94 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
