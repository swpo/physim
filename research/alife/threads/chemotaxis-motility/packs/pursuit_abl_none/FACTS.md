# Evidence pack: pursuit (seed 0)

- world: `../../../../home/user/physim/research/alife/threads/chemotaxis-motility/worlds/pursuit/world.py`, family `chemotaxis`
- parent: kstrail; mutation: two kstrail species with cross-taxis (predator up prey signal, prey down predator signal) + predation and nutrient-limited prey growth
- run: 201 frames x 60 steps x dt 0.05 = time 600; grid [160, 160]; wall 121s; status ok
- command: `WORLD_P='{"chi_x":0.0,"chi_y":0.0}' python -m labkit.run threads/chemotaxis-motility/worlds/pursuit/world.py --out threads/chemotaxis-motility/packs/pursuit_abl_none --frames 200 --spf 60 --size 160 160 --no-movie`
- segmentation: matter > 0.35 of robust range [0.0041, 1.133], min area 6 px

## Measurements
- components: final 7, mean 5.8, max 11; occupancy final 0.06
- tracks: 61; persistent (alive >= 50% of run): 1; longest 109 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 9.42 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [9, 7, 6], H1 [0, 0, 0]
- motion: 17 long-lived tracks moved >= 1 body length; max speed 0.55/time; max body lengths 9.7
- replication: splits 16, persistent splits 1, max generation 1, merges 15, nucleations 15
- channel total drift (end/start - 1): [-0.0001, 0.0, 0.0]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 6 at frame 101: holes 0, rim-vs-core 0.29, rim-vs-outside 0.53, heterogeneity 0.07; core [0.968, 0.109, 0.0] rim [0.677, 0.111, 0.0]
  - track 41 at frame 155: holes 0, rim-vs-core 0.28, rim-vs-outside 0.54, heterogeneity 0.06; core [0.959, 0.028, 0.0] rim [0.682, 0.03, 0.0]
  - track 4 at frame 76: holes 0, rim-vs-core 0.28, rim-vs-outside 0.55, heterogeneity 0.07; core [0.951, 0.115, 0.0] rim [0.673, 0.115, 0.0]
  - track 48 at frame 171: holes 0, rim-vs-core 0.38, rim-vs-outside 0.46, heterogeneity 0.17; core [0.934, 0.502, 0.0] rim [0.562, 0.551, 0.0]

## Warnings
- none

## Files
sheet.png, tracks.png, lineage.png, timeseries.png, movie.mp4, metrics.json

Measurements are screens, not verdicts: judge them against the images.
