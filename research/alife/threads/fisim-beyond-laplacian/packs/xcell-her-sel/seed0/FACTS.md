# Evidence pack: xcell-her-sel (seed 0)

- world: `../../../worlds/xcell-her-sel/world.py`, family `fisim-extended-rd`
- parent: xcell-div; mutation: xcell-div + a bistable marker activator h (-h^3+h-0.2, vacuum = low root, Dh=0.3) tilted toward its on-state inside bodies by a body deposit (kb=0.25) and retained by the membrane gate; marker feeds body kh=0.1 (selection test). Half of the initial cells receive an h poke; h-state is heritable through division.
- run: 201 frames x 100 steps x dt 0.02 = time 400; grid [160, 160]; wall 239s; status ok
- command: `python -m labkit.run threads/fisim-beyond-laplacian/worlds/xcell-her-sel/world.py --out threads/fisim-beyond-laplacian/packs/xcell-her-sel --seeds 0 1 2`
- segmentation: matter > 0.35 of robust range [0.0, 1.9218], min area 6 px

## Measurements
- components: final 15, mean 13.6, max 15; occupancy final 0.21
- tracks: 20; persistent (alive >= 50% of run): 13; longest 201 frames; alive start-to-end: 6
- size of persistent tracks: max/min area ratio 4.18 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [16, 15, 15], H1 [0, 0, 0]
- motion: 3 long-lived tracks moved >= 1 body length; max speed 0.0888/time; max body lengths 2.2
- replication: splits 5, persistent splits 5, max generation 2, merges 0, nucleations 0
- channel total drift (end/start - 1): [0.8605, None, 2.5611]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 0 at frame 101: holes 0, rim-vs-core 0.36, rim-vs-outside 1.00, heterogeneity 0.21; core [0.966, 0.52, 0.984] rim [0.753, 0.723, 0.785]
  - track 1 at frame 101: holes 0, rim-vs-core 0.56, rim-vs-outside 0.79, heterogeneity 0.25; core [0.966, 0.531, 0.959] rim [0.668, 0.811, 0.576]
  - track 2 at frame 101: holes 0, rim-vs-core 0.69, rim-vs-outside 0.62, heterogeneity 0.24; core [0.929, 0.533, 0.973] rim [0.578, 0.88, 0.497]
  - track 18 at frame 155: holes 0, rim-vs-core 0.48, rim-vs-outside 0.43, heterogeneity 0.14; core [0.928, 0.621, 0.092] rim [0.568, 0.938, 0.047]

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, lineage.png, timeseries.png, movie.mp4, metrics.json

Measurements are screens, not verdicts: judge them against the images.
