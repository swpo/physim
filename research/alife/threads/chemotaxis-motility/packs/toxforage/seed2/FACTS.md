# Evidence pack: toxforage (seed 2)

- world: `../../../worlds/toxforage/world.py`, family `chemotaxis`
- parent: toxtrail; mutation: growth limited by a consumed, regrowing nutrient n (metabolism), with chemotaxis up n
- run: 201 frames x 120 steps x dt 0.05 = time 1200; grid [160, 160]; wall 96s; status ok
- command: `python -m labkit.run threads/chemotaxis-motility/worlds/toxforage/world.py --out threads/chemotaxis-motility/packs/toxforage --seeds 0 1 2`
- segmentation: matter > 0.35 of robust range [0.0, 0.9946], min area 6 px

## Measurements
- components: final 9, mean 8.5, max 13; occupancy final 0.05
- tracks: 132; persistent (alive >= 50% of run): 0; longest 73 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 0.00 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [9, 9, 9], H1 [0, 0, 0]
- motion: 28 long-lived tracks moved >= 1 body length; max speed 0.393/time; max body lengths 14.8
- replication: splits 39, persistent splits 0, max generation 0, merges 40, nucleations 24
- channel total drift (end/start - 1): [-0.0448, -0.0799, -0.0833, -0.0578]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 40 at frame 81: holes 0, rim-vs-core 0.48, rim-vs-outside 0.65, heterogeneity 0.21; core [0.974, 0.831, 0.691, 0.098] rim [0.649, 0.638, 0.517, 0.335]
  - track 1 at frame 50: holes 0, rim-vs-core 0.52, rim-vs-outside 0.66, heterogeneity 0.22; core [0.983, 0.84, 0.728, 0.079] rim [0.641, 0.632, 0.523, 0.336]
  - track 99 at frame 166: holes 0, rim-vs-core 0.48, rim-vs-outside 0.67, heterogeneity 0.21; core [0.978, 0.85, 0.707, 0.089] rim [0.661, 0.656, 0.518, 0.334]
  - track 48 at frame 86: holes 0, rim-vs-core 0.35, rim-vs-outside 0.33, heterogeneity 0.13; core [0.833, 0.427, 0.305, 0.417] rim [0.532, 0.365, 0.236, 0.567]

## Warnings
- none

## Files
sheet.png, tracks.png, lineage.png, timeseries.png, movie.mp4, metrics.json

Measurements are screens, not verdicts: judge them against the images.
