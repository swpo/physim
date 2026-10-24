# Evidence pack: phase-swimdiv (seed 0)

- world: `../../../worlds/phase_swimdiv/world.py`, family `autopoiesis`
- parent: threads/autopoiesis/worlds/phase_swim; mutation: phoretic mobility lowered to mu=1.5 (near threshold): cells swim AND divide
- run: 161 frames x 50 steps x dt 1.0 = time 8000; grid [128, 128]; wall 27s; status ok
- command: `python -m labkit.run threads/autopoiesis/worlds/phase_swimdiv/world.py --out threads/autopoiesis/packs/phase_swimdiv --seeds 0 1 2 --frames 160`
- segmentation: matter > 0.35 of robust range [0.0, 1.5441], min area 6 px

## Measurements
- components: final 12, mean 5.5, max 12; occupancy final 0.19
- tracks: 71; persistent (alive >= 50% of run): 0; longest 48 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 0.00 (1 = constant size)
- enclosures: components with a hole mean 1.57, final 3; holes at thresholds 0.2/0.35/0.5 final [0, 3, 13]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [12, 12, 12], H1 [13, 13, 2]
- motion: 24 long-lived tracks moved >= 1 body length; max speed 0.0605/time; max body lengths 5.1
- replication: splits 26, persistent splits 1, max generation 1, merges 15, nucleations 0
- channel total drift (end/start - 1): [-0.3021, 35.5891, 23.7253, 17.1231]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 0 at frame 24: holes 1, rim-vs-core 0.25, rim-vs-outside 0.83, heterogeneity 0.19; core [0.111, 0.756, 0.679, 0.755] rim [0.181, 0.598, 0.614, 0.583]
  - track 20 at frame 109: holes 0, rim-vs-core 0.58, rim-vs-outside 1.02, heterogeneity 0.23; core [0.055, 0.855, 0.747, 0.357] rim [0.303, 0.514, 0.642, 0.748]
  - track 40 at frame 143: holes 0, rim-vs-core 0.53, rim-vs-outside 0.86, heterogeneity 0.21; core [0.111, 0.854, 0.821, 0.569] rim [0.349, 0.425, 0.64, 0.679]
  - track 23 at frame 109: holes 0, rim-vs-core 0.44, rim-vs-outside 0.99, heterogeneity 0.21; core [0.049, 0.811, 0.694, 0.387] rim [0.236, 0.55, 0.641, 0.684]

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, lineage.png, timeseries.png, movie.mp4, metrics.json

Measurements are screens, not verdicts: judge them against the images.
