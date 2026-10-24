# Evidence pack: ad5-evolve (seed 0)

- world: `../../../worlds/ad5-evolve/world.py`, family `phase-field`
- parent: ad2-catalysts; mutation: N catalyst alleles with different rates, rare local mutation patches, random dilution disks
- run: 201 frames x 200 steps x dt 0.5 = time 20000; grid [128, 128]; wall 273s; status ok
- command: `python -m labkit.run threads/active-droplets/worlds/ad5-evolve/world.py --out threads/active-droplets/packs/ad5-evolve --seeds 0 1 2 --frames 200`
- segmentation: matter > 0.35 of robust range [-1.0658, 1.4451], min area 6 px

## Measurements
- components: final 12, mean 8.8, max 12; occupancy final 0.13
- tracks: 20; persistent (alive >= 50% of run): 8; longest 201 frames; alive start-to-end: 1
- size of persistent tracks: max/min area ratio 2.79 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [12, 12, 12], H1 [0, 0, 0]
- motion: 4 long-lived tracks moved >= 1 body length; max speed 0.00277/time; max body lengths 1.5
- replication: splits 8, persistent splits 8, max generation 4, merges 0, nucleations 0
- channel total drift (end/start - 1): [0.1174, -0.6255, -0.9498, None, None, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 0 at frame 101: holes 0, rim-vs-core 0.43, rim-vs-outside 0.76, heterogeneity 0.08; core [0.966, 0.095, 0.0, 0.998, 0.0, 0.0] rim [0.664, 0.169, 0.0, 0.696, 0.0, 0.0]
  - track 5 at frame 109: holes 0, rim-vs-core 0.45, rim-vs-outside 0.58, heterogeneity 0.09; core [0.961, 0.062, 0.071, 0.35, 0.0, 0.541] rim [0.627, 0.151, 0.042, 0.2, 0.0, 0.303]
  - track 8 at frame 134: holes 0, rim-vs-core 0.35, rim-vs-outside 0.81, heterogeneity 0.06; core [0.959, 0.057, 0.0, 0.0, 1.0, 0.0] rim [0.636, 0.136, 0.0, 0.0, 0.889, 0.0]
  - track 16 at frame 166: holes 0, rim-vs-core 0.27, rim-vs-outside 0.84, heterogeneity 0.08; core [0.938, 0.042, 0.0, 0.0, 0.0, 0.9] rim [0.762, 0.075, 0.0, 0.0, 0.0, 0.693]

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, lineage.png, timeseries.png, movie.mp4, metrics.json

Measurements are screens, not verdicts: judge them against the images.
