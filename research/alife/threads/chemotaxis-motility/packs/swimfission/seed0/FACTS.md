# Evidence pack: swimfission (seed 0)

- world: `../../../worlds/swimfission/world.py`, family `chemotaxis`
- parent: toxforage; mutation: shorter cohesion range (Da 4 -> 2): grown swimmers exceed it and divide
- run: 201 frames x 120 steps x dt 0.05 = time 1200; grid [160, 160]; wall 142s; status ok
- command: `python -m labkit.run threads/chemotaxis-motility/worlds/swimfission/world.py --out threads/chemotaxis-motility/packs/swimfission --seeds 0 1 2`
- segmentation: matter > 0.35 of robust range [0.0, 0.9966], min area 6 px

## Measurements
- components: final 8, mean 13.3, max 29; occupancy final 0.03
- tracks: 176; persistent (alive >= 50% of run): 1; longest 110 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 5.56 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [8, 8, 8], H1 [0, 0, 0]
- motion: 43 long-lived tracks moved >= 1 body length; max speed 0.382/time; max body lengths 16.1
- replication: splits 45, persistent splits 3, max generation 2, merges 56, nucleations 32
- channel total drift (end/start - 1): [-0.4615, -0.4362, -0.4274, -0.0359]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 11 at frame 62: holes 0, rim-vs-core 0.54, rim-vs-outside 0.52, heterogeneity 0.20; core [0.965, 0.846, 0.734, 0.094] rim [0.581, 0.63, 0.528, 0.334]
  - track 122 at frame 155: holes 0, rim-vs-core 0.62, rim-vs-outside 0.45, heterogeneity 0.21; core [0.952, 0.83, 0.729, 0.101] rim [0.488, 0.604, 0.502, 0.365]
  - track 101 at frame 121: holes 0, rim-vs-core 0.61, rim-vs-outside 0.48, heterogeneity 0.21; core [0.955, 0.827, 0.725, 0.103] rim [0.511, 0.601, 0.488, 0.373]
  - track 150 at frame 175: holes 0, rim-vs-core 0.52, rim-vs-outside 0.56, heterogeneity 0.21; core [0.955, 0.836, 0.711, 0.109] rim [0.575, 0.632, 0.534, 0.328]

## Warnings
- none

## Files
sheet.png, tracks.png, lineage.png, timeseries.png, movie.mp4, metrics.json

Measurements are screens, not verdicts: judge them against the images.
