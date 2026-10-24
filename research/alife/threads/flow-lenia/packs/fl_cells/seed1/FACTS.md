# Evidence pack: fl_cells (seed 1)

- world: `../../../worlds/fl_cells/world.py`, family `flow-lenia`
- parent: flow-lenia/fl_base; mutation: 3-channel random rule 0 at R_scale 0.4 from 6 noise patches: layered cells (screen pop_r0)
- run: 201 frames x 10 steps x dt 0.2 = time 400; grid [128, 128]; wall 24s; status ok
- command: `python -m labkit.run threads/flow-lenia/worlds/fl_cells/world.py --out threads/flow-lenia/packs/fl_cells --frames 200 --seeds 0 1 2`
- segmentation: matter > 0.35 of robust range [0.0, 1.9862], min area 6 px

## Measurements
- components: final 6, mean 7.8, max 11; occupancy final 0.09
- tracks: 20; persistent (alive >= 50% of run): 9; longest 201 frames; alive start-to-end: 1
- size of persistent tracks: max/min area ratio 1.29 (1 = constant size)
- enclosures: components with a hole mean 2.53, final 2; holes at thresholds 0.2/0.35/0.5 final [4, 8, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [13, 6, 4], H1 [14, 10, 2]
- motion: 0 long-lived tracks moved >= 1 body length; max speed 0/time; max body lengths 0.6
- replication: splits 4, persistent splits 0, max generation 0, merges 5, nucleations 0
- channel total drift (end/start - 1): [-0.0, -0.0, 0.0]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 4 at frame 101: holes 4, rim-vs-core 0.36, rim-vs-outside 0.37, heterogeneity 0.33; core [0.528, 0.021, 0.186] rim [0.286, 0.283, 0.191]
  - track 9 at frame 101: holes 0, rim-vs-core 0.26, rim-vs-outside 0.44, heterogeneity 0.07; core [0.964, 0.0, 0.128] rim [0.729, 0.0, 0.014]
  - track 14 at frame 101: holes 0, rim-vs-core 0.25, rim-vs-outside 0.46, heterogeneity 0.08; core [0.946, 0.0, 0.133] rim [0.722, 0.0, 0.013]

## Warnings
- none

## Files
sheet.png, tracks.png, lineage.png, timeseries.png, movie.mp4, metrics.json

Measurements are screens, not verdicts: judge them against the images.
