# Evidence pack: ad7-gated-d4 (seed 2)

- world: `../../../worlds/ad7-gated-d4/world.py`, family `phase-field`
- parent: ad7-gated; mutation: 4x dilution rate (dil 0.0005 -> 0.002): turnover so non-dividing droplets are replaced
- run: 201 frames x 200 steps x dt 0.5 = time 20000; grid [128, 128]; wall 404s; status ok
- command: `python -m labkit.run threads/active-droplets/worlds/ad7-gated-d4/world.py --out threads/active-droplets/packs/ad7-gated-d4 --seeds 0 1 2 --frames 200 --no-movie`
- segmentation: matter > 0.35 of robust range [-1.0629, 1.4899], min area 6 px

## Measurements
- components: final 8, mean 6.3, max 9; occupancy final 0.09
- tracks: 20; persistent (alive >= 50% of run): 4; longest 201 frames; alive start-to-end: 1
- size of persistent tracks: max/min area ratio 9.88 (1 = constant size)
- enclosures: components with a hole mean 0.16, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [8, 8, 8], H1 [0, 0, 0]
- motion: 0 long-lived tracks moved >= 1 body length; max speed 0/time; max body lengths 0.9
- replication: splits 7, persistent splits 4, max generation 1, merges 0, nucleations 0
- channel total drift (end/start - 1): [0.0174, -0.4196, None, -0.2394, None, None, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 3 at frame 101: holes 0, rim-vs-core 0.55, rim-vs-outside 0.63, heterogeneity 0.10; core [0.851, 0.047, 0.662, 0.0, 0.0, 0.0, 1.0] rim [0.509, 0.272, 1.0, 0.0, 0.0, 0.0, 0.877]
  - track 7 at frame 114: holes 0, rim-vs-core 0.50, rim-vs-outside 0.57, heterogeneity 0.07; core [0.951, 0.06, 0.0, 0.879, 0.0, 0.0, 0.0] rim [0.644, 0.19, 0.0, 0.508, 0.0, 0.0, 0.0]
  - track 8 at frame 113: holes 0, rim-vs-core 0.39, rim-vs-outside 0.69, heterogeneity 0.07; core [0.954, 0.056, 0.0, 0.887, 0.0, 0.0, 0.0] rim [0.718, 0.16, 0.0, 0.597, 0.0, 0.0, 0.0]
  - track 13 at frame 150: holes 0, rim-vs-core 0.37, rim-vs-outside 1.01, heterogeneity 0.11; core [0.933, 0.031, 0.065, 0.8, 0.005, 0.941, 0.0] rim [0.742, 0.097, 0.2, 0.608, 0.004, 0.742, 0.0]

## Warnings
- none

## Files
sheet.png, tracks.png, lineage.png, timeseries.png, movie.mp4, metrics.json

Measurements are screens, not verdicts: judge them against the images.
