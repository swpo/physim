# Evidence pack: pursuit (seed 1)

- world: `../../../worlds/pursuit/world.py`, family `chemotaxis`
- parent: kstrail; mutation: two kstrail species with cross-taxis (predator up prey signal, prey down predator signal) + predation and nutrient-limited prey growth
- run: 201 frames x 60 steps x dt 0.05 = time 600; grid [160, 160]; wall 114s; status ok
- command: `python -m labkit.run threads/chemotaxis-motility/worlds/pursuit/world.py --out threads/chemotaxis-motility/packs/pursuit --seeds 0 1 2`
- segmentation: matter > 0.35 of robust range [0.0002, 1.8224], min area 6 px

## Measurements
- components: final 7, mean 8.1, max 20; occupancy final 0.05
- tracks: 91; persistent (alive >= 50% of run): 0; longest 96 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 0.00 (1 = constant size)
- enclosures: components with a hole mean 0.04, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [7, 7, 6], H1 [0, 0, 0]
- motion: 28 long-lived tracks moved >= 1 body length; max speed 0.619/time; max body lengths 18.3
- replication: splits 26, persistent splits 3, max generation 1, merges 18, nucleations 22
- channel total drift (end/start - 1): [-0.0, -0.0008, 0.0]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 30 at frame 128: holes 0, rim-vs-core 0.24, rim-vs-outside 0.22, heterogeneity 0.28; core [0.674, 0.554, 0.0] rim [0.521, 0.372, 0.0]
  - track 34 at frame 124: holes 0, rim-vs-core 0.31, rim-vs-outside 0.26, heterogeneity 0.20; core [0.775, 0.552, 0.0] rim [0.581, 0.31, 0.0]
  - track 19 at frame 109: holes 0, rim-vs-core 0.39, rim-vs-outside 0.26, heterogeneity 0.23; core [0.794, 0.631, 0.0] rim [0.584, 0.299, 0.0]
  - track 39 at frame 118: holes 0, rim-vs-core 0.17, rim-vs-outside 0.29, heterogeneity 0.05; core [0.977, 0.155, 0.0] rim [0.861, 0.032, 0.0]

## Warnings
- none

## Files
sheet.png, tracks.png, lineage.png, timeseries.png, movie.mp4, metrics.json

Measurements are screens, not verdicts: judge them against the images.
