# Evidence pack: nematic-fuelcell (seed 1)

- world: `../../../20261025T1412-c15-nematic-fuelcell-claim/world.py`, family `active-nematic`
- parent: None; mutation: new class: CH droplets with internal Landau-de Gennes nematic order and extensile active stress, Brinkman-Stokes flow
- run: 201 frames x 100 steps x dt 0.05 = time 1000; grid [128, 128]; wall 541s; status ok
- command: `python -m labkit.run collective/contrib/20261025T1412-c15-nematic-fuelcell-claim/world.py --out collective/contrib/20261025T1619-c19-fuelcell-slowd-twins/chis0_Df0.5/seed1 --seeds 1 --no-movie`
- segmentation: matter > 0.58 of robust range [-0.8555, 0.6115], min area 6 px

## Measurements
- components: final 9, mean 4.8, max 9; occupancy final 0.07
- tracks: 20; persistent (alive >= 50% of run): 4; longest 119 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 18.11 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [13, 10, 8], H1 [3, 0, 0]
- motion: 4 long-lived tracks moved >= 1 body length; max speed 0.031/time; max body lengths 1.8
- replication (lineage window K = 20 frames = time 100, default): splits 8, persistent splits 4 (0 more failed only because the siblings re-merged within K), max generation 2, merges 1, merge/split ratio 0.125, nucleations 3
- channel total drift (end/start - 1): [-0.4928, -0.4323, None, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 3 at frame 89: holes 0, rim-vs-core 0.27, rim-vs-outside 0.72, heterogeneity 0.11; core [0.99, 0.943, 0.973, 0.978] rim [0.855, 0.736, 0.938, 0.869]
  - track 1 at frame 71: holes 0, rim-vs-core 0.36, rim-vs-outside 0.44, heterogeneity 0.11; core [0.957, 0.9, 0.955, 0.915] rim [0.751, 0.643, 0.894, 0.771]
  - track 5 at frame 150: holes 0, rim-vs-core 0.22, rim-vs-outside 0.66, heterogeneity 0.10; core [0.966, 0.813, 0.967, 0.92] rim [0.838, 0.65, 0.935, 0.838]
  - track 12 at frame 175: holes 0, rim-vs-core 0.43, rim-vs-outside 0.38, heterogeneity 0.11; core [0.967, 0.877, 0.839, 0.798] rim [0.741, 0.549, 0.779, 0.648]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 34 components >= 12 px at frames [34, 67, 101, 133, 166, 200]):
  - radial phi (droplet): peak at rho=0.25 (OUTSIDE the peak band 0.5-1.5), rim/core 0.841, rim/outside 3.26 (aggregate of 34 individuals; 6/34 membrane-like individually; rim level 0.565)
  - radial order |Q|: peak at rho=0.35 (OUTSIDE the peak band 0.5-1.5), rim/core 0.837, rim/outside 4.67 (aggregate of 34 individuals; 6/34 membrane-like individually; rim level 0.498)
  - radial shell s: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.939, rim/outside 1.44 (aggregate of 34 individuals; 0/34 membrane-like individually; rim level 0.822)
  - radial fuel f: peak at rho=0.25 (OUTSIDE the peak band 0.5-1.5), rim/core 0.904, rim/outside 2.15 (aggregate of 34 individuals; 1/34 membrane-like individually; rim level 0.713)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #3 (t=445, R_eq 6.91, ring): ['phi (droplet)', 'order |Q|']; #1 (t=355, R_eq 5.75): none; #5 (t=750, R_eq 8.1): none; #12 (t=875, R_eq 2.82): none

## Warnings
- radial: 10 of 34 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
