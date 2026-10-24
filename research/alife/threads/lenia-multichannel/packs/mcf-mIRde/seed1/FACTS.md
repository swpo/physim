# Evidence pack: mcf-mIRde (seed 1)

- world: `../../../worlds/mcf-mIRde/world.py`, family `lenia`
- parent: mc-mIRde; mutation: matter can only be built from a consumed, regrowing, diffusing food field F (yield 2): population limited by food supply
- run: 301 frames x 10 steps x dt 0.1 = time 300; grid [192, 192]; wall 62s; status ok
- command: `python -m labkit.run threads/lenia-multichannel/worlds/mcf-mIRde/world.py --out threads/lenia-multichannel/packs/mcf-mIRde --seeds 0 1 2 --frames 300`
- segmentation: matter > 0.35 of robust range [0.0, 2.4813], min area 6 px

## Measurements
- components: final 0, mean 1.7, max 10; occupancy final 0.00
- tracks: 87; persistent (alive >= 50% of run): 0; longest 56 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 0.00 (1 = constant size)
- enclosures: components with a hole mean 0.29, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [0, 0, 0], H1 [0, 0, 0]
- motion: 2 long-lived tracks moved >= 1 body length; max speed 0.633/time; max body lengths 1.4
- replication: splits 27, persistent splits 0, max generation 0, merges 12, nucleations 15
- channel total drift (end/start - 1): [-1.0, -1.0, -1.0, -0.0025]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 9 at frame 43: holes 0, rim-vs-core 0.40, rim-vs-outside 0.67, heterogeneity 0.31; core [0.83, 0.887, 0.452, 0.001] rim [0.518, 0.77, 0.23, 0.041]
  - track 13 at frame 40: holes 0, rim-vs-core 0.30, rim-vs-outside 0.79, heterogeneity 0.26; core [0.813, 0.941, 0.507, 0.0] rim [0.671, 0.726, 0.354, 0.024]
  - track 11 at frame 35: holes 0, rim-vs-core 0.42, rim-vs-outside 0.90, heterogeneity 0.25; core [0.884, 0.91, 0.669, 0.006] rim [0.644, 0.875, 0.33, 0.038]
  - track 12 at frame 35: holes 0, rim-vs-core 0.41, rim-vs-outside 0.63, heterogeneity 0.30; core [0.854, 0.866, 0.552, 0.013] rim [0.556, 0.689, 0.344, 0.061]

## Warnings
- no components at the end: matter died out or fell below threshold
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, lineage.png, timeseries.png, movie.mp4, metrics.json

Measurements are screens, not verdicts: judge them against the images.
