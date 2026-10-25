# Evidence pack: nematic-fuelcell-outslow (seed 12)

- world: `../../world.py`, family `active-nematic`
- parent: None; mutation: new class: CH droplets with internal Landau-de Gennes nematic order and extensile active stress, Brinkman-Stokes flow
- run: 201 frames x 100 steps x dt 0.05 = time 1000; grid [128, 128]; wall 394s; status ok
- command: `python -m labkit.run world.py --out outslow/seed12 --seeds 12 --no-movie`
- segmentation: matter > 0.56 of robust range [-0.8601, 0.6819], min area 6 px

## Measurements
- components: final 25, mean 12.4, max 27; occupancy final 0.09
- tracks: 56; persistent (alive >= 50% of run): 5; longest 154 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 31.83 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [28, 25, 25], H1 [0, 0, 0]
- motion: 12 long-lived tracks moved >= 1 body length; max speed 0.0685/time; max body lengths 1.8
- replication (lineage window K = 20 frames = time 100, default): splits 23, persistent splits 16 (0 more failed only because the siblings re-merged within K), max generation 3, merges 3, merge/split ratio 0.13, nucleations 7
- channel total drift (end/start - 1): [-0.5083, -0.0837, None, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 5 at frame 101: holes 0, rim-vs-core 0.37, rim-vs-outside 0.64, heterogeneity 0.10; core [0.987, 0.933, 0.963, 0.917] rim [0.792, 0.62, 0.922, 0.866]
  - track 9 at frame 128: holes 0, rim-vs-core 0.44, rim-vs-outside 0.37, heterogeneity 0.11; core [0.945, 0.918, 0.883, 0.876] rim [0.701, 0.583, 0.799, 0.773]
  - track 10 at frame 114: holes 0, rim-vs-core 0.27, rim-vs-outside 0.60, heterogeneity 0.11; core [0.95, 0.759, 0.986, 0.965] rim [0.798, 0.575, 0.924, 0.867]
  - track 40 at frame 190: holes 0, rim-vs-core 0.43, rim-vs-outside 0.41, heterogeneity 0.11; core [0.956, 0.934, 0.932, 0.923] rim [0.707, 0.604, 0.843, 0.818]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 86 components >= 12 px at frames [34, 67, 101, 133, 166, 200]):
  - radial phi (droplet): peak at rho=0.25 (OUTSIDE the peak band 0.5-1.5), rim/core 0.812, rim/outside 4.32 (aggregate of 86 individuals; 5/86 membrane-like individually; rim level 0.631)
  - radial order |Q|: peak at rho=0.25 (OUTSIDE the peak band 0.5-1.5), rim/core 0.792, rim/outside 6.4 (aggregate of 86 individuals; 5/86 membrane-like individually; rim level 0.541)
  - radial shell s: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.914, rim/outside 1.53 (aggregate of 86 individuals; 0/86 membrane-like individually; rim level 0.844)
  - radial fuel f: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.911, rim/outside 2.05 (aggregate of 86 individuals; 0/86 membrane-like individually; rim level 0.82)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #5 (t=505, R_eq 6.43): none; #9 (t=640, R_eq 3.57): none; #10 (t=570, R_eq 6.41, ring): ['phi (droplet)', 'order |Q|']; #40 (t=950, R_eq 3.83): none

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 13 of 86 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
