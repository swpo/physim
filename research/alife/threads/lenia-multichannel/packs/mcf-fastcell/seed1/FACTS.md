# Evidence pack: mcf-fastcell (seed 1)

- world: `../../../worlds/mcf-fastcell/world.py`, family `lenia`
- parent: mc-fastcell; mutation: matter can only be built from a consumed, regrowing, diffusing food field F (yield Y=5): motion now costs food
- run: 301 frames x 10 steps x dt 0.1 = time 300; grid [192, 192]; wall 59s; status ok
- command: `python -m labkit.run threads/lenia-multichannel/worlds/mcf-fastcell/world.py --out threads/lenia-multichannel/packs/mcf-fastcell --seeds 0 1 2 --frames 300 --spf 10`
- segmentation: matter > 0.35 of robust range [0.0, 2.0], min area 6 px

## Measurements
- components: final 4, mean 4.2, max 6; occupancy final 0.04
- tracks: 39; persistent (alive >= 50% of run): 1; longest 213 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 1.37 (1 = constant size)
- enclosures: components with a hole mean 0.73, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 1]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [5, 4, 4], H1 [0, 0, 0]
- motion: 12 long-lived tracks moved >= 1 body length; max speed 1.35/time; max body lengths 8.4
- replication: splits 16, persistent splits 0, max generation 0, merges 2, nucleations 1
- channel total drift (end/start - 1): [-0.071, -0.0176, 0.0258, -0.2899]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 14 at frame 194: holes 0, rim-vs-core 0.27, rim-vs-outside 0.67, heterogeneity 0.21; core [0.0, 0.731, 0.742, 0.212] rim [0.003, 0.759, 0.476, 0.249]
  - track 6 at frame 88: holes 0, rim-vs-core 0.35, rim-vs-outside 0.54, heterogeneity 0.23; core [0.0, 0.842, 0.72, 0.35] rim [0.051, 0.581, 0.504, 0.402]
  - track 30 at frame 247: holes 0, rim-vs-core 0.16, rim-vs-outside 0.67, heterogeneity 0.19; core [0.0, 0.854, 0.654, 0.0] rim [0.002, 0.705, 0.596, 0.003]
  - track 12 at frame 126: holes 0, rim-vs-core 0.37, rim-vs-outside 0.66, heterogeneity 0.23; core [0.003, 0.71, 0.813, 0.349] rim [0.029, 0.72, 0.452, 0.396]

## Warnings
- none

## Files
sheet.png, tracks.png, lineage.png, timeseries.png, movie.mp4, metrics.json

Measurements are screens, not verdicts: judge them against the images.
