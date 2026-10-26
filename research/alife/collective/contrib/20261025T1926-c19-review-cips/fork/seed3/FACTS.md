# Evidence pack: cips-fuel (seed 3)

- world: `../../../20261025T1845-c23-cips-metabolic-claim/world.py`, family `catalysis-induced-phase-separation`
- parent: collective/contrib/20261025T1650-c00-q-cips-fuel-limited-condensates; mutation: Cotton et al. CIPS (enzyme drifts up its own product) with the fuel made a consumed, regrowing field
- run: 301 frames x 100 steps x dt 0.1 = time 3000; grid [256, 256]; wall 316s; status ok
- command: `python -m labkit.run collective/contrib/20261025T1845-c23-cips-metabolic-claim/world.py --out collective/contrib/20261025T1926-c19-review-cips/fork/seed3 --seeds 3 --frames 300 --no-movie`
- segmentation: matter > 0.50 of robust range [0.0001, 0.9974], min area 6 px

## Measurements
- components: final 0, mean 111.0, max 301; occupancy final 0.00
- tracks: 383; persistent (alive >= 50% of run): 0; longest 137 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 0.00 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [12, 5, 1], H1 [9, 6, 0]
- motion: 0 long-lived tracks moved >= 1 body length; max speed 0/time; max body lengths 1.0
- replication (lineage window K = 20 frames = time 200, default): splits 1, persistent splits 0 (0 more failed only because the siblings re-merged within K), max generation 0, merges 74, merge/split ratio 74, nucleations 307
- channel total drift (end/start - 1): [0.0, -1.0, -1.0]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 1 at frame 88: holes 0, rim-vs-core 0.27, rim-vs-outside 0.49, heterogeneity 0.08; core [0.982, 0.938, 0.638] rim [0.782, 0.766, 0.7]
  - track 2 at frame 88: holes 0, rim-vs-core 0.30, rim-vs-outside 0.50, heterogeneity 0.09; core [0.98, 0.934, 0.644] rim [0.756, 0.753, 0.709]
  - track 15 at frame 88: holes 0, rim-vs-core 0.27, rim-vs-outside 0.49, heterogeneity 0.09; core [0.986, 0.955, 0.612] rim [0.793, 0.784, 0.678]
  - track 28 at frame 91: holes 0, rim-vs-core 0.30, rim-vs-outside 0.51, heterogeneity 0.09; core [0.985, 0.967, 0.609] rim [0.765, 0.784, 0.69]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 726 components >= 12 px at frames [50, 101, 151]):
  - radial e: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.931, rim/outside 36.9 (aggregate of 726 individuals; 0/726 membrane-like individually; rim level 0.921)
  - radial p: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.9, rim/outside 2.87 (aggregate of 726 individuals; 0/726 membrane-like individually; rim level 0.703)
  - radial F: peak at rho=2.45 (OUTSIDE the peak band 0.5-1.5), rim/core 1.28, rim/outside 0.894 (aggregate of 726 individuals; 0/726 membrane-like individually; rim level 0.627)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #1 (t=880, R_eq 3.48): none; #2 (t=880, R_eq 3.52): none; #15 (t=880, R_eq 3.7): none; #28 (t=910, R_eq 4.18): none

## Warnings
- no components at the end: matter died out or fell below threshold
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
