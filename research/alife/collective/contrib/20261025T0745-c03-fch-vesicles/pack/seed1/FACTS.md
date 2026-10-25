# Evidence pack: fch-vesicles (seed 1)

- world: `../../world.py`, family `fch-bilayer`
- parent: None; mutation: new class: functionalized Cahn-Hilliard (Promislow/Gavish) with an asymmetric double well, O(1) functionalization
- run: 101 frames x 200 steps x dt 0.02 = time 400; grid [128, 128]; wall 36s; status ok
- command: `python -m labkit.run collective/contrib/20261025T0745-c03-fch-vesicles/world.py --out collective/contrib/20261025T0745-c03-fch-vesicles/pack --seeds 0 1 --frames 100 --no-movie`
- segmentation: matter > 0.24 of robust range [0.1296, 1.6886], min area 6 px

## Measurements
- components: final 1, mean 1.0, max 1; occupancy final 0.14
- tracks: 2; persistent (alive >= 50% of run): 1; longest 100 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 23.06 (1 = constant size)
- enclosures: components with a hole mean 0.07, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [2, 1, 1], H1 [2, 1, 0]
- motion: 0 long-lived tracks moved >= 1 body length; max speed 0/time; max body lengths 0.0
- replication (lineage window K = 20 frames = time 80, default): splits 0, persistent splits 0 (0 more failed only because the siblings re-merged within K), max generation 0, merges 0, merge/split ratio n/a, nucleations 1
- channel total drift (end/start - 1): [0.0]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 1 at frame 51: holes 0, rim-vs-core 0.01, rim-vs-outside 0.69, heterogeneity 0.17; core [0.74] rim [0.728]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 6 components >= 12 px at frames [17, 33, 50, 67, 83, 100]):
  - radial amphiphile u (shifted, u + 1.6): peak at rho=0.85 (in the peak band 0.5-1.5), rim/core 1.24, rim/outside 59.6 (aggregate of 6 individuals; 0/6 membrane-like individually; rim level 0.943)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #1 (t=204, R_eq 27.31): none; #0 (t=0, R_eq 1.38): none

## Warnings
- none

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
