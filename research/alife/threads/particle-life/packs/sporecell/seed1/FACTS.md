# Evidence pack: sporecell (seed 1)

- world: `../../../worlds/sporecell/world.py`, family `particle`
- parent: eatbud-m2; mutation: promoted settings: membrane induced by food contact (mrule=food), turnover k_dec=0.01
- run: 241 frames x 50 steps x dt 0.02 = time 240; grid [128, 128]; wall 234s; status ok
- command: `python -m labkit.run threads/particle-life/worlds/sporecell/world.py --out threads/particle-life/packs/sporecell --seeds 0 1 2 --frames 240`
- segmentation: matter > 0.35 of robust range [0.0, 2.7064], min area 6 px

## Measurements
- components: final 38, mean 20.8, max 39; occupancy final 0.07
- tracks: 132; persistent (alive >= 50% of run): 5; longest 198 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 8.33 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [39, 39, 31], H1 [0, 0, 0]
- motion: 16 long-lived tracks moved >= 1 body length; max speed 0.488/time; max body lengths 4.2
- replication: splits 2, persistent splits 0, max generation 0, merges 2, nucleations 126
- channel total drift (end/start - 1): [-0.8882, 176.65, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 0 at frame 143: holes 0, rim-vs-core 0.24, rim-vs-outside 0.19, heterogeneity 0.05; core [0.007, 0.823, 0.0] rim [0.02, 0.585, 0.0]
  - track 1 at frame 149: holes 0, rim-vs-core 0.39, rim-vs-outside 0.32, heterogeneity 0.07; core [0.0, 0.986, 0.0] rim [0.001, 0.6, 0.0]
  - track 10 at frame 173: holes 0, rim-vs-core 0.29, rim-vs-outside 0.25, heterogeneity 0.06; core [0.001, 0.885, 0.0] rim [0.005, 0.595, 0.0]
  - track 22 at frame 177: holes 0, rim-vs-core 0.32, rim-vs-outside 0.25, heterogeneity 0.06; core [0.001, 0.924, 0.0] rim [0.005, 0.607, 0.0]

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, lineage.png, timeseries.png, particles.png, movie.mp4, metrics.json

Measurements are screens, not verdicts: judge them against the images.
