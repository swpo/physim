# Evidence pack: pursuit (seed 0)

- world: `../../../../home/user/physim/research/alife/threads/chemotaxis-motility/worlds/pursuit/world.py`, family `chemotaxis`
- parent: kstrail; mutation: two kstrail species with cross-taxis (predator up prey signal, prey down predator signal) + predation and nutrient-limited prey growth
- run: 201 frames x 60 steps x dt 0.05 = time 600; grid [160, 160]; wall 118s; status ok
- command: `WORLD_P='{"chi_x":0.0}' python -m labkit.run threads/chemotaxis-motility/worlds/pursuit/world.py --out threads/chemotaxis-motility/packs/pursuit_abl_noX --frames 200 --spf 60 --size 160 160 --no-movie`
- segmentation: matter > 0.35 of robust range [0.0, 1.994], min area 6 px

## Measurements
- components: final 4, mean 5.7, max 11; occupancy final 0.05
- tracks: 39; persistent (alive >= 50% of run): 2; longest 118 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 6.39 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [5, 5, 4], H1 [0, 0, 0]
- motion: 17 long-lived tracks moved >= 1 body length; max speed 0.433/time; max body lengths 11.0
- replication: splits 8, persistent splits 2, max generation 2, merges 11, nucleations 12
- channel total drift (end/start - 1): [-0.0001, 0.0003, 0.0]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 4 at frame 103: holes 0, rim-vs-core 0.66, rim-vs-outside 0.35, heterogeneity 0.15; core [0.949, 0.784, 0.0] rim [0.751, 0.153, 0.0]
  - track 6 at frame 101: holes 0, rim-vs-core 0.66, rim-vs-outside 0.35, heterogeneity 0.16; core [0.96, 0.765, 0.0] rim [0.758, 0.134, 0.0]
  - track 22 at frame 150: holes 0, rim-vs-core 0.49, rim-vs-outside 0.43, heterogeneity 0.25; core [0.863, 0.854, 0.0] rim [0.5, 0.526, 0.0]
  - track 32 at frame 171: holes 0, rim-vs-core 0.55, rim-vs-outside 0.57, heterogeneity 0.20; core [0.969, 0.947, 0.0] rim [0.682, 0.48, 0.0]

## Warnings
- none

## Files
sheet.png, tracks.png, lineage.png, timeseries.png, movie.mp4, metrics.json

Measurements are screens, not verdicts: judge them against the images.
