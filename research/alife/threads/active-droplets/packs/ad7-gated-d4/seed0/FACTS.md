# Evidence pack: ad7-gated-d4 (seed 0)

- world: `../../../worlds/ad7-gated-d4/world.py`, family `phase-field`
- parent: ad7-gated; mutation: 4x dilution rate (dil 0.0005 -> 0.002): turnover so non-dividing droplets are replaced
- run: 201 frames x 200 steps x dt 0.5 = time 20000; grid [128, 128]; wall 420s; status ok
- command: `python -m labkit.run threads/active-droplets/worlds/ad7-gated-d4/world.py --out threads/active-droplets/packs/ad7-gated-d4 --seeds 0 1 2 --frames 200 --no-movie`
- segmentation: matter > 0.35 of robust range [-1.0621, 1.4902], min area 6 px

## Measurements
- components: final 5, mean 5.5, max 7; occupancy final 0.08
- tracks: 14; persistent (alive >= 50% of run): 6; longest 173 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 16.00 (1 = constant size)
- enclosures: components with a hole mean 0.06, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [5, 5, 5], H1 [0, 0, 0]
- motion: 4 long-lived tracks moved >= 1 body length; max speed 0.00183/time; max body lengths 1.4
- replication: splits 5, persistent splits 4, max generation 2, merges 0, nucleations 0
- channel total drift (end/start - 1): [-0.0136, -0.3542, None, -0.2508, None, None, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 5 at frame 114: holes 0, rim-vs-core 0.50, rim-vs-outside 0.54, heterogeneity 0.06; core [0.956, 0.087, 0.0, 0.805, 0.0, 0.0, 0.0] rim [0.617, 0.193, 0.002, 0.46, 0.0, 0.0, 0.0]
  - track 7 at frame 116: holes 0, rim-vs-core 0.50, rim-vs-outside 0.56, heterogeneity 0.07; core [0.933, 0.056, 0.009, 0.865, 0.041, 0.028, 0.0] rim [0.615, 0.178, 0.041, 0.497, 0.024, 0.016, 0.0]
  - track 11 at frame 128: holes 0, rim-vs-core 0.52, rim-vs-outside 0.55, heterogeneity 0.07; core [0.958, 0.065, 0.001, 0.854, 0.0, 0.003, 0.0] rim [0.618, 0.19, 0.004, 0.483, 0.0, 0.002, 0.0]
  - track 12 at frame 175: holes 0, rim-vs-core 0.69, rim-vs-outside 0.95, heterogeneity 0.08; core [0.916, 0.009, 0.363, 0.0, 0.0, 1.0, 0.0] rim [0.614, 0.128, 0.973, 0.0, 0.0, 0.994, 0.0]

## Warnings
- none

## Files
sheet.png, tracks.png, lineage.png, timeseries.png, movie.mp4, metrics.json

Measurements are screens, not verdicts: judge them against the images.
