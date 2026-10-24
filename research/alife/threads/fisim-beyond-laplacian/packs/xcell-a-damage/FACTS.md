# Evidence pack: xcell-a (seed 0)

- world: `../../worlds/xcell-a/world.py`, family `fisim-extended-rd`
- parent: blobkit m4; mutation: m4 + (i) membrane channel m deposited at the activator front (band nonlinearity 4s(1-s)) with a Cahn-Hilliard term (wells 0/1) that sharpens it into a ring, and (ii) a fast-diffusing cargo channel produced by the body whose diffusion is gated by the membrane, D_c*exp(-5 m).
- run: 201 frames x 100 steps x dt 0.02 = time 400; grid [160, 160]; wall 143s; status ok
- command: `python -m labkit.run threads/fisim-beyond-laplacian/worlds/xcell-a/world.py --out threads/fisim-beyond-laplacian/packs/xcell-a-damage --seeds 0 --damage 100:0.5`
- segmentation: matter > 0.35 of robust range [0.0, 1.8291], min area 6 px

## Measurements
- components: final 7, mean 7.5, max 8; occupancy final 0.04
- tracks: 8; persistent (alive >= 50% of run): 8; longest 201 frames; alive start-to-end: 7
- size of persistent tracks: max/min area ratio 3.94 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [7, 7, 7], H1 [0, 0, 0]
- motion: 8 long-lived tracks moved >= 1 body length; max speed 0.277/time; max body lengths 8.7
- replication: splits 0, persistent splits 0, max generation 0, merges 0, nucleations 0
- channel total drift (end/start - 1): [-0.5099, None, -0.4255]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 0 at frame 101: holes 0, rim-vs-core 0.57, rim-vs-outside 0.51, heterogeneity 0.20; core [0.93, 0.67, 0.884] rim [0.574, 0.953, 0.545]
  - track 1 at frame 101: holes 0, rim-vs-core 0.58, rim-vs-outside 0.51, heterogeneity 0.20; core [0.926, 0.678, 0.885] rim [0.555, 0.961, 0.538]
  - track 2 at frame 101: holes 0, rim-vs-core 0.58, rim-vs-outside 0.51, heterogeneity 0.20; core [0.927, 0.67, 0.879] rim [0.562, 0.957, 0.534]
  - track 3 at frame 101: holes 0, rim-vs-core 0.58, rim-vs-outside 0.51, heterogeneity 0.20; core [0.927, 0.664, 0.877] rim [0.559, 0.955, 0.532]
- damage applied at frame 100: erased 82 px of a 162 px component

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, lineage.png, timeseries.png, movie.mp4, metrics.json

Measurements are screens, not verdicts: judge them against the images.
