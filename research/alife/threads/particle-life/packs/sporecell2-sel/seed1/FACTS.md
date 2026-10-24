# Evidence pack: sporecell2-sel (seed 1)

- world: `../../../worlds/sporecell2-sel/world.py`, family `particle`
- parent: sporecell2; mutation: promoted L7 settings: mu=0.1 per copy, kind 1 catalyses 1.3x faster (neutral control: k_cat1=0.05)
- run: 201 frames x 100 steps x dt 0.02 = time 400; grid [128, 128]; wall 132s; status ok
- command: `python -m labkit.run threads/particle-life/worlds/sporecell2-sel/world.py --out threads/particle-life/packs/sporecell2-sel --seeds 0 1 2 --frames 200 --spf 100 --no-movie`
- segmentation: matter > 0.35 of robust range [0.0, 5.6312], min area 6 px

## Measurements
- components: final 14, mean 8.1, max 15; occupancy final 0.02
- tracks: 133; persistent (alive >= 50% of run): 1; longest 114 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 6.00 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [20, 18, 12], H1 [0, 0, 0]
- motion: 17 long-lived tracks moved >= 1 body length; max speed 0.275/time; max body lengths 3.0
- replication: splits 0, persistent splits 0, max generation 0, merges 0, nucleations 133
- channel total drift (end/start - 1): [-0.8892, 99.6, None, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 43 at frame 145: holes 0, rim-vs-core 0.19, rim-vs-outside 0.34, heterogeneity 0.03; core [0.0, 0.003, 0.0, 1.0] rim [0.002, 0.005, 0.0, 0.815]
  - track 38 at frame 126: holes 0, rim-vs-core 0.15, rim-vs-outside 0.31, heterogeneity 0.03; core [0.0, 0.999, 0.0, 0.019] rim [0.0, 0.848, 0.0, 0.012]
  - track 53 at frame 138: holes 0, rim-vs-core 0.24, rim-vs-outside 0.27, heterogeneity 0.03; core [0.0, 0.0, 0.0, 0.998] rim [0.0, 0.0, 0.0, 0.762]
  - track 56 at frame 131: holes 0, rim-vs-core 0.13, rim-vs-outside 0.25, heterogeneity 0.03; core [0.129, 1.0, 0.0, 0.0] rim [0.082, 0.876, 0.0, 0.0]

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, lineage.png, timeseries.png, particles.png, movie.mp4, metrics.json

Measurements are screens, not verdicts: judge them against the images.
