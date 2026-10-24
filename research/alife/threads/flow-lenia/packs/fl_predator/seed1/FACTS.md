# Evidence pack: fl_predator (seed 1)

- world: `../../../worlds/fl_predator/world.py`, family `flow-lenia`
- parent: flow-lenia/fl_forager (prey and predator both use glider rule C2_r202); mutation: two glider species with their own rules; predator matter converts prey matter it overlaps (mass-conserving), is drawn up a blurred prey field and decays to food; prey eat food
- run: 301 frames x 40 steps x dt 0.2 = time 2400; grid [128, 128]; wall 263s; status ok
- command: `python -m labkit.run threads/flow-lenia/worlds/fl_predator/world.py --out threads/flow-lenia/packs/fl_predator/seed1 --frames 300 --seeds 1`
- segmentation: matter > 0.07 of robust range [0.0, 2.1988], min area 6 px

## Measurements
- components: final 15, mean 12.5, max 20; occupancy final 0.08
- tracks: 649; persistent (alive >= 50% of run): 0; longest 40 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 0.00 (1 = constant size)
- enclosures: components with a hole mean 0.19, final 0; holes at thresholds 0.2/0.35/0.5 final [1, 2, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [26, 17, 12], H1 [5, 0, 0]
- motion: 6 long-lived tracks moved >= 1 body length; max speed 0.287/time; max body lengths 13.1
- replication: splits 208, persistent splits 0, max generation 0, merges 160, nucleations 86
- channel total drift (end/start - 1): [1.1619, 0.0847, -0.2161]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 138 at frame 93: holes 0, rim-vs-core 0.54, rim-vs-outside 0.05, heterogeneity 0.17; core [0.558, 0.199, 0.23] rim [0.025, 0.142, 0.287]
  - track 318 at frame 189: holes 0, rim-vs-core 0.51, rim-vs-outside 0.05, heterogeneity 0.14; core [0.546, 0.049, 0.105] rim [0.038, 0.046, 0.159]
  - track 224 at frame 134: holes 0, rim-vs-core 0.58, rim-vs-outside 0.07, heterogeneity 0.11; core [0.632, 0.003, 0.146] rim [0.058, 0.003, 0.186]
  - track 230 at frame 139: holes 0, rim-vs-core 0.41, rim-vs-outside 0.20, heterogeneity 0.14; core [0.602, 0.021, 0.206] rim [0.199, 0.018, 0.262]

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, lineage.png, timeseries.png, movie.mp4, metrics.json

Measurements are screens, not verdicts: judge them against the images.
