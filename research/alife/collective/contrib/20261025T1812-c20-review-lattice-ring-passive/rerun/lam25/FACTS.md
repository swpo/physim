# Evidence pack: lattice-chem (seed 2)

- world: `../world.py`, family `lattice-artificial-chemistry`
- parent: None; mutation: new class: stochastic lattice gas of reacting particles with pairwise repulsion (Ono-Ikegami type)
- run: 201 frames x 50 steps x dt 1.0 = time 10000; grid [128, 128]; wall 379s; status ok
- command: `python -m labkit.run /tmp/c20lc/world.py --out /tmp/c20lc/lam25 --seeds 2 --no-movie`
- segmentation: matter > 0.35 of robust range [0.0, 28.0], min area 6 px

## Measurements
- components: final 62, mean 73.7, max 143; occupancy final 0.15
- tracks: 825; persistent (alive >= 50% of run): 55; longest 198 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 6.67 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [77, 63, 61], H1 [0, 0, 0]
- motion: 0 long-lived tracks moved >= 1 body length; max speed 0/time; max body lengths 0.9
- replication (lineage window K = 20 frames = time 1000, default): splits 193, persistent splits 0 (0 more failed only because the siblings re-merged within K), max generation 0, merges 288, merge/split ratio 1.49, nucleations 171
- channel total drift (end/start - 1): [2.4938, None, -0.5977, 1.2219]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 16 at frame 103: holes 0, rim-vs-core 0.15, rim-vs-outside 0.45, heterogeneity 0.15; core [0.648, 0.091, 0.045, 0.505] rim [0.628, 0.194, 0.138, 0.451]
  - track 17 at frame 103: holes 0, rim-vs-core 0.28, rim-vs-outside 0.43, heterogeneity 0.15; core [0.771, 0.033, 0.06, 0.378] rim [0.603, 0.205, 0.046, 0.513]
  - track 20 at frame 103: holes 0, rim-vs-core 0.20, rim-vs-outside 0.47, heterogeneity 0.16; core [0.644, 0.067, 0.047, 0.407] rim [0.65, 0.237, 0.093, 0.504]
  - track 24 at frame 103: holes 0, rim-vs-core 0.24, rim-vs-outside 0.39, heterogeneity 0.15; core [0.779, 0.1, 0.0, 0.544] rim [0.619, 0.238, 0.043, 0.429]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 415 components >= 12 px at frames [34, 67, 101, 133, 166, 200]):
  - radial A (autocatalyst): peak at rho=0.25 (OUTSIDE the peak band 0.5-1.5), rim/core 0.883, rim/outside 10.1 (aggregate of 415 individuals; 9/415 membrane-like individually; rim level 0.556)
  - radial M (membrane): peak at rho=1.25 (in the peak band 0.5-1.5), rim/core 3.47, rim/outside 4.43 (aggregate of 415 individuals; 387/415 membrane-like individually; rim level 0.349)  MEMBRANE-LIKE
  - radial X (food): peak at rho=2.35 (OUTSIDE the peak band 0.5-1.5), rim/core 3.88, rim/outside 0.676 (aggregate of 415 individuals; 1/415 membrane-like individually; rim level 0.236)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): M (membrane)
- membrane-like channels per top track at mid-life: #16 (t=5150, R_eq 2.93): ['M (membrane)']; #17 (t=5150, R_eq 2.71): ['M (membrane)']; #20 (t=5150, R_eq 3.09): ['M (membrane)']; #24 (t=5150, R_eq 2.76): ['M (membrane)']

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 14 of 415 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
