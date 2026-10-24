# Evidence pack: kstrail (seed 0)

- world: `../../../worlds/kstrail/world.py`, family `chemotaxis`
- parent: None; mutation: Keller-Segel with volume filling + second, slow self-secreted repellent (trail)
- run: 201 frames x 60 steps x dt 0.05 = time 600; grid [192, 192]; wall 81s; status ok
- command: `python -m labkit.run threads/chemotaxis-motility/worlds/kstrail/world.py --out threads/chemotaxis-motility/packs/kstrail --seeds 0 1 2`
- segmentation: matter > 0.35 of robust range [0.0, 0.9982], min area 6 px

## Measurements
- components: final 11, mean 9.9, max 16; occupancy final 0.05
- tracks: 89; persistent (alive >= 50% of run): 6; longest 166 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 25.00 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [12, 12, 11], H1 [0, 0, 0]
- motion: 24 long-lived tracks moved >= 1 body length; max speed 0.496/time; max body lengths 23.3
- replication: splits 24, persistent splits 3, max generation 1, merges 20, nucleations 24
- channel total drift (end/start - 1): [-0.0, -0.0, -0.0]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 3 at frame 118: holes 0, rim-vs-core 0.45, rim-vs-outside 0.57, heterogeneity 0.22; core [0.974, 0.89, 0.751] rim [0.638, 0.671, 0.553]
  - track 32 at frame 133: holes 0, rim-vs-core 0.37, rim-vs-outside 0.31, heterogeneity 0.12; core [0.847, 0.393, 0.274] rim [0.495, 0.321, 0.21]
  - track 44 at frame 146: holes 0, rim-vs-core 0.42, rim-vs-outside 0.60, heterogeneity 0.19; core [0.96, 0.972, 0.895] rim [0.644, 0.801, 0.681]
  - track 22 at frame 109: holes 0, rim-vs-core 0.43, rim-vs-outside 0.33, heterogeneity 0.17; core [0.909, 0.601, 0.488] rim [0.521, 0.464, 0.357]

## Warnings
- none

## Files
sheet.png, tracks.png, lineage.png, timeseries.png, movie.mp4, metrics.json

Measurements are screens, not verdicts: judge them against the images.
