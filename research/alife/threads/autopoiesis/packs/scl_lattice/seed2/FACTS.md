# Evidence pack: scl-lattice (seed 2)

- world: `../../../worlds/scl_lattice/world.py`, family `autopoiesis`
- parent: None; mutation: reference lattice SCL (McMullin-Varela rules: bond angle >= 90 deg, no crossing, splicing)
- run: 151 frames x 20 steps x dt 1.0 = time 3000; grid [64, 64]; wall 1s; status ok
- command: `python -m labkit.run threads/autopoiesis/worlds/scl_lattice/world.py --out threads/autopoiesis/packs/scl_lattice --seeds 0 1 2 --frames 150 --spf 20`
- segmentation: matter > 0.35 of robust range [0.0, 2.0], min area 6 px

## Measurements
- components: final 2, mean 1.0, max 2; occupancy final 0.03
- tracks: 3; persistent (alive >= 50% of run): 1; longest 148 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 2.50 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [5, 3, 2], H1 [1, 0, 0]
- motion: 0 long-lived tracks moved >= 1 body length; max speed 0/time; max body lengths 0.1
- replication: splits 1, persistent splits 0, max generation 0, merges 0, nucleations 0
- channel total drift (end/start - 1): [-0.0057, 0.0, None, -0.1042]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 0 at frame 74: holes 0, rim-vs-core 0.43, rim-vs-outside 0.40, heterogeneity 0.25; core [0.729, 0.006, 0.017, 0.0] rim [0.465, 0.0, 0.0, 0.333]
  - track 1 at frame 150: holes 0, rim-vs-core 1.15, rim-vs-outside 0.16, heterogeneity 0.24; core [0.0, 0.0, 0.0, 1.0] rim [0.621, 0.0, 0.0, 0.034]
  - track 2 at frame 150: holes 0, rim-vs-core 1.10, rim-vs-outside 0.09, heterogeneity 0.24; core [0.0, 0.0, 0.0, 1.0] rim [0.556, 0.0, 0.0, 0.056]

## Warnings
- none

## Files
sheet.png, tracks.png, lineage.png, timeseries.png, movie.mp4, metrics.json

Measurements are screens, not verdicts: judge them against the images.
