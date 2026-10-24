# Evidence pack: ad7t-thick (seed 2)

- world: `../../../worlds/ad7t-thick/world.py`, family `phase-field`
- parent: ad7-gated-d4; mutation: two-sided test: ancestor is the thick-membrane allele 3 (kp=4) instead of allele 0 (kp=0)
- run: 201 frames x 200 steps x dt 0.5 = time 20000; grid [128, 128]; wall 406s; status ok
- command: `python -m labkit.run threads/active-droplets/worlds/ad7t-thick/world.py --out threads/active-droplets/packs/ad7t-thick --seeds 0 1 2 --frames 200 --no-movie`
- segmentation: matter > 0.35 of robust range [-1.0615, 1.4413], min area 6 px

## Measurements
- components: final 13, mean 9.3, max 13; occupancy final 0.10
- tracks: 28; persistent (alive >= 50% of run): 6; longest 201 frames; alive start-to-end: 2
- size of persistent tracks: max/min area ratio 7.71 (1 = constant size)
- enclosures: components with a hole mean 0.07, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [13, 13, 13], H1 [0, 0, 0]
- motion: 3 long-lived tracks moved >= 1 body length; max speed 0.00223/time; max body lengths 1.5
- replication: splits 11, persistent splits 9, max generation 3, merges 0, nucleations 0
- channel total drift (end/start - 1): [0.0492, -0.4871, None, None, None, None, -0.5463]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 3 at frame 101: holes 0, rim-vs-core 0.87, rim-vs-outside 0.53, heterogeneity 0.13; core [0.875, 0.058, 0.39, 0.0, 0.0, 0.0, 0.907] rim [0.518, 0.299, 0.983, 0.0, 0.0, 0.0, 0.437]
  - track 5 at frame 101: holes 0, rim-vs-core 0.88, rim-vs-outside 0.53, heterogeneity 0.13; core [0.882, 0.056, 0.375, 0.0, 0.0, 0.0, 0.913] rim [0.526, 0.283, 0.99, 0.0, 0.0, 0.0, 0.443]
  - track 0 at frame 84: holes 0, rim-vs-core 0.89, rim-vs-outside 0.53, heterogeneity 0.13; core [0.875, 0.059, 0.396, 0.0, 0.0, 0.0, 0.907] rim [0.505, 0.313, 0.996, 0.0, 0.0, 0.0, 0.421]
  - track 18 at frame 170: holes 0, rim-vs-core 0.39, rim-vs-outside 0.70, heterogeneity 0.07; core [0.979, 0.125, 0.001, 0.898, 0.0, 0.002, 0.0] rim [0.726, 0.196, 0.008, 0.609, 0.0, 0.002, 0.0]

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, lineage.png, timeseries.png, movie.mp4, metrics.json

Measurements are screens, not verdicts: judge them against the images.
