# Evidence pack: fl_cells (seed 1)

- world: `../../worlds/fl_cells/world.py`, family `flow-lenia`
- parent: flow-lenia/fl_base; mutation: 3-channel random rule 0 at R_scale 0.4 from 6 noise patches: layered cells (screen pop_r0)
- run: 201 frames x 10 steps x dt 0.2 = time 400; grid [128, 128]; wall 28s; status ok
- command: `python -m labkit.run threads/flow-lenia/worlds/fl_cells/world.py --out threads/flow-lenia/packs/fl_cells_damage --frames 200 --seeds 1 --damage 60:0.7`
- segmentation: matter > 0.35 of robust range [0.0, 1.9643], min area 6 px

## Measurements
- components: final 6, mean 7.8, max 11; occupancy final 0.08
- tracks: 26; persistent (alive >= 50% of run): 9; longest 199 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 1.14 (1 = constant size)
- enclosures: components with a hole mean 2.44, final 2; holes at thresholds 0.2/0.35/0.5 final [4, 5, 2]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [15, 6, 4], H1 [11, 6, 1]
- motion: 0 long-lived tracks moved >= 1 body length; max speed 0/time; max body lengths 0.5
- replication: splits 6, persistent splits 0, max generation 0, merges 7, nucleations 0
- channel total drift (end/start - 1): [-0.1731, -0.0728, -0.0582]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 9 at frame 101: holes 0, rim-vs-core 0.26, rim-vs-outside 0.44, heterogeneity 0.07; core [0.965, 0.0, 0.128] rim [0.73, 0.0, 0.014]
  - track 14 at frame 101: holes 0, rim-vs-core 0.25, rim-vs-outside 0.46, heterogeneity 0.08; core [0.949, 0.0, 0.135] rim [0.73, 0.0, 0.01]
- damage applied at frame 60: erased 190 px of a 430 px component

## Warnings
- none

## Files
sheet.png, tracks.png, lineage.png, timeseries.png, movie.mp4, metrics.json

Measurements are screens, not verdicts: judge them against the images.
