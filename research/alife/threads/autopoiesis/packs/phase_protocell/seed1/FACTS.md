# Evidence pack: phase-protocell (seed 1)

- world: `../../../worlds/phase_protocell/world.py`, family `autopoiesis`
- parent: threads/autopoiesis/worlds/gated_protocell; mutation: membrane is an Allen-Cahn domain wall (always closed) instead of a polymerized field; the inside phase is tilted by catalyst-made links; K and L mobility ~ phi^2
- run: 161 frames x 50 steps x dt 1.0 = time 8000; grid [128, 128]; wall 9s; status ok
- command: `python -m labkit.run threads/autopoiesis/worlds/phase_protocell/world.py --out threads/autopoiesis/packs/phase_protocell --seeds 0 1 2 --frames 160`
- segmentation: matter > 0.35 of robust range [0.0, 1.528], min area 6 px

## Measurements
- components: final 43, mean 18.2, max 43; occupancy final 0.36
- tracks: 81; persistent (alive >= 50% of run): 2; longest 101 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 1.74 (1 = constant size)
- enclosures: components with a hole mean 2.45, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 9]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [44, 43, 43], H1 [46, 40, 0]
- motion: 1 long-lived tracks moved >= 1 body length; max speed 0.00421/time; max body lengths 1.2
- replication: splits 38, persistent splits 33, max generation 4, merges 0, nucleations 0
- channel total drift (end/start - 1): [-0.523, 14.4092, 9.7661, 9.96]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 8 at frame 87: holes 0, rim-vs-core 0.28, rim-vs-outside 1.05, heterogeneity 0.20; core [0.105, 0.865, 0.796, 0.68] rim [0.205, 0.634, 0.73, 0.585]
  - track 24 at frame 116: holes 1, rim-vs-core 0.32, rim-vs-outside 0.85, heterogeneity 0.19; core [0.098, 0.838, 0.75, 0.664] rim [0.228, 0.568, 0.692, 0.554]
  - track 27 at frame 125: holes 0, rim-vs-core 0.37, rim-vs-outside 0.96, heterogeneity 0.19; core [0.091, 0.855, 0.764, 0.61] rim [0.261, 0.53, 0.724, 0.609]
  - track 41 at frame 132: holes 0, rim-vs-core 0.46, rim-vs-outside 1.03, heterogeneity 0.19; core [0.093, 0.893, 0.822, 0.618] rim [0.281, 0.496, 0.733, 0.705]

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, lineage.png, timeseries.png, movie.mp4, metrics.json

Measurements are screens, not verdicts: judge them against the images.
