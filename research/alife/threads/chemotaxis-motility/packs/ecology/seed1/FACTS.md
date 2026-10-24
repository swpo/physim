# Evidence pack: ecology (seed 1)

- world: `../../../worlds/ecology/world.py`, family `chemotaxis`
- parent: pursuit; mutation: pursuit + toxforage kinetics: nutrient-limited prey growth, predation, self-toxic trails for both species
- run: 201 frames x 100 steps x dt 0.05 = time 1000; grid [192, 192]; wall 249s; status ok
- command: `python -m labkit.run threads/chemotaxis-motility/worlds/ecology/world.py --out threads/chemotaxis-motility/packs/ecology --seeds 0 1 2`
- segmentation: matter > 0.35 of robust range [0.0001, 1.4964], min area 6 px

## Measurements
- components: final 22, mean 18.0, max 39; occupancy final 0.05
- tracks: 543; persistent (alive >= 50% of run): 0; longest 69 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 0.00 (1 = constant size)
- enclosures: components with a hole mean 0.01, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [26, 20, 15], H1 [0, 0, 0]
- motion: 39 long-lived tracks moved >= 1 body length; max speed 0.645/time; max body lengths 10.2
- replication: splits 141, persistent splits 0, max generation 0, merges 123, nucleations 150
- channel total drift (end/start - 1): [-0.1694, 0.0203, -0.2789]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 140 at frame 87: holes 0, rim-vs-core 0.08, rim-vs-outside 0.18, heterogeneity 0.28; core [0.435, 0.399, 0.163] rim [0.388, 0.365, 0.214]
  - track 359 at frame 153: holes 0, rim-vs-core 0.26, rim-vs-outside 0.27, heterogeneity 0.32; core [0.631, 0.484, 0.152] rim [0.473, 0.317, 0.28]
  - track 293 at frame 123: holes 0, rim-vs-core 0.36, rim-vs-outside 0.24, heterogeneity 0.28; core [0.776, 0.287, 0.206] rim [0.442, 0.35, 0.325]
  - track 200 at frame 89: holes 0, rim-vs-core 0.24, rim-vs-outside 0.25, heterogeneity 0.31; core [0.566, 0.498, 0.151] rim [0.458, 0.319, 0.261]

## Warnings
- none

## Files
sheet.png, tracks.png, lineage.png, timeseries.png, movie.mp4, metrics.json

Measurements are screens, not verdicts: judge them against the images.
