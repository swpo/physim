# Evidence pack: xcell-div-nofb (seed 0)

- world: `../../worlds/xcell-div-nofb/world.py`, family `fisim-extended-rd`
- parent: xcell-div; mutation: ablation: cargo feedback on body removed (kc=0)
- run: 201 frames x 100 steps x dt 0.02 = time 400; grid [160, 160]; wall 152s; status ok
- command: `python -m labkit.run threads/fisim-beyond-laplacian/worlds/xcell-div-nofb/world.py --out threads/fisim-beyond-laplacian/packs/xcell-div-nofb --seeds 0`
- segmentation: matter > 0.35 of robust range [0.0, 1.8403], min area 6 px

## Measurements
- components: final 8, mean 8.0, max 8; occupancy final 0.05
- tracks: 8; persistent (alive >= 50% of run): 8; longest 201 frames; alive start-to-end: 8
- size of persistent tracks: max/min area ratio 3.92 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [8, 8, 8], H1 [0, 0, 0]
- motion: 8 long-lived tracks moved >= 1 body length; max speed 0.11/time; max body lengths 3.6
- replication: splits 0, persistent splits 0, max generation 0, merges 0, nucleations 0
- channel total drift (end/start - 1): [-0.5125, None, -0.4246]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 0 at frame 101: holes 0, rim-vs-core 0.47, rim-vs-outside 0.62, heterogeneity 0.19; core [0.935, 0.678, 0.897] rim [0.647, 0.923, 0.614]
  - track 1 at frame 101: holes 0, rim-vs-core 0.55, rim-vs-outside 0.51, heterogeneity 0.19; core [0.933, 0.69, 0.895] rim [0.596, 0.971, 0.561]
  - track 2 at frame 101: holes 0, rim-vs-core 0.56, rim-vs-outside 0.52, heterogeneity 0.19; core [0.933, 0.696, 0.896] rim [0.584, 0.974, 0.553]
  - track 3 at frame 101: holes 0, rim-vs-core 0.55, rim-vs-outside 0.52, heterogeneity 0.19; core [0.933, 0.694, 0.9] rim [0.595, 0.971, 0.567]

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, lineage.png, timeseries.png, movie.mp4, metrics.json

Measurements are screens, not verdicts: judge them against the images.
