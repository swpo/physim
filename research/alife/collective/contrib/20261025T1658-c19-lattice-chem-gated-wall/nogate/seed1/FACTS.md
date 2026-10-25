# Evidence pack: lattice-chem-gate (seed 1)

- world: `../../world.py`, family `lattice-artificial-chemistry`
- parent: None; mutation: new class: stochastic lattice gas of reacting particles with pairwise repulsion (Ono-Ikegami type)
- run: 201 frames x 50 steps x dt 1.0 = time 10000; grid [128, 128]; wall 348s; status ok
- command: `python -m labkit.run collective/contrib/20261025T1658-c19-lattice-chem-gated-wall/world.py --out collective/contrib/20261025T1658-c19-lattice-chem-gated-wall/nogate/seed1 --seeds 1 --no-movie`
- segmentation: matter > 0.35 of robust range [0.0, 14.0], min area 6 px

## Measurements
- components: final 88, mean 68.3, max 100; occupancy final 0.16
- tracks: 8197; persistent (alive >= 50% of run): 0; longest 23 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 0.00 (1 = constant size)
- enclosures: components with a hole mean 1.67, final 2; holes at thresholds 0.2/0.35/0.5 final [52, 2, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [121, 40, 2], H1 [57, 11, 0]
- motion: 0 long-lived tracks moved >= 1 body length; max speed 0/time; max body lengths 3.3
- replication (lineage window K = 20 frames = time 1000, default): splits 2404, persistent splits 0 (0 more failed only because the siblings re-merged within K), max generation 0, merges 2417, merge/split ratio 1, nucleations 1641
- channel total drift (end/start - 1): [2.4342, None, -0.614, 1.2922]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 35 at frame 20: holes 0, rim-vs-core 0.15, rim-vs-outside 0.21, heterogeneity 0.19; core [0.594, 0.26, 0.103, 0.45] rim [0.509, 0.302, 0.154, 0.338]
  - track 8 at frame 15: holes 0, rim-vs-core 0.19, rim-vs-outside 0.36, heterogeneity 0.21; core [0.554, 0.311, 0.117, 0.514] rim [0.56, 0.413, 0.17, 0.357]
  - track 12 at frame 17: holes 0, rim-vs-core 0.14, rim-vs-outside 0.32, heterogeneity 0.21; core [0.584, 0.306, 0.113, 0.464] rim [0.528, 0.384, 0.175, 0.384]
  - track 37 at frame 18: holes 0, rim-vs-core 0.08, rim-vs-outside 0.30, heterogeneity 0.19; core [0.573, 0.312, 0.144, 0.396] rim [0.56, 0.383, 0.175, 0.395]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 333 components >= 12 px at frames [34, 67, 101, 133, 166, 200]):
  - radial A (autocatalyst): peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.905, rim/outside 1.58 (aggregate of 333 individuals; 30/333 membrane-like individually; rim level 0.458)
  - radial M (membrane): peak at rho=0.95 (in the peak band 0.5-1.5), rim/core 1.14, rim/outside 1.38 (aggregate of 333 individuals; 158/333 membrane-like individually; rim level 0.3)
  - radial X (food): peak at rho=2.25 (OUTSIDE the peak band 0.5-1.5), rim/core 1.35, rim/outside 0.876 (aggregate of 333 individuals; 36/333 membrane-like individually; rim level 0.194)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #35 (t=1000, R_eq 5.47): none; #8 (t=750, R_eq 7.36): none; #12 (t=850, R_eq 7.57): none; #37 (t=900, R_eq 5.94): none

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 34 of 333 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
