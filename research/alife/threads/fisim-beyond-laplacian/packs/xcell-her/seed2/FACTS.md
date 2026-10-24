# Evidence pack: xcell-her (seed 2)

- world: `../../../worlds/xcell-her/world.py`, family `fisim-extended-rd`
- parent: xcell-div; mutation: xcell-div + a bistable marker activator h (-h^3+h-0.2, vacuum = low root, Dh=0.3) tilted toward its on-state inside bodies by a body deposit (kb=0.25) and retained by the membrane gate; neutral marker kh=0. Half of the initial cells receive an h poke; h-state is heritable through division.
- run: 201 frames x 100 steps x dt 0.02 = time 400; grid [160, 160]; wall 234s; status ok
- command: `python -m labkit.run threads/fisim-beyond-laplacian/worlds/xcell-her/world.py --out threads/fisim-beyond-laplacian/packs/xcell-her --seeds 0 1 2`
- segmentation: matter > 0.35 of robust range [0.0, 1.8706], min area 6 px

## Measurements
- components: final 19, mean 17.0, max 19; occupancy final 0.14
- tracks: 28; persistent (alive >= 50% of run): 19; longest 201 frames; alive start-to-end: 1
- size of persistent tracks: max/min area ratio 1.53 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [19, 19, 19], H1 [0, 0, 0]
- motion: 3 long-lived tracks moved >= 1 body length; max speed 0.0535/time; max body lengths 1.2
- replication: splits 9, persistent splits 9, max generation 1, merges 0, nucleations 0
- channel total drift (end/start - 1): [0.2887, None, 0.5876]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 1 at frame 101: holes 0, rim-vs-core 0.38, rim-vs-outside 0.89, heterogeneity 0.24; core [0.919, 0.64, 0.985] rim [0.719, 0.783, 0.697]
  - track 10 at frame 121: holes 0, rim-vs-core 0.51, rim-vs-outside 0.44, heterogeneity 0.15; core [0.941, 0.577, 0.092] rim [0.59, 0.942, 0.048]
  - track 11 at frame 121: holes 0, rim-vs-core 0.52, rim-vs-outside 0.44, heterogeneity 0.15; core [0.938, 0.583, 0.092] rim [0.571, 0.943, 0.047]
  - track 12 at frame 121: holes 0, rim-vs-core 0.51, rim-vs-outside 0.44, heterogeneity 0.15; core [0.94, 0.579, 0.092] rim [0.58, 0.942, 0.048]

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, lineage.png, timeseries.png, movie.mp4, metrics.json

Measurements are screens, not verdicts: judge them against the images.
