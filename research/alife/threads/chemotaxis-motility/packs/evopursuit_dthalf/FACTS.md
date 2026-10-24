# Evidence pack: evopursuit (seed 0)

- world: `../../worlds/evopursuit/world.py`, family `chemotaxis`
- parent: ecology + swimevo (alleles: active-droplets/ad5-evolve); mutation: prey carry a heritable evasion allele (chi_x x (1+e) at growth cost), prey divide (Da_p 2)
- run: 126 frames x 480 steps x dt 0.05 = time 3000; grid [160, 160]; wall 680s; status ok
- command: `WORLD_P='{"dt":0.025}' python -m labkit.run threads/chemotaxis-motility/worlds/evopursuit/world.py --out threads/chemotaxis-motility/packs/evopursuit_dthalf --seeds 0 --frames 125 --spf 480 --no-movie`
- segmentation: matter > 0.35 of robust range [0.0001, 1.7843], min area 6 px

## Measurements
- components: final 29, mean 16.6, max 36; occupancy final 0.07
- tracks: 858; persistent (alive >= 50% of run): 0; longest 32 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 0.00 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [34, 31, 27], H1 [0, 0, 0]
- motion: 22 long-lived tracks moved >= 1 body length; max speed 0.279/time; max body lengths 22.2
- replication: splits 9, persistent splits 0, max generation 0, merges 11, nucleations 829
- channel total drift (end/start - 1): [-0.9566, None, 0.627, -0.0909]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 139 at frame 45: holes 0, rim-vs-core 0.45, rim-vs-outside 0.37, heterogeneity 0.23; core [0.603, 0.01, 0.924, 0.081] rim [0.497, 0.009, 0.561, 0.324]
  - track 125 at frame 41: holes 0, rim-vs-core 0.36, rim-vs-outside 0.27, heterogeneity 0.25; core [0.524, 0.02, 0.816, 0.034] rim [0.474, 0.02, 0.519, 0.234]
  - track 44 at frame 25: holes 0, rim-vs-core 0.38, rim-vs-outside 0.37, heterogeneity 0.24; core [0.628, 0.0, 0.859, 0.051] rim [0.462, 0.0, 0.57, 0.233]
  - track 203 at frame 61: holes 0, rim-vs-core 0.41, rim-vs-outside 0.35, heterogeneity 0.25; core [0.533, 0.048, 0.833, 0.206] rim [0.51, 0.047, 0.496, 0.442]

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, lineage.png, timeseries.png, movie.mp4, metrics.json

Measurements are screens, not verdicts: judge them against the images.
