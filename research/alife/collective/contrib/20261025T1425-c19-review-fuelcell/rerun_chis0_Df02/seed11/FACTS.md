# Evidence pack: nematic-fuelcell (seed 11)

- world: `../../../20261025T1412-c15-nematic-fuelcell-claim/world.py`, family `active-nematic`
- parent: None; mutation: new class: CH droplets with internal Landau-de Gennes nematic order and extensile active stress, Brinkman-Stokes flow
- run: 201 frames x 100 steps x dt 0.05 = time 1000; grid [128, 128]; wall 594s; status ok
- command: `python -m labkit.run collective/contrib/20261025T1412-c15-nematic-fuelcell-claim/world.py --out collective/contrib/20261025T1425-c19-review-fuelcell/rerun_chis0_Df02/seed11 --seeds 11 --no-movie`
- segmentation: matter > 0.56 of robust range [-0.8484, 0.6768], min area 6 px

## Measurements
- components: final 31, mean 16.3, max 31; occupancy final 0.08
- tracks: 65; persistent (alive >= 50% of run): 7; longest 174 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 32.57 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [35, 31, 31], H1 [0, 0, 0]
- motion: 13 long-lived tracks moved >= 1 body length; max speed 0.0603/time; max body lengths 2.9
- replication (lineage window K = 20 frames = time 100, default): splits 27, persistent splits 17 (0 more failed only because the siblings re-merged within K), max generation 4, merges 2, merge/split ratio 0.074, nucleations 9
- channel total drift (end/start - 1): [-0.5045, -0.2329, None, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 9 at frame 114: holes 0, rim-vs-core 0.35, rim-vs-outside 0.41, heterogeneity 0.13; core [0.964, 0.847, 0.985, 0.996] rim [0.741, 0.607, 0.91, 0.881]
  - track 10 at frame 114: holes 0, rim-vs-core 0.41, rim-vs-outside 0.41, heterogeneity 0.12; core [0.93, 0.894, 0.906, 0.861] rim [0.732, 0.609, 0.844, 0.66]
  - track 7 at frame 103: holes 0, rim-vs-core 0.34, rim-vs-outside 0.37, heterogeneity 0.10; core [0.911, 0.763, 0.94, 0.826] rim [0.726, 0.537, 0.881, 0.653]
  - track 44 at frame 168: holes 0, rim-vs-core 0.28, rim-vs-outside 0.61, heterogeneity 0.11; core [0.974, 0.994, 1.0, 0.991] rim [0.827, 0.777, 0.975, 0.883]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 112 components >= 12 px at frames [34, 67, 101, 133, 166, 200]):
  - radial phi (droplet): peak at rho=0.25 (OUTSIDE the peak band 0.5-1.5), rim/core 0.799, rim/outside 4.23 (aggregate of 112 individuals; 4/112 membrane-like individually; rim level 0.656)
  - radial order |Q|: peak at rho=0.25 (OUTSIDE the peak band 0.5-1.5), rim/core 0.779, rim/outside 6.54 (aggregate of 112 individuals; 5/112 membrane-like individually; rim level 0.54)
  - radial shell s: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.921, rim/outside 1.45 (aggregate of 112 individuals; 0/112 membrane-like individually; rim level 0.842)
  - radial fuel f: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.789, rim/outside 2.79 (aggregate of 112 individuals; 3/112 membrane-like individually; rim level 0.626)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #9 (t=570, R_eq 4.33): none; #10 (t=570, R_eq 3.95): none; #7 (t=515, R_eq 4.55): none; #44 (t=840, R_eq 4.51): none

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 11 of 112 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
