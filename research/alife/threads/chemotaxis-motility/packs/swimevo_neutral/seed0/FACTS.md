# Evidence pack: swimevo-neutral (seed 0)

- world: `../../../worlds/swimevo_neutral/world.py`, family `chemotaxis`
- parent: swimevo; mutation: NEUTRAL CONTROL of swimevo (s = 0, same mutation process); original: split rho into two heritable alleles with own-density cooperative growth (body purification), symmetric patch mutations, allele B grows (1+s) faster
- run: 151 frames x 240 steps x dt 0.05 = time 1800; grid [160, 160]; wall 211s; status ok
- command: `python -m labkit.run threads/chemotaxis-motility/worlds/swimevo_neutral/world.py --out threads/chemotaxis-motility/packs/swimevo_neutral --seeds 0 1 2 --frames 150 --spf 240`
- segmentation: matter > 0.35 of robust range [0.0, 0.9951], min area 6 px

## Measurements
- components: final 7, mean 11.8, max 29; occupancy final 0.02
- tracks: 181; persistent (alive >= 50% of run): 0; longest 61 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 0.00 (1 = constant size)
- enclosures: components with a hole mean 0.01, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [7, 7, 7], H1 [0, 0, 0]
- motion: 40 long-lived tracks moved >= 1 body length; max speed 0.307/time; max body lengths 18.3
- replication: splits 39, persistent splits 1, max generation 1, merges 57, nucleations 51
- channel total drift (end/start - 1): [-0.777, None, -0.5889, -0.0249]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 47 at frame 45: holes 0, rim-vs-core 0.51, rim-vs-outside 0.50, heterogeneity 0.16; core [0.966, 0.001, 0.739, 0.077] rim [0.579, 0.001, 0.514, 0.324]
  - track 144 at frame 116: holes 0, rim-vs-core 0.34, rim-vs-outside 0.63, heterogeneity 0.13; core [0.112, 1.0, 0.668, 0.166] rim [0.061, 0.992, 0.462, 0.43]
  - track 148 at frame 110: holes 0, rim-vs-core 0.34, rim-vs-outside 0.57, heterogeneity 0.11; core [0.0, 1.0, 0.734, 0.088] rim [0.0, 1.0, 0.511, 0.339]
  - track 107 at frame 74: holes 0, rim-vs-core 0.33, rim-vs-outside 0.68, heterogeneity 0.17; core [0.955, 0.0, 0.723, 0.093] rim [0.685, 0.0, 0.613, 0.238]

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, lineage.png, timeseries.png, movie.mp4, metrics.json

Measurements are screens, not verdicts: judge them against the images.
