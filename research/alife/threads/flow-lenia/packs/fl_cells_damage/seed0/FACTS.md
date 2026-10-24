# Evidence pack: fl_cells (seed 0)

- world: `../../../worlds/fl_cells/world.py`, family `flow-lenia`
- parent: flow-lenia/fl_base; mutation: 3-channel random rule 0 at R_scale 0.4 from 6 noise patches: layered cells (screen pop_r0)
- run: 201 frames x 10 steps x dt 0.2 = time 400; grid [128, 128]; wall 28s; status ok
- command: `python -m labkit.run threads/flow-lenia/worlds/fl_cells/world.py --out threads/flow-lenia/packs/fl_cells_damage/seed0 --frames 200 --seeds 0 --damage 60:0.7`
- segmentation: matter > 0.35 of robust range [0.0, 1.9893], min area 6 px

## Measurements
- components: final 7, mean 6.7, max 10; occupancy final 0.09
- tracks: 40; persistent (alive >= 50% of run): 5; longest 199 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 1.14 (1 = constant size)
- enclosures: components with a hole mean 1.94, final 2; holes at thresholds 0.2/0.35/0.5 final [7, 5, 1]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [14, 7, 4], H1 [12, 6, 1]
- motion: 0 long-lived tracks moved >= 1 body length; max speed 0/time; max body lengths 0.4
- replication: splits 11, persistent splits 3, max generation 2, merges 11, nucleations 0
- channel total drift (end/start - 1): [-0.1604, -0.0872, -0.0272]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 9 at frame 101: holes 0, rim-vs-core 0.30, rim-vs-outside 0.45, heterogeneity 0.07; core [0.995, 0.0, 0.124] rim [0.708, 0.0, 0.029]
  - track 13 at frame 101: holes 0, rim-vs-core 0.24, rim-vs-outside 0.45, heterogeneity 0.09; core [0.926, 0.0, 0.134] rim [0.716, 0.0, 0.01]
  - track 38 at frame 178: holes 0, rim-vs-core 0.47, rim-vs-outside 0.43, heterogeneity 0.21; core [0.004, 0.913, 0.016] rim [0.005, 0.483, 0.216]
- damage applied at frame 60: erased 186 px of a 489 px component

## Warnings
- none

## Files
sheet.png, tracks.png, lineage.png, timeseries.png, movie.mp4, metrics.json

Measurements are screens, not verdicts: judge them against the images.
