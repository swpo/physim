# Evidence pack: lattice-chem-gate (seed 2)

- world: `../../world.py`, family `lattice-artificial-chemistry`
- parent: None; mutation: new class: stochastic lattice gas of reacting particles with pairwise repulsion (Ono-Ikegami type)
- run: 201 frames x 50 steps x dt 1.0 = time 10000; grid [128, 128]; wall 232s; status ok
- command: `python -m labkit.run collective/contrib/c17-latgate-wip/world.py --out collective/contrib/c17-latgate-wip/gate/seed2 --seeds 2 --no-movie`
- segmentation: matter > 0.35 of robust range [0.0, 18.0], min area 6 px

## Measurements
- components: final 79, mean 73.9, max 91; occupancy final 0.08
- tracks: 4641; persistent (alive >= 50% of run): 0; longest 63 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 0.00 (1 = constant size)
- enclosures: components with a hole mean 0.11, final 0; holes at thresholds 0.2/0.35/0.5 final [8, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [109, 52, 11], H1 [29, 8, 0]
- motion: 13 long-lived tracks moved >= 1 body length; max speed 0.0114/time; max body lengths 2.5
- replication (lineage window K = 20 frames = time 1000, default): splits 1030, persistent splits 0 (0 more failed only because the siblings re-merged within K), max generation 0, merges 1026, merge/split ratio 0.996, nucleations 1679
- channel total drift (end/start - 1): [2.464, None, -0.6154, 1.2901]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 1163 at frame 86: holes 0, rim-vs-core 0.29, rim-vs-outside 0.27, heterogeneity 0.17; core [0.692, 0.196, 0.135, 0.297] rim [0.55, 0.357, 0.09, 0.49]
  - track 3416 at frame 175: holes 0, rim-vs-core 0.39, rim-vs-outside 0.27, heterogeneity 0.21; core [0.733, 0.143, 0.056, 0.208] rim [0.578, 0.413, 0.12, 0.431]
  - track 3420 at frame 175: holes 0, rim-vs-core 0.24, rim-vs-outside 0.21, heterogeneity 0.17; core [0.692, 0.179, 0.062, 0.281] rim [0.487, 0.275, 0.109, 0.337]
  - track 2247 at frame 126: holes 0, rim-vs-core 0.14, rim-vs-outside 0.31, heterogeneity 0.16; core [0.619, 0.082, 0.071, 0.554] rim [0.545, 0.13, 0.098, 0.443]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 312 components >= 12 px at frames [34, 67, 101, 133, 166, 200]):
  - radial A (autocatalyst): peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.901, rim/outside 2.11 (aggregate of 312 individuals; 37/312 membrane-like individually; rim level 0.508)
  - radial M (membrane): peak at rho=1.05 (in the peak band 0.5-1.5), rim/core 1.6, rim/outside 1.63 (aggregate of 312 individuals; 242/312 membrane-like individually; rim level 0.317)  MEMBRANE-LIKE
  - radial X (food): peak at rho=2.45 (OUTSIDE the peak band 0.5-1.5), rim/core 1.65, rim/outside 0.771 (aggregate of 312 individuals; 14/312 membrane-like individually; rim level 0.18)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): M (membrane)
- membrane-like channels per top track at mid-life: #1163 (t=4300, R_eq 2.52): ['M (membrane)']; #3416 (t=8750, R_eq 1.95): ['M (membrane)']; #3420 (t=8750, R_eq 2.59): ['M (membrane)']; #2247 (t=6300, R_eq 2.39): ['M (membrane)']

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 8 of 312 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
