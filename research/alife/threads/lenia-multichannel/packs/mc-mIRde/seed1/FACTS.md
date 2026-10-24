# Evidence pack: mc-mIRde (seed 1)

- world: `../../../worlds/mc-mIRde/world.py`, family `lenia`
- parent: Chakazul/Lenia found/233s.json#A39RG5<3G9TC1; mutation: reference creature in this thread's multi-channel engine
- run: 301 frames x 10 steps x dt 0.1 = time 300; grid [192, 192]; wall 53s; status ok
- command: `python -m labkit.run threads/lenia-multichannel/worlds/mc-mIRde/world.py --out threads/lenia-multichannel/packs/mc-mIRde --seeds 0 1 2 --frames 300 --no-movie`
- segmentation: matter > 0.35 of robust range [0.0, 3.0], min area 6 px

## Measurements
- components: final 33, mean 16.1, max 40; occupancy final 0.08
- tracks: 1019; persistent (alive >= 50% of run): 0; longest 58 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 0.00 (1 = constant size)
- enclosures: components with a hole mean 1.16, final 3; holes at thresholds 0.2/0.35/0.5 final [6, 3, 3]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [97, 26, 13], H1 [12, 1, 0]
- motion: 4 long-lived tracks moved >= 1 body length; max speed 0.646/time; max body lengths 3.0
- replication: splits 315, persistent splits 0, max generation 0, merges 176, nucleations 219
- channel total drift (end/start - 1): [8.749, 5.2439, 4.1197]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 497 at frame 224: holes 0, rim-vs-core 0.17, rim-vs-outside 0.96, heterogeneity 0.37; core [0.684, 0.981, 0.316] rim [0.656, 0.823, 0.383]
  - track 494 at frame 224: holes 0, rim-vs-core 0.10, rim-vs-outside 1.01, heterogeneity 0.36; core [0.768, 0.904, 0.317] rim [0.723, 0.893, 0.23]
  - track 554 at frame 232: holes 0, rim-vs-core 0.28, rim-vs-outside 0.71, heterogeneity 0.37; core [0.76, 0.939, 0.262] rim [0.529, 0.779, 0.298]
  - track 41 at frame 66: holes 0, rim-vs-core 0.28, rim-vs-outside 0.59, heterogeneity 0.37; core [0.682, 0.688, 0.646] rim [0.548, 0.629, 0.41]

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, lineage.png, timeseries.png, movie.mp4, metrics.json

Measurements are screens, not verdicts: judge them against the images.
