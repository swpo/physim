# Evidence pack: prod-catalyst-rods (seed 0)

- world: `../../world.py`, family `active-nematic`
- parent: None; mutation: new class: CH droplets with internal Landau-de Gennes nematic order and extensile active stress, Brinkman-Stokes flow
- run: 201 frames x 100 steps x dt 0.05 = time 1000; grid [128, 128]; wall 562s; status ok
- command: `python -m labkit.run scratch/c14/prod/world.py --out scratch/c14/prod/packF7/seed0 --seeds 0 --no-movie`
- segmentation: matter > 0.50 of robust range [-0.8915, 0.9022], min area 6 px

## Measurements
- components: final 16, mean 19.4, max 31; occupancy final 0.06
- tracks: 227; persistent (alive >= 50% of run): 3; longest 172 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 5.83 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [17, 17, 15], H1 [0, 0, 0]
- motion: 32 long-lived tracks moved >= 1 body length; max speed 0.125/time; max body lengths 3.5
- replication (lineage window K = 20 frames = time 100, default): splits 90, persistent splits 11 (0 more failed only because the siblings re-merged within K), max generation 2, merges 29, merge/split ratio 0.322, nucleations 19
- channel total drift (end/start - 1): [-0.7493, -0.3365, None, -0.3381]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 28 at frame 114: holes 0, rim-vs-core 0.30, rim-vs-outside 0.35, heterogeneity 0.12; core [0.777, 0.473, 0.381, 0.781] rim [0.654, 0.36, 0.584, 0.638]
  - track 66 at frame 124: holes 0, rim-vs-core 0.38, rim-vs-outside 0.40, heterogeneity 0.15; core [0.831, 0.619, 0.306, 0.632] rim [0.666, 0.428, 0.572, 0.538]
  - track 46 at frame 104: holes 0, rim-vs-core 0.46, rim-vs-outside 0.29, heterogeneity 0.13; core [0.815, 0.561, 0.334, 0.603] rim [0.623, 0.358, 0.674, 0.48]
  - track 161 at frame 166: holes 0, rim-vs-core 0.44, rim-vs-outside 0.32, heterogeneity 0.15; core [0.826, 0.621, 0.291, 0.578] rim [0.636, 0.402, 0.614, 0.498]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 122 components >= 12 px at frames [34, 67, 101, 133, 166, 200]):
  - radial phi (droplet): peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.804, rim/outside 4.68 (aggregate of 122 individuals; 0/122 membrane-like individually; rim level 0.655)
  - radial order |Q|: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.707, rim/outside 7.82 (aggregate of 122 individuals; 2/122 membrane-like individually; rim level 0.437)
  - radial surfactant s: peak at rho=0.85 (in the peak band 0.5-1.5), rim/core 1.55, rim/outside 2.32 (aggregate of 122 individuals; 87/122 membrane-like individually; rim level 0.521)  MEMBRANE-LIKE
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): surfactant s
- membrane-like channels per top track at mid-life: #28 (t=570, R_eq 4.33): none; #66 (t=620, R_eq 2.93): ['surfactant s']; #46 (t=520, R_eq 2.76): ['surfactant s']; #161 (t=830, R_eq 2.93): ['surfactant s']

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 4 of 122 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, particles.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
