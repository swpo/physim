# Evidence pack: ad7t-thick (seed 1)

- world: `../../../worlds/ad7t-thick/world.py`, family `phase-field`
- parent: ad7-gated-d4; mutation: two-sided test: ancestor is the thick-membrane allele 3 (kp=4) instead of allele 0 (kp=0)
- run: 201 frames x 200 steps x dt 0.5 = time 20000; grid [128, 128]; wall 451s; status ok
- command: `python -m labkit.run threads/active-droplets/worlds/ad7t-thick/world.py --out threads/active-droplets/packs/ad7t-thick --seeds 0 1 2 --frames 200 --no-movie`
- segmentation: matter > 0.35 of robust range [-1.0607, 1.4312], min area 6 px

## Measurements
- components: final 11, mean 8.9, max 12; occupancy final 0.12
- tracks: 21; persistent (alive >= 50% of run): 4; longest 201 frames; alive start-to-end: 2
- size of persistent tracks: max/min area ratio 7.37 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [13, 11, 11], H1 [0, 0, 0]
- motion: 5 long-lived tracks moved >= 1 body length; max speed 0.00295/time; max body lengths 1.8
- replication: splits 8, persistent splits 6, max generation 2, merges 0, nucleations 0
- channel total drift (end/start - 1): [0.0798, -0.5424, None, None, None, None, -0.9402]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 3 at frame 101: holes 0, rim-vs-core 0.71, rim-vs-outside 0.80, heterogeneity 0.11; core [0.946, 0.02, 0.142, 0.0, 0.0, 0.989, 0.005] rim [0.64, 0.159, 0.626, 0.0, 0.0, 0.586, 0.003]
  - track 4 at frame 101: holes 0, rim-vs-core 0.48, rim-vs-outside 0.71, heterogeneity 0.12; core [0.879, 0.06, 0.492, 0.0, 0.0, 0.0, 0.981] rim [0.656, 0.199, 0.809, 0.0, 0.0, 0.0, 0.726]
  - track 2 at frame 92: holes 0, rim-vs-core 0.50, rim-vs-outside 0.61, heterogeneity 0.07; core [0.971, 0.078, 0.005, 0.984, 0.0, 0.016, 0.0] rim [0.624, 0.19, 0.025, 0.641, 0.0, 0.009, 0.0]
  - track 15 at frame 153: holes 0, rim-vs-core 0.53, rim-vs-outside 0.71, heterogeneity 0.08; core [0.961, 0.033, 0.051, 0.0, 0.963, 0.0, 0.0] rim [0.64, 0.128, 0.218, 0.0, 0.585, 0.0, 0.0]

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, lineage.png, timeseries.png, movie.mp4, metrics.json

Measurements are screens, not verdicts: judge them against the images.
