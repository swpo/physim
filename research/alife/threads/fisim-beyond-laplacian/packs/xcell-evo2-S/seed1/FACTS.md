# Evidence pack: xcell-evo2-S (seed 1)

- world: `../../../worlds/xcell-evo2-S/world.py`, family `fisim-extended-rd`
- parent: xcell-her (sprint 1); maintenance/turnover idea from lenia-multichannel mcfd-MIRd; 5-px mutation patches + neutral arm from active-droplets ad5; mutation: Arm S of the sprint-2 evolution experiment. xcell-her minus its unused hdep channel plus one membrane-gated waste q (tau=40, D=2, K=0.15; turnover). Turnover is IMPOSED: chemostat-style dilution erases a random disk (radius 5) at Poisson rate KILL_RATE, identically in every arm. No marker is planted: h-on kinds arise only from rare cell-scale h kicks (Poisson, rate 0.005 per time unit, Gaussian disk sigma 1.5, amplitude 2.5, anywhere in the box). Only bodies (+ v, w dress) are planted. Selection arm: an h-on cell adds W[c,h]=0.15 cargo production (cargo activates the body, so on-cells grow and refill space faster).
- run: 201 frames x 500 steps x dt 0.02 = time 2000; grid [128, 128]; wall 774s; status ok
- command: `python -m labkit.run threads/fisim-beyond-laplacian/worlds/xcell-evo2-S/world.py --out threads/fisim-beyond-laplacian/packs/xcell-evo2-S --seeds 0 1 2 --frames 200 --spf 500`
- segmentation: matter > 0.35 of robust range [0.0, 1.8742], min area 6 px

## Measurements
- components: final 12, mean 10.6, max 12; occupancy final 0.13
- tracks: 36; persistent (alive >= 50% of run): 9; longest 201 frames; alive start-to-end: 1
- size of persistent tracks: max/min area ratio 3.64 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [12, 12, 12], H1 [0, 0, 0]
- motion: 23 long-lived tracks moved >= 1 body length; max speed 0.15/time; max body lengths 8.9
- replication: splits 13, persistent splits 7, max generation 2, merges 0, nucleations 0
- channel total drift (end/start - 1): [-0.2804, None, 4.635, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 1 at frame 101: holes 0, rim-vs-core 0.69, rim-vs-outside 0.58, heterogeneity 0.21; core [0.929, 0.603, 0.822, 0.862] rim [0.568, 0.932, 0.428, 0.561]
  - track 11 at frame 109: holes 0, rim-vs-core 0.70, rim-vs-outside 0.57, heterogeneity 0.21; core [0.931, 0.584, 0.83, 0.869] rim [0.579, 0.931, 0.436, 0.567]
  - track 19 at frame 131: holes 0, rim-vs-core 0.69, rim-vs-outside 0.60, heterogeneity 0.20; core [0.932, 0.616, 0.826, 0.93] rim [0.582, 0.933, 0.438, 0.614]
  - track 22 at frame 94: holes 0, rim-vs-core 0.71, rim-vs-outside 0.60, heterogeneity 0.21; core [0.932, 0.611, 0.826, 0.91] rim [0.569, 0.933, 0.428, 0.589]

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, lineage.png, timeseries.png, movie.mp4, metrics.json

Measurements are screens, not verdicts: judge them against the images.
