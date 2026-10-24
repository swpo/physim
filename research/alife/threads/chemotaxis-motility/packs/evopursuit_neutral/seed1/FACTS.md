# Evidence pack: evopursuit-neutral (seed 1)

- world: `../../../worlds/evopursuit_neutral/world.py`, family `chemotaxis`
- parent: evopursuit; mutation: NEUTRAL CONTROL (e = cost = 0, same mutation process); original: prey carry a heritable evasion allele (chi_x x (1+e) at growth cost), prey divide (Da_p 2)
- run: 126 frames x 240 steps x dt 0.05 = time 1500; grid [160, 160]; wall 307s; status ok
- command: `python -m labkit.run threads/chemotaxis-motility/worlds/evopursuit_neutral/world.py --out threads/chemotaxis-motility/packs/evopursuit_neutral --seeds 0 1 2 --frames 125 --no-movie`
- segmentation: matter > 0.35 of robust range [0.0003, 1.6709], min area 6 px

## Measurements
- components: final 2, mean 7.2, max 26; occupancy final 0.00
- tracks: 257; persistent (alive >= 50% of run): 1; longest 76 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 4.47 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [2, 2, 2], H1 [0, 0, 0]
- motion: 16 long-lived tracks moved >= 1 body length; max speed 0.538/time; max body lengths 49.6
- replication: splits 1, persistent splits 1, max generation 1, merges 6, nucleations 249
- channel total drift (end/start - 1): [-0.9455, None, -0.7827, -0.0028]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 51 at frame 53: holes 0, rim-vs-core 0.39, rim-vs-outside 0.44, heterogeneity 0.22; core [0.699, 0.022, 0.882, 0.0] rim [0.532, 0.016, 0.548, 0.1]
  - track 172 at frame 83: holes 0, rim-vs-core 0.37, rim-vs-outside 0.47, heterogeneity 0.29; core [0.632, 0.426, 0.92, 0.0] rim [0.496, 0.334, 0.599, 0.065]
  - track 43 at frame 35: holes 0, rim-vs-core 0.34, rim-vs-outside 0.42, heterogeneity 0.21; core [0.617, 0.0, 0.879, 0.0] rim [0.503, 0.0, 0.554, 0.027]
  - track 75 at frame 40: holes 0, rim-vs-core 0.43, rim-vs-outside 0.46, heterogeneity 0.23; core [0.719, 0.079, 0.943, 0.026] rim [0.509, 0.054, 0.586, 0.147]

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, lineage.png, timeseries.png, movie.mp4, metrics.json

Measurements are screens, not verdicts: judge them against the images.
