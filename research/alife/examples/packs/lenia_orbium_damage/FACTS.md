# Evidence pack: lenia-orbium-ref (seed 0)

- world: `../../lenia_orbium/world.py`, family `lenia`
- parent: None; mutation: reference
- run: 151 frames x 2 steps x dt 0.1 = time 30; grid [128, 128]; wall 0s; status ok
- command: `python -m labkit.run examples/lenia_orbium/world.py --out examples/packs/lenia_orbium_damage --frames 150 --damage 40:0.4`
- segmentation: matter > 0.35 of robust range [0.0, 0.9423], min area 6 px

## Measurements
- components: final 1, mean 1.8, max 6; occupancy final 0.00
- tracks: 29; persistent (alive >= 50% of run): 1; longest 89 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 1.38 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [3, 1, 1], H1 [1, 0, 0]
- motion: 5 long-lived tracks moved >= 1 body length; max speed 5.9/time; max body lengths 12.8
- replication: splits 9, persistent splits 0, max generation 0, merges 4, nucleations 4
- channel total drift (end/start - 1): [-0.6772]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 28 at frame 106: holes 0, rim-vs-core 0.17, rim-vs-outside 0.48, heterogeneity 0.12; core [0.991] rim [0.822]
  - track 4 at frame 29: holes 0, rim-vs-core 0.23, rim-vs-outside 0.47, heterogeneity 0.16; core [0.995] rim [0.767]
  - track 16 at frame 48: holes 0, rim-vs-core 0.20, rim-vs-outside 0.47, heterogeneity 0.14; core [0.986] rim [0.79]
  - track 6 at frame 14: holes 0, rim-vs-core 0.22, rim-vs-outside 0.46, heterogeneity 0.18; core [0.994] rim [0.773]
- damage applied at frame 40: erased 26 px of a 63 px component

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, lineage.png, timeseries.png, movie.mp4, metrics.json

Measurements are screens, not verdicts: judge them against the images.
