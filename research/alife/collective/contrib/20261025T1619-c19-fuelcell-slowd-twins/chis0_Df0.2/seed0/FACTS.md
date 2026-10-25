# Evidence pack: nematic-fuelcell (seed 0)

- world: `../../../20261025T1412-c15-nematic-fuelcell-claim/world.py`, family `active-nematic`
- parent: None; mutation: new class: CH droplets with internal Landau-de Gennes nematic order and extensile active stress, Brinkman-Stokes flow
- run: 201 frames x 100 steps x dt 0.05 = time 1000; grid [128, 128]; wall 512s; status ok
- command: `python -m labkit.run collective/contrib/20261025T1412-c15-nematic-fuelcell-claim/world.py --out collective/contrib/20261025T1619-c19-fuelcell-slowd-twins/chis0_Df0.2/seed0 --seeds 0 --no-movie`
- segmentation: matter > 0.57 of robust range [-0.8489, 0.6414], min area 6 px

## Measurements
- components: final 25, mean 11.9, max 25; occupancy final 0.07
- tracks: 55; persistent (alive >= 50% of run): 10; longest 188 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 26.75 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [29, 25, 22], H1 [0, 0, 0]
- motion: 9 long-lived tracks moved >= 1 body length; max speed 0.0452/time; max body lengths 2.3
- replication (lineage window K = 20 frames = time 100, default): splits 21, persistent splits 8 (0 more failed only because the siblings re-merged within K), max generation 3, merges 4, merge/split ratio 0.19, nucleations 9
- channel total drift (end/start - 1): [-0.5044, -0.3475, None, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 1 at frame 108: holes 0, rim-vs-core 0.31, rim-vs-outside 0.37, heterogeneity 0.10; core [0.905, 0.706, 0.939, 0.843] rim [0.732, 0.512, 0.888, 0.689]
  - track 5 at frame 92: holes 0, rim-vs-core 0.35, rim-vs-outside 0.68, heterogeneity 0.10; core [0.981, 0.863, 0.967, 0.956] rim [0.814, 0.612, 0.928, 0.782]
  - track 3 at frame 87: holes 0, rim-vs-core 0.33, rim-vs-outside 0.38, heterogeneity 0.10; core [0.931, 0.727, 0.974, 0.901] rim [0.748, 0.518, 0.919, 0.725]
  - track 24 at frame 175: holes 0, rim-vs-core 0.46, rim-vs-outside 0.40, heterogeneity 0.12; core [0.969, 0.917, 0.854, 0.832] rim [0.75, 0.586, 0.793, 0.604]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 86 components >= 12 px at frames [34, 67, 101, 133, 166, 200]):
  - radial phi (droplet): peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.778, rim/outside 3.8 (aggregate of 86 individuals; 2/86 membrane-like individually; rim level 0.635)
  - radial order |Q|: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.797, rim/outside 5.45 (aggregate of 86 individuals; 2/86 membrane-like individually; rim level 0.524)
  - radial shell s: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.912, rim/outside 1.45 (aggregate of 86 individuals; 0/86 membrane-like individually; rim level 0.851)
  - radial fuel f: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.781, rim/outside 2.72 (aggregate of 86 individuals; 1/86 membrane-like individually; rim level 0.64)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #1 (t=540, R_eq 5.26): none; #5 (t=460, R_eq 6.51): none; #3 (t=435, R_eq 4.72): none; #24 (t=875, R_eq 2.82): none

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 11 of 86 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
