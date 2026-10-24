# Evidence pack: evopursuit-nopred (seed 2)

- world: `../../../worlds/evopursuit_nopred/world.py`, family `chemotaxis`
- parent: evopursuit; mutation: NO-PREDATOR CONTROL (pred = 0); original: prey carry a heritable evasion allele (chi_x x (1+e) at growth cost), prey divide (Da_p 2)
- run: 126 frames x 240 steps x dt 0.05 = time 1500; grid [160, 160]; wall 342s; status ok
- command: `python -m labkit.run threads/chemotaxis-motility/worlds/evopursuit_nopred/world.py --out threads/chemotaxis-motility/packs/evopursuit_nopred --seeds 0 1 2 --frames 125 --no-movie`
- segmentation: matter > 0.35 of robust range [0.0, 0.995], min area 6 px

## Measurements
- components: final 8, mean 13.3, max 28; occupancy final 0.03
- tracks: 152; persistent (alive >= 50% of run): 3; longest 94 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 7.33 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [9, 8, 8], H1 [0, 0, 0]
- motion: 43 long-lived tracks moved >= 1 body length; max speed 0.289/time; max body lengths 34.4
- replication: splits 32, persistent splits 2, max generation 1, merges 47, nucleations 45
- channel total drift (end/start - 1): [-0.4867, None, None, -0.0349]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 50 at frame 66: holes 0, rim-vs-core 0.52, rim-vs-outside 0.44, heterogeneity 0.11; core [0.955, 0.0, 0.0, 0.098] rim [0.51, 0.0, 0.0, 0.358]
  - track 52 at frame 66: holes 0, rim-vs-core 0.24, rim-vs-outside 0.21, heterogeneity 0.05; core [0.002, 1.0, 0.0, 0.157] rim [0.001, 1.0, 0.0, 0.401]
  - track 102 at frame 90: holes 0, rim-vs-core 0.51, rim-vs-outside 0.44, heterogeneity 0.11; core [0.954, 0.0, 0.0, 0.104] rim [0.511, 0.0, 0.0, 0.36]
  - track 43 at frame 46: holes 0, rim-vs-core 0.48, rim-vs-outside 0.46, heterogeneity 0.10; core [0.959, 0.003, 0.0, 0.093] rim [0.542, 0.002, 0.0, 0.338]

## Warnings
- none

## Files
sheet.png, tracks.png, lineage.png, timeseries.png, movie.mp4, metrics.json

Measurements are screens, not verdicts: judge them against the images.
