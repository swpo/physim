# Evidence pack: ad7n-neutral (seed 0)

- world: `../../../worlds/ad7n-neutral/world.py`, family `phase-field`
- parent: ad7-gated; mutation: neutral control: all four alleles make no amphiphile (kp=0), same mutation and dilution
- run: 201 frames x 200 steps x dt 0.5 = time 20000; grid [128, 128]; wall 421s; status ok
- command: `python -m labkit.run threads/active-droplets/worlds/ad7n-neutral/world.py --out threads/active-droplets/packs/ad7n-neutral --seeds 0 1 2 --frames 200`
- segmentation: matter > 0.35 of robust range [-1.0599, 1.4701], min area 6 px

## Measurements
- components: final 5, mean 4.2, max 5; occupancy final 0.09
- tracks: 8; persistent (alive >= 50% of run): 4; longest 201 frames; alive start-to-end: 1
- size of persistent tracks: max/min area ratio 3.67 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [5, 5, 5], H1 [0, 0, 0]
- motion: 1 long-lived tracks moved >= 1 body length; max speed 0.00117/time; max body lengths 1.0
- replication: splits 2, persistent splits 2, max generation 1, merges 0, nucleations 0
- channel total drift (end/start - 1): [0.0181, -0.4223, None, 0.794, None, None, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 1 at frame 101: holes 0, rim-vs-core 0.46, rim-vs-outside 0.72, heterogeneity 0.07; core [0.963, 0.029, 0.0, 0.92, 0.0, 0.0, 0.003] rim [0.709, 0.159, 0.0, 0.56, 0.0, 0.0, 0.002]
  - track 4 at frame 129: holes 0, rim-vs-core 0.34, rim-vs-outside 0.72, heterogeneity 0.07; core [0.952, 0.051, 0.0, 0.855, 0.0, 0.0, 0.0] rim [0.735, 0.14, 0.0, 0.607, 0.0, 0.0, 0.0]
  - track 5 at frame 129: holes 0, rim-vs-core 0.50, rim-vs-outside 0.56, heterogeneity 0.07; core [0.957, 0.052, 0.0, 0.858, 0.006, 0.01, 0.005] rim [0.638, 0.178, 0.0, 0.492, 0.004, 0.006, 0.003]
  - track 3 at frame 55: holes 0, rim-vs-core 0.38, rim-vs-outside 0.84, heterogeneity 0.08; core [0.942, 0.023, 0.0, 0.91, 0.0, 0.0, 0.444] rim [0.771, 0.132, 0.0, 0.623, 0.0, 0.0, 0.312]

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, lineage.png, timeseries.png, movie.mp4, metrics.json

Measurements are screens, not verdicts: judge them against the images.
