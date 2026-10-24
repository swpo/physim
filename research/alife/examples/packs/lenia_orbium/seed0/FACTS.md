# Evidence pack: lenia-orbium-ref (seed 0)

- world: `../../../lenia_orbium/world.py`, family `lenia`
- parent: None; mutation: reference
- run: 151 frames x 2 steps x dt 0.1 = time 30; grid [128, 128]; wall 0s; status ok
- command: `python -m labkit.run examples/lenia_orbium/world.py --out examples/packs/lenia_orbium --frames 150 --seeds 0 1 2`
- segmentation: matter > 0.35 of robust range [0.0, 0.9862], min area 6 px

## Measurements
- components: final 4, mean 2.6, max 5; occupancy final 0.01
- tracks: 31; persistent (alive >= 50% of run): 2; longest 105 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 1.58 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [8, 3, 2], H1 [1, 0, 0]
- motion: 6 long-lived tracks moved >= 1 body length; max speed 5.82/time; max body lengths 15.1
- replication: splits 9, persistent splits 0, max generation 0, merges 4, nucleations 7
- channel total drift (end/start - 1): [-0.3226]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 13 at frame 97: holes 0, rim-vs-core 0.28, rim-vs-outside 0.43, heterogeneity 0.19; core [0.971] rim [0.696]
  - track 23 at frame 105: holes 0, rim-vs-core 0.29, rim-vs-outside 0.40, heterogeneity 0.20; core [0.958] rim [0.668]
  - track 0 at frame 25: holes 0, rim-vs-core 0.30, rim-vs-outside 0.40, heterogeneity 0.21; core [0.96] rim [0.664]
  - track 1 at frame 13: holes 0, rim-vs-core 0.28, rim-vs-outside 0.41, heterogeneity 0.20; core [0.979] rim [0.7]

## Warnings
- none

## Files
sheet.png, tracks.png, lineage.png, timeseries.png, movie.mp4, metrics.json

Measurements are screens, not verdicts: judge them against the images.
