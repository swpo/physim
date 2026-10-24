# Evidence pack: evopursuit (seed 0)

- world: `../../../../home/user/physim/research/alife/threads/chemotaxis-motility/worlds/evopursuit/world.py`, family `chemotaxis`
- parent: ecology + swimevo (alleles: active-droplets/ad5-evolve); mutation: prey carry a heritable evasion allele (chi_x x (1+e) at growth cost), prey divide (Da_p 2)
- run: 126 frames x 240 steps x dt 0.05 = time 1500; grid [160, 160]; wall 332s; status ok
- command: `WORLD_P='{"cost":0.3}' python -m labkit.run threads/chemotaxis-motility/worlds/evopursuit/world.py --out threads/chemotaxis-motility/packs/evopursuit_cost30_s0 --frames 125 --spf 240 --size 160 160 --no-movie`
- segmentation: matter > 0.35 of robust range [0.0003, 1.6842], min area 6 px

## Measurements
- components: final 2, mean 8.1, max 29; occupancy final 0.00
- tracks: 274; persistent (alive >= 50% of run): 1; longest 66 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 3.29 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [3, 3, 2], H1 [0, 0, 0]
- motion: 19 long-lived tracks moved >= 1 body length; max speed 0.545/time; max body lengths 34.4
- replication: splits 2, persistent splits 0, max generation 0, merges 4, nucleations 266
- channel total drift (end/start - 1): [-0.9322, None, -0.7422, -0.0021]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 58 at frame 46: holes 0, rim-vs-core 0.41, rim-vs-outside 0.44, heterogeneity 0.21; core [0.729, 0.001, 0.909, 0.004] rim [0.502, 0.001, 0.584, 0.104]
  - track 180 at frame 64: holes 0, rim-vs-core 0.40, rim-vs-outside 0.48, heterogeneity 0.23; core [0.607, 0.007, 0.9, 0.008] rim [0.481, 0.005, 0.547, 0.156]
  - track 43 at frame 25: holes 0, rim-vs-core 0.30, rim-vs-outside 0.33, heterogeneity 0.23; core [0.597, 0.002, 0.79, 0.002] rim [0.505, 0.001, 0.502, 0.03]
  - track 163 at frame 54: holes 0, rim-vs-core 0.34, rim-vs-outside 0.45, heterogeneity 0.22; core [0.558, 0.021, 0.92, 0.005] rim [0.488, 0.02, 0.6, 0.09]

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, lineage.png, timeseries.png, movie.mp4, metrics.json

Measurements are screens, not verdicts: judge them against the images.
