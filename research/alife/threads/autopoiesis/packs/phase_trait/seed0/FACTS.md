# Evidence pack: phase-trait (seed 0)

- world: `../../../worlds/phase_trait/world.py`, family `autopoiesis`
- parent: threads/autopoiesis/worlds/phase_kinds; mutation: continuous heritable catalyst trait c (growth rate) with link-output trade-off b(c) and +-delta point mutations
- run: 161 frames x 300 steps x dt 1.0 = time 48000; grid [128, 128]; wall 68s; status ok
- command: `python -m labkit.run threads/autopoiesis/worlds/phase_trait/world.py --out threads/autopoiesis/packs/phase_trait --seeds 0 1 2 --frames 160 --spf 300`
- segmentation: matter > 0.35 of robust range [0.0, 1.5075], min area 6 px

## Measurements
- components: final 39, mean 30.8, max 39; occupancy final 0.40
- tracks: 89; persistent (alive >= 50% of run): 28; longest 148 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 3.33 (1 = constant size)
- enclosures: components with a hole mean 8.35, final 8; holes at thresholds 0.2/0.35/0.5 final [0, 8, 32]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [39, 39, 39], H1 [40, 39, 0]
- motion: 1 long-lived tracks moved >= 1 body length; max speed 0.000994/time; max body lengths 1.1
- replication: splits 41, persistent splits 26, max generation 4, merges 0, nucleations 0
- channel total drift (end/start - 1): [-0.5276, 13.3944, 33.8199, 10.853, 9.0395]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 9 at frame 87: holes 1, rim-vs-core 0.34, rim-vs-outside 1.11, heterogeneity 0.19; core [0.118, 0.741, 0.711, 0.887, 0.608] rim [0.239, 0.471, 0.624, 0.744, 0.602]
  - track 17 at frame 87: holes 0, rim-vs-core 0.51, rim-vs-outside 1.38, heterogeneity 0.18; core [0.066, 0.943, 0.947, 0.855, 0.615] rim [0.271, 0.492, 0.92, 0.741, 0.674]
  - track 18 at frame 87: holes 0, rim-vs-core 0.38, rim-vs-outside 1.52, heterogeneity 0.18; core [0.061, 0.982, 1.0, 0.865, 0.626] rim [0.215, 0.646, 0.989, 0.791, 0.685]
  - track 81 at frame 149: holes 0, rim-vs-core 0.39, rim-vs-outside 1.40, heterogeneity 0.17; core [0.07, 0.889, 0.879, 0.861, 0.57] rim [0.23, 0.561, 0.869, 0.774, 0.69]

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, lineage.png, timeseries.png, movie.mp4, metrics.json

Measurements are screens, not verdicts: judge them against the images.
