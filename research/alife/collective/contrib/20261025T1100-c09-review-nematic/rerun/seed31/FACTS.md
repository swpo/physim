# Evidence pack: active-nematic-droplets (seed 31)

- world: `../../../20261025T1014-c11-active-nematic-colony/world.py`, family `active-nematic`
- parent: None; mutation: new class: CH droplets with internal Landau-de Gennes nematic order and extensile active stress, Brinkman-Stokes flow
- run: 201 frames x 100 steps x dt 0.05 = time 1000; grid [128, 128]; wall 271s; status ok
- command: `python -m labkit.run collective/contrib/20261025T1014-c11-active-nematic-colony/world.py --out collective/contrib/20261025T1100-c09-review-nematic/rerun/seed31 --seeds 31 --no-movie`
- segmentation: matter > 0.56 of robust range [-0.8253, 0.6354], min area 6 px

## Measurements
- components: final 27, mean 18.5, max 28; occupancy final 0.06
- tracks: 103; persistent (alive >= 50% of run): 4; longest 128 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 2.28 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [29, 28, 25], H1 [0, 0, 0]
- motion: 48 long-lived tracks moved >= 1 body length; max speed 0.119/time; max body lengths 2.9
- replication (lineage window K = 20 frames = time 100, default): splits 42, persistent splits 24 (0 more failed only because the siblings re-merged within K), max generation 4, merges 12, merge/split ratio 0.286, nucleations 7
- channel total drift (end/start - 1): [-0.4988, -0.4403, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 27 at frame 138: holes 0, rim-vs-core 0.39, rim-vs-outside 0.37, heterogeneity 0.16; core [0.954, 0.931, 0.52] rim [0.733, 0.614, 0.506]
  - track 33 at frame 139: holes 0, rim-vs-core 0.36, rim-vs-outside 0.36, heterogeneity 0.15; core [0.938, 0.882, 0.535] rim [0.734, 0.591, 0.535]
  - track 35 at frame 143: holes 0, rim-vs-core 0.38, rim-vs-outside 0.39, heterogeneity 0.16; core [0.973, 0.976, 0.426] rim [0.749, 0.669, 0.44]
  - track 76 at frame 170: holes 0, rim-vs-core 0.20, rim-vs-outside 0.41, heterogeneity 0.14; core [0.906, 0.787, 0.478] rim [0.772, 0.634, 0.479]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 122 components >= 12 px at frames [34, 67, 101, 133, 166, 200]):
  - radial phi (droplet): peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.816, rim/outside 4.68 (aggregate of 122 individuals; 0/122 membrane-like individually; rim level 0.745)
  - radial order |Q|: peak at rho=0.25 (OUTSIDE the peak band 0.5-1.5), rim/core 0.778, rim/outside 7.72 (aggregate of 122 individuals; 2/122 membrane-like individually; rim level 0.633)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #27 (t=690, R_eq 3.09): none; #33 (t=695, R_eq 3.24): none; #35 (t=715, R_eq 3.14): none; #76 (t=850, R_eq 3.52): none

## Warnings
- radial: 4 of 122 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
