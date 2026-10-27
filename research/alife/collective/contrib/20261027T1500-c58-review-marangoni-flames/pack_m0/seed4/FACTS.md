# Evidence pack: marangoni-flames (seed 4)

- world: `../../../20261027T0319-c51-marangoni-flames-negative/world.py`, family `reactive-marangoni`
- parent: None; mutation: -
- run: 601 frames x 25 steps x dt 0.04 = time 600; grid [128, 128]; wall 51s; status ok
- command: `python -m labkit.run collective/contrib/20261027T0319-c51-marangoni-flames-negative/world.py --out collective/contrib/20261027T1500-c58-review-marangoni-flames/pack_m0 --seeds 4 5 --frames 600 --spf 25 --no-movie`
- segmentation: matter > 0.34 of robust range [0.0, 0.7327], min area 6 px

## Measurements
- components: final 0, mean 0.6, max 41; occupancy final 0.00
- tracks: 92; persistent (alive >= 50% of run): 0; longest 25 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 0.00 (1 = constant size)
- enclosures: components with a hole mean 0.03, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [0, 0, 0], H1 [0, 0, 0]
- motion: 0 long-lived tracks moved >= 1 body length; max speed 0/time; max body lengths 0.7
- replication (lineage window K = 20 frames = time 20, default): splits 22, persistent splits 0 (0 more failed only because the siblings re-merged within K), max generation 0, merges 4, merge/split ratio 0.182, nucleations 3
- channel total drift (end/start - 1): [-1.0, -0.0, None, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 16 at frame 15: holes 0, rim-vs-core 0.21, rim-vs-outside 0.66, heterogeneity 0.05; core [0.997, 0.006, 0.0, 1.0] rim [0.806, 0.087, 0.0, 1.0]
  - track 14 at frame 15: holes 0, rim-vs-core 0.19, rim-vs-outside 0.57, heterogeneity 0.04; core [0.975, 0.008, 0.0, 1.0] rim [0.797, 0.086, 0.0, 1.0]
  - track 17 at frame 15: holes 0, rim-vs-core 0.17, rim-vs-outside 0.57, heterogeneity 0.04; core [1.0, 0.006, 0.0, 1.0] rim [0.847, 0.075, 0.0, 1.0]
  - track 7 at frame 5: holes 0, rim-vs-core 0.15, rim-vs-outside 1.24, heterogeneity 0.07; core [1.0, 0.004, 0.0, 1.0] rim [0.911, 0.129, 0.0, 1.0]
- radial profiles: no component with area >= 12 px at the sampled frames

## Warnings
- no components at the end: matter died out or fell below threshold
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
