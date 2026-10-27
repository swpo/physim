# Evidence pack: cips-gene (seed 5)

- world: `../../20261027T0027-c48-cips-gene-nucleation-breaks-heredity/world.py`, family `catalysis-induced-phase-separation`
- parent: collective/contrib/20261026T1100-c40-cips-layered-divide-claim; mutation: c48: the enzyme turnover d(e0-e) replaced by inactivation -d e and fuel-powered reactivation r F i of a diffusing inactive enzyme i (consumes fuel); c40's layered world: an amphiphile s made only by catalysis, adsorbing at the enzyme interface (drift up grad 4e(1-e)), decaying
- run: 201 frames x 1000 steps x dt 0.1 = time 20000; grid [192, 192]; wall 1720s; status ok
- command: `python -m labkit.run collective/contrib/20261027T0027-c48-cips-gene-nucleation-breaks-heredity/world.py --out collective/contrib/c57-w9/twin --seeds 5 --frames 200 --no-movie`
- segmentation: matter > 0.50 of robust range [0.0221, 0.9744], min area 6 px

## Measurements
- components: final 10, mean 8.5, max 11; occupancy final 0.06
- tracks: 42; persistent (alive >= 50% of run): 2; longest 112 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 2.01 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [10, 10, 10], H1 [0, 0, 0]
- motion: 3 long-lived tracks moved >= 1 body length; max speed 0.0029/time; max body lengths 1.9
- replication (lineage window K = 20 frames = time 2000, default): splits 18, persistent splits 10 (0 more failed only because the siblings re-merged within K), max generation 3, merges 0, merge/split ratio 0, nucleations 6
- channel total drift (end/start - 1): [-0.0151, 0.3123, -0.054, None, None, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 12 at frame 94: holes 0, rim-vs-core 0.56, rim-vs-outside 1.13, heterogeneity 0.11; core [0.982, 0.942, 0.033, 0.084, 1.0, 0.0] rim [0.776, 0.705, 0.209, 0.518, 1.0, 0.0]
  - track 10 at frame 94: holes 0, rim-vs-core 0.37, rim-vs-outside 1.24, heterogeneity 0.11; core [0.982, 0.939, 0.049, 0.082, 0.0, 1.0] rim [0.847, 0.796, 0.146, 0.374, 0.0, 0.999]
  - track 14 at frame 97: holes 0, rim-vs-core 0.59, rim-vs-outside 1.15, heterogeneity 0.11; core [0.985, 0.951, 0.04, 0.084, 0.0, 1.0] rim [0.769, 0.705, 0.223, 0.538, 0.0, 0.999]
  - track 34 at frame 188: holes 0, rim-vs-core 0.60, rim-vs-outside 1.16, heterogeneity 0.12; core [0.987, 0.954, 0.043, 0.082, 1.0, 0.0] rim [0.762, 0.699, 0.23, 0.545, 0.997, 0.0]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 51 components >= 12 px at frames [34, 67, 101, 133, 166, 200]):
  - radial e: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.852, rim/outside 25 (aggregate of 51 individuals; 0/51 membrane-like individually; rim level 0.821)
  - radial p: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.856, rim/outside 11 (aggregate of 51 individuals; 0/51 membrane-like individually; rim level 0.807)
  - radial F: peak at rho=2.45 (OUTSIDE the peak band 0.5-1.5), rim/core 20.5, rim/outside 0.637 (aggregate of 51 individuals; 0/51 membrane-like individually; rim level 0.479)
  - radial s: peak at rho=0.95 (in the peak band 0.5-1.5), rim/core 3.38, rim/outside 13.3 (aggregate of 51 individuals; 44/51 membrane-like individually; rim level 0.44)  MEMBRANE-LIKE
  - radial g1: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.837, rim/outside 18.8 (aggregate of 51 individuals; 0/51 membrane-like individually; rim level 0.242)
  - radial g2: peak at rho=0.25 (OUTSIDE the peak band 0.5-1.5), rim/core 0.876, rim/outside 36.2 (aggregate of 51 individuals; 0/51 membrane-like individually; rim level 0.612)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): s
- membrane-like channels per top track at mid-life: #12 (t=9400, R_eq 8.46): ['s']; #10 (t=9400, R_eq 8.21): ['s']; #14 (t=9700, R_eq 8.04): ['s']; #34 (t=18800, R_eq 7.78): ['s']

## Warnings
- none

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
