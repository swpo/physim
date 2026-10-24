# Evidence pack: swimevo-neutral (seed 1)

- world: `../../../worlds/swimevo_neutral/world.py`, family `chemotaxis`
- parent: swimevo; mutation: NEUTRAL CONTROL of swimevo (s = 0, same mutation process); original: split rho into two heritable alleles with own-density cooperative growth (body purification), symmetric patch mutations, allele B grows (1+s) faster
- run: 151 frames x 240 steps x dt 0.05 = time 1800; grid [160, 160]; wall 204s; status ok
- command: `python -m labkit.run threads/chemotaxis-motility/worlds/swimevo_neutral/world.py --out threads/chemotaxis-motility/packs/swimevo_neutral --seeds 0 1 2 --frames 150 --spf 240`
- segmentation: matter > 0.35 of robust range [0.0, 0.9951], min area 6 px

## Measurements
- components: final 7, mean 12.3, max 32; occupancy final 0.02
- tracks: 175; persistent (alive >= 50% of run): 2; longest 135 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 6.47 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [8, 8, 7], H1 [0, 0, 0]
- motion: 40 long-lived tracks moved >= 1 body length; max speed 0.27/time; max body lengths 40.8
- replication: splits 31, persistent splits 1, max generation 1, merges 53, nucleations 63
- channel total drift (end/start - 1): [-0.6894, None, -0.5838, -0.0261]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 52 at frame 82: holes 0, rim-vs-core 0.43, rim-vs-outside 0.64, heterogeneity 0.16; core [0.66, 1.0, 0.717, 0.167] rim [0.379, 0.977, 0.511, 0.419]
  - track 8 at frame 42: holes 0, rim-vs-core 0.50, rim-vs-outside 0.49, heterogeneity 0.15; core [0.964, 0.0, 0.816, 0.059] rim [0.573, 0.0, 0.593, 0.278]
  - track 10 at frame 40: holes 0, rim-vs-core 0.54, rim-vs-outside 0.44, heterogeneity 0.16; core [0.955, 0.0, 0.819, 0.065] rim [0.509, 0.0, 0.61, 0.289]
  - track 158 at frame 124: holes 0, rim-vs-core 0.53, rim-vs-outside 0.47, heterogeneity 0.17; core [0.958, 0.0, 0.726, 0.095] rim [0.544, 0.0, 0.506, 0.347]

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, lineage.png, timeseries.png, movie.mp4, metrics.json

Measurements are screens, not verdicts: judge them against the images.
