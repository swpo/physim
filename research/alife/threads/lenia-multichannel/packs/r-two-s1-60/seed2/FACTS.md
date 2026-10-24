# Evidence pack: r-two-s1-60 (seed 2)

- world: `../../../worlds/r-two-s1-60/world.py`, family `lenia`
- parent: screen:two#60; mutation: random 'two' channel/kernel graph
- run: 301 frames x 5 steps x dt 0.1 = time 150; grid [192, 192]; wall 12s; status ok
- command: `python -m labkit.run threads/lenia-multichannel/worlds/r-two-s1-60/world.py --out threads/lenia-multichannel/packs/r-two-s1-60 --seeds 0 1 2 --frames 300`
- segmentation: matter > 0.35 of robust range [0.0, 1.5016], min area 6 px

## Measurements
- components: final 44, mean 45.1, max 55; occupancy final 0.11
- tracks: 347; persistent (alive >= 50% of run): 30; longest 296 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 12.00 (1 = constant size)
- enclosures: components with a hole mean 0.57, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [63, 47, 43], H1 [5, 0, 0]
- motion: 22 long-lived tracks moved >= 1 body length; max speed 0.617/time; max body lengths 3.0
- replication: splits 95, persistent splits 3, max generation 1, merges 57, nucleations 48
- channel total drift (end/start - 1): [-0.3262, -1.0]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 62 at frame 154: holes 0, rim-vs-core 0.06, rim-vs-outside 0.61, heterogeneity 0.11; core [0.926, 0.0] rim [0.869, 0.0]
  - track 75 at frame 154: holes 0, rim-vs-core 0.01, rim-vs-outside 0.82, heterogeneity 0.07; core [0.977, 0.0] rim [0.964, 0.0]
  - track 76 at frame 154: holes 0, rim-vs-core 0.08, rim-vs-outside 0.70, heterogeneity 0.07; core [0.994, 0.0] rim [0.918, 0.0]
  - track 229 at frame 207: holes 0, rim-vs-core 0.04, rim-vs-outside 0.86, heterogeneity 0.04; core [1.0, 0.0] rim [0.961, 0.0]

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, lineage.png, timeseries.png, movie.mp4, metrics.json

Measurements are screens, not verdicts: judge them against the images.
