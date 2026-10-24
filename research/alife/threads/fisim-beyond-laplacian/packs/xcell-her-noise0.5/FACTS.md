# Evidence pack: xcell-her-noise0.5 (seed 0)

- world: `../../worlds/xcell-her-noise0.5/world.py`, family `fisim-extended-rd`
- parent: xcell-her; mutation: xcell-her + additive noise (amplitude 0.5, blobkit convention noise*sqrt(dt)*N(0,1) on activators) so that marker kinds can switch during the run (variation)
- run: 201 frames x 100 steps x dt 0.02 = time 400; grid [160, 160]; wall 255s; status ok
- command: `python -m labkit.run threads/fisim-beyond-laplacian/worlds/xcell-her-noise0.5/world.py --out threads/fisim-beyond-laplacian/packs/xcell-her-noise0.5 --seeds 0`
- segmentation: matter > 0.35 of robust range [0.0, 2.0193], min area 6 px

## Measurements
- components: final 29, mean 26.5, max 29; occupancy final 0.18
- tracks: 33; persistent (alive >= 50% of run): 28; longest 201 frames; alive start-to-end: 9
- size of persistent tracks: max/min area ratio 31.25 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [29, 29, 29], H1 [0, 0, 0]
- motion: 9 long-lived tracks moved >= 1 body length; max speed 0.0881/time; max body lengths 1.6
- replication: splits 4, persistent splits 4, max generation 1, merges 0, nucleations 15
- channel total drift (end/start - 1): [0.6891, None, 1.119]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 0 at frame 101: holes 0, rim-vs-core 0.28, rim-vs-outside 0.84, heterogeneity 0.20; core [0.875, 0.615, 0.95] rim [0.722, 0.733, 0.742]
  - track 1 at frame 101: holes 0, rim-vs-core 0.62, rim-vs-outside 0.46, heterogeneity 0.23; core [0.886, 0.613, 0.886] rim [0.555, 0.874, 0.426]
  - track 2 at frame 101: holes 0, rim-vs-core 0.47, rim-vs-outside 0.61, heterogeneity 0.20; core [0.875, 0.643, 0.922] rim [0.566, 0.879, 0.651]
  - track 25 at frame 133: holes 0, rim-vs-core 0.42, rim-vs-outside 0.42, heterogeneity 0.15; core [0.897, 0.571, 0.11] rim [0.578, 0.848, 0.077]

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, lineage.png, timeseries.png, movie.mp4, metrics.json

Measurements are screens, not verdicts: judge them against the images.
