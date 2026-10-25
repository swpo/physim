# Evidence pack: nematic-fuelcell (seed 11)

- world: `../world.py`, family `active-nematic`
- parent: None; mutation: new class: CH droplets with internal Landau-de Gennes nematic order and extensile active stress, Brinkman-Stokes flow
- run: 201 frames x 100 steps x dt 0.05 = time 1000; grid [128, 128]; wall 672s; status ok
- command: `python -m labkit.run /tmp/c20rev/world.py --out /tmp/c20rev/chis0_s11 --seeds 11 --no-movie`
- segmentation: matter > 0.55 of robust range [-0.8768, 0.7123], min area 6 px

## Measurements
- components: final 20, mean 11.0, max 20; occupancy final 0.11
- tracks: 33; persistent (alive >= 50% of run): 8; longest 187 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 53.57 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [27, 21, 20], H1 [1, 0, 0]
- motion: 7 long-lived tracks moved >= 1 body length; max speed 0.0433/time; max body lengths 1.6
- replication (lineage window K = 20 frames = time 100, default): splits 12, persistent splits 10 (0 more failed only because the siblings re-merged within K), max generation 3, merges 0, merge/split ratio 0, nucleations 9
- channel total drift (end/start - 1): [-0.5045, 0.054, None, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 5 at frame 108: holes 0, rim-vs-core 0.37, rim-vs-outside 0.62, heterogeneity 0.10; core [0.972, 0.913, 0.921, 0.926] rim [0.779, 0.611, 0.876, 0.863]
  - track 6 at frame 97: holes 0, rim-vs-core 0.30, rim-vs-outside 0.62, heterogeneity 0.10; core [0.949, 0.848, 0.952, 0.913] rim [0.784, 0.609, 0.899, 0.841]
  - track 1 at frame 77: holes 0, rim-vs-core 0.29, rim-vs-outside 0.63, heterogeneity 0.10; core [0.955, 0.852, 0.961, 0.921] rim [0.785, 0.628, 0.911, 0.859]
  - track 25 at frame 188: holes 0, rim-vs-core 0.39, rim-vs-outside 0.40, heterogeneity 0.11; core [0.943, 0.923, 0.956, 0.989] rim [0.718, 0.624, 0.868, 0.939]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 74 components >= 12 px at frames [34, 67, 101, 133, 166, 200]):
  - radial phi (droplet): peak at rho=0.25 (OUTSIDE the peak band 0.5-1.5), rim/core 0.789, rim/outside 3.39 (aggregate of 74 individuals; 10/74 membrane-like individually; rim level 0.539)
  - radial order |Q|: peak at rho=0.25 (OUTSIDE the peak band 0.5-1.5), rim/core 0.793, rim/outside 4.78 (aggregate of 74 individuals; 10/74 membrane-like individually; rim level 0.459)
  - radial shell s: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.907, rim/outside 1.54 (aggregate of 74 individuals; 0/74 membrane-like individually; rim level 0.801)
  - radial fuel f: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.919, rim/outside 1.5 (aggregate of 74 individuals; 0/74 membrane-like individually; rim level 0.813)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #5 (t=540, R_eq 6.21): none; #6 (t=485, R_eq 7.63, ring): ['phi (droplet)', 'order |Q|']; #1 (t=385, R_eq 7.05, ring): none; #25 (t=940, R_eq 4.75): none

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 18 of 74 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
