# Evidence pack: ad7-gated (seed 1)

- world: `../../../worlds/ad7-gated/world.py`, family `phase-field`
- parent: ad5-evolve + ad3-membrane + fisim-beyond-laplacian (gated diffusion); mutation: membrane gates fuel and catalyst diffusion (D e^{-b psi}); alleles differ in amphiphile output, not catalysis
- run: 201 frames x 200 steps x dt 0.5 = time 20000; grid [128, 128]; wall 424s; status ok
- command: `python -m labkit.run threads/active-droplets/worlds/ad7-gated/world.py --out threads/active-droplets/packs/ad7-gated --seeds 0 1 2 --frames 200`
- segmentation: matter > 0.35 of robust range [-1.0636, 1.4731], min area 6 px

## Measurements
- components: final 8, mean 6.7, max 9; occupancy final 0.10
- tracks: 15; persistent (alive >= 50% of run): 4; longest 201 frames; alive start-to-end: 3
- size of persistent tracks: max/min area ratio 3.24 (1 = constant size)
- enclosures: components with a hole mean 0.04, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [8, 8, 8], H1 [0, 0, 0]
- motion: 2 long-lived tracks moved >= 1 body length; max speed 0.000885/time; max body lengths 1.1
- replication: splits 5, persistent splits 4, max generation 3, merges 0, nucleations 0
- channel total drift (end/start - 1): [0.0477, -0.4804, None, 0.2235, None, None, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 0 at frame 101: holes 0, rim-vs-core 0.32, rim-vs-outside 0.72, heterogeneity 0.07; core [0.952, 0.077, 0.0, 0.836, 0.0, 0.0, 0.0] rim [0.729, 0.148, 0.0, 0.614, 0.0, 0.0, 0.0]
  - track 1 at frame 101: holes 0, rim-vs-core 0.48, rim-vs-outside 0.56, heterogeneity 0.07; core [0.949, 0.065, 0.017, 0.798, 0.067, 0.0, 0.0] rim [0.629, 0.177, 0.074, 0.464, 0.04, 0.0, 0.0]
  - track 4 at frame 101: holes 0, rim-vs-core 0.37, rim-vs-outside 0.70, heterogeneity 0.07; core [0.957, 0.069, 0.0, 0.853, 0.0, 0.0, 0.0] rim [0.72, 0.157, 0.0, 0.587, 0.0, 0.0, 0.0]
  - track 11 at frame 175: holes 0, rim-vs-core 0.66, rim-vs-outside 0.72, heterogeneity 0.08; core [0.92, 0.012, 0.366, 0.0, 0.043, 1.0, 0.004] rim [0.628, 0.126, 0.947, 0.0, 0.027, 1.0, 0.003]

## Warnings
- none

## Files
sheet.png, tracks.png, lineage.png, timeseries.png, movie.mp4, metrics.json

Measurements are screens, not verdicts: judge them against the images.
