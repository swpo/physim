# Evidence pack: ad3s-soup (seed 1)

- world: `../../../worlds/ad3s-soup/world.py`, family `phase-field`
- parent: ad3-membrane; mutation: unstructured start: 8 random blobs of random radius (1.5-6) and amplitude instead of 2 planted disks
- run: 201 frames x 200 steps x dt 0.5 = time 20000; grid [128, 128]; wall 178s; status ok
- command: `python -m labkit.run threads/active-droplets/worlds/ad3s-soup/world.py --out threads/active-droplets/packs/ad3s-soup --seeds 0 1 2 --frames 200`
- segmentation: matter > 0.35 of robust range [-1.0442, 1.2281], min area 6 px

## Measurements
- components: final 17, mean 14.3, max 17; occupancy final 0.14
- tracks: 30; persistent (alive >= 50% of run): 16; longest 174 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 6.16 (1 = constant size)
- enclosures: components with a hole mean 0.03, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [17, 17, 17], H1 [0, 0, 0]
- motion: 2 long-lived tracks moved >= 1 body length; max speed 0.000938/time; max body lengths 1.1
- replication: splits 11, persistent splits 10, max generation 2, merges 1, nucleations 0
- channel total drift (end/start - 1): [0.187, -0.6364, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 10 at frame 114: holes 0, rim-vs-core 0.67, rim-vs-outside 0.66, heterogeneity 0.19; core [0.945, 0.026, 0.191] rim [0.59, 0.092, 0.755]
  - track 12 at frame 114: holes 0, rim-vs-core 0.63, rim-vs-outside 0.65, heterogeneity 0.18; core [0.965, 0.024, 0.186] rim [0.612, 0.089, 0.708]
  - track 13 at frame 114: holes 0, rim-vs-core 0.64, rim-vs-outside 0.66, heterogeneity 0.18; core [0.964, 0.025, 0.186] rim [0.611, 0.09, 0.721]
  - track 22 at frame 131: holes 0, rim-vs-core 0.63, rim-vs-outside 0.65, heterogeneity 0.18; core [0.969, 0.028, 0.176] rim [0.62, 0.087, 0.694]

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, lineage.png, timeseries.png, movie.mp4, metrics.json

Measurements are screens, not verdicts: judge them against the images.
