# Evidence pack: nematic-fuelcell (seed 31)

- world: `../../../20261025T1412-c15-nematic-fuelcell-claim/world.py`, family `active-nematic`
- parent: None; mutation: new class: CH droplets with internal Landau-de Gennes nematic order and extensile active stress, Brinkman-Stokes flow
- run: 201 frames x 100 steps x dt 0.05 = time 1000; grid [128, 128]; wall 509s; status ok
- command: `python -m labkit.run collective/contrib/20261025T1412-c15-nematic-fuelcell-claim/world.py --out collective/contrib/20261025T2105-c25-review-fuelring-slowd/controls/slowD06_s31 --seeds 31 --no-movie`
- segmentation: matter > 0.57 of robust range [-0.8684, 0.6447], min area 6 px

## Measurements
- components: final 21, mean 9.2, max 21; occupancy final 0.10
- tracks: 35; persistent (alive >= 50% of run): 7; longest 185 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 52.86 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [28, 22, 21], H1 [0, 0, 0]
- motion: 4 long-lived tracks moved >= 1 body length; max speed 0.0425/time; max body lengths 2.5
- replication (lineage window K = 20 frames = time 100, default): splits 14, persistent splits 6 (0 more failed only because the siblings re-merged within K), max generation 1, merges 0, merge/split ratio 0, nucleations 7
- channel total drift (end/start - 1): [-0.4988, -0.1191, None, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 4 at frame 109: holes 0, rim-vs-core 0.32, rim-vs-outside 0.62, heterogeneity 0.10; core [0.963, 0.86, 0.974, 0.957] rim [0.81, 0.612, 0.932, 0.829]
  - track 1 at frame 86: holes 0, rim-vs-core 0.26, rim-vs-outside 0.66, heterogeneity 0.09; core [0.954, 0.817, 0.976, 0.936] rim [0.817, 0.631, 0.941, 0.83]
  - track 2 at frame 86: holes 0, rim-vs-core 0.23, rim-vs-outside 0.64, heterogeneity 0.09; core [0.943, 0.759, 0.99, 0.963] rim [0.816, 0.621, 0.939, 0.836]
  - track 7 at frame 160: holes 0, rim-vs-core 0.42, rim-vs-outside 0.41, heterogeneity 0.12; core [0.962, 0.938, 0.906, 0.973] rim [0.735, 0.627, 0.821, 0.825]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 66 components >= 12 px at frames [34, 67, 101, 133, 166, 200]):
  - radial phi (droplet): peak at rho=0.25 (OUTSIDE the peak band 0.5-1.5), rim/core 0.848, rim/outside 3.34 (aggregate of 66 individuals; 13/66 membrane-like individually; rim level 0.546)
  - radial order |Q|: peak at rho=0.25 (OUTSIDE the peak band 0.5-1.5), rim/core 0.831, rim/outside 4.85 (aggregate of 66 individuals; 13/66 membrane-like individually; rim level 0.467)
  - radial shell s: peak at rho=0.25 (OUTSIDE the peak band 0.5-1.5), rim/core 0.942, rim/outside 1.44 (aggregate of 66 individuals; 0/66 membrane-like individually; rim level 0.796)
  - radial fuel f: peak at rho=0.25 (OUTSIDE the peak band 0.5-1.5), rim/core 0.904, rim/outside 1.96 (aggregate of 66 individuals; 1/66 membrane-like individually; rim level 0.71)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #4 (t=545, R_eq 7.53, ring): ['phi (droplet)', 'order |Q|']; #1 (t=430, R_eq 8.21, ring): ['phi (droplet)', 'order |Q|']; #2 (t=430, R_eq 7.9, ring): ['phi (droplet)', 'order |Q|']; #7 (t=800, R_eq 3.91): none

## Warnings
- radial: 22 of 66 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
