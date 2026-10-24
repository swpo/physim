# Evidence pack: ad7-gated-d4 (seed 1)

- world: `../../../worlds/ad7-gated-d4/world.py`, family `phase-field`
- parent: ad7-gated; mutation: 4x dilution rate (dil 0.0005 -> 0.002): turnover so non-dividing droplets are replaced
- run: 201 frames x 200 steps x dt 0.5 = time 20000; grid [128, 128]; wall 390s; status ok
- command: `python -m labkit.run threads/active-droplets/worlds/ad7-gated-d4/world.py --out threads/active-droplets/packs/ad7-gated-d4 --seeds 0 1 2 --frames 200 --no-movie`
- segmentation: matter > 0.35 of robust range [-1.0621, 1.4765], min area 6 px

## Measurements
- components: final 10, mean 7.7, max 11; occupancy final 0.11
- tracks: 19; persistent (alive >= 50% of run): 5; longest 201 frames; alive start-to-end: 1
- size of persistent tracks: max/min area ratio 2.97 (1 = constant size)
- enclosures: components with a hole mean 0.04, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [12, 10, 10], H1 [0, 0, 0]
- motion: 1 long-lived tracks moved >= 1 body length; max speed 0.00131/time; max body lengths 1.6
- replication: splits 7, persistent splits 6, max generation 2, merges 0, nucleations 0
- channel total drift (end/start - 1): [0.0599, -0.5009, None, -0.6531, None, None, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 3 at frame 101: holes 0, rim-vs-core 0.51, rim-vs-outside 0.57, heterogeneity 0.07; core [0.947, 0.067, 0.007, 0.855, 0.062, 0.0, 0.0] rim [0.621, 0.189, 0.03, 0.489, 0.036, 0.0, 0.0]
  - track 5 at frame 129: holes 0, rim-vs-core 0.63, rim-vs-outside 0.72, heterogeneity 0.11; core [0.915, 0.019, 0.149, 0.0, 0.298, 0.735, 0.0] rim [0.651, 0.135, 0.627, 0.0, 0.191, 0.459, 0.0]
  - track 1 at frame 64: holes 0, rim-vs-core 0.49, rim-vs-outside 0.64, heterogeneity 0.10; core [0.925, 0.029, 0.074, 0.678, 0.04, 0.316, 0.0] rim [0.626, 0.153, 0.287, 0.397, 0.024, 0.195, 0.0]
  - track 11 at frame 153: holes 0, rim-vs-core 0.58, rim-vs-outside 0.62, heterogeneity 0.10; core [0.853, 0.063, 0.592, 0.0, 0.0, 0.0, 1.0] rim [0.501, 0.268, 1.0, 0.0, 0.0, 0.0, 0.932]

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, lineage.png, timeseries.png, movie.mp4, metrics.json

Measurements are screens, not verdicts: judge them against the images.
