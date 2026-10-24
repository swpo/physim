# Evidence pack: evopursuit (seed 1)

- world: `../../../../home/user/physim/research/alife/threads/chemotaxis-motility/worlds/evopursuit/world.py`, family `chemotaxis`
- parent: ecology + swimevo (alleles: active-droplets/ad5-evolve); mutation: prey carry a heritable evasion allele (chi_x x (1+e) at growth cost), prey divide (Da_p 2)
- run: 126 frames x 240 steps x dt 0.05 = time 1500; grid [160, 160]; wall 335s; status ok
- command: `WORLD_P='{"cost":0.3}' python -m labkit.run threads/chemotaxis-motility/worlds/evopursuit/world.py --out threads/chemotaxis-motility/packs/evopursuit_cost30_s1 --seeds 1 --frames 125 --no-movie`
- segmentation: matter > 0.35 of robust range [0.0003, 1.6704], min area 6 px

## Measurements
- components: final 2, mean 7.4, max 26; occupancy final 0.00
- tracks: 267; persistent (alive >= 50% of run): 0; longest 42 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 0.00 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [3, 2, 2], H1 [0, 0, 0]
- motion: 19 long-lived tracks moved >= 1 body length; max speed 0.557/time; max body lengths 31.8
- replication: splits 1, persistent splits 1, max generation 1, merges 8, nucleations 257
- channel total drift (end/start - 1): [-0.9246, None, -0.6625, -0.0031]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 51 at frame 36: holes 0, rim-vs-core 0.36, rim-vs-outside 0.42, heterogeneity 0.21; core [0.735, 0.001, 0.822, 0.0] rim [0.545, 0.0, 0.516, 0.0]
  - track 73 at frame 39: holes 0, rim-vs-core 0.34, rim-vs-outside 0.43, heterogeneity 0.22; core [0.685, 0.055, 0.896, 0.0] rim [0.489, 0.039, 0.629, 0.07]
  - track 43 at frame 33: holes 0, rim-vs-core 0.29, rim-vs-outside 0.33, heterogeneity 0.21; core [0.448, 0.0, 0.924, 0.001] rim [0.376, 0.0, 0.649, 0.049]
  - track 104 at frame 42: holes 0, rim-vs-core 0.38, rim-vs-outside 0.43, heterogeneity 0.23; core [0.584, 0.008, 0.94, 0.026] rim [0.497, 0.007, 0.581, 0.104]

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, lineage.png, timeseries.png, movie.mp4, metrics.json

Measurements are screens, not verdicts: judge them against the images.
