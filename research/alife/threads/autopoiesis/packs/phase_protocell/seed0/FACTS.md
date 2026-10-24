# Evidence pack: phase-protocell (seed 0)

- world: `../../../worlds/phase_protocell/world.py`, family `autopoiesis`
- parent: threads/autopoiesis/worlds/gated_protocell; mutation: membrane is an Allen-Cahn domain wall (always closed) instead of a polymerized field; the inside phase is tilted by catalyst-made links; K and L mobility ~ phi^2
- run: 161 frames x 50 steps x dt 1.0 = time 8000; grid [128, 128]; wall 9s; status ok
- command: `python -m labkit.run threads/autopoiesis/worlds/phase_protocell/world.py --out threads/autopoiesis/packs/phase_protocell --seeds 0 1 2 --frames 160`
- segmentation: matter > 0.35 of robust range [0.0, 1.5282], min area 6 px

## Measurements
- components: final 43, mean 20.3, max 43; occupancy final 0.36
- tracks: 80; persistent (alive >= 50% of run): 3; longest 94 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 2.05 (1 = constant size)
- enclosures: components with a hole mean 1.88, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 13]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [43, 43, 43], H1 [43, 42, 0]
- motion: 0 long-lived tracks moved >= 1 body length; max speed 0/time; max body lengths 0.8
- replication: splits 37, persistent splits 32, max generation 5, merges 0, nucleations 0
- channel total drift (end/start - 1): [-0.5236, 14.5465, 9.7447, 8.6603]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 23 at frame 114: holes 0, rim-vs-core 0.44, rim-vs-outside 1.06, heterogeneity 0.18; core [0.083, 0.877, 0.783, 0.582] rim [0.276, 0.517, 0.745, 0.734]
  - track 24 at frame 116: holes 0, rim-vs-core 0.32, rim-vs-outside 1.10, heterogeneity 0.19; core [0.09, 0.894, 0.813, 0.575] rim [0.219, 0.631, 0.761, 0.679]
  - track 27 at frame 116: holes 0, rim-vs-core 0.48, rim-vs-outside 1.02, heterogeneity 0.19; core [0.101, 0.909, 0.853, 0.631] rim [0.288, 0.492, 0.738, 0.701]
  - track 60 at frame 148: holes 0, rim-vs-core 0.51, rim-vs-outside 1.02, heterogeneity 0.19; core [0.11, 0.927, 0.892, 0.67] rim [0.283, 0.48, 0.729, 0.681]

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, lineage.png, timeseries.png, movie.mp4, metrics.json

Measurements are screens, not verdicts: judge them against the images.
