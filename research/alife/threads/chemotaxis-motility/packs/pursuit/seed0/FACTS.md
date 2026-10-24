# Evidence pack: pursuit (seed 0)

- world: `../../../worlds/pursuit/world.py`, family `chemotaxis`
- parent: kstrail; mutation: two kstrail species with cross-taxis (predator up prey signal, prey down predator signal) + predation and nutrient-limited prey growth
- run: 201 frames x 60 steps x dt 0.05 = time 600; grid [160, 160]; wall 122s; status ok
- command: `python -m labkit.run threads/chemotaxis-motility/worlds/pursuit/world.py --out threads/chemotaxis-motility/packs/pursuit --seeds 0 1 2`
- segmentation: matter > 0.35 of robust range [0.0001, 1.8442], min area 6 px

## Measurements
- components: final 11, mean 8.1, max 15; occupancy final 0.05
- tracks: 99; persistent (alive >= 50% of run): 0; longest 88 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 0.00 (1 = constant size)
- enclosures: components with a hole mean 0.02, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [14, 12, 6], H1 [0, 0, 0]
- motion: 28 long-lived tracks moved >= 1 body length; max speed 0.625/time; max body lengths 14.2
- replication: splits 29, persistent splits 5, max generation 3, merges 20, nucleations 24
- channel total drift (end/start - 1): [-0.0001, -0.0, 0.0]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 24 at frame 128: holes 0, rim-vs-core 0.42, rim-vs-outside 0.29, heterogeneity 0.22; core [0.894, 0.601, 0.0] rim [0.676, 0.236, 0.0]
  - track 2 at frame 86: holes 0, rim-vs-core 0.32, rim-vs-outside 0.40, heterogeneity 0.29; core [0.655, 0.66, 0.0] rim [0.608, 0.342, 0.0]
  - track 34 at frame 129: holes 0, rim-vs-core 0.36, rim-vs-outside 0.52, heterogeneity 0.25; core [0.725, 0.772, 0.0] rim [0.701, 0.408, 0.0]
  - track 71 at frame 182: holes 0, rim-vs-core 0.32, rim-vs-outside 0.28, heterogeneity 0.11; core [0.911, 0.428, 0.0] rim [0.788, 0.131, 0.0]

## Warnings
- none

## Files
sheet.png, tracks.png, lineage.png, timeseries.png, movie.mp4, metrics.json

Measurements are screens, not verdicts: judge them against the images.
