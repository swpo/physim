# Evidence pack: ad3-membrane (seed 1)

- world: `../../worlds/ad3-membrane/world.py`, family `phase-field`
- parent: ad1-fuel; mutation: fuel reaction also makes an amphiphile psi that is drawn to |grad phi|^2 (ternary surfactant coupling) and lowers interfacial stiffness
- run: 201 frames x 200 steps x dt 0.5 = time 20000; grid [128, 128]; wall 200s; status ok
- command: `python -m labkit.run threads/active-droplets/worlds/ad3-membrane/world.py --out threads/active-droplets/packs/ad3-membrane-damage --seeds 1 --frames 200 --damage 120:0.5`
- segmentation: matter > 0.35 of robust range [-1.0506, 1.2332], min area 6 px

## Measurements
- components: final 16, mean 10.6, max 16; occupancy final 0.14
- tracks: 30; persistent (alive >= 50% of run): 12; longest 143 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 1.38 (1 = constant size)
- enclosures: components with a hole mean 0.18, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [16, 16, 16], H1 [0, 0, 0]
- motion: 6 long-lived tracks moved >= 1 body length; max speed 0.00339/time; max body lengths 1.6
- replication: splits 14, persistent splits 10, max generation 4, merges 0, nucleations 0
- channel total drift (end/start - 1): [0.1744, -0.6312, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 6 at frame 129: holes 0, rim-vs-core 0.39, rim-vs-outside 0.66, heterogeneity 0.18; core [0.956, 0.033, 0.186] rim [0.74, 0.068, 0.504]
  - track 7 at frame 129: holes 0, rim-vs-core 0.55, rim-vs-outside 0.63, heterogeneity 0.18; core [0.968, 0.028, 0.17] rim [0.648, 0.083, 0.61]
  - track 14 at frame 138: holes 0, rim-vs-core 0.42, rim-vs-outside 0.66, heterogeneity 0.18; core [0.951, 0.025, 0.206] rim [0.728, 0.07, 0.561]
  - track 26 at frame 161: holes 0, rim-vs-core 0.64, rim-vs-outside 0.65, heterogeneity 0.18; core [0.965, 0.027, 0.182] rim [0.606, 0.092, 0.709]
- damage applied at frame 120: erased 95 px of a 191 px component

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, lineage.png, timeseries.png, movie.mp4, metrics.json

Measurements are screens, not verdicts: judge them against the images.
