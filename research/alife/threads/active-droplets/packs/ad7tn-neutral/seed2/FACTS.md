# Evidence pack: ad7tn-neutral (seed 2)

- world: `../../../worlds/ad7tn-neutral/world.py`, family `phase-field`
- parent: ad7t-thick; mutation: neutral control for ad7t: all four alleles kp=4 (same mutation, dilution, ancestor phenotype)
- run: 201 frames x 200 steps x dt 0.5 = time 20000; grid [128, 128]; wall 418s; status ok
- command: `python -m labkit.run threads/active-droplets/worlds/ad7tn-neutral/world.py --out threads/active-droplets/packs/ad7tn-neutral --seeds 0 1 2 --frames 200 --no-movie`
- segmentation: matter > 0.35 of robust range [-1.041, 1.2223], min area 6 px

## Measurements
- components: final 7, mean 6.0, max 7; occupancy final 0.05
- tracks: 10; persistent (alive >= 50% of run): 6; longest 201 frames; alive start-to-end: 3
- size of persistent tracks: max/min area ratio 2.98 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [8, 7, 7], H1 [0, 0, 0]
- motion: 1 long-lived tracks moved >= 1 body length; max speed 0.000867/time; max body lengths 1.0
- replication: splits 2, persistent splits 2, max generation 1, merges 0, nucleations 0
- channel total drift (end/start - 1): [-0.0704, -0.2279, None, None, None, None, -0.8678]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 0 at frame 101: holes 0, rim-vs-core 0.85, rim-vs-outside 0.95, heterogeneity 0.14; core [0.975, 0.014, 0.202, 1.0, 0.0, 0.0, 0.0] rim [0.608, 0.287, 0.807, 0.625, 0.0, 0.0, 0.0]
  - track 3 at frame 101: holes 0, rim-vs-core 0.82, rim-vs-outside 0.96, heterogeneity 0.14; core [0.971, 0.015, 0.204, 0.0, 0.0, 0.0, 1.0] rim [0.616, 0.28, 0.809, 0.0, 0.0, 0.0, 0.668]
  - track 5 at frame 101: holes 0, rim-vs-core 0.86, rim-vs-outside 0.94, heterogeneity 0.17; core [0.971, 0.021, 0.206, 0.0, 0.954, 0.323, 0.0] rim [0.608, 0.286, 0.819, 0.0, 0.589, 0.177, 0.0]
  - track 6 at frame 138: holes 0, rim-vs-core 0.95, rim-vs-outside 0.62, heterogeneity 0.18; core [0.915, 0.069, 0.353, 0.549, 0.693, 0.0, 0.0] rim [0.478, 0.374, 0.944, 0.218, 0.29, 0.0, 0.0]

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, lineage.png, timeseries.png, movie.mp4, metrics.json

Measurements are screens, not verdicts: judge them against the images.
