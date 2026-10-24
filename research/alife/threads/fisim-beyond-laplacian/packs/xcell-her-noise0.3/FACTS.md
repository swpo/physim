# Evidence pack: xcell-her-noise0.3 (seed 0)

- world: `../../worlds/xcell-her-noise0.3/world.py`, family `fisim-extended-rd`
- parent: xcell-her; mutation: xcell-her + additive noise (amplitude 0.3, blobkit convention noise*sqrt(dt)*N(0,1) on activators) so that marker kinds can switch during the run (variation)
- run: 201 frames x 100 steps x dt 0.02 = time 400; grid [160, 160]; wall 263s; status ok
- command: `python -m labkit.run threads/fisim-beyond-laplacian/worlds/xcell-her-noise0.3/world.py --out threads/fisim-beyond-laplacian/packs/xcell-her-noise0.3 --seeds 0`
- segmentation: matter > 0.35 of robust range [0.0, 1.9463], min area 6 px

## Measurements
- components: final 24, mean 19.5, max 24; occupancy final 0.17
- tracks: 37; persistent (alive >= 50% of run): 20; longest 201 frames; alive start-to-end: 3
- size of persistent tracks: max/min area ratio 8.91 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [24, 24, 24], H1 [0, 0, 0]
- motion: 6 long-lived tracks moved >= 1 body length; max speed 0.234/time; max body lengths 1.6
- replication: splits 13, persistent splits 13, max generation 2, merges 0, nucleations 1
- channel total drift (end/start - 1): [0.5329, None, 1.1538]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 2 at frame 101: holes 0, rim-vs-core 0.62, rim-vs-outside 0.61, heterogeneity 0.23; core [0.926, 0.554, 0.942] rim [0.6, 0.878, 0.524]
  - track 6 at frame 101: holes 0, rim-vs-core 0.49, rim-vs-outside 0.42, heterogeneity 0.16; core [0.916, 0.552, 0.106] rim [0.565, 0.886, 0.049]
  - track 7 at frame 101: holes 0, rim-vs-core 0.47, rim-vs-outside 0.42, heterogeneity 0.15; core [0.933, 0.57, 0.104] rim [0.583, 0.88, 0.051]
  - track 25 at frame 136: holes 0, rim-vs-core 0.47, rim-vs-outside 0.44, heterogeneity 0.15; core [0.918, 0.548, 0.096] rim [0.597, 0.882, 0.054]

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, lineage.png, timeseries.png, movie.mp4, metrics.json

Measurements are screens, not verdicts: judge them against the images.
