# Evidence pack: nematic-fuelcell (seed 24)

- world: `../../../20261025T1412-c15-nematic-fuelcell-claim/world.py`, family `active-nematic`
- parent: None; mutation: new class: CH droplets with internal Landau-de Gennes nematic order and extensile active stress, Brinkman-Stokes flow
- run: 201 frames x 100 steps x dt 0.05 = time 1000; grid [128, 128]; wall 638s; status ok
- command: `python -m labkit.run collective/contrib/20261025T1412-c15-nematic-fuelcell-claim/world.py --out collective/contrib/20261025T1834-c24-review-fuelring/chis0/seed24 --seeds 24 --no-movie`
- segmentation: matter > 0.56 of robust range [-0.8751, 0.6979], min area 6 px

## Measurements
- components: final 14, mean 7.3, max 14; occupancy final 0.09
- tracks: 22; persistent (alive >= 50% of run): 5; longest 193 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 62.67 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [21, 14, 14], H1 [1, 0, 0]
- motion: 4 long-lived tracks moved >= 1 body length; max speed 0.032/time; max body lengths 1.6
- replication (lineage window K = 20 frames = time 100, default): splits 8, persistent splits 5 (0 more failed only because the siblings re-merged within K), max generation 2, merges 0, merge/split ratio 0, nucleations 6
- channel total drift (end/start - 1): [-0.5028, -0.1086, None, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 0 at frame 104: holes 0, rim-vs-core 0.35, rim-vs-outside 0.66, heterogeneity 0.10; core [0.98, 0.948, 0.951, 0.949] rim [0.799, 0.67, 0.905, 0.863]
  - track 5 at frame 114: holes 0, rim-vs-core 0.27, rim-vs-outside 0.66, heterogeneity 0.10; core [0.958, 0.863, 0.971, 0.928] rim [0.804, 0.662, 0.918, 0.859]
  - track 4 at frame 96: holes 0, rim-vs-core 0.26, rim-vs-outside 0.62, heterogeneity 0.09; core [0.944, 0.843, 0.969, 0.942] rim [0.793, 0.653, 0.911, 0.879]
  - track 13 at frame 171: holes 0, rim-vs-core 0.33, rim-vs-outside 0.45, heterogeneity 0.11; core [0.941, 0.868, 0.95, 0.953] rim [0.749, 0.619, 0.883, 0.885]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 50 components >= 12 px at frames [34, 67, 101, 133, 166, 200]):
  - radial phi (droplet): peak at rho=0.25 (OUTSIDE the peak band 0.5-1.5), rim/core 0.83, rim/outside 3.11 (aggregate of 50 individuals; 9/50 membrane-like individually; rim level 0.516)
  - radial order |Q|: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.794, rim/outside 4.12 (aggregate of 50 individuals; 9/50 membrane-like individually; rim level 0.425)
  - radial shell s: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.925, rim/outside 1.51 (aggregate of 50 individuals; 0/50 membrane-like individually; rim level 0.798)
  - radial fuel f: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.924, rim/outside 1.53 (aggregate of 50 individuals; 0/50 membrane-like individually; rim level 0.805)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #0 (t=520, R_eq 7.02, ring): none; #5 (t=570, R_eq 7.57, ring): ['phi (droplet)', 'order |Q|']; #4 (t=480, R_eq 7.8): none; #13 (t=855, R_eq 5.17): none

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 19 of 50 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
