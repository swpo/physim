# Evidence pack: xcell-turn (seed 1)

- world: `../../../worlds/xcell-turn/world.py`, family `fisim-extended-rd`
- parent: xcell-div; mutation: xcell-div + a slow waste channel q (tau=40, D=2) produced by the body, trapped by the same membrane gate (D_q exp(-5m)) and inhibiting the body (K=+0.3). Trapped waste ages cells; division dilutes it; cells die and the freed global resource lets others divide (turnover).
- run: 201 frames x 200 steps x dt 0.02 = time 800; grid [128, 128]; wall 201s; status ok
- command: `python -m labkit.run threads/fisim-beyond-laplacian/worlds/xcell-turn/world.py --out threads/fisim-beyond-laplacian/packs/xcell-turn --seeds 0 1 2`
- segmentation: matter > 0.35 of robust range [0.0, 1.8876], min area 6 px

## Measurements
- components: final 20, mean 15.3, max 20; occupancy final 0.18
- tracks: 46; persistent (alive >= 50% of run): 19; longest 174 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 2.25 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [20, 20, 20], H1 [0, 0, 0]
- motion: 25 long-lived tracks moved >= 1 body length; max speed 0.351/time; max body lengths 15.9
- replication: splits 19, persistent splits 19, max generation 6, merges 0, nucleations 0
- channel total drift (end/start - 1): [0.2964, None, 0.3242, -0.166]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 16 at frame 114: holes 0, rim-vs-core 0.63, rim-vs-outside 0.54, heterogeneity 0.21; core [0.922, 0.672, 0.852, 0.619] rim [0.566, 0.904, 0.503, 0.305]
  - track 17 at frame 114: holes 0, rim-vs-core 0.68, rim-vs-outside 0.57, heterogeneity 0.20; core [0.916, 0.694, 0.868, 0.771] rim [0.581, 0.925, 0.531, 0.347]
  - track 22 at frame 119: holes 0, rim-vs-core 0.63, rim-vs-outside 0.55, heterogeneity 0.21; core [0.924, 0.646, 0.861, 0.629] rim [0.577, 0.904, 0.518, 0.322]
  - track 44 at frame 182: holes 0, rim-vs-core 0.62, rim-vs-outside 0.54, heterogeneity 0.21; core [0.925, 0.663, 0.846, 0.588] rim [0.571, 0.905, 0.502, 0.297]

## Warnings
- none

## Files
sheet.png, tracks.png, lineage.png, timeseries.png, movie.mp4, metrics.json

Measurements are screens, not verdicts: judge them against the images.
