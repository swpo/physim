# Evidence pack: xcell-her (seed 1)

- world: `../../../worlds/xcell-her/world.py`, family `fisim-extended-rd`
- parent: xcell-div; mutation: xcell-div + a bistable marker activator h (-h^3+h-0.2, vacuum = low root, Dh=0.3) tilted toward its on-state inside bodies by a body deposit (kb=0.25) and retained by the membrane gate; neutral marker kh=0. Half of the initial cells receive an h poke; h-state is heritable through division.
- run: 201 frames x 100 steps x dt 0.02 = time 400; grid [160, 160]; wall 231s; status ok
- command: `python -m labkit.run threads/fisim-beyond-laplacian/worlds/xcell-her/world.py --out threads/fisim-beyond-laplacian/packs/xcell-her --seeds 0 1 2`
- segmentation: matter > 0.35 of robust range [0.0, 1.8789], min area 6 px

## Measurements
- components: final 23, mean 18.3, max 23; occupancy final 0.16
- tracks: 36; persistent (alive >= 50% of run): 17; longest 201 frames; alive start-to-end: 3
- size of persistent tracks: max/min area ratio 1.61 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [23, 23, 23], H1 [0, 0, 0]
- motion: 4 long-lived tracks moved >= 1 body length; max speed 0.0533/time; max body lengths 1.2
- replication: splits 13, persistent splits 13, max generation 2, merges 0, nucleations 0
- channel total drift (end/start - 1): [0.4736, None, 0.5473]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 1 at frame 101: holes 0, rim-vs-core 0.70, rim-vs-outside 0.64, heterogeneity 0.24; core [0.934, 0.592, 0.99] rim [0.567, 0.936, 0.498]
  - track 3 at frame 101: holes 0, rim-vs-core 0.50, rim-vs-outside 0.44, heterogeneity 0.15; core [0.939, 0.583, 0.093] rim [0.587, 0.938, 0.049]
  - track 7 at frame 101: holes 0, rim-vs-core 0.68, rim-vs-outside 0.66, heterogeneity 0.24; core [0.935, 0.586, 0.988] rim [0.583, 0.936, 0.526]
  - track 24 at frame 138: holes 0, rim-vs-core 0.48, rim-vs-outside 0.44, heterogeneity 0.14; core [0.939, 0.598, 0.092] rim [0.588, 0.928, 0.048]

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, lineage.png, timeseries.png, movie.mp4, metrics.json

Measurements are screens, not verdicts: judge them against the images.
