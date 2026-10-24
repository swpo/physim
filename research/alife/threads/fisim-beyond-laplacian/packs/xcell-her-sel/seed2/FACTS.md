# Evidence pack: xcell-her-sel (seed 2)

- world: `../../../worlds/xcell-her-sel/world.py`, family `fisim-extended-rd`
- parent: xcell-div; mutation: xcell-div + a bistable marker activator h (-h^3+h-0.2, vacuum = low root, Dh=0.3) tilted toward its on-state inside bodies by a body deposit (kb=0.25) and retained by the membrane gate; marker feeds body kh=0.1 (selection test). Half of the initial cells receive an h poke; h-state is heritable through division.
- run: 201 frames x 100 steps x dt 0.02 = time 400; grid [160, 160]; wall 242s; status ok
- command: `python -m labkit.run threads/fisim-beyond-laplacian/worlds/xcell-her-sel/world.py --out threads/fisim-beyond-laplacian/packs/xcell-her-sel --seeds 0 1 2`
- segmentation: matter > 0.35 of robust range [0.0, 1.9159], min area 6 px

## Measurements
- components: final 17, mean 14.6, max 17; occupancy final 0.20
- tracks: 24; persistent (alive >= 50% of run): 16; longest 201 frames; alive start-to-end: 5
- size of persistent tracks: max/min area ratio 4.84 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [18, 17, 17], H1 [0, 0, 0]
- motion: 4 long-lived tracks moved >= 1 body length; max speed 0.0888/time; max body lengths 2.1
- replication: splits 7, persistent splits 7, max generation 2, merges 0, nucleations 0
- channel total drift (end/start - 1): [0.7537, None, 1.7782]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 0 at frame 101: holes 0, rim-vs-core 0.42, rim-vs-outside 0.92, heterogeneity 0.21; core [0.97, 0.543, 0.966] rim [0.701, 0.763, 0.723]
  - track 1 at frame 101: holes 0, rim-vs-core 0.39, rim-vs-outside 1.03, heterogeneity 0.20; core [0.984, 0.485, 0.992] rim [0.754, 0.725, 0.792]
  - track 6 at frame 101: holes 0, rim-vs-core 0.70, rim-vs-outside 0.65, heterogeneity 0.24; core [0.939, 0.507, 0.988] rim [0.583, 0.89, 0.526]
  - track 20 at frame 145: holes 0, rim-vs-core 0.49, rim-vs-outside 0.43, heterogeneity 0.15; core [0.93, 0.596, 0.092] rim [0.578, 0.941, 0.048]

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, lineage.png, timeseries.png, movie.mp4, metrics.json

Measurements are screens, not verdicts: judge them against the images.
