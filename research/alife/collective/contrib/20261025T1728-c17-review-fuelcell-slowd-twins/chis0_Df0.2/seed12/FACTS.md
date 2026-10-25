# Evidence pack: nematic-fuelcell (seed 12)

- world: `../../world.py`, family `active-nematic`
- parent: None; mutation: new class: CH droplets with internal Landau-de Gennes nematic order and extensile active stress, Brinkman-Stokes flow
- run: 201 frames x 100 steps x dt 0.05 = time 1000; grid [128, 128]; wall 386s; status ok
- command: `python -m labkit.run collective/contrib/c17-twins-wip/world.py --out collective/contrib/c17-twins-wip/chis0_Df0.2/seed12 --seeds 12 --no-movie`
- segmentation: matter > 0.56 of robust range [-0.8453, 0.667], min area 6 px

## Measurements
- components: final 24, mean 13.0, max 24; occupancy final 0.07
- tracks: 59; persistent (alive >= 50% of run): 5; longest 139 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 19.22 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [27, 24, 24], H1 [0, 0, 0]
- motion: 14 long-lived tracks moved >= 1 body length; max speed 0.0365/time; max body lengths 1.9
- replication (lineage window K = 20 frames = time 100, default): splits 25, persistent splits 13 (0 more failed only because the siblings re-merged within K), max generation 3, merges 2, merge/split ratio 0.08, nucleations 7
- channel total drift (end/start - 1): [-0.5083, -0.3514, None, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 6 at frame 94: holes 0, rim-vs-core 0.28, rim-vs-outside 0.66, heterogeneity 0.10; core [0.955, 0.782, 0.964, 0.915] rim [0.809, 0.599, 0.931, 0.774]
  - track 3 at frame 77: holes 0, rim-vs-core 0.32, rim-vs-outside 0.69, heterogeneity 0.10; core [0.969, 0.891, 0.974, 0.941] rim [0.813, 0.668, 0.934, 0.783]
  - track 27 at frame 165: holes 0, rim-vs-core 0.44, rim-vs-outside 0.44, heterogeneity 0.13; core [0.949, 0.936, 0.918, 0.891] rim [0.738, 0.645, 0.854, 0.647]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 91 components >= 12 px at frames [34, 67, 101, 133, 166, 200]):
  - radial phi (droplet): peak at rho=0.25 (OUTSIDE the peak band 0.5-1.5), rim/core 0.81, rim/outside 4.51 (aggregate of 91 individuals; 1/91 membrane-like individually; rim level 0.692)
  - radial order |Q|: peak at rho=0.25 (OUTSIDE the peak band 0.5-1.5), rim/core 0.807, rim/outside 7.13 (aggregate of 91 individuals; 3/91 membrane-like individually; rim level 0.59)
  - radial shell s: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.922, rim/outside 1.47 (aggregate of 91 individuals; 0/91 membrane-like individually; rim level 0.861)
  - radial fuel f: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.797, rim/outside 2.94 (aggregate of 91 individuals; 1/91 membrane-like individually; rim level 0.668)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #6 (t=470, R_eq 6.79): none; #4 (t=385, R_eq 6.56): none; #3 (t=385, R_eq 6.43): none; #27 (t=825, R_eq 3.29): none

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 6 of 91 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
