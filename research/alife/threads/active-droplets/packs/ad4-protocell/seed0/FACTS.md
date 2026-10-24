# Evidence pack: ad4-protocell (seed 0)

- world: `../../../worlds/ad4-protocell/world.py`, family `phase-field`
- parent: ad2-catalysts + ad3-membrane; mutation: merge: catalyst-driven production (heredity) with amphiphile synthesis and interface binding (membrane)
- run: 201 frames x 200 steps x dt 0.5 = time 20000; grid [128, 128]; wall 239s; status ok
- command: `python -m labkit.run threads/active-droplets/worlds/ad4-protocell/world.py --out threads/active-droplets/packs/ad4-protocell --seeds 0 1 2 --frames 200`
- segmentation: matter > 0.35 of robust range [-1.0648, 1.4382], min area 6 px

## Measurements
- components: final 11, mean 9.5, max 11; occupancy final 0.13
- tracks: 18; persistent (alive >= 50% of run): 11; longest 196 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 2.26 (1 = constant size)
- enclosures: components with a hole mean 0.01, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [12, 12, 11], H1 [0, 0, 0]
- motion: 4 long-lived tracks moved >= 1 body length; max speed 0.00193/time; max body lengths 1.7
- replication: splits 7, persistent splits 6, max generation 2, merges 0, nucleations 0
- channel total drift (end/start - 1): [0.1024, -0.5987, 2.7264, 1.0389, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 4 at frame 103: holes 0, rim-vs-core 0.45, rim-vs-outside 0.85, heterogeneity 0.15; core [0.941, 0.04, 0.912, 0.0, 0.165] rim [0.749, 0.081, 0.685, 0.0, 0.493]
  - track 5 at frame 103: holes 0, rim-vs-core 0.74, rim-vs-outside 0.75, heterogeneity 0.15; core [0.951, 0.028, 0.94, 0.0, 0.165] rim [0.639, 0.115, 0.545, 0.0, 0.697]
  - track 7 at frame 106: holes 0, rim-vs-core 0.77, rim-vs-outside 0.75, heterogeneity 0.16; core [0.957, 0.088, 0.0, 0.935, 0.162] rim [0.605, 0.173, 0.0, 0.515, 0.696]
  - track 12 at frame 133: holes 0, rim-vs-core 0.56, rim-vs-outside 0.80, heterogeneity 0.15; core [0.967, 0.092, 0.0, 0.942, 0.148] rim [0.705, 0.154, 0.0, 0.623, 0.529]

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, lineage.png, timeseries.png, movie.mp4, metrics.json

Measurements are screens, not verdicts: judge them against the images.
