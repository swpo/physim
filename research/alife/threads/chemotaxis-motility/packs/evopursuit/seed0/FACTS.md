# Evidence pack: evopursuit (seed 0)

- world: `../../../worlds/evopursuit/world.py`, family `chemotaxis`
- parent: ecology + swimevo (alleles: active-droplets/ad5-evolve); mutation: prey carry a heritable evasion allele (chi_x x (1+e) at growth cost), prey divide (Da_p 2)
- run: 126 frames x 240 steps x dt 0.05 = time 1500; grid [160, 160]; wall 342s; status ok
- command: `python -m labkit.run threads/chemotaxis-motility/worlds/evopursuit/world.py --out threads/chemotaxis-motility/packs/evopursuit --seeds 0 1 2 --frames 125`
- segmentation: matter > 0.35 of robust range [0.0, 1.8456], min area 6 px

## Measurements
- components: final 26, mean 21.3, max 33; occupancy final 0.06
- tracks: 1126; persistent (alive >= 50% of run): 0; longest 40 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 0.00 (1 = constant size)
- enclosures: components with a hole mean 0.01, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [31, 26, 18], H1 [0, 0, 0]
- motion: 19 long-lived tracks moved >= 1 body length; max speed 0.56/time; max body lengths 18.4
- replication: splits 14, persistent splits 0, max generation 0, merges 23, nucleations 1076
- channel total drift (end/start - 1): [-0.9803, None, 0.6122, -0.079]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 62 at frame 35: holes 0, rim-vs-core 0.41, rim-vs-outside 0.35, heterogeneity 0.24; core [0.676, 0.001, 0.813, 0.155] rim [0.488, 0.001, 0.528, 0.388]
  - track 59 at frame 33: holes 0, rim-vs-core 0.44, rim-vs-outside 0.37, heterogeneity 0.23; core [0.661, 0.001, 0.867, 0.151] rim [0.534, 0.001, 0.521, 0.399]
  - track 236 at frame 58: holes 0, rim-vs-core 0.43, rim-vs-outside 0.36, heterogeneity 0.25; core [0.668, 0.027, 0.854, 0.129] rim [0.535, 0.02, 0.521, 0.367]
  - track 60 at frame 24: holes 0, rim-vs-core 0.35, rim-vs-outside 0.30, heterogeneity 0.24; core [0.517, 0.0, 0.782, 0.128] rim [0.489, 0.0, 0.5, 0.342]

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, lineage.png, timeseries.png, movie.mp4, metrics.json

Measurements are screens, not verdicts: judge them against the images.
