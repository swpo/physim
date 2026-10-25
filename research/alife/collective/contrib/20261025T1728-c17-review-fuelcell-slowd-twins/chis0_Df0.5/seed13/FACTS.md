# Evidence pack: nematic-fuelcell (seed 13)

- world: `../../world.py`, family `active-nematic`
- parent: None; mutation: new class: CH droplets with internal Landau-de Gennes nematic order and extensile active stress, Brinkman-Stokes flow
- run: 201 frames x 100 steps x dt 0.05 = time 1000; grid [128, 128]; wall 390s; status ok
- command: `python -m labkit.run collective/contrib/c17-twins-wip/world.py --out collective/contrib/c17-twins-wip/chis0_Df0.5/seed13 --seeds 13 --no-movie`
- segmentation: matter > 0.56 of robust range [-0.8563, 0.6624], min area 6 px

## Measurements
- components: final 19, mean 11.3, max 19; occupancy final 0.09
- tracks: 40; persistent (alive >= 50% of run): 7; longest 173 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 20.00 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [26, 20, 19], H1 [1, 0, 0]
- motion: 14 long-lived tracks moved >= 1 body length; max speed 0.0482/time; max body lengths 3.1
- replication (lineage window K = 20 frames = time 100, default): splits 15, persistent splits 9 (0 more failed only because the siblings re-merged within K), max generation 3, merges 3, merge/split ratio 0.2, nucleations 7
- channel total drift (end/start - 1): [-0.5021, -0.2534, None, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 5 at frame 114: holes 0, rim-vs-core 0.41, rim-vs-outside 0.41, heterogeneity 0.11; core [0.969, 0.96, 0.885, 0.92] rim [0.761, 0.669, 0.815, 0.735]
  - track 6 at frame 118: holes 0, rim-vs-core 0.30, rim-vs-outside 0.33, heterogeneity 0.10; core [0.904, 0.701, 0.911, 0.866] rim [0.731, 0.494, 0.859, 0.753]
  - track 7 at frame 124: holes 0, rim-vs-core 0.29, rim-vs-outside 0.69, heterogeneity 0.11; core [0.96, 0.858, 0.961, 0.92] rim [0.795, 0.655, 0.911, 0.802]
  - track 25 at frame 175: holes 0, rim-vs-core 0.32, rim-vs-outside 0.38, heterogeneity 0.10; core [0.919, 0.756, 0.927, 0.86] rim [0.733, 0.537, 0.865, 0.727]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 77 components >= 12 px at frames [34, 67, 101, 133, 166, 200]):
  - radial phi (droplet): peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.877, rim/outside 4 (aggregate of 77 individuals; 8/77 membrane-like individually; rim level 0.647)
  - radial order |Q|: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.859, rim/outside 5.96 (aggregate of 77 individuals; 9/77 membrane-like individually; rim level 0.539)
  - radial shell s: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.934, rim/outside 1.48 (aggregate of 77 individuals; 0/77 membrane-like individually; rim level 0.841)
  - radial fuel f: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.891, rim/outside 2.21 (aggregate of 77 individuals; 0/77 membrane-like individually; rim level 0.721)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #5 (t=570, R_eq 3.34): none; #6 (t=590, R_eq 4.55): none; #7 (t=620, R_eq 6.05, ring): none; #25 (t=875, R_eq 4.82): none

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 15 of 77 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
