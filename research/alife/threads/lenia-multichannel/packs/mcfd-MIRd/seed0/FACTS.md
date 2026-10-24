# Evidence pack: mcfd-MIRd (seed 0)

- world: `../../worlds/mcfd-MIRd/world.py`, family `lenia`
- parent: mcf-MIRd; mutation: add a maintenance cost: all matter decays at rate 0.03 and must be rebuilt from food (no free dormancy)
- run: 701 frames x 20 steps x dt 0.1 = time 1400; grid [128, 128]; wall 148s; status ok
- command: `python -m labkit.run threads/lenia-multichannel/worlds/mcfd-MIRd/world.py --out threads/lenia-multichannel/packs/mcfd-MIRd --seeds 0 --frames 700`
- segmentation: matter > 0.35 of robust range [0.0, 0.997], min area 6 px

## Measurements
- components: final 3, mean 10.4, max 28; occupancy final 0.03
- tracks: 1701; persistent (alive >= 50% of run): 0; longest 99 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 0.00 (1 = constant size)
- enclosures: components with a hole mean 0.47, final 0; holes at thresholds 0.2/0.35/0.5 final [1, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [7, 4, 3], H1 [0, 0, 0]
- motion: 0 long-lived tracks moved >= 1 body length; max speed 0/time; max body lengths 2.6
- replication: splits 431, persistent splits 0, max generation 0, merges 319, nucleations 549
- channel total drift (end/start - 1): [1.1559, 0.8161, 0.4106, -0.4126]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 60 at frame 118: holes 0, rim-vs-core 0.62, rim-vs-outside 0.96, heterogeneity 0.27; core [1.0, 0.696, 0.599, 0.11] rim [0.806, 0.989, 0.092, 0.183]
  - track 529 at frame 218: holes 0, rim-vs-core 0.42, rim-vs-outside 0.75, heterogeneity 0.26; core [0.96, 0.875, 0.291, 0.044] rim [0.72, 0.554, 0.215, 0.129]
  - track 61 at frame 100: holes 0, rim-vs-core 0.46, rim-vs-outside 0.77, heterogeneity 0.29; core [1.0, 0.847, 0.503, 0.105] rim [0.764, 0.63, 0.185, 0.178]
  - track 254 at frame 159: holes 0, rim-vs-core 0.33, rim-vs-outside 0.96, heterogeneity 0.23; core [1.0, 0.799, 0.254, 0.053] rim [0.805, 0.908, 0.028, 0.128]

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, lineage.png, timeseries.png, movie.mp4, metrics.json

Measurements are screens, not verdicts: judge them against the images.
