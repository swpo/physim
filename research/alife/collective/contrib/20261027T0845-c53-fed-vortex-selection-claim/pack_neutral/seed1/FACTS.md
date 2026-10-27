# Evidence pack: fed-vortices (seed 1)

- world: `../../world.py`, family `fed-vortex`
- parent: None; mutation: -
- run: 1501 frames x 150 steps x dt 0.02 = time 4500; grid [128, 128]; wall 863s; status ok
- command: `python -m labkit.run collective/contrib/c53-fvh/world.py --out collective/contrib/c53-fvh/pack_neutral --seeds 1 2 --frames 1500 --spf 150 --no-movie`
- segmentation: matter > 0.29 of robust range [0.0, 0.2045], min area 6 px

## Measurements
- components: final 29, mean 29.7, max 49; occupancy final 0.15
- tracks: 399; persistent (alive >= 50% of run): 8; longest 1048 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 14.00 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [33, 32, 29], H1 [0, 0, 0]
- motion: 209 long-lived tracks moved >= 1 body length; max speed 0.483/time; max body lengths 38.6
- replication (lineage window K = 20 frames = time 60, default): splits 122, persistent splits 54 (0 more failed only because the siblings re-merged within K), max generation 10, merges 108, merge/split ratio 0.885, nucleations 0
- channel total drift (end/start - 1): [-0.5265, 0.1421, None, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 149 at frame 882: holes 0, rim-vs-core 0.67, rim-vs-outside 0.41, heterogeneity 0.15; core [0.878, 0.117, 0.902, 0.016] rim [0.455, 0.303, 0.42, 0.008]
  - track 106 at frame 693: holes 0, rim-vs-core 0.70, rim-vs-outside 0.37, heterogeneity 0.16; core [0.843, 0.107, 0.887, 0.012] rim [0.42, 0.319, 0.378, 0.006]
  - track 200 at frame 1021: holes 0, rim-vs-core 0.63, rim-vs-outside 0.36, heterogeneity 0.14; core [0.759, 0.101, 0.864, 0.02] rim [0.409, 0.322, 0.384, 0.01]
  - track 313 at frame 1324: holes 0, rim-vs-core 0.60, rim-vs-outside 0.31, heterogeneity 0.17; core [0.814, 0.123, 0.591, 0.383] rim [0.403, 0.307, 0.238, 0.19]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 173 components >= 12 px at frames [252, 504, 756, 996, 1248, 1500]):
  - radial |vorticity|: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.768, rim/outside 15.6 (aggregate of 173 individuals; 0/173 membrane-like individually; rim level 0.677)
  - radial fuel Y: peak at rho=2.45 (OUTSIDE the peak band 0.5-1.5), rim/core 10.3, rim/outside 0.77 (aggregate of 173 individuals; 0/173 membrane-like individually; rim level 0.476)
  - radial label a: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.784, rim/outside 17.2 (aggregate of 173 individuals; 2/173 membrane-like individually; rim level 0.458)
  - radial label b: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.782, rim/outside 13.7 (aggregate of 173 individuals; 2/173 membrane-like individually; rim level 0.365)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #149 (t=2646, R_eq 3.78): none; #106 (t=2079, R_eq 4.58): none; #200 (t=3063, R_eq 5.7): none; #313 (t=3972, R_eq 4.3): none

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 2 of 173 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
