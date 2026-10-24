# Evidence pack: toxforage (seed 0)

- world: `../../../../home/user/physim/research/alife/threads/chemotaxis-motility/worlds/toxforage/world.py`, family `chemotaxis`
- parent: toxtrail; mutation: growth limited by a consumed, regrowing nutrient n (metabolism), with chemotaxis up n
- run: 151 frames x 200 steps x dt 0.05 = time 1500; grid [128, 128]; wall 92s; status ok
- command: `WORLD_P='{"r":0.06}' python -m labkit.run threads/chemotaxis-motility/worlds/toxforage/world.py --out threads/chemotaxis-motility/packs/toxforage_long_128 --frames 150 --spf 200 --size 128 128 --no-movie`
- segmentation: matter > 0.35 of robust range [0.0, 0.9948], min area 6 px

## Measurements
- components: final 7, mean 6.0, max 9; occupancy final 0.07
- tracks: 135; persistent (alive >= 50% of run): 0; longest 38 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 0.00 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [7, 7, 7], H1 [0, 0, 0]
- motion: 19 long-lived tracks moved >= 1 body length; max speed 0.449/time; max body lengths 12.9
- replication: splits 41, persistent splits 0, max generation 0, merges 45, nucleations 16
- channel total drift (end/start - 1): [0.1743, 0.1362, 0.1326, -0.0712]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 48 at frame 83: holes 0, rim-vs-core 0.50, rim-vs-outside 0.34, heterogeneity 0.18; core [0.894, 0.582, 0.479, 0.255] rim [0.489, 0.46, 0.346, 0.485]
  - track 0 at frame 21: holes 0, rim-vs-core 0.44, rim-vs-outside 0.65, heterogeneity 0.24; core [0.968, 0.793, 0.599, 0.166] rim [0.684, 0.614, 0.444, 0.401]
  - track 63 at frame 96: holes 0, rim-vs-core 0.47, rim-vs-outside 0.64, heterogeneity 0.21; core [0.971, 0.836, 0.7, 0.101] rim [0.646, 0.652, 0.531, 0.334]
  - track 42 at frame 68: holes 0, rim-vs-core 0.28, rim-vs-outside 0.81, heterogeneity 0.21; core [0.963, 0.73, 0.65, 0.129] rim [0.745, 0.65, 0.568, 0.27]

## Warnings
- none

## Files
sheet.png, tracks.png, lineage.png, timeseries.png, movie.mp4, metrics.json

Measurements are screens, not verdicts: judge them against the images.
