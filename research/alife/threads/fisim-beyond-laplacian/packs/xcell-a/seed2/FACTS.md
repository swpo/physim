# Evidence pack: xcell-a (seed 2)

- world: `../../../worlds/xcell-a/world.py`, family `fisim-extended-rd`
- parent: blobkit m4; mutation: m4 + (i) membrane channel m deposited at the activator front (band nonlinearity 4s(1-s)) with a Cahn-Hilliard term (wells 0/1) that sharpens it into a ring, and (ii) a fast-diffusing cargo channel produced by the body whose diffusion is gated by the membrane, D_c*exp(-5 m).
- run: 201 frames x 100 steps x dt 0.02 = time 400; grid [160, 160]; wall 135s; status ok
- command: `python -m labkit.run threads/fisim-beyond-laplacian/worlds/xcell-a/world.py --out threads/fisim-beyond-laplacian/packs/xcell-a --seeds 0 1 2`
- segmentation: matter > 0.35 of robust range [0.0, 1.8292], min area 6 px

## Measurements
- components: final 8, mean 8.0, max 8; occupancy final 0.05
- tracks: 8; persistent (alive >= 50% of run): 8; longest 201 frames; alive start-to-end: 8
- size of persistent tracks: max/min area ratio 2.31 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [8, 8, 8], H1 [0, 0, 0]
- motion: 8 long-lived tracks moved >= 1 body length; max speed 0.257/time; max body lengths 8.1
- replication: splits 0, persistent splits 0, max generation 0, merges 0, nucleations 0
- channel total drift (end/start - 1): [-0.4437, None, -0.3456]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 0 at frame 101: holes 0, rim-vs-core 0.58, rim-vs-outside 0.51, heterogeneity 0.19; core [0.925, 0.685, 0.875] rim [0.558, 0.956, 0.524]
  - track 1 at frame 101: holes 0, rim-vs-core 0.57, rim-vs-outside 0.52, heterogeneity 0.20; core [0.927, 0.67, 0.877] rim [0.567, 0.956, 0.538]
  - track 2 at frame 101: holes 0, rim-vs-core 0.58, rim-vs-outside 0.51, heterogeneity 0.20; core [0.928, 0.672, 0.886] rim [0.567, 0.961, 0.54]
  - track 3 at frame 101: holes 0, rim-vs-core 0.56, rim-vs-outside 0.52, heterogeneity 0.19; core [0.932, 0.667, 0.891] rim [0.583, 0.956, 0.557]

## Warnings
- none

## Files
sheet.png, tracks.png, lineage.png, timeseries.png, movie.mp4, metrics.json

Measurements are screens, not verdicts: judge them against the images.
