# Evidence pack: kstrail (seed 1)

- world: `../../../worlds/kstrail/world.py`, family `chemotaxis`
- parent: None; mutation: Keller-Segel with volume filling + second, slow self-secreted repellent (trail)
- run: 201 frames x 60 steps x dt 0.05 = time 600; grid [192, 192]; wall 64s; status ok
- command: `python -m labkit.run threads/chemotaxis-motility/worlds/kstrail/world.py --out threads/chemotaxis-motility/packs/kstrail --seeds 0 1 2`
- segmentation: matter > 0.35 of robust range [0.0, 1.0], min area 6 px

## Measurements
- components: final 9, mean 8.5, max 15; occupancy final 0.05
- tracks: 61; persistent (alive >= 50% of run): 4; longest 157 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 14.40 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [9, 9, 9], H1 [0, 0, 0]
- motion: 22 long-lived tracks moved >= 1 body length; max speed 0.607/time; max body lengths 14.7
- replication: splits 16, persistent splits 3, max generation 2, merges 14, nucleations 15
- channel total drift (end/start - 1): [-0.0, -0.0, -0.0]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 15 at frame 123: holes 0, rim-vs-core 0.37, rim-vs-outside 0.54, heterogeneity 0.17; core [0.952, 0.549, 0.498] rim [0.635, 0.422, 0.37]
  - track 33 at frame 145: holes 0, rim-vs-core 0.42, rim-vs-outside 0.31, heterogeneity 0.15; core [0.873, 0.412, 0.343] rim [0.47, 0.323, 0.258]
  - track 0 at frame 84: holes 0, rim-vs-core 0.24, rim-vs-outside 0.65, heterogeneity 0.18; core [0.951, 0.58, 0.538] rim [0.724, 0.518, 0.477]
  - track 49 at frame 171: holes 0, rim-vs-core 0.36, rim-vs-outside 0.56, heterogeneity 0.17; core [0.94, 0.59, 0.531] rim [0.641, 0.455, 0.379]

## Warnings
- none

## Files
sheet.png, tracks.png, lineage.png, timeseries.png, movie.mp4, metrics.json

Measurements are screens, not verdicts: judge them against the images.
