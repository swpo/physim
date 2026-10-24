# Evidence pack: mc-fastcell (seed 0)

- world: `../../../worlds/mc-fastcell/world.py`, family `lenia`
- parent: Chakazul/Lenia found/233s.json#N5NYG2<L6218A; mutation: reference creature in this thread's multi-channel engine
- run: 301 frames x 5 steps x dt 0.1 = time 150; grid [192, 192]; wall 35s; status ok
- command: `python -m labkit.run threads/lenia-multichannel/worlds/mc-fastcell/world.py --out threads/lenia-multichannel/packs/mc-fastcell --seeds 0 1 2 --frames 300`
- segmentation: matter > 0.35 of robust range [0.0, 2.0], min area 6 px

## Measurements
- components: final 2, mean 2.9, max 6; occupancy final 0.02
- tracks: 17; persistent (alive >= 50% of run): 2; longest 272 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 1.58 (1 = constant size)
- enclosures: components with a hole mean 0.43, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 1]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [3, 2, 2], H1 [1, 0, 0]
- motion: 5 long-lived tracks moved >= 1 body length; max speed 1.3/time; max body lengths 8.2
- replication: splits 7, persistent splits 0, max generation 0, merges 0, nucleations 0
- channel total drift (end/start - 1): [-0.4723, -0.4303, -0.2635]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 5 at frame 166: holes 0, rim-vs-core 0.30, rim-vs-outside 0.52, heterogeneity 0.28; core [0.0, 0.845, 0.626] rim [0.047, 0.57, 0.504]
  - track 3 at frame 159: holes 0, rim-vs-core 0.35, rim-vs-outside 0.44, heterogeneity 0.26; core [0.0, 0.79, 0.74] rim [0.0, 0.609, 0.441]
  - track 11 at frame 176: holes 0, rim-vs-core 0.45, rim-vs-outside 0.48, heterogeneity 0.28; core [0.0, 0.944, 0.446] rim [0.02, 0.511, 0.557]
  - track 6 at frame 53: holes 1, rim-vs-core 0.35, rim-vs-outside 0.50, heterogeneity 0.30; core [0.0, 0.914, 0.509] rim [0.019, 0.574, 0.431]

## Warnings
- none

## Files
sheet.png, tracks.png, lineage.png, timeseries.png, movie.mp4, metrics.json

Measurements are screens, not verdicts: judge them against the images.
