# Evidence pack: ad4-protocell (seed 1)

- world: `../../../worlds/ad4-protocell/world.py`, family `phase-field`
- parent: ad2-catalysts + ad3-membrane; mutation: merge: catalyst-driven production (heredity) with amphiphile synthesis and interface binding (membrane)
- run: 201 frames x 200 steps x dt 0.5 = time 20000; grid [128, 128]; wall 235s; status ok
- command: `python -m labkit.run threads/active-droplets/worlds/ad4-protocell/world.py --out threads/active-droplets/packs/ad4-protocell --seeds 0 1 2 --frames 200`
- segmentation: matter > 0.35 of robust range [-1.0641, 1.4257], min area 6 px

## Measurements
- components: final 11, mean 9.7, max 11; occupancy final 0.13
- tracks: 17; persistent (alive >= 50% of run): 11; longest 201 frames; alive start-to-end: 1
- size of persistent tracks: max/min area ratio 2.62 (1 = constant size)
- enclosures: components with a hole mean 0.05, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [11, 11, 11], H1 [0, 0, 0]
- motion: 4 long-lived tracks moved >= 1 body length; max speed 0.00141/time; max body lengths 1.8
- replication: splits 6, persistent splits 6, max generation 2, merges 0, nucleations 0
- channel total drift (end/start - 1): [0.1052, -0.6034, 3.34, 0.4164, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 3 at frame 101: holes 0, rim-vs-core 0.77, rim-vs-outside 0.75, heterogeneity 0.16; core [0.961, 0.088, 0.0, 0.939, 0.164] rim [0.606, 0.176, 0.0, 0.515, 0.694]
  - track 5 at frame 104: holes 0, rim-vs-core 0.78, rim-vs-outside 0.76, heterogeneity 0.16; core [0.961, 0.083, 0.0, 0.944, 0.173] rim [0.608, 0.178, 0.0, 0.52, 0.72]
  - track 6 at frame 104: holes 0, rim-vs-core 0.69, rim-vs-outside 0.73, heterogeneity 0.15; core [0.964, 0.111, 0.0, 0.924, 0.137] rim [0.636, 0.177, 0.0, 0.53, 0.597]
  - track 13 at frame 134: holes 0, rim-vs-core 0.75, rim-vs-outside 0.75, heterogeneity 0.16; core [0.955, 0.035, 0.93, 0.0, 0.163] rim [0.616, 0.119, 0.518, 0.0, 0.688]

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, lineage.png, timeseries.png, movie.mp4, metrics.json

Measurements are screens, not verdicts: judge them against the images.
