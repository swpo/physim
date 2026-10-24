# Evidence pack: phase-trait-c20 (seed 1)

- world: `../../../worlds/phase_trait_c20/world.py`, family `autopoiesis`
- parent: threads/autopoiesis/worlds/phase_trait; mutation: same as phase_trait, ancestral trait c0 = 0.20 instead of 0.15 (convergence test)
- run: 161 frames x 300 steps x dt 1.0 = time 48000; grid [128, 128]; wall 68s; status ok
- command: `python -m labkit.run threads/autopoiesis/worlds/phase_trait_c20/world.py --out threads/autopoiesis/packs/phase_trait_c20 --seeds 0 1 2 --frames 160 --spf 300`
- segmentation: matter > 0.35 of robust range [0.0, 1.5614], min area 6 px

## Measurements
- components: final 42, mean 37.3, max 45; occupancy final 0.38
- tracks: 117; persistent (alive >= 50% of run): 36; longest 151 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 4.33 (1 = constant size)
- enclosures: components with a hole mean 3.35, final 2; holes at thresholds 0.2/0.35/0.5 final [0, 2, 29]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [42, 42, 42], H1 [43, 37, 0]
- motion: 2 long-lived tracks moved >= 1 body length; max speed 0.00285/time; max body lengths 1.4
- replication: splits 57, persistent splits 36, max generation 3, merges 0, nucleations 0
- channel total drift (end/start - 1): [-0.5328, 14.0801, 27.2275, 10.4372, 10.2483]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 21 at frame 86: holes 0, rim-vs-core 0.27, rim-vs-outside 1.37, heterogeneity 0.16; core [0.098, 0.818, 0.839, 0.902, 0.75] rim [0.183, 0.604, 0.83, 0.811, 0.642]
  - track 26 at frame 87: holes 0, rim-vs-core 0.61, rim-vs-outside 1.21, heterogeneity 0.14; core [0.109, 0.903, 0.99, 0.915, 0.779] rim [0.293, 0.405, 0.99, 0.726, 0.548]
  - track 31 at frame 87: holes 0, rim-vs-core 0.67, rim-vs-outside 1.20, heterogeneity 0.15; core [0.115, 0.902, 1.0, 0.924, 0.787] rim [0.299, 0.374, 1.0, 0.682, 0.514]
  - track 67 at frame 94: holes 0, rim-vs-core 0.67, rim-vs-outside 1.23, heterogeneity 0.15; core [0.122, 0.895, 0.99, 0.945, 0.797] rim [0.295, 0.373, 0.99, 0.678, 0.519]

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, lineage.png, timeseries.png, movie.mp4, metrics.json

Measurements are screens, not verdicts: judge them against the images.
