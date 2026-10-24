# Evidence pack: fl_food_r8 (seed 0)

- world: `../../worlds/fl_food_r8/world.py`, family `flow-lenia`
- parent: flow-lenia/fl_food; mutation: fl_food with rule_seed 8, food0 0.3, Hill eating (n=3, K=0.3: only dense bodies eat), k_eat 0.05 (screen foodH3_r8)
- run: 201 frames x 15 steps x dt 0.2 = time 600; grid [128, 128]; wall 43s; status ok
- command: `python -m labkit.run threads/flow-lenia/worlds/fl_food_r8/world.py --out threads/flow-lenia/packs/scr_food_r8 --frames 200 --no-movie`
- segmentation: matter > 0.35 of robust range [0.0, 2.9784], min area 6 px

## Measurements
- components: final 15, mean 26.3, max 41; occupancy final 0.05
- tracks: 1738; persistent (alive >= 50% of run): 0; longest 57 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 0.00 (1 = constant size)
- enclosures: components with a hole mean 0.59, final 2; holes at thresholds 0.2/0.35/0.5 final [9, 4, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [28, 10, 4], H1 [16, 5, 0]
- motion: 27 long-lived tracks moved >= 1 body length; max speed 0.341/time; max body lengths 5.5
- replication: splits 530, persistent splits 0, max generation 0, merges 491, nucleations 281
- channel total drift (end/start - 1): [10.7366, -0.3003, 0.1399, -0.8454]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 368 at frame 77: holes 0, rim-vs-core 0.14, rim-vs-outside 0.17, heterogeneity 0.25; core [0.439, 0.083, 0.235, 0.091] rim [0.466, 0.213, 0.275, 0.091]
  - track 99 at frame 30: holes 0, rim-vs-core 0.66, rim-vs-outside 0.37, heterogeneity 0.13; core [0.182, 1.0, 0.394, 0.086] rim [0.216, 0.368, 0.215, 0.071]
  - track 88 at frame 27: holes 0, rim-vs-core 0.50, rim-vs-outside 0.38, heterogeneity 0.20; core [0.242, 0.756, 0.601, 0.094] rim [0.307, 0.379, 0.274, 0.082]

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, lineage.png, timeseries.png, movie.mp4, metrics.json

Measurements are screens, not verdicts: judge them against the images.
