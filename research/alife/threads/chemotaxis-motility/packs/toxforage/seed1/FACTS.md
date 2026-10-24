# Evidence pack: toxforage (seed 1)

- world: `../../../worlds/toxforage/world.py`, family `chemotaxis`
- parent: toxtrail; mutation: growth limited by a consumed, regrowing nutrient n (metabolism), with chemotaxis up n
- run: 201 frames x 120 steps x dt 0.05 = time 1200; grid [160, 160]; wall 95s; status ok
- command: `python -m labkit.run threads/chemotaxis-motility/worlds/toxforage/world.py --out threads/chemotaxis-motility/packs/toxforage --seeds 0 1 2`
- segmentation: matter > 0.35 of robust range [0.0, 0.9991], min area 6 px

## Measurements
- components: final 14, mean 11.6, max 17; occupancy final 0.10
- tracks: 360; persistent (alive >= 50% of run): 0; longest 49 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 0.00 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [16, 15, 14], H1 [0, 0, 0]
- motion: 34 long-lived tracks moved >= 1 body length; max speed 0.443/time; max body lengths 7.8
- replication: splits 113, persistent splits 1, max generation 1, merges 118, nucleations 35
- channel total drift (end/start - 1): [0.7431, 0.7174, 0.7166, -0.1056]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 285 at frame 176: holes 0, rim-vs-core 0.48, rim-vs-outside 0.65, heterogeneity 0.21; core [0.971, 0.764, 0.686, 0.114] rim [0.641, 0.582, 0.52, 0.352]
  - track 95 at frame 87: holes 0, rim-vs-core 0.46, rim-vs-outside 0.62, heterogeneity 0.20; core [0.964, 0.741, 0.652, 0.126] rim [0.642, 0.575, 0.497, 0.358]
  - track 284 at frame 175: holes 0, rim-vs-core 0.47, rim-vs-outside 0.66, heterogeneity 0.20; core [0.975, 0.733, 0.669, 0.111] rim [0.66, 0.555, 0.491, 0.356]
  - track 295 at frame 178: holes 0, rim-vs-core 0.46, rim-vs-outside 0.64, heterogeneity 0.20; core [0.979, 0.775, 0.674, 0.107] rim [0.656, 0.597, 0.525, 0.333]

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, lineage.png, timeseries.png, movie.mp4, metrics.json

Measurements are screens, not verdicts: judge them against the images.
