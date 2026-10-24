# Evidence pack: phase-trait-c20 (seed 2)

- world: `../../../worlds/phase_trait_c20/world.py`, family `autopoiesis`
- parent: threads/autopoiesis/worlds/phase_trait; mutation: same as phase_trait, ancestral trait c0 = 0.20 instead of 0.15 (convergence test)
- run: 161 frames x 300 steps x dt 1.0 = time 48000; grid [128, 128]; wall 72s; status ok
- command: `python -m labkit.run threads/autopoiesis/worlds/phase_trait_c20/world.py --out threads/autopoiesis/packs/phase_trait_c20 --seeds 0 1 2 --frames 160 --spf 300`
- segmentation: matter > 0.35 of robust range [0.0, 1.5421], min area 6 px

## Measurements
- components: final 37, mean 36.9, max 44; occupancy final 0.37
- tracks: 99; persistent (alive >= 50% of run): 38; longest 149 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 3.75 (1 = constant size)
- enclosures: components with a hole mean 4.07, final 9; holes at thresholds 0.2/0.35/0.5 final [0, 9, 31]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [37, 37, 37], H1 [38, 38, 0]
- motion: 2 long-lived tracks moved >= 1 body length; max speed 0.000744/time; max body lengths 1.3
- replication: splits 46, persistent splits 39, max generation 5, merges 0, nucleations 0
- channel total drift (end/start - 1): [-0.5201, 13.6339, 26.1426, 10.1837, 8.673]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 17 at frame 86: holes 0, rim-vs-core 0.23, rim-vs-outside 1.15, heterogeneity 0.16; core [0.157, 0.618, 0.589, 0.931, 0.614] rim [0.243, 0.444, 0.562, 0.811, 0.612]
  - track 30 at frame 87: holes 0, rim-vs-core 0.47, rim-vs-outside 1.06, heterogeneity 0.17; core [0.186, 0.576, 0.512, 0.991, 0.521] rim [0.338, 0.294, 0.424, 0.751, 0.748]
  - track 34 at frame 87: holes 0, rim-vs-core 0.43, rim-vs-outside 1.35, heterogeneity 0.14; core [0.07, 0.831, 0.877, 0.826, 0.61] rim [0.269, 0.468, 0.877, 0.774, 0.7]
  - track 87 at frame 112: holes 0, rim-vs-core 0.45, rim-vs-outside 1.25, heterogeneity 0.15; core [0.094, 0.742, 0.719, 0.894, 0.516] rim [0.27, 0.436, 0.698, 0.799, 0.778]

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, lineage.png, timeseries.png, movie.mp4, metrics.json

Measurements are screens, not verdicts: judge them against the images.
