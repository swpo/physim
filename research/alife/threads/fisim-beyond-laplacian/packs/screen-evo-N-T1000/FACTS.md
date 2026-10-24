# Evidence pack: xcell-evo-N (seed 0)

- world: `../../worlds/xcell-evo-N/world.py`, family `fisim-extended-rd`
- parent: xcell-her (sprint 1); maintenance/turnover idea from lenia-multichannel mcfd-MIRd; 5-px mutation patches + neutral arm from active-droplets ad5; mutation: Arm N of the sprint-2 evolution experiment. xcell-her minus its unused hdep channel plus one membrane-gated waste q (tau=40, D=2, K=0.15; turnover). No marker is planted: h-on kinds arise only from rare cell-scale h kicks (Poisson, rate 0.02 per time unit, Gaussian disk sigma 1.5, amplitude 2.5, anywhere in the box). Only bodies (+ v, w dress) are planted. Neutral arm: the marker has no effect on the cell.
- run: 101 frames x 500 steps x dt 0.02 = time 1000; grid [128, 128]; wall 415s; status ok
- command: `python -m labkit.run threads/fisim-beyond-laplacian/worlds/xcell-evo-N/world.py --out threads/fisim-beyond-laplacian/packs/screen-evo-N-T1000 --seeds 0 --frames 100 --spf 500`
- segmentation: matter > 0.35 of robust range [0.0, 1.8663], min area 6 px

## Measurements
- components: final 12, mean 11.7, max 12; occupancy final 0.13
- tracks: 14; persistent (alive >= 50% of run): 12; longest 101 frames; alive start-to-end: 9
- size of persistent tracks: max/min area ratio 1.71 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [12, 12, 12], H1 [0, 0, 0]
- motion: 13 long-lived tracks moved >= 1 body length; max speed 0.201/time; max body lengths 14.3
- replication: splits 2, persistent splits 2, max generation 2, merges 0, nucleations 0
- channel total drift (end/start - 1): [-0.258, None, 19.7413, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 1 at frame 50: holes 0, rim-vs-core 0.57, rim-vs-outside 0.53, heterogeneity 0.23; core [0.934, 0.612, 0.239, 0.891] rim [0.583, 0.943, 0.197, 0.583]
  - track 2 at frame 50: holes 0, rim-vs-core 0.56, rim-vs-outside 0.51, heterogeneity 0.16; core [0.932, 0.605, 0.091, 0.858] rim [0.587, 0.936, 0.048, 0.565]
  - track 3 at frame 50: holes 0, rim-vs-core 0.70, rim-vs-outside 0.56, heterogeneity 0.26; core [0.934, 0.612, 0.788, 0.848] rim [0.577, 0.94, 0.384, 0.549]
  - track 12 at frame 60: holes 0, rim-vs-core 0.58, rim-vs-outside 0.50, heterogeneity 0.16; core [0.928, 0.62, 0.09, 0.842] rim [0.559, 0.94, 0.046, 0.538]

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, lineage.png, timeseries.png, movie.mp4, metrics.json

Measurements are screens, not verdicts: judge them against the images.
