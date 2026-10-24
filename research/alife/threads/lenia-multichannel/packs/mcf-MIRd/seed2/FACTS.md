# Evidence pack: mcf-MIRd (seed 2)

- world: `../../../worlds/mcf-MIRd/world.py`, family `lenia`
- parent: mc-MIRd; mutation: matter can only be built from a consumed, regrowing, diffusing food field F (yield 2, regrowth 0.01): replication limited by food
- run: 401 frames x 10 steps x dt 0.1 = time 400; grid [192, 192]; wall 76s; status ok
- command: `python -m labkit.run threads/lenia-multichannel/worlds/mcf-MIRd/world.py --out threads/lenia-multichannel/packs/mcf-MIRd --seeds 0 1 2 --frames 400`
- segmentation: matter > 0.35 of robust range [0.0, 1.0], min area 6 px

## Measurements
- components: final 11, mean 18.6, max 38; occupancy final 0.04
- tracks: 878; persistent (alive >= 50% of run): 0; longest 173 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 0.00 (1 = constant size)
- enclosures: components with a hole mean 0.69, final 1; holes at thresholds 0.2/0.35/0.5 final [0, 1, 2]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [38, 20, 9], H1 [3, 3, 1]
- motion: 4 long-lived tracks moved >= 1 body length; max speed 0.449/time; max body lengths 2.1
- replication: splits 254, persistent splits 6, max generation 3, merges 146, nucleations 225
- channel total drift (end/start - 1): [4.7339, 2.6391, 2.7839, -0.5107]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 383 at frame 282: holes 0, rim-vs-core 0.34, rim-vs-outside 0.93, heterogeneity 0.27; core [1.0, 0.807, 0.442, 0.36] rim [0.774, 0.845, 0.194, 0.371]
  - track 315 at frame 242: holes 0, rim-vs-core 0.33, rim-vs-outside 0.92, heterogeneity 0.25; core [1.0, 0.907, 0.394, 0.368] rim [0.805, 0.807, 0.151, 0.377]
  - track 753 at frame 356: holes 0, rim-vs-core 0.20, rim-vs-outside 0.80, heterogeneity 0.19; core [0.998, 0.0, 0.256, 0.322] rim [0.798, 0.0, 0.238, 0.337]
  - track 288 at frame 212: holes 0, rim-vs-core 0.54, rim-vs-outside 1.00, heterogeneity 0.27; core [1.0, 0.647, 0.511, 0.36] rim [0.875, 0.991, 0.116, 0.356]

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, lineage.png, timeseries.png, movie.mp4, metrics.json

Measurements are screens, not verdicts: judge them against the images.
