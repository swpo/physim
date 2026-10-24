# Evidence pack: xcell-div (seed 0)

- world: `../../../worlds/xcell-div/world.py`, family `fisim-extended-rd`
- parent: xcell-a; mutation: xcell-a + cargo feeds back on the body (K[u,c]=-0.25: the contained cargo activates u) + a global depletion channel (D=100, tau=10, K=1) that caps total body mass. Membrane-gated cargo makes bodies grow, elongate and divide; daughters inherit membrane and cargo.
- run: 201 frames x 100 steps x dt 0.02 = time 400; grid [160, 160]; wall 141s; status ok
- command: `python -m labkit.run threads/fisim-beyond-laplacian/worlds/xcell-div/world.py --out threads/fisim-beyond-laplacian/packs/xcell-div --seeds 0 1 2`
- segmentation: matter > 0.35 of robust range [0.0, 1.8824], min area 6 px

## Measurements
- components: final 21, mean 17.3, max 21; occupancy final 0.17
- tracks: 34; persistent (alive >= 50% of run): 21; longest 201 frames; alive start-to-end: 1
- size of persistent tracks: max/min area ratio 4.82 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [22, 21, 21], H1 [0, 0, 0]
- motion: 8 long-lived tracks moved >= 1 body length; max speed 0.0807/time; max body lengths 1.9
- replication: splits 13, persistent splits 13, max generation 2, merges 0, nucleations 0
- channel total drift (end/start - 1): [0.905, None, 1.0917]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 6 at frame 101: holes 0, rim-vs-core 0.37, rim-vs-outside 0.75, heterogeneity 0.15; core [0.949, 0.647, 0.823] rim [0.702, 0.829, 0.612]
  - track 8 at frame 119: holes 0, rim-vs-core 0.60, rim-vs-outside 0.53, heterogeneity 0.20; core [0.935, 0.592, 0.876] rim [0.582, 0.932, 0.528]
  - track 10 at frame 119: holes 0, rim-vs-core 0.60, rim-vs-outside 0.52, heterogeneity 0.20; core [0.934, 0.612, 0.859] rim [0.568, 0.931, 0.507]
  - track 22 at frame 136: holes 0, rim-vs-core 0.59, rim-vs-outside 0.53, heterogeneity 0.20; core [0.936, 0.61, 0.862] rim [0.584, 0.931, 0.519]

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, lineage.png, timeseries.png, movie.mp4, metrics.json

Measurements are screens, not verdicts: judge them against the images.
