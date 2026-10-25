# Evidence pack: lattice-chem (seed 2)

- world: `../world.py`, family `lattice-artificial-chemistry`
- parent: None; mutation: new class: stochastic lattice gas of reacting particles with pairwise repulsion (Ono-Ikegami type)
- run: 201 frames x 50 steps x dt 1.0 = time 10000; grid [128, 128]; wall 372s; status ok
- command: `python -m labkit.run /tmp/c20lc/world.py --out /tmp/c20lc/lam0 --seeds 2 --no-movie`
- segmentation: matter > 0.35 of robust range [0.0, 27.0], min area 6 px

## Measurements
- components: final 50, mean 68.1, max 150; occupancy final 0.17
- tracks: 1480; persistent (alive >= 50% of run): 36; longest 198 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 5.50 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [81, 49, 46], H1 [0, 0, 0]
- motion: 0 long-lived tracks moved >= 1 body length; max speed 0/time; max body lengths 1.1
- replication (lineage window K = 20 frames = time 1000, default): splits 406, persistent splits 0 (0 more failed only because the siblings re-merged within K), max generation 0, merges 524, merge/split ratio 1.29, nucleations 185
- channel total drift (end/start - 1): [2.5535, None, -0.6196, 1.3083]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 22 at frame 103: holes 0, rim-vs-core 0.19, rim-vs-outside 0.25, heterogeneity 0.13; core [0.638, 0.175, 0.033, 0.531] rim [0.619, 0.352, 0.077, 0.487]
  - track 33 at frame 103: holes 0, rim-vs-core 0.12, rim-vs-outside 0.33, heterogeneity 0.17; core [0.63, 0.314, 0.07, 0.333] rim [0.649, 0.418, 0.069, 0.393]
  - track 149 at frame 103: holes 0, rim-vs-core 0.21, rim-vs-outside 0.43, heterogeneity 0.17; core [0.722, 0.231, 0.008, 0.513] rim [0.643, 0.357, 0.093, 0.397]
  - track 175 at frame 104: holes 0, rim-vs-core 0.19, rim-vs-outside 0.50, heterogeneity 0.17; core [0.623, 0.314, 0.047, 0.563] rim [0.71, 0.468, 0.056, 0.481]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 376 components >= 12 px at frames [34, 67, 101, 133, 166, 200]):
  - radial A (autocatalyst): peak at rho=0.25 (OUTSIDE the peak band 0.5-1.5), rim/core 0.921, rim/outside 8.18 (aggregate of 376 individuals; 20/376 membrane-like individually; rim level 0.516)
  - radial M (membrane): peak at rho=0.95 (in the peak band 0.5-1.5), rim/core 1.04, rim/outside 2.89 (aggregate of 376 individuals; 162/376 membrane-like individually; rim level 0.334)
  - radial X (food): peak at rho=2.25 (OUTSIDE the peak band 0.5-1.5), rim/core 2.95, rim/outside 0.716 (aggregate of 376 individuals; 0/376 membrane-like individually; rim level 0.238)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #22 (t=5150, R_eq 2.65): ['M (membrane)']; #33 (t=5150, R_eq 2.71): none; #149 (t=5150, R_eq 2.93): ['M (membrane)']; #175 (t=5200, R_eq 3.24): ['M (membrane)']

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 27 of 376 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
