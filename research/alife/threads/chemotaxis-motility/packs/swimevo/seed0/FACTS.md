# Evidence pack: swimevo (seed 0)

- world: `../../../worlds/swimevo/world.py`, family `chemotaxis`
- parent: swimfission + active-droplets/ad5-evolve (confined alleles); mutation: split rho into two heritable alleles with own-density cooperative growth (body purification), symmetric patch mutations, allele B grows (1+s) faster
- run: 151 frames x 240 steps x dt 0.05 = time 1800; grid [160, 160]; wall 216s; status ok
- command: `python -m labkit.run threads/chemotaxis-motility/worlds/swimevo/world.py --out threads/chemotaxis-motility/packs/swimevo --seeds 0 1 2 --frames 150 --spf 240`
- segmentation: matter > 0.35 of robust range [0.0, 0.9961], min area 6 px

## Measurements
- components: final 9, mean 11.8, max 29; occupancy final 0.04
- tracks: 173; persistent (alive >= 50% of run): 1; longest 89 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 2.31 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [9, 9, 9], H1 [0, 0, 0]
- motion: 34 long-lived tracks moved >= 1 body length; max speed 0.307/time; max body lengths 24.5
- replication: splits 39, persistent splits 1, max generation 1, merges 52, nucleations 51
- channel total drift (end/start - 1): [-0.8618, None, -0.3756, -0.0429]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 12 at frame 48: holes 0, rim-vs-core 0.59, rim-vs-outside 0.46, heterogeneity 0.17; core [0.007, 0.971, 0.751, 0.057] rim [0.004, 0.496, 0.508, 0.307]
  - track 47 at frame 43: holes 0, rim-vs-core 0.52, rim-vs-outside 0.42, heterogeneity 0.18; core [0.121, 0.873, 0.753, 0.087] rim [0.066, 0.469, 0.545, 0.331]
  - track 72 at frame 55: holes 0, rim-vs-core 0.32, rim-vs-outside 0.66, heterogeneity 0.16; core [0.969, 0.001, 0.696, 0.124] rim [0.704, 0.001, 0.594, 0.282]
  - track 154 at frame 130: holes 0, rim-vs-core 0.53, rim-vs-outside 0.49, heterogeneity 0.16; core [0.001, 0.97, 0.663, 0.077] rim [0.001, 0.565, 0.444, 0.329]

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, lineage.png, timeseries.png, movie.mp4, metrics.json

Measurements are screens, not verdicts: judge them against the images.
