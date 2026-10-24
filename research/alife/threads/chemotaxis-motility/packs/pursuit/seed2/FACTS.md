# Evidence pack: pursuit (seed 2)

- world: `../../../worlds/pursuit/world.py`, family `chemotaxis`
- parent: kstrail; mutation: two kstrail species with cross-taxis (predator up prey signal, prey down predator signal) + predation and nutrient-limited prey growth
- run: 201 frames x 60 steps x dt 0.05 = time 600; grid [160, 160]; wall 107s; status ok
- command: `python -m labkit.run threads/chemotaxis-motility/worlds/pursuit/world.py --out threads/chemotaxis-motility/packs/pursuit --seeds 0 1 2`
- segmentation: matter > 0.35 of robust range [0.0001, 1.7078], min area 6 px

## Measurements
- components: final 9, mean 8.9, max 16; occupancy final 0.06
- tracks: 118; persistent (alive >= 50% of run): 1; longest 101 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 2.06 (1 = constant size)
- enclosures: components with a hole mean 0.04, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [10, 9, 7], H1 [0, 0, 0]
- motion: 28 long-lived tracks moved >= 1 body length; max speed 0.599/time; max body lengths 12.9
- replication: splits 32, persistent splits 6, max generation 3, merges 30, nucleations 24
- channel total drift (end/start - 1): [-0.0, -0.0002, 0.0]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 55 at frame 146: holes 0, rim-vs-core 0.12, rim-vs-outside 0.34, heterogeneity 0.03; core [0.0, 0.983, 0.0] rim [0.0, 0.859, 0.0]
  - track 23 at frame 114: holes 0, rim-vs-core 0.28, rim-vs-outside 0.43, heterogeneity 0.28; core [0.68, 0.605, 0.0] rim [0.574, 0.347, 0.0]
  - track 49 at frame 131: holes 0, rim-vs-core 0.13, rim-vs-outside 0.31, heterogeneity 0.03; core [0.977, 0.032, 0.0] rim [0.847, 0.006, 0.0]
  - track 112 at frame 188: holes 0, rim-vs-core 0.28, rim-vs-outside 0.44, heterogeneity 0.29; core [0.694, 0.603, 0.0] rim [0.581, 0.344, 0.0]

## Warnings
- none

## Files
sheet.png, tracks.png, lineage.png, timeseries.png, movie.mp4, metrics.json

Measurements are screens, not verdicts: judge them against the images.
