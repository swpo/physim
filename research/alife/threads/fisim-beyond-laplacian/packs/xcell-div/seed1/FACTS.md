# Evidence pack: xcell-div (seed 1)

- world: `../../../worlds/xcell-div/world.py`, family `fisim-extended-rd`
- parent: xcell-a; mutation: xcell-a + cargo feeds back on the body (K[u,c]=-0.25: the contained cargo activates u) + a global depletion channel (D=100, tau=10, K=1) that caps total body mass. Membrane-gated cargo makes bodies grow, elongate and divide; daughters inherit membrane and cargo.
- run: 201 frames x 100 steps x dt 0.02 = time 400; grid [160, 160]; wall 133s; status ok
- command: `python -m labkit.run threads/fisim-beyond-laplacian/worlds/xcell-div/world.py --out threads/fisim-beyond-laplacian/packs/xcell-div --seeds 0 1 2`
- segmentation: matter > 0.35 of robust range [0.0, 1.8834], min area 6 px

## Measurements
- components: final 23, mean 18.6, max 23; occupancy final 0.18
- tracks: 38; persistent (alive >= 50% of run): 23; longest 168 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 3.30 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [24, 23, 23], H1 [0, 0, 0]
- motion: 4 long-lived tracks moved >= 1 body length; max speed 0.0686/time; max body lengths 1.4
- replication: splits 15, persistent splits 15, max generation 2, merges 0, nucleations 0
- channel total drift (end/start - 1): [0.9638, None, 1.146]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 8 at frame 118: holes 0, rim-vs-core 0.60, rim-vs-outside 0.53, heterogeneity 0.20; core [0.936, 0.61, 0.869] rim [0.574, 0.938, 0.515]
  - track 9 at frame 118: holes 0, rim-vs-core 0.58, rim-vs-outside 0.54, heterogeneity 0.20; core [0.937, 0.613, 0.859] rim [0.585, 0.93, 0.517]
  - track 13 at frame 119: holes 0, rim-vs-core 0.61, rim-vs-outside 0.53, heterogeneity 0.21; core [0.931, 0.604, 0.87] rim [0.568, 0.939, 0.516]
  - track 22 at frame 136: holes 0, rim-vs-core 0.60, rim-vs-outside 0.54, heterogeneity 0.20; core [0.938, 0.595, 0.882] rim [0.588, 0.941, 0.533]

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, lineage.png, timeseries.png, movie.mp4, metrics.json

Measurements are screens, not verdicts: judge them against the images.
