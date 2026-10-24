# Evidence pack: ad7-gated (seed 0)

- world: `../../../worlds/ad7-gated/world.py`, family `phase-field`
- parent: ad5-evolve + ad3-membrane + fisim-beyond-laplacian (gated diffusion); mutation: membrane gates fuel and catalyst diffusion (D e^{-b psi}); alleles differ in amphiphile output, not catalysis
- run: 201 frames x 200 steps x dt 0.5 = time 20000; grid [128, 128]; wall 419s; status ok
- command: `python -m labkit.run threads/active-droplets/worlds/ad7-gated/world.py --out threads/active-droplets/packs/ad7-gated --seeds 0 1 2 --frames 200`
- segmentation: matter > 0.35 of robust range [-1.0612, 1.4777], min area 6 px

## Measurements
- components: final 7, mean 6.2, max 8; occupancy final 0.10
- tracks: 16; persistent (alive >= 50% of run): 4; longest 174 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 2.38 (1 = constant size)
- enclosures: components with a hole mean 0.08, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [8, 7, 7], H1 [0, 0, 0]
- motion: 3 long-lived tracks moved >= 1 body length; max speed 0.00117/time; max body lengths 1.1
- replication: splits 6, persistent splits 5, max generation 2, merges 0, nucleations 0
- channel total drift (end/start - 1): [0.0348, -0.4588, None, 0.3332, None, None, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 4 at frame 114: holes 0, rim-vs-core 0.35, rim-vs-outside 0.85, heterogeneity 0.09; core [0.915, 0.037, 0.037, 0.944, 0.0, 0.0, 0.506] rim [0.719, 0.105, 0.126, 0.709, 0.0, 0.0, 0.382]
  - track 9 at frame 123: holes 0, rim-vs-core 0.50, rim-vs-outside 0.56, heterogeneity 0.07; core [0.953, 0.07, 0.0, 0.854, 0.0, 0.0, 0.0] rim [0.627, 0.19, 0.003, 0.489, 0.0, 0.0, 0.0]
  - track 10 at frame 131: holes 0, rim-vs-core 0.49, rim-vs-outside 0.55, heterogeneity 0.07; core [0.959, 0.086, 0.0, 0.822, 0.0, 0.0, 0.0] rim [0.628, 0.195, 0.002, 0.472, 0.0, 0.0, 0.0]
  - track 12 at frame 156: holes 0, rim-vs-core 0.55, rim-vs-outside 0.91, heterogeneity 0.12; core [0.916, 0.01, 0.282, 0.0, 0.0, 1.0, 0.0] rim [0.704, 0.1, 0.731, 0.0, 0.0, 0.775, 0.0]

## Warnings
- none

## Files
sheet.png, tracks.png, lineage.png, timeseries.png, movie.mp4, metrics.json

Measurements are screens, not verdicts: judge them against the images.
