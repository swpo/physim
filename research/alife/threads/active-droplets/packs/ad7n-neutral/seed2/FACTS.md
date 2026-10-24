# Evidence pack: ad7n-neutral (seed 2)

- world: `../../../worlds/ad7n-neutral/world.py`, family `phase-field`
- parent: ad7-gated; mutation: neutral control: all four alleles make no amphiphile (kp=0), same mutation and dilution
- run: 201 frames x 200 steps x dt 0.5 = time 20000; grid [128, 128]; wall 442s; status ok
- command: `python -m labkit.run threads/active-droplets/worlds/ad7n-neutral/world.py --out threads/active-droplets/packs/ad7n-neutral --seeds 0 1 2 --frames 200`
- segmentation: matter > 0.35 of robust range [-1.0594, 1.455], min area 6 px

## Measurements
- components: final 4, mean 4.6, max 6; occupancy final 0.08
- tracks: 6; persistent (alive >= 50% of run): 5; longest 201 frames; alive start-to-end: 4
- size of persistent tracks: max/min area ratio 4.63 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [4, 4, 4], H1 [0, 0, 0]
- motion: 2 long-lived tracks moved >= 1 body length; max speed 0.00103/time; max body lengths 1.2
- replication: splits 0, persistent splits 0, max generation 0, merges 0, nucleations 0
- channel total drift (end/start - 1): [-0.0076, -0.3855, None, -0.6219, None, None, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 0 at frame 101: holes 0, rim-vs-core 0.53, rim-vs-outside 0.57, heterogeneity 0.07; core [0.957, 0.056, 0.0, 0.0, 0.0, 0.071, 0.949] rim [0.61, 0.189, 0.0, 0.0, 0.0, 0.041, 0.57]
  - track 1 at frame 101: holes 0, rim-vs-core 0.42, rim-vs-outside 0.67, heterogeneity 0.07; core [0.96, 0.046, 0.0, 0.906, 0.001, 0.0, 0.0] rim [0.71, 0.156, 0.0, 0.59, 0.001, 0.0, 0.0]
  - track 4 at frame 101: holes 0, rim-vs-core 0.60, rim-vs-outside 0.60, heterogeneity 0.09; core [0.959, 0.063, 0.0, 0.677, 0.0, 0.931, 0.0] rim [0.624, 0.195, 0.0, 0.379, 0.0, 0.559, 0.0]
  - track 5 at frame 101: holes 0, rim-vs-core 0.54, rim-vs-outside 0.56, heterogeneity 0.07; core [0.965, 0.069, 0.0, 0.003, 0.892, 0.005, 0.113] rim [0.612, 0.196, 0.0, 0.002, 0.506, 0.003, 0.064]

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, lineage.png, timeseries.png, movie.mp4, metrics.json

Measurements are screens, not verdicts: judge them against the images.
