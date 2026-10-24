# Evidence pack: ad7n-neutral (seed 1)

- world: `../../../worlds/ad7n-neutral/world.py`, family `phase-field`
- parent: ad7-gated; mutation: neutral control: all four alleles make no amphiphile (kp=0), same mutation and dilution
- run: 201 frames x 200 steps x dt 0.5 = time 20000; grid [128, 128]; wall 426s; status ok
- command: `python -m labkit.run threads/active-droplets/worlds/ad7n-neutral/world.py --out threads/active-droplets/packs/ad7n-neutral --seeds 0 1 2 --frames 200`
- segmentation: matter > 0.35 of robust range [-1.0594, 1.4673], min area 6 px

## Measurements
- components: final 5, mean 5.0, max 5; occupancy final 0.09
- tracks: 5; persistent (alive >= 50% of run): 5; longest 201 frames; alive start-to-end: 5
- size of persistent tracks: max/min area ratio 3.23 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [5, 5, 5], H1 [0, 0, 0]
- motion: 3 long-lived tracks moved >= 1 body length; max speed 0.00126/time; max body lengths 1.5
- replication: splits 0, persistent splits 0, max generation 0, merges 0, nucleations 0
- channel total drift (end/start - 1): [0.0188, -0.4272, None, 0.1707, None, None, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 0 at frame 101: holes 0, rim-vs-core 0.27, rim-vs-outside 0.73, heterogeneity 0.07; core [0.949, 0.073, 0.0, 0.655, 0.341, 0.0, 0.0] rim [0.746, 0.132, 0.0, 0.509, 0.267, 0.0, 0.0]
  - track 1 at frame 101: holes 0, rim-vs-core 0.50, rim-vs-outside 0.56, heterogeneity 0.07; core [0.96, 0.058, 0.0, 0.842, 0.0, 0.0, 0.0] rim [0.629, 0.178, 0.0, 0.481, 0.0, 0.0, 0.0]
  - track 2 at frame 101: holes 0, rim-vs-core 0.53, rim-vs-outside 0.55, heterogeneity 0.07; core [0.95, 0.049, 0.0, 0.856, 0.0, 0.256, 0.001] rim [0.62, 0.18, 0.0, 0.482, 0.0, 0.149, 0.0]
  - track 3 at frame 101: holes 0, rim-vs-core 0.53, rim-vs-outside 0.56, heterogeneity 0.08; core [0.96, 0.064, 0.0, 0.236, 0.007, 0.0, 0.862] rim [0.621, 0.192, 0.0, 0.134, 0.004, 0.0, 0.487]

## Warnings
- none

## Files
sheet.png, tracks.png, lineage.png, timeseries.png, movie.mp4, metrics.json

Measurements are screens, not verdicts: judge them against the images.
