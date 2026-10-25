# Evidence pack: nematic-fuelcell (seed 6)

- world: `../../../20261025T1412-c15-nematic-fuelcell-claim/world.py`, family `active-nematic`
- parent: None; mutation: new class: CH droplets with internal Landau-de Gennes nematic order and extensile active stress, Brinkman-Stokes flow
- run: 201 frames x 100 steps x dt 0.05 = time 1000; grid [128, 128]; wall 491s; status ok
- command: `python -m labkit.run collective/contrib/20261025T1412-c15-nematic-fuelcell-claim/world.py --out collective/contrib/20261025T2005-c21-audit-fuelcell/rerun --seeds 5 6 --no-movie`
- segmentation: matter > 0.57 of robust range [-0.8542, 0.6415], min area 6 px

## Measurements
- components: final 24, mean 11.8, max 25; occupancy final 0.09
- tracks: 47; persistent (alive >= 50% of run): 6; longest 184 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 42.71 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [26, 24, 24], H1 [0, 0, 0]
- motion: 7 long-lived tracks moved >= 1 body length; max speed 0.0592/time; max body lengths 3.5
- replication (lineage window K = 20 frames = time 100, default): splits 19, persistent splits 12 (0 more failed only because the siblings re-merged within K), max generation 3, merges 2, merge/split ratio 0.105, nucleations 7
- channel total drift (end/start - 1): [-0.4995, -0.2103, None, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 3 at frame 109: holes 0, rim-vs-core 0.60, rim-vs-outside 0.71, heterogeneity 0.16; core [0.993, 0.948, 0.28, 0.802] rim [0.802, 0.594, 0.723, 0.727]
  - track 6 at frame 116: holes 0, rim-vs-core 0.55, rim-vs-outside 0.41, heterogeneity 0.15; core [0.945, 0.91, 0.415, 0.749] rim [0.731, 0.599, 0.791, 0.618]
  - track 1 at frame 89: holes 0, rim-vs-core 0.45, rim-vs-outside 0.74, heterogeneity 0.15; core [0.949, 0.807, 0.394, 0.881] rim [0.803, 0.567, 0.737, 0.779]
  - track 33 at frame 190: holes 0, rim-vs-core 0.57, rim-vs-outside 0.47, heterogeneity 0.17; core [0.961, 0.94, 0.373, 0.791] rim [0.754, 0.669, 0.801, 0.64]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 83 components >= 12 px at frames [34, 67, 101, 133, 166, 200]):
  - radial phi (droplet): peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.792, rim/outside 3.96 (aggregate of 83 individuals; 4/83 membrane-like individually; rim level 0.629)
  - radial order |Q|: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.78, rim/outside 6.18 (aggregate of 83 individuals; 3/83 membrane-like individually; rim level 0.537)
  - radial shell s: peak at rho=0.55 (in the peak band 0.5-1.5), rim/core 1.17, rim/outside 2.2 (aggregate of 83 individuals; 38/83 membrane-like individually; rim level 0.58)
  - radial fuel f: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.788, rim/outside 2.42 (aggregate of 83 individuals; 4/83 membrane-like individually; rim level 0.545)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #3 (t=545, R_eq 6.46): none; #6 (t=580, R_eq 3.83): ['shell s']; #1 (t=445, R_eq 8.02, ring): ['phi (droplet)', 'shell s', 'fuel f']; #33 (t=950, R_eq 3.78): ['shell s']

## Warnings
- radial: 12 of 83 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
