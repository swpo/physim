# Evidence pack: nematic-fuelcell (seed 0)

- world: `../../world.py`, family `active-nematic`
- parent: None; mutation: new class: CH droplets with internal Landau-de Gennes nematic order and extensile active stress, Brinkman-Stokes flow
- run: 201 frames x 100 steps x dt 0.05 = time 1000; grid [128, 128]; wall 676s; status ok
- command: `python -m labkit.run /root/w/world.py --out /root/w/z45/chis0_s0 --seeds 0 --no-movie`
- segmentation: matter > 0.55 of robust range [-0.8741, 0.7192], min area 6 px

## Measurements
- components: final 13, mean 10.1, max 13; occupancy final 0.10
- tracks: 25; persistent (alive >= 50% of run): 10; longest 182 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 36.14 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [23, 14, 13], H1 [0, 0, 0]
- motion: 9 long-lived tracks moved >= 1 body length; max speed 0.0418/time; max body lengths 3.2
- replication (lineage window K = 20 frames = time 100, default): splits 7, persistent splits 5 (0 more failed only because the siblings re-merged within K), max generation 2, merges 2, merge/split ratio 0.286, nucleations 9
- channel total drift (end/start - 1): [-0.5044, -0.0629, None, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 5 at frame 111: holes 0, rim-vs-core 0.31, rim-vs-outside 0.65, heterogeneity 0.10; core [0.966, 0.907, 0.971, 0.954] rim [0.793, 0.664, 0.926, 0.886]
  - track 8 at frame 114: holes 0, rim-vs-core 0.27, rim-vs-outside 0.62, heterogeneity 0.10; core [0.946, 0.855, 0.964, 0.926] rim [0.792, 0.644, 0.919, 0.871]
  - track 6 at frame 99: holes 0, rim-vs-core 0.25, rim-vs-outside 0.63, heterogeneity 0.09; core [0.939, 0.842, 0.975, 0.928] rim [0.793, 0.663, 0.919, 0.862]
  - track 15 at frame 175: holes 0, rim-vs-core 0.44, rim-vs-outside 0.41, heterogeneity 0.12; core [0.949, 0.923, 0.907, 0.958] rim [0.7, 0.59, 0.812, 0.852]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 67 components >= 12 px at frames [34, 67, 101, 133, 166, 200]):
  - radial phi (droplet): peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.784, rim/outside 3.79 (aggregate of 67 individuals; 4/67 membrane-like individually; rim level 0.572)
  - radial order |Q|: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.772, rim/outside 5.42 (aggregate of 67 individuals; 5/67 membrane-like individually; rim level 0.483)
  - radial shell s: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.903, rim/outside 1.54 (aggregate of 67 individuals; 0/67 membrane-like individually; rim level 0.816)
  - radial fuel f: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.916, rim/outside 1.52 (aggregate of 67 individuals; 0/67 membrane-like individually; rim level 0.813)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #5 (t=555, R_eq 7.48): none; #8 (t=570, R_eq 6.56, ring): none; #6 (t=495, R_eq 7.57): none; #15 (t=875, R_eq 4.3): none

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 13 of 67 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
