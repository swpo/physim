# Evidence pack: xcell-her-sel (seed 1)

- world: `../../../worlds/xcell-her-sel/world.py`, family `fisim-extended-rd`
- parent: xcell-div; mutation: xcell-div + a bistable marker activator h (-h^3+h-0.2, vacuum = low root, Dh=0.3) tilted toward its on-state inside bodies by a body deposit (kb=0.25) and retained by the membrane gate; marker feeds body kh=0.1 (selection test). Half of the initial cells receive an h poke; h-state is heritable through division.
- run: 201 frames x 100 steps x dt 0.02 = time 400; grid [160, 160]; wall 229s; status ok
- command: `python -m labkit.run threads/fisim-beyond-laplacian/worlds/xcell-her-sel/world.py --out threads/fisim-beyond-laplacian/packs/xcell-her-sel --seeds 0 1 2`
- segmentation: matter > 0.35 of robust range [0.0, 1.9173], min area 6 px

## Measurements
- components: final 16, mean 13.8, max 16; occupancy final 0.19
- tracks: 22; persistent (alive >= 50% of run): 14; longest 201 frames; alive start-to-end: 8
- size of persistent tracks: max/min area ratio 4.18 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [16, 16, 16], H1 [0, 0, 0]
- motion: 8 long-lived tracks moved >= 1 body length; max speed 0.118/time; max body lengths 1.8
- replication: splits 6, persistent splits 6, max generation 2, merges 0, nucleations 0
- channel total drift (end/start - 1): [0.7432, None, 1.9131]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 0 at frame 101: holes 0, rim-vs-core 0.49, rim-vs-outside 0.86, heterogeneity 0.23; core [0.967, 0.535, 0.959] rim [0.693, 0.79, 0.648]
  - track 1 at frame 101: holes 0, rim-vs-core 0.49, rim-vs-outside 0.87, heterogeneity 0.23; core [0.97, 0.552, 0.984] rim [0.688, 0.791, 0.668]
  - track 2 at frame 101: holes 0, rim-vs-core 0.47, rim-vs-outside 0.88, heterogeneity 0.21; core [0.958, 0.549, 0.993] rim [0.68, 0.793, 0.7]
  - track 14 at frame 141: holes 0, rim-vs-core 0.49, rim-vs-outside 0.43, heterogeneity 0.14; core [0.928, 0.613, 0.092] rim [0.57, 0.943, 0.047]

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, lineage.png, timeseries.png, movie.mp4, metrics.json

Measurements are screens, not verdicts: judge them against the images.
