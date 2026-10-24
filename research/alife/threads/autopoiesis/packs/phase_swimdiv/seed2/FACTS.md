# Evidence pack: phase-swimdiv (seed 2)

- world: `../../../worlds/phase_swimdiv/world.py`, family `autopoiesis`
- parent: threads/autopoiesis/worlds/phase_swim; mutation: phoretic mobility lowered to mu=1.5 (near threshold): cells swim AND divide
- run: 161 frames x 50 steps x dt 1.0 = time 8000; grid [128, 128]; wall 27s; status ok
- command: `python -m labkit.run threads/autopoiesis/worlds/phase_swimdiv/world.py --out threads/autopoiesis/packs/phase_swimdiv --seeds 0 1 2 --frames 160`
- segmentation: matter > 0.35 of robust range [0.0, 1.5467], min area 6 px

## Measurements
- components: final 6, mean 4.1, max 7; occupancy final 0.17
- tracks: 48; persistent (alive >= 50% of run): 0; longest 48 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 0.00 (1 = constant size)
- enclosures: components with a hole mean 1.22, final 3; holes at thresholds 0.2/0.35/0.5 final [0, 3, 7]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [7, 7, 6], H1 [7, 7, 3]
- motion: 18 long-lived tracks moved >= 1 body length; max speed 0.0741/time; max body lengths 7.7
- replication: splits 17, persistent splits 4, max generation 3, merges 12, nucleations 0
- channel total drift (end/start - 1): [-0.2749, 31.463, 20.5405, 13.676]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 0 at frame 24: holes 1, rim-vs-core 0.25, rim-vs-outside 0.82, heterogeneity 0.19; core [0.115, 0.73, 0.658, 0.757] rim [0.184, 0.578, 0.596, 0.585]
  - track 30 at frame 136: holes 0, rim-vs-core 0.42, rim-vs-outside 0.99, heterogeneity 0.25; core [0.063, 0.843, 0.752, 0.342] rim [0.238, 0.593, 0.646, 0.613]
  - track 26 at frame 116: holes 0, rim-vs-core 0.46, rim-vs-outside 0.89, heterogeneity 0.24; core [0.108, 0.855, 0.81, 0.44] rim [0.285, 0.514, 0.609, 0.608]
  - track 36 at frame 151: holes 0, rim-vs-core 0.58, rim-vs-outside 1.01, heterogeneity 0.24; core [0.057, 0.823, 0.721, 0.342] rim [0.319, 0.512, 0.646, 0.742]

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, lineage.png, timeseries.png, movie.mp4, metrics.json

Measurements are screens, not verdicts: judge them against the images.
