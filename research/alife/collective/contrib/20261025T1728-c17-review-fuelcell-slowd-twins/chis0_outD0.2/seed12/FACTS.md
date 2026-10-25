# Evidence pack: nematic-fuelcell-outD (seed 12)

- world: `../../world_outD.py`, family `active-nematic`
- parent: None; mutation: new class: CH droplets with internal Landau-de Gennes nematic order and extensile active stress, Brinkman-Stokes flow
- run: 201 frames x 100 steps x dt 0.05 = time 1000; grid [128, 128]; wall 393s; status ok
- command: `python -m labkit.run collective/contrib/c17-twins-wip/world_outD.py --out collective/contrib/c17-twins-wip/chis0_outD0.2/seed12 --seeds 12 --no-movie`
- segmentation: matter > 0.56 of robust range [-0.8513, 0.6667], min area 6 px

## Measurements
- components: final 23, mean 14.1, max 24; occupancy final 0.08
- tracks: 60; persistent (alive >= 50% of run): 5; longest 158 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 21.00 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [27, 24, 23], H1 [0, 0, 0]
- motion: 18 long-lived tracks moved >= 1 body length; max speed 0.0608/time; max body lengths 3.0
- replication (lineage window K = 20 frames = time 100, default): splits 24, persistent splits 14 (0 more failed only because the siblings re-merged within K), max generation 3, merges 4, merge/split ratio 0.167, nucleations 7
- channel total drift (end/start - 1): [-0.5083, -0.2214, None, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 9 at frame 123: holes 0, rim-vs-core 0.27, rim-vs-outside 0.32, heterogeneity 0.09; core [0.972, 0.57, 0.999, 1.0] rim [0.745, 0.437, 0.942, 1.0]
  - track 10 at frame 121: holes 0, rim-vs-core 0.36, rim-vs-outside 0.41, heterogeneity 0.10; core [0.945, 0.913, 0.947, 0.892] rim [0.737, 0.628, 0.876, 0.846]
  - track 11 at frame 109: holes 0, rim-vs-core 0.39, rim-vs-outside 0.41, heterogeneity 0.10; core [0.953, 0.935, 0.931, 0.884] rim [0.73, 0.631, 0.857, 0.832]
  - track 42 at frame 183: holes 0, rim-vs-core 0.40, rim-vs-outside 0.39, heterogeneity 0.10; core [0.962, 0.945, 0.879, 0.802] rim [0.733, 0.627, 0.803, 0.749]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 96 components >= 12 px at frames [34, 67, 101, 133, 166, 200]):
  - radial phi (droplet): peak at rho=0.25 (OUTSIDE the peak band 0.5-1.5), rim/core 0.801, rim/outside 4.46 (aggregate of 96 individuals; 3/96 membrane-like individually; rim level 0.662)
  - radial order |Q|: peak at rho=0.25 (OUTSIDE the peak band 0.5-1.5), rim/core 0.774, rim/outside 6.87 (aggregate of 96 individuals; 5/96 membrane-like individually; rim level 0.561)
  - radial shell s: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.92, rim/outside 1.48 (aggregate of 96 individuals; 0/96 membrane-like individually; rim level 0.86)
  - radial fuel f: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.916, rim/outside 2.39 (aggregate of 96 individuals; 1/96 membrane-like individually; rim level 0.809)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #9 (t=615, R_eq 3.95): none; #10 (t=605, R_eq 3.95): none; #11 (t=545, R_eq 3.43): none; #42 (t=915, R_eq 3.29): none

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 10 of 96 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
