# Evidence pack: xcell-div (seed 2)

- world: `../../../worlds/xcell-div/world.py`, family `fisim-extended-rd`
- parent: xcell-a; mutation: xcell-a + cargo feeds back on the body (K[u,c]=-0.25: the contained cargo activates u) + a global depletion channel (D=100, tau=10, K=1) that caps total body mass. Membrane-gated cargo makes bodies grow, elongate and divide; daughters inherit membrane and cargo.
- run: 201 frames x 100 steps x dt 0.02 = time 400; grid [160, 160]; wall 133s; status ok
- command: `python -m labkit.run threads/fisim-beyond-laplacian/worlds/xcell-div/world.py --out threads/fisim-beyond-laplacian/packs/xcell-div --seeds 0 1 2`
- segmentation: matter > 0.35 of robust range [0.0, 1.8839], min area 6 px

## Measurements
- components: final 23, mean 18.4, max 23; occupancy final 0.18
- tracks: 38; persistent (alive >= 50% of run): 23; longest 167 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 3.43 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [24, 23, 23], H1 [0, 0, 0]
- motion: 7 long-lived tracks moved >= 1 body length; max speed 0.13/time; max body lengths 1.6
- replication: splits 15, persistent splits 15, max generation 2, merges 0, nucleations 0
- channel total drift (end/start - 1): [0.9539, None, 1.1349]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 9 at frame 118: holes 0, rim-vs-core 0.60, rim-vs-outside 0.52, heterogeneity 0.20; core [0.934, 0.608, 0.865] rim [0.572, 0.933, 0.513]
  - track 11 at frame 119: holes 0, rim-vs-core 0.60, rim-vs-outside 0.52, heterogeneity 0.20; core [0.932, 0.605, 0.863] rim [0.57, 0.931, 0.512]
  - track 12 at frame 119: holes 0, rim-vs-core 0.60, rim-vs-outside 0.53, heterogeneity 0.20; core [0.936, 0.595, 0.874] rim [0.58, 0.932, 0.523]
  - track 24 at frame 138: holes 0, rim-vs-core 0.60, rim-vs-outside 0.53, heterogeneity 0.21; core [0.935, 0.602, 0.87] rim [0.575, 0.938, 0.52]

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, lineage.png, timeseries.png, movie.mp4, metrics.json

Measurements are screens, not verdicts: judge them against the images.
