# Evidence pack: mcf-MIRd-norefill (seed 0)

- world: `../../../worlds/mcf-MIRd-norefill/world.py`, family `lenia`
- parent: mcf-MIRd; mutation: ABLATION of mcf-MIRd: food does not regrow (rho=0)
- run: 401 frames x 10 steps x dt 0.1 = time 400; grid [192, 192]; wall 94s; status ok
- command: `python -m labkit.run threads/lenia-multichannel/worlds/mcf-MIRd-norefill/world.py --out threads/lenia-multichannel/packs/mcf-MIRd-norefill --seeds 0 1 2 --frames 400 --no-movie`
- segmentation: matter > 0.35 of robust range [0.0, 1.0], min area 6 px

## Measurements
- components: final 0, mean 2.7, max 10; occupancy final 0.00
- tracks: 160; persistent (alive >= 50% of run): 0; longest 55 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 0.00 (1 = constant size)
- enclosures: components with a hole mean 0.11, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [0, 0, 0], H1 [0, 0, 0]
- motion: 1 long-lived tracks moved >= 1 body length; max speed 0.489/time; max body lengths 2.0
- replication: splits 53, persistent splits 1, max generation 1, merges 21, nucleations 30
- channel total drift (end/start - 1): [-1.0, -1.0, -1.0, -0.6284]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 21 at frame 84: holes 0, rim-vs-core 0.48, rim-vs-outside 0.76, heterogeneity 0.25; core [0.998, 0.963, 0.151, 0.16] rim [0.777, 0.534, 0.145, 0.194]
  - track 3 at frame 20: holes 0, rim-vs-core 0.29, rim-vs-outside 0.67, heterogeneity 0.22; core [0.959, 0.03, 0.22, 0.388] rim [0.719, 0.181, 0.202, 0.436]
  - track 11 at frame 61: holes 0, rim-vs-core 0.31, rim-vs-outside 0.78, heterogeneity 0.28; core [1.0, 0.473, 0.141, 0.158] rim [0.763, 0.667, 0.169, 0.197]
  - track 76 at frame 128: holes 0, rim-vs-core 0.32, rim-vs-outside 0.69, heterogeneity 0.20; core [0.941, 0.156, 0.035, 0.005] rim [0.743, 0.395, 0.117, 0.018]

## Warnings
- no components at the end: matter died out or fell below threshold
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, lineage.png, timeseries.png, movie.mp4, metrics.json

Measurements are screens, not verdicts: judge them against the images.
