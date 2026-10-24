# Evidence pack: evopursuit-neutral (seed 2)

- world: `../../../worlds/evopursuit_neutral/world.py`, family `chemotaxis`
- parent: evopursuit; mutation: NEUTRAL CONTROL (e = cost = 0, same mutation process); original: prey carry a heritable evasion allele (chi_x x (1+e) at growth cost), prey divide (Da_p 2)
- run: 126 frames x 240 steps x dt 0.05 = time 1500; grid [160, 160]; wall 324s; status ok
- command: `python -m labkit.run threads/chemotaxis-motility/worlds/evopursuit_neutral/world.py --out threads/chemotaxis-motility/packs/evopursuit_neutral --seeds 0 1 2 --frames 125 --no-movie`
- segmentation: matter > 0.35 of robust range [0.0003, 1.6794], min area 6 px

## Measurements
- components: final 2, mean 7.3, max 25; occupancy final 0.00
- tracks: 222; persistent (alive >= 50% of run): 0; longest 45 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 0.00 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [2, 2, 2], H1 [0, 0, 0]
- motion: 23 long-lived tracks moved >= 1 body length; max speed 0.543/time; max body lengths 31.5
- replication: splits 5, persistent splits 0, max generation 0, merges 7, nucleations 206
- channel total drift (end/start - 1): [-0.9551, None, -0.8323, -0.003]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 158 at frame 72: holes 0, rim-vs-core 0.36, rim-vs-outside 0.43, heterogeneity 0.23; core [0.663, 0.023, 0.886, 0.012] rim [0.514, 0.017, 0.576, 0.119]
  - track 122 at frame 55: holes 0, rim-vs-core 0.40, rim-vs-outside 0.43, heterogeneity 0.25; core [0.609, 0.166, 0.939, 0.012] rim [0.473, 0.14, 0.587, 0.137]
  - track 169 at frame 78: holes 0, rim-vs-core 0.34, rim-vs-outside 0.44, heterogeneity 0.24; core [0.621, 0.18, 0.916, 0.001] rim [0.503, 0.144, 0.613, 0.1]
  - track 209 at frame 109: holes 0, rim-vs-core 0.36, rim-vs-outside 0.40, heterogeneity 0.15; core [0.022, 1.0, 0.931, 0.007] rim [0.016, 0.92, 0.601, 0.113]

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, lineage.png, timeseries.png, movie.mp4, metrics.json

Measurements are screens, not verdicts: judge them against the images.
