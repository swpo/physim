# Evidence pack: pursuit (seed 0)

- world: `../../../../home/user/physim/research/alife/threads/chemotaxis-motility/worlds/pursuit/world.py`, family `chemotaxis`
- parent: kstrail; mutation: two kstrail species with cross-taxis (predator up prey signal, prey down predator signal) + predation and nutrient-limited prey growth
- run: 201 frames x 60 steps x dt 0.05 = time 600; grid [160, 160]; wall 119s; status ok
- command: `WORLD_P='{"chi_y":0.0}' python -m labkit.run threads/chemotaxis-motility/worlds/pursuit/world.py --out threads/chemotaxis-motility/packs/pursuit_abl_noY --frames 200 --spf 60 --size 160 160 --no-movie`
- segmentation: matter > 0.35 of robust range [0.0044, 1.0259], min area 6 px

## Measurements
- components: final 11, mean 6.9, max 14; occupancy final 0.06
- tracks: 64; persistent (alive >= 50% of run): 2; longest 139 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 11.13 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [15, 12, 11], H1 [2, 0, 0]
- motion: 19 long-lived tracks moved >= 1 body length; max speed 0.572/time; max body lengths 18.2
- replication: splits 18, persistent splits 3, max generation 1, merges 11, nucleations 17
- channel total drift (end/start - 1): [-0.0, 0.0, 0.0]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 1 at frame 104: holes 0, rim-vs-core 0.33, rim-vs-outside 0.52, heterogeneity 0.08; core [0.962, 0.134, 0.0] rim [0.637, 0.133, 0.0]
  - track 28 at frame 150: holes 0, rim-vs-core 0.32, rim-vs-outside 0.31, heterogeneity 0.07; core [0.845, 0.068, 0.0] rim [0.524, 0.07, 0.0]
  - track 38 at frame 155: holes 0, rim-vs-core 0.36, rim-vs-outside 0.47, heterogeneity 0.08; core [0.968, 0.014, 0.0] rim [0.605, 0.029, 0.0]
  - track 5 at frame 81: holes 0, rim-vs-core 0.22, rim-vs-outside 0.60, heterogeneity 0.08; core [0.946, 0.14, 0.0] rim [0.726, 0.149, 0.0]

## Warnings
- none

## Files
sheet.png, tracks.png, lineage.png, timeseries.png, movie.mp4, metrics.json

Measurements are screens, not verdicts: judge them against the images.
