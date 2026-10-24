# Evidence pack: toxforage (seed 0)

- world: `../../../worlds/toxforage/world.py`, family `chemotaxis`
- parent: toxtrail; mutation: growth limited by a consumed, regrowing nutrient n (metabolism), with chemotaxis up n
- run: 201 frames x 120 steps x dt 0.05 = time 1200; grid [160, 160]; wall 118s; status ok
- command: `python -m labkit.run threads/chemotaxis-motility/worlds/toxforage/world.py --out threads/chemotaxis-motility/packs/toxforage --seeds 0 1 2`
- segmentation: matter > 0.35 of robust range [0.0, 0.995], min area 6 px

## Measurements
- components: final 10, mean 9.2, max 13; occupancy final 0.08
- tracks: 166; persistent (alive >= 50% of run): 0; longest 63 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 0.00 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [12, 11, 10], H1 [0, 0, 0]
- motion: 30 long-lived tracks moved >= 1 body length; max speed 0.422/time; max body lengths 10.0
- replication: splits 52, persistent splits 4, max generation 3, merges 53, nucleations 14
- channel total drift (end/start - 1): [0.3155, 0.3093, 0.3075, -0.0809]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 26 at frame 71: holes 0, rim-vs-core 0.47, rim-vs-outside 0.67, heterogeneity 0.21; core [0.979, 0.853, 0.714, 0.094] rim [0.662, 0.657, 0.543, 0.327]
  - track 125 at frame 176: holes 0, rim-vs-core 0.47, rim-vs-outside 0.66, heterogeneity 0.21; core [0.971, 0.778, 0.671, 0.111] rim [0.658, 0.591, 0.496, 0.353]
  - track 105 at frame 148: holes 0, rim-vs-core 0.49, rim-vs-outside 0.65, heterogeneity 0.21; core [0.97, 0.769, 0.661, 0.117] rim [0.645, 0.582, 0.478, 0.367]
  - track 144 at frame 190: holes 0, rim-vs-core 0.45, rim-vs-outside 0.66, heterogeneity 0.20; core [0.969, 0.771, 0.653, 0.117] rim [0.668, 0.595, 0.493, 0.349]

## Warnings
- none

## Files
sheet.png, tracks.png, lineage.png, timeseries.png, movie.mp4, metrics.json

Measurements are screens, not verdicts: judge them against the images.
