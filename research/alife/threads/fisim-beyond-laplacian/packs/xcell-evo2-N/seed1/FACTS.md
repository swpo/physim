# Evidence pack: xcell-evo2-N (seed 1)

- world: `../../../worlds/xcell-evo2-N/world.py`, family `fisim-extended-rd`
- parent: xcell-her (sprint 1); maintenance/turnover idea from lenia-multichannel mcfd-MIRd; 5-px mutation patches + neutral arm from active-droplets ad5; mutation: Arm N of the sprint-2 evolution experiment. xcell-her minus its unused hdep channel plus one membrane-gated waste q (tau=40, D=2, K=0.15; turnover). Turnover is IMPOSED: chemostat-style dilution erases a random disk (radius 5) at Poisson rate KILL_RATE, identically in every arm. No marker is planted: h-on kinds arise only from rare cell-scale h kicks (Poisson, rate 0.005 per time unit, Gaussian disk sigma 1.5, amplitude 2.5, anywhere in the box). Only bodies (+ v, w dress) are planted. Neutral arm: identical except the marker has no effect (W[c,h]=0).
- run: 201 frames x 500 steps x dt 0.02 = time 2000; grid [128, 128]; wall 779s; status ok
- command: `python -m labkit.run threads/fisim-beyond-laplacian/worlds/xcell-evo2-N/world.py --out threads/fisim-beyond-laplacian/packs/xcell-evo2-N --seeds 0 1 2 --frames 200 --spf 500`
- segmentation: matter > 0.35 of robust range [0.0, 1.8729], min area 6 px

## Measurements
- components: final 11, mean 11.2, max 13; occupancy final 0.12
- tracks: 28; persistent (alive >= 50% of run): 8; longest 201 frames; alive start-to-end: 2
- size of persistent tracks: max/min area ratio 5.49 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [11, 11, 11], H1 [0, 0, 0]
- motion: 21 long-lived tracks moved >= 1 body length; max speed 0.186/time; max body lengths 9.3
- replication: splits 9, persistent splits 8, max generation 4, merges 0, nucleations 0
- channel total drift (end/start - 1): [-0.3151, None, 8.3921, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 5 at frame 101: holes 0, rim-vs-core 0.58, rim-vs-outside 0.67, heterogeneity 0.21; core [0.945, 0.561, 0.843, 0.766] rim [0.647, 0.886, 0.51, 0.582]
  - track 8 at frame 101: holes 0, rim-vs-core 0.71, rim-vs-outside 0.59, heterogeneity 0.21; core [0.923, 0.573, 0.837, 0.888] rim [0.567, 0.931, 0.444, 0.578]
  - track 11 at frame 109: holes 0, rim-vs-core 0.39, rim-vs-outside 0.80, heterogeneity 0.21; core [0.921, 0.634, 0.81, 0.824] rim [0.707, 0.8, 0.585, 0.649]
  - track 26 at frame 185: holes 0, rim-vs-core 0.36, rim-vs-outside 0.81, heterogeneity 0.21; core [0.91, 0.66, 0.79, 0.836] rim [0.71, 0.79, 0.589, 0.663]

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, lineage.png, timeseries.png, movie.mp4, metrics.json

Measurements are screens, not verdicts: judge them against the images.
