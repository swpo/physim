# Evidence pack: fl_forager (seed 1)

- world: `../../../worlds/fl_forager/world.py`, family `flow-lenia`
- parent: flow-lenia/fl_food (rule from motion search screens/mot/C2_r202); mutation: fl_food applied to a glider-forming 2-channel rule (rule_seed 202, R_scale 0.4) at food0 0.1, Hill uptake
- run: 401 frames x 10 steps x dt 0.2 = time 800; grid [128, 128]; wall 39s; status ok
- command: `python -m labkit.run threads/flow-lenia/worlds/fl_forager/world.py --out threads/flow-lenia/packs/fl_forager --frames 400 --seeds 0 1 2`
- segmentation: matter > 0.07 of robust range [0.0, 2.081], min area 6 px

## Measurements
- components: final 14, mean 7.1, max 15; occupancy final 0.09
- tracks: 129; persistent (alive >= 50% of run): 0; longest 129 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 0.00 (1 = constant size)
- enclosures: components with a hole mean 0.04, final 0; holes at thresholds 0.2/0.35/0.5 final [2, 3, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [28, 19, 14], H1 [6, 4, 0]
- motion: 24 long-lived tracks moved >= 1 body length; max speed 0.728/time; max body lengths 11.5
- replication: splits 48, persistent splits 1, max generation 1, merges 35, nucleations 0
- channel total drift (end/start - 1): [4.2201, 7.9714, -0.5217]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 53 at frame 336: holes 0, rim-vs-core 0.30, rim-vs-outside 0.22, heterogeneity 0.24; core [0.353, 0.35, 0.056] rim [0.096, 0.196, 0.078]
  - track 4 at frame 108: holes 0, rim-vs-core 0.35, rim-vs-outside 0.25, heterogeneity 0.29; core [0.336, 0.364, 0.305] rim [0.063, 0.201, 0.46]
  - track 47 at frame 309: holes 0, rim-vs-core 0.37, rim-vs-outside 0.10, heterogeneity 0.24; core [0.269, 0.371, 0.116] rim [0.082, 0.055, 0.137]
  - track 39 at frame 289: holes 0, rim-vs-core 0.30, rim-vs-outside 0.24, heterogeneity 0.25; core [0.307, 0.34, 0.038] rim [0.026, 0.234, 0.064]

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, lineage.png, timeseries.png, movie.mp4, metrics.json

Measurements are screens, not verdicts: judge them against the images.
