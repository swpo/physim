# Evidence pack: phase-swimdiv (seed 1)

- world: `../../../worlds/phase_swimdiv/world.py`, family `autopoiesis`
- parent: threads/autopoiesis/worlds/phase_swim; mutation: phoretic mobility lowered to mu=1.5 (near threshold): cells swim AND divide
- run: 161 frames x 50 steps x dt 1.0 = time 8000; grid [128, 128]; wall 27s; status ok
- command: `python -m labkit.run threads/autopoiesis/worlds/phase_swimdiv/world.py --out threads/autopoiesis/packs/phase_swimdiv --seeds 0 1 2 --frames 160`
- segmentation: matter > 0.35 of robust range [0.0, 1.5416], min area 6 px

## Measurements
- components: final 12, mean 5.1, max 12; occupancy final 0.18
- tracks: 64; persistent (alive >= 50% of run): 0; longest 62 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 0.00 (1 = constant size)
- enclosures: components with a hole mean 1.13, final 2; holes at thresholds 0.2/0.35/0.5 final [0, 2, 10]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [13, 12, 12], H1 [12, 11, 1]
- motion: 17 long-lived tracks moved >= 1 body length; max speed 0.0622/time; max body lengths 7.7
- replication: splits 24, persistent splits 1, max generation 1, merges 12, nucleations 0
- channel total drift (end/start - 1): [-0.2901, 34.0524, 23.6962, 15.6846]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 30 at frame 124: holes 0, rim-vs-core 0.59, rim-vs-outside 1.00, heterogeneity 0.24; core [0.058, 0.859, 0.759, 0.359] rim [0.306, 0.509, 0.642, 0.743]
  - track 29 at frame 120: holes 0, rim-vs-core 0.59, rim-vs-outside 1.02, heterogeneity 0.23; core [0.051, 0.852, 0.741, 0.332] rim [0.296, 0.528, 0.654, 0.749]
  - track 35 at frame 126: holes 0, rim-vs-core 0.59, rim-vs-outside 1.02, heterogeneity 0.23; core [0.053, 0.852, 0.743, 0.339] rim [0.301, 0.523, 0.652, 0.755]
  - track 0 at frame 24: holes 1, rim-vs-core 0.27, rim-vs-outside 0.82, heterogeneity 0.19; core [0.114, 0.757, 0.685, 0.767] rim [0.183, 0.593, 0.613, 0.576]

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, lineage.png, timeseries.png, movie.mp4, metrics.json

Measurements are screens, not verdicts: judge them against the images.
