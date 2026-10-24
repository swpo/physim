# Evidence pack: ad1-fuel (seed 2)

- world: `../../../worlds/ad1-fuel/world.py`, family `phase-field`
- parent: ad0-zwicker; mutation: production needs a diffusing, consumed fuel u and is autocatalytic in phi; decay first order
- run: 201 frames x 200 steps x dt 0.5 = time 20000; grid [128, 128]; wall 142s; status ok
- command: `python -m labkit.run threads/active-droplets/worlds/ad1-fuel/world.py --out threads/active-droplets/packs/ad1-fuel --seeds 0 1 2 --frames 200`
- segmentation: matter > 0.35 of robust range [-1.0493, 1.2757], min area 6 px

## Measurements
- components: final 18, mean 12.0, max 18; occupancy final 0.13
- tracks: 34; persistent (alive >= 50% of run): 10; longest 155 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 1.62 (1 = constant size)
- enclosures: components with a hole mean 0.08, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [18, 18, 18], H1 [0, 0, 0]
- motion: 6 long-lived tracks moved >= 1 body length; max speed 0.00272/time; max body lengths 1.2
- replication: splits 16, persistent splits 12, max generation 2, merges 0, nucleations 0
- channel total drift (end/start - 1): [0.1696, -0.6444]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 12 at frame 124: holes 0, rim-vs-core 0.34, rim-vs-outside 0.49, heterogeneity 0.12; core [0.965, 0.028] rim [0.626, 0.09]
  - track 13 at frame 124: holes 0, rim-vs-core 0.34, rim-vs-outside 0.50, heterogeneity 0.12; core [0.966, 0.027] rim [0.632, 0.089]
  - track 14 at frame 131: holes 0, rim-vs-core 0.22, rim-vs-outside 0.62, heterogeneity 0.13; core [0.945, 0.035] rim [0.732, 0.067]
  - track 22 at frame 145: holes 0, rim-vs-core 0.34, rim-vs-outside 0.49, heterogeneity 0.12; core [0.953, 0.024] rim [0.625, 0.095]

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, lineage.png, timeseries.png, movie.mp4, metrics.json

Measurements are screens, not verdicts: judge them against the images.
