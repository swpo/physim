# Evidence pack: r-two56 (seed 2)

- world: `../../../worlds/r-two56/world.py`, family `lenia`
- parent: screen:two#56; mutation: random 'two' channel/kernel graph
- run: 201 frames x 5 steps x dt 0.1 = time 100; grid [192, 192]; wall 8s; status ok
- command: `python -m labkit.run threads/lenia-multichannel/worlds/r-two56/world.py --out threads/lenia-multichannel/packs/r-two56 --seeds 0 1 2 --frames 200`
- segmentation: matter > 0.35 of robust range [0.0, 2.0], min area 6 px

## Measurements
- components: final 4, mean 5.4, max 13; occupancy final 0.03
- tracks: 80; persistent (alive >= 50% of run): 4; longest 146 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 1.41 (1 = constant size)
- enclosures: components with a hole mean 3.01, final 3; holes at thresholds 0.2/0.35/0.5 final [0, 5, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [4, 4, 4], H1 [5, 0, 0]
- motion: 0 long-lived tracks moved >= 1 body length; max speed 0/time; max body lengths 0.6
- replication: splits 33, persistent splits 0, max generation 0, merges 8, nucleations 1
- channel total drift (end/start - 1): [-0.9461, -0.8748]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 39 at frame 128: holes 0, rim-vs-core 0.53, rim-vs-outside 0.46, heterogeneity 0.47; core [0.692, 0.483] rim [0.228, 0.733]
  - track 59 at frame 138: holes 0, rim-vs-core 0.68, rim-vs-outside 0.51, heterogeneity 0.47; core [0.712, 0.414] rim [0.147, 0.798]
  - track 60 at frame 139: holes 0, rim-vs-core 0.66, rim-vs-outside 0.50, heterogeneity 0.47; core [0.675, 0.421] rim [0.144, 0.804]
  - track 75 at frame 150: holes 1, rim-vs-core 0.70, rim-vs-outside 0.52, heterogeneity 0.47; core [0.747, 0.413] rim [0.153, 0.791]

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, lineage.png, timeseries.png, movie.mp4, metrics.json

Measurements are screens, not verdicts: judge them against the images.
