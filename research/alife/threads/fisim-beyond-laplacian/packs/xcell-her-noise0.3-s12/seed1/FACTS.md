# Evidence pack: xcell-her-noise0.3 (seed 1)

- world: `../../../worlds/xcell-her-noise0.3/world.py`, family `fisim-extended-rd`
- parent: xcell-her; mutation: xcell-her + additive noise (amplitude 0.3, blobkit convention noise*sqrt(dt)*N(0,1) on activators) so that marker kinds can switch during the run (variation)
- run: 201 frames x 100 steps x dt 0.02 = time 400; grid [160, 160]; wall 255s; status ok
- command: `python -m labkit.run threads/fisim-beyond-laplacian/worlds/xcell-her-noise0.3/world.py --out threads/fisim-beyond-laplacian/packs/xcell-her-noise0.3-s12 --seeds 1 2`
- segmentation: matter > 0.35 of robust range [0.0, 1.9486], min area 6 px

## Measurements
- components: final 25, mean 20.4, max 25; occupancy final 0.17
- tracks: 39; persistent (alive >= 50% of run): 24; longest 201 frames; alive start-to-end: 2
- size of persistent tracks: max/min area ratio 2.29 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [25, 25, 25], H1 [0, 0, 0]
- motion: 10 long-lived tracks moved >= 1 body length; max speed 0.205/time; max body lengths 2.0
- replication: splits 14, persistent splits 14, max generation 2, merges 0, nucleations 1
- channel total drift (end/start - 1): [0.5534, None, 1.0042]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 5 at frame 101: holes 0, rim-vs-core 0.46, rim-vs-outside 0.43, heterogeneity 0.15; core [0.916, 0.595, 0.115] rim [0.573, 0.895, 0.073]
  - track 7 at frame 101: holes 0, rim-vs-core 0.67, rim-vs-outside 0.60, heterogeneity 0.24; core [0.928, 0.545, 0.943] rim [0.583, 0.881, 0.471]
  - track 11 at frame 114: holes 0, rim-vs-core 0.45, rim-vs-outside 0.43, heterogeneity 0.15; core [0.914, 0.592, 0.095] rim [0.577, 0.888, 0.059]
  - track 27 at frame 141: holes 0, rim-vs-core 0.61, rim-vs-outside 0.59, heterogeneity 0.23; core [0.918, 0.573, 0.929] rim [0.579, 0.894, 0.536]

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, lineage.png, timeseries.png, movie.mp4, metrics.json

Measurements are screens, not verdicts: judge them against the images.
