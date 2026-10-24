# Evidence pack: plife-m2 (seed 2)

- world: `../../../worlds/plife-m2/world.py`, family `particle`
- parent: particle life (Mohr force, LITERATURE 2.3.2), random matrix screen; mutation: none (baseline); periodic box at ~21 particles per r_max^2
- run: 161 frames x 25 steps x dt 0.02 = time 80; grid [128, 128]; wall 29s; status ok
- command: `python -m labkit.run threads/particle-life/worlds/plife-m2/world.py --out threads/particle-life/packs/plife-m2 --seeds 0 1 2 --frames 160`
- segmentation: matter > 0.35 of robust range [0.0, 8.6921], min area 6 px

## Measurements
- components: final 6, mean 6.4, max 8; occupancy final 0.02
- tracks: 86; persistent (alive >= 50% of run): 5; longest 151 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 2.94 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [11, 8, 6], H1 [0, 0, 0]
- motion: 12 long-lived tracks moved >= 1 body length; max speed 7.45/time; max body lengths 13.2
- replication: splits 0, persistent splits 0, max generation 0, merges 0, nucleations 86
- channel total drift (end/start - 1): [0.0, -0.0, 0.0, 0.0, 0.0]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 12 at frame 86: holes 0, rim-vs-core 0.19, rim-vs-outside 0.35, heterogeneity 0.03; core [0.0, 1.0, 0.0, 0.744, 0.0] rim [0.0, 0.985, 0.0, 0.934, 0.0]
  - track 16 at frame 86: holes 0, rim-vs-core 0.10, rim-vs-outside 0.46, heterogeneity 0.02; core [0.0, 1.0, 0.0, 0.866, 0.0] rim [0.0, 0.987, 0.0, 0.964, 0.0]
  - track 23 at frame 83: holes 0, rim-vs-core 0.51, rim-vs-outside 0.44, heterogeneity 0.20; core [0.478, 0.0, 0.02, 0.656, 0.945] rim [0.754, 0.0, 0.012, 0.321, 0.675]
  - track 59 at frame 113: holes 0, rim-vs-core 0.35, rim-vs-outside 0.50, heterogeneity 0.11; core [0.612, 0.0, 0.602, 0.014, 1.0] rim [0.738, 0.0, 0.296, 0.008, 0.884]

## Warnings
- none

## Files
sheet.png, tracks.png, lineage.png, timeseries.png, particles.png, movie.mp4, metrics.json

Measurements are screens, not verdicts: judge them against the images.
