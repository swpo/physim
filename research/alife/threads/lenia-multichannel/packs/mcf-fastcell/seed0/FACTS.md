# Evidence pack: mcf-fastcell (seed 0)

- world: `../../../worlds/mcf-fastcell/world.py`, family `lenia`
- parent: mc-fastcell; mutation: matter can only be built from a consumed, regrowing, diffusing food field F (yield Y=5): motion now costs food
- run: 301 frames x 10 steps x dt 0.1 = time 300; grid [192, 192]; wall 74s; status ok
- command: `python -m labkit.run threads/lenia-multichannel/worlds/mcf-fastcell/world.py --out threads/lenia-multichannel/packs/mcf-fastcell --seeds 0 1 2 --frames 300 --spf 10`
- segmentation: matter > 0.35 of robust range [0.0, 2.0], min area 6 px

## Measurements
- components: final 3, mean 3.6, max 5; occupancy final 0.04
- tracks: 26; persistent (alive >= 50% of run): 4; longest 197 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 6.56 (1 = constant size)
- enclosures: components with a hole mean 0.55, final 1; holes at thresholds 0.2/0.35/0.5 final [2, 1, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [7, 4, 3], H1 [2, 1, 0]
- motion: 7 long-lived tracks moved >= 1 body length; max speed 1.28/time; max body lengths 12.6
- replication: splits 8, persistent splits 0, max generation 0, merges 2, nucleations 4
- channel total drift (end/start - 1): [-0.1738, -0.2555, -0.035, -0.226]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 0 at frame 98: holes 0, rim-vs-core 0.28, rim-vs-outside 0.55, heterogeneity 0.20; core [0.0, 0.743, 0.68, 0.328] rim [0.0, 0.67, 0.42, 0.384]
  - track 8 at frame 212: holes 0, rim-vs-core 0.28, rim-vs-outside 0.61, heterogeneity 0.21; core [0.0, 0.645, 0.701, 0.226] rim [0.004, 0.689, 0.429, 0.246]
  - track 3 at frame 88: holes 0, rim-vs-core 0.26, rim-vs-outside 0.73, heterogeneity 0.20; core [0.005, 0.847, 0.832, 0.0] rim [0.021, 0.683, 0.633, 0.024]
  - track 2 at frame 76: holes 0, rim-vs-core 0.18, rim-vs-outside 0.60, heterogeneity 0.20; core [0.0, 0.622, 0.651, 0.009] rim [0.0, 0.629, 0.475, 0.03]

## Warnings
- none

## Files
sheet.png, tracks.png, lineage.png, timeseries.png, movie.mp4, metrics.json

Measurements are screens, not verdicts: judge them against the images.
