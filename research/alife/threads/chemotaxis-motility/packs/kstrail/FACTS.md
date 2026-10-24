# Evidence pack: kstrail (seed 0)

- world: `../../worlds/kstrail/world.py`, family `chemotaxis`
- parent: None; mutation: Keller-Segel with volume filling + second, slow self-secreted repellent (trail)
- run: 201 frames x 60 steps x dt 0.05 = time 600; grid [128, 128]; wall 31s; status ok
- command: `python -m labkit.run threads/chemotaxis-motility/worlds/kstrail/world.py --out threads/chemotaxis-motility/packs/kstrail --seeds 0 --frames 200`
- segmentation: matter > 0.35 of robust range [0.0, 0.9986], min area 6 px

## Measurements
- components: final 5, mean 4.3, max 7; occupancy final 0.05
- tracks: 35; persistent (alive >= 50% of run): 0; longest 92 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 0.00 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [5, 5, 5], H1 [0, 0, 0]
- motion: 13 long-lived tracks moved >= 1 body length; max speed 0.518/time; max body lengths 12.9
- replication: splits 10, persistent splits 3, max generation 2, merges 9, nucleations 7
- channel total drift (end/start - 1): [-0.0, -0.0, -0.0]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 21 at frame 155: holes 0, rim-vs-core 0.39, rim-vs-outside 0.65, heterogeneity 0.21; core [0.973, 0.94, 0.804] rim [0.65, 0.752, 0.69]
  - track 17 at frame 138: holes 0, rim-vs-core 0.41, rim-vs-outside 0.35, heterogeneity 0.17; core [0.9, 0.567, 0.438] rim [0.517, 0.45, 0.333]
  - track 0 at frame 59: holes 0, rim-vs-core 0.18, rim-vs-outside 0.34, heterogeneity 0.09; core [0.753, 0.358, 0.242] rim [0.578, 0.334, 0.224]
  - track 22 at frame 134: holes 0, rim-vs-core 0.38, rim-vs-outside 0.57, heterogeneity 0.19; core [0.972, 0.696, 0.582] rim [0.655, 0.536, 0.442]

## Warnings
- none

## Files
sheet.png, tracks.png, lineage.png, timeseries.png, movie.mp4, metrics.json

Measurements are screens, not verdicts: judge them against the images.
