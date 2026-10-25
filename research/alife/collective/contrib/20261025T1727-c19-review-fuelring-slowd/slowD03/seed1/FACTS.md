# Evidence pack: nematic-fuelcell (seed 1)

- world: `../../../20261025T1412-c15-nematic-fuelcell-claim/world.py`, family `active-nematic`
- parent: None; mutation: new class: CH droplets with internal Landau-de Gennes nematic order and extensile active stress, Brinkman-Stokes flow
- run: 201 frames x 100 steps x dt 0.05 = time 1000; grid [128, 128]; wall 518s; status ok
- command: `python -m labkit.run collective/contrib/20261025T1412-c15-nematic-fuelcell-claim/world.py --out collective/contrib/20261025T1727-c19-review-fuelring-slowd/slowD03/seed1 --seeds 1 --no-movie`
- segmentation: matter > 0.58 of robust range [-0.8388, 0.6004], min area 6 px

## Measurements
- components: final 14, mean 6.7, max 15; occupancy final 0.07
- tracks: 33; persistent (alive >= 50% of run): 0; longest 100 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 0.00 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [21, 14, 14], H1 [1, 0, 0]
- motion: 7 long-lived tracks moved >= 1 body length; max speed 0.0567/time; max body lengths 2.0
- replication (lineage window K = 20 frames = time 100, default): splits 14, persistent splits 6 (0 more failed only because the siblings re-merged within K), max generation 3, merges 2, merge/split ratio 0.143, nucleations 3
- channel total drift (end/start - 1): [-0.4928, -0.4294, None, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 1 at frame 64: holes 0, rim-vs-core 0.33, rim-vs-outside 0.44, heterogeneity 0.10; core [0.956, 0.884, 0.966, 0.923] rim [0.785, 0.66, 0.916, 0.767]
  - track 3 at frame 74: holes 0, rim-vs-core 0.35, rim-vs-outside 0.70, heterogeneity 0.11; core [1.0, 0.959, 0.965, 0.955] rim [0.838, 0.672, 0.943, 0.835]
  - track 4 at frame 74: holes 0, rim-vs-core 0.37, rim-vs-outside 0.40, heterogeneity 0.13; core [0.98, 0.758, 0.992, 0.983] rim [0.748, 0.523, 0.928, 0.828]
  - track 17 at frame 171: holes 0, rim-vs-core 0.38, rim-vs-outside 0.40, heterogeneity 0.11; core [0.947, 0.896, 0.955, 0.924] rim [0.749, 0.632, 0.893, 0.751]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 48 components >= 12 px at frames [34, 67, 101, 133, 166, 200]):
  - radial phi (droplet): peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.825, rim/outside 3.84 (aggregate of 48 individuals; 3/48 membrane-like individually; rim level 0.63)
  - radial order |Q|: peak at rho=0.25 (OUTSIDE the peak band 0.5-1.5), rim/core 0.854, rim/outside 5.55 (aggregate of 48 individuals; 3/48 membrane-like individually; rim level 0.559)
  - radial shell s: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.93, rim/outside 1.45 (aggregate of 48 individuals; 0/48 membrane-like individually; rim level 0.861)
  - radial fuel f: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.863, rim/outside 2.55 (aggregate of 48 individuals; 1/48 membrane-like individually; rim level 0.71)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #1 (t=320, R_eq 5.2): none; #3 (t=370, R_eq 6.13, ring): ['phi (droplet)', 'order |Q|']; #4 (t=370, R_eq 4.33): none; #17 (t=855, R_eq 4.79): none

## Warnings
- radial: 7 of 48 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
