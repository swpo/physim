# Evidence pack: ad7n-neutral-d4 (seed 1)

- world: `../../../worlds/ad7n-neutral-d4/world.py`, family `phase-field`
- parent: ad7n-neutral; mutation: 4x dilution rate (dil 0.0005 -> 0.002): turnover so non-dividing droplets are replaced
- run: 201 frames x 200 steps x dt 0.5 = time 20000; grid [128, 128]; wall 392s; status ok
- command: `python -m labkit.run threads/active-droplets/worlds/ad7n-neutral-d4/world.py --out threads/active-droplets/packs/ad7n-neutral-d4 --seeds 0 1 2 --frames 200 --no-movie`
- segmentation: matter > 0.35 of robust range [-1.0583, 1.4688], min area 6 px

## Measurements
- components: final 4, mean 4.5, max 5; occupancy final 0.08
- tracks: 5; persistent (alive >= 50% of run): 5; longest 201 frames; alive start-to-end: 4
- size of persistent tracks: max/min area ratio 7.59 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [4, 4, 4], H1 [0, 0, 0]
- motion: 2 long-lived tracks moved >= 1 body length; max speed 0.00156/time; max body lengths 1.3
- replication: splits 0, persistent splits 0, max generation 0, merges 0, nucleations 0
- channel total drift (end/start - 1): [-0.0058, -0.3621, None, -0.2817, None, None, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 0 at frame 101: holes 0, rim-vs-core 0.26, rim-vs-outside 0.71, heterogeneity 0.07; core [0.954, 0.072, 0.0, 0.592, 0.279, 0.0, 0.0] rim [0.751, 0.134, 0.0, 0.458, 0.216, 0.0, 0.0]
  - track 1 at frame 101: holes 0, rim-vs-core 0.52, rim-vs-outside 0.57, heterogeneity 0.07; core [0.96, 0.058, 0.0, 0.0, 0.936, 0.0, 0.012] rim [0.623, 0.178, 0.0, 0.0, 0.564, 0.0, 0.007]
  - track 3 at frame 101: holes 0, rim-vs-core 0.48, rim-vs-outside 0.53, heterogeneity 0.07; core [0.96, 0.061, 0.0, 0.669, 0.224, 0.004, 0.001] rim [0.621, 0.19, 0.0, 0.375, 0.128, 0.002, 0.001]
  - track 4 at frame 101: holes 0, rim-vs-core 0.33, rim-vs-outside 0.73, heterogeneity 0.07; core [0.951, 0.049, 0.0, 0.892, 0.0, 0.0, 0.0] rim [0.741, 0.129, 0.0, 0.654, 0.0, 0.0, 0.0]

## Warnings
- none

## Files
sheet.png, tracks.png, lineage.png, timeseries.png, movie.mp4, metrics.json

Measurements are screens, not verdicts: judge them against the images.
