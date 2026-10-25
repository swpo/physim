# Evidence pack: nematic-fuelcell (seed 1)

- world: `../../../20261025T1412-c15-nematic-fuelcell-claim/world.py`, family `active-nematic`
- parent: None; mutation: new class: CH droplets with internal Landau-de Gennes nematic order and extensile active stress, Brinkman-Stokes flow
- run: 201 frames x 100 steps x dt 0.05 = time 1000; grid [128, 128]; wall 537s; status ok
- command: `python -m labkit.run collective/contrib/20261025T1412-c15-nematic-fuelcell-claim/world.py --out collective/contrib/20261025T1619-c19-fuelcell-slowd-twins/chis0_Df0.2/seed1 --seeds 1 --no-movie`
- segmentation: matter > 0.57 of robust range [-0.8356, 0.6249], min area 6 px

## Measurements
- components: final 15, mean 6.7, max 15; occupancy final 0.06
- tracks: 35; persistent (alive >= 50% of run): 4; longest 125 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 15.78 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [20, 15, 15], H1 [2, 0, 0]
- motion: 10 long-lived tracks moved >= 1 body length; max speed 0.0483/time; max body lengths 2.5
- replication (lineage window K = 20 frames = time 100, default): splits 15, persistent splits 5 (0 more failed only because the siblings re-merged within K), max generation 2, merges 2, merge/split ratio 0.133, nucleations 3
- channel total drift (end/start - 1): [-0.4928, -0.4516, None, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 5 at frame 138: holes 0, rim-vs-core 0.27, rim-vs-outside 0.35, heterogeneity 0.10; core [0.902, 0.715, 0.904, 0.904] rim [0.753, 0.535, 0.864, 0.776]
  - track 6 at frame 138: holes 0, rim-vs-core 0.32, rim-vs-outside 0.40, heterogeneity 0.11; core [0.933, 0.805, 0.948, 0.869] rim [0.767, 0.596, 0.894, 0.705]
  - track 1 at frame 67: holes 0, rim-vs-core 0.34, rim-vs-outside 0.45, heterogeneity 0.11; core [0.938, 0.829, 0.964, 0.893] rim [0.752, 0.617, 0.905, 0.711]
  - track 4 at frame 79: holes 0, rim-vs-core 0.34, rim-vs-outside 0.53, heterogeneity 0.11; core [0.976, 0.985, 0.989, 1.0] rim [0.748, 0.767, 0.921, 0.898]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 47 components >= 12 px at frames [34, 67, 101, 133, 166, 200]):
  - radial phi (droplet): peak at rho=0.25 (OUTSIDE the peak band 0.5-1.5), rim/core 0.835, rim/outside 4.28 (aggregate of 47 individuals; 3/47 membrane-like individually; rim level 0.668)
  - radial order |Q|: peak at rho=0.25 (OUTSIDE the peak band 0.5-1.5), rim/core 0.866, rim/outside 6.52 (aggregate of 47 individuals; 6/47 membrane-like individually; rim level 0.608)
  - radial shell s: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.935, rim/outside 1.47 (aggregate of 47 individuals; 0/47 membrane-like individually; rim level 0.869)
  - radial fuel f: peak at rho=0.25 (OUTSIDE the peak band 0.5-1.5), rim/core 0.842, rim/outside 2.92 (aggregate of 47 individuals; 1/47 membrane-like individually; rim level 0.69)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #5 (t=690, R_eq 4.26): none; #6 (t=690, R_eq 6): none; #1 (t=335, R_eq 5.35): none; #4 (t=395, R_eq 4.37): none

## Warnings
- radial: 7 of 47 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
