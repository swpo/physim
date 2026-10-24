# Evidence pack: xcell-evo2-N (seed 0)

- world: `../../../worlds/xcell-evo2-N/world.py`, family `fisim-extended-rd`
- parent: xcell-her (sprint 1); maintenance/turnover idea from lenia-multichannel mcfd-MIRd; 5-px mutation patches + neutral arm from active-droplets ad5; mutation: Arm N of the sprint-2 evolution experiment. xcell-her minus its unused hdep channel plus one membrane-gated waste q (tau=40, D=2, K=0.15; turnover). Turnover is IMPOSED: chemostat-style dilution erases a random disk (radius 5) at Poisson rate KILL_RATE, identically in every arm. No marker is planted: h-on kinds arise only from rare cell-scale h kicks (Poisson, rate 0.005 per time unit, Gaussian disk sigma 1.5, amplitude 2.5, anywhere in the box). Only bodies (+ v, w dress) are planted. Neutral arm: identical except the marker has no effect (W[c,h]=0).
- run: 201 frames x 500 steps x dt 0.02 = time 2000; grid [128, 128]; wall 827s; status ok
- command: `python -m labkit.run threads/fisim-beyond-laplacian/worlds/xcell-evo2-N/world.py --out threads/fisim-beyond-laplacian/packs/xcell-evo2-N --seeds 0 1 2 --frames 200 --spf 500`
- segmentation: matter > 0.35 of robust range [0.0, 1.8769], min area 6 px

## Measurements
- components: final 12, mean 10.6, max 12; occupancy final 0.13
- tracks: 26; persistent (alive >= 50% of run): 9; longest 201 frames; alive start-to-end: 2
- size of persistent tracks: max/min area ratio 8.64 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [12, 12, 12], H1 [0, 0, 0]
- motion: 21 long-lived tracks moved >= 1 body length; max speed 0.165/time; max body lengths 14.2
- replication: splits 8, persistent splits 6, max generation 2, merges 0, nucleations 0
- channel total drift (end/start - 1): [-0.2447, None, 8.5751, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 5 at frame 101: holes 0, rim-vs-core 0.36, rim-vs-outside 0.69, heterogeneity 0.16; core [0.92, 0.606, 0.141, 0.926] rim [0.71, 0.802, 0.1, 0.708]
  - track 7 at frame 101: holes 0, rim-vs-core 0.58, rim-vs-outside 0.51, heterogeneity 0.17; core [0.926, 0.613, 0.139, 0.874] rim [0.565, 0.939, 0.072, 0.559]
  - track 10 at frame 106: holes 0, rim-vs-core 0.57, rim-vs-outside 0.51, heterogeneity 0.16; core [0.934, 0.626, 0.14, 0.863] rim [0.578, 0.938, 0.073, 0.557]
  - track 16 at frame 134: holes 0, rim-vs-core 0.47, rim-vs-outside 0.63, heterogeneity 0.16; core [0.927, 0.589, 0.144, 0.922] rim [0.679, 0.85, 0.092, 0.619]

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, lineage.png, timeseries.png, movie.mp4, metrics.json

Measurements are screens, not verdicts: judge them against the images.
