# Evidence pack: phase-trait (seed 1)

- world: `../../../worlds/phase_trait/world.py`, family `autopoiesis`
- parent: threads/autopoiesis/worlds/phase_kinds; mutation: continuous heritable catalyst trait c (growth rate) with link-output trade-off b(c) and +-delta point mutations
- run: 161 frames x 300 steps x dt 1.0 = time 48000; grid [128, 128]; wall 68s; status ok
- command: `python -m labkit.run threads/autopoiesis/worlds/phase_trait/world.py --out threads/autopoiesis/packs/phase_trait --seeds 0 1 2 --frames 160 --spf 300`
- segmentation: matter > 0.35 of robust range [0.0, 1.4975], min area 6 px

## Measurements
- components: final 36, mean 31.7, max 38; occupancy final 0.41
- tracks: 81; persistent (alive >= 50% of run): 35; longest 145 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 4.18 (1 = constant size)
- enclosures: components with a hole mean 4.96, final 12; holes at thresholds 0.2/0.35/0.5 final [0, 12, 35]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [36, 36, 36], H1 [37, 36, 0]
- motion: 0 long-lived tracks moved >= 1 body length; max speed 0/time; max body lengths 0.8
- replication: splits 37, persistent splits 28, max generation 3, merges 0, nucleations 0
- channel total drift (end/start - 1): [-0.5264, 13.1895, 32.6516, 11.0037, 10.277]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 19 at frame 89: holes 0, rim-vs-core 0.50, rim-vs-outside 1.25, heterogeneity 0.18; core [0.089, 0.821, 0.8, 0.882, 0.54] rim [0.283, 0.421, 0.746, 0.733, 0.703]
  - track 20 at frame 89: holes 0, rim-vs-core 0.48, rim-vs-outside 1.16, heterogeneity 0.19; core [0.101, 0.74, 0.735, 0.852, 0.534] rim [0.297, 0.369, 0.648, 0.705, 0.693]
  - track 26 at frame 90: holes 0, rim-vs-core 0.47, rim-vs-outside 1.11, heterogeneity 0.18; core [0.12, 0.667, 0.648, 0.854, 0.493] rim [0.301, 0.35, 0.557, 0.71, 0.733]
  - track 37 at frame 93: holes 0, rim-vs-core 0.52, rim-vs-outside 1.41, heterogeneity 0.18; core [0.068, 0.953, 0.963, 0.87, 0.61] rim [0.268, 0.498, 0.949, 0.747, 0.681]

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, lineage.png, timeseries.png, movie.mp4, metrics.json

Measurements are screens, not verdicts: judge them against the images.
