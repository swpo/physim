# Evidence pack: nematic-fuelcell (seed 1)

- world: `../../world.py`, family `active-nematic`
- parent: None; mutation: new class: CH droplets with internal Landau-de Gennes nematic order and extensile active stress, Brinkman-Stokes flow
- run: 201 frames x 100 steps x dt 0.05 = time 1000; grid [128, 128]; wall 680s; status ok
- command: `python -m labkit.run /root/w/world.py --out /root/w/z45/chis0_s1 --seeds 1 --no-movie`
- segmentation: matter > 0.55 of robust range [-0.8608, 0.693], min area 6 px

## Measurements
- components: final 11, mean 5.0, max 11; occupancy final 0.08
- tracks: 19; persistent (alive >= 50% of run): 2; longest 185 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 35.67 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [16, 12, 10], H1 [0, 0, 0]
- motion: 3 long-lived tracks moved >= 1 body length; max speed 0.0415/time; max body lengths 1.9
- replication (lineage window K = 20 frames = time 100, default): splits 8, persistent splits 2 (0 more failed only because the siblings re-merged within K), max generation 1, merges 0, merge/split ratio 0, nucleations 3
- channel total drift (end/start - 1): [-0.4928, -0.2296, None, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 1 at frame 108: holes 0, rim-vs-core 0.31, rim-vs-outside 0.70, heterogeneity 0.10; core [0.994, 0.981, 0.995, 0.983] rim [0.827, 0.741, 0.943, 0.904]
  - track 4 at frame 150: holes 0, rim-vs-core 0.43, rim-vs-outside 0.36, heterogeneity 0.12; core [0.941, 0.909, 0.931, 0.928] rim [0.696, 0.585, 0.839, 0.812]
  - track 2 at frame 66: holes 0, rim-vs-core 0.28, rim-vs-outside 0.74, heterogeneity 0.11; core [0.99, 0.981, 0.996, 0.99] rim [0.826, 0.777, 0.944, 0.913]
  - track 0 at frame 54: holes 0, rim-vs-core 0.29, rim-vs-outside 0.67, heterogeneity 0.11; core [0.971, 0.904, 0.989, 0.935] rim [0.805, 0.694, 0.933, 0.854]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 35 components >= 12 px at frames [34, 67, 101, 133, 166, 200]):
  - radial phi (droplet): peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.755, rim/outside 3.55 (aggregate of 35 individuals; 3/35 membrane-like individually; rim level 0.55)
  - radial order |Q|: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.762, rim/outside 5.09 (aggregate of 35 individuals; 3/35 membrane-like individually; rim level 0.497)
  - radial shell s: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.891, rim/outside 1.54 (aggregate of 35 individuals; 0/35 membrane-like individually; rim level 0.811)
  - radial fuel f: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.909, rim/outside 1.6 (aggregate of 35 individuals; 0/35 membrane-like individually; rim level 0.828)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #1 (t=540, R_eq 7.29): none; #4 (t=750, R_eq 5.01): none; #2 (t=330, R_eq 7.2): none; #0 (t=270, R_eq 7.07, ring): none

## Warnings
- radial: 8 of 35 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
