# Evidence pack: sporecell2-sel (seed 2)

- world: `../../../worlds/sporecell2-sel/world.py`, family `particle`
- parent: sporecell2; mutation: promoted L7 settings: mu=0.1 per copy, kind 1 catalyses 1.3x faster (neutral control: k_cat1=0.05)
- run: 201 frames x 100 steps x dt 0.02 = time 400; grid [128, 128]; wall 139s; status ok
- command: `python -m labkit.run threads/particle-life/worlds/sporecell2-sel/world.py --out threads/particle-life/packs/sporecell2-sel --seeds 0 1 2 --frames 200 --spf 100 --no-movie`
- segmentation: matter > 0.35 of robust range [0.0, 5.6038], min area 6 px

## Measurements
- components: final 12, mean 9.0, max 14; occupancy final 0.03
- tracks: 134; persistent (alive >= 50% of run): 1; longest 169 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 9.67 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [15, 15, 7], H1 [0, 0, 0]
- motion: 12 long-lived tracks moved >= 1 body length; max speed 0.518/time; max body lengths 3.0
- replication: splits 0, persistent splits 0, max generation 0, merges 0, nucleations 134
- channel total drift (end/start - 1): [-0.8943, 43.88, None, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 1 at frame 116: holes 0, rim-vs-core 0.08, rim-vs-outside 0.28, heterogeneity 0.02; core [0.0, 1.0, 0.0, 0.064] rim [0.0, 0.928, 0.0, 0.036]
  - track 56 at frame 146: holes 0, rim-vs-core 0.05, rim-vs-outside 0.29, heterogeneity 0.02; core [0.0, 1.0, 0.0, 0.071] rim [0.0, 0.963, 0.0, 0.041]
  - track 28 at frame 108: holes 0, rim-vs-core 0.18, rim-vs-outside 0.15, heterogeneity 0.03; core [0.0, 0.0, 0.0, 0.797] rim [0.0, 0.0, 0.0, 0.621]
  - track 11 at frame 87: holes 0, rim-vs-core 0.06, rim-vs-outside 0.29, heterogeneity 0.04; core [0.0, 1.0, 0.092, 0.006] rim [0.0, 0.95, 0.064, 0.003]

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, lineage.png, timeseries.png, particles.png, movie.mp4, metrics.json

Measurements are screens, not verdicts: judge them against the images.
