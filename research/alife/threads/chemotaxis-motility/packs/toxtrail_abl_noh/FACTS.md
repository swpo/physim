# Evidence pack: toxtrail (seed 0)

- world: `../../../../home/user/physim/research/alife/threads/chemotaxis-motility/worlds/toxtrail/world.py`, family `chemotaxis`
- parent: kstrail; mutation: the repellent trail is also toxic (death kd*h*rho), plus cooperative growth g: metabolism coupled to motility
- run: 201 frames x 80 steps x dt 0.05 = time 800; grid [160, 160]; wall 71s; status ok
- command: `WORLD_P='{"chi_h":0.0}' python -m labkit.run threads/chemotaxis-motility/worlds/toxtrail/world.py --out threads/chemotaxis-motility/packs/toxtrail_abl_noh --frames 200 --spf 80 --size 160 160 --no-movie`
- segmentation: matter > 0.35 of robust range [0.0, 0.9941], min area 6 px

## Measurements
- components: final 20, mean 25.4, max 43; occupancy final 0.02
- tracks: 62; persistent (alive >= 50% of run): 20; longest 195 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 7.86 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [20, 20, 20], H1 [0, 0, 0]
- motion: 21 long-lived tracks moved >= 1 body length; max speed 0.0876/time; max body lengths 1.8
- replication: splits 0, persistent splits 0, max generation 0, merges 19, nucleations 43
- channel total drift (end/start - 1): [-0.5954, -0.5956, -0.5958]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 0 at frame 104: holes 0, rim-vs-core 0.50, rim-vs-outside 0.51, heterogeneity 0.17; core [0.953, 0.781, 0.895] rim [0.561, 0.638, 0.625]
  - track 1 at frame 104: holes 0, rim-vs-core 0.47, rim-vs-outside 0.53, heterogeneity 0.16; core [0.96, 0.797, 0.906] rim [0.6, 0.658, 0.645]
  - track 3 at frame 104: holes 0, rim-vs-core 0.45, rim-vs-outside 0.55, heterogeneity 0.15; core [0.968, 0.795, 0.914] rim [0.628, 0.658, 0.656]
  - track 5 at frame 104: holes 0, rim-vs-core 0.45, rim-vs-outside 0.53, heterogeneity 0.14; core [0.958, 0.797, 0.901] rim [0.613, 0.659, 0.642]

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, lineage.png, timeseries.png, movie.mp4, metrics.json

Measurements are screens, not verdicts: judge them against the images.
