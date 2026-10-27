# Evidence pack: cips-gene (seed 5)

- world: `../../20261026T2334-c48-cips-turnover-window/world.py`, family `catalysis-induced-phase-separation`
- parent: collective/contrib/20261026T1100-c40-cips-layered-divide-claim; mutation: c48: the enzyme turnover d(e0-e) replaced by inactivation -d e and fuel-powered reactivation r F i of a diffusing inactive enzyme i (consumes fuel); c40's layered world: an amphiphile s made only by catalysis, adsorbing at the enzyme interface (drift up grad 4e(1-e)), decaying
- run: 101 frames x 1000 steps x dt 0.1 = time 10000; grid [192, 192]; wall 840s; status ok
- command: `python -m labkit.run collective/contrib/20261026T2334-c48-cips-turnover-window/world.py --out collective/contrib/c57-w5/rerun_b1.0 --seeds 5 --frames 100 --no-movie`
- segmentation: matter > 0.50 of robust range [0.0222, 0.9753], min area 6 px

## Measurements
- components: final 13, mean 9.0, max 13; occupancy final 0.07
- tracks: 20; persistent (alive >= 50% of run): 9; longest 99 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 6.15 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [14, 13, 13], H1 [0, 0, 0]
- motion: 3 long-lived tracks moved >= 1 body length; max speed 0.00313/time; max body lengths 1.8
- replication (lineage window K = 20 frames = time 2000, default): splits 7, persistent splits 6 (0 more failed only because the siblings re-merged within K), max generation 2, merges 0, merge/split ratio 0, nucleations 6
- channel total drift (end/start - 1): [-0.0233, 0.4393, -0.0729, None, None, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 2 at frame 51: holes 0, rim-vs-core 0.70, rim-vs-outside 0.97, heterogeneity 0.11; core [0.963, 0.935, 0.196, 0.111, 0.0, 1.0] rim [0.696, 0.678, 0.357, 0.678, 0.0, 1.0]
  - track 4 at frame 38: holes 0, rim-vs-core 0.59, rim-vs-outside 1.17, heterogeneity 0.11; core [0.982, 0.94, 0.027, 0.09, 0.999, 0.0] rim [0.766, 0.694, 0.209, 0.541, 0.999, 0.0]
  - track 7 at frame 67: holes 0, rim-vs-core 0.61, rim-vs-outside 1.17, heterogeneity 0.11; core [0.983, 0.945, 0.035, 0.088, 1.0, 0.0] rim [0.76, 0.693, 0.221, 0.562, 0.999, 0.0]
  - track 14 at frame 85: holes 0, rim-vs-core 0.57, rim-vs-outside 1.15, heterogeneity 0.11; core [0.989, 0.956, 0.041, 0.081, 1.0, 0.0] rim [0.778, 0.708, 0.223, 0.514, 0.999, 0.0]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 58 components >= 12 px at frames [17, 33, 50, 67, 83, 100]):
  - radial e: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.884, rim/outside 29.6 (aggregate of 58 individuals; 0/58 membrane-like individually; rim level 0.858)
  - radial p: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.873, rim/outside 11.4 (aggregate of 58 individuals; 0/58 membrane-like individually; rim level 0.833)
  - radial F: peak at rho=2.45 (OUTSIDE the peak band 0.5-1.5), rim/core 16.1, rim/outside 0.648 (aggregate of 58 individuals; 0/58 membrane-like individually; rim level 0.488)
  - radial s: peak at rho=1.05 (in the peak band 0.5-1.5), rim/core 4.24, rim/outside 16.9 (aggregate of 58 individuals; 51/58 membrane-like individually; rim level 0.517)  MEMBRANE-LIKE
  - radial g1: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.884, rim/outside 43.5 (aggregate of 58 individuals; 0/58 membrane-like individually; rim level 0.784)
  - radial g2: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.991, rim/outside 11.2 (aggregate of 58 individuals; 0/58 membrane-like individually; rim level 0.102)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): s
- membrane-like channels per top track at mid-life: #2 (t=5100, R_eq 5.81): ['s']; #4 (t=3800, R_eq 8.41): ['s']; #7 (t=6700, R_eq 8.23): ['s']; #14 (t=8500, R_eq 7.63): ['s']

## Warnings
- none

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
