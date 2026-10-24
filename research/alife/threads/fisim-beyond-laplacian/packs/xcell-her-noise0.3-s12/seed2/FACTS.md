# Evidence pack: xcell-her-noise0.3 (seed 2)

- world: `../../../worlds/xcell-her-noise0.3/world.py`, family `fisim-extended-rd`
- parent: xcell-her; mutation: xcell-her + additive noise (amplitude 0.3, blobkit convention noise*sqrt(dt)*N(0,1) on activators) so that marker kinds can switch during the run (variation)
- run: 201 frames x 100 steps x dt 0.02 = time 400; grid [160, 160]; wall 241s; status ok
- command: `python -m labkit.run threads/fisim-beyond-laplacian/worlds/xcell-her-noise0.3/world.py --out threads/fisim-beyond-laplacian/packs/xcell-her-noise0.3-s12 --seeds 1 2`
- segmentation: matter > 0.35 of robust range [0.0, 1.9468], min area 6 px

## Measurements
- components: final 26, mean 19.5, max 26; occupancy final 0.18
- tracks: 42; persistent (alive >= 50% of run): 19; longest 201 frames; alive start-to-end: 1
- size of persistent tracks: max/min area ratio 2.08 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [26, 26, 26], H1 [0, 0, 0]
- motion: 8 long-lived tracks moved >= 1 body length; max speed 0.0997/time; max body lengths 1.8
- replication: splits 16, persistent splits 15, max generation 2, merges 0, nucleations 0
- channel total drift (end/start - 1): [0.5968, None, 1.0851]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 8 at frame 101: holes 0, rim-vs-core 0.34, rim-vs-outside 0.54, heterogeneity 0.15; core [0.914, 0.536, 0.112] rim [0.689, 0.784, 0.065]
  - track 13 at frame 114: holes 0, rim-vs-core 0.47, rim-vs-outside 0.43, heterogeneity 0.15; core [0.925, 0.561, 0.101] rim [0.585, 0.877, 0.063]
  - track 14 at frame 118: holes 0, rim-vs-core 0.22, rim-vs-outside 0.56, heterogeneity 0.14; core [0.91, 0.637, 0.083] rim [0.716, 0.731, 0.073]
  - track 20 at frame 124: holes 0, rim-vs-core 0.44, rim-vs-outside 0.43, heterogeneity 0.14; core [0.93, 0.614, 0.118] rim [0.595, 0.889, 0.047]

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, lineage.png, timeseries.png, movie.mp4, metrics.json

Measurements are screens, not verdicts: judge them against the images.
