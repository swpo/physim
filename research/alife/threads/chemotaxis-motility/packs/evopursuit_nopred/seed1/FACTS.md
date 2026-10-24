# Evidence pack: evopursuit-nopred (seed 1)

- world: `../../../worlds/evopursuit_nopred/world.py`, family `chemotaxis`
- parent: evopursuit; mutation: NO-PREDATOR CONTROL (pred = 0); original: prey carry a heritable evasion allele (chi_x x (1+e) at growth cost), prey divide (Da_p 2)
- run: 126 frames x 240 steps x dt 0.05 = time 1500; grid [160, 160]; wall 323s; status ok
- command: `python -m labkit.run threads/chemotaxis-motility/worlds/evopursuit_nopred/world.py --out threads/chemotaxis-motility/packs/evopursuit_nopred --seeds 0 1 2 --frames 125 --no-movie`
- segmentation: matter > 0.35 of robust range [0.0, 0.9958], min area 6 px

## Measurements
- components: final 8, mean 13.1, max 28; occupancy final 0.03
- tracks: 194; persistent (alive >= 50% of run): 1; longest 77 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 3.02 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [8, 8, 8], H1 [0, 0, 0]
- motion: 38 long-lived tracks moved >= 1 body length; max speed 0.293/time; max body lengths 23.3
- replication: splits 46, persistent splits 3, max generation 2, merges 63, nucleations 44
- channel total drift (end/start - 1): [-0.5423, None, None, -0.0292]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 133 at frame 87: holes 0, rim-vs-core 0.43, rim-vs-outside 1.00, heterogeneity 0.16; core [0.977, 0.982, 0.0, 0.034] rim [0.69, 0.77, 0.0, 0.274]
  - track 153 at frame 91: holes 0, rim-vs-core 0.48, rim-vs-outside 0.46, heterogeneity 0.10; core [0.96, 0.0, 0.0, 0.1] rim [0.557, 0.0, 0.0, 0.353]
  - track 174 at frame 106: holes 0, rim-vs-core 0.46, rim-vs-outside 0.45, heterogeneity 0.10; core [0.782, 1.0, 0.0, 0.183] rim [0.402, 1.0, 0.0, 0.445]
  - track 187 at frame 114: holes 0, rim-vs-core 0.56, rim-vs-outside 0.46, heterogeneity 0.13; core [0.945, 0.431, 0.0, 0.117] rim [0.505, 0.231, 0.0, 0.391]

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, lineage.png, timeseries.png, movie.mp4, metrics.json

Measurements are screens, not verdicts: judge them against the images.
