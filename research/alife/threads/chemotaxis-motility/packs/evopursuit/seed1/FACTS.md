# Evidence pack: evopursuit (seed 1)

- world: `../../../worlds/evopursuit/world.py`, family `chemotaxis`
- parent: ecology + swimevo (alleles: active-droplets/ad5-evolve); mutation: prey carry a heritable evasion allele (chi_x x (1+e) at growth cost), prey divide (Da_p 2)
- run: 126 frames x 240 steps x dt 0.05 = time 1500; grid [160, 160]; wall 305s; status ok
- command: `python -m labkit.run threads/chemotaxis-motility/worlds/evopursuit/world.py --out threads/chemotaxis-motility/packs/evopursuit --seeds 0 1 2 --frames 125`
- segmentation: matter > 0.35 of robust range [0.0001, 1.7946], min area 6 px

## Measurements
- components: final 30, mean 17.2, max 35; occupancy final 0.07
- tracks: 857; persistent (alive >= 50% of run): 0; longest 60 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 0.00 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [33, 28, 24], H1 [0, 0, 0]
- motion: 18 long-lived tracks moved >= 1 body length; max speed 0.478/time; max body lengths 36.1
- replication: splits 4, persistent splits 0, max generation 0, merges 16, nucleations 834
- channel total drift (end/start - 1): [-0.9949, None, 0.5957, -0.0838]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 78 at frame 48: holes 0, rim-vs-core 0.45, rim-vs-outside 0.37, heterogeneity 0.23; core [0.671, 0.008, 0.869, 0.083] rim [0.5, 0.006, 0.544, 0.335]
  - track 41 at frame 40: holes 0, rim-vs-core 0.29, rim-vs-outside 0.50, heterogeneity 0.23; core [0.583, 0.0, 0.891, 0.071] rim [0.583, 0.0, 0.643, 0.23]
  - track 65 at frame 42: holes 0, rim-vs-core 0.43, rim-vs-outside 0.38, heterogeneity 0.23; core [0.658, 0.0, 0.863, 0.058] rim [0.517, 0.0, 0.546, 0.309]
  - track 118 at frame 40: holes 0, rim-vs-core 0.43, rim-vs-outside 0.38, heterogeneity 0.25; core [0.711, 0.0, 0.833, 0.084] rim [0.534, 0.0, 0.54, 0.336]

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, lineage.png, timeseries.png, movie.mp4, metrics.json

Measurements are screens, not verdicts: judge them against the images.
