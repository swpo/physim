# Evidence pack: r-two-s1-85 (seed 1)

- world: `../../../worlds/r-two-s1-85/world.py`, family `lenia`
- parent: screen:two#85; mutation: random 'two' channel/kernel graph
- run: 301 frames x 5 steps x dt 0.1 = time 150; grid [192, 192]; wall 12s; status ok
- command: `python -m labkit.run threads/lenia-multichannel/worlds/r-two-s1-85/world.py --out threads/lenia-multichannel/packs/r-two-s1-85 --seeds 0 1 2 --frames 300`
- segmentation: matter > 0.35 of robust range [0.0, 2.0], min area 6 px

## Measurements
- components: final 28, mean 33.6, max 215; occupancy final 0.10
- tracks: 796; persistent (alive >= 50% of run): 15; longest 298 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 2.62 (1 = constant size)
- enclosures: components with a hole mean 3.45, final 5; holes at thresholds 0.2/0.35/0.5 final [0, 7, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [52, 36, 23], H1 [20, 0, 0]
- motion: 0 long-lived tracks moved >= 1 body length; max speed 0/time; max body lengths 1.1
- replication: splits 167, persistent splits 6, max generation 2, merges 185, nucleations 118
- channel total drift (end/start - 1): [-0.6917, -0.5673]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 272 at frame 151: holes 0, rim-vs-core 0.75, rim-vs-outside 0.44, heterogeneity 0.49; core [0.956, 0.077] rim [0.388, 0.569]
  - track 327 at frame 154: holes 0, rim-vs-core 0.50, rim-vs-outside 0.30, heterogeneity 0.49; core [0.724, 0.265] rim [0.36, 0.605]
  - track 331 at frame 154: holes 0, rim-vs-core 0.55, rim-vs-outside 0.26, heterogeneity 0.49; core [0.707, 0.251] rim [0.305, 0.63]
  - track 737 at frame 229: holes 0, rim-vs-core 0.99, rim-vs-outside 0.12, heterogeneity 0.48; core [0.874, 0.153] rim [0.094, 0.758]

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, lineage.png, timeseries.png, movie.mp4, metrics.json

Measurements are screens, not verdicts: judge them against the images.
