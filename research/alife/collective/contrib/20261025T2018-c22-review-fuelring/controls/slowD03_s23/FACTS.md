# Evidence pack: nematic-fuelcell (seed 23)

- world: `../../../20261025T1412-c15-nematic-fuelcell-claim/world.py`, family `active-nematic`
- parent: None; mutation: new class: CH droplets with internal Landau-de Gennes nematic order and extensile active stress, Brinkman-Stokes flow
- run: 201 frames x 100 steps x dt 0.05 = time 1000; grid [128, 128]; wall 377s; status ok
- command: `python -m labkit.run collective/contrib/20261025T1412-c15-nematic-fuelcell-claim/world.py --out collective/contrib/20261025T2030-c22-review-fuelring/controls/slowD03_s23 --seeds 23 --no-movie`
- segmentation: matter > 0.57 of robust range [-0.8546, 0.6576], min area 6 px

## Measurements
- components: final 29, mean 17.3, max 30; occupancy final 0.09
- tracks: 62; persistent (alive >= 50% of run): 10; longest 175 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 29.75 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [34, 30, 29], H1 [0, 0, 0]
- motion: 22 long-lived tracks moved >= 1 body length; max speed 0.0536/time; max body lengths 3.1
- replication (lineage window K = 20 frames = time 100, default): splits 25, persistent splits 13 (0 more failed only because the siblings re-merged within K), max generation 2, merges 2, merge/split ratio 0.08, nucleations 10
- channel total drift (end/start - 1): [-0.4914, -0.1924, None, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 11 at frame 114: holes 0, rim-vs-core 0.37, rim-vs-outside 0.36, heterogeneity 0.11; core [0.912, 0.799, 0.928, 0.85] rim [0.724, 0.538, 0.87, 0.684]
  - track 13 at frame 126: holes 0, rim-vs-core 0.49, rim-vs-outside 0.40, heterogeneity 0.13; core [0.954, 0.928, 0.851, 0.86] rim [0.71, 0.578, 0.775, 0.622]
  - track 9 at frame 92: holes 0, rim-vs-core 0.32, rim-vs-outside 0.44, heterogeneity 0.10; core [0.924, 0.833, 0.951, 0.853] rim [0.763, 0.604, 0.899, 0.706]
  - track 21 at frame 143: holes 0, rim-vs-core 0.46, rim-vs-outside 0.40, heterogeneity 0.12; core [0.95, 0.932, 0.895, 0.882] rim [0.725, 0.61, 0.825, 0.659]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 119 components >= 12 px at frames [34, 67, 101, 133, 166, 200]):
  - radial phi (droplet): peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.798, rim/outside 4.24 (aggregate of 119 individuals; 2/119 membrane-like individually; rim level 0.668)
  - radial order |Q|: peak at rho=0.25 (OUTSIDE the peak band 0.5-1.5), rim/core 0.806, rim/outside 6.91 (aggregate of 119 individuals; 2/119 membrane-like individually; rim level 0.57)
  - radial shell s: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.921, rim/outside 1.46 (aggregate of 119 individuals; 0/119 membrane-like individually; rim level 0.854)
  - radial fuel f: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.826, rim/outside 2.58 (aggregate of 119 individuals; 2/119 membrane-like individually; rim level 0.694)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #11 (t=570, R_eq 5.05): none; #13 (t=630, R_eq 3.19): none; #9 (t=460, R_eq 4.15): none; #21 (t=715, R_eq 3.24): none

## Warnings
- radial: 6 of 119 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
