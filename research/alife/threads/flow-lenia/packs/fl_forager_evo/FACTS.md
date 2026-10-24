# Evidence pack: fl_forager_evo (seed 1)

- world: `../../worlds/fl_forager_evo/world.py`, family `flow-lenia`
- parent: flow-lenia/fl_forager; mutation: parameter localization (stochastic mixing) + founders that differ in (m,s,h) + rare body-scale mutations: kinds compete for food
- run: 301 frames x 20 steps x dt 0.2 = time 1200; grid [128, 128]; wall 289s; status ok
- command: `python -m labkit.run threads/flow-lenia/worlds/fl_forager_evo/world.py --out threads/flow-lenia/packs/fl_forager_evo --frames 300 --spf 20 --seeds 1`
- segmentation: matter > 0.07 of robust range [0.0, 2.1671], min area 6 px

## Measurements
- components: final 47, mean 22.5, max 47; occupancy final 0.16
- tracks: 1920; persistent (alive >= 50% of run): 0; longest 79 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 0.00 (1 = constant size)
- enclosures: components with a hole mean 1.40, final 2; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [71, 58, 16], H1 [1, 0, 0]
- motion: 16 long-lived tracks moved >= 1 body length; max speed 0.16/time; max body lengths 11.0
- replication: splits 680, persistent splits 0, max generation 0, merges 624, nucleations 46
- channel total drift (end/start - 1): [-0.8595, 3.731, -0.5174]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 1093 at frame 262: holes 0, rim-vs-core 0.27, rim-vs-outside 0.14, heterogeneity 0.08; core [0.0, 0.419, 0.149] rim [0.0, 0.145, 0.169]
  - track 312 at frame 121: holes 0, rim-vs-core 0.16, rim-vs-outside 0.14, heterogeneity 0.09; core [0.0, 0.309, 0.238] rim [0.0, 0.148, 0.271]
  - track 367 at frame 141: holes 0, rim-vs-core 0.30, rim-vs-outside 0.10, heterogeneity 0.09; core [0.0, 0.417, 0.134] rim [0.0, 0.119, 0.146]
  - track 114 at frame 58: holes 0, rim-vs-core 0.49, rim-vs-outside 0.09, heterogeneity 0.13; core [0.0, 0.559, 0.255] rim [0.0, 0.075, 0.328]

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, lineage.png, timeseries.png, movie.mp4, metrics.json

Measurements are screens, not verdicts: judge them against the images.
