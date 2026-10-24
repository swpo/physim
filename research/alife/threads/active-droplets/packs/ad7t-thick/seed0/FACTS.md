# Evidence pack: ad7t-thick (seed 0)

- world: `../../../worlds/ad7t-thick/world.py`, family `phase-field`
- parent: ad7-gated-d4; mutation: two-sided test: ancestor is the thick-membrane allele 3 (kp=4) instead of allele 0 (kp=0)
- run: 201 frames x 200 steps x dt 0.5 = time 20000; grid [128, 128]; wall 433s; status ok
- command: `python -m labkit.run threads/active-droplets/worlds/ad7t-thick/world.py --out threads/active-droplets/packs/ad7t-thick --seeds 0 1 2 --frames 200 --no-movie`
- segmentation: matter > 0.35 of robust range [-1.0629, 1.469], min area 6 px

## Measurements
- components: final 12, mean 8.8, max 12; occupancy final 0.11
- tracks: 24; persistent (alive >= 50% of run): 6; longest 198 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 12.41 (1 = constant size)
- enclosures: components with a hole mean 0.03, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [13, 12, 12], H1 [0, 0, 0]
- motion: 3 long-lived tracks moved >= 1 body length; max speed 0.00176/time; max body lengths 1.5
- replication: splits 10, persistent splits 7, max generation 4, merges 0, nucleations 0
- channel total drift (end/start - 1): [0.0681, -0.5256, None, None, None, None, -0.8005]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 4 at frame 103: holes 0, rim-vs-core 0.35, rim-vs-outside 0.73, heterogeneity 0.12; core [0.842, 0.082, 0.488, 0.0, 0.0, 0.0, 0.908] rim [0.688, 0.153, 0.71, 0.0, 0.0, 0.0, 0.704]
  - track 6 at frame 103: holes 0, rim-vs-core 0.81, rim-vs-outside 0.58, heterogeneity 0.12; core [0.853, 0.077, 0.432, 0.0, 0.0, 0.0, 0.925] rim [0.508, 0.216, 0.991, 0.0, 0.0, 0.0, 0.472]
  - track 7 at frame 103: holes 0, rim-vs-core 0.50, rim-vs-outside 0.66, heterogeneity 0.07; core [0.969, 0.053, 0.011, 0.967, 0.0, 0.0, 0.016] rim [0.647, 0.163, 0.057, 0.61, 0.0, 0.0, 0.01]
  - track 20 at frame 175: holes 0, rim-vs-core 0.59, rim-vs-outside 0.69, heterogeneity 0.09; core [0.977, 0.1, 0.042, 0.0, 0.926, 0.0, 0.0] rim [0.616, 0.204, 0.233, 0.0, 0.51, 0.0, 0.0]

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, lineage.png, timeseries.png, movie.mp4, metrics.json

Measurements are screens, not verdicts: judge them against the images.
