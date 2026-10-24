# Evidence pack: xcell-evo2-N (seed 2)

- world: `../../../worlds/xcell-evo2-N/world.py`, family `fisim-extended-rd`
- parent: xcell-her (sprint 1); maintenance/turnover idea from lenia-multichannel mcfd-MIRd; 5-px mutation patches + neutral arm from active-droplets ad5; mutation: Arm N of the sprint-2 evolution experiment. xcell-her minus its unused hdep channel plus one membrane-gated waste q (tau=40, D=2, K=0.15; turnover). Turnover is IMPOSED: chemostat-style dilution erases a random disk (radius 5) at Poisson rate KILL_RATE, identically in every arm. No marker is planted: h-on kinds arise only from rare cell-scale h kicks (Poisson, rate 0.005 per time unit, Gaussian disk sigma 1.5, amplitude 2.5, anywhere in the box). Only bodies (+ v, w dress) are planted. Neutral arm: identical except the marker has no effect (W[c,h]=0).
- run: 201 frames x 500 steps x dt 0.02 = time 2000; grid [128, 128]; wall 802s; status ok
- command: `python -m labkit.run threads/fisim-beyond-laplacian/worlds/xcell-evo2-N/world.py --out threads/fisim-beyond-laplacian/packs/xcell-evo2-N --seeds 0 1 2 --frames 200 --spf 500`
- segmentation: matter > 0.35 of robust range [0.0, 1.8717], min area 6 px

## Measurements
- components: final 9, mean 10.6, max 13; occupancy final 0.10
- tracks: 26; persistent (alive >= 50% of run): 10; longest 201 frames; alive start-to-end: 1
- size of persistent tracks: max/min area ratio 3.07 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [9, 9, 9], H1 [0, 0, 0]
- motion: 22 long-lived tracks moved >= 1 body length; max speed 0.248/time; max body lengths 12.8
- replication: splits 8, persistent splits 6, max generation 2, merges 0, nucleations 0
- channel total drift (end/start - 1): [-0.4049, None, 3.4675, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 0 at frame 101: holes 0, rim-vs-core 0.59, rim-vs-outside 0.71, heterogeneity 0.21; core [0.939, 0.58, 0.856, 0.903] rim [0.662, 0.868, 0.527, 0.629]
  - track 7 at frame 97: holes 0, rim-vs-core 0.65, rim-vs-outside 0.60, heterogeneity 0.19; core [0.937, 0.64, 0.836, 0.928] rim [0.596, 0.935, 0.459, 0.639]
  - track 10 at frame 109: holes 0, rim-vs-core 0.68, rim-vs-outside 0.58, heterogeneity 0.20; core [0.933, 0.677, 0.805, 0.877] rim [0.573, 0.944, 0.412, 0.555]
  - track 15 at frame 133: holes 0, rim-vs-core 0.67, rim-vs-outside 0.59, heterogeneity 0.20; core [0.932, 0.612, 0.833, 0.918] rim [0.593, 0.93, 0.453, 0.622]

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, lineage.png, timeseries.png, movie.mp4, metrics.json

Measurements are screens, not verdicts: judge them against the images.
