# Evidence pack: plife-m2 (seed 1)

- world: `../../../worlds/plife-m2/world.py`, family `particle`
- parent: particle life (Mohr force, LITERATURE 2.3.2), random matrix screen; mutation: none (baseline); periodic box at ~21 particles per r_max^2
- run: 161 frames x 25 steps x dt 0.02 = time 80; grid [128, 128]; wall 32s; status ok
- command: `python -m labkit.run threads/particle-life/worlds/plife-m2/world.py --out threads/particle-life/packs/plife-m2 --seeds 0 1 2 --frames 160`
- segmentation: matter > 0.35 of robust range [0.0, 9.231], min area 6 px

## Measurements
- components: final 5, mean 5.3, max 7; occupancy final 0.02
- tracks: 51; persistent (alive >= 50% of run): 3; longest 130 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 1.41 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [8, 7, 5], H1 [0, 0, 0]
- motion: 8 long-lived tracks moved >= 1 body length; max speed 4.79/time; max body lengths 12.4
- replication: splits 0, persistent splits 0, max generation 0, merges 0, nucleations 51
- channel total drift (end/start - 1): [0.0, 0.0, 0.0, 0.0, 0.0]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 32 at frame 95: holes 0, rim-vs-core 0.70, rim-vs-outside 0.33, heterogeneity 0.15; core [0.53, 0.0, 0.876, 0.178, 0.959] rim [0.973, 0.0, 1.0, 0.084, 0.434]
  - track 3 at frame 65: holes 0, rim-vs-core 0.11, rim-vs-outside 0.54, heterogeneity 0.03; core [0.0, 1.0, 0.0, 0.983, 0.0] rim [0.0, 0.888, 0.0, 0.998, 0.0]
  - track 0 at frame 50: holes 0, rim-vs-core 0.10, rim-vs-outside 0.54, heterogeneity 0.03; core [0.0, 1.0, 0.0, 0.896, 0.0] rim [0.0, 0.927, 0.0, 0.971, 0.0]
  - track 18 at frame 54: holes 0, rim-vs-core 0.21, rim-vs-outside 0.47, heterogeneity 0.04; core [0.0, 1.0, 0.0, 1.0, 0.0] rim [0.0, 0.792, 0.0, 0.986, 0.0]

## Warnings
- none

## Files
sheet.png, tracks.png, lineage.png, timeseries.png, particles.png, movie.mp4, metrics.json

Measurements are screens, not verdicts: judge them against the images.
