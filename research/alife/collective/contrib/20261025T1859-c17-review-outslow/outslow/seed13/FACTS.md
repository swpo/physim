# Evidence pack: nematic-fuelcell-outslow (seed 13)

- world: `../../world.py`, family `active-nematic`
- parent: None; mutation: new class: CH droplets with internal Landau-de Gennes nematic order and extensile active stress, Brinkman-Stokes flow
- run: 201 frames x 100 steps x dt 0.05 = time 1000; grid [128, 128]; wall 399s; status ok
- command: `python -m labkit.run world.py --out outslow/seed13 --seeds 13 --no-movie`
- segmentation: matter > 0.56 of robust range [-0.86, 0.6842], min area 6 px

## Measurements
- components: final 22, mean 11.9, max 22; occupancy final 0.09
- tracks: 40; persistent (alive >= 50% of run): 9; longest 173 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 17.45 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [30, 25, 22], H1 [1, 0, 0]
- motion: 13 long-lived tracks moved >= 1 body length; max speed 0.0572/time; max body lengths 3.6
- replication (lineage window K = 20 frames = time 100, default): splits 16, persistent splits 11 (0 more failed only because the siblings re-merged within K), max generation 4, merges 1, merge/split ratio 0.062, nucleations 7
- channel total drift (end/start - 1): [-0.5021, -0.1887, None, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 5 at frame 114: holes 0, rim-vs-core 0.43, rim-vs-outside 0.36, heterogeneity 0.11; core [0.947, 0.918, 0.888, 0.877] rim [0.711, 0.583, 0.808, 0.778]
  - track 6 at frame 118: holes 0, rim-vs-core 0.36, rim-vs-outside 0.34, heterogeneity 0.11; core [0.939, 0.749, 0.962, 0.978] rim [0.712, 0.497, 0.876, 0.903]
  - track 7 at frame 123: holes 0, rim-vs-core 0.31, rim-vs-outside 0.35, heterogeneity 0.10; core [0.902, 0.738, 0.953, 0.879] rim [0.702, 0.517, 0.883, 0.807]
  - track 25 at frame 176: holes 0, rim-vs-core 0.41, rim-vs-outside 0.42, heterogeneity 0.10; core [0.973, 0.963, 0.909, 0.923] rim [0.744, 0.647, 0.829, 0.825]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 83 components >= 12 px at frames [34, 67, 101, 133, 166, 200]):
  - radial phi (droplet): peak at rho=0.25 (OUTSIDE the peak band 0.5-1.5), rim/core 0.809, rim/outside 4.36 (aggregate of 83 individuals; 5/83 membrane-like individually; rim level 0.644)
  - radial order |Q|: peak at rho=0.25 (OUTSIDE the peak band 0.5-1.5), rim/core 0.812, rim/outside 6.65 (aggregate of 83 individuals; 4/83 membrane-like individually; rim level 0.555)
  - radial shell s: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.916, rim/outside 1.51 (aggregate of 83 individuals; 0/83 membrane-like individually; rim level 0.848)
  - radial fuel f: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.916, rim/outside 1.99 (aggregate of 83 individuals; 0/83 membrane-like individually; rim level 0.816)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #5 (t=570, R_eq 3.61): none; #6 (t=590, R_eq 4.44): none; #7 (t=615, R_eq 6): none; #25 (t=880, R_eq 3.43): none

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 8 of 83 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
