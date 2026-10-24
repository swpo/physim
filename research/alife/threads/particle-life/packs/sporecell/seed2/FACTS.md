# Evidence pack: sporecell (seed 2)

- world: `../../../worlds/sporecell/world.py`, family `particle`
- parent: eatbud-m2; mutation: promoted settings: membrane induced by food contact (mrule=food), turnover k_dec=0.01
- run: 241 frames x 50 steps x dt 0.02 = time 240; grid [128, 128]; wall 248s; status ok
- command: `python -m labkit.run threads/particle-life/worlds/sporecell/world.py --out threads/particle-life/packs/sporecell --seeds 0 1 2 --frames 240`
- segmentation: matter > 0.35 of robust range [0.0, 2.6691], min area 6 px

## Measurements
- components: final 41, mean 19.7, max 42; occupancy final 0.08
- tracks: 157; persistent (alive >= 50% of run): 4; longest 156 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 8.67 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [42, 42, 38], H1 [0, 0, 0]
- motion: 19 long-lived tracks moved >= 1 body length; max speed 0.245/time; max body lengths 4.1
- replication: splits 0, persistent splits 0, max generation 0, merges 0, nucleations 157
- channel total drift (end/start - 1): [-0.8875, 141.08, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 6 at frame 163: holes 0, rim-vs-core 0.36, rim-vs-outside 0.22, heterogeneity 0.07; core [0.0, 0.916, 0.0] rim [0.003, 0.552, 0.0]
  - track 3 at frame 157: holes 0, rim-vs-core 0.33, rim-vs-outside 0.21, heterogeneity 0.06; core [0.0, 0.867, 0.0] rim [0.0, 0.541, 0.0]
  - track 14 at frame 177: holes 0, rim-vs-core 0.35, rim-vs-outside 0.23, heterogeneity 0.07; core [0.003, 0.898, 0.0] rim [0.012, 0.551, 0.0]
  - track 2 at frame 135: holes 0, rim-vs-core 0.28, rim-vs-outside 0.21, heterogeneity 0.10; core [0.002, 0.8, 0.251] rim [0.01, 0.527, 0.188]

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, lineage.png, timeseries.png, particles.png, movie.mp4, metrics.json

Measurements are screens, not verdicts: judge them against the images.
