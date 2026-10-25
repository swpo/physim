# Evidence pack: cips-fuel (seed 0)

- world: `../world.py`, family `catalysis-induced-phase-separation`
- parent: collective/contrib/20261025T1650-c00-q-cips-fuel-limited-condensates; mutation: Cotton et al. CIPS (enzyme drifts up its own product) with the fuel made a consumed, regrowing field
- run: 251 frames x 100 steps x dt 0.1 = time 2500; grid [256, 256]; wall 224s; status ok
- command: `python -m labkit.run collective/contrib/20261025T1845-c23-cips-metabolic-claim/world.py --out collective/contrib/20261025T1845-c23-cips-metabolic-claim/cut17 --seeds 0 --frames 250 --no-movie`
- segmentation: matter > 0.50 of robust range [-0.0, 0.9988], min area 6 px

## Measurements
- components: final 188, mean 208.7, max 301; occupancy final 0.14
- tracks: 414; persistent (alive >= 50% of run): 200; longest 233 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 9.17 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [192, 190, 188], H1 [0, 0, 0]
- motion: 0 long-lived tracks moved >= 1 body length; max speed 0/time; max body lengths 1.0
- replication (lineage window K = 20 frames = time 200, default): splits 0, persistent splits 0 (0 more failed only because the siblings re-merged within K), max generation 0, merges 106, merge/split ratio n/a, nucleations 308
- channel total drift (end/start - 1): [0.0, -0.2165, 0.1365]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 0 at frame 134: holes 0, rim-vs-core 0.34, rim-vs-outside 0.51, heterogeneity 0.11; core [0.971, 0.863, 0.203] rim [0.725, 0.674, 0.346]
  - track 1 at frame 134: holes 0, rim-vs-core 0.29, rim-vs-outside 0.51, heterogeneity 0.10; core [0.976, 0.871, 0.18] rim [0.775, 0.7, 0.311]
  - track 3 at frame 134: holes 0, rim-vs-core 0.28, rim-vs-outside 0.50, heterogeneity 0.09; core [0.984, 0.902, 0.17] rim [0.82, 0.725, 0.31]
  - track 4 at frame 134: holes 0, rim-vs-core 0.31, rim-vs-outside 0.51, heterogeneity 0.10; core [0.977, 0.885, 0.144] rim [0.771, 0.705, 0.285]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 1345 components >= 12 px at frames [42, 84, 126, 166, 208, 250]):
  - radial e: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.947, rim/outside 44.5 (aggregate of 1345 individuals; 0/1345 membrane-like individually; rim level 0.938)
  - radial p: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.878, rim/outside 3.9 (aggregate of 1345 individuals; 0/1345 membrane-like individually; rim level 0.816)
  - radial F: peak at rho=2.45 (OUTSIDE the peak band 0.5-1.5), rim/core 4.78, rim/outside 0.686 (aggregate of 1345 individuals; 0/1345 membrane-like individually; rim level 0.458)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #0 (t=1340, R_eq 3.43): none; #1 (t=1340, R_eq 3.34): none; #3 (t=1340, R_eq 3.43): none; #4 (t=1340, R_eq 3.57): none

## Warnings
- none

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
