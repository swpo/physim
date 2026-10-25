# Evidence pack: nematic-fuelcell (seed 13)

- world: `../../world.py`, family `active-nematic`
- parent: None; mutation: new class: CH droplets with internal Landau-de Gennes nematic order and extensile active stress, Brinkman-Stokes flow
- run: 201 frames x 100 steps x dt 0.05 = time 1000; grid [128, 128]; wall 393s; status ok
- command: `python -m labkit.run collective/contrib/c17-twins-wip/world.py --out collective/contrib/c17-twins-wip/chis0_Df0.2/seed13 --seeds 13 --no-movie`
- segmentation: matter > 0.56 of robust range [-0.8442, 0.6553], min area 6 px

## Measurements
- components: final 23, mean 12.8, max 23; occupancy final 0.08
- tracks: 56; persistent (alive >= 50% of run): 8; longest 173 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 20.64 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [29, 24, 22], H1 [0, 0, 0]
- motion: 14 long-lived tracks moved >= 1 body length; max speed 0.0549/time; max body lengths 3.7
- replication (lineage window K = 20 frames = time 100, default): splits 22, persistent splits 12 (0 more failed only because the siblings re-merged within K), max generation 3, merges 4, merge/split ratio 0.182, nucleations 7
- channel total drift (end/start - 1): [-0.5021, -0.3616, None, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 5 at frame 114: holes 0, rim-vs-core 0.43, rim-vs-outside 0.40, heterogeneity 0.11; core [0.967, 0.961, 0.871, 0.848] rim [0.767, 0.656, 0.812, 0.633]
  - track 10 at frame 136: holes 0, rim-vs-core 0.33, rim-vs-outside 0.39, heterogeneity 0.09; core [0.926, 0.765, 0.915, 0.81] rim [0.75, 0.55, 0.863, 0.647]
  - track 8 at frame 104: holes 0, rim-vs-core 0.41, rim-vs-outside 0.40, heterogeneity 0.11; core [0.932, 0.875, 0.891, 0.814] rim [0.732, 0.59, 0.83, 0.616]
  - track 43 at frame 180: holes 0, rim-vs-core 0.36, rim-vs-outside 0.68, heterogeneity 0.10; core [0.976, 0.893, 0.984, 0.975] rim [0.815, 0.63, 0.936, 0.798]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 87 components >= 12 px at frames [34, 67, 101, 133, 166, 200]):
  - radial phi (droplet): peak at rho=0.25 (OUTSIDE the peak band 0.5-1.5), rim/core 0.803, rim/outside 4.34 (aggregate of 87 individuals; 2/87 membrane-like individually; rim level 0.671)
  - radial order |Q|: peak at rho=0.25 (OUTSIDE the peak band 0.5-1.5), rim/core 0.795, rim/outside 6.79 (aggregate of 87 individuals; 3/87 membrane-like individually; rim level 0.567)
  - radial shell s: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.92, rim/outside 1.46 (aggregate of 87 individuals; 0/87 membrane-like individually; rim level 0.85)
  - radial fuel f: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.787, rim/outside 2.88 (aggregate of 87 individuals; 2/87 membrane-like individually; rim level 0.648)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #5 (t=570, R_eq 3.09): none; #10 (t=680, R_eq 4.3): none; #8 (t=520, R_eq 3.83): none; #43 (t=900, R_eq 6.79, ring): ['phi (droplet)', 'order |Q|']

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 9 of 87 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
