# Evidence pack: fl_forager_mut (seed 0)

- world: `../../worlds/fl_forager_mut/world.py`, family `flow-lenia`
- parent: flow-lenia/fl_forager_evo; mutation: one founder; rare body-scale mutations of (m,s,h) create new genotypes (ids + parent table carried with matter)
- run: 401 frames x 20 steps x dt 0.2 = time 1600; grid [128, 128]; wall 353s; status ok
- command: `python -m labkit.run threads/flow-lenia/worlds/fl_forager_mut/world.py --out threads/flow-lenia/packs/fl_forager_mut --frames 400 --spf 20`
- segmentation: matter > 0.07 of robust range [0.0, 2.0809], min area 6 px

## Measurements
- components: final 16, mean 11.4, max 19; occupancy final 0.14
- tracks: 510; persistent (alive >= 50% of run): 0; longest 81 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 0.00 (1 = constant size)
- enclosures: components with a hole mean 0.72, final 1; holes at thresholds 0.2/0.35/0.5 final [5, 1, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [33, 21, 16], H1 [8, 4, 0]
- motion: 13 long-lived tracks moved >= 1 body length; max speed 0.471/time; max body lengths 11.6
- replication: splits 177, persistent splits 0, max generation 0, merges 169, nucleations 0
- channel total drift (end/start - 1): [1.544, None, None, -0.5909]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 91 at frame 175: holes 0, rim-vs-core 0.07, rim-vs-outside 0.34, heterogeneity 0.06; core [0.411, 0.0, 0.0, 0.0] rim [0.339, 0.0, 0.0, 0.004]
  - track 64 at frame 124: holes 0, rim-vs-core 0.79, rim-vs-outside 0.19, heterogeneity 0.12; core [0.0, 0.976, 0.0, 0.219] rim [0.0, 0.187, 0.0, 0.248]
  - track 395 at frame 370: holes 3, rim-vs-core 0.10, rim-vs-outside 0.28, heterogeneity 0.13; core [0.317, 0.124, 0.0, 0.005] rim [0.273, 0.031, 0.018, 0.013]
  - track 144 at frame 218: holes 0, rim-vs-core 0.61, rim-vs-outside 0.06, heterogeneity 0.10; core [0.674, 0.0, 0.0, 0.168] rim [0.062, 0.0, 0.0, 0.144]

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, lineage.png, timeseries.png, movie.mp4, metrics.json

Measurements are screens, not verdicts: judge them against the images.
