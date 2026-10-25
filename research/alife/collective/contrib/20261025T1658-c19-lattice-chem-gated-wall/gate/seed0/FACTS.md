# Evidence pack: lattice-chem-gate (seed 0)

- world: `../../world.py`, family `lattice-artificial-chemistry`
- parent: None; mutation: new class: stochastic lattice gas of reacting particles with pairwise repulsion (Ono-Ikegami type)
- run: 201 frames x 50 steps x dt 1.0 = time 10000; grid [128, 128]; wall 319s; status ok
- command: `python -m labkit.run collective/contrib/20261025T1658-c19-lattice-chem-gated-wall/world.py --out collective/contrib/20261025T1658-c19-lattice-chem-gated-wall/gate/seed0 --seeds 0 --no-movie`
- segmentation: matter > 0.35 of robust range [0.0, 18.0], min area 6 px

## Measurements
- components: final 84, mean 74.7, max 91; occupancy final 0.09
- tracks: 4219; persistent (alive >= 50% of run): 0; longest 61 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 0.00 (1 = constant size)
- enclosures: components with a hole mean 0.04, final 0; holes at thresholds 0.2/0.35/0.5 final [5, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [102, 52, 14], H1 [36, 12, 0]
- motion: 16 long-lived tracks moved >= 1 body length; max speed 0.00808/time; max body lengths 3.1
- replication (lineage window K = 20 frames = time 1000, default): splits 900, persistent splits 0 (0 more failed only because the siblings re-merged within K), max generation 0, merges 888, merge/split ratio 0.987, nucleations 1672
- channel total drift (end/start - 1): [2.4172, None, -0.6211, 1.2795]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 1748 at frame 118: holes 0, rim-vs-core 0.40, rim-vs-outside 0.17, heterogeneity 0.21; core [0.794, 0.032, 0.102, 0.403] rim [0.536, 0.339, 0.146, 0.43]
  - track 2339 at frame 145: holes 0, rim-vs-core 0.20, rim-vs-outside 0.17, heterogeneity 0.17; core [0.612, 0.143, 0.107, 0.518] rim [0.543, 0.276, 0.111, 0.392]
  - track 1544 at frame 103: holes 0, rim-vs-core 0.18, rim-vs-outside 0.21, heterogeneity 0.16; core [0.668, 0.126, 0.074, 0.36] rim [0.594, 0.286, 0.079, 0.408]
  - track 38 at frame 30: holes 0, rim-vs-core 0.10, rim-vs-outside 0.31, heterogeneity 0.18; core [0.622, 0.235, 0.065, 0.5] rim [0.625, 0.223, 0.115, 0.414]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 338 components >= 12 px at frames [34, 67, 101, 133, 166, 200]):
  - radial A (autocatalyst): peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.929, rim/outside 2.15 (aggregate of 338 individuals; 33/338 membrane-like individually; rim level 0.552)
  - radial M (membrane): peak at rho=1.05 (in the peak band 0.5-1.5), rim/core 1.59, rim/outside 1.63 (aggregate of 338 individuals; 249/338 membrane-like individually; rim level 0.327)  MEMBRANE-LIKE
  - radial X (food): peak at rho=2.35 (OUTSIDE the peak band 0.5-1.5), rim/core 1.72, rim/outside 0.789 (aggregate of 338 individuals; 24/338 membrane-like individually; rim level 0.185)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): M (membrane)
- membrane-like channels per top track at mid-life: #1748 (t=5900, R_eq 2.82): ['M (membrane)']; #2339 (t=7250, R_eq 2.65): none; #1544 (t=5150, R_eq 3.39): ['M (membrane)']; #38 (t=1500, R_eq 3.09): none

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 4 of 338 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
