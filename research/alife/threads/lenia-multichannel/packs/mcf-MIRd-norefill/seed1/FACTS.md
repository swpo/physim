# Evidence pack: mcf-MIRd-norefill (seed 1)

- world: `../../../worlds/mcf-MIRd-norefill/world.py`, family `lenia`
- parent: mcf-MIRd; mutation: ABLATION of mcf-MIRd: food does not regrow (rho=0)
- run: 401 frames x 10 steps x dt 0.1 = time 400; grid [192, 192]; wall 74s; status ok
- command: `python -m labkit.run threads/lenia-multichannel/worlds/mcf-MIRd-norefill/world.py --out threads/lenia-multichannel/packs/mcf-MIRd-norefill --seeds 0 1 2 --frames 400 --no-movie`
- segmentation: matter > 0.35 of robust range [0.0, 1.0], min area 6 px

## Measurements
- components: final 0, mean 3.5, max 12; occupancy final 0.00
- tracks: 202; persistent (alive >= 50% of run): 0; longest 72 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 0.00 (1 = constant size)
- enclosures: components with a hole mean 0.09, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [0, 0, 0], H1 [0, 0, 0]
- motion: 3 long-lived tracks moved >= 1 body length; max speed 0.428/time; max body lengths 2.3
- replication: splits 71, persistent splits 1, max generation 1, merges 27, nucleations 34
- channel total drift (end/start - 1): [-1.0, -1.0, -1.0, -0.7322]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 63 at frame 128: holes 0, rim-vs-core 0.37, rim-vs-outside 0.71, heterogeneity 0.23; core [0.982, 0.808, 0.077, 0.04] rim [0.698, 0.565, 0.065, 0.045]
  - track 176 at frame 232: holes 0, rim-vs-core 0.27, rim-vs-outside 0.64, heterogeneity 0.24; core [0.921, 0.694, 0.156, 0.001] rim [0.685, 0.574, 0.114, 0.005]
  - track 32 at frame 84: holes 0, rim-vs-core 0.30, rim-vs-outside 0.68, heterogeneity 0.20; core [0.938, 0.006, 0.172, 0.043] rim [0.708, 0.176, 0.268, 0.052]
  - track 15 at frame 61: holes 0, rim-vs-core 0.26, rim-vs-outside 0.79, heterogeneity 0.26; core [1.0, 0.574, 0.143, 0.152] rim [0.784, 0.701, 0.094, 0.191]

## Warnings
- no components at the end: matter died out or fell below threshold
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, lineage.png, timeseries.png, movie.mp4, metrics.json

Measurements are screens, not verdicts: judge them against the images.
