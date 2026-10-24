# Evidence pack: r-two56 (seed 0)

- world: `../../../worlds/r-two56/world.py`, family `lenia`
- parent: screen:two#56; mutation: random 'two' channel/kernel graph
- run: 201 frames x 5 steps x dt 0.1 = time 100; grid [192, 192]; wall 11s; status ok
- command: `python -m labkit.run threads/lenia-multichannel/worlds/r-two56/world.py --out threads/lenia-multichannel/packs/r-two56_damage --seeds 0 1 2 --frames 200 --damage 120:0.5 --no-movie`
- segmentation: matter > 0.35 of robust range [0.0, 2.0], min area 6 px

## Measurements
- components: final 5, mean 6.4, max 16; occupancy final 0.03
- tracks: 111; persistent (alive >= 50% of run): 4; longest 181 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 2.98 (1 = constant size)
- enclosures: components with a hole mean 4.13, final 5; holes at thresholds 0.2/0.35/0.5 final [2, 9, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [5, 5, 5], H1 [13, 0, 0]
- motion: 0 long-lived tracks moved >= 1 body length; max speed 0/time; max body lengths 0.9
- replication: splits 40, persistent splits 1, max generation 1, merges 15, nucleations 2
- channel total drift (end/start - 1): [-0.9312, -0.8422]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 10 at frame 111: holes 1, rim-vs-core 0.75, rim-vs-outside 0.53, heterogeneity 0.47; core [0.857, 0.415] rim [0.186, 0.755]
  - track 13 at frame 101: holes 3, rim-vs-core 0.73, rim-vs-outside 0.46, heterogeneity 0.46; core [0.823, 0.459] rim [0.164, 0.765]
  - track 38 at frame 129: holes 0, rim-vs-core 0.70, rim-vs-outside 0.48, heterogeneity 0.47; core [0.795, 0.436] rim [0.17, 0.754]
  - track 78 at frame 145: holes 1, rim-vs-core 0.49, rim-vs-outside 0.53, heterogeneity 0.47; core [0.537, 0.357] rim [0.28, 0.778]
- damage applied at frame 120: erased 174 px of a 547 px component

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, lineage.png, timeseries.png, movie.mp4, metrics.json

Measurements are screens, not verdicts: judge them against the images.
