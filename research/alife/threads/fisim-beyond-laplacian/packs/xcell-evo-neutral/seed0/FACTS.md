# Evidence pack: xcell-evo-neutral (seed 0)

- world: `../../../worlds/xcell-evo-neutral/world.py`, family `fisim-extended-rd`
- parent: xcell-her-noise0.3 (+ resource/maintenance idea from the lenia-multichannel and autopoiesis threads); mutation: xcell-her + additive activator noise 0.3 (marker loss at unequal division = in-run variation) + a membrane-trapped waste q (tau=40, D=2, K=0.15) as a maintenance cost that gives continual death and birth. The marker changes waste production by W[q,h]=0.0. Neutral control: identical, but the marker does not touch waste (same noise, same mutation process).
- run: 201 frames x 200 steps x dt 0.02 = time 800; grid [160, 160]; wall 551s; status ok
- command: `python -m labkit.run threads/fisim-beyond-laplacian/worlds/xcell-evo-neutral/world.py --out threads/fisim-beyond-laplacian/packs/xcell-evo-neutral --seeds 0 1 2 --frames 200`
- segmentation: matter > 0.35 of robust range [0.0, 1.9451], min area 6 px

## Measurements
- components: final 23, mean 21.5, max 23; occupancy final 0.15
- tracks: 32; persistent (alive >= 50% of run): 23; longest 201 frames; alive start-to-end: 4
- size of persistent tracks: max/min area ratio 21.47 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [23, 23, 23], H1 [0, 0, 0]
- motion: 24 long-lived tracks moved >= 1 body length; max speed 0.269/time; max body lengths 8.3
- replication: splits 9, persistent splits 9, max generation 3, merges 0, nucleations 4
- channel total drift (end/start - 1): [0.3246, None, 0.1287, -0.1194]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 0 at frame 101: holes 0, rim-vs-core 0.62, rim-vs-outside 0.52, heterogeneity 0.24; core [0.912, 0.608, 0.681, 0.807] rim [0.586, 0.896, 0.331, 0.546]
  - track 1 at frame 101: holes 0, rim-vs-core 0.68, rim-vs-outside 0.62, heterogeneity 0.23; core [0.931, 0.638, 0.873, 0.858] rim [0.601, 0.9, 0.435, 0.559]
  - track 7 at frame 101: holes 0, rim-vs-core 0.53, rim-vs-outside 0.51, heterogeneity 0.16; core [0.914, 0.598, 0.117, 0.851] rim [0.581, 0.881, 0.05, 0.561]
  - track 30 at frame 124: holes 0, rim-vs-core 0.55, rim-vs-outside 0.51, heterogeneity 0.16; core [0.912, 0.616, 0.109, 0.862] rim [0.569, 0.898, 0.049, 0.536]

## Warnings
- none

## Files
sheet.png, tracks.png, lineage.png, timeseries.png, movie.mp4, metrics.json

Measurements are screens, not verdicts: judge them against the images.
