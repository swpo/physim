# Evidence pack: nematic-fuelcell-outslow (seed 1)

- world: `../../world_outslow.py`, family `active-nematic`
- parent: None; mutation: new class: CH droplets with internal Landau-de Gennes nematic order and extensile active stress, Brinkman-Stokes flow
- run: 201 frames x 100 steps x dt 0.05 = time 1000; grid [128, 128]; wall 681s; status ok
- command: `python -m labkit.run /root/w/world_outslow.py --out /root/w/outslow/s1 --seeds 1 --no-movie`
- segmentation: matter > 0.57 of robust range [-0.8511, 0.6526], min area 6 px

## Measurements
- components: final 11, mean 5.8, max 11; occupancy final 0.07
- tracks: 25; persistent (alive >= 50% of run): 4; longest 114 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 17.11 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [16, 11, 11], H1 [1, 0, 0]
- motion: 5 long-lived tracks moved >= 1 body length; max speed 0.0499/time; max body lengths 1.9
- replication (lineage window K = 20 frames = time 100, default): splits 10, persistent splits 7 (0 more failed only because the siblings re-merged within K), max generation 3, merges 2, merge/split ratio 0.2, nucleations 3
- channel total drift (end/start - 1): [-0.4928, -0.3426, None, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 1 at frame 71: holes 0, rim-vs-core 0.35, rim-vs-outside 0.40, heterogeneity 0.10; core [0.94, 0.864, 0.962, 0.902] rim [0.732, 0.601, 0.897, 0.834]
  - track 3 at frame 86: holes 0, rim-vs-core 0.29, rim-vs-outside 0.66, heterogeneity 0.11; core [0.974, 0.891, 0.975, 0.921] rim [0.817, 0.662, 0.932, 0.867]
  - track 6 at frame 148: holes 0, rim-vs-core 0.30, rim-vs-outside 0.62, heterogeneity 0.09; core [0.974, 0.849, 0.988, 0.93] rim [0.814, 0.606, 0.943, 0.861]
  - track 19 at frame 178: holes 0, rim-vs-core 0.30, rim-vs-outside 0.35, heterogeneity 0.11; core [0.948, 0.745, 0.983, 0.978] rim [0.746, 0.533, 0.924, 0.921]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 40 components >= 12 px at frames [34, 67, 101, 133, 166, 200]):
  - radial phi (droplet): peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.787, rim/outside 3.45 (aggregate of 40 individuals; 4/40 membrane-like individually; rim level 0.572)
  - radial order |Q|: peak at rho=0.25 (OUTSIDE the peak band 0.5-1.5), rim/core 0.801, rim/outside 4.82 (aggregate of 40 individuals; 5/40 membrane-like individually; rim level 0.508)
  - radial shell s: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.925, rim/outside 1.47 (aggregate of 40 individuals; 0/40 membrane-like individually; rim level 0.837)
  - radial fuel f: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.926, rim/outside 2 (aggregate of 40 individuals; 0/40 membrane-like individually; rim level 0.805)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #1 (t=355, R_eq 5.7): none; #3 (t=430, R_eq 6.79, ring): ['phi (droplet)', 'order |Q|']; #6 (t=740, R_eq 8.69, ring): ['phi (droplet)', 'order |Q|']; #19 (t=890, R_eq 5.08): none

## Warnings
- radial: 8 of 40 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
