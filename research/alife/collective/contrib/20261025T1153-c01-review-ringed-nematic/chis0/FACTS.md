# Evidence pack: active-nematic-droplets (seed 3)

- world: `../../20261025T1141-c11-active-nematic-ringed/world.py`, family `active-nematic`
- parent: None; mutation: new class: CH droplets with internal Landau-de Gennes nematic order and extensile active stress, Brinkman-Stokes flow
- run: 201 frames x 100 steps x dt 0.05 = time 1000; grid [128, 128]; wall 335s; status ok
- command: `python -m labkit.run collective/contrib/20261025T1141-c11-active-nematic-ringed/world.py --out collective/contrib/20261025T1153-c01-review-ringed-nematic/chis0 --seeds 3 --no-movie`
- segmentation: matter > 0.57 of robust range [-0.8228, 0.6151], min area 6 px

## Measurements
- components: final 31, mean 19.3, max 34; occupancy final 0.07
- tracks: 109; persistent (alive >= 50% of run): 4; longest 168 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 3.59 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [33, 31, 29], H1 [0, 0, 0]
- motion: 53 long-lived tracks moved >= 1 body length; max speed 0.0907/time; max body lengths 3.4
- replication (lineage window K = 20 frames = time 100, default): splits 46, persistent splits 25 (0 more failed only because the siblings re-merged within K), max generation 4, merges 11, merge/split ratio 0.239, nucleations 6
- channel total drift (end/start - 1): [-0.5034, -0.4154, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 7 at frame 111: holes 0, rim-vs-core 0.37, rim-vs-outside 0.32, heterogeneity 0.11; core [0.934, 0.87, 0.956] rim [0.73, 0.568, 0.894]
  - track 27 at frame 138: holes 0, rim-vs-core 0.34, rim-vs-outside 0.37, heterogeneity 0.11; core [0.951, 0.904, 0.887] rim [0.761, 0.632, 0.835]
  - track 14 at frame 89: holes 0, rim-vs-core 0.29, rim-vs-outside 0.41, heterogeneity 0.09; core [0.93, 0.95, 0.995] rim [0.752, 0.73, 0.953]
  - track 64 at frame 163: holes 0, rim-vs-core 0.17, rim-vs-outside 0.40, heterogeneity 0.09; core [0.908, 0.747, 0.915] rim [0.79, 0.625, 0.888]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 130 components >= 12 px at frames [34, 67, 101, 133, 166, 200]):
  - radial phi (droplet): peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.807, rim/outside 4.63 (aggregate of 130 individuals; 0/130 membrane-like individually; rim level 0.749)
  - radial order |Q|: peak at rho=0.25 (OUTSIDE the peak band 0.5-1.5), rim/core 0.756, rim/outside 8.06 (aggregate of 130 individuals; 2/130 membrane-like individually; rim level 0.632)
  - radial surfactant s: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.929, rim/outside 1.38 (aggregate of 130 individuals; 0/130 membrane-like individually; rim level 0.88)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #7 (t=555, R_eq 3.52): none; #27 (t=690, R_eq 2.82): none; #14 (t=445, R_eq 4.03): none; #64 (t=815, R_eq 3.52): none

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 2 of 130 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
