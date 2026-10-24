# Evidence pack: ad3-membrane (seed 2)

- world: `../../../worlds/ad3-membrane/world.py`, family `phase-field`
- parent: ad1-fuel; mutation: fuel reaction also makes an amphiphile psi that is drawn to |grad phi|^2 (ternary surfactant coupling) and lowers interfacial stiffness
- run: 201 frames x 200 steps x dt 0.5 = time 20000; grid [128, 128]; wall 191s; status ok
- command: `python -m labkit.run threads/active-droplets/worlds/ad3-membrane/world.py --out threads/active-droplets/packs/ad3-membrane --seeds 0 1 2 --frames 200`
- segmentation: matter > 0.35 of robust range [-1.0504, 1.2303], min area 6 px

## Measurements
- components: final 16, mean 10.0, max 16; occupancy final 0.14
- tracks: 30; persistent (alive >= 50% of run): 8; longest 141 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 1.27 (1 = constant size)
- enclosures: components with a hole mean 0.08, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [16, 16, 16], H1 [0, 0, 0]
- motion: 6 long-lived tracks moved >= 1 body length; max speed 0.00206/time; max body lengths 1.5
- replication: splits 14, persistent splits 14, max generation 4, merges 0, nucleations 0
- channel total drift (end/start - 1): [0.173, -0.6285, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 8 at frame 131: holes 0, rim-vs-core 0.63, rim-vs-outside 0.64, heterogeneity 0.18; core [0.968, 0.03, 0.179] rim [0.619, 0.091, 0.703]
  - track 9 at frame 131: holes 0, rim-vs-core 0.64, rim-vs-outside 0.64, heterogeneity 0.18; core [0.968, 0.03, 0.18] rim [0.615, 0.092, 0.705]
  - track 14 at frame 139: holes 0, rim-vs-core 0.66, rim-vs-outside 0.66, heterogeneity 0.19; core [0.96, 0.028, 0.186] rim [0.597, 0.095, 0.729]
  - track 26 at frame 180: holes 0, rim-vs-core 0.64, rim-vs-outside 0.65, heterogeneity 0.18; core [0.969, 0.032, 0.173] rim [0.603, 0.091, 0.69]

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, lineage.png, timeseries.png, movie.mp4, metrics.json

Measurements are screens, not verdicts: judge them against the images.
