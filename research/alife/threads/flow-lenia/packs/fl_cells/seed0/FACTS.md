# Evidence pack: fl_cells (seed 0)

- world: `../../../worlds/fl_cells/world.py`, family `flow-lenia`
- parent: flow-lenia/fl_base; mutation: 3-channel random rule 0 at R_scale 0.4 from 6 noise patches: layered cells (screen pop_r0)
- run: 201 frames x 10 steps x dt 0.2 = time 400; grid [128, 128]; wall 28s; status ok
- command: `python -m labkit.run threads/flow-lenia/worlds/fl_cells/world.py --out threads/flow-lenia/packs/fl_cells --frames 200 --seeds 0 1 2`
- segmentation: matter > 0.35 of robust range [0.0, 2.0016], min area 6 px

## Measurements
- components: final 7, mean 6.6, max 11; occupancy final 0.09
- tracks: 32; persistent (alive >= 50% of run): 5; longest 199 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 1.15 (1 = constant size)
- enclosures: components with a hole mean 2.08, final 2; holes at thresholds 0.2/0.35/0.5 final [12, 8, 1]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [16, 7, 4], H1 [13, 9, 1]
- motion: 0 long-lived tracks moved >= 1 body length; max speed 0/time; max body lengths 0.4
- replication: splits 9, persistent splits 2, max generation 2, merges 8, nucleations 0
- channel total drift (end/start - 1): [0.0, 0.0, 0.0]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 10 at frame 101: holes 0, rim-vs-core 0.29, rim-vs-outside 0.45, heterogeneity 0.07; core [0.996, 0.0, 0.125] rim [0.723, 0.0, 0.03]
  - track 16 at frame 101: holes 0, rim-vs-core 0.24, rim-vs-outside 0.45, heterogeneity 0.09; core [0.926, 0.0, 0.133] rim [0.716, 0.0, 0.01]
  - track 30 at frame 178: holes 0, rim-vs-core 0.47, rim-vs-outside 0.42, heterogeneity 0.20; core [0.004, 0.889, 0.016] rim [0.005, 0.467, 0.216]

## Warnings
- none

## Files
sheet.png, tracks.png, lineage.png, timeseries.png, movie.mp4, metrics.json

Measurements are screens, not verdicts: judge them against the images.
