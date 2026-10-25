# Evidence pack: nematic-fuelcell (seed 23)

- world: `../../../20261025T1412-c15-nematic-fuelcell-claim/world.py`, family `active-nematic`
- parent: None; mutation: new class: CH droplets with internal Landau-de Gennes nematic order and extensile active stress, Brinkman-Stokes flow
- run: 201 frames x 100 steps x dt 0.05 = time 1000; grid [128, 128]; wall 353s; status ok
- command: `python -m labkit.run collective/contrib/20261025T1412-c15-nematic-fuelcell-claim/world.py --out collective/contrib/20261025T2030-c22-review-fuelring/controls/chis0_s23 --seeds 23 --no-movie`
- segmentation: matter > 0.55 of robust range [-0.8771, 0.7207], min area 6 px

## Measurements
- components: final 18, mean 12.7, max 18; occupancy final 0.11
- tracks: 34; persistent (alive >= 50% of run): 9; longest 192 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 28.62 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [26, 18, 17], H1 [0, 0, 0]
- motion: 13 long-lived tracks moved >= 1 body length; max speed 0.0417/time; max body lengths 2.7
- replication (lineage window K = 20 frames = time 100, default): splits 11, persistent splits 3 (0 more failed only because the siblings re-merged within K), max generation 1, merges 2, merge/split ratio 0.182, nucleations 10
- channel total drift (end/start - 1): [-0.4914, 0.1132, None, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 1 at frame 106: holes 0, rim-vs-core 0.26, rim-vs-outside 0.61, heterogeneity 0.09; core [0.941, 0.825, 0.971, 0.917] rim [0.787, 0.621, 0.934, 0.868]
  - track 6 at frame 106: holes 0, rim-vs-core 0.35, rim-vs-outside 0.36, heterogeneity 0.10; core [0.911, 0.809, 0.931, 0.851] rim [0.707, 0.543, 0.864, 0.769]
  - track 8 at frame 111: holes 0, rim-vs-core 0.38, rim-vs-outside 0.34, heterogeneity 0.12; core [0.949, 0.689, 0.979, 0.995] rim [0.68, 0.452, 0.876, 0.944]
  - track 24 at frame 166: holes 0, rim-vs-core 0.38, rim-vs-outside 0.35, heterogeneity 0.11; core [0.923, 0.803, 0.968, 0.973] rim [0.695, 0.523, 0.885, 0.89]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 83 components >= 12 px at frames [34, 67, 101, 133, 166, 200]):
  - radial phi (droplet): peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.788, rim/outside 3.43 (aggregate of 83 individuals; 10/83 membrane-like individually; rim level 0.539)
  - radial order |Q|: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.774, rim/outside 4.8 (aggregate of 83 individuals; 11/83 membrane-like individually; rim level 0.46)
  - radial shell s: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.912, rim/outside 1.55 (aggregate of 83 individuals; 0/83 membrane-like individually; rim level 0.807)
  - radial fuel f: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.923, rim/outside 1.49 (aggregate of 83 individuals; 0/83 membrane-like individually; rim level 0.811)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #1 (t=530, R_eq 7.46, ring): ['phi (droplet)', 'order |Q|']; #6 (t=530, R_eq 5.08): none; #8 (t=555, R_eq 4.72): ['order |Q|']; #24 (t=830, R_eq 5.32): none

## Warnings
- radial: 21 of 83 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
