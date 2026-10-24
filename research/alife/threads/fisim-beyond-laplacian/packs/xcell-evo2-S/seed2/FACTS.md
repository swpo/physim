# Evidence pack: xcell-evo2-S (seed 2)

- world: `../../../worlds/xcell-evo2-S/world.py`, family `fisim-extended-rd`
- parent: xcell-her (sprint 1); maintenance/turnover idea from lenia-multichannel mcfd-MIRd; 5-px mutation patches + neutral arm from active-droplets ad5; mutation: Arm S of the sprint-2 evolution experiment. xcell-her minus its unused hdep channel plus one membrane-gated waste q (tau=40, D=2, K=0.15; turnover). Turnover is IMPOSED: chemostat-style dilution erases a random disk (radius 5) at Poisson rate KILL_RATE, identically in every arm. No marker is planted: h-on kinds arise only from rare cell-scale h kicks (Poisson, rate 0.005 per time unit, Gaussian disk sigma 1.5, amplitude 2.5, anywhere in the box). Only bodies (+ v, w dress) are planted. Selection arm: an h-on cell adds W[c,h]=0.15 cargo production (cargo activates the body, so on-cells grow and refill space faster).
- run: 201 frames x 500 steps x dt 0.02 = time 2000; grid [128, 128]; wall 790s; status ok
- command: `python -m labkit.run threads/fisim-beyond-laplacian/worlds/xcell-evo2-S/world.py --out threads/fisim-beyond-laplacian/packs/xcell-evo2-S --seeds 0 1 2 --frames 200 --spf 500`
- segmentation: matter > 0.35 of robust range [0.0, 1.8714], min area 6 px

## Measurements
- components: final 11, mean 11.3, max 13; occupancy final 0.12
- tracks: 26; persistent (alive >= 50% of run): 9; longest 201 frames; alive start-to-end: 4
- size of persistent tracks: max/min area ratio 12.16 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [11, 11, 11], H1 [0, 0, 0]
- motion: 22 long-lived tracks moved >= 1 body length; max speed 0.17/time; max body lengths 13.4
- replication: splits 8, persistent splits 6, max generation 2, merges 0, nucleations 0
- channel total drift (end/start - 1): [-0.294, None, 13.5189, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 1 at frame 101: holes 0, rim-vs-core 0.68, rim-vs-outside 0.60, heterogeneity 0.20; core [0.926, 0.618, 0.819, 0.894] rim [0.57, 0.927, 0.437, 0.59]
  - track 2 at frame 101: holes 0, rim-vs-core 0.56, rim-vs-outside 0.71, heterogeneity 0.21; core [0.935, 0.586, 0.827, 0.87] rim [0.647, 0.869, 0.513, 0.653]
  - track 4 at frame 101: holes 0, rim-vs-core 0.74, rim-vs-outside 0.53, heterogeneity 0.21; core [0.937, 0.552, 0.817, 0.499] rim [0.557, 0.913, 0.367, 0.227]
  - track 14 at frame 141: holes 0, rim-vs-core 0.68, rim-vs-outside 0.59, heterogeneity 0.21; core [0.934, 0.619, 0.82, 0.866] rim [0.586, 0.936, 0.436, 0.567]

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, lineage.png, timeseries.png, movie.mp4, metrics.json

Measurements are screens, not verdicts: judge them against the images.
