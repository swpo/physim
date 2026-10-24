# Evidence pack: ad7n-neutral-d4 (seed 0)

- world: `../../../worlds/ad7n-neutral-d4/world.py`, family `phase-field`
- parent: ad7n-neutral; mutation: 4x dilution rate (dil 0.0005 -> 0.002): turnover so non-dividing droplets are replaced
- run: 201 frames x 200 steps x dt 0.5 = time 20000; grid [128, 128]; wall 419s; status ok
- command: `python -m labkit.run threads/active-droplets/worlds/ad7n-neutral-d4/world.py --out threads/active-droplets/packs/ad7n-neutral-d4 --seeds 0 1 2 --frames 200 --no-movie`
- segmentation: matter > 0.35 of robust range [-1.0595, 1.4712], min area 6 px

## Measurements
- components: final 2, mean 3.8, max 5; occupancy final 0.05
- tracks: 8; persistent (alive >= 50% of run): 4; longest 201 frames; alive start-to-end: 1
- size of persistent tracks: max/min area ratio 4.82 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [2, 2, 2], H1 [0, 0, 0]
- motion: 1 long-lived tracks moved >= 1 body length; max speed 0.00172/time; max body lengths 1.3
- replication: splits 2, persistent splits 2, max generation 1, merges 0, nucleations 0
- channel total drift (end/start - 1): [-0.0736, -0.227, None, -0.1206, None, None, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 1 at frame 101: holes 0, rim-vs-core 0.47, rim-vs-outside 0.72, heterogeneity 0.07; core [0.962, 0.03, 0.0, 0.921, 0.0, 0.0, 0.001] rim [0.698, 0.161, 0.0, 0.556, 0.0, 0.0, 0.001]
  - track 5 at frame 129: holes 0, rim-vs-core 0.52, rim-vs-outside 0.55, heterogeneity 0.07; core [0.953, 0.051, 0.0, 0.864, 0.0, 0.001, 0.0] rim [0.617, 0.182, 0.0, 0.486, 0.0, 0.001, 0.0]
  - track 4 at frame 118: holes 0, rim-vs-core 0.41, rim-vs-outside 0.68, heterogeneity 0.07; core [0.956, 0.043, 0.0, 0.877, 0.0, 0.0, 0.0] rim [0.705, 0.154, 0.0, 0.571, 0.0, 0.0, 0.0]
  - track 3 at frame 55: holes 0, rim-vs-core 0.37, rim-vs-outside 0.84, heterogeneity 0.08; core [0.942, 0.022, 0.0, 0.914, 0.0, 0.0, 0.393] rim [0.77, 0.132, 0.0, 0.626, 0.0, 0.0, 0.275]

## Warnings
- none

## Files
sheet.png, tracks.png, lineage.png, timeseries.png, movie.mp4, metrics.json

Measurements are screens, not verdicts: judge them against the images.
