# Evidence pack: cips-fuel (seed 5)

- world: `../world.py`, family `catalysis-induced-phase-separation`
- parent: collective/contrib/20261025T1650-c00-q-cips-fuel-limited-condensates; mutation: Cotton et al. CIPS (enzyme drifts up its own product) with the fuel made a consumed, regrowing field
- run: 301 frames x 100 steps x dt 0.1 = time 3000; grid [256, 256]; wall 453s; status ok
- command: `python -m labkit.run /tmp/c20nc/world.py --out /tmp/c20nc/hold --seeds 5 --frames 300 --no-movie`
- segmentation: matter > 0.50 of robust range [-0.0011, 1.0027], min area 6 px

## Measurements
- components: final 165, mean 222.0, max 399; occupancy final 0.14
- tracks: 634; persistent (alive >= 50% of run): 182; longest 292 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 7.88 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [167, 167, 165], H1 [0, 0, 0]
- motion: 6 long-lived tracks moved >= 1 body length; max speed 0.00909/time; max body lengths 1.3
- replication (lineage window K = 20 frames = time 200, default): splits 1, persistent splits 0 (0 more failed only because the siblings re-merged within K), max generation 0, merges 212, merge/split ratio 212, nucleations 420
- channel total drift (end/start - 1): [0.0, -0.1978, 0.0]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 10 at frame 156: holes 0, rim-vs-core 0.18, rim-vs-outside 0.53, heterogeneity 0.06; core [0.993, 0.72, 0.0] rim [0.861, 0.594, 0.0]
  - track 13 at frame 156: holes 0, rim-vs-core 0.23, rim-vs-outside 0.56, heterogeneity 0.07; core [0.991, 0.794, 0.0] rim [0.825, 0.629, 0.0]
  - track 15 at frame 156: holes 0, rim-vs-core 0.23, rim-vs-outside 0.57, heterogeneity 0.06; core [0.992, 0.786, 0.0] rim [0.837, 0.617, 0.0]
  - track 16 at frame 156: holes 0, rim-vs-core 0.14, rim-vs-outside 0.67, heterogeneity 0.07; core [0.987, 0.749, 0.0] rim [0.874, 0.673, 0.0]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 1277 components >= 12 px at frames [50, 101, 151, 199, 250, 300]):
  - radial e: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.971, rim/outside 59 (aggregate of 1277 individuals; 0/1277 membrane-like individually; rim level 0.966)
  - radial p: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.864, rim/outside 4.09 (aggregate of 1277 individuals; 0/1277 membrane-like individually; rim level 0.756)
  - radial F: flat profile (no radial structure; level 0; aggregate of 1277 individuals)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #10 (t=1560, R_eq 2.76): none; #13 (t=1560, R_eq 3.48): none; #15 (t=1560, R_eq 3.43): none; #16 (t=1560, R_eq 3.34): none

## Warnings
- none

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
