# Evidence pack: nematic-fuelcell-rodsrc (seed 5)

- world: `../../world_rodsrc.py`, family `active-nematic`
- parent: None; mutation: new class: CH droplets with internal Landau-de Gennes nematic order and extensile active stress, Brinkman-Stokes flow
- run: 201 frames x 100 steps x dt 0.05 = time 1000; grid [128, 128]; wall 325s; status ok
- command: `python -m labkit.run collective/contrib/20261025T2039-c23-audit-fuelcell/world_rodsrc.py --out collective/contrib/20261025T2039-c23-audit-fuelcell/rodsrc_ks5/seed5 --seeds 5 --no-movie`
- segmentation: matter > 0.56 of robust range [-0.8661, 0.6772], min area 6 px

## Measurements
- components: final 22, mean 13.8, max 23; occupancy final 0.10
- tracks: 39; persistent (alive >= 50% of run): 9; longest 188 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 42.14 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [30, 23, 22], H1 [0, 0, 0]
- motion: 14 long-lived tracks moved >= 1 body length; max speed 0.0435/time; max body lengths 2.0
- replication (lineage window K = 20 frames = time 100, default): splits 14, persistent splits 11 (0 more failed only because the siblings re-merged within K), max generation 2, merges 1, merge/split ratio 0.071, nucleations 10
- channel total drift (end/start - 1): [-0.5101, -0.0542, None, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 1 at frame 108: holes 0, rim-vs-core 0.43, rim-vs-outside 0.39, heterogeneity 0.14; core [0.894, 0.715, 0.605, 0.808] rim [0.707, 0.508, 0.895, 0.648]
  - track 5 at frame 109: holes 0, rim-vs-core 0.44, rim-vs-outside 0.41, heterogeneity 0.14; core [0.903, 0.757, 0.593, 0.879] rim [0.732, 0.553, 0.898, 0.713]
  - track 8 at frame 113: holes 0, rim-vs-core 0.45, rim-vs-outside 0.37, heterogeneity 0.14; core [0.9, 0.772, 0.572, 0.742] rim [0.699, 0.527, 0.859, 0.602]
  - track 20 at frame 161: holes 0, rim-vs-core 0.55, rim-vs-outside 0.42, heterogeneity 0.15; core [0.949, 0.917, 0.484, 0.851] rim [0.737, 0.619, 0.861, 0.704]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 94 components >= 12 px at frames [34, 67, 101, 133, 166, 200]):
  - radial phi (droplet): peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.775, rim/outside 3.96 (aggregate of 94 individuals; 4/94 membrane-like individually; rim level 0.6)
  - radial order |Q|: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.762, rim/outside 6.01 (aggregate of 94 individuals; 4/94 membrane-like individually; rim level 0.494)
  - radial shell s: peak at rho=0.45 (OUTSIDE the peak band 0.5-1.5), rim/core 1.02, rim/outside 3 (aggregate of 94 individuals; 29/94 membrane-like individually; rim level 0.623)
  - radial fuel f: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.797, rim/outside 1.93 (aggregate of 94 individuals; 2/94 membrane-like individually; rim level 0.594)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #1 (t=540, R_eq 5.89, ring): none; #5 (t=545, R_eq 6): none; #8 (t=565, R_eq 4.72): none; #20 (t=805, R_eq 3.43): ['shell s']

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 11 of 94 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
