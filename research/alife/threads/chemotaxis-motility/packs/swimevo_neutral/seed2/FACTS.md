# Evidence pack: swimevo-neutral (seed 2)

- world: `../../../worlds/swimevo_neutral/world.py`, family `chemotaxis`
- parent: swimevo; mutation: NEUTRAL CONTROL of swimevo (s = 0, same mutation process); original: split rho into two heritable alleles with own-density cooperative growth (body purification), symmetric patch mutations, allele B grows (1+s) faster
- run: 151 frames x 240 steps x dt 0.05 = time 1800; grid [160, 160]; wall 208s; status ok
- command: `python -m labkit.run threads/chemotaxis-motility/worlds/swimevo_neutral/world.py --out threads/chemotaxis-motility/packs/swimevo_neutral --seeds 0 1 2 --frames 150 --spf 240`
- segmentation: matter > 0.35 of robust range [0.0, 0.9942], min area 6 px

## Measurements
- components: final 6, mean 10.8, max 32; occupancy final 0.02
- tracks: 141; persistent (alive >= 50% of run): 3; longest 110 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 4.58 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [6, 6, 6], H1 [0, 0, 0]
- motion: 33 long-lived tracks moved >= 1 body length; max speed 0.323/time; max body lengths 39.3
- replication: splits 23, persistent splits 3, max generation 2, merges 42, nucleations 54
- channel total drift (end/start - 1): [-0.6532, None, -0.6404, -0.0226]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 8 at frame 58: holes 0, rim-vs-core 0.56, rim-vs-outside 0.46, heterogeneity 0.18; core [0.958, 0.0, 0.737, 0.085] rim [0.508, 0.0, 0.51, 0.338]
  - track 78 at frame 78: holes 0, rim-vs-core 0.49, rim-vs-outside 0.47, heterogeneity 0.16; core [0.953, 0.0, 0.633, 0.119] rim [0.57, 0.0, 0.447, 0.364]
  - track 91 at frame 74: holes 0, rim-vs-core 0.59, rim-vs-outside 0.71, heterogeneity 0.21; core [0.868, 1.0, 0.777, 0.1] rim [0.437, 0.766, 0.566, 0.35]
  - track 121 at frame 120: holes 0, rim-vs-core 0.63, rim-vs-outside 0.58, heterogeneity 0.22; core [0.927, 0.802, 0.778, 0.079] rim [0.52, 0.445, 0.558, 0.314]

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, lineage.png, timeseries.png, movie.mp4, metrics.json

Measurements are screens, not verdicts: judge them against the images.
