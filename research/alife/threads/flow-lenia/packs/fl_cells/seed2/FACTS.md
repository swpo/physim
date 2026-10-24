# Evidence pack: fl_cells (seed 2)

- world: `../../../worlds/fl_cells/world.py`, family `flow-lenia`
- parent: flow-lenia/fl_base; mutation: 3-channel random rule 0 at R_scale 0.4 from 6 noise patches: layered cells (screen pop_r0)
- run: 201 frames x 10 steps x dt 0.2 = time 400; grid [128, 128]; wall 24s; status ok
- command: `python -m labkit.run threads/flow-lenia/worlds/fl_cells/world.py --out threads/flow-lenia/packs/fl_cells --frames 200 --seeds 0 1 2`
- segmentation: matter > 0.35 of robust range [0.0, 1.9933], min area 6 px

## Measurements
- components: final 5, mean 6.4, max 12; occupancy final 0.10
- tracks: 51; persistent (alive >= 50% of run): 7; longest 199 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 1.17 (1 = constant size)
- enclosures: components with a hole mean 2.50, final 3; holes at thresholds 0.2/0.35/0.5 final [4, 9, 2]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [18, 5, 4], H1 [11, 8, 2]
- motion: 1 long-lived tracks moved >= 1 body length; max speed 0.0618/time; max body lengths 2.0
- replication: splits 17, persistent splits 0, max generation 0, merges 13, nucleations 0
- channel total drift (end/start - 1): [-0.0, 0.0, 0.0]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 11 at frame 101: holes 1, rim-vs-core 0.32, rim-vs-outside 0.45, heterogeneity 0.09; core [0.987, 0.0, 0.164] rim [0.709, 0.0, 0.014]
  - track 7 at frame 59: holes 0, rim-vs-core 0.22, rim-vs-outside 0.48, heterogeneity 0.09; core [0.907, 0.0, 0.132] rim [0.731, 0.0, 0.003]
  - track 9 at frame 59: holes 0, rim-vs-core 0.22, rim-vs-outside 0.48, heterogeneity 0.08; core [0.93, 0.0, 0.128] rim [0.75, 0.0, 0.009]

## Warnings
- none

## Files
sheet.png, tracks.png, lineage.png, timeseries.png, movie.mp4, metrics.json

Measurements are screens, not verdicts: judge them against the images.
