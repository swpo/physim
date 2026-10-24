# Evidence pack: kstrail (seed 2)

- world: `../../../worlds/kstrail/world.py`, family `chemotaxis`
- parent: None; mutation: Keller-Segel with volume filling + second, slow self-secreted repellent (trail)
- run: 201 frames x 60 steps x dt 0.05 = time 600; grid [192, 192]; wall 65s; status ok
- command: `python -m labkit.run threads/chemotaxis-motility/worlds/kstrail/world.py --out threads/chemotaxis-motility/packs/kstrail --seeds 0 1 2`
- segmentation: matter > 0.35 of robust range [0.0, 0.9999], min area 6 px

## Measurements
- components: final 9, mean 9.4, max 18; occupancy final 0.06
- tracks: 85; persistent (alive >= 50% of run): 2; longest 147 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 14.26 (1 = constant size)
- enclosures: components with a hole mean 0.02, final 0; holes at thresholds 0.2/0.35/0.5 final [1, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [10, 10, 9], H1 [1, 0, 0]
- motion: 25 long-lived tracks moved >= 1 body length; max speed 0.507/time; max body lengths 12.0
- replication: splits 23, persistent splits 5, max generation 2, merges 20, nucleations 21
- channel total drift (end/start - 1): [-0.0001, -0.0001, -0.0001]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 0 at frame 101: holes 0, rim-vs-core 0.43, rim-vs-outside 0.55, heterogeneity 0.20; core [0.964, 0.747, 0.658] rim [0.617, 0.56, 0.482]
  - track 5 at frame 86: holes 0, rim-vs-core 0.46, rim-vs-outside 0.55, heterogeneity 0.21; core [0.975, 0.861, 0.709] rim [0.634, 0.645, 0.494]
  - track 6 at frame 76: holes 0, rim-vs-core 0.43, rim-vs-outside 0.53, heterogeneity 0.19; core [0.967, 0.706, 0.58] rim [0.61, 0.533, 0.411]
  - track 53 at frame 163: holes 0, rim-vs-core 0.39, rim-vs-outside 0.33, heterogeneity 0.15; core [0.88, 0.471, 0.378] rim [0.509, 0.376, 0.283]

## Warnings
- none

## Files
sheet.png, tracks.png, lineage.png, timeseries.png, movie.mp4, metrics.json

Measurements are screens, not verdicts: judge them against the images.
