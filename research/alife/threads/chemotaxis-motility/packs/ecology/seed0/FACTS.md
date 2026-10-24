# Evidence pack: ecology (seed 0)

- world: `../../../worlds/ecology/world.py`, family `chemotaxis`
- parent: pursuit; mutation: pursuit + toxforage kinetics: nutrient-limited prey growth, predation, self-toxic trails for both species
- run: 201 frames x 100 steps x dt 0.05 = time 1000; grid [192, 192]; wall 269s; status ok
- command: `python -m labkit.run threads/chemotaxis-motility/worlds/ecology/world.py --out threads/chemotaxis-motility/packs/ecology --seeds 0 1 2`
- segmentation: matter > 0.35 of robust range [0.0001, 1.5104], min area 6 px

## Measurements
- components: final 24, mean 19.4, max 31; occupancy final 0.05
- tracks: 619; persistent (alive >= 50% of run): 0; longest 52 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 0.00 (1 = constant size)
- enclosures: components with a hole mean 0.06, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [26, 24, 15], H1 [0, 0, 0]
- motion: 40 long-lived tracks moved >= 1 body length; max speed 0.609/time; max body lengths 11.6
- replication: splits 169, persistent splits 0, max generation 0, merges 128, nucleations 169
- channel total drift (end/start - 1): [-0.1296, 0.0719, -0.2929]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 148 at frame 86: holes 0, rim-vs-core 0.28, rim-vs-outside 0.24, heterogeneity 0.27; core [0.537, 0.565, 0.096] rim [0.492, 0.304, 0.19]
  - track 430 at frame 170: holes 0, rim-vs-core 0.37, rim-vs-outside 0.30, heterogeneity 0.35; core [0.712, 0.481, 0.169] rim [0.391, 0.408, 0.339]
  - track 354 at frame 141: holes 0, rim-vs-core 0.26, rim-vs-outside 0.28, heterogeneity 0.33; core [0.626, 0.524, 0.1] rim [0.461, 0.361, 0.223]
  - track 339 at frame 131: holes 0, rim-vs-core 0.28, rim-vs-outside 0.48, heterogeneity 0.34; core [0.629, 0.563, 0.068] rim [0.559, 0.332, 0.214]

## Warnings
- none

## Files
sheet.png, tracks.png, lineage.png, timeseries.png, movie.mp4, metrics.json

Measurements are screens, not verdicts: judge them against the images.
