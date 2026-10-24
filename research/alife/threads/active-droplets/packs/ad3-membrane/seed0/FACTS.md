# Evidence pack: ad3-membrane (seed 0)

- world: `../../../worlds/ad3-membrane/world.py`, family `phase-field`
- parent: ad1-fuel; mutation: fuel reaction also makes an amphiphile psi that is drawn to |grad phi|^2 (ternary surfactant coupling) and lowers interfacial stiffness
- run: 201 frames x 200 steps x dt 0.5 = time 20000; grid [128, 128]; wall 202s; status ok
- command: `python -m labkit.run threads/active-droplets/worlds/ad3-membrane/world.py --out threads/active-droplets/packs/ad3-membrane --seeds 0 1 2 --frames 200`
- segmentation: matter > 0.35 of robust range [-1.0503, 1.2325], min area 6 px

## Measurements
- components: final 18, mean 11.3, max 18; occupancy final 0.14
- tracks: 34; persistent (alive >= 50% of run): 6; longest 143 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 1.31 (1 = constant size)
- enclosures: components with a hole mean 0.19, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [18, 18, 18], H1 [0, 0, 0]
- motion: 0 long-lived tracks moved >= 1 body length; max speed 0/time; max body lengths 1.0
- replication: splits 16, persistent splits 12, max generation 2, merges 0, nucleations 0
- channel total drift (end/start - 1): [0.1776, -0.6355, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 12 at frame 129: holes 0, rim-vs-core 0.51, rim-vs-outside 0.64, heterogeneity 0.18; core [0.975, 0.024, 0.162] rim [0.699, 0.076, 0.582]
  - track 13 at frame 129: holes 0, rim-vs-core 0.39, rim-vs-outside 0.66, heterogeneity 0.18; core [0.959, 0.034, 0.178] rim [0.751, 0.064, 0.502]
  - track 15 at frame 131: holes 0, rim-vs-core 0.64, rim-vs-outside 0.66, heterogeneity 0.18; core [0.966, 0.029, 0.176] rim [0.604, 0.088, 0.701]
  - track 22 at frame 158: holes 0, rim-vs-core 0.65, rim-vs-outside 0.65, heterogeneity 0.18; core [0.963, 0.025, 0.19] rim [0.614, 0.09, 0.733]

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, lineage.png, timeseries.png, movie.mp4, metrics.json

Measurements are screens, not verdicts: judge them against the images.
