# Evidence pack: ecology (seed 0)

- world: `../../../../home/user/physim/research/alife/threads/chemotaxis-motility/worlds/ecology/world.py`, family `chemotaxis`
- parent: pursuit; mutation: pursuit + toxforage kinetics: nutrient-limited prey growth, predation, self-toxic trails for both species
- run: 201 frames x 200 steps x dt 0.05 = time 2000; grid [160, 160]; wall 370s; status ok
- command: `WORLD_P='{}' python -m labkit.run threads/chemotaxis-motility/worlds/ecology/world.py --out threads/chemotaxis-motility/packs/ecology_long_160 --frames 200 --spf 200 --size 160 160 --no-movie`
- segmentation: matter > 0.35 of robust range [0.0001, 1.4901], min area 6 px

## Measurements
- components: final 14, mean 12.3, max 23; occupancy final 0.05
- tracks: 583; persistent (alive >= 50% of run): 0; longest 41 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 0.00 (1 = constant size)
- enclosures: components with a hole mean 0.03, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [16, 13, 12], H1 [0, 0, 0]
- motion: 15 long-lived tracks moved >= 1 body length; max speed 0.53/time; max body lengths 12.9
- replication: splits 56, persistent splits 0, max generation 0, merges 47, nucleations 424
- channel total drift (end/start - 1): [-0.1851, 0.0891, -0.2764]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 270 at frame 96: holes 0, rim-vs-core 0.32, rim-vs-outside 0.31, heterogeneity 0.33; core [0.489, 0.615, 0.059] rim [0.506, 0.327, 0.195]
  - track 364 at frame 131: holes 0, rim-vs-core 0.34, rim-vs-outside 0.49, heterogeneity 0.34; core [0.574, 0.602, 0.134] rim [0.566, 0.313, 0.308]
  - track 169 at frame 64: holes 0, rim-vs-core 0.26, rim-vs-outside 0.26, heterogeneity 0.33; core [0.609, 0.482, 0.185] rim [0.42, 0.36, 0.32]
  - track 470 at frame 171: holes 0, rim-vs-core 0.42, rim-vs-outside 0.46, heterogeneity 0.35; core [0.849, 0.357, 0.178] rim [0.477, 0.418, 0.369]

## Warnings
- none

## Files
sheet.png, tracks.png, lineage.png, timeseries.png, movie.mp4, metrics.json

Measurements are screens, not verdicts: judge them against the images.
