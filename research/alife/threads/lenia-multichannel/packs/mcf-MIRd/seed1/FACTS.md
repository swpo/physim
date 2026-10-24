# Evidence pack: mcf-MIRd (seed 1)

- world: `../../../worlds/mcf-MIRd/world.py`, family `lenia`
- parent: mc-MIRd; mutation: matter can only be built from a consumed, regrowing, diffusing food field F (yield 2, regrowth 0.01): replication limited by food
- run: 401 frames x 10 steps x dt 0.1 = time 400; grid [192, 192]; wall 71s; status ok
- command: `python -m labkit.run threads/lenia-multichannel/worlds/mcf-MIRd/world.py --out threads/lenia-multichannel/packs/mcf-MIRd --seeds 0 1 2 --frames 400`
- segmentation: matter > 0.35 of robust range [0.0, 1.0], min area 6 px

## Measurements
- components: final 13, mean 18.7, max 42; occupancy final 0.03
- tracks: 906; persistent (alive >= 50% of run): 1; longest 212 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 1.37 (1 = constant size)
- enclosures: components with a hole mean 0.69, final 1; holes at thresholds 0.2/0.35/0.5 final [1, 1, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [39, 23, 9], H1 [5, 1, 0]
- motion: 3 long-lived tracks moved >= 1 body length; max speed 0.684/time; max body lengths 2.0
- replication: splits 257, persistent splits 3, max generation 1, merges 149, nucleations 238
- channel total drift (end/start - 1): [4.3587, 5.0338, 4.2058, -0.5766]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 368 at frame 296: holes 0, rim-vs-core 0.47, rim-vs-outside 0.99, heterogeneity 0.26; core [1.0, 0.717, 0.427, 0.405] rim [0.81, 0.999, 0.106, 0.401]
  - track 410 at frame 282: holes 0, rim-vs-core 0.59, rim-vs-outside 1.06, heterogeneity 0.26; core [1.0, 0.678, 0.541, 0.439] rim [0.878, 1.0, 0.064, 0.429]
  - track 240 at frame 229: holes 0, rim-vs-core 0.20, rim-vs-outside 0.95, heterogeneity 0.27; core [0.998, 0.884, 0.336, 0.226] rim [0.839, 0.784, 0.41, 0.243]
  - track 361 at frame 259: holes 0, rim-vs-core 0.33, rim-vs-outside 0.90, heterogeneity 0.24; core [0.999, 0.963, 0.302, 0.105] rim [0.827, 0.726, 0.158, 0.132]

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, lineage.png, timeseries.png, movie.mp4, metrics.json

Measurements are screens, not verdicts: judge them against the images.
