# Evidence pack: r-two56 (seed 2)

- world: `../../../worlds/r-two56/world.py`, family `lenia`
- parent: screen:two#56; mutation: random 'two' channel/kernel graph
- run: 201 frames x 5 steps x dt 0.1 = time 100; grid [192, 192]; wall 8s; status ok
- command: `python -m labkit.run threads/lenia-multichannel/worlds/r-two56/world.py --out threads/lenia-multichannel/packs/r-two56_damage --seeds 0 1 2 --frames 200 --damage 120:0.5 --no-movie`
- segmentation: matter > 0.35 of robust range [0.0, 2.0], min area 6 px

## Measurements
- components: final 3, mean 5.0, max 13; occupancy final 0.02
- tracks: 87; persistent (alive >= 50% of run): 3; longest 146 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 1.41 (1 = constant size)
- enclosures: components with a hole mean 3.01, final 3; holes at thresholds 0.2/0.35/0.5 final [0, 5, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [3, 3, 3], H1 [5, 0, 0]
- motion: 0 long-lived tracks moved >= 1 body length; max speed 0/time; max body lengths 0.6
- replication: splits 35, persistent splits 0, max generation 0, merges 8, nucleations 1
- channel total drift (end/start - 1): [-0.96, -0.9063]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 39 at frame 128: holes 0, rim-vs-core 0.53, rim-vs-outside 0.46, heterogeneity 0.47; core [0.692, 0.483] rim [0.228, 0.733]
  - track 60 at frame 139: holes 0, rim-vs-core 0.66, rim-vs-outside 0.50, heterogeneity 0.47; core [0.675, 0.421] rim [0.144, 0.804]
  - track 75 at frame 150: holes 1, rim-vs-core 0.70, rim-vs-outside 0.52, heterogeneity 0.47; core [0.747, 0.413] rim [0.153, 0.791]
  - track 27 at frame 87: holes 2, rim-vs-core 0.67, rim-vs-outside 0.42, heterogeneity 0.46; core [0.794, 0.454] rim [0.196, 0.745]
- damage applied at frame 120: erased 114 px of a 278 px component

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, lineage.png, timeseries.png, movie.mp4, metrics.json

Measurements are screens, not verdicts: judge them against the images.
