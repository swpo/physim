# Evidence pack: swimfission (seed 2)

- world: `../../../worlds/swimfission/world.py`, family `chemotaxis`
- parent: toxforage; mutation: shorter cohesion range (Da 4 -> 2): grown swimmers exceed it and divide
- run: 201 frames x 120 steps x dt 0.05 = time 1200; grid [160, 160]; wall 105s; status ok
- command: `python -m labkit.run threads/chemotaxis-motility/worlds/swimfission/world.py --out threads/chemotaxis-motility/packs/swimfission --seeds 0 1 2`
- segmentation: matter > 0.35 of robust range [0.0, 0.9945], min area 6 px

## Measurements
- components: final 10, mean 13.8, max 32; occupancy final 0.04
- tracks: 142; persistent (alive >= 50% of run): 3; longest 142 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 1.52 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [10, 10, 10], H1 [0, 0, 0]
- motion: 45 long-lived tracks moved >= 1 body length; max speed 0.335/time; max body lengths 21.3
- replication: splits 31, persistent splits 8, max generation 3, merges 45, nucleations 37
- channel total drift (end/start - 1): [-0.3585, -0.3663, -0.3695, -0.0414]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 84 at frame 129: holes 0, rim-vs-core 0.61, rim-vs-outside 0.47, heterogeneity 0.21; core [0.953, 0.839, 0.726, 0.104] rim [0.507, 0.615, 0.5, 0.365]
  - track 87 at frame 119: holes 0, rim-vs-core 0.54, rim-vs-outside 0.52, heterogeneity 0.19; core [0.965, 0.846, 0.734, 0.094] rim [0.593, 0.63, 0.519, 0.337]
  - track 113 at frame 146: holes 0, rim-vs-core 0.58, rim-vs-outside 0.50, heterogeneity 0.20; core [0.957, 0.838, 0.731, 0.098] rim [0.539, 0.616, 0.514, 0.35]
  - track 126 at frame 163: holes 0, rim-vs-core 0.53, rim-vs-outside 0.47, heterogeneity 0.20; core [0.945, 0.753, 0.633, 0.143] rim [0.539, 0.582, 0.464, 0.378]

## Warnings
- none

## Files
sheet.png, tracks.png, lineage.png, timeseries.png, movie.mp4, metrics.json

Measurements are screens, not verdicts: judge them against the images.
