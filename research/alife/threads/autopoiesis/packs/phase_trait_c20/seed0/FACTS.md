# Evidence pack: phase-trait-c20 (seed 0)

- world: `../../../worlds/phase_trait_c20/world.py`, family `autopoiesis`
- parent: threads/autopoiesis/worlds/phase_trait; mutation: same as phase_trait, ancestral trait c0 = 0.20 instead of 0.15 (convergence test)
- run: 161 frames x 300 steps x dt 1.0 = time 48000; grid [128, 128]; wall 67s; status ok
- command: `python -m labkit.run threads/autopoiesis/worlds/phase_trait_c20/world.py --out threads/autopoiesis/packs/phase_trait_c20 --seeds 0 1 2 --frames 160 --spf 300`
- segmentation: matter > 0.35 of robust range [0.0, 1.5393], min area 6 px

## Measurements
- components: final 42, mean 37.0, max 43; occupancy final 0.38
- tracks: 112; persistent (alive >= 50% of run): 34; longest 147 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 3.08 (1 = constant size)
- enclosures: components with a hole mean 4.35, final 4; holes at thresholds 0.2/0.35/0.5 final [0, 4, 26]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [42, 42, 42], H1 [42, 41, 0]
- motion: 2 long-lived tracks moved >= 1 body length; max speed 0.000878/time; max body lengths 1.2
- replication: splits 53, persistent splits 39, max generation 6, merges 0, nucleations 0
- channel total drift (end/start - 1): [-0.5307, 13.8195, 26.6391, 10.526, 8.9827]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 26 at frame 87: holes 1, rim-vs-core 0.33, rim-vs-outside 1.10, heterogeneity 0.18; core [0.119, 0.706, 0.685, 0.869, 0.613] rim [0.244, 0.442, 0.624, 0.732, 0.592]
  - track 33 at frame 87: holes 0, rim-vs-core 0.45, rim-vs-outside 1.38, heterogeneity 0.16; core [0.069, 0.894, 0.894, 0.847, 0.603] rim [0.265, 0.509, 0.881, 0.776, 0.717]
  - track 35 at frame 89: holes 0, rim-vs-core 0.45, rim-vs-outside 1.35, heterogeneity 0.17; core [0.07, 0.878, 0.894, 0.835, 0.63] rim [0.265, 0.487, 0.882, 0.751, 0.695]
  - track 106 at frame 138: holes 0, rim-vs-core 0.47, rim-vs-outside 1.29, heterogeneity 0.17; core [0.093, 0.838, 0.804, 0.906, 0.612] rim [0.272, 0.445, 0.791, 0.757, 0.707]

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, lineage.png, timeseries.png, movie.mp4, metrics.json

Measurements are screens, not verdicts: judge them against the images.
