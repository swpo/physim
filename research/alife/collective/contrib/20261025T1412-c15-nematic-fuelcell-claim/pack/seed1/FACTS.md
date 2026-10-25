# Evidence pack: nematic-fuelcell (seed 1)

- world: `../../world.py`, family `active-nematic`
- parent: None; mutation: new class: CH droplets with internal Landau-de Gennes nematic order and extensile active stress, Brinkman-Stokes flow
- run: 201 frames x 100 steps x dt 0.05 = time 1000; grid [128, 128]; wall 714s; status ok
- command: `python -m labkit.run /root/w/world.py --out /root/w/z45/shell_s1 --seeds 1 --no-movie`
- segmentation: matter > 0.58 of robust range [-0.8463, 0.6059], min area 6 px

## Measurements
- components: final 12, mean 4.9, max 12; occupancy final 0.07
- tracks: 21; persistent (alive >= 50% of run): 2; longest 170 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 34.38 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [16, 13, 12], H1 [0, 0, 0]
- motion: 4 long-lived tracks moved >= 1 body length; max speed 0.0355/time; max body lengths 1.9
- replication (lineage window K = 20 frames = time 100, default): splits 9, persistent splits 5 (0 more failed only because the siblings re-merged within K), max generation 3, merges 0, merge/split ratio 0, nucleations 3
- channel total drift (end/start - 1): [-0.4928, -0.445, None, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 1 at frame 99: holes 0, rim-vs-core 0.55, rim-vs-outside 0.83, heterogeneity 0.16; core [1.0, 0.995, 0.295, 0.854] rim [0.845, 0.732, 0.743, 0.758]
  - track 5 at frame 158: holes 0, rim-vs-core 0.49, rim-vs-outside 0.45, heterogeneity 0.16; core [0.945, 0.787, 0.553, 0.865] rim [0.755, 0.575, 0.897, 0.66]
  - track 10 at frame 176: holes 0, rim-vs-core 0.52, rim-vs-outside 0.52, heterogeneity 0.15; core [0.981, 0.979, 0.409, 0.796] rim [0.809, 0.786, 0.825, 0.636]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 36 components >= 12 px at frames [34, 67, 101, 133, 166, 200]):
  - radial phi (droplet): peak at rho=0.25 (OUTSIDE the peak band 0.5-1.5), rim/core 0.839, rim/outside 3.16 (aggregate of 36 individuals; 7/36 membrane-like individually; rim level 0.53)
  - radial order |Q|: peak at rho=0.25 (OUTSIDE the peak band 0.5-1.5), rim/core 0.847, rim/outside 4.34 (aggregate of 36 individuals; 7/36 membrane-like individually; rim level 0.455)
  - radial shell s: peak at rho=0.45 (OUTSIDE the peak band 0.5-1.5), rim/core 1.03, rim/outside 2.02 (aggregate of 36 individuals; 14/36 membrane-like individually; rim level 0.525)
  - radial fuel f: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.836, rim/outside 2.39 (aggregate of 36 individuals; 7/36 membrane-like individually; rim level 0.514)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #1 (t=495, R_eq 6.91): none; #0 (t=310, R_eq 7.29, ring): ['phi (droplet)', 'order |Q|', 'shell s', 'fuel f']; #5 (t=790, R_eq 5.86, ring): ['phi (droplet)', 'order |Q|', 'fuel f']; #10 (t=880, R_eq 4.79): none

## Warnings
- radial: 14 of 36 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
