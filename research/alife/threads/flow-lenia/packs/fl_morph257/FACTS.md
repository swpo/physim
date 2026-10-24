# Evidence pack: fl_morph257 (seed 0)

- world: `../../worlds/fl_morph257/world.py`, family `flow-lenia`
- parent: flow-lenia/fl_forager; mutation: rule_seed 257 (two coexisting morphs: orange rings, cyan crescents) in the forager food world; 20x20 patch
- run: 301 frames x 20 steps x dt 0.2 = time 1200; grid [128, 128]; wall 73s; status ok
- command: `python -m labkit.run threads/flow-lenia/worlds/fl_morph257/world.py --out threads/flow-lenia/packs/fl_morph257 --frames 300 --spf 20`
- segmentation: matter > 0.08 of robust range [0.0, 1.8706], min area 6 px

## Measurements
- components: final 13, mean 11.2, max 17; occupancy final 0.16
- tracks: 462; persistent (alive >= 50% of run): 1; longest 163 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 1.20 (1 = constant size)
- enclosures: components with a hole mean 0.71, final 2; holes at thresholds 0.2/0.35/0.5 final [19, 2, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [42, 15, 11], H1 [22, 7, 0]
- motion: 17 long-lived tracks moved >= 1 body length; max speed 0.316/time; max body lengths 6.7
- replication: splits 161, persistent splits 2, max generation 1, merges 154, nucleations 0
- channel total drift (end/start - 1): [3.8941, 0.6719, -0.5872]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 206 at frame 204: holes 0, rim-vs-core 0.16, rim-vs-outside 0.27, heterogeneity 0.12; core [0.43, 0.0, 0.041] rim [0.265, 0.0, 0.04]
  - track 237 at frame 207: holes 0, rim-vs-core 0.04, rim-vs-outside 0.36, heterogeneity 0.14; core [0.0, 0.406, 0.089] rim [0.0, 0.361, 0.087]
  - track 302 at frame 239: holes 0, rim-vs-core 0.13, rim-vs-outside 0.31, heterogeneity 0.12; core [0.439, 0.0, 0.063] rim [0.31, 0.0, 0.07]
  - track 305 at frame 242: holes 0, rim-vs-core 0.10, rim-vs-outside 0.31, heterogeneity 0.12; core [0.413, 0.0, 0.059] rim [0.311, 0.0, 0.069]

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, lineage.png, timeseries.png, movie.mp4, metrics.json

Measurements are screens, not verdicts: judge them against the images.
