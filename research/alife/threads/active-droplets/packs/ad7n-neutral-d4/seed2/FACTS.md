# Evidence pack: ad7n-neutral-d4 (seed 2)

- world: `../../../worlds/ad7n-neutral-d4/world.py`, family `phase-field`
- parent: ad7n-neutral; mutation: 4x dilution rate (dil 0.0005 -> 0.002): turnover so non-dividing droplets are replaced
- run: 201 frames x 200 steps x dt 0.5 = time 20000; grid [128, 128]; wall 404s; status ok
- command: `python -m labkit.run threads/active-droplets/worlds/ad7n-neutral-d4/world.py --out threads/active-droplets/packs/ad7n-neutral-d4 --seeds 0 1 2 --frames 200 --no-movie`
- segmentation: matter > 0.35 of robust range [-1.0579, 1.4683], min area 6 px

## Measurements
- components: final 4, mean 4.5, max 6; occupancy final 0.08
- tracks: 6; persistent (alive >= 50% of run): 4; longest 201 frames; alive start-to-end: 4
- size of persistent tracks: max/min area ratio 3.64 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [4, 4, 4], H1 [0, 0, 0]
- motion: 1 long-lived tracks moved >= 1 body length; max speed 0.00114/time; max body lengths 1.3
- replication: splits 0, persistent splits 0, max generation 0, merges 0, nucleations 0
- channel total drift (end/start - 1): [-0.0023, -0.37, None, -0.2331, None, None, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 0 at frame 101: holes 0, rim-vs-core 0.46, rim-vs-outside 0.74, heterogeneity 0.07; core [0.961, 0.031, 0.0, 0.0, 0.0, 0.0, 0.985] rim [0.687, 0.165, 0.0, 0.0, 0.0, 0.0, 0.642]
  - track 3 at frame 101: holes 0, rim-vs-core 0.39, rim-vs-outside 0.65, heterogeneity 0.05; core [0.949, 0.05, 0.0, 0.0, 1.0, 0.0, 0.0] rim [0.617, 0.183, 0.0, 0.0, 0.843, 0.0, 0.0]
  - track 4 at frame 101: holes 0, rim-vs-core 0.47, rim-vs-outside 0.72, heterogeneity 0.07; core [0.964, 0.03, 0.0, 0.915, 0.0, 0.0, 0.044] rim [0.706, 0.163, 0.0, 0.552, 0.0, 0.0, 0.027]
  - track 5 at frame 101: holes 0, rim-vs-core 0.51, rim-vs-outside 0.57, heterogeneity 0.07; core [0.956, 0.049, 0.0, 0.892, 0.001, 0.0, 0.001] rim [0.633, 0.178, 0.0, 0.518, 0.001, 0.0, 0.001]

## Warnings
- none

## Files
sheet.png, tracks.png, lineage.png, timeseries.png, movie.mp4, metrics.json

Measurements are screens, not verdicts: judge them against the images.
