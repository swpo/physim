# Evidence pack: mcf-fastcell (seed 2)

- world: `../../../worlds/mcf-fastcell/world.py`, family `lenia`
- parent: mc-fastcell; mutation: matter can only be built from a consumed, regrowing, diffusing food field F (yield Y=5): motion now costs food
- run: 301 frames x 10 steps x dt 0.1 = time 300; grid [192, 192]; wall 61s; status ok
- command: `python -m labkit.run threads/lenia-multichannel/worlds/mcf-fastcell/world.py --out threads/lenia-multichannel/packs/mcf-fastcell --seeds 0 1 2 --frames 300 --spf 10`
- segmentation: matter > 0.35 of robust range [0.0, 2.0], min area 6 px

## Measurements
- components: final 3, mean 3.5, max 5; occupancy final 0.03
- tracks: 13; persistent (alive >= 50% of run): 3; longest 301 frames; alive start-to-end: 2
- size of persistent tracks: max/min area ratio 1.60 (1 = constant size)
- enclosures: components with a hole mean 0.57, final 1; holes at thresholds 0.2/0.35/0.5 final [0, 1, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [4, 3, 3], H1 [1, 0, 0]
- motion: 5 long-lived tracks moved >= 1 body length; max speed 0.997/time; max body lengths 15.1
- replication: splits 4, persistent splits 0, max generation 0, merges 0, nucleations 1
- channel total drift (end/start - 1): [-0.2554, -0.2447, -0.2524, -0.2212]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 1 at frame 151: holes 0, rim-vs-core 0.50, rim-vs-outside 0.63, heterogeneity 0.20; core [0.0, 0.732, 0.875, 0.001] rim [0.009, 0.728, 0.377, 0.04]
  - track 2 at frame 151: holes 0, rim-vs-core 0.46, rim-vs-outside 0.44, heterogeneity 0.23; core [0.0, 0.944, 0.564, 0.248] rim [0.03, 0.504, 0.453, 0.282]
  - track 3 at frame 91: holes 0, rim-vs-core 0.45, rim-vs-outside 0.54, heterogeneity 0.20; core [0.0, 0.874, 0.824, 0.258] rim [0.007, 0.605, 0.464, 0.316]
  - track 0 at frame 61: holes 1, rim-vs-core 0.29, rim-vs-outside 0.56, heterogeneity 0.28; core [0.001, 0.722, 0.746, 0.309] rim [0.071, 0.555, 0.519, 0.317]

## Warnings
- none

## Files
sheet.png, tracks.png, lineage.png, timeseries.png, movie.mp4, metrics.json

Measurements are screens, not verdicts: judge them against the images.
