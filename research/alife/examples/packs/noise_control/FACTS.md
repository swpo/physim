# Evidence pack: noise-control (seed 0)

- world: `../../noise_control/world.py`, family `control`
- parent: None; mutation: reference
- run: 101 frames x 1 steps x dt 1.0 = time 100; grid [128, 128]; wall 0s; status ok
- command: `python -m labkit.run examples/noise_control/world.py --out examples/packs/noise_control --frames 100`
- segmentation: matter > 0.35 of robust range [-0.0902, 0.1196], min area 6 px

## Measurements
- components: final 3, mean 2.1, max 5; occupancy final 0.64
- tracks: 174; persistent (alive >= 50% of run): 0; longest 4 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 0.00 (1 = constant size)
- enclosures: components with a hole mean 0.99, final 1; holes at thresholds 0.2/0.35/0.5 final [25, 20, 1]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [28, 6, 1], H1 [36, 12, 0]
- motion: 0 long-lived tracks moved >= 1 body length; max speed 0/time; max body lengths 0.0
- replication: splits 56, persistent splits 0, max generation 0, merges 55, nucleations 10
- channel total drift (end/start - 1): [None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 29 at frame 19: holes 21, rim-vs-core 0.33, rim-vs-outside 0.36, heterogeneity 0.15; core [0.925] rim [0.592]
  - track 45 at frame 30: holes 20, rim-vs-core 0.07, rim-vs-outside 0.37, heterogeneity 0.14; core [0.539] rim [0.607]

## Warnings
- matter fills >80% of the domain at some point: components may be one connected sea

## Files
sheet.png, tracks.png, lineage.png, timeseries.png, movie.mp4, metrics.json

Measurements are screens, not verdicts: judge them against the images.
