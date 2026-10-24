# Evidence pack: ad1-fuel (seed 0)

- world: `../../worlds/ad1-fuel/world.py`, family `phase-field`
- parent: ad0-zwicker; mutation: production needs a diffusing, consumed fuel u and is autocatalytic in phi; decay first order
- run: 201 frames x 200 steps x dt 0.5 = time 20000; grid [128, 128]; wall 139s; status ok
- command: `python -m labkit.run threads/active-droplets/worlds/ad1-fuel/world.py --out threads/active-droplets/packs/ad1-fuel-damage --seeds 0 --frames 200 --damage 60:0.5`
- segmentation: matter > 0.35 of robust range [-1.0489, 1.2755], min area 6 px

## Measurements
- components: final 19, mean 13.0, max 19; occupancy final 0.13
- tracks: 36; persistent (alive >= 50% of run): 9; longest 156 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 1.44 (1 = constant size)
- enclosures: components with a hole mean 0.17, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [19, 19, 19], H1 [0, 0, 0]
- motion: 4 long-lived tracks moved >= 1 body length; max speed 0.00314/time; max body lengths 1.1
- replication: splits 17, persistent splits 13, max generation 2, merges 0, nucleations 0
- channel total drift (end/start - 1): [0.173, -0.6507]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 12 at frame 123: holes 0, rim-vs-core 0.27, rim-vs-outside 0.58, heterogeneity 0.12; core [0.967, 0.023] rim [0.703, 0.074]
  - track 13 at frame 123: holes 0, rim-vs-core 0.21, rim-vs-outside 0.62, heterogeneity 0.12; core [0.945, 0.037] rim [0.742, 0.063]
  - track 14 at frame 124: holes 0, rim-vs-core 0.34, rim-vs-outside 0.50, heterogeneity 0.12; core [0.962, 0.026] rim [0.632, 0.086]
  - track 22 at frame 150: holes 0, rim-vs-core 0.33, rim-vs-outside 0.50, heterogeneity 0.12; core [0.962, 0.025] rim [0.634, 0.086]
- damage applied at frame 60: erased 82 px of a 277 px component

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, lineage.png, timeseries.png, movie.mp4, metrics.json

Measurements are screens, not verdicts: judge them against the images.
