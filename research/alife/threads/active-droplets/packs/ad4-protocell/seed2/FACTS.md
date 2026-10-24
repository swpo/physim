# Evidence pack: ad4-protocell (seed 2)

- world: `../../../worlds/ad4-protocell/world.py`, family `phase-field`
- parent: ad2-catalysts + ad3-membrane; mutation: merge: catalyst-driven production (heredity) with amphiphile synthesis and interface binding (membrane)
- run: 201 frames x 200 steps x dt 0.5 = time 20000; grid [128, 128]; wall 238s; status ok
- command: `python -m labkit.run threads/active-droplets/worlds/ad4-protocell/world.py --out threads/active-droplets/packs/ad4-protocell --seeds 0 1 2 --frames 200`
- segmentation: matter > 0.35 of robust range [-1.0638, 1.4285], min area 6 px

## Measurements
- components: final 11, mean 9.8, max 11; occupancy final 0.13
- tracks: 16; persistent (alive >= 50% of run): 11; longest 201 frames; alive start-to-end: 2
- size of persistent tracks: max/min area ratio 2.64 (1 = constant size)
- enclosures: components with a hole mean 0.12, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [11, 11, 11], H1 [0, 0, 0]
- motion: 5 long-lived tracks moved >= 1 body length; max speed 0.00266/time; max body lengths 1.5
- replication: splits 5, persistent splits 5, max generation 2, merges 0, nucleations 0
- channel total drift (end/start - 1): [0.1009, -0.5986, 2.9678, 0.6807, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 1 at frame 101: holes 0, rim-vs-core 0.66, rim-vs-outside 0.78, heterogeneity 0.16; core [0.959, 0.072, 0.0, 0.948, 0.178] rim [0.662, 0.16, 0.0, 0.586, 0.63]
  - track 3 at frame 101: holes 0, rim-vs-core 0.72, rim-vs-outside 0.74, heterogeneity 0.15; core [0.963, 0.093, 0.0, 0.931, 0.145] rim [0.632, 0.168, 0.0, 0.533, 0.638]
  - track 7 at frame 111: holes 0, rim-vs-core 0.74, rim-vs-outside 0.74, heterogeneity 0.15; core [0.952, 0.028, 0.938, 0.0, 0.168] rim [0.634, 0.115, 0.537, 0.0, 0.698]
  - track 12 at frame 129: holes 0, rim-vs-core 0.55, rim-vs-outside 0.81, heterogeneity 0.15; core [0.958, 0.023, 0.952, 0.0, 0.173] rim [0.719, 0.093, 0.645, 0.0, 0.549]

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, lineage.png, timeseries.png, movie.mp4, metrics.json

Measurements are screens, not verdicts: judge them against the images.
