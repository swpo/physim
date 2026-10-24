# Evidence pack: eco-MIRd-Rplus (seed 1)

- world: `../../../worlds/eco-MIRd-Rplus/world.py`, family `lenia`
- parent: mcf-MIRd; mutation: two species (separate channel sets and rules) sharing one food field with space exclusion
- run: 301 frames x 10 steps x dt 0.1 = time 300; grid [160, 160]; wall 77s; status ok
- command: `python -m labkit.run threads/lenia-multichannel/worlds/eco-MIRd-Rplus/world.py --out threads/lenia-multichannel/packs/eco-MIRd-Rplus --seeds 0 1 2 --frames 300`
- segmentation: matter > 0.35 of robust range [0.0, 1.0], min area 6 px

## Measurements
- components: final 65, mean 70.2, max 97; occupancy final 0.24
- tracks: 2042; persistent (alive >= 50% of run): 8; longest 230 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 3.67 (1 = constant size)
- enclosures: components with a hole mean 3.00, final 5; holes at thresholds 0.2/0.35/0.5 final [3, 5, 7]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [133, 82, 46], H1 [23, 7, 4]
- motion: 6 long-lived tracks moved >= 1 body length; max speed 0.231/time; max body lengths 2.2
- replication: splits 496, persistent splits 2, max generation 1, merges 494, nucleations 569
- channel total drift (end/start - 1): [2.8441, 2.0032, 2.31, 6.0499, 3.9947, 5.4639, -0.8178]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 610 at frame 187: holes 0, rim-vs-core 0.21, rim-vs-outside 1.18, heterogeneity 0.08; core [0.0, 0.0, 0.0, 1.0, 0.819, 1.0, 0.42] rim [0.0, 0.0, 0.0, 0.896, 1.0, 0.975, 0.411]
  - track 678 at frame 189: holes 0, rim-vs-core 0.18, rim-vs-outside 1.24, heterogeneity 0.09; core [0.0, 0.0, 0.0, 1.0, 0.879, 1.0, 0.539] rim [0.0, 0.0, 0.0, 0.892, 1.0, 0.919, 0.53]
  - track 693 at frame 192: holes 0, rim-vs-core 0.13, rim-vs-outside 0.98, heterogeneity 0.13; core [0.0, 0.0, 0.0, 0.962, 0.947, 0.589, 0.059] rim [0.0, 0.0, 0.0, 0.841, 0.955, 0.564, 0.079]

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, lineage.png, timeseries.png, movie.mp4, metrics.json

Measurements are screens, not verdicts: judge them against the images.
