# Evidence pack: sporecell2-sel (seed 0)

- world: `../../../worlds/sporecell2-sel/world.py`, family `particle`
- parent: sporecell2; mutation: promoted L7 settings: mu=0.1 per copy, kind 1 catalyses 1.3x faster (neutral control: k_cat1=0.05)
- run: 201 frames x 100 steps x dt 0.02 = time 400; grid [128, 128]; wall 143s; status ok
- command: `python -m labkit.run threads/particle-life/worlds/sporecell2-sel/world.py --out threads/particle-life/packs/sporecell2-sel --seeds 0 1 2 --frames 200 --spf 100 --no-movie`
- segmentation: matter > 0.35 of robust range [0.0, 5.6861], min area 6 px

## Measurements
- components: final 11, mean 8.4, max 14; occupancy final 0.03
- tracks: 131; persistent (alive >= 50% of run): 2; longest 137 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 5.79 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [16, 12, 7], H1 [0, 0, 0]
- motion: 19 long-lived tracks moved >= 1 body length; max speed 0.346/time; max body lengths 3.0
- replication: splits 0, persistent splits 0, max generation 0, merges 2, nucleations 129
- channel total drift (end/start - 1): [-0.8989, 34.4, None, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 33 at frame 133: holes 0, rim-vs-core 0.34, rim-vs-outside 0.21, heterogeneity 0.06; core [0.019, 0.0, 0.0, 0.95] rim [0.033, 0.0, 0.0, 0.607]
  - track 57 at frame 143: holes 0, rim-vs-core 0.01, rim-vs-outside 0.00, heterogeneity 0.01; core [0.0, 1.0, 0.0, 0.022] rim [0.001, 1.0, 0.0, 0.034]
  - track 38 at frame 109: holes 0, rim-vs-core 0.29, rim-vs-outside 0.27, heterogeneity 0.05; core [0.002, 0.0, 0.0, 0.949] rim [0.004, 0.0, 0.0, 0.656]
  - track 55 at frame 123: holes 0, rim-vs-core 0.33, rim-vs-outside 0.22, heterogeneity 0.05; core [0.001, 0.011, 0.0, 0.936] rim [0.004, 0.01, 0.0, 0.61]

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, lineage.png, timeseries.png, particles.png, movie.mp4, metrics.json

Measurements are screens, not verdicts: judge them against the images.
