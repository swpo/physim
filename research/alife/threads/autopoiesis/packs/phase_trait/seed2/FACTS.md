# Evidence pack: phase-trait (seed 2)

- world: `../../../worlds/phase_trait/world.py`, family `autopoiesis`
- parent: threads/autopoiesis/worlds/phase_kinds; mutation: continuous heritable catalyst trait c (growth rate) with link-output trade-off b(c) and +-delta point mutations
- run: 161 frames x 300 steps x dt 1.0 = time 48000; grid [128, 128]; wall 72s; status ok
- command: `python -m labkit.run threads/autopoiesis/worlds/phase_trait/world.py --out threads/autopoiesis/packs/phase_trait --seeds 0 1 2 --frames 160 --spf 300`
- segmentation: matter > 0.35 of robust range [0.0, 1.5017], min area 6 px

## Measurements
- components: final 38, mean 31.2, max 40; occupancy final 0.40
- tracks: 79; persistent (alive >= 50% of run): 36; longest 147 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 5.62 (1 = constant size)
- enclosures: components with a hole mean 5.28, final 12; holes at thresholds 0.2/0.35/0.5 final [0, 12, 32]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [38, 38, 38], H1 [39, 37, 0]
- motion: 1 long-lived tracks moved >= 1 body length; max speed 0.000585/time; max body lengths 1.3
- replication: splits 36, persistent splits 21, max generation 4, merges 0, nucleations 0
- channel total drift (end/start - 1): [-0.5257, 13.3919, 33.7135, 10.7755, 8.9598]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 13 at frame 87: holes 0, rim-vs-core 0.54, rim-vs-outside 1.00, heterogeneity 0.20; core [0.168, 0.654, 0.552, 0.977, 0.54] rim [0.338, 0.295, 0.365, 0.692, 0.686]
  - track 17 at frame 87: holes 0, rim-vs-core 0.49, rim-vs-outside 1.19, heterogeneity 0.18; core [0.097, 0.767, 0.695, 0.887, 0.515] rim [0.288, 0.395, 0.651, 0.734, 0.717]
  - track 18 at frame 89: holes 0, rim-vs-core 0.50, rim-vs-outside 1.20, heterogeneity 0.18; core [0.097, 0.771, 0.691, 0.894, 0.503] rim [0.287, 0.407, 0.636, 0.75, 0.734]
  - track 73 at frame 130: holes 1, rim-vs-core 0.31, rim-vs-outside 1.11, heterogeneity 0.18; core [0.111, 0.762, 0.71, 0.879, 0.625] rim [0.221, 0.506, 0.658, 0.756, 0.589]

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, lineage.png, timeseries.png, movie.mp4, metrics.json

Measurements are screens, not verdicts: judge them against the images.
