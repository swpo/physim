# Evidence pack: fl_food_r0 (seed 0)

- world: `../../worlds/fl_food_r0/world.py`, family `flow-lenia`
- parent: flow-lenia/fl_food; mutation: fl_food with rule_seed 0 and food0 0.3 (screen food_r0)
- run: 201 frames x 10 steps x dt 0.2 = time 400; grid [128, 128]; wall 28s; status ok
- command: `python -m labkit.run threads/flow-lenia/worlds/fl_food_r0/world.py --out threads/flow-lenia/packs/scr_food_r0 --frames 200 --no-movie`
- segmentation: matter > 0.35 of robust range [0.0, 1.8971], min area 6 px

## Measurements
- components: final 20, mean 13.7, max 20; occupancy final 0.03
- tracks: 93; persistent (alive >= 50% of run): 9; longest 163 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 8.70 (1 = constant size)
- enclosures: components with a hole mean 0.40, final 0; holes at thresholds 0.2/0.35/0.5 final [2, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [41, 17, 10], H1 [3, 0, 0]
- motion: 24 long-lived tracks moved >= 1 body length; max speed 0.27/time; max body lengths 9.9
- replication: splits 28, persistent splits 2, max generation 1, merges 21, nucleations 14
- channel total drift (end/start - 1): [6.6103, -0.3455, 4.5007, -0.8491]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 19 at frame 119: holes 1, rim-vs-core 0.06, rim-vs-outside 0.20, heterogeneity 0.09; core [0.025, 0.441, 0.214, 0.112] rim [0.032, 0.386, 0.247, 0.107]
  - track 22 at frame 124: holes 0, rim-vs-core 0.44, rim-vs-outside 0.33, heterogeneity 0.16; core [0.039, 0.836, 0.178, 0.158] rim [0.054, 0.403, 0.222, 0.138]
  - track 27 at frame 124: holes 0, rim-vs-core 0.51, rim-vs-outside 0.31, heterogeneity 0.17; core [0.046, 0.828, 0.122, 0.165] rim [0.056, 0.342, 0.274, 0.147]
  - track 32 at frame 133: holes 0, rim-vs-core 0.50, rim-vs-outside 0.34, heterogeneity 0.14; core [0.051, 0.842, 0.026, 0.134] rim [0.059, 0.417, 0.284, 0.119]

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, lineage.png, timeseries.png, movie.mp4, metrics.json

Measurements are screens, not verdicts: judge them against the images.
