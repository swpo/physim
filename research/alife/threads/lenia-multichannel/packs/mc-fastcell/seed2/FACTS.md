# Evidence pack: mc-fastcell (seed 2)

- world: `../../../worlds/mc-fastcell/world.py`, family `lenia`
- parent: Chakazul/Lenia found/233s.json#N5NYG2<L6218A; mutation: reference creature in this thread's multi-channel engine
- run: 301 frames x 5 steps x dt 0.1 = time 150; grid [192, 192]; wall 28s; status ok
- command: `python -m labkit.run threads/lenia-multichannel/worlds/mc-fastcell/world.py --out threads/lenia-multichannel/packs/mc-fastcell --seeds 0 1 2 --frames 300`
- segmentation: matter > 0.35 of robust range [0.0, 2.0], min area 6 px

## Measurements
- components: final 3, mean 3.0, max 6; occupancy final 0.03
- tracks: 17; persistent (alive >= 50% of run): 2; longest 272 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 1.31 (1 = constant size)
- enclosures: components with a hole mean 0.50, final 2; holes at thresholds 0.2/0.35/0.5 final [0, 2, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [3, 3, 3], H1 [1, 0, 0]
- motion: 5 long-lived tracks moved >= 1 body length; max speed 1.37/time; max body lengths 4.5
- replication: splits 7, persistent splits 0, max generation 0, merges 0, nucleations 0
- channel total drift (end/start - 1): [-0.2278, -0.1689, 0.0075]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 7 at frame 166: holes 0, rim-vs-core 0.17, rim-vs-outside 0.63, heterogeneity 0.33; core [0.0, 0.717, 0.635] rim [0.107, 0.615, 0.556]
  - track 3 at frame 106: holes 0, rim-vs-core 0.20, rim-vs-outside 0.63, heterogeneity 0.25; core [0.0, 0.838, 0.621] rim [0.0, 0.644, 0.589]
  - track 10 at frame 229: holes 0, rim-vs-core 0.38, rim-vs-outside 0.45, heterogeneity 0.31; core [0.0, 0.83, 0.559] rim [0.021, 0.447, 0.565]
  - track 5 at frame 93: holes 0, rim-vs-core 0.27, rim-vs-outside 0.60, heterogeneity 0.30; core [0.0, 0.792, 0.7] rim [0.044, 0.615, 0.5]

## Warnings
- none

## Files
sheet.png, tracks.png, lineage.png, timeseries.png, movie.mp4, metrics.json

Measurements are screens, not verdicts: judge them against the images.
