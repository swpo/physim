# Evidence pack: mc-mIRde (seed 0)

- world: `../../../worlds/mc-mIRde/world.py`, family `lenia`
- parent: Chakazul/Lenia found/233s.json#A39RG5<3G9TC1; mutation: reference creature in this thread's multi-channel engine
- run: 301 frames x 10 steps x dt 0.1 = time 300; grid [192, 192]; wall 66s; status ok
- command: `python -m labkit.run threads/lenia-multichannel/worlds/mc-mIRde/world.py --out threads/lenia-multichannel/packs/mc-mIRde --seeds 0 1 2 --frames 300 --no-movie`
- segmentation: matter > 0.35 of robust range [0.0, 3.0], min area 6 px

## Measurements
- components: final 12, mean 16.3, max 32; occupancy final 0.05
- tracks: 989; persistent (alive >= 50% of run): 0; longest 51 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 0.00 (1 = constant size)
- enclosures: components with a hole mean 0.94, final 1; holes at thresholds 0.2/0.35/0.5 final [3, 1, 1]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [51, 18, 9], H1 [6, 0, 0]
- motion: 3 long-lived tracks moved >= 1 body length; max speed 0.563/time; max body lengths 2.3
- replication: splits 305, persistent splits 1, max generation 1, merges 169, nucleations 212
- channel total drift (end/start - 1): [3.9291, 2.7851, 1.723]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 157 at frame 111: holes 0, rim-vs-core 0.32, rim-vs-outside 0.63, heterogeneity 0.39; core [0.665, 0.895, 0.302] rim [0.588, 0.602, 0.405]
  - track 163 at frame 124: holes 0, rim-vs-core 0.16, rim-vs-outside 0.93, heterogeneity 0.35; core [0.62, 0.955, 0.237] rim [0.692, 0.821, 0.28]
  - track 414 at frame 184: holes 0, rim-vs-core 0.33, rim-vs-outside 0.82, heterogeneity 0.36; core [0.916, 0.909, 0.377] rim [0.616, 0.776, 0.322]
  - track 332 at frame 164: holes 1, rim-vs-core 0.35, rim-vs-outside 0.81, heterogeneity 0.36; core [0.854, 0.999, 0.397] rim [0.543, 0.856, 0.314]

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, lineage.png, timeseries.png, movie.mp4, metrics.json

Measurements are screens, not verdicts: judge them against the images.
