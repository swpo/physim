# Evidence pack: xcell-div-nogate (seed 0)

- world: `../../worlds/xcell-div-nogate/world.py`, family `fisim-extended-rd`
- parent: xcell-div; mutation: ablation: membrane gating of cargo removed (beta=0)
- run: 201 frames x 100 steps x dt 0.02 = time 400; grid [160, 160]; wall 150s; status ok
- command: `python -m labkit.run threads/fisim-beyond-laplacian/worlds/xcell-div-nogate/world.py --out threads/fisim-beyond-laplacian/packs/xcell-div-nogate --seeds 0`
- segmentation: matter > 0.35 of robust range [0.0, 1.8458], min area 6 px

## Measurements
- components: final 16, mean 14.4, max 16; occupancy final 0.11
- tracks: 24; persistent (alive >= 50% of run): 16; longest 201 frames; alive start-to-end: 1
- size of persistent tracks: max/min area ratio 1.76 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [16, 16, 16], H1 [0, 0, 0]
- motion: 23 long-lived tracks moved >= 1 body length; max speed 0.308/time; max body lengths 8.7
- replication: splits 8, persistent splits 8, max generation 2, merges 0, nucleations 0
- channel total drift (end/start - 1): [0.1596, None, -0.1842]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 3 at frame 101: holes 0, rim-vs-core 0.51, rim-vs-outside 0.46, heterogeneity 0.18; core [0.923, 0.629, 0.87] rim [0.575, 0.92, 0.634]
  - track 8 at frame 118: holes 0, rim-vs-core 0.30, rim-vs-outside 0.60, heterogeneity 0.18; core [0.909, 0.666, 0.836] rim [0.693, 0.815, 0.7]
  - track 9 at frame 118: holes 0, rim-vs-core 0.51, rim-vs-outside 0.46, heterogeneity 0.17; core [0.929, 0.631, 0.856] rim [0.582, 0.93, 0.625]
  - track 22 at frame 131: holes 0, rim-vs-core 0.51, rim-vs-outside 0.46, heterogeneity 0.17; core [0.931, 0.623, 0.861] rim [0.586, 0.921, 0.628]

## Warnings
- none

## Files
sheet.png, tracks.png, lineage.png, timeseries.png, movie.mp4, metrics.json

Measurements are screens, not verdicts: judge them against the images.
