# Evidence pack: ad5-evolve (seed 2)

- world: `../../../worlds/ad5-evolve/world.py`, family `phase-field`
- parent: ad2-catalysts; mutation: N catalyst alleles with different rates, rare local mutation patches, random dilution disks
- run: 201 frames x 200 steps x dt 0.5 = time 20000; grid [128, 128]; wall 249s; status ok
- command: `python -m labkit.run threads/active-droplets/worlds/ad5-evolve/world.py --out threads/active-droplets/packs/ad5-evolve --seeds 0 1 2 --frames 200`
- segmentation: matter > 0.35 of robust range [-1.067, 1.4474], min area 6 px

## Measurements
- components: final 11, mean 8.2, max 11; occupancy final 0.12
- tracks: 16; persistent (alive >= 50% of run): 7; longest 201 frames; alive start-to-end: 3
- size of persistent tracks: max/min area ratio 2.99 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [11, 11, 11], H1 [0, 0, 0]
- motion: 3 long-lived tracks moved >= 1 body length; max speed 0.00123/time; max body lengths 1.4
- replication: splits 5, persistent splits 4, max generation 2, merges 0, nucleations 0
- channel total drift (end/start - 1): [0.099, -0.5973, -0.8116, None, None, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 1 at frame 101: holes 0, rim-vs-core 0.45, rim-vs-outside 0.73, heterogeneity 0.08; core [0.966, 0.109, 0.96, 0.002, 0.0, 0.0] rim [0.69, 0.204, 0.619, 0.001, 0.0, 0.0]
  - track 3 at frame 101: holes 0, rim-vs-core 0.53, rim-vs-outside 0.65, heterogeneity 0.08; core [0.964, 0.129, 0.945, 0.0, 0.0, 0.0] rim [0.63, 0.217, 0.541, 0.0, 0.0, 0.0]
  - track 5 at frame 101: holes 0, rim-vs-core 0.54, rim-vs-outside 0.64, heterogeneity 0.08; core [0.962, 0.125, 0.944, 0.0, 0.0, 0.0] rim [0.619, 0.218, 0.533, 0.0, 0.0, 0.0]
  - track 11 at frame 163: holes 0, rim-vs-core 0.53, rim-vs-outside 0.65, heterogeneity 0.08; core [0.942, 0.014, 0.0, 0.0, 0.0, 0.967] rim [0.619, 0.094, 0.0, 0.0, 0.0, 0.557]

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, lineage.png, timeseries.png, movie.mp4, metrics.json

Measurements are screens, not verdicts: judge them against the images.
