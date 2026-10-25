# Evidence pack: lattice-chem (seed 4)

- world: `../world.py`, family `lattice-artificial-chemistry`
- parent: None; mutation: new class: stochastic lattice gas of reacting particles with pairwise repulsion (Ono-Ikegami type)
- run: 201 frames x 100 steps x dt 1.0 = time 20000; grid [128, 128]; wall 540s; status ok
- command: `python -m labkit.run scratch/c14/rev_lat/world.py --out scratch/c14/rev_lat/km04 --seeds 4 --frames 200 --spf 100 --no-movie`
- segmentation: matter > 0.35 of robust range [0.0, 28.0], min area 6 px

## Measurements
- components: final 46, mean 59.2, max 133; occupancy final 0.15
- tracks: 552; persistent (alive >= 50% of run): 46; longest 199 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 7.50 (1 = constant size)
- enclosures: components with a hole mean 0.01, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [62, 47, 46], H1 [0, 0, 0]
- motion: 1 long-lived tracks moved >= 1 body length; max speed 0.000298/time; max body lengths 1.1
- replication (lineage window K = 20 frames = time 2000, default): splits 99, persistent splits 0 (0 more failed only because the siblings re-merged within K), max generation 0, merges 204, merge/split ratio 2.06, nucleations 161
- channel total drift (end/start - 1): [2.3777, None, -0.5993, -0.2906]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 3 at frame 101: holes 0, rim-vs-core 0.18, rim-vs-outside 0.43, heterogeneity 0.18; core [0.782, 0.118, 0.044, 0.4] rim [0.64, 0.214, 0.088, 0.4]
  - track 5 at frame 101: holes 0, rim-vs-core 0.21, rim-vs-outside 0.33, heterogeneity 0.16; core [0.694, 0.114, 0.047, 0.471] rim [0.536, 0.2, 0.073, 0.36]
  - track 8 at frame 101: holes 0, rim-vs-core 0.22, rim-vs-outside 0.34, heterogeneity 0.15; core [0.696, 0.113, 0.079, 0.4] rim [0.612, 0.29, 0.094, 0.3]
  - track 31 at frame 101: holes 0, rim-vs-core 0.14, rim-vs-outside 0.32, heterogeneity 0.14; core [0.66, 0.131, 0.046, 0.308] rim [0.605, 0.249, 0.053, 0.353]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 327 components >= 12 px at frames [34, 67, 101, 133, 166, 200]):
  - radial A (autocatalyst): peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.902, rim/outside 9.26 (aggregate of 327 individuals; 10/327 membrane-like individually; rim level 0.55)
  - radial M (membrane): peak at rho=1.35 (in the peak band 0.5-1.5), rim/core 2.39, rim/outside 2.81 (aggregate of 327 individuals; 291/327 membrane-like individually; rim level 0.393)  MEMBRANE-LIKE
  - radial X (food): peak at rho=2.15 (OUTSIDE the peak band 0.5-1.5), rim/core 3.16, rim/outside 0.673 (aggregate of 327 individuals; 0/327 membrane-like individually; rim level 0.246)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): M (membrane)
- membrane-like channels per top track at mid-life: #3 (t=10100, R_eq 3.29): ['M (membrane)']; #5 (t=10100, R_eq 3.19): ['M (membrane)']; #8 (t=10100, R_eq 3.09): ['M (membrane)']; #31 (t=10100, R_eq 3.09): ['M (membrane)']

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 20 of 327 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
