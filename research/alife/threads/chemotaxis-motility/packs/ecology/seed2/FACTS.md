# Evidence pack: ecology (seed 2)

- world: `../../../worlds/ecology/world.py`, family `chemotaxis`
- parent: pursuit; mutation: pursuit + toxforage kinetics: nutrient-limited prey growth, predation, self-toxic trails for both species
- run: 201 frames x 100 steps x dt 0.05 = time 1000; grid [192, 192]; wall 251s; status ok
- command: `python -m labkit.run threads/chemotaxis-motility/worlds/ecology/world.py --out threads/chemotaxis-motility/packs/ecology --seeds 0 1 2`
- segmentation: matter > 0.35 of robust range [0.0001, 1.5548], min area 6 px

## Measurements
- components: final 15, mean 19.8, max 39; occupancy final 0.04
- tracks: 710; persistent (alive >= 50% of run): 0; longest 51 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 0.00 (1 = constant size)
- enclosures: components with a hole mean 0.03, final 1; holes at thresholds 0.2/0.35/0.5 final [0, 1, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [18, 15, 13], H1 [0, 0, 0]
- motion: 28 long-lived tracks moved >= 1 body length; max speed 0.618/time; max body lengths 13.6
- replication: splits 185, persistent splits 0, max generation 0, merges 151, nucleations 207
- channel total drift (end/start - 1): [-0.3061, -0.1456, -0.2377]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 150 at frame 81: holes 0, rim-vs-core 0.24, rim-vs-outside 0.23, heterogeneity 0.29; core [0.506, 0.493, 0.176] rim [0.535, 0.271, 0.263]
  - track 451 at frame 136: holes 0, rim-vs-core 0.30, rim-vs-outside 0.44, heterogeneity 0.33; core [0.512, 0.598, 0.123] rim [0.56, 0.325, 0.24]
  - track 461 at frame 134: holes 0, rim-vs-core 0.31, rim-vs-outside 0.26, heterogeneity 0.34; core [0.666, 0.463, 0.18] rim [0.391, 0.436, 0.325]
  - track 381 at frame 108: holes 0, rim-vs-core 0.23, rim-vs-outside 0.27, heterogeneity 0.33; core [0.584, 0.485, 0.063] rim [0.478, 0.331, 0.19]

## Warnings
- none

## Files
sheet.png, tracks.png, lineage.png, timeseries.png, movie.mp4, metrics.json

Measurements are screens, not verdicts: judge them against the images.
