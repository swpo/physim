# Evidence pack: evopursuit (seed 2)

- world: `../../../worlds/evopursuit/world.py`, family `chemotaxis`
- parent: ecology + swimevo (alleles: active-droplets/ad5-evolve); mutation: prey carry a heritable evasion allele (chi_x x (1+e) at growth cost), prey divide (Da_p 2)
- run: 126 frames x 240 steps x dt 0.05 = time 1500; grid [160, 160]; wall 321s; status ok
- command: `python -m labkit.run threads/chemotaxis-motility/worlds/evopursuit/world.py --out threads/chemotaxis-motility/packs/evopursuit --seeds 0 1 2 --frames 125`
- segmentation: matter > 0.35 of robust range [0.0001, 1.7873], min area 6 px

## Measurements
- components: final 28, mean 16.5, max 35; occupancy final 0.07
- tracks: 843; persistent (alive >= 50% of run): 0; longest 58 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 0.00 (1 = constant size)
- enclosures: components with a hole mean 0.01, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [35, 28, 18], H1 [0, 0, 0]
- motion: 24 long-lived tracks moved >= 1 body length; max speed 0.548/time; max body lengths 23.8
- replication: splits 16, persistent splits 0, max generation 0, merges 17, nucleations 796
- channel total drift (end/start - 1): [-0.993, None, 0.6746, -0.0864]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 62 at frame 44: holes 0, rim-vs-core 0.36, rim-vs-outside 0.29, heterogeneity 0.23; core [0.437, 0.007, 0.873, 0.246] rim [0.458, 0.008, 0.574, 0.442]
  - track 67 at frame 33: holes 0, rim-vs-core 0.44, rim-vs-outside 0.42, heterogeneity 0.24; core [0.654, 0.001, 0.878, 0.096] rim [0.537, 0.001, 0.539, 0.358]
  - track 154 at frame 58: holes 0, rim-vs-core 0.45, rim-vs-outside 0.36, heterogeneity 0.26; core [0.648, 0.086, 0.819, 0.07] rim [0.575, 0.078, 0.43, 0.283]
  - track 37 at frame 25: holes 0, rim-vs-core 0.39, rim-vs-outside 0.56, heterogeneity 0.17; core [1.0, 0.0, 0.699, 0.094] rim [0.866, 0.0, 0.381, 0.27]

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, lineage.png, timeseries.png, movie.mp4, metrics.json

Measurements are screens, not verdicts: judge them against the images.
