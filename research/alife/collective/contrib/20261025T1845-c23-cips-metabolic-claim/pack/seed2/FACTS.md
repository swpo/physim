# Evidence pack: cips-fuel (seed 2)

- world: `../world.py`, family `catalysis-induced-phase-separation`
- parent: collective/contrib/20261025T1650-c00-q-cips-fuel-limited-condensates; mutation: Cotton et al. CIPS (enzyme drifts up its own product) with the fuel made a consumed, regrowing field
- run: 301 frames x 100 steps x dt 0.1 = time 3000; grid [256, 256]; wall 248s; status ok
- command: `python -m labkit.run collective/contrib/20261025T1845-c23-cips-metabolic-claim/world.py --out collective/contrib/20261025T1845-c23-cips-metabolic-claim/fed2 --seeds 2 --frames 300 --no-movie`
- segmentation: matter > 0.50 of robust range [-0.0, 0.9989], min area 6 px

## Measurements
- components: final 184, mean 207.9, max 305; occupancy final 0.14
- tracks: 429; persistent (alive >= 50% of run): 202; longest 282 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 8.33 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [184, 184, 183], H1 [0, 0, 0]
- motion: 1 long-lived tracks moved >= 1 body length; max speed 0.00171/time; max body lengths 1.1
- replication (lineage window K = 20 frames = time 200, default): splits 0, persistent splits 0 (0 more failed only because the siblings re-merged within K), max generation 0, merges 113, merge/split ratio n/a, nucleations 316
- channel total drift (end/start - 1): [0.0, -0.2193, 0.1513]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 0 at frame 161: holes 0, rim-vs-core 0.29, rim-vs-outside 0.50, heterogeneity 0.10; core [0.973, 0.842, 0.177] rim [0.77, 0.681, 0.299]
  - track 2 at frame 161: holes 0, rim-vs-core 0.33, rim-vs-outside 0.50, heterogeneity 0.11; core [0.979, 0.89, 0.07] rim [0.763, 0.7, 0.226]
  - track 3 at frame 161: holes 0, rim-vs-core 0.30, rim-vs-outside 0.52, heterogeneity 0.10; core [0.981, 0.894, 0.138] rim [0.792, 0.713, 0.285]
  - track 5 at frame 161: holes 0, rim-vs-core 0.31, rim-vs-outside 0.51, heterogeneity 0.10; core [0.977, 0.868, 0.134] rim [0.766, 0.691, 0.272]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 1314 components >= 12 px at frames [50, 101, 151, 199, 250, 300]):
  - radial e: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.95, rim/outside 45.6 (aggregate of 1314 individuals; 0/1314 membrane-like individually; rim level 0.94)
  - radial p: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.876, rim/outside 3.96 (aggregate of 1314 individuals; 0/1314 membrane-like individually; rim level 0.813)
  - radial F: peak at rho=2.45 (OUTSIDE the peak band 0.5-1.5), rim/core 5.21, rim/outside 0.678 (aggregate of 1314 individuals; 0/1314 membrane-like individually; rim level 0.454)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #0 (t=1610, R_eq 3.19): none; #2 (t=1610, R_eq 3.87): none; #3 (t=1610, R_eq 3.61): none; #5 (t=1610, R_eq 3.52): none

## Warnings
- none

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
