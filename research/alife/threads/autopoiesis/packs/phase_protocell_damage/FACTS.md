# Evidence pack: phase-protocell (seed 0)

- world: `../../worlds/phase_protocell/world.py`, family `autopoiesis`
- parent: threads/autopoiesis/worlds/gated_protocell; mutation: membrane is an Allen-Cahn domain wall (always closed) instead of a polymerized field; the inside phase is tilted by catalyst-made links; K and L mobility ~ phi^2
- run: 161 frames x 50 steps x dt 1.0 = time 8000; grid [128, 128]; wall 9s; status ok
- command: `python -m labkit.run threads/autopoiesis/worlds/phase_protocell/world.py --out threads/autopoiesis/packs/phase_protocell_damage --frames 160 --damage 30:0.3`
- segmentation: matter > 0.35 of robust range [0.0, 1.5285], min area 6 px

## Measurements
- components: final 40, mean 20.2, max 40; occupancy final 0.36
- tracks: 74; persistent (alive >= 50% of run): 3; longest 91 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 1.77 (1 = constant size)
- enclosures: components with a hole mean 2.06, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 12]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [40, 40, 40], H1 [42, 38, 0]
- motion: 0 long-lived tracks moved >= 1 body length; max speed 0/time; max body lengths 0.8
- replication: splits 34, persistent splits 31, max generation 5, merges 0, nucleations 0
- channel total drift (end/start - 1): [-0.5221, 14.3458, 9.625, 8.6322]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 25 at frame 116: holes 0, rim-vs-core 0.48, rim-vs-outside 1.06, heterogeneity 0.19; core [0.097, 0.928, 0.867, 0.597] rim [0.28, 0.522, 0.756, 0.732]
  - track 26 at frame 116: holes 0, rim-vs-core 0.34, rim-vs-outside 1.10, heterogeneity 0.20; core [0.088, 0.9, 0.816, 0.553] rim [0.228, 0.617, 0.753, 0.677]
  - track 29 at frame 116: holes 0, rim-vs-core 0.44, rim-vs-outside 0.97, heterogeneity 0.19; core [0.09, 0.84, 0.759, 0.639] rim [0.292, 0.453, 0.708, 0.665]
  - track 62 at frame 151: holes 0, rim-vs-core 0.52, rim-vs-outside 1.02, heterogeneity 0.20; core [0.108, 0.932, 0.897, 0.658] rim [0.281, 0.48, 0.716, 0.683]
- damage applied at frame 30: erased 49 px of a 475 px component

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, lineage.png, timeseries.png, movie.mp4, metrics.json

Measurements are screens, not verdicts: judge them against the images.
