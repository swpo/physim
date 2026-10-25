# Evidence pack: nematic-fuelcell (seed 12)

- world: `../../world.py`, family `active-nematic`
- parent: None; mutation: new class: CH droplets with internal Landau-de Gennes nematic order and extensile active stress, Brinkman-Stokes flow
- run: 201 frames x 100 steps x dt 0.05 = time 1000; grid [128, 128]; wall 399s; status ok
- command: `python -m labkit.run world.py --out noise_lamf1/seed12 --seeds 12 --no-movie`
- segmentation: matter > 0.54 of robust range [-0.8478, 0.7192], min area 6 px

## Measurements
- components: final 25, mean 11.7, max 25; occupancy final 0.08
- tracks: 54; persistent (alive >= 50% of run): 5; longest 128 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 3.26 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [26, 25, 22], H1 [0, 0, 0]
- motion: 8 long-lived tracks moved >= 1 body length; max speed 0.032/time; max body lengths 3.1
- replication (lineage window K = 20 frames = time 100, default): splits 22, persistent splits 10 (0 more failed only because the siblings re-merged within K), max generation 3, merges 3, merge/split ratio 0.136, nucleations 7
- channel total drift (end/start - 1): [-0.5083, -0.1705, None, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 8 at frame 131: holes 0, rim-vs-core 0.52, rim-vs-outside 0.43, heterogeneity 0.15; core [0.91, 0.907, 0.482, 0.787] rim [0.712, 0.626, 0.844, 0.635]
  - track 10 at frame 138: holes 0, rim-vs-core 0.61, rim-vs-outside 0.57, heterogeneity 0.19; core [0.973, 0.88, 0.385, 1.0] rim [0.745, 0.637, 0.88, 0.877]
  - track 11 at frame 145: holes 0, rim-vs-core 0.67, rim-vs-outside 0.55, heterogeneity 0.19; core [0.979, 0.944, 0.379, 0.994] rim [0.74, 0.589, 0.871, 0.822]
  - track 29 at frame 176: holes 0, rim-vs-core 0.61, rim-vs-outside 0.54, heterogeneity 0.20; core [0.966, 0.854, 0.416, 0.991] rim [0.711, 0.634, 0.896, 0.827]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 85 components >= 12 px at frames [34, 67, 101, 133, 166, 200]):
  - radial phi (droplet): peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.78, rim/outside 4.36 (aggregate of 85 individuals; 0/85 membrane-like individually; rim level 0.663)
  - radial order |Q|: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.783, rim/outside 6.53 (aggregate of 85 individuals; 1/85 membrane-like individually; rim level 0.562)
  - radial shell s: peak at rho=0.65 (in the peak band 0.5-1.5), rim/core 1.18, rim/outside 2.33 (aggregate of 85 individuals; 46/85 membrane-like individually; rim level 0.598)
  - radial fuel f: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.773, rim/outside 2.75 (aggregate of 85 individuals; 1/85 membrane-like individually; rim level 0.538)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #8 (t=655, R_eq 4.26): none; #10 (t=690, R_eq 4.48): ['shell s']; #11 (t=725, R_eq 4.3): ['shell s']; #29 (t=880, R_eq 4.58): ['shell s']

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 5 of 85 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
