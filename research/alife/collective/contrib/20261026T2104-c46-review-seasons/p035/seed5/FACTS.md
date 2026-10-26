# Evidence pack: cips-layered-divide (seed 5)

- world: `../../../20261026T1526-c44-cips-seasons-negative/world.py`, family `catalysis-induced-phase-separation`
- parent: collective/contrib/20261026T1025-c40-cips-turnover-divide-claim; mutation: c40 dividing CIPS world plus an amphiphile s made only by catalysis, adsorbing at the enzyme interface (drift up grad 4e(1-e)), decaying
- run: 201 frames x 1000 steps x dt 0.1 = time 20000; grid [128, 128]; wall 433s; status ok
- command: `python -m labkit.run collective/contrib/20261026T1526-c44-cips-seasons-negative/world.py --out collective/contrib/20261026T2104-c46-review-seasons/p035/seed5 --seeds 5 --size 128 128 --frames 200 --no-movie`
- segmentation: matter > 0.50 of robust range [0.0229, 0.9732], min area 6 px

## Measurements
- components: final 0, mean 5.3, max 6; occupancy final 0.00
- tracks: 44; persistent (alive >= 50% of run): 0; longest 78 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 0.00 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [6, 6, 6], H1 [0, 0, 0]
- motion: 1 long-lived tracks moved >= 1 body length; max speed 0.00401/time; max body lengths 1.0
- replication (lineage window K = 20 frames = time 2000, default): splits 2, persistent splits 2 (0 more failed only because the siblings re-merged within K), max generation 1, merges 0, merge/split ratio 0, nucleations 40
- channel total drift (end/start - 1): [-0.0, -0.9793, -0.869, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 0 at frame 40: holes 0, rim-vs-core 0.56, rim-vs-outside 0.61, heterogeneity 0.16; core [0.984, 0.945, 0.303, 0.093] rim [0.768, 0.698, 0.449, 0.522]
  - track 3 at frame 44: holes 0, rim-vs-core 0.45, rim-vs-outside 0.67, heterogeneity 0.16; core [0.982, 0.943, 0.306, 0.084] rim [0.811, 0.747, 0.432, 0.424]
  - track 4 at frame 59: holes 0, rim-vs-core 0.38, rim-vs-outside 0.73, heterogeneity 0.16; core [0.982, 0.936, 0.314, 0.085] rim [0.835, 0.78, 0.403, 0.385]
  - track 5 at frame 59: holes 0, rim-vs-core 0.50, rim-vs-outside 0.62, heterogeneity 0.15; core [0.989, 0.958, 0.321, 0.08] rim [0.794, 0.722, 0.453, 0.456]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 28 components >= 12 px at frames [34, 67, 101, 133, 166]):
  - radial e: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.92, rim/outside 36.7 (aggregate of 28 individuals; 0/28 membrane-like individually; rim level 0.904)
  - radial p: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.891, rim/outside 12.9 (aggregate of 28 individuals; 0/28 membrane-like individually; rim level 0.867)
  - radial F: peak at rho=2.45 (OUTSIDE the peak band 0.5-1.5), rim/core 2.35, rim/outside 0.769 (aggregate of 28 individuals; 0/28 membrane-like individually; rim level 0.645)
  - radial s: peak at rho=1.05 (in the peak band 0.5-1.5), rim/core 4.28, rim/outside 17.3 (aggregate of 28 individuals; 27/28 membrane-like individually; rim level 0.485)  MEMBRANE-LIKE
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): s
- membrane-like channels per top track at mid-life: #0 (t=4000, R_eq 8.44): ['s']; #3 (t=4400, R_eq 8.44): ['s']; #4 (t=5900, R_eq 8.44): ['s']; #5 (t=5900, R_eq 7.72): ['s']

## Warnings
- no components at the end: matter died out or fell below threshold
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
