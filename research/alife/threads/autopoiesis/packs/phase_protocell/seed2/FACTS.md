# Evidence pack: phase-protocell (seed 2)

- world: `../../../worlds/phase_protocell/world.py`, family `autopoiesis`
- parent: threads/autopoiesis/worlds/gated_protocell; mutation: membrane is an Allen-Cahn domain wall (always closed) instead of a polymerized field; the inside phase is tilted by catalyst-made links; K and L mobility ~ phi^2
- run: 161 frames x 50 steps x dt 1.0 = time 8000; grid [128, 128]; wall 9s; status ok
- command: `python -m labkit.run threads/autopoiesis/worlds/phase_protocell/world.py --out threads/autopoiesis/packs/phase_protocell --seeds 0 1 2 --frames 160`
- segmentation: matter > 0.35 of robust range [0.0, 1.5275], min area 6 px

## Measurements
- components: final 36, mean 19.1, max 36; occupancy final 0.36
- tracks: 67; persistent (alive >= 50% of run): 9; longest 92 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 2.16 (1 = constant size)
- enclosures: components with a hole mean 1.63, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 18]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [37, 36, 36], H1 [36, 33, 0]
- motion: 0 long-lived tracks moved >= 1 body length; max speed 0/time; max body lengths 0.9
- replication: splits 31, persistent splits 22, max generation 2, merges 0, nucleations 0
- channel total drift (end/start - 1): [-0.5188, 14.4171, 9.4771, 8.5305]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 23 at frame 114: holes 0, rim-vs-core 0.47, rim-vs-outside 1.02, heterogeneity 0.19; core [0.085, 0.889, 0.801, 0.58] rim [0.288, 0.487, 0.728, 0.693]
  - track 24 at frame 114: holes 0, rim-vs-core 0.45, rim-vs-outside 1.00, heterogeneity 0.19; core [0.091, 0.873, 0.799, 0.638] rim [0.285, 0.475, 0.719, 0.688]
  - track 25 at frame 116: holes 0, rim-vs-core 0.35, rim-vs-outside 1.08, heterogeneity 0.19; core [0.083, 0.871, 0.784, 0.615] rim [0.239, 0.578, 0.749, 0.703]
  - track 31 at frame 117: holes 0, rim-vs-core 0.30, rim-vs-outside 1.09, heterogeneity 0.18; core [0.115, 0.879, 0.846, 0.739] rim [0.207, 0.623, 0.748, 0.659]

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, lineage.png, timeseries.png, movie.mp4, metrics.json

Measurements are screens, not verdicts: judge them against the images.
