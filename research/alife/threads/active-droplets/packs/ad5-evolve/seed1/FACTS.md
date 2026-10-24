# Evidence pack: ad5-evolve (seed 1)

- world: `../../../worlds/ad5-evolve/world.py`, family `phase-field`
- parent: ad2-catalysts; mutation: N catalyst alleles with different rates, rare local mutation patches, random dilution disks
- run: 201 frames x 200 steps x dt 0.5 = time 20000; grid [128, 128]; wall 265s; status ok
- command: `python -m labkit.run threads/active-droplets/worlds/ad5-evolve/world.py --out threads/active-droplets/packs/ad5-evolve --seeds 0 1 2 --frames 200`
- segmentation: matter > 0.35 of robust range [-1.0689, 1.4532], min area 6 px

## Measurements
- components: final 11, mean 7.4, max 12; occupancy final 0.12
- tracks: 19; persistent (alive >= 50% of run): 6; longest 201 frames; alive start-to-end: 1
- size of persistent tracks: max/min area ratio 2.82 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [11, 11, 11], H1 [0, 0, 0]
- motion: 3 long-lived tracks moved >= 1 body length; max speed 0.00216/time; max body lengths 1.6
- replication: splits 7, persistent splits 5, max generation 2, merges 0, nucleations 0
- channel total drift (end/start - 1): [0.0913, -0.5706, -0.2343, None, None, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 3 at frame 101: holes 0, rim-vs-core 0.47, rim-vs-outside 0.71, heterogeneity 0.11; core [0.94, 0.103, 0.644, 0.951, 0.005, 0.0] rim [0.621, 0.215, 0.362, 0.776, 0.003, 0.0]
  - track 1 at frame 96: holes 0, rim-vs-core 0.52, rim-vs-outside 0.63, heterogeneity 0.08; core [0.955, 0.111, 0.89, 0.064, 0.072, 0.0] rim [0.627, 0.214, 0.506, 0.04, 0.045, 0.0]
  - track 5 at frame 134: holes 0, rim-vs-core 0.37, rim-vs-outside 0.78, heterogeneity 0.07; core [0.936, 0.029, 0.001, 0.11, 1.0, 0.001] rim [0.619, 0.131, 0.001, 0.07, 0.834, 0.0]
  - track 12 at frame 160: holes 0, rim-vs-core 0.55, rim-vs-outside 0.62, heterogeneity 0.08; core [0.931, 0.014, 0.0, 0.0, 0.0, 0.951] rim [0.601, 0.099, 0.0, 0.0, 0.0, 0.525]

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, lineage.png, timeseries.png, movie.mp4, metrics.json

Measurements are screens, not verdicts: judge them against the images.
