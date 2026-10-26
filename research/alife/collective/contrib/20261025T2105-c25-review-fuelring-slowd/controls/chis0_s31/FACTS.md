# Evidence pack: nematic-fuelcell (seed 31)

- world: `../../../20261025T1412-c15-nematic-fuelcell-claim/world.py`, family `active-nematic`
- parent: None; mutation: new class: CH droplets with internal Landau-de Gennes nematic order and extensile active stress, Brinkman-Stokes flow
- run: 201 frames x 100 steps x dt 0.05 = time 1000; grid [128, 128]; wall 500s; status ok
- command: `python -m labkit.run collective/contrib/20261025T1412-c15-nematic-fuelcell-claim/world.py --out collective/contrib/20261025T2105-c25-review-fuelring-slowd/controls/chis0_s31 --seeds 31 --no-movie`
- segmentation: matter > 0.56 of robust range [-0.879, 0.6987], min area 6 px

## Measurements
- components: final 13, mean 7.5, max 13; occupancy final 0.11
- tracks: 19; persistent (alive >= 50% of run): 7; longest 189 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 51.43 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [21, 13, 12], H1 [0, 0, 0]
- motion: 2 long-lived tracks moved >= 1 body length; max speed 0.0285/time; max body lengths 1.1
- replication (lineage window K = 20 frames = time 100, default): splits 6, persistent splits 4 (0 more failed only because the siblings re-merged within K), max generation 2, merges 0, merge/split ratio 0, nucleations 7
- channel total drift (end/start - 1): [-0.4988, 0.0243, None, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 3 at frame 106: holes 0, rim-vs-core 0.27, rim-vs-outside 0.58, heterogeneity 0.09; core [0.947, 0.826, 0.95, 0.943] rim [0.796, 0.622, 0.901, 0.881]
  - track 4 at frame 109: holes 0, rim-vs-core 0.30, rim-vs-outside 0.63, heterogeneity 0.10; core [0.956, 0.883, 0.977, 0.976] rim [0.788, 0.657, 0.92, 0.896]
  - track 5 at frame 109: holes 0, rim-vs-core 0.40, rim-vs-outside 0.66, heterogeneity 0.10; core [0.998, 0.989, 0.939, 0.959] rim [0.801, 0.648, 0.897, 0.883]
  - track 13 at frame 188: holes 0, rim-vs-core 0.29, rim-vs-outside 0.51, heterogeneity 0.09; core [0.965, 0.962, 0.965, 1.0] rim [0.787, 0.744, 0.893, 0.992]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 50 components >= 12 px at frames [34, 67, 101, 133, 166, 200]):
  - radial phi (droplet): peak at rho=0.25 (OUTSIDE the peak band 0.5-1.5), rim/core 0.788, rim/outside 2.56 (aggregate of 50 individuals; 14/50 membrane-like individually; rim level 0.428)
  - radial order |Q|: peak at rho=0.25 (OUTSIDE the peak band 0.5-1.5), rim/core 0.771, rim/outside 3.27 (aggregate of 50 individuals; 14/50 membrane-like individually; rim level 0.353)
  - radial shell s: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.933, rim/outside 1.47 (aggregate of 50 individuals; 0/50 membrane-like individually; rim level 0.756)
  - radial fuel f: peak at rho=0.25 (OUTSIDE the peak band 0.5-1.5), rim/core 0.937, rim/outside 1.43 (aggregate of 50 individuals; 0/50 membrane-like individually; rim level 0.785)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #3 (t=530, R_eq 6.08): none; #4 (t=545, R_eq 8.02, ring): none; #5 (t=545, R_eq 6.79): none; #13 (t=940, R_eq 4.3): none

## Warnings
- radial: 20 of 50 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
