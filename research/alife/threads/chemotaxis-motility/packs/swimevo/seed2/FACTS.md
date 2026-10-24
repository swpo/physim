# Evidence pack: swimevo (seed 2)

- world: `../../../worlds/swimevo/world.py`, family `chemotaxis`
- parent: swimfission + active-droplets/ad5-evolve (confined alleles); mutation: split rho into two heritable alleles with own-density cooperative growth (body purification), symmetric patch mutations, allele B grows (1+s) faster
- run: 151 frames x 240 steps x dt 0.05 = time 1800; grid [160, 160]; wall 212s; status ok
- command: `python -m labkit.run threads/chemotaxis-motility/worlds/swimevo/world.py --out threads/chemotaxis-motility/packs/swimevo --seeds 0 1 2 --frames 150 --spf 240`
- segmentation: matter > 0.35 of robust range [0.0, 0.9941], min area 6 px

## Measurements
- components: final 7, mean 10.1, max 32; occupancy final 0.02
- tracks: 110; persistent (alive >= 50% of run): 7; longest 148 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 6.08 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [7, 7, 7], H1 [0, 0, 0]
- motion: 24 long-lived tracks moved >= 1 body length; max speed 0.323/time; max body lengths 43.9
- replication: splits 15, persistent splits 0, max generation 0, merges 31, nucleations 51
- channel total drift (end/start - 1): [-0.8357, None, -0.5877, -0.0274]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 8 at frame 77: holes 0, rim-vs-core 0.19, rim-vs-outside 0.65, heterogeneity 0.13; core [0.145, 1.0, 0.702, 0.087] rim [0.105, 0.997, 0.603, 0.238]
  - track 80 at frame 88: holes 0, rim-vs-core 0.47, rim-vs-outside 0.52, heterogeneity 0.16; core [0.972, 0.0, 0.757, 0.069] rim [0.61, 0.0, 0.548, 0.291]
  - track 89 at frame 91: holes 0, rim-vs-core 0.55, rim-vs-outside 0.48, heterogeneity 0.17; core [0.959, 0.0, 0.742, 0.082] rim [0.527, 0.0, 0.509, 0.336]
  - track 87 at frame 87: holes 0, rim-vs-core 0.48, rim-vs-outside 0.51, heterogeneity 0.16; core [0.971, 0.0, 0.753, 0.074] rim [0.594, 0.0, 0.551, 0.3]

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, lineage.png, timeseries.png, movie.mp4, metrics.json

Measurements are screens, not verdicts: judge them against the images.
