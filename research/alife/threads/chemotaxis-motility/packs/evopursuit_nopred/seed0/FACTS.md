# Evidence pack: evopursuit-nopred (seed 0)

- world: `../../../worlds/evopursuit_nopred/world.py`, family `chemotaxis`
- parent: evopursuit; mutation: NO-PREDATOR CONTROL (pred = 0); original: prey carry a heritable evasion allele (chi_x x (1+e) at growth cost), prey divide (Da_p 2)
- run: 126 frames x 240 steps x dt 0.05 = time 1500; grid [160, 160]; wall 327s; status ok
- command: `python -m labkit.run threads/chemotaxis-motility/worlds/evopursuit_nopred/world.py --out threads/chemotaxis-motility/packs/evopursuit_nopred --seeds 0 1 2 --frames 125 --no-movie`
- segmentation: matter > 0.35 of robust range [0.0, 0.9941], min area 6 px

## Measurements
- components: final 8, mean 12.1, max 27; occupancy final 0.03
- tracks: 133; persistent (alive >= 50% of run): 4; longest 70 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 2.57 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [9, 8, 8], H1 [0, 0, 0]
- motion: 36 long-lived tracks moved >= 1 body length; max speed 0.321/time; max body lengths 21.7
- replication: splits 24, persistent splits 2, max generation 1, merges 45, nucleations 41
- channel total drift (end/start - 1): [-0.4815, None, None, -0.0383]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 97 at frame 90: holes 0, rim-vs-core 0.42, rim-vs-outside 0.68, heterogeneity 0.11; core [0.766, 1.0, 0.0, 0.196] rim [0.435, 0.972, 0.0, 0.449]
  - track 98 at frame 89: holes 0, rim-vs-core 0.38, rim-vs-outside 0.56, heterogeneity 0.12; core [0.623, 0.999, 0.0, 0.15] rim [0.342, 0.93, 0.0, 0.4]
  - track 103 at frame 95: holes 0, rim-vs-core 0.53, rim-vs-outside 0.44, heterogeneity 0.11; core [0.957, 0.009, 0.0, 0.099] rim [0.498, 0.005, 0.0, 0.361]
  - track 75 at frame 65: holes 0, rim-vs-core 0.61, rim-vs-outside 0.46, heterogeneity 0.15; core [0.907, 0.606, 0.0, 0.135] rim [0.454, 0.305, 0.0, 0.404]

## Warnings
- none

## Files
sheet.png, tracks.png, lineage.png, timeseries.png, movie.mp4, metrics.json

Measurements are screens, not verdicts: judge them against the images.
