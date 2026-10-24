# Evidence pack: phase-swimdiv (seed 1)

- world: `../../worlds/phase_swimdiv/world.py`, family `autopoiesis`
- parent: threads/autopoiesis/worlds/phase_swim; mutation: phoretic mobility lowered to mu=1.5 (near threshold): cells swim AND divide
- run: 241 frames x 50 steps x dt 1.0 = time 12000; grid [192, 192]; wall 75s; status ok
- command: `python -m labkit.run threads/autopoiesis/worlds/phase_swimdiv/world.py --out threads/autopoiesis/packs/phase_swimdiv_movie --seeds 1 --size 192 192 --frames 240`
- segmentation: matter > 0.35 of robust range [0.0, 1.5062], min area 6 px

## Measurements
- components: final 1, mean 2.3, max 10; occupancy final 0.03
- tracks: 43; persistent (alive >= 50% of run): 1; longest 126 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 14.21 (1 = constant size)
- enclosures: components with a hole mean 0.69, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 1]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [1, 1, 1], H1 [1, 1, 0]
- motion: 5 long-lived tracks moved >= 1 body length; max speed 0.0527/time; max body lengths 13.2
- replication: splits 11, persistent splits 1, max generation 1, merges 11, nucleations 0
- channel total drift (end/start - 1): [-0.0473, 12.085, 7.5202, 4.6282]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 39 at frame 177: holes 0, rim-vs-core 0.64, rim-vs-outside 1.19, heterogeneity 0.24; core [0.005, 0.93, 0.825, 0.245] rim [0.196, 0.653, 0.744, 0.784]
  - track 0 at frame 24: holes 1, rim-vs-core 0.31, rim-vs-outside 0.91, heterogeneity 0.21; core [0.044, 0.842, 0.782, 0.845] rim [0.136, 0.66, 0.7, 0.621]
  - track 1 at frame 65: holes 1, rim-vs-core 0.34, rim-vs-outside 1.05, heterogeneity 0.24; core [0.026, 0.912, 0.838, 0.503] rim [0.176, 0.665, 0.738, 0.643]
  - track 2 at frame 65: holes 1, rim-vs-core 0.31, rim-vs-outside 1.06, heterogeneity 0.23; core [0.023, 0.902, 0.82, 0.503] rim [0.172, 0.679, 0.749, 0.646]

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, lineage.png, timeseries.png, movie.mp4, metrics.json

Measurements are screens, not verdicts: judge them against the images.
