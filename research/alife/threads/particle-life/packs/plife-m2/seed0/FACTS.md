# Evidence pack: plife-m2 (seed 0)

- world: `../../../worlds/plife-m2/world.py`, family `particle`
- parent: particle life (Mohr force, LITERATURE 2.3.2), random matrix screen; mutation: none (baseline); periodic box at ~21 particles per r_max^2
- run: 161 frames x 25 steps x dt 0.02 = time 80; grid [128, 128]; wall 35s; status ok
- command: `python -m labkit.run threads/particle-life/worlds/plife-m2/world.py --out threads/particle-life/packs/plife-m2 --seeds 0 1 2 --frames 160`
- segmentation: matter > 0.35 of robust range [0.0, 10.6059], min area 6 px

## Measurements
- components: final 6, mean 5.8, max 8; occupancy final 0.01
- tracks: 54; persistent (alive >= 50% of run): 4; longest 155 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 4.35 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [7, 6, 2], H1 [0, 0, 0]
- motion: 6 long-lived tracks moved >= 1 body length; max speed 0.731/time; max body lengths 8.9
- replication: splits 0, persistent splits 0, max generation 0, merges 0, nucleations 54
- channel total drift (end/start - 1): [0.0, 0.0, 0.0, 0.0, 0.0]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 3 at frame 83: holes 0, rim-vs-core 0.15, rim-vs-outside 0.38, heterogeneity 0.02; core [0.0, 1.0, 0.0, 1.0, 0.0] rim [0.0, 0.848, 0.0, 1.0, 0.0]
  - track 24 at frame 90: holes 0, rim-vs-core 0.05, rim-vs-outside 0.09, heterogeneity 0.02; core [0.002, 1.0, 0.0, 0.617, 0.0] rim [0.008, 1.0, 0.0, 0.669, 0.0]
  - track 25 at frame 90: holes 0, rim-vs-core 0.57, rim-vs-outside 0.40, heterogeneity 0.16; core [0.494, 0.0, 0.0, 0.818, 1.0] rim [0.808, 0.0, 0.0, 0.364, 0.845]
  - track 23 at frame 58: holes 0, rim-vs-core 0.12, rim-vs-outside 0.53, heterogeneity 0.02; core [0.0, 1.0, 0.0, 1.0, 0.0] rim [0.0, 0.882, 0.0, 1.0, 0.0]

## Warnings
- none

## Files
sheet.png, tracks.png, lineage.png, timeseries.png, particles.png, movie.mp4, metrics.json

Measurements are screens, not verdicts: judge them against the images.
