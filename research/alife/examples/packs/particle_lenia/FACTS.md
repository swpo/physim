# Evidence pack: particle-lenia-ref (seed 0)

- world: `../../particle_lenia/world.py`, family `particle`
- parent: None; mutation: reference
- run: 101 frames x 20 steps x dt 0.1 = time 200; grid [128, 128]; wall 31s; status ok
- command: `python -m labkit.run examples/particle_lenia/world.py --out examples/packs/particle_lenia --frames 100`
- segmentation: matter > 0.35 of robust range [0.0, 1.0261], min area 6 px

## Measurements
- components: final 1, mean 1.0, max 1; occupancy final 0.04
- tracks: 1; persistent (alive >= 50% of run): 1; longest 101 frames; alive start-to-end: 1
- size of persistent tracks: max/min area ratio 1.24 (1 = constant size)
- enclosures: components with a hole mean 0.65, final 1; holes at thresholds 0.2/0.35/0.5 final [0, 3, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [2, 1, 1], H1 [1, 0, 0]
- motion: 0 long-lived tracks moved >= 1 body length; max speed 0/time; max body lengths 0.0
- replication: splits 0, persistent splits 0, max generation 0, merges 0, nucleations 0
- channel total drift (end/start - 1): [-0.0]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 0 at frame 50: holes 3, rim-vs-core 0.38, rim-vs-outside 0.29, heterogeneity 0.20; core [0.931] rim [0.554]

## Warnings
- none

## Files
sheet.png, tracks.png, lineage.png, timeseries.png, particles.png, movie.mp4, metrics.json

Measurements are screens, not verdicts: judge them against the images.
