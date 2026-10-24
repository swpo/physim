# Evidence pack: phase-swim (seed 2)

- world: `../../../worlds/phase_swim/world.py`, family `autopoiesis`
- parent: threads/autopoiesis/worlds/phase_protocell; mutation: rigid-droplet phoresis: each cell advected with mu * cell-mean grad S; parent: membrane is an Allen-Cahn domain wall (always closed) instead of a polymerized field; the inside phase is tilted by catalyst-made links; K and L mobility ~ phi^2
- run: 121 frames x 50 steps x dt 1.0 = time 6000; grid [128, 128]; wall 20s; status ok
- command: `python -m labkit.run threads/autopoiesis/worlds/phase_swim/world.py --out threads/autopoiesis/packs/phase_swim --seeds 0 1 2 --frames 120`
- segmentation: matter > 0.35 of robust range [0.0, 1.5783], min area 6 px

## Measurements
- components: final 1, mean 1.0, max 1; occupancy final 0.13
- tracks: 1; persistent (alive >= 50% of run): 1; longest 121 frames; alive start-to-end: 1
- size of persistent tracks: max/min area ratio 15.04 (1 = constant size)
- enclosures: components with a hole mean 0.95, final 1; holes at thresholds 0.2/0.35/0.5 final [0, 1, 1]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [1, 1, 1], H1 [1, 1, 0]
- motion: 1 long-lived tracks moved >= 1 body length; max speed 0.1/time; max body lengths 18.5
- replication: splits 0, persistent splits 0, max generation 0, merges 0, nucleations 0
- channel total drift (end/start - 1): [-0.2546, 30.4353, 19.1117, 8.0988]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 0 at frame 61: holes 1, rim-vs-core 0.39, rim-vs-outside 0.92, heterogeneity 0.26; core [0.047, 0.736, 0.608, 0.164] rim [0.198, 0.617, 0.594, 0.502]

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, lineage.png, timeseries.png, movie.mp4, metrics.json

Measurements are screens, not verdicts: judge them against the images.
