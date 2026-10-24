# Evidence pack: scl-lattice (seed 0)

- world: `../../../worlds/scl_lattice/world.py`, family `autopoiesis`
- parent: None; mutation: reference lattice SCL (McMullin-Varela rules: bond angle >= 90 deg, no crossing, splicing)
- run: 151 frames x 20 steps x dt 1.0 = time 3000; grid [64, 64]; wall 3s; status ok
- command: `python -m labkit.run threads/autopoiesis/worlds/scl_lattice/world.py --out threads/autopoiesis/packs/scl_lattice --seeds 0 1 2 --frames 150 --spf 20`
- segmentation: matter > 0.35 of robust range [0.0, 2.0], min area 6 px

## Measurements
- components: final 1, mean 1.0, max 1; occupancy final 0.08
- tracks: 1; persistent (alive >= 50% of run): 1; longest 151 frames; alive start-to-end: 1
- size of persistent tracks: max/min area ratio 1.01 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 1]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [4, 1, 1], H1 [1, 0, 0]
- motion: 0 long-lived tracks moved >= 1 body length; max speed 0/time; max body lengths 0.0
- replication: splits 0, persistent splits 0, max generation 0, merges 0, nucleations 0
- channel total drift (end/start - 1): [-0.0077, 0.0, None, 0.0]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 0 at frame 76: holes 0, rim-vs-core 0.37, rim-vs-outside 0.41, heterogeneity 0.27; core [0.6, 0.006, 0.033, 0.0] rim [0.451, 0.0, 0.021, 0.333]

## Warnings
- none

## Files
sheet.png, tracks.png, lineage.png, timeseries.png, movie.mp4, metrics.json

Measurements are screens, not verdicts: judge them against the images.
