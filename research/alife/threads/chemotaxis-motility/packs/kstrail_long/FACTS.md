# Evidence pack: kstrail (seed 0)

- world: `../../../../home/user/physim/research/alife/threads/chemotaxis-motility/worlds/kstrail/world.py`, family `chemotaxis`
- parent: None; mutation: Keller-Segel with volume filling + second, slow self-secreted repellent (trail)
- run: 151 frames x 240 steps x dt 0.05 = time 1800; grid [192, 192]; wall 239s; status ok
- command: `WORLD_P='{}' python -m labkit.run threads/chemotaxis-motility/worlds/kstrail/world.py --out threads/chemotaxis-motility/packs/kstrail_long --frames 150 --spf 240 --size 192 192 --no-movie`
- segmentation: matter > 0.35 of robust range [0.0, 1.0], min area 6 px

## Measurements
- components: final 2, mean 7.9, max 14; occupancy final 0.05
- tracks: 126; persistent (alive >= 50% of run): 0; longest 67 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 0.00 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [2, 2, 2], H1 [0, 0, 0]
- motion: 24 long-lived tracks moved >= 1 body length; max speed 0.51/time; max body lengths 28.6
- replication: splits 24, persistent splits 2, max generation 1, merges 22, nucleations 56
- channel total drift (end/start - 1): [-0.0002, -0.0002, -0.0002]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 94 at frame 110: holes 0, rim-vs-core 0.38, rim-vs-outside 0.34, heterogeneity 0.13; core [0.889, 0.365, 0.342] rim [0.527, 0.291, 0.258]
  - track 104 at frame 118: holes 0, rim-vs-core 0.45, rim-vs-outside 0.92, heterogeneity 0.19; core [0.999, 0.967, 0.962] rim [0.795, 0.707, 0.656]
  - track 95 at frame 102: holes 0, rim-vs-core 0.40, rim-vs-outside 0.51, heterogeneity 0.17; core [0.952, 0.522, 0.514] rim [0.612, 0.388, 0.365]
  - track 18 at frame 37: holes 0, rim-vs-core 0.37, rim-vs-outside 0.52, heterogeneity 0.16; core [0.956, 0.494, 0.478] rim [0.629, 0.377, 0.356]

## Warnings
- none

## Files
sheet.png, tracks.png, lineage.png, timeseries.png, movie.mp4, metrics.json

Measurements are screens, not verdicts: judge them against the images.
