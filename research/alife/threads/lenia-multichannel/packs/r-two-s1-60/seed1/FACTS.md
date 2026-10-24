# Evidence pack: r-two-s1-60 (seed 1)

- world: `../../../worlds/r-two-s1-60/world.py`, family `lenia`
- parent: screen:two#60; mutation: random 'two' channel/kernel graph
- run: 301 frames x 5 steps x dt 0.1 = time 150; grid [192, 192]; wall 13s; status ok
- command: `python -m labkit.run threads/lenia-multichannel/worlds/r-two-s1-60/world.py --out threads/lenia-multichannel/packs/r-two-s1-60 --seeds 0 1 2 --frames 300`
- segmentation: matter > 0.35 of robust range [0.0, 1.5063], min area 6 px

## Measurements
- components: final 47, mean 43.9, max 49; occupancy final 0.11
- tracks: 264; persistent (alive >= 50% of run): 38; longest 296 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 18.00 (1 = constant size)
- enclosures: components with a hole mean 0.73, final 1; holes at thresholds 0.2/0.35/0.5 final [1, 1, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [72, 56, 43], H1 [4, 0, 0]
- motion: 26 long-lived tracks moved >= 1 body length; max speed 0.585/time; max body lengths 3.0
- replication: splits 80, persistent splits 0, max generation 0, merges 31, nucleations 38
- channel total drift (end/start - 1): [-0.3219, -1.0]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 52 at frame 154: holes 0, rim-vs-core 0.00, rim-vs-outside 0.88, heterogeneity 0.00; core [1.0, 0.0] rim [1.0, 0.0]
  - track 55 at frame 154: holes 0, rim-vs-core 0.02, rim-vs-outside 0.80, heterogeneity 0.04; core [0.99, 0.0] rim [0.971, 0.0]
  - track 63 at frame 154: holes 0, rim-vs-core 0.04, rim-vs-outside 0.79, heterogeneity 0.04; core [1.0, 0.0] rim [0.961, 0.0]
  - track 64 at frame 154: holes 0, rim-vs-core 0.00, rim-vs-outside 0.86, heterogeneity 0.00; core [1.0, 0.0] rim [1.0, 0.0]

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, lineage.png, timeseries.png, movie.mp4, metrics.json

Measurements are screens, not verdicts: judge them against the images.
