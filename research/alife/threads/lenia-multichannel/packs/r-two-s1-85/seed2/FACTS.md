# Evidence pack: r-two-s1-85 (seed 2)

- world: `../../../worlds/r-two-s1-85/world.py`, family `lenia`
- parent: screen:two#85; mutation: random 'two' channel/kernel graph
- run: 301 frames x 5 steps x dt 0.1 = time 150; grid [192, 192]; wall 12s; status ok
- command: `python -m labkit.run threads/lenia-multichannel/worlds/r-two-s1-85/world.py --out threads/lenia-multichannel/packs/r-two-s1-85 --seeds 0 1 2 --frames 300`
- segmentation: matter > 0.35 of robust range [0.0, 2.0], min area 6 px

## Measurements
- components: final 30, mean 32.8, max 221; occupancy final 0.09
- tracks: 1021; persistent (alive >= 50% of run): 13; longest 296 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 1.69 (1 = constant size)
- enclosures: components with a hole mean 4.24, final 4; holes at thresholds 0.2/0.35/0.5 final [0, 8, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [66, 39, 19], H1 [22, 1, 0]
- motion: 1 long-lived tracks moved >= 1 body length; max speed 0.261/time; max body lengths 2.2
- replication: splits 249, persistent splits 4, max generation 2, merges 227, nucleations 130
- channel total drift (end/start - 1): [-0.7096, -0.5968]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 394 at frame 154: holes 0, rim-vs-core 0.94, rim-vs-outside 0.43, heterogeneity 0.49; core [0.848, 0.08] rim [0.197, 0.759]
  - track 460 at frame 154: holes 0, rim-vs-core 0.70, rim-vs-outside 0.37, heterogeneity 0.49; core [0.844, 0.14] rim [0.319, 0.602]
  - track 494 at frame 156: holes 0, rim-vs-core 0.88, rim-vs-outside 0.18, heterogeneity 0.49; core [0.731, 0.284] rim [0.086, 0.883]
  - track 936 at frame 222: holes 0, rim-vs-core 0.55, rim-vs-outside 0.32, heterogeneity 0.48; core [0.787, 0.237] rim [0.367, 0.591]

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, lineage.png, timeseries.png, movie.mp4, metrics.json

Measurements are screens, not verdicts: judge them against the images.
