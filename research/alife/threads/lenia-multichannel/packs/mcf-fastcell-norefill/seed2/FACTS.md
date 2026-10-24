# Evidence pack: mcf-fastcell-norefill (seed 2)

- world: `../../../worlds/mcf-fastcell-norefill/world.py`, family `lenia`
- parent: mcf-fastcell; mutation: ABLATION of mcf-fastcell: food does not regrow (rho=0)
- run: 301 frames x 10 steps x dt 0.1 = time 300; grid [192, 192]; wall 62s; status ok
- command: `python -m labkit.run threads/lenia-multichannel/worlds/mcf-fastcell-norefill/world.py --out threads/lenia-multichannel/packs/mcf-fastcell-norefill --seeds 0 1 2 --frames 300 --spf 10 --no-movie`
- segmentation: matter > 0.35 of robust range [0.0, 2.0], min area 6 px

## Measurements
- components: final 1, mean 2.7, max 5; occupancy final 0.01
- tracks: 30; persistent (alive >= 50% of run): 3; longest 184 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 30.53 (1 = constant size)
- enclosures: components with a hole mean 0.44, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [1, 1, 1], H1 [1, 0, 0]
- motion: 5 long-lived tracks moved >= 1 body length; max speed 1.02/time; max body lengths 7.7
- replication: splits 12, persistent splits 0, max generation 0, merges 3, nucleations 0
- channel total drift (end/start - 1): [-0.7523, -0.7585, -0.7412, -0.5423]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 3 at frame 91: holes 0, rim-vs-core 0.45, rim-vs-outside 0.53, heterogeneity 0.19; core [0.0, 0.874, 0.824, 0.484] rim [0.007, 0.605, 0.464, 0.52]
  - track 2 at frame 86: holes 0, rim-vs-core 0.15, rim-vs-outside 0.61, heterogeneity 0.23; core [0.0, 0.795, 0.579, 0.504] rim [0.015, 0.662, 0.511, 0.501]
  - track 1 at frame 78: holes 0, rim-vs-core 0.27, rim-vs-outside 0.64, heterogeneity 0.26; core [0.007, 0.875, 0.673, 0.433] rim [0.057, 0.636, 0.569, 0.454]
  - track 0 at frame 61: holes 1, rim-vs-core 0.29, rim-vs-outside 0.56, heterogeneity 0.28; core [0.001, 0.722, 0.746, 0.452] rim [0.071, 0.555, 0.519, 0.453]

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, lineage.png, timeseries.png, movie.mp4, metrics.json

Measurements are screens, not verdicts: judge them against the images.
