# Evidence pack: swimfission (seed 1)

- world: `../../../worlds/swimfission/world.py`, family `chemotaxis`
- parent: toxforage; mutation: shorter cohesion range (Da 4 -> 2): grown swimmers exceed it and divide
- run: 201 frames x 120 steps x dt 0.05 = time 1200; grid [160, 160]; wall 103s; status ok
- command: `python -m labkit.run threads/chemotaxis-motility/worlds/swimfission/world.py --out threads/chemotaxis-motility/packs/swimfission --seeds 0 1 2`
- segmentation: matter > 0.35 of robust range [0.0, 0.9966], min area 6 px

## Measurements
- components: final 11, mean 15.0, max 33; occupancy final 0.04
- tracks: 167; persistent (alive >= 50% of run): 6; longest 155 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 6.47 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [11, 11, 11], H1 [0, 0, 0]
- motion: 43 long-lived tracks moved >= 1 body length; max speed 0.341/time; max body lengths 27.4
- replication: splits 39, persistent splits 6, max generation 2, merges 56, nucleations 38
- channel total drift (end/start - 1): [-0.3841, -0.3682, -0.3478, -0.0408]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 8 at frame 84: holes 0, rim-vs-core 0.55, rim-vs-outside 0.51, heterogeneity 0.19; core [0.961, 0.919, 0.803, 0.075] rim [0.571, 0.706, 0.582, 0.303]
  - track 24 at frame 82: holes 0, rim-vs-core 0.52, rim-vs-outside 0.49, heterogeneity 0.19; core [0.953, 0.845, 0.758, 0.1] rim [0.573, 0.658, 0.563, 0.326]
  - track 56 at frame 97: holes 0, rim-vs-core 0.59, rim-vs-outside 0.49, heterogeneity 0.21; core [0.956, 0.833, 0.731, 0.106] rim [0.538, 0.611, 0.501, 0.366]
  - track 125 at frame 156: holes 0, rim-vs-core 0.49, rim-vs-outside 0.57, heterogeneity 0.20; core [0.964, 0.851, 0.706, 0.107] rim [0.621, 0.646, 0.527, 0.327]

## Warnings
- none

## Files
sheet.png, tracks.png, lineage.png, timeseries.png, movie.mp4, metrics.json

Measurements are screens, not verdicts: judge them against the images.
