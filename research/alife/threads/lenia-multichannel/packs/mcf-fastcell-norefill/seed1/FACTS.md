# Evidence pack: mcf-fastcell-norefill (seed 1)

- world: `../../../worlds/mcf-fastcell-norefill/world.py`, family `lenia`
- parent: mcf-fastcell; mutation: ABLATION of mcf-fastcell: food does not regrow (rho=0)
- run: 301 frames x 10 steps x dt 0.1 = time 300; grid [192, 192]; wall 66s; status ok
- command: `python -m labkit.run threads/lenia-multichannel/worlds/mcf-fastcell-norefill/world.py --out threads/lenia-multichannel/packs/mcf-fastcell-norefill --seeds 0 1 2 --frames 300 --spf 10 --no-movie`
- segmentation: matter > 0.35 of robust range [0.0, 2.0], min area 6 px

## Measurements
- components: final 0, mean 2.8, max 6; occupancy final 0.00
- tracks: 30; persistent (alive >= 50% of run): 0; longest 143 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 0.00 (1 = constant size)
- enclosures: components with a hole mean 0.47, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [0, 0, 0], H1 [0, 0, 0]
- motion: 9 long-lived tracks moved >= 1 body length; max speed 1.35/time; max body lengths 8.9
- replication: splits 11, persistent splits 0, max generation 0, merges 1, nucleations 1
- channel total drift (end/start - 1): [-1.0, -1.0, -1.0, -0.604]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 6 at frame 86: holes 0, rim-vs-core 0.28, rim-vs-outside 0.66, heterogeneity 0.24; core [0.001, 0.682, 0.738, 0.492] rim [0.064, 0.708, 0.47, 0.522]
  - track 12 at frame 149: holes 0, rim-vs-core 0.33, rim-vs-outside 0.62, heterogeneity 0.22; core [0.0, 0.693, 0.739, 0.45] rim [0.04, 0.722, 0.416, 0.479]
  - track 21 at frame 202: holes 0, rim-vs-core 0.21, rim-vs-outside 0.64, heterogeneity 0.20; core [0.0, 0.767, 0.752, 0.419] rim [0.004, 0.666, 0.562, 0.422]
  - track 1 at frame 43: holes 0, rim-vs-core 0.40, rim-vs-outside 0.54, heterogeneity 0.22; core [0.0, 0.913, 0.713, 0.476] rim [0.044, 0.587, 0.497, 0.515]

## Warnings
- no components at the end: matter died out or fell below threshold
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, lineage.png, timeseries.png, movie.mp4, metrics.json

Measurements are screens, not verdicts: judge them against the images.
