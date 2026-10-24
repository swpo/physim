# Evidence pack: ad7-gated (seed 2)

- world: `../../../worlds/ad7-gated/world.py`, family `phase-field`
- parent: ad5-evolve + ad3-membrane + fisim-beyond-laplacian (gated diffusion); mutation: membrane gates fuel and catalyst diffusion (D e^{-b psi}); alleles differ in amphiphile output, not catalysis
- run: 201 frames x 200 steps x dt 0.5 = time 20000; grid [128, 128]; wall 445s; status ok
- command: `python -m labkit.run threads/active-droplets/worlds/ad7-gated/world.py --out threads/active-droplets/packs/ad7-gated --seeds 0 1 2 --frames 200`
- segmentation: matter > 0.35 of robust range [-1.0648, 1.4806], min area 6 px

## Measurements
- components: final 10, mean 7.6, max 11; occupancy final 0.10
- tracks: 20; persistent (alive >= 50% of run): 4; longest 201 frames; alive start-to-end: 1
- size of persistent tracks: max/min area ratio 13.00 (1 = constant size)
- enclosures: components with a hole mean 0.02, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [10, 10, 10], H1 [0, 0, 0]
- motion: 1 long-lived tracks moved >= 1 body length; max speed 0.000914/time; max body lengths 1.0
- replication: splits 7, persistent splits 6, max generation 3, merges 0, nucleations 0
- channel total drift (end/start - 1): [0.0423, -0.4849, None, -0.4558, None, None, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 5 at frame 101: holes 0, rim-vs-core 0.49, rim-vs-outside 0.56, heterogeneity 0.07; core [0.96, 0.096, 0.0, 0.833, 0.0, 0.0, 0.0] rim [0.631, 0.202, 0.001, 0.482, 0.0, 0.0, 0.0]
  - track 6 at frame 116: holes 0, rim-vs-core 0.53, rim-vs-outside 0.54, heterogeneity 0.07; core [0.952, 0.082, 0.0, 0.858, 0.0, 0.001, 0.0] rim [0.602, 0.201, 0.001, 0.481, 0.0, 0.0, 0.0]
  - track 1 at frame 84: holes 0, rim-vs-core 0.32, rim-vs-outside 0.69, heterogeneity 0.09; core [0.952, 0.077, 0.023, 0.624, 0.226, 0.0, 0.0] rim [0.745, 0.141, 0.053, 0.396, 0.245, 0.0, 0.0]
  - track 16 at frame 183: holes 0, rim-vs-core 0.63, rim-vs-outside 0.74, heterogeneity 0.10; core [0.928, 0.026, 0.103, 0.0, 0.978, 0.0, 0.006] rim [0.607, 0.128, 0.462, 0.0, 0.586, 0.0, 0.004]

## Warnings
- none

## Files
sheet.png, tracks.png, lineage.png, timeseries.png, movie.mp4, metrics.json

Measurements are screens, not verdicts: judge them against the images.
