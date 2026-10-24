# Evidence pack: xcell-div (seed 0)

- world: `../../worlds/xcell-div/world.py`, family `fisim-extended-rd`
- parent: xcell-a; mutation: xcell-a + cargo feeds back on the body (K[u,c]=-0.25: the contained cargo activates u) + a global depletion channel (D=100, tau=10, K=1) that caps total body mass. Membrane-gated cargo makes bodies grow, elongate and divide; daughters inherit membrane and cargo.
- run: 201 frames x 100 steps x dt 0.02 = time 400; grid [160, 160]; wall 148s; status ok
- command: `python -m labkit.run threads/fisim-beyond-laplacian/worlds/xcell-div/world.py --out threads/fisim-beyond-laplacian/packs/xcell-div-damage --seeds 0 --damage 100:0.5`
- segmentation: matter > 0.35 of robust range [0.0, 1.881], min area 6 px

## Measurements
- components: final 23, mean 18.1, max 23; occupancy final 0.16
- tracks: 38; persistent (alive >= 50% of run): 21; longest 165 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 1.33 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [23, 23, 23], H1 [0, 0, 0]
- motion: 6 long-lived tracks moved >= 1 body length; max speed 0.07/time; max body lengths 1.3
- replication: splits 15, persistent splits 15, max generation 2, merges 0, nucleations 0
- channel total drift (end/start - 1): [0.8335, None, 1.0362]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 8 at frame 119: holes 0, rim-vs-core 0.60, rim-vs-outside 0.53, heterogeneity 0.20; core [0.938, 0.588, 0.877] rim [0.586, 0.932, 0.53]
  - track 10 at frame 119: holes 0, rim-vs-core 0.61, rim-vs-outside 0.52, heterogeneity 0.21; core [0.935, 0.604, 0.86] rim [0.565, 0.932, 0.504]
  - track 11 at frame 119: holes 0, rim-vs-core 0.60, rim-vs-outside 0.53, heterogeneity 0.20; core [0.938, 0.594, 0.872] rim [0.585, 0.933, 0.525]
  - track 22 at frame 136: holes 0, rim-vs-core 0.59, rim-vs-outside 0.53, heterogeneity 0.20; core [0.938, 0.603, 0.866] rim [0.587, 0.931, 0.522]
- damage applied at frame 100: erased 128 px of a 494 px component

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, lineage.png, timeseries.png, movie.mp4, metrics.json

Measurements are screens, not verdicts: judge them against the images.
