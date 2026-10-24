# Evidence pack: fl_cells_food (seed 0)

- world: `../../worlds/fl_cells_food/world.py`, family `flow-lenia`
- parent: flow-lenia/fl_food + flow-lenia/fl_cells (rule 0); mutation: food metabolism on the layered-cell rule (C=3 rule 0) with a steep uptake gate (n=4, K=0.6), food0 0.2
- run: 251 frames x 40 steps x dt 0.2 = time 2000; grid [128, 128]; wall 144s; status ok
- command: `python -m labkit.run threads/flow-lenia/worlds/fl_cells_food/world.py --out threads/flow-lenia/packs/fl_cells_food --frames 250`
- segmentation: matter > 0.35 of robust range [0.0, 1.8997], min area 6 px

## Measurements
- components: final 72, mean 26.9, max 77; occupancy final 0.06
- tracks: 445; persistent (alive >= 50% of run): 1; longest 131 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 9.37 (1 = constant size)
- enclosures: components with a hole mean 0.89, final 1; holes at thresholds 0.2/0.35/0.5 final [1, 1, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [90, 84, 72], H1 [1, 1, 0]
- motion: 69 long-lived tracks moved >= 1 body length; max speed 0.091/time; max body lengths 10.4
- replication: splits 67, persistent splits 2, max generation 1, merges 64, nucleations 257
- channel total drift (end/start - 1): [-0.9984, 10.1668, -0.9764, -0.6504]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 221 at frame 206: holes 0, rim-vs-core 0.10, rim-vs-outside 0.18, heterogeneity 0.02; core [0.0, 0.698, 0.0, 0.028] rim [0.0, 0.6, 0.0, 0.045]
  - track 156 at frame 141: holes 0, rim-vs-core 0.22, rim-vs-outside 0.44, heterogeneity 0.07; core [0.004, 0.794, 0.001, 0.002] rim [0.01, 0.609, 0.122, 0.007]

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, lineage.png, timeseries.png, movie.mp4, metrics.json

Measurements are screens, not verdicts: judge them against the images.
