# Evidence pack: lattice-chem-gate (seed 1)

- world: `../../world.py`, family `lattice-artificial-chemistry`
- parent: None; mutation: new class: stochastic lattice gas of reacting particles with pairwise repulsion (Ono-Ikegami type)
- run: 201 frames x 50 steps x dt 1.0 = time 10000; grid [128, 128]; wall 317s; status ok
- command: `python -m labkit.run collective/contrib/20261025T1658-c19-lattice-chem-gated-wall/world.py --out collective/contrib/20261025T1658-c19-lattice-chem-gated-wall/gate/seed1 --seeds 1 --no-movie`
- segmentation: matter > 0.35 of robust range [0.0, 18.0], min area 6 px

## Measurements
- components: final 89, mean 73.8, max 89; occupancy final 0.09
- tracks: 4619; persistent (alive >= 50% of run): 0; longest 42 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 0.00 (1 = constant size)
- enclosures: components with a hole mean 0.08, final 0; holes at thresholds 0.2/0.35/0.5 final [17, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [114, 55, 8], H1 [35, 8, 0]
- motion: 6 long-lived tracks moved >= 1 body length; max speed 0.00574/time; max body lengths 3.6
- replication (lineage window K = 20 frames = time 1000, default): splits 1033, persistent splits 0 (0 more failed only because the siblings re-merged within K), max generation 0, merges 1017, merge/split ratio 0.985, nucleations 1683
- channel total drift (end/start - 1): [2.4776, None, -0.6192, 1.2993]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 3656 at frame 180: holes 0, rim-vs-core 0.34, rim-vs-outside 0.19, heterogeneity 0.19; core [0.75, 0.357, 0.021, 0.344] rim [0.475, 0.357, 0.156, 0.484]
  - track 2930 at frame 148: holes 0, rim-vs-core 0.26, rim-vs-outside 0.23, heterogeneity 0.18; core [0.65, 0.054, 0.125, 0.359] rim [0.569, 0.297, 0.141, 0.404]
  - track 3595 at frame 176: holes 0, rim-vs-core 0.10, rim-vs-outside 0.27, heterogeneity 0.19; core [0.525, 0.259, 0.109, 0.414] rim [0.592, 0.286, 0.103, 0.346]
  - track 3710 at frame 182: holes 0, rim-vs-core 0.22, rim-vs-outside 0.17, heterogeneity 0.18; core [0.658, 0.232, 0.083, 0.391] rim [0.528, 0.396, 0.109, 0.327]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 334 components >= 12 px at frames [34, 67, 101, 133, 166, 200]):
  - radial A (autocatalyst): peak at rho=0.25 (OUTSIDE the peak band 0.5-1.5), rim/core 0.91, rim/outside 2.11 (aggregate of 334 individuals; 48/334 membrane-like individually; rim level 0.507)
  - radial M (membrane): peak at rho=1.25 (in the peak band 0.5-1.5), rim/core 1.6, rim/outside 1.58 (aggregate of 334 individuals; 260/334 membrane-like individually; rim level 0.316)  MEMBRANE-LIKE
  - radial X (food): peak at rho=2.45 (OUTSIDE the peak band 0.5-1.5), rim/core 1.56, rim/outside 0.732 (aggregate of 334 individuals; 11/334 membrane-like individually; rim level 0.169)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): M (membrane)
- membrane-like channels per top track at mid-life: #3656 (t=9000, R_eq 1.95): ['M (membrane)']; #2930 (t=7400, R_eq 2.59): ['M (membrane)']; #3595 (t=8800, R_eq 3.24): ['A (autocatalyst)']; #3710 (t=9100, R_eq 2.59): ['M (membrane)']

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 10 of 334 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
