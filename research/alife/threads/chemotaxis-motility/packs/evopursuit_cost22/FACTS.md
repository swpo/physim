# Evidence pack: evopursuit (seed 0)

- world: `../../../../home/user/physim/research/alife/threads/chemotaxis-motility/worlds/evopursuit/world.py`, family `chemotaxis`
- parent: ecology + swimevo (alleles: active-droplets/ad5-evolve); mutation: prey carry a heritable evasion allele (chi_x x (1+e) at growth cost), prey divide (Da_p 2)
- run: 126 frames x 240 steps x dt 0.05 = time 1500; grid [160, 160]; wall 338s; status ok
- command: `WORLD_P='{"cost":0.22}' python -m labkit.run threads/chemotaxis-motility/worlds/evopursuit/world.py --out threads/chemotaxis-motility/packs/evopursuit_cost22 --seeds 0 --frames 125 --no-movie`
- segmentation: matter > 0.35 of robust range [0.0001, 1.7278], min area 6 px

## Measurements
- components: final 28, mean 15.8, max 30; occupancy final 0.05
- tracks: 824; persistent (alive >= 50% of run): 0; longest 41 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 0.00 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [36, 30, 20], H1 [0, 0, 0]
- motion: 24 long-lived tracks moved >= 1 body length; max speed 0.542/time; max body lengths 16.8
- replication: splits 5, persistent splits 0, max generation 0, merges 18, nucleations 797
- channel total drift (end/start - 1): [-0.9718, None, 0.406, -0.0652]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 188 at frame 64: holes 0, rim-vs-core 0.43, rim-vs-outside 0.41, heterogeneity 0.24; core [0.684, 0.003, 0.853, 0.054] rim [0.527, 0.003, 0.517, 0.265]
  - track 341 at frame 96: holes 0, rim-vs-core 0.43, rim-vs-outside 0.32, heterogeneity 0.24; core [0.008, 0.703, 0.741, 0.061] rim [0.007, 0.626, 0.351, 0.223]
  - track 59 at frame 28: holes 0, rim-vs-core 0.43, rim-vs-outside 0.41, heterogeneity 0.24; core [0.62, 0.055, 0.862, 0.105] rim [0.585, 0.048, 0.468, 0.27]
  - track 56 at frame 27: holes 0, rim-vs-core 0.39, rim-vs-outside 0.54, heterogeneity 0.20; core [0.551, 0.0, 0.994, 0.088] rim [0.277, 0.0, 0.792, 0.279]

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, lineage.png, timeseries.png, movie.mp4, metrics.json

Measurements are screens, not verdicts: judge them against the images.
