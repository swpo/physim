# Evidence pack: ad5n-neutral (seed 1)

- world: `../../../worlds/ad5n-neutral/world.py`, family `phase-field`
- parent: ad5-evolve; mutation: neutral control: all four alleles have the same catalytic rate k=0.13
- run: 201 frames x 200 steps x dt 0.5 = time 20000; grid [128, 128]; wall 265s; status ok
- command: `python -m labkit.run threads/active-droplets/worlds/ad5n-neutral/world.py --out threads/active-droplets/packs/ad5n-neutral --seeds 0 1 2 --frames 200`
- segmentation: matter > 0.35 of robust range [-1.0646, 1.4296], min area 6 px

## Measurements
- components: final 10, mean 8.7, max 11; occupancy final 0.12
- tracks: 19; persistent (alive >= 50% of run): 6; longest 193 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 2.88 (1 = constant size)
- enclosures: components with a hole mean 0.03, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [10, 10, 10], H1 [0, 0, 0]
- motion: 2 long-lived tracks moved >= 1 body length; max speed 0.00256/time; max body lengths 1.3
- replication: splits 7, persistent splits 6, max generation 2, merges 0, nucleations 0
- channel total drift (end/start - 1): [0.0937, -0.5728, 1.2214, None, None, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 6 at frame 104: holes 0, rim-vs-core 0.50, rim-vs-outside 0.56, heterogeneity 0.09; core [0.957, 0.056, 0.546, 0.021, 0.446, 0.0] rim [0.591, 0.147, 0.29, 0.012, 0.243, 0.0]
  - track 7 at frame 118: holes 0, rim-vs-core 0.52, rim-vs-outside 0.63, heterogeneity 0.11; core [0.954, 0.041, 0.809, 0.434, 0.0, 0.0] rim [0.624, 0.138, 0.453, 0.261, 0.0, 0.0]
  - track 8 at frame 118: holes 0, rim-vs-core 0.52, rim-vs-outside 0.65, heterogeneity 0.11; core [0.948, 0.043, 0.772, 0.555, 0.0, 0.0] rim [0.628, 0.135, 0.44, 0.335, 0.0, 0.0]
  - track 15 at frame 155: holes 0, rim-vs-core 0.40, rim-vs-outside 0.78, heterogeneity 0.08; core [0.964, 0.047, 0.93, 0.0, 0.0, 0.0] rim [0.713, 0.11, 0.628, 0.0, 0.0, 0.0]

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, lineage.png, timeseries.png, movie.mp4, metrics.json

Measurements are screens, not verdicts: judge them against the images.
