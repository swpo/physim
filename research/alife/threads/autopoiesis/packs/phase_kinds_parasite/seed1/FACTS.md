# Evidence pack: phase-kinds-parasite (seed 1)

- world: `../../../worlds/phase_kinds_parasite/world.py`, family `autopoiesis`
- parent: threads/autopoiesis/worlds/phase_kinds; mutation: mutant kind K2 is selfish: faster (c2=0.3 vs 0.2) but makes no links (b2=0)
- run: 161 frames x 200 steps x dt 1.0 = time 32000; grid [128, 128]; wall 48s; status ok
- command: `python -m labkit.run threads/autopoiesis/worlds/phase_kinds_parasite/world.py --out threads/autopoiesis/packs/phase_kinds_parasite --seeds 0 1 2 --frames 160 --spf 200`
- segmentation: matter > 0.35 of robust range [0.0, 1.5246], min area 6 px

## Measurements
- components: final 0, mean 19.6, max 47; occupancy final 0.00
- tracks: 153; persistent (alive >= 50% of run): 2; longest 88 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 20.31 (1 = constant size)
- enclosures: components with a hole mean 1.11, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [0, 0, 0], H1 [0, 0, 0]
- motion: 12 long-lived tracks moved >= 1 body length; max speed 0.00462/time; max body lengths 1.7
- replication: splits 74, persistent splits 35, max generation 4, merges 0, nucleations 0
- channel total drift (end/start - 1): [0.006, -1.0, None, -1.0, -1.0]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 61 at frame 79: holes 0, rim-vs-core 0.51, rim-vs-outside 1.02, heterogeneity 0.16; core [0.089, 0.929, 0.0, 0.879, 0.635] rim [0.278, 0.484, 0.0, 0.738, 0.682]
  - track 62 at frame 77: holes 0, rim-vs-core 0.47, rim-vs-outside 1.07, heterogeneity 0.15; core [0.086, 0.936, 0.0, 0.881, 0.617] rim [0.267, 0.528, 0.0, 0.774, 0.724]
  - track 31 at frame 62: holes 0, rim-vs-core 0.47, rim-vs-outside 1.06, heterogeneity 0.15; core [0.079, 0.92, 0.0, 0.847, 0.596] rim [0.272, 0.516, 0.0, 0.763, 0.716]
  - track 77 at frame 67: holes 0, rim-vs-core 0.48, rim-vs-outside 1.06, heterogeneity 0.15; core [0.082, 0.926, 0.0, 0.86, 0.603] rim [0.272, 0.516, 0.0, 0.762, 0.716]

## Warnings
- no components at the end: matter died out or fell below threshold
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, lineage.png, timeseries.png, movie.mp4, metrics.json

Measurements are screens, not verdicts: judge them against the images.
