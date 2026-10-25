# Evidence pack: nematic-fuelcell (seed 12)

- world: `../../world.py`, family `active-nematic`
- parent: None; mutation: new class: CH droplets with internal Landau-de Gennes nematic order and extensile active stress, Brinkman-Stokes flow
- run: 201 frames x 100 steps x dt 0.05 = time 1000; grid [128, 128]; wall 390s; status ok
- command: `python -m labkit.run collective/contrib/c17-slowD-wip/world.py --out collective/contrib/c17-slowD-wip/slowD03/seed12 --seeds 12 --no-movie`
- segmentation: matter > 0.57 of robust range [-0.8551, 0.641], min area 6 px

## Measurements
- components: final 20, mean 10.1, max 20; occupancy final 0.09
- tracks: 37; persistent (alive >= 50% of run): 6; longest 163 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 28.50 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [28, 21, 20], H1 [0, 0, 0]
- motion: 7 long-lived tracks moved >= 1 body length; max speed 0.0365/time; max body lengths 2.1
- replication (lineage window K = 20 frames = time 100, default): splits 15, persistent splits 10 (0 more failed only because the siblings re-merged within K), max generation 3, merges 0, merge/split ratio 0, nucleations 7
- channel total drift (end/start - 1): [-0.5083, -0.2092, None, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 3 at frame 97: holes 0, rim-vs-core 0.28, rim-vs-outside 0.64, heterogeneity 0.10; core [0.956, 0.845, 0.968, 0.933] rim [0.816, 0.645, 0.93, 0.806]
  - track 5 at frame 101: holes 0, rim-vs-core 0.39, rim-vs-outside 0.70, heterogeneity 0.11; core [1.0, 0.953, 0.97, 0.979] rim [0.821, 0.648, 0.934, 0.814]
  - track 0 at frame 84: holes 0, rim-vs-core 0.25, rim-vs-outside 0.66, heterogeneity 0.10; core [0.934, 0.778, 0.965, 0.914] rim [0.807, 0.6, 0.938, 0.797]
  - track 29 at frame 190: holes 0, rim-vs-core 0.44, rim-vs-outside 0.40, heterogeneity 0.12; core [0.953, 0.902, 0.912, 0.901] rim [0.737, 0.586, 0.847, 0.693]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 71 components >= 12 px at frames [34, 67, 101, 133, 166, 200]):
  - radial phi (droplet): peak at rho=0.25 (OUTSIDE the peak band 0.5-1.5), rim/core 0.786, rim/outside 3.44 (aggregate of 71 individuals; 5/71 membrane-like individually; rim level 0.576)
  - radial order |Q|: peak at rho=0.25 (OUTSIDE the peak band 0.5-1.5), rim/core 0.808, rim/outside 4.77 (aggregate of 71 individuals; 5/71 membrane-like individually; rim level 0.477)
  - radial shell s: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.918, rim/outside 1.48 (aggregate of 71 individuals; 0/71 membrane-like individually; rim level 0.837)
  - radial fuel f: peak at rho=0.25 (OUTSIDE the peak band 0.5-1.5), rim/core 0.846, rim/outside 2.55 (aggregate of 71 individuals; 1/71 membrane-like individually; rim level 0.662)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #3 (t=485, R_eq 7.09): none; #5 (t=505, R_eq 6.33): none; #0 (t=420, R_eq 7.33, ring): none; #29 (t=950, R_eq 3.14): none

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 12 of 71 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
