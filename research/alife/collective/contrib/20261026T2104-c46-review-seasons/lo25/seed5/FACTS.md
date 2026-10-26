# Evidence pack: cips-layered-divide (seed 5)

- world: `../../../20261026T1526-c44-cips-seasons-negative/world.py`, family `catalysis-induced-phase-separation`
- parent: collective/contrib/20261026T1025-c40-cips-turnover-divide-claim; mutation: c40 dividing CIPS world plus an amphiphile s made only by catalysis, adsorbing at the enzyme interface (drift up grad 4e(1-e)), decaying
- run: 201 frames x 1000 steps x dt 0.1 = time 20000; grid [128, 128]; wall 443s; status ok
- command: `python -m labkit.run collective/contrib/20261026T1526-c44-cips-seasons-negative/world.py --out collective/contrib/20261026T2104-c46-review-seasons/lo25/seed5 --seeds 5 --size 128 128 --frames 200 --no-movie`
- segmentation: matter > 0.50 of robust range [0.0234, 0.9727], min area 6 px

## Measurements
- components: final 6, mean 5.5, max 6; occupancy final 0.05
- tracks: 8; persistent (alive >= 50% of run): 6; longest 199 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 4.66 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [6, 6, 6], H1 [0, 0, 0]
- motion: 4 long-lived tracks moved >= 1 body length; max speed 0.00153/time; max body lengths 1.8
- replication (lineage window K = 20 frames = time 2000, default): splits 2, persistent splits 2 (0 more failed only because the siblings re-merged within K), max generation 1, merges 0, merge/split ratio 0, nucleations 4
- channel total drift (end/start - 1): [-0.0, -0.7917, 0.1846, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 0 at frame 101: holes 0, rim-vs-core 0.56, rim-vs-outside 0.63, heterogeneity 0.16; core [0.991, 0.963, 0.126, 0.08] rim [0.774, 0.713, 0.308, 0.488]
  - track 3 at frame 104: holes 0, rim-vs-core 0.43, rim-vs-outside 0.73, heterogeneity 0.17; core [0.989, 0.958, 0.094, 0.096] rim [0.828, 0.769, 0.245, 0.419]
  - track 4 at frame 119: holes 0, rim-vs-core 0.37, rim-vs-outside 0.40, heterogeneity 0.10; core [0.918, 0.592, 0.0, 0.054] rim [0.698, 0.44, 0.048, 0.3]
  - track 5 at frame 119: holes 0, rim-vs-core 0.37, rim-vs-outside 0.41, heterogeneity 0.10; core [0.92, 0.593, 0.0, 0.053] rim [0.696, 0.44, 0.05, 0.301]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 34 components >= 12 px at frames [34, 67, 101, 133, 166, 200]):
  - radial e: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.923, rim/outside 23.4 (aggregate of 34 individuals; 0/34 membrane-like individually; rim level 0.897)
  - radial p: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.888, rim/outside 12.3 (aggregate of 34 individuals; 0/34 membrane-like individually; rim level 0.757)
  - radial F: peak at rho=2.45 (OUTSIDE the peak band 0.5-1.5), rim/core 10.4, rim/outside 0.652 (aggregate of 34 individuals; 0/34 membrane-like individually; rim level 0.417)
  - radial s: peak at rho=1.05 (in the peak band 0.5-1.5), rim/core 5.72, rim/outside 22.3 (aggregate of 34 individuals; 33/34 membrane-like individually; rim level 0.55)  MEMBRANE-LIKE
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): s
- membrane-like channels per top track at mid-life: #0 (t=10100, R_eq 7.72): ['s']; #3 (t=10400, R_eq 8.35): ['s']; #4 (t=11900, R_eq 6.38): ['s']; #5 (t=11900, R_eq 6.33): ['s']

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
