# Evidence pack: mc-MIRd (seed 1)

- world: `../../../worlds/mc-MIRd/world.py`, family `lenia`
- parent: Chakazul/Lenia found/233.json#M4HFAN<A39RG5; mutation: reference creature in this thread's multi-channel engine
- run: 201 frames x 10 steps x dt 0.1 = time 200; grid [192, 192]; wall 35s; status ok
- command: `python -m labkit.run threads/lenia-multichannel/worlds/mc-MIRd/world.py --out threads/lenia-multichannel/packs/mc-MIRd --seeds 0 1 2 --frames 200`
- segmentation: matter > 0.35 of robust range [0.0, 1.0], min area 6 px

## Measurements
- components: final 41, mean 17.7, max 43; occupancy final 0.17
- tracks: 262; persistent (alive >= 50% of run): 1; longest 134 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 1.37 (1 = constant size)
- enclosures: components with a hole mean 0.34, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 1]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [101, 61, 39], H1 [3, 1, 0]
- motion: 4 long-lived tracks moved >= 1 body length; max speed 0.86/time; max body lengths 2.8
- replication: splits 98, persistent splits 17, max generation 4, merges 32, nucleations 37
- channel total drift (end/start - 1): [27.1858, 20.0151, 14.1916]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 28 at frame 134: holes 0, rim-vs-core 0.38, rim-vs-outside 0.83, heterogeneity 0.32; core [0.995, 0.914, 0.215] rim [0.787, 0.602, 0.239]
  - track 124 at frame 163: holes 0, rim-vs-core 0.28, rim-vs-outside 1.08, heterogeneity 0.27; core [1.0, 0.783, 0.342] rim [0.959, 0.94, 0.117]
  - track 125 at frame 163: holes 0, rim-vs-core 0.36, rim-vs-outside 0.91, heterogeneity 0.34; core [1.0, 0.77, 0.378] rim [0.789, 0.975, 0.175]
  - track 185 at frame 180: holes 0, rim-vs-core 0.42, rim-vs-outside 0.89, heterogeneity 0.35; core [1.0, 0.729, 0.428] rim [0.803, 0.988, 0.164]

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, lineage.png, timeseries.png, movie.mp4, metrics.json

Measurements are screens, not verdicts: judge them against the images.
