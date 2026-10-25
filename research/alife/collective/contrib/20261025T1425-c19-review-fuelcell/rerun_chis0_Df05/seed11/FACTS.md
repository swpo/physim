# Evidence pack: nematic-fuelcell (seed 11)

- world: `../../../20261025T1412-c15-nematic-fuelcell-claim/world.py`, family `active-nematic`
- parent: None; mutation: new class: CH droplets with internal Landau-de Gennes nematic order and extensile active stress, Brinkman-Stokes flow
- run: 201 frames x 100 steps x dt 0.05 = time 1000; grid [128, 128]; wall 589s; status ok
- command: `python -m labkit.run collective/contrib/20261025T1412-c15-nematic-fuelcell-claim/world.py --out collective/contrib/20261025T1425-c19-review-fuelcell/rerun_chis0_Df05/seed11 --seeds 11 --no-movie`
- segmentation: matter > 0.57 of robust range [-0.8624, 0.6516], min area 6 px

## Measurements
- components: final 25, mean 12.5, max 25; occupancy final 0.10
- tracks: 46; persistent (alive >= 50% of run): 11; longest 167 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 52.71 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [31, 25, 24], H1 [0, 0, 0]
- motion: 8 long-lived tracks moved >= 1 body length; max speed 0.0393/time; max body lengths 3.3
- replication (lineage window K = 20 frames = time 100, default): splits 18, persistent splits 12 (0 more failed only because the siblings re-merged within K), max generation 3, merges 1, merge/split ratio 0.056, nucleations 9
- channel total drift (end/start - 1): [-0.5045, -0.1265, None, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 10 at frame 118: holes 0, rim-vs-core 0.42, rim-vs-outside 0.36, heterogeneity 0.12; core [0.924, 0.872, 0.9, 0.869] rim [0.701, 0.567, 0.826, 0.7]
  - track 9 at frame 114: holes 0, rim-vs-core 0.37, rim-vs-outside 0.38, heterogeneity 0.11; core [0.925, 0.823, 0.931, 0.93] rim [0.721, 0.565, 0.862, 0.779]
  - track 6 at frame 89: holes 0, rim-vs-core 0.32, rim-vs-outside 0.65, heterogeneity 0.10; core [0.962, 0.857, 0.97, 0.942] rim [0.809, 0.613, 0.933, 0.805]
  - track 31 at frame 190: holes 0, rim-vs-core 0.32, rim-vs-outside 0.34, heterogeneity 0.10; core [0.916, 0.753, 0.943, 0.869] rim [0.741, 0.519, 0.895, 0.746]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 87 components >= 12 px at frames [34, 67, 101, 133, 166, 200]):
  - radial phi (droplet): peak at rho=0.25 (OUTSIDE the peak band 0.5-1.5), rim/core 0.839, rim/outside 3.86 (aggregate of 87 individuals; 7/87 membrane-like individually; rim level 0.614)
  - radial order |Q|: peak at rho=0.25 (OUTSIDE the peak band 0.5-1.5), rim/core 0.862, rim/outside 5.96 (aggregate of 87 individuals; 10/87 membrane-like individually; rim level 0.527)
  - radial shell s: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.924, rim/outside 1.48 (aggregate of 87 individuals; 0/87 membrane-like individually; rim level 0.827)
  - radial fuel f: peak at rho=0.25 (OUTSIDE the peak band 0.5-1.5), rim/core 0.881, rim/outside 2.21 (aggregate of 87 individuals; 1/87 membrane-like individually; rim level 0.717)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #10 (t=590, R_eq 4.22): none; #9 (t=570, R_eq 4.79): none; #6 (t=445, R_eq 7.51, ring): ['phi (droplet)', 'order |Q|']; #31 (t=950, R_eq 4.62): none

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 16 of 87 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
