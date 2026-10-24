# Evidence pack: xcell-evo2-S (seed 0)

- world: `../../../worlds/xcell-evo2-S/world.py`, family `fisim-extended-rd`
- parent: xcell-her (sprint 1); maintenance/turnover idea from lenia-multichannel mcfd-MIRd; 5-px mutation patches + neutral arm from active-droplets ad5; mutation: Arm S of the sprint-2 evolution experiment. xcell-her minus its unused hdep channel plus one membrane-gated waste q (tau=40, D=2, K=0.15; turnover). Turnover is IMPOSED: chemostat-style dilution erases a random disk (radius 5) at Poisson rate KILL_RATE, identically in every arm. No marker is planted: h-on kinds arise only from rare cell-scale h kicks (Poisson, rate 0.005 per time unit, Gaussian disk sigma 1.5, amplitude 2.5, anywhere in the box). Only bodies (+ v, w dress) are planted. Selection arm: an h-on cell adds W[c,h]=0.15 cargo production (cargo activates the body, so on-cells grow and refill space faster).
- run: 201 frames x 500 steps x dt 0.02 = time 2000; grid [128, 128]; wall 825s; status ok
- command: `python -m labkit.run threads/fisim-beyond-laplacian/worlds/xcell-evo2-S/world.py --out threads/fisim-beyond-laplacian/packs/xcell-evo2-S --seeds 0 1 2 --frames 200 --spf 500`
- segmentation: matter > 0.35 of robust range [0.0, 1.8874], min area 6 px

## Measurements
- components: final 13, mean 10.8, max 13; occupancy final 0.14
- tracks: 34; persistent (alive >= 50% of run): 9; longest 201 frames; alive start-to-end: 2
- size of persistent tracks: max/min area ratio 10.00 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [13, 13, 13], H1 [0, 0, 0]
- motion: 26 long-lived tracks moved >= 1 body length; max speed 0.186/time; max body lengths 9.1
- replication: splits 12, persistent splits 11, max generation 6, merges 0, nucleations 0
- channel total drift (end/start - 1): [-0.1902, None, 9.4913, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 1 at frame 101: holes 0, rim-vs-core 0.56, rim-vs-outside 0.52, heterogeneity 0.15; core [0.936, 0.621, 0.095, 0.897] rim [0.593, 0.934, 0.051, 0.592]
  - track 6 at frame 101: holes 0, rim-vs-core 0.75, rim-vs-outside 0.71, heterogeneity 0.23; core [0.934, 0.6, 0.986, 0.92] rim [0.57, 0.929, 0.52, 0.592]
  - track 7 at frame 84: holes 0, rim-vs-core 0.46, rim-vs-outside 0.62, heterogeneity 0.16; core [0.941, 0.596, 0.095, 0.878] rim [0.649, 0.873, 0.058, 0.661]
  - track 28 at frame 183: holes 0, rim-vs-core 0.55, rim-vs-outside 0.50, heterogeneity 0.16; core [0.936, 0.611, 0.094, 0.797] rim [0.581, 0.932, 0.05, 0.522]

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, lineage.png, timeseries.png, movie.mp4, metrics.json

Measurements are screens, not verdicts: judge them against the images.
