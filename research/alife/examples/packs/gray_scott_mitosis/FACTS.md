# Evidence pack: gray-scott-mitosis-ref (seed 0)

- world: `../../gray_scott_mitosis/world.py`, family `reaction-diffusion`
- parent: None; mutation: reference
- run: 161 frames x 50 steps x dt 1.0 = time 8000; grid [128, 128]; wall 4s; status ok
- command: `python -m labkit.run examples/gray_scott_mitosis/world.py --out examples/packs/gray_scott_mitosis --frames 160`
- segmentation: matter > 0.35 of robust range [0.0, 0.3881], min area 6 px

## Measurements
- components: final 72, mean 31.4, max 72; occupancy final 0.28
- tracks: 140; persistent (alive >= 50% of run): 6; longest 112 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 1.39 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [73, 73, 72], H1 [0, 0, 0]
- motion: 5 long-lived tracks moved >= 1 body length; max speed 0.00543/time; max body lengths 1.6
- replication: splits 68, persistent splits 63, max generation 5, merges 0, nucleations 0
- channel total drift (end/start - 1): [-0.2637, 11.0971]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 14 at frame 105: holes 0, rim-vs-core 0.24, rim-vs-outside 0.50, heterogeneity 0.19; core [0.157, 0.828] rim [0.299, 0.635]
  - track 34 at frame 117: holes 0, rim-vs-core 0.47, rim-vs-outside 0.30, heterogeneity 0.18; core [0.123, 0.874] rim [0.403, 0.499]
  - track 36 at frame 117: holes 0, rim-vs-core 0.49, rim-vs-outside 0.29, heterogeneity 0.19; core [0.13, 0.851] rim [0.43, 0.469]
  - track 100 at frame 143: holes 0, rim-vs-core 0.46, rim-vs-outside 0.30, heterogeneity 0.18; core [0.127, 0.844] rim [0.421, 0.486]

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, lineage.png, timeseries.png, movie.mp4, metrics.json

Measurements are screens, not verdicts: judge them against the images.
