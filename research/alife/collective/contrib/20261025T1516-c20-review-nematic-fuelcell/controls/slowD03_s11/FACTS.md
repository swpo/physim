# Evidence pack: nematic-fuelcell (seed 11)

- world: `../world.py`, family `active-nematic`
- parent: None; mutation: new class: CH droplets with internal Landau-de Gennes nematic order and extensile active stress, Brinkman-Stokes flow
- run: 201 frames x 100 steps x dt 0.05 = time 1000; grid [128, 128]; wall 683s; status ok
- command: `python -m labkit.run /tmp/c20rev/world.py --out /tmp/c20rev/slowD03_s11 --seeds 11 --no-movie`
- segmentation: matter > 0.57 of robust range [-0.857, 0.6412], min area 6 px

## Measurements
- components: final 25, mean 13.9, max 25; occupancy final 0.09
- tracks: 51; persistent (alive >= 50% of run): 8; longest 172 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 30.29 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [31, 26, 25], H1 [0, 0, 0]
- motion: 9 long-lived tracks moved >= 1 body length; max speed 0.0533/time; max body lengths 2.6
- replication (lineage window K = 20 frames = time 100, default): splits 20, persistent splits 15 (0 more failed only because the siblings re-merged within K), max generation 3, merges 1, merge/split ratio 0.05, nucleations 10
- channel total drift (end/start - 1): [-0.5045, -0.2093, None, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 10 at frame 114: holes 0, rim-vs-core 0.45, rim-vs-outside 0.45, heterogeneity 0.12; core [0.984, 0.922, 0.996, 0.997] rim [0.755, 0.57, 0.923, 0.865]
  - track 8 at frame 103: holes 0, rim-vs-core 0.32, rim-vs-outside 0.38, heterogeneity 0.10; core [0.926, 0.805, 0.941, 0.865] rim [0.754, 0.586, 0.886, 0.717]
  - track 11 at frame 109: holes 0, rim-vs-core 0.41, rim-vs-outside 0.40, heterogeneity 0.11; core [0.938, 0.919, 0.911, 0.881] rim [0.735, 0.621, 0.844, 0.688]
  - track 32 at frame 176: holes 0, rim-vs-core 0.46, rim-vs-outside 0.42, heterogeneity 0.12; core [0.974, 0.976, 0.868, 0.914] rim [0.75, 0.663, 0.793, 0.667]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 95 components >= 12 px at frames [34, 67, 101, 133, 166, 200]):
  - radial phi (droplet): peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.835, rim/outside 3.73 (aggregate of 95 individuals; 6/95 membrane-like individually; rim level 0.614)
  - radial order |Q|: peak at rho=0.25 (OUTSIDE the peak band 0.5-1.5), rim/core 0.857, rim/outside 5.46 (aggregate of 95 individuals; 8/95 membrane-like individually; rim level 0.509)
  - radial shell s: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.928, rim/outside 1.47 (aggregate of 95 individuals; 0/95 membrane-like individually; rim level 0.834)
  - radial fuel f: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.854, rim/outside 2.52 (aggregate of 95 individuals; 2/95 membrane-like individually; rim level 0.668)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #10 (t=570, R_eq 4.37): none; #8 (t=515, R_eq 4.55): none; #11 (t=545, R_eq 4.07): none; #32 (t=880, R_eq 3.34): none

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 18 of 95 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
