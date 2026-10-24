# Evidence pack: evopursuit-neutral (seed 0)

- world: `../../../worlds/evopursuit_neutral/world.py`, family `chemotaxis`
- parent: evopursuit; mutation: NEUTRAL CONTROL (e = cost = 0, same mutation process); original: prey carry a heritable evasion allele (chi_x x (1+e) at growth cost), prey divide (Da_p 2)
- run: 126 frames x 240 steps x dt 0.05 = time 1500; grid [160, 160]; wall 339s; status ok
- command: `python -m labkit.run threads/chemotaxis-motility/worlds/evopursuit_neutral/world.py --out threads/chemotaxis-motility/packs/evopursuit_neutral --seeds 0 1 2 --frames 125 --no-movie`
- segmentation: matter > 0.35 of robust range [0.0003, 1.667], min area 6 px

## Measurements
- components: final 1, mean 8.0, max 29; occupancy final 0.00
- tracks: 299; persistent (alive >= 50% of run): 0; longest 45 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 0.00 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [1, 1, 1], H1 [0, 0, 0]
- motion: 18 long-lived tracks moved >= 1 body length; max speed 0.551/time; max body lengths 33.3
- replication: splits 2, persistent splits 0, max generation 0, merges 5, nucleations 290
- channel total drift (end/start - 1): [-0.9496, None, -0.7461, -0.0013]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 127 at frame 57: holes 0, rim-vs-core 0.37, rim-vs-outside 0.47, heterogeneity 0.24; core [0.634, 0.152, 0.895, 0.0] rim [0.49, 0.114, 0.572, 0.093]
  - track 195 at frame 81: holes 0, rim-vs-core 0.44, rim-vs-outside 0.44, heterogeneity 0.35; core [0.492, 0.603, 0.909, 0.068] rim [0.389, 0.522, 0.555, 0.288]
  - track 58 at frame 33: holes 0, rim-vs-core 0.34, rim-vs-outside 0.44, heterogeneity 0.21; core [0.627, 0.01, 0.901, 0.0] rim [0.502, 0.008, 0.588, 0.069]
  - track 110 at frame 42: holes 0, rim-vs-core 0.42, rim-vs-outside 0.41, heterogeneity 0.19; core [0.045, 0.957, 0.954, 0.007] rim [0.034, 0.756, 0.6, 0.129]

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, lineage.png, timeseries.png, movie.mp4, metrics.json

Measurements are screens, not verdicts: judge them against the images.
