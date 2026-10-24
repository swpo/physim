# Evidence pack: fl_predator (seed 0)

- world: `../../../worlds/fl_predator/world.py`, family `flow-lenia`
- parent: flow-lenia/fl_forager (prey and predator both use glider rule C2_r202); mutation: two glider species with their own rules; predator matter converts prey matter it overlaps (mass-conserving), is drawn up a blurred prey field and decays to food; prey eat food
- run: 301 frames x 40 steps x dt 0.2 = time 2400; grid [128, 128]; wall 256s; status ok
- command: `python -m labkit.run threads/flow-lenia/worlds/fl_predator/world.py --out threads/flow-lenia/packs/fl_predator/seed0 --frames 300 --seeds 0`
- segmentation: matter > 0.07 of robust range [0.0, 2.1354], min area 6 px

## Measurements
- components: final 10, mean 10.5, max 20; occupancy final 0.08
- tracks: 586; persistent (alive >= 50% of run): 0; longest 44 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 0.00 (1 = constant size)
- enclosures: components with a hole mean 0.20, final 0; holes at thresholds 0.2/0.35/0.5 final [2, 4, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [17, 10, 8], H1 [5, 2, 0]
- motion: 5 long-lived tracks moved >= 1 body length; max speed 0.438/time; max body lengths 11.3
- replication: splits 171, persistent splits 0, max generation 0, merges 150, nucleations 103
- channel total drift (end/start - 1): [0.7871, -0.1831, -0.1134]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 395 at frame 136: holes 0, rim-vs-core 0.55, rim-vs-outside 0.04, heterogeneity 0.15; core [0.583, 0.059, 0.094] rim [0.032, 0.051, 0.15]
  - track 355 at frame 118: holes 0, rim-vs-core 0.49, rim-vs-outside 0.07, heterogeneity 0.15; core [0.552, 0.026, 0.151] rim [0.064, 0.023, 0.218]
  - track 496 at frame 222: holes 0, rim-vs-core 0.35, rim-vs-outside 0.26, heterogeneity 0.14; core [0.592, 0.004, 0.135] rim [0.248, 0.002, 0.216]
  - track 497 at frame 222: holes 0, rim-vs-core 0.31, rim-vs-outside 0.24, heterogeneity 0.17; core [0.538, 0.107, 0.154] rim [0.231, 0.081, 0.207]

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, lineage.png, timeseries.png, movie.mp4, metrics.json

Measurements are screens, not verdicts: judge them against the images.
