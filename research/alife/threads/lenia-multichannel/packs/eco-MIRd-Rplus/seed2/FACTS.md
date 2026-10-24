# Evidence pack: eco-MIRd-Rplus (seed 2)

- world: `../../../worlds/eco-MIRd-Rplus/world.py`, family `lenia`
- parent: mcf-MIRd; mutation: two species (separate channel sets and rules) sharing one food field with space exclusion
- run: 301 frames x 10 steps x dt 0.1 = time 300; grid [160, 160]; wall 78s; status ok
- command: `python -m labkit.run threads/lenia-multichannel/worlds/eco-MIRd-Rplus/world.py --out threads/lenia-multichannel/packs/eco-MIRd-Rplus --seeds 0 1 2 --frames 300`
- segmentation: matter > 0.35 of robust range [0.0, 1.0], min area 6 px

## Measurements
- components: final 76, mean 67.5, max 93; occupancy final 0.21
- tracks: 1896; persistent (alive >= 50% of run): 11; longest 254 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 14.40 (1 = constant size)
- enclosures: components with a hole mean 2.62, final 2; holes at thresholds 0.2/0.35/0.5 final [1, 2, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [122, 89, 57], H1 [12, 2, 0]
- motion: 5 long-lived tracks moved >= 1 body length; max speed 0.197/time; max body lengths 1.8
- replication: splits 479, persistent splits 4, max generation 2, merges 409, nucleations 534
- channel total drift (end/start - 1): [0.7137, 0.5979, 0.5781, 5.7007, 4.5681, 5.5376, -0.8036]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 339 at frame 174: holes 0, rim-vs-core 0.09, rim-vs-outside 1.25, heterogeneity 0.09; core [0.0, 0.0, 0.0, 1.0, 0.895, 1.0, 0.522] rim [0.0, 0.0, 0.0, 0.915, 0.925, 0.982, 0.514]
  - track 464 at frame 176: holes 0, rim-vs-core 0.12, rim-vs-outside 1.20, heterogeneity 0.09; core [0.0, 0.0, 0.0, 1.0, 0.92, 0.883, 0.425] rim [0.0, 0.0, 0.0, 0.916, 1.0, 0.913, 0.416]
  - track 656 at frame 192: holes 0, rim-vs-core 0.24, rim-vs-outside 1.19, heterogeneity 0.12; core [0.0, 0.0, 0.0, 0.992, 0.987, 0.4, 0.208] rim [0.0, 0.0, 0.0, 0.824, 0.957, 0.573, 0.224]
  - track 1134 at frame 232: holes 0, rim-vs-core 0.60, rim-vs-outside 0.85, heterogeneity 0.12; core [0.0, 0.0, 0.0, 1.0, 1.0, 0.885, 0.32] rim [0.0, 0.0, 0.0, 0.736, 1.0, 0.343, 0.318]

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, lineage.png, timeseries.png, movie.mp4, metrics.json

Measurements are screens, not verdicts: judge them against the images.
