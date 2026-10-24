# Evidence pack: fl_cells (seed 2)

- world: `../../../worlds/fl_cells/world.py`, family `flow-lenia`
- parent: flow-lenia/fl_base; mutation: 3-channel random rule 0 at R_scale 0.4 from 6 noise patches: layered cells (screen pop_r0)
- run: 201 frames x 10 steps x dt 0.2 = time 400; grid [128, 128]; wall 28s; status ok
- command: `python -m labkit.run threads/flow-lenia/worlds/fl_cells/world.py --out threads/flow-lenia/packs/fl_cells_damage/seed2 --frames 200 --seeds 2 --damage 60:0.7`
- segmentation: matter > 0.35 of robust range [0.0, 1.9572], min area 6 px

## Measurements
- components: final 4, mean 6.2, max 12; occupancy final 0.09
- tracks: 44; persistent (alive >= 50% of run): 6; longest 199 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 1.16 (1 = constant size)
- enclosures: components with a hole mean 2.41, final 3; holes at thresholds 0.2/0.35/0.5 final [5, 9, 3]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [21, 5, 3], H1 [11, 10, 4]
- motion: 0 long-lived tracks moved >= 1 body length; max speed 0/time; max body lengths 0.5
- replication: splits 12, persistent splits 0, max generation 0, merges 12, nucleations 1
- channel total drift (end/start - 1): [-0.2006, -0.1029, -0.0595]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 11 at frame 101: holes 1, rim-vs-core 0.35, rim-vs-outside 0.45, heterogeneity 0.09; core [0.984, 0.0, 0.157] rim [0.669, 0.0, 0.014]
  - track 7 at frame 59: holes 0, rim-vs-core 0.23, rim-vs-outside 0.48, heterogeneity 0.10; core [0.908, 0.0, 0.132] rim [0.717, 0.0, 0.003]
  - track 9 at frame 59: holes 0, rim-vs-core 0.22, rim-vs-outside 0.48, heterogeneity 0.08; core [0.93, 0.0, 0.129] rim [0.751, 0.0, 0.009]
- damage applied at frame 60: erased 259 px of a 741 px component

## Warnings
- none

## Files
sheet.png, tracks.png, lineage.png, timeseries.png, movie.mp4, metrics.json

Measurements are screens, not verdicts: judge them against the images.
