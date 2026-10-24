# Evidence pack: fl_forager (seed 0)

- world: `../../worlds/fl_forager/world.py`, family `flow-lenia`
- parent: flow-lenia/fl_food (rule from motion search screens/mot/C2_r202); mutation: fl_food applied to a glider-forming 2-channel rule (rule_seed 202, R_scale 0.4) at food0 0.1, Hill uptake
- run: 401 frames x 10 steps x dt 0.2 = time 800; grid [128, 128]; wall 48s; status ok
- command: `python -m labkit.run threads/flow-lenia/worlds/fl_forager/world.py --out threads/flow-lenia/packs/scr_forager --frames 400`
- segmentation: matter > 0.07 of robust range [0.0, 2.1218], min area 6 px

## Measurements
- components: final 11, mean 7.8, max 15; occupancy final 0.09
- tracks: 139; persistent (alive >= 50% of run): 0; longest 147 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 0.00 (1 = constant size)
- enclosures: components with a hole mean 0.09, final 0; holes at thresholds 0.2/0.35/0.5 final [2, 1, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [29, 18, 11], H1 [8, 2, 0]
- motion: 25 long-lived tracks moved >= 1 body length; max speed 0.691/time; max body lengths 10.0
- replication: splits 49, persistent splits 2, max generation 2, merges 40, nucleations 0
- channel total drift (end/start - 1): [3.9682, 7.0193, -0.5266]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 2 at frame 81: holes 0, rim-vs-core 0.31, rim-vs-outside 0.28, heterogeneity 0.30; core [0.381, 0.354, 0.325] rim [0.209, 0.132, 0.458]
  - track 81 at frame 339: holes 0, rim-vs-core 0.49, rim-vs-outside 0.04, heterogeneity 0.23; core [0.286, 0.441, 0.084] rim [0.042, 0.013, 0.079]
  - track 19 at frame 178: holes 0, rim-vs-core 0.44, rim-vs-outside 0.06, heterogeneity 0.24; core [0.281, 0.395, 0.142] rim [0.055, 0.023, 0.185]
  - track 89 at frame 336: holes 0, rim-vs-core 0.41, rim-vs-outside 0.05, heterogeneity 0.23; core [0.254, 0.385, 0.071] rim [0.044, 0.029, 0.075]

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, lineage.png, timeseries.png, movie.mp4, metrics.json

Measurements are screens, not verdicts: judge them against the images.
