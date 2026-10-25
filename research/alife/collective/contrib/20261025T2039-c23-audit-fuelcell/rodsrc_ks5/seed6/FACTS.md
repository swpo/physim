# Evidence pack: nematic-fuelcell-rodsrc (seed 6)

- world: `../../world_rodsrc.py`, family `active-nematic`
- parent: None; mutation: new class: CH droplets with internal Landau-de Gennes nematic order and extensile active stress, Brinkman-Stokes flow
- run: 201 frames x 100 steps x dt 0.05 = time 1000; grid [128, 128]; wall 326s; status ok
- command: `python -m labkit.run collective/contrib/20261025T2039-c23-audit-fuelcell/world_rodsrc.py --out collective/contrib/20261025T2039-c23-audit-fuelcell/rodsrc_ks5/seed6 --seeds 6 --no-movie`
- segmentation: matter > 0.57 of robust range [-0.8683, 0.6616], min area 6 px

## Measurements
- components: final 15, mean 8.8, max 15; occupancy final 0.10
- tracks: 23; persistent (alive >= 50% of run): 6; longest 189 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 50.57 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [23, 16, 15], H1 [0, 0, 0]
- motion: 5 long-lived tracks moved >= 1 body length; max speed 0.0348/time; max body lengths 1.8
- replication (lineage window K = 20 frames = time 100, default): splits 8, persistent splits 4 (0 more failed only because the siblings re-merged within K), max generation 2, merges 0, merge/split ratio 0, nucleations 7
- channel total drift (end/start - 1): [-0.4995, -0.1585, None, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 1 at frame 106: holes 0, rim-vs-core 0.41, rim-vs-outside 0.71, heterogeneity 0.14; core [0.948, 0.827, 0.484, 0.922] rim [0.806, 0.62, 0.794, 0.809]
  - track 3 at frame 109: holes 0, rim-vs-core 0.51, rim-vs-outside 0.71, heterogeneity 0.14; core [0.976, 0.921, 0.416, 0.869] rim [0.801, 0.64, 0.782, 0.75]
  - track 6 at frame 116: holes 0, rim-vs-core 0.54, rim-vs-outside 0.41, heterogeneity 0.15; core [0.951, 0.931, 0.513, 0.845] rim [0.726, 0.613, 0.842, 0.673]
  - track 19 at frame 182: holes 0, rim-vs-core 0.54, rim-vs-outside 0.72, heterogeneity 0.15; core [0.986, 0.937, 0.396, 0.926] rim [0.813, 0.635, 0.783, 0.802]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 60 components >= 12 px at frames [34, 67, 101, 133, 166, 200]):
  - radial phi (droplet): peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.78, rim/outside 3.09 (aggregate of 60 individuals; 6/60 membrane-like individually; rim level 0.529)
  - radial order |Q|: peak at rho=0.25 (OUTSIDE the peak band 0.5-1.5), rim/core 0.761, rim/outside 4.34 (aggregate of 60 individuals; 7/60 membrane-like individually; rim level 0.434)
  - radial shell s: peak at rho=0.45 (OUTSIDE the peak band 0.5-1.5), rim/core 0.975, rim/outside 2.61 (aggregate of 60 individuals; 16/60 membrane-like individually; rim level 0.551)
  - radial fuel f: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.818, rim/outside 1.8 (aggregate of 60 individuals; 1/60 membrane-like individually; rim level 0.58)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #1 (t=530, R_eq 9.18, ring): ['phi (droplet)', 'order |Q|', 'shell s']; #3 (t=545, R_eq 6.79): none; #6 (t=580, R_eq 3.61): ['shell s']; #19 (t=910, R_eq 6.15): none

## Warnings
- radial: 16 of 60 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
