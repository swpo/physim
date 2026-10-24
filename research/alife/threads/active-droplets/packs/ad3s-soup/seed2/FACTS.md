# Evidence pack: ad3s-soup (seed 2)

- world: `../../../worlds/ad3s-soup/world.py`, family `phase-field`
- parent: ad3-membrane; mutation: unstructured start: 8 random blobs of random radius (1.5-6) and amplitude instead of 2 planted disks
- run: 201 frames x 200 steps x dt 0.5 = time 20000; grid [128, 128]; wall 179s; status ok
- command: `python -m labkit.run threads/active-droplets/worlds/ad3s-soup/world.py --out threads/active-droplets/packs/ad3s-soup --seeds 0 1 2 --frames 200`
- segmentation: matter > 0.35 of robust range [-1.0429, 1.2196], min area 6 px

## Measurements
- components: final 15, mean 13.5, max 15; occupancy final 0.14
- tracks: 26; persistent (alive >= 50% of run): 15; longest 197 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 1.35 (1 = constant size)
- enclosures: components with a hole mean 0.09, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [15, 15, 15], H1 [0, 0, 0]
- motion: 1 long-lived tracks moved >= 1 body length; max speed 0.000858/time; max body lengths 1.1
- replication: splits 9, persistent splits 8, max generation 2, merges 1, nucleations 0
- channel total drift (end/start - 1): [0.1695, -0.624, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 9 at frame 103: holes 0, rim-vs-core 0.62, rim-vs-outside 0.64, heterogeneity 0.18; core [0.963, 0.023, 0.194] rim [0.645, 0.093, 0.726]
  - track 10 at frame 113: holes 0, rim-vs-core 0.61, rim-vs-outside 0.64, heterogeneity 0.18; core [0.97, 0.027, 0.18] rim [0.634, 0.089, 0.688]
  - track 11 at frame 113: holes 0, rim-vs-core 0.64, rim-vs-outside 0.65, heterogeneity 0.18; core [0.969, 0.031, 0.177] rim [0.611, 0.092, 0.698]
  - track 22 at frame 121: holes 0, rim-vs-core 0.63, rim-vs-outside 0.65, heterogeneity 0.18; core [0.968, 0.026, 0.184] rim [0.625, 0.092, 0.71]

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, lineage.png, timeseries.png, movie.mp4, metrics.json

Measurements are screens, not verdicts: judge them against the images.
