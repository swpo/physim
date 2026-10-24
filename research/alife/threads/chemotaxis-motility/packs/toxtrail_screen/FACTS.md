# Evidence pack: toxtrail (seed 0)

- world: `../../../../home/user/physim/research/alife/threads/chemotaxis-motility/worlds/toxtrail/world.py`, family `chemotaxis`
- parent: kstrail; mutation: the repellent trail is also toxic (death kd*h*rho), plus cooperative growth g: metabolism coupled to motility
- run: 201 frames x 80 steps x dt 0.05 = time 800; grid [160, 160]; wall 71s; status ok
- command: `WORLD_P='{"kd":0.005}' python -m labkit.run threads/chemotaxis-motility/worlds/toxtrail/world.py --out threads/chemotaxis-motility/packs/toxtrail_screen --frames 200 --spf 80 --size 160 160 --no-movie`
- segmentation: matter > 0.35 of robust range [0.0, 0.9993], min area 6 px

## Measurements
- components: final 9, mean 7.9, max 11; occupancy final 0.06
- tracks: 92; persistent (alive >= 50% of run): 1; longest 111 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 1.57 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [9, 9, 9], H1 [0, 0, 0]
- motion: 21 long-lived tracks moved >= 1 body length; max speed 0.418/time; max body lengths 10.2
- replication: splits 27, persistent splits 3, max generation 2, merges 25, nucleations 13
- channel total drift (end/start - 1): [0.1141, 0.133, 0.144]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 29 at frame 133: holes 0, rim-vs-core 0.44, rim-vs-outside 0.59, heterogeneity 0.21; core [0.975, 0.818, 0.715] rim [0.641, 0.618, 0.511]
  - track 38 at frame 141: holes 0, rim-vs-core 0.44, rim-vs-outside 0.54, heterogeneity 0.21; core [0.965, 0.754, 0.651] rim [0.605, 0.572, 0.487]
  - track 19 at frame 101: holes 0, rim-vs-core 0.39, rim-vs-outside 0.68, heterogeneity 0.20; core [0.955, 0.944, 0.867] rim [0.709, 0.761, 0.622]
  - track 10 at frame 72: holes 0, rim-vs-core 0.44, rim-vs-outside 0.58, heterogeneity 0.21; core [0.963, 0.79, 0.718] rim [0.634, 0.589, 0.5]

## Warnings
- none

## Files
sheet.png, tracks.png, lineage.png, timeseries.png, movie.mp4, metrics.json

Measurements are screens, not verdicts: judge them against the images.
