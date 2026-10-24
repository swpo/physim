# Evidence pack: mc-fastcell (seed 1)

- world: `../../../worlds/mc-fastcell/world.py`, family `lenia`
- parent: Chakazul/Lenia found/233s.json#N5NYG2<L6218A; mutation: reference creature in this thread's multi-channel engine
- run: 301 frames x 5 steps x dt 0.1 = time 150; grid [192, 192]; wall 28s; status ok
- command: `python -m labkit.run threads/lenia-multichannel/worlds/mc-fastcell/world.py --out threads/lenia-multichannel/packs/mc-fastcell --seeds 0 1 2 --frames 300`
- segmentation: matter > 0.35 of robust range [0.0, 2.0], min area 6 px

## Measurements
- components: final 2, mean 2.8, max 5; occupancy final 0.02
- tracks: 21; persistent (alive >= 50% of run): 2; longest 216 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 1.27 (1 = constant size)
- enclosures: components with a hole mean 0.41, final 1; holes at thresholds 0.2/0.35/0.5 final [0, 1, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [3, 2, 2], H1 [1, 0, 0]
- motion: 6 long-lived tracks moved >= 1 body length; max speed 1.83/time; max body lengths 6.4
- replication: splits 9, persistent splits 0, max generation 0, merges 0, nucleations 0
- channel total drift (end/start - 1): [-0.3358, -0.3273, -0.3579]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 1 at frame 108: holes 0, rim-vs-core 0.27, rim-vs-outside 0.47, heterogeneity 0.30; core [0.0, 0.711, 0.718] rim [0.028, 0.55, 0.504]
  - track 4 at frame 124: holes 0, rim-vs-core 0.47, rim-vs-outside 0.64, heterogeneity 0.24; core [0.0, 0.803, 0.897] rim [0.002, 0.718, 0.435]
  - track 5 at frame 76: holes 0, rim-vs-core 0.43, rim-vs-outside 0.70, heterogeneity 0.25; core [0.0, 0.742, 0.87] rim [0.007, 0.738, 0.442]
  - track 17 at frame 267: holes 0, rim-vs-core 0.35, rim-vs-outside 0.57, heterogeneity 0.25; core [0.0, 0.792, 0.784] rim [0.008, 0.628, 0.479]

## Warnings
- none

## Files
sheet.png, tracks.png, lineage.png, timeseries.png, movie.mp4, metrics.json

Measurements are screens, not verdicts: judge them against the images.
