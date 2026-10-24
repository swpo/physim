# Evidence pack: sporecell (seed 0)

- world: `../../../worlds/sporecell/world.py`, family `particle`
- parent: eatbud-m2; mutation: promoted settings: membrane induced by food contact (mrule=food), turnover k_dec=0.01
- run: 241 frames x 50 steps x dt 0.02 = time 240; grid [128, 128]; wall 208s; status ok
- command: `python -m labkit.run threads/particle-life/worlds/sporecell/world.py --out threads/particle-life/packs/sporecell --seeds 0 1 2 --frames 240`
- segmentation: matter > 0.35 of robust range [0.0, 2.5878], min area 6 px

## Measurements
- components: final 39, mean 15.6, max 40; occupancy final 0.08
- tracks: 99; persistent (alive >= 50% of run): 3; longest 182 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 8.00 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [40, 40, 38], H1 [0, 0, 0]
- motion: 21 long-lived tracks moved >= 1 body length; max speed 0.476/time; max body lengths 4.1
- replication: splits 0, persistent splits 0, max generation 0, merges 0, nucleations 99
- channel total drift (end/start - 1): [-0.8918, 236.9333, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 0 at frame 151: holes 0, rim-vs-core 0.26, rim-vs-outside 0.37, heterogeneity 0.11; core [0.006, 0.932, 0.087] rim [0.025, 0.673, 0.133]
  - track 3 at frame 177: holes 0, rim-vs-core 0.28, rim-vs-outside 0.30, heterogeneity 0.06; core [0.004, 0.918, 0.0] rim [0.011, 0.639, 0.0]
  - track 1 at frame 155: holes 0, rim-vs-core 0.39, rim-vs-outside 0.23, heterogeneity 0.11; core [0.005, 0.891, 0.325] rim [0.029, 0.545, 0.149]
  - track 4 at frame 182: holes 0, rim-vs-core 0.33, rim-vs-outside 0.27, heterogeneity 0.07; core [0.003, 0.941, 0.0] rim [0.01, 0.614, 0.0]

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, lineage.png, timeseries.png, particles.png, movie.mp4, metrics.json

Measurements are screens, not verdicts: judge them against the images.
