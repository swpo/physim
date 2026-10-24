# Evidence pack: ad3s-soup (seed 0)

- world: `../../../worlds/ad3s-soup/world.py`, family `phase-field`
- parent: ad3-membrane; mutation: unstructured start: 8 random blobs of random radius (1.5-6) and amplitude instead of 2 planted disks
- run: 201 frames x 200 steps x dt 0.5 = time 20000; grid [128, 128]; wall 199s; status ok
- command: `python -m labkit.run threads/active-droplets/worlds/ad3s-soup/world.py --out threads/active-droplets/packs/ad3s-soup --seeds 0 1 2 --frames 200`
- segmentation: matter > 0.35 of robust range [-1.0448, 1.2294], min area 6 px

## Measurements
- components: final 18, mean 14.6, max 18; occupancy final 0.14
- tracks: 30; persistent (alive >= 50% of run): 17; longest 170 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 1.51 (1 = constant size)
- enclosures: components with a hole mean 0.18, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [18, 18, 18], H1 [0, 0, 0]
- motion: 3 long-lived tracks moved >= 1 body length; max speed 0.00101/time; max body lengths 1.3
- replication: splits 12, persistent splits 12, max generation 3, merges 0, nucleations 1
- channel total drift (end/start - 1): [0.1804, -0.6404, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 10 at frame 116: holes 0, rim-vs-core 0.63, rim-vs-outside 0.65, heterogeneity 0.18; core [0.966, 0.026, 0.182] rim [0.617, 0.084, 0.701]
  - track 11 at frame 116: holes 0, rim-vs-core 0.64, rim-vs-outside 0.65, heterogeneity 0.18; core [0.968, 0.025, 0.179] rim [0.623, 0.085, 0.712]
  - track 13 at frame 118: holes 0, rim-vs-core 0.65, rim-vs-outside 0.66, heterogeneity 0.18; core [0.966, 0.026, 0.181] rim [0.608, 0.087, 0.721]
  - track 24 at frame 136: holes 0, rim-vs-core 0.65, rim-vs-outside 0.65, heterogeneity 0.18; core [0.96, 0.021, 0.198] rim [0.622, 0.088, 0.749]

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, lineage.png, timeseries.png, movie.mp4, metrics.json

Measurements are screens, not verdicts: judge them against the images.
