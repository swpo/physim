# Evidence pack: toxforage (seed 0)

- world: `../../worlds/toxforage/world.py`, family `chemotaxis`
- parent: toxtrail; mutation: growth limited by a consumed, regrowing nutrient n (metabolism), with chemotaxis up n
- run: 201 frames x 120 steps x dt 0.05 = time 1200; grid [160, 160]; wall 125s; status ok
- command: `python -m labkit.run threads/chemotaxis-motility/worlds/toxforage/world.py --out threads/chemotaxis-motility/packs/toxforage_damage --seeds 0 --damage 100:0.5 --no-movie`
- segmentation: matter > 0.35 of robust range [0.0, 0.995], min area 6 px

## Measurements
- components: final 10, mean 8.9, max 12; occupancy final 0.07
- tracks: 150; persistent (alive >= 50% of run): 1; longest 101 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 2.06 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [11, 11, 10], H1 [0, 0, 0]
- motion: 28 long-lived tracks moved >= 1 body length; max speed 0.425/time; max body lengths 16.8
- replication: splits 47, persistent splits 2, max generation 2, merges 46, nucleations 15
- channel total drift (end/start - 1): [0.2019, 0.1992, 0.1988, -0.0739]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 78 at frame 151: holes 0, rim-vs-core 0.50, rim-vs-outside 0.36, heterogeneity 0.18; core [0.906, 0.677, 0.563, 0.21] rim [0.517, 0.544, 0.416, 0.443]
  - track 79 at frame 141: holes 0, rim-vs-core 0.45, rim-vs-outside 0.62, heterogeneity 0.20; core [0.966, 0.691, 0.571, 0.156] rim [0.643, 0.543, 0.429, 0.388]
  - track 26 at frame 71: holes 0, rim-vs-core 0.47, rim-vs-outside 0.67, heterogeneity 0.21; core [0.98, 0.864, 0.718, 0.092] rim [0.663, 0.665, 0.545, 0.324]
  - track 119 at frame 171: holes 0, rim-vs-core 0.49, rim-vs-outside 0.65, heterogeneity 0.21; core [0.973, 0.794, 0.672, 0.107] rim [0.646, 0.608, 0.488, 0.357]
- damage applied at frame 100: erased 137 px of a 416 px component

## Warnings
- none

## Files
sheet.png, tracks.png, lineage.png, timeseries.png, movie.mp4, metrics.json

Measurements are screens, not verdicts: judge them against the images.
