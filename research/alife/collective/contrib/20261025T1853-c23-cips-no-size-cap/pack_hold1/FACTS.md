# Evidence pack: cips-fuel (seed 1)

- world: `../world.py`, family `catalysis-induced-phase-separation`
- parent: collective/contrib/20261025T1650-c00-q-cips-fuel-limited-condensates; mutation: Cotton et al. CIPS (enzyme drifts up its own product) with the fuel made a consumed, regrowing field
- run: 401 frames x 100 steps x dt 0.1 = time 4000; grid [256, 256]; wall 300s; status ok
- command: `python -m labkit.run collective/contrib/20261025T1853-c23-cips-no-size-cap/world.py --out collective/contrib/20261025T1853-c23-cips-no-size-cap/hold1 --seeds 1 --frames 400 --no-movie`
- segmentation: matter > 0.50 of robust range [-0.0011, 1.0026], min area 6 px

## Measurements
- components: final 142, mean 203.9, max 403; occupancy final 0.14
- tracks: 646; persistent (alive >= 50% of run): 161; longest 393 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 7.67 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [143, 143, 142], H1 [0, 0, 0]
- motion: 11 long-lived tracks moved >= 1 body length; max speed 0.00699/time; max body lengths 1.4
- replication (lineage window K = 20 frames = time 200, default): splits 0, persistent splits 0 (0 more failed only because the siblings re-merged within K), max generation 0, merges 232, merge/split ratio n/a, nucleations 414
- channel total drift (end/start - 1): [0.0, -0.2114, 0.0]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 4 at frame 205: holes 0, rim-vs-core 0.24, rim-vs-outside 0.57, heterogeneity 0.07; core [0.99, 0.73, 0.0] rim [0.801, 0.58, 0.0]
  - track 8 at frame 205: holes 0, rim-vs-core 0.15, rim-vs-outside 0.50, heterogeneity 0.04; core [0.992, 0.68, 0.0] rim [0.89, 0.574, 0.0]
  - track 13 at frame 205: holes 0, rim-vs-core 0.21, rim-vs-outside 0.55, heterogeneity 0.06; core [0.992, 0.752, 0.0] rim [0.84, 0.606, 0.0]
  - track 22 at frame 205: holes 0, rim-vs-core 0.16, rim-vs-outside 0.52, heterogeneity 0.05; core [0.992, 0.687, 0.0] rim [0.871, 0.577, 0.0]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 1140 components >= 12 px at frames [67, 134, 202, 266, 333, 400]):
  - radial e: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.971, rim/outside 59.1 (aggregate of 1140 individuals; 0/1140 membrane-like individually; rim level 0.966)
  - radial p: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.861, rim/outside 4.28 (aggregate of 1140 individuals; 0/1140 membrane-like individually; rim level 0.749)
  - radial F: flat profile (no radial structure; level 0; aggregate of 1140 individuals)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #4 (t=2050, R_eq 3.24): none; #8 (t=2050, R_eq 2.59): none; #13 (t=2050, R_eq 3.24): none; #22 (t=2050, R_eq 2.65): none

## Warnings
- none

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
