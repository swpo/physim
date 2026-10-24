# Evidence pack: mcf-fastcell-norefill (seed 0)

- world: `../../../worlds/mcf-fastcell-norefill/world.py`, family `lenia`
- parent: mcf-fastcell; mutation: ABLATION of mcf-fastcell: food does not regrow (rho=0)
- run: 301 frames x 10 steps x dt 0.1 = time 300; grid [192, 192]; wall 75s; status ok
- command: `python -m labkit.run threads/lenia-multichannel/worlds/mcf-fastcell-norefill/world.py --out threads/lenia-multichannel/packs/mcf-fastcell-norefill --seeds 0 1 2 --frames 300 --spf 10 --no-movie`
- segmentation: matter > 0.35 of robust range [0.0, 2.0], min area 6 px

## Measurements
- components: final 0, mean 2.4, max 5; occupancy final 0.00
- tracks: 33; persistent (alive >= 50% of run): 1; longest 202 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 1.62 (1 = constant size)
- enclosures: components with a hole mean 0.30, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [0, 0, 0], H1 [0, 0, 0]
- motion: 5 long-lived tracks moved >= 1 body length; max speed 1.31/time; max body lengths 8.5
- replication: splits 14, persistent splits 0, max generation 0, merges 1, nucleations 0
- channel total drift (end/start - 1): [-1.0, -1.0, -1.0, -0.517]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 0 at frame 101: holes 0, rim-vs-core 0.39, rim-vs-outside 0.50, heterogeneity 0.21; core [0.0, 0.818, 0.765, 0.515] rim [0.006, 0.648, 0.415, 0.544]
  - track 6 at frame 113: holes 0, rim-vs-core 0.34, rim-vs-outside 0.60, heterogeneity 0.22; core [0.032, 0.704, 0.84, 0.209] rim [0.07, 0.619, 0.514, 0.246]
  - track 3 at frame 45: holes 0, rim-vs-core 0.13, rim-vs-outside 0.65, heterogeneity 0.21; core [0.0, 0.718, 0.594, 0.483] rim [0.005, 0.703, 0.469, 0.509]
  - track 2 at frame 40: holes 0, rim-vs-core 0.24, rim-vs-outside 0.48, heterogeneity 0.23; core [0.004, 0.69, 0.653, 0.42] rim [0.022, 0.607, 0.438, 0.486]

## Warnings
- no components at the end: matter died out or fell below threshold
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, lineage.png, timeseries.png, movie.mp4, metrics.json

Measurements are screens, not verdicts: judge them against the images.
