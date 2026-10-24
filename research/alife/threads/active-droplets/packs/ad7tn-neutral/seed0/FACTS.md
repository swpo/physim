# Evidence pack: ad7tn-neutral (seed 0)

- world: `../../../worlds/ad7tn-neutral/world.py`, family `phase-field`
- parent: ad7t-thick; mutation: neutral control for ad7t: all four alleles kp=4 (same mutation, dilution, ancestor phenotype)
- run: 201 frames x 200 steps x dt 0.5 = time 20000; grid [128, 128]; wall 445s; status ok
- command: `python -m labkit.run threads/active-droplets/worlds/ad7tn-neutral/world.py --out threads/active-droplets/packs/ad7tn-neutral --seeds 0 1 2 --frames 200 --no-movie`
- segmentation: matter > 0.35 of robust range [-1.0398, 1.2367], min area 6 px

## Measurements
- components: final 6, mean 6.3, max 8; occupancy final 0.04
- tracks: 14; persistent (alive >= 50% of run): 5; longest 198 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 1.80 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [6, 6, 6], H1 [0, 0, 0]
- motion: 2 long-lived tracks moved >= 1 body length; max speed 0.00092/time; max body lengths 1.2
- replication: splits 5, persistent splits 3, max generation 1, merges 0, nucleations 0
- channel total drift (end/start - 1): [-0.085, -0.185, None, None, None, None, -0.7564]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 4 at frame 103: holes 0, rim-vs-core 0.47, rim-vs-outside 0.82, heterogeneity 0.14; core [0.909, 0.064, 0.356, 0.0, 0.0, 0.934, 0.133] rim [0.685, 0.209, 0.637, 0.0, 0.0, 0.668, 0.097]
  - track 7 at frame 103: holes 0, rim-vs-core 0.92, rim-vs-outside 0.64, heterogeneity 0.14; core [0.906, 0.06, 0.363, 0.957, 0.0, 0.0, 0.001] rim [0.468, 0.355, 0.926, 0.458, 0.0, 0.0, 0.001]
  - track 8 at frame 136: holes 0, rim-vs-core 0.76, rim-vs-outside 0.78, heterogeneity 0.11; core [0.908, 0.059, 0.362, 0.0, 1.0, 0.0, 0.0] rim [0.487, 0.346, 0.927, 0.0, 0.93, 0.0, 0.0]
  - track 9 at frame 136: holes 0, rim-vs-core 0.90, rim-vs-outside 0.61, heterogeneity 0.13; core [0.918, 0.052, 0.341, 0.0, 0.0, 0.0, 0.922] rim [0.516, 0.315, 0.928, 0.0, 0.0, 0.0, 0.433]

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, lineage.png, timeseries.png, movie.mp4, metrics.json

Measurements are screens, not verdicts: judge them against the images.
