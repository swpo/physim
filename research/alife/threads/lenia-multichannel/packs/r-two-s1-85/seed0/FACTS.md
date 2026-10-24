# Evidence pack: r-two-s1-85 (seed 0)

- world: `../../../worlds/r-two-s1-85/world.py`, family `lenia`
- parent: screen:two#85; mutation: random 'two' channel/kernel graph
- run: 301 frames x 5 steps x dt 0.1 = time 150; grid [192, 192]; wall 15s; status ok
- command: `python -m labkit.run threads/lenia-multichannel/worlds/r-two-s1-85/world.py --out threads/lenia-multichannel/packs/r-two-s1-85 --seeds 0 1 2 --frames 300`
- segmentation: matter > 0.35 of robust range [0.0, 2.0], min area 6 px

## Measurements
- components: final 28, mean 31.8, max 212; occupancy final 0.11
- tracks: 1161; persistent (alive >= 50% of run): 8; longest 298 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 2.57 (1 = constant size)
- enclosures: components with a hole mean 6.01, final 5; holes at thresholds 0.2/0.35/0.5 final [10, 15, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [88, 47, 10], H1 [48, 9, 0]
- motion: 1 long-lived tracks moved >= 1 body length; max speed 0.0675/time; max body lengths 2.0
- replication: splits 294, persistent splits 0, max generation 0, merges 302, nucleations 130
- channel total drift (end/start - 1): [-0.6444, -0.5308]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 325 at frame 151: holes 0, rim-vs-core 0.81, rim-vs-outside 0.16, heterogeneity 0.49; core [0.775, 0.268] rim [0.148, 0.78]
  - track 350 at frame 154: holes 0, rim-vs-core 0.79, rim-vs-outside 0.39, heterogeneity 0.49; core [0.859, 0.122] rim [0.293, 0.672]
  - track 463 at frame 156: holes 0, rim-vs-core 0.89, rim-vs-outside 0.15, heterogeneity 0.49; core [0.775, 0.222] rim [0.125, 0.829]
  - track 469 at frame 156: holes 1, rim-vs-core 0.78, rim-vs-outside 0.22, heterogeneity 0.49; core [0.839, 0.236] rim [0.246, 0.737]

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, lineage.png, timeseries.png, movie.mp4, metrics.json

Measurements are screens, not verdicts: judge them against the images.
