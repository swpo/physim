# Evidence pack: mcf-mIRde (seed 2)

- world: `../../../worlds/mcf-mIRde/world.py`, family `lenia`
- parent: mc-mIRde; mutation: matter can only be built from a consumed, regrowing, diffusing food field F (yield 2): population limited by food supply
- run: 301 frames x 10 steps x dt 0.1 = time 300; grid [192, 192]; wall 61s; status ok
- command: `python -m labkit.run threads/lenia-multichannel/worlds/mcf-mIRde/world.py --out threads/lenia-multichannel/packs/mcf-mIRde --seeds 0 1 2 --frames 300`
- segmentation: matter > 0.35 of robust range [0.0, 2.5753], min area 6 px

## Measurements
- components: final 1, mean 3.0, max 14; occupancy final 0.01
- tracks: 166; persistent (alive >= 50% of run): 0; longest 59 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 0.00 (1 = constant size)
- enclosures: components with a hole mean 0.50, final 1; holes at thresholds 0.2/0.35/0.5 final [0, 2, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [3, 3, 1], H1 [2, 0, 0]
- motion: 4 long-lived tracks moved >= 1 body length; max speed 0.838/time; max body lengths 1.8
- replication: splits 53, persistent splits 3, max generation 1, merges 28, nucleations 32
- channel total drift (end/start - 1): [-0.5091, -0.5314, -0.7609, -0.0555]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 6 at frame 45: holes 0, rim-vs-core 0.28, rim-vs-outside 0.52, heterogeneity 0.33; core [0.6, 0.862, 0.319, 0.051] rim [0.515, 0.598, 0.304, 0.108]
  - track 3 at frame 43: holes 0, rim-vs-core 0.30, rim-vs-outside 0.60, heterogeneity 0.31; core [0.611, 0.926, 0.261, 0.045] rim [0.558, 0.642, 0.319, 0.113]
  - track 8 at frame 43: holes 0, rim-vs-core 0.30, rim-vs-outside 0.60, heterogeneity 0.31; core [0.611, 0.926, 0.261, 0.045] rim [0.558, 0.642, 0.319, 0.113]
  - track 4 at frame 33: holes 0, rim-vs-core 0.32, rim-vs-outside 0.69, heterogeneity 0.30; core [0.719, 0.81, 0.539, 0.059] rim [0.487, 0.731, 0.362, 0.15]

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, lineage.png, timeseries.png, movie.mp4, metrics.json

Measurements are screens, not verdicts: judge them against the images.
