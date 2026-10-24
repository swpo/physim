# Evidence pack: xcell-her (seed 0)

- world: `../../../worlds/xcell-her/world.py`, family `fisim-extended-rd`
- parent: xcell-div; mutation: xcell-div + a bistable marker activator h (-h^3+h-0.2, vacuum = low root, Dh=0.3) tilted toward its on-state inside bodies by a body deposit (kb=0.25) and retained by the membrane gate; neutral marker kh=0. Half of the initial cells receive an h poke; h-state is heritable through division.
- run: 201 frames x 100 steps x dt 0.02 = time 400; grid [160, 160]; wall 242s; status ok
- command: `python -m labkit.run threads/fisim-beyond-laplacian/worlds/xcell-her/world.py --out threads/fisim-beyond-laplacian/packs/xcell-her --seeds 0 1 2`
- segmentation: matter > 0.35 of robust range [0.0, 1.8756], min area 6 px

## Measurements
- components: final 21, mean 18.1, max 21; occupancy final 0.16
- tracks: 32; persistent (alive >= 50% of run): 21; longest 164 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 1.38 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [21, 21, 21], H1 [0, 0, 0]
- motion: 5 long-lived tracks moved >= 1 body length; max speed 0.0561/time; max body lengths 1.3
- replication: splits 11, persistent splits 11, max generation 2, merges 0, nucleations 0
- channel total drift (end/start - 1): [0.3863, None, 0.9844]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 10 at frame 119: holes 0, rim-vs-core 0.67, rim-vs-outside 0.66, heterogeneity 0.24; core [0.938, 0.586, 0.988] rim [0.585, 0.935, 0.53]
  - track 11 at frame 119: holes 0, rim-vs-core 0.40, rim-vs-outside 0.87, heterogeneity 0.24; core [0.924, 0.644, 0.985] rim [0.711, 0.785, 0.674]
  - track 12 at frame 121: holes 0, rim-vs-core 0.70, rim-vs-outside 0.64, heterogeneity 0.24; core [0.935, 0.591, 0.988] rim [0.57, 0.933, 0.499]
  - track 30 at frame 150: holes 0, rim-vs-core 0.48, rim-vs-outside 0.47, heterogeneity 0.15; core [0.941, 0.571, 0.093] rim [0.605, 0.915, 0.05]

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, lineage.png, timeseries.png, movie.mp4, metrics.json

Measurements are screens, not verdicts: judge them against the images.
