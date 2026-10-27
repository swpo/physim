# Evidence pack: cips-gene (seed 5)

- world: `../../20261027T0027-c48-cips-gene-nucleation-breaks-heredity/world.py`, family `catalysis-induced-phase-separation`
- parent: collective/contrib/20261026T1100-c40-cips-layered-divide-claim; mutation: c48: the enzyme turnover d(e0-e) replaced by inactivation -d e and fuel-powered reactivation r F i of a diffusing inactive enzyme i (consumes fuel); c40's layered world: an amphiphile s made only by catalysis, adsorbing at the enzyme interface (drift up grad 4e(1-e)), decaying
- run: 201 frames x 1000 steps x dt 0.1 = time 20000; grid [192, 192]; wall 1734s; status ok
- command: `python -m labkit.run collective/contrib/20261027T0027-c48-cips-gene-nucleation-breaks-heredity/world.py --out collective/contrib/c57-w9/trait --seeds 5 --frames 200 --no-movie`
- segmentation: matter > 0.50 of robust range [0.0267, 0.9711], min area 6 px

## Measurements
- components: final 1, mean 4.5, max 7; occupancy final 0.01
- tracks: 23; persistent (alive >= 50% of run): 1; longest 131 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 2.29 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [1, 1, 1], H1 [0, 0, 0]
- motion: 1 long-lived tracks moved >= 1 body length; max speed 0.0034/time; max body lengths 1.5
- replication (lineage window K = 20 frames = time 2000, default): splits 8, persistent splits 2 (0 more failed only because the siblings re-merged within K), max generation 2, merges 0, merge/split ratio 0, nucleations 7
- channel total drift (end/start - 1): [-0.0015, -0.0187, -0.005, None, None, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 0 at frame 67: holes 0, rim-vs-core 0.57, rim-vs-outside 1.14, heterogeneity 0.11; core [0.989, 0.969, 0.014, 0.093, 0.0, 1.0] rim [0.795, 0.739, 0.174, 0.547, 0.0, 1.0]
  - track 1 at frame 47: holes 0, rim-vs-core 0.61, rim-vs-outside 1.17, heterogeneity 0.12; core [0.986, 0.964, 0.02, 0.092, 0.0, 1.0] rim [0.77, 0.725, 0.186, 0.587, 0.0, 1.0]
  - track 2 at frame 35: holes 0, rim-vs-core 0.62, rim-vs-outside 1.15, heterogeneity 0.11; core [0.988, 0.967, 0.019, 0.093, 0.0, 1.0] rim [0.777, 0.727, 0.186, 0.592, 0.0, 1.0]
  - track 10 at frame 96: holes 0, rim-vs-core 0.61, rim-vs-outside 1.15, heterogeneity 0.11; core [0.986, 0.949, 0.008, 0.098, 1.0, 0.0] rim [0.773, 0.709, 0.152, 0.601, 0.996, 0.0]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 24 components >= 12 px at frames [34, 67, 101, 133, 166, 200]):
  - radial e: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.83, rim/outside 29.6 (aggregate of 24 individuals; 0/24 membrane-like individually; rim level 0.809)
  - radial p: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.848, rim/outside 11.5 (aggregate of 24 individuals; 0/24 membrane-like individually; rim level 0.814)
  - radial F: peak at rho=2.45 (OUTSIDE the peak band 0.5-1.5), rim/core 33.7, rim/outside 0.604 (aggregate of 24 individuals; 0/24 membrane-like individually; rim level 0.453)
  - radial s: peak at rho=0.95 (in the peak band 0.5-1.5), rim/core 3.32, rim/outside 13.7 (aggregate of 24 individuals; 22/24 membrane-like individually; rim level 0.428)  MEMBRANE-LIKE
  - radial g1: peak at rho=0.25 (OUTSIDE the peak band 0.5-1.5), rim/core 0.658, rim/outside 13.9 (aggregate of 24 individuals; 0/24 membrane-like individually; rim level 0.16)
  - radial g2: peak at rho=0.25 (OUTSIDE the peak band 0.5-1.5), rim/core 0.909, rim/outside 49.9 (aggregate of 24 individuals; 0/24 membrane-like individually; rim level 0.639)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): s
- membrane-like channels per top track at mid-life: #0 (t=6700, R_eq 7.84): ['s']; #1 (t=4700, R_eq 7.96): ['s']; #2 (t=3500, R_eq 7.78): ['s']; #10 (t=9600, R_eq 8.63): ['s']

## Warnings
- none

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
