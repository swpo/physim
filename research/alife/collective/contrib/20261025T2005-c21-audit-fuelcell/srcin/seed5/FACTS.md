# Evidence pack: nematic-fuelcell-srcin (seed 5)

- world: `../../world_srcin.py`, family `active-nematic`
- parent: None; mutation: new class: CH droplets with internal Landau-de Gennes nematic order and extensile active stress, Brinkman-Stokes flow
- run: 201 frames x 100 steps x dt 0.05 = time 1000; grid [128, 128]; wall 500s; status ok
- command: `python -m labkit.run collective/contrib/20261025T2005-c21-audit-fuelcell/world_srcin.py --out collective/contrib/20261025T2005-c21-audit-fuelcell/srcin --seeds 5 6 --no-movie`
- segmentation: matter > 0.55 of robust range [-0.8769, 0.7188], min area 6 px

## Measurements
- components: final 19, mean 12.3, max 19; occupancy final 0.10
- tracks: 33; persistent (alive >= 50% of run): 10; longest 188 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 50.33 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [28, 20, 19], H1 [0, 0, 0]
- motion: 9 long-lived tracks moved >= 1 body length; max speed 0.0365/time; max body lengths 2.7
- replication (lineage window K = 20 frames = time 100, default): splits 11, persistent splits 8 (0 more failed only because the siblings re-merged within K), max generation 2, merges 1, merge/split ratio 0.091, nucleations 10
- channel total drift (end/start - 1): [-0.5101, 0.044, None, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 1 at frame 108: holes 0, rim-vs-core 0.49, rim-vs-outside 0.63, heterogeneity 0.13; core [0.961, 0.883, 0.369, 0.922] rim [0.784, 0.635, 0.744, 0.85]
  - track 2 at frame 108: holes 0, rim-vs-core 0.47, rim-vs-outside 0.34, heterogeneity 0.14; core [0.907, 0.808, 0.514, 0.886] rim [0.701, 0.551, 0.833, 0.801]
  - track 8 at frame 113: holes 0, rim-vs-core 0.45, rim-vs-outside 0.33, heterogeneity 0.13; core [0.9, 0.795, 0.504, 0.874] rim [0.694, 0.54, 0.8, 0.797]
  - track 20 at frame 171: holes 0, rim-vs-core 0.55, rim-vs-outside 0.35, heterogeneity 0.16; core [0.932, 0.886, 0.503, 0.952] rim [0.694, 0.56, 0.868, 0.844]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 84 components >= 12 px at frames [34, 67, 101, 133, 166, 200]):
  - radial phi (droplet): peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.757, rim/outside 3.78 (aggregate of 84 individuals; 6/84 membrane-like individually; rim level 0.571)
  - radial order |Q|: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.75, rim/outside 5.58 (aggregate of 84 individuals; 6/84 membrane-like individually; rim level 0.487)
  - radial shell s: peak at rho=0.55 (in the peak band 0.5-1.5), rim/core 1.01, rim/outside 2.96 (aggregate of 84 individuals; 30/84 membrane-like individually; rim level 0.559)
  - radial fuel f: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.918, rim/outside 1.51 (aggregate of 84 individuals; 0/84 membrane-like individually; rim level 0.818)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #1 (t=540, R_eq 6.23, ring): none; #2 (t=540, R_eq 5.38): none; #8 (t=565, R_eq 4.69): none; #20 (t=855, R_eq 4.3): ['shell s']

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 12 of 84 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
