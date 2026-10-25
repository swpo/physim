# Evidence pack: nematic-fuelcell-outslow (seed 13)

- world: `../../world.py`, family `active-nematic`
- parent: None; mutation: new class: CH droplets with internal Landau-de Gennes nematic order and extensile active stress, Brinkman-Stokes flow
- run: 201 frames x 100 steps x dt 0.05 = time 1000; grid [128, 128]; wall 378s; status ok
- command: `python -m labkit.run world.py --out outslow03/seed13 --seeds 13 --no-movie`
- segmentation: matter > 0.56 of robust range [-0.866, 0.6927], min area 6 px

## Measurements
- components: final 22, mean 10.7, max 22; occupancy final 0.08
- tracks: 45; persistent (alive >= 50% of run): 7; longest 167 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 21.00 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [27, 22, 20], H1 [0, 0, 0]
- motion: 12 long-lived tracks moved >= 1 body length; max speed 0.0421/time; max body lengths 3.9
- replication (lineage window K = 20 frames = time 100, default): splits 18, persistent splits 9 (0 more failed only because the siblings re-merged within K), max generation 3, merges 2, merge/split ratio 0.111, nucleations 7
- channel total drift (end/start - 1): [-0.5021, -0.1431, None, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 6 at frame 118: holes 0, rim-vs-core 0.42, rim-vs-outside 0.41, heterogeneity 0.10; core [0.967, 0.956, 0.989, 1.0] rim [0.714, 0.629, 0.895, 0.981]
  - track 1 at frame 89: holes 0, rim-vs-core 0.31, rim-vs-outside 0.60, heterogeneity 0.09; core [0.954, 0.824, 0.975, 0.881] rim [0.786, 0.58, 0.929, 0.822]
  - track 7 at frame 121: holes 0, rim-vs-core 0.32, rim-vs-outside 0.35, heterogeneity 0.10; core [0.907, 0.789, 0.932, 0.858] rim [0.712, 0.559, 0.867, 0.789]
  - track 22 at frame 168: holes 0, rim-vs-core 0.36, rim-vs-outside 0.35, heterogeneity 0.10; core [0.902, 0.767, 0.9, 0.832] rim [0.682, 0.497, 0.833, 0.764]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 75 components >= 12 px at frames [34, 67, 101, 133, 166, 200]):
  - radial phi (droplet): peak at rho=0.25 (OUTSIDE the peak band 0.5-1.5), rim/core 0.809, rim/outside 4.14 (aggregate of 75 individuals; 6/75 membrane-like individually; rim level 0.619)
  - radial order |Q|: peak at rho=0.25 (OUTSIDE the peak band 0.5-1.5), rim/core 0.794, rim/outside 6.44 (aggregate of 75 individuals; 6/75 membrane-like individually; rim level 0.531)
  - radial shell s: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.917, rim/outside 1.53 (aggregate of 75 individuals; 0/75 membrane-like individually; rim level 0.84)
  - radial fuel f: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.921, rim/outside 1.83 (aggregate of 75 individuals; 0/75 membrane-like individually; rim level 0.813)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #6 (t=590, R_eq 4.72): none; #1 (t=445, R_eq 6.33, ring): ['phi (droplet)', 'order |Q|']; #7 (t=605, R_eq 5.81): none; #22 (t=840, R_eq 4.92): none

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 12 of 75 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
