# Evidence pack: ad5n-neutral (seed 2)

- world: `../../../worlds/ad5n-neutral/world.py`, family `phase-field`
- parent: ad5-evolve; mutation: neutral control: all four alleles have the same catalytic rate k=0.13
- run: 201 frames x 200 steps x dt 0.5 = time 20000; grid [128, 128]; wall 242s; status ok
- command: `python -m labkit.run threads/active-droplets/worlds/ad5n-neutral/world.py --out threads/active-droplets/packs/ad5n-neutral --seeds 0 1 2 --frames 200`
- segmentation: matter > 0.35 of robust range [-1.0648, 1.4289], min area 6 px

## Measurements
- components: final 11, mean 8.8, max 11; occupancy final 0.12
- tracks: 16; persistent (alive >= 50% of run): 9; longest 201 frames; alive start-to-end: 3
- size of persistent tracks: max/min area ratio 3.00 (1 = constant size)
- enclosures: components with a hole mean 0.09, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [11, 11, 11], H1 [0, 0, 0]
- motion: 2 long-lived tracks moved >= 1 body length; max speed 0.0012/time; max body lengths 1.7
- replication: splits 5, persistent splits 5, max generation 2, merges 0, nucleations 0
- channel total drift (end/start - 1): [0.0904, -0.5767, 0.0145, None, None, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 0 at frame 101: holes 0, rim-vs-core 0.54, rim-vs-outside 0.65, heterogeneity 0.08; core [0.953, 0.036, 0.0, 0.01, 0.967, 0.0] rim [0.62, 0.131, 0.0, 0.006, 0.557, 0.0]
  - track 2 at frame 101: holes 0, rim-vs-core 0.53, rim-vs-outside 0.64, heterogeneity 0.08; core [0.953, 0.034, 0.944, 0.001, 0.0, 0.0] rim [0.627, 0.132, 0.537, 0.001, 0.0, 0.0]
  - track 3 at frame 101: holes 0, rim-vs-core 0.50, rim-vs-outside 0.64, heterogeneity 0.10; core [0.942, 0.049, 0.146, 0.0, 0.0, 0.887] rim [0.623, 0.133, 0.097, 0.0, 0.0, 0.512]
  - track 12 at frame 165: holes 0, rim-vs-core 0.52, rim-vs-outside 0.65, heterogeneity 0.08; core [0.963, 0.045, 0.933, 0.0, 0.0, 0.0] rim [0.634, 0.126, 0.535, 0.0, 0.0, 0.0]

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, lineage.png, timeseries.png, movie.mp4, metrics.json

Measurements are screens, not verdicts: judge them against the images.
