# Evidence pack: r-two56 (seed 1)

- world: `../../../worlds/r-two56/world.py`, family `lenia`
- parent: screen:two#56; mutation: random 'two' channel/kernel graph
- run: 201 frames x 5 steps x dt 0.1 = time 100; grid [192, 192]; wall 8s; status ok
- command: `python -m labkit.run threads/lenia-multichannel/worlds/r-two56/world.py --out threads/lenia-multichannel/packs/r-two56 --seeds 0 1 2 --frames 200`
- segmentation: matter > 0.35 of robust range [0.0, 2.0], min area 6 px

## Measurements
- components: final 5, mean 5.1, max 15; occupancy final 0.04
- tracks: 100; persistent (alive >= 50% of run): 2; longest 151 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 1.49 (1 = constant size)
- enclosures: components with a hole mean 3.46, final 3; holes at thresholds 0.2/0.35/0.5 final [1, 6, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [7, 6, 5], H1 [11, 0, 0]
- motion: 0 long-lived tracks moved >= 1 body length; max speed 0/time; max body lengths 0.8
- replication: splits 41, persistent splits 2, max generation 1, merges 8, nucleations 2
- channel total drift (end/start - 1): [-0.9099, -0.8109]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 37 at frame 126: holes 1, rim-vs-core 0.65, rim-vs-outside 0.53, heterogeneity 0.47; core [0.669, 0.429] rim [0.141, 0.811]
  - track 76 at frame 148: holes 2, rim-vs-core 0.88, rim-vs-outside 0.48, heterogeneity 0.48; core [0.871, 0.307] rim [0.15, 0.806]
  - track 11 at frame 50: holes 1, rim-vs-core 0.46, rim-vs-outside 0.46, heterogeneity 0.45; core [0.615, 0.39] rim [0.29, 0.711]
  - track 81 at frame 146: holes 1, rim-vs-core 0.72, rim-vs-outside 0.49, heterogeneity 0.47; core [0.766, 0.368] rim [0.178, 0.78]

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, lineage.png, timeseries.png, movie.mp4, metrics.json

Measurements are screens, not verdicts: judge them against the images.
