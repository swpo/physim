# Evidence pack: fl_forager (seed 2)

- world: `../../../worlds/fl_forager/world.py`, family `flow-lenia`
- parent: flow-lenia/fl_food (rule from motion search screens/mot/C2_r202); mutation: fl_food applied to a glider-forming 2-channel rule (rule_seed 202, R_scale 0.4) at food0 0.1, Hill uptake
- run: 401 frames x 10 steps x dt 0.2 = time 800; grid [128, 128]; wall 41s; status ok
- command: `python -m labkit.run threads/flow-lenia/worlds/fl_forager/world.py --out threads/flow-lenia/packs/fl_forager --frames 400 --seeds 0 1 2`
- segmentation: matter > 0.08 of robust range [0.0, 1.981], min area 6 px

## Measurements
- components: final 10, mean 5.0, max 10; occupancy final 0.09
- tracks: 109; persistent (alive >= 50% of run): 0; longest 118 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 0.00 (1 = constant size)
- enclosures: components with a hole mean 0.13, final 0; holes at thresholds 0.2/0.35/0.5 final [2, 2, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [22, 14, 10], H1 [12, 4, 0]
- motion: 13 long-lived tracks moved >= 1 body length; max speed 0.605/time; max body lengths 7.1
- replication: splits 40, persistent splits 1, max generation 1, merges 29, nucleations 0
- channel total drift (end/start - 1): [3.8935, 7.6874, -0.491]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 51 at frame 319: holes 0, rim-vs-core 0.30, rim-vs-outside 0.25, heterogeneity 0.27; core [0.304, 0.405, 0.208] rim [0.124, 0.187, 0.312]
  - track 2 at frame 61: holes 0, rim-vs-core 0.34, rim-vs-outside 0.28, heterogeneity 0.29; core [0.362, 0.367, 0.277] rim [0.093, 0.238, 0.443]
  - track 55 at frame 309: holes 0, rim-vs-core 0.28, rim-vs-outside 0.30, heterogeneity 0.25; core [0.303, 0.309, 0.019] rim [0.027, 0.298, 0.066]
  - track 62 at frame 343: holes 0, rim-vs-core 0.46, rim-vs-outside 0.05, heterogeneity 0.25; core [0.305, 0.408, 0.096] rim [0.029, 0.037, 0.119]

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, lineage.png, timeseries.png, movie.mp4, metrics.json

Measurements are screens, not verdicts: judge them against the images.
