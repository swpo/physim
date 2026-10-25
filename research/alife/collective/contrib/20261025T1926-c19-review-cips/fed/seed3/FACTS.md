# Evidence pack: cips-fuel (seed 3)

- world: `../../../20261025T1845-c23-cips-metabolic-claim/world.py`, family `catalysis-induced-phase-separation`
- parent: collective/contrib/20261025T1650-c00-q-cips-fuel-limited-condensates; mutation: Cotton et al. CIPS (enzyme drifts up its own product) with the fuel made a consumed, regrowing field
- run: 301 frames x 100 steps x dt 0.1 = time 3000; grid [256, 256]; wall 317s; status ok
- command: `python -m labkit.run collective/contrib/20261025T1845-c23-cips-metabolic-claim/world.py --out collective/contrib/20261025T1926-c19-review-cips/fed/seed3 --seeds 3 --frames 300 --no-movie`
- segmentation: matter > 0.50 of robust range [-0.0, 0.9988], min area 6 px

## Measurements
- components: final 182, mean 206.5, max 301; occupancy final 0.14
- tracks: 417; persistent (alive >= 50% of run): 202; longest 282 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 9.83 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [184, 183, 179], H1 [0, 0, 0]
- motion: 1 long-lived tracks moved >= 1 body length; max speed 0.00206/time; max body lengths 1.0
- replication (lineage window K = 20 frames = time 200, default): splits 0, persistent splits 0 (0 more failed only because the siblings re-merged within K), max generation 0, merges 110, merge/split ratio n/a, nucleations 307
- channel total drift (end/start - 1): [0.0, -0.2191, 0.1509]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 0 at frame 161: holes 0, rim-vs-core 0.30, rim-vs-outside 0.50, heterogeneity 0.10; core [0.972, 0.846, 0.197] rim [0.754, 0.679, 0.324]
  - track 1 at frame 161: holes 0, rim-vs-core 0.31, rim-vs-outside 0.51, heterogeneity 0.10; core [0.976, 0.869, 0.139] rim [0.762, 0.689, 0.278]
  - track 2 at frame 161: holes 0, rim-vs-core 0.29, rim-vs-outside 0.51, heterogeneity 0.09; core [0.981, 0.877, 0.147] rim [0.795, 0.703, 0.283]
  - track 5 at frame 161: holes 0, rim-vs-core 0.30, rim-vs-outside 0.50, heterogeneity 0.10; core [0.971, 0.842, 0.172] rim [0.757, 0.679, 0.295]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 1303 components >= 12 px at frames [50, 101, 151, 199, 250, 300]):
  - radial e: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.947, rim/outside 46.4 (aggregate of 1303 individuals; 0/1303 membrane-like individually; rim level 0.938)
  - radial p: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.877, rim/outside 3.9 (aggregate of 1303 individuals; 0/1303 membrane-like individually; rim level 0.817)
  - radial F: peak at rho=2.45 (OUTSIDE the peak band 0.5-1.5), rim/core 5.47, rim/outside 0.676 (aggregate of 1303 individuals; 0/1303 membrane-like individually; rim level 0.445)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #0 (t=1610, R_eq 3.24): none; #1 (t=1610, R_eq 3.52): none; #2 (t=1610, R_eq 3.43): none; #5 (t=1610, R_eq 3.24): none

## Warnings
- none

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
