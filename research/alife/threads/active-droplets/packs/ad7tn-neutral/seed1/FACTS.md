# Evidence pack: ad7tn-neutral (seed 1)

- world: `../../../worlds/ad7tn-neutral/world.py`, family `phase-field`
- parent: ad7t-thick; mutation: neutral control for ad7t: all four alleles kp=4 (same mutation, dilution, ancestor phenotype)
- run: 201 frames x 200 steps x dt 0.5 = time 20000; grid [128, 128]; wall 434s; status ok
- command: `python -m labkit.run threads/active-droplets/worlds/ad7tn-neutral/world.py --out threads/active-droplets/packs/ad7tn-neutral --seeds 0 1 2 --frames 200 --no-movie`
- segmentation: matter > 0.35 of robust range [-1.0408, 1.2343], min area 6 px

## Measurements
- components: final 8, mean 6.6, max 8; occupancy final 0.05
- tracks: 13; persistent (alive >= 50% of run): 6; longest 201 frames; alive start-to-end: 2
- size of persistent tracks: max/min area ratio 6.38 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [8, 8, 8], H1 [0, 0, 0]
- motion: 0 long-lived tracks moved >= 1 body length; max speed 0/time; max body lengths 0.9
- replication: splits 4, persistent splits 3, max generation 1, merges 0, nucleations 0
- channel total drift (end/start - 1): [-0.0633, -0.238, None, None, None, None, -0.7519]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 1 at frame 101: holes 0, rim-vs-core 0.92, rim-vs-outside 0.60, heterogeneity 0.14; core [0.907, 0.059, 0.345, 0.0, 0.922, 0.0, 0.0] rim [0.499, 0.346, 0.933, 0.0, 0.423, 0.0, 0.0]
  - track 2 at frame 101: holes 0, rim-vs-core 0.82, rim-vs-outside 0.90, heterogeneity 0.20; core [0.941, 0.024, 0.196, 0.003, 0.4, 0.776, 0.002] rim [0.616, 0.261, 0.837, 0.001, 0.214, 0.525, 0.001]
  - track 4 at frame 57: holes 0, rim-vs-core 0.66, rim-vs-outside 0.97, heterogeneity 0.18; core [0.962, 0.02, 0.204, 0.0, 0.703, 0.624, 0.003] rim [0.735, 0.192, 0.618, 0.0, 0.599, 0.211, 0.001]
  - track 7 at frame 146: holes 0, rim-vs-core 0.84, rim-vs-outside 0.73, heterogeneity 0.13; core [0.904, 0.066, 0.366, 0.0, 0.0, 0.999, 0.0] rim [0.458, 0.367, 0.925, 0.0, 0.0, 0.666, 0.0]

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, lineage.png, timeseries.png, movie.mp4, metrics.json

Measurements are screens, not verdicts: judge them against the images.
