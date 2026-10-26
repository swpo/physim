# Evidence pack: lattice-chem (seed 4)

- world: `../world.py`, family `lattice-artificial-chemistry`
- parent: None; mutation: new class: stochastic lattice gas of reacting particles with pairwise repulsion (Ono-Ikegami type)
- run: 201 frames x 100 steps x dt 1.0 = time 20000; grid [128, 128]; wall 564s; status ok
- command: `python -m labkit.run scratch/c14/rev_lat/world.py --out scratch/c14/rev_lat/default --seeds 4 --frames 200 --spf 100 --no-movie`
- segmentation: matter > 0.35 of robust range [0.0, 27.0], min area 6 px

## Measurements
- components: final 60, mean 70.8, max 161; occupancy final 0.16
- tracks: 468; persistent (alive >= 50% of run): 57; longest 200 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 7.33 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [77, 61, 59], H1 [0, 0, 0]
- motion: 0 long-lived tracks moved >= 1 body length; max speed 0/time; max body lengths 1.1
- replication (lineage window K = 20 frames = time 2000, default): splits 60, persistent splits 0 (0 more failed only because the siblings re-merged within K), max generation 0, merges 170, merge/split ratio 2.83, nucleations 180
- channel total drift (end/start - 1): [2.4633, None, -0.5891, 1.2529]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 2 at frame 101: holes 0, rim-vs-core 0.05, rim-vs-outside 0.43, heterogeneity 0.15; core [0.633, 0.111, 0.06, 0.511] rim [0.599, 0.148, 0.058, 0.532]
  - track 4 at frame 101: holes 0, rim-vs-core 0.16, rim-vs-outside 0.44, heterogeneity 0.17; core [0.673, 0.14, 0.042, 0.532] rim [0.544, 0.229, 0.088, 0.51]
  - track 19 at frame 101: holes 0, rim-vs-core 0.16, rim-vs-outside 0.44, heterogeneity 0.16; core [0.756, 0.071, 0.043, 0.532] rim [0.606, 0.133, 0.047, 0.533]
  - track 44 at frame 101: holes 0, rim-vs-core 0.20, rim-vs-outside 0.44, heterogeneity 0.16; core [0.64, 0.063, 0.036, 0.524] rim [0.682, 0.201, 0.087, 0.396]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 401 components >= 12 px at frames [34, 67, 101, 133, 166, 200]):
  - radial A (autocatalyst): peak at rho=0.25 (OUTSIDE the peak band 0.5-1.5), rim/core 0.922, rim/outside 12.6 (aggregate of 401 individuals; 8/401 membrane-like individually; rim level 0.574)
  - radial M (membrane): peak at rho=1.25 (in the peak band 0.5-1.5), rim/core 3.83, rim/outside 6.16 (aggregate of 401 individuals; 382/401 membrane-like individually; rim level 0.379)  MEMBRANE-LIKE
  - radial X (food): peak at rho=2.45 (OUTSIDE the peak band 0.5-1.5), rim/core 3.94, rim/outside 0.675 (aggregate of 401 individuals; 0/401 membrane-like individually; rim level 0.248)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): M (membrane)
- membrane-like channels per top track at mid-life: #2 (t=10100, R_eq 3.04): ['M (membrane)']; #4 (t=10100, R_eq 3.39): ['M (membrane)']; #19 (t=10100, R_eq 3.04): ['M (membrane)']; #44 (t=10100, R_eq 3.09): ['M (membrane)']

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 6 of 401 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
