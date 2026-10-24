# Evidence pack: ad1-fuel (seed 1)

- world: `../../../worlds/ad1-fuel/world.py`, family `phase-field`
- parent: ad0-zwicker; mutation: production needs a diffusing, consumed fuel u and is autocatalytic in phi; decay first order
- run: 201 frames x 200 steps x dt 0.5 = time 20000; grid [128, 128]; wall 138s; status ok
- command: `python -m labkit.run threads/active-droplets/worlds/ad1-fuel/world.py --out threads/active-droplets/packs/ad1-fuel --seeds 0 1 2 --frames 200`
- segmentation: matter > 0.35 of robust range [-1.0491, 1.2761], min area 6 px

## Measurements
- components: final 18, mean 11.7, max 18; occupancy final 0.13
- tracks: 34; persistent (alive >= 50% of run): 10; longest 157 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 1.73 (1 = constant size)
- enclosures: components with a hole mean 0.15, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [18, 18, 18], H1 [0, 0, 0]
- motion: 6 long-lived tracks moved >= 1 body length; max speed 0.00209/time; max body lengths 1.5
- replication: splits 16, persistent splits 16, max generation 4, merges 0, nucleations 0
- channel total drift (end/start - 1): [0.1697, -0.6448]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 10 at frame 123: holes 0, rim-vs-core 0.35, rim-vs-outside 0.49, heterogeneity 0.13; core [0.965, 0.027] rim [0.618, 0.093]
  - track 12 at frame 123: holes 0, rim-vs-core 0.21, rim-vs-outside 0.62, heterogeneity 0.12; core [0.955, 0.031] rim [0.749, 0.068]
  - track 15 at frame 131: holes 0, rim-vs-core 0.37, rim-vs-outside 0.49, heterogeneity 0.13; core [0.962, 0.027] rim [0.602, 0.095]
  - track 26 at frame 176: holes 0, rim-vs-core 0.41, rim-vs-outside 0.29, heterogeneity 0.12; core [0.905, 0.046] rim [0.501, 0.101]

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, lineage.png, timeseries.png, movie.mp4, metrics.json

Measurements are screens, not verdicts: judge them against the images.
