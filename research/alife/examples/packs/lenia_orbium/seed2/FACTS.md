# Evidence pack: lenia-orbium-ref (seed 2)

- world: `../../../lenia_orbium/world.py`, family `lenia`
- parent: None; mutation: reference
- run: 151 frames x 2 steps x dt 0.1 = time 30; grid [128, 128]; wall 0s; status ok
- command: `python -m labkit.run examples/lenia_orbium/world.py --out examples/packs/lenia_orbium --frames 150 --seeds 0 1 2`
- segmentation: matter > 0.35 of robust range [0.0, 0.9581], min area 6 px

## Measurements
- components: final 1, mean 2.0, max 7; occupancy final 0.00
- tracks: 49; persistent (alive >= 50% of run): 1; longest 101 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 1.28 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [3, 1, 1], H1 [2, 0, 0]
- motion: 4 long-lived tracks moved >= 1 body length; max speed 6.07/time; max body lengths 15.1
- replication: splits 9, persistent splits 0, max generation 0, merges 10, nucleations 16
- channel total drift (end/start - 1): [-0.677]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 48 at frame 101: holes 0, rim-vs-core 0.14, rim-vs-outside 0.50, heterogeneity 0.13; core [0.997] rim [0.855]
  - track 11 at frame 24: holes 0, rim-vs-core 0.20, rim-vs-outside 0.56, heterogeneity 0.18; core [0.993] rim [0.792]
  - track 14 at frame 21: holes 0, rim-vs-core 0.13, rim-vs-outside 0.56, heterogeneity 0.14; core [0.997] rim [0.87]
  - track 10 at frame 20: holes 0, rim-vs-core 0.21, rim-vs-outside 0.40, heterogeneity 0.22; core [0.995] rim [0.78]

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, lineage.png, timeseries.png, movie.mp4, metrics.json

Measurements are screens, not verdicts: judge them against the images.
