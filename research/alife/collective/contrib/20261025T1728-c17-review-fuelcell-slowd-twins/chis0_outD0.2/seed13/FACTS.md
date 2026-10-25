# Evidence pack: nematic-fuelcell-outD (seed 13)

- world: `../../world_outD.py`, family `active-nematic`
- parent: None; mutation: new class: CH droplets with internal Landau-de Gennes nematic order and extensile active stress, Brinkman-Stokes flow
- run: 201 frames x 100 steps x dt 0.05 = time 1000; grid [128, 128]; wall 399s; status ok
- command: `python -m labkit.run collective/contrib/c17-twins-wip/world_outD.py --out collective/contrib/c17-twins-wip/chis0_outD0.2/seed13 --seeds 13 --no-movie`
- segmentation: matter > 0.56 of robust range [-0.8459, 0.6782], min area 6 px

## Measurements
- components: final 25, mean 14.4, max 25; occupancy final 0.07
- tracks: 53; persistent (alive >= 50% of run): 5; longest 173 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 6.00 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [28, 25, 25], H1 [0, 0, 0]
- motion: 25 long-lived tracks moved >= 1 body length; max speed 0.0821/time; max body lengths 2.9
- replication (lineage window K = 20 frames = time 100, default): splits 22, persistent splits 17 (0 more failed only because the siblings re-merged within K), max generation 4, merges 2, merge/split ratio 0.091, nucleations 7
- channel total drift (end/start - 1): [-0.5021, -0.2819, None, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 5 at frame 114: holes 0, rim-vs-core 0.38, rim-vs-outside 0.38, heterogeneity 0.09; core [0.954, 0.922, 0.907, 0.821] rim [0.743, 0.618, 0.835, 0.774]
  - track 8 at frame 123: holes 0, rim-vs-core 0.41, rim-vs-outside 0.40, heterogeneity 0.10; core [0.953, 0.927, 0.906, 0.799] rim [0.718, 0.598, 0.829, 0.747]
  - track 10 at frame 124: holes 0, rim-vs-core 0.37, rim-vs-outside 0.39, heterogeneity 0.10; core [0.954, 0.931, 0.928, 0.879] rim [0.739, 0.638, 0.855, 0.831]
  - track 38 at frame 173: holes 0, rim-vs-core 0.39, rim-vs-outside 0.38, heterogeneity 0.10; core [0.953, 0.935, 0.9, 0.855] rim [0.73, 0.627, 0.821, 0.8]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 97 components >= 12 px at frames [34, 67, 101, 133, 166, 200]):
  - radial phi (droplet): peak at rho=0.25 (OUTSIDE the peak band 0.5-1.5), rim/core 0.825, rim/outside 4.94 (aggregate of 97 individuals; 3/97 membrane-like individually; rim level 0.7)
  - radial order |Q|: peak at rho=0.25 (OUTSIDE the peak band 0.5-1.5), rim/core 0.815, rim/outside 7.94 (aggregate of 97 individuals; 5/97 membrane-like individually; rim level 0.602)
  - radial shell s: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.922, rim/outside 1.49 (aggregate of 97 individuals; 0/97 membrane-like individually; rim level 0.862)
  - radial fuel f: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.921, rim/outside 2.38 (aggregate of 97 individuals; 0/97 membrane-like individually; rim level 0.786)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #5 (t=570, R_eq 3.66): none; #8 (t=615, R_eq 3.52): none; #10 (t=620, R_eq 3.43): none; #38 (t=865, R_eq 3.66): none

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 7 of 97 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
