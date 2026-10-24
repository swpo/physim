# Evidence pack: xcell-turn-leaky (seed 0)

- world: `../../worlds/xcell-turn-leaky/world.py`, family `fisim-extended-rd`
- parent: xcell-turn; mutation: ablation: waste not trapped by the membrane (gate beta_q=0)
- run: 201 frames x 200 steps x dt 0.02 = time 800; grid [128, 128]; wall 222s; status ok
- command: `python -m labkit.run threads/fisim-beyond-laplacian/worlds/xcell-turn-leaky/world.py --out threads/fisim-beyond-laplacian/packs/xcell-turn-leaky --seeds 0`
- segmentation: matter > 0.35 of robust range [0.0, 1.8525], min area 6 px

## Measurements
- components: final 8, mean 8.0, max 8; occupancy final 0.09
- tracks: 8; persistent (alive >= 50% of run): 8; longest 201 frames; alive start-to-end: 8
- size of persistent tracks: max/min area ratio 4.15 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [8, 8, 8], H1 [0, 0, 0]
- motion: 2 long-lived tracks moved >= 1 body length; max speed 0.0195/time; max body lengths 1.1
- replication: splits 0, persistent splits 0, max generation 0, merges 0, nucleations 0
- channel total drift (end/start - 1): [-0.3352, None, -0.2324, -0.6243]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 0 at frame 101: holes 0, rim-vs-core 0.66, rim-vs-outside 0.53, heterogeneity 0.19; core [0.937, 0.603, 0.878, 0.843] rim [0.567, 0.965, 0.526, 0.642]
  - track 1 at frame 101: holes 0, rim-vs-core 0.65, rim-vs-outside 0.55, heterogeneity 0.19; core [0.936, 0.602, 0.881, 0.842] rim [0.577, 0.965, 0.536, 0.643]
  - track 2 at frame 101: holes 0, rim-vs-core 0.66, rim-vs-outside 0.54, heterogeneity 0.19; core [0.935, 0.604, 0.879, 0.829] rim [0.567, 0.967, 0.529, 0.628]
  - track 3 at frame 101: holes 0, rim-vs-core 0.31, rim-vs-outside 0.76, heterogeneity 0.19; core [0.921, 0.666, 0.848, 0.825] rim [0.716, 0.797, 0.673, 0.737]

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, lineage.png, timeseries.png, movie.mp4, metrics.json

Measurements are screens, not verdicts: judge them against the images.
