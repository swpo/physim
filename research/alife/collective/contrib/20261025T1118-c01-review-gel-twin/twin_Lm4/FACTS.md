# Evidence pack: active-gel-fed-comets-twin (seed 3)

- world: `../../20261025T1046-c09-active-gel-bd-twin/world_twin_Lm4.py`, family `active-gel`
- parent: none (new class); mutation: new class: advection of stress generator and regulator by a contractile active-gel flow
- run: 201 frames x 100 steps x dt 0.01 = time 200; grid [128, 128]; wall 55s; status ok
- command: `python -m labkit.run collective/contrib/20261025T1046-c09-active-gel-bd-twin/world_twin_Lm4.py --out collective/contrib/20261025T1118-c01-review-gel-twin/twin_Lm4 --seeds 3 --frames 200 --no-movie`
- segmentation: matter > 0.60 of robust range [0.027, 1.6578], min area 6 px

## Measurements
- components: final 0, mean 1.1, max 50; occupancy final 0.00
- tracks: 53; persistent (alive >= 50% of run): 0; longest 6 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 0.00 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [7, 3, 1], H1 [5, 4, 0]
- motion: 0 long-lived tracks moved >= 1 body length; max speed 0/time; max body lengths 1.0
- replication (lineage window K = 20 frames = time 20, default): splits 1, persistent splits 0 (0 more failed only because the siblings re-merged within K), max generation 0, merges 0, merge/split ratio 0, nucleations 51
- channel total drift (end/start - 1): [-0.8036, -0.6854, -0.4968]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 0 at frame 7: holes 0, rim-vs-core 0.01, rim-vs-outside 0.01, heterogeneity 0.01; core [1.0, 0.987, 0.0] rim [1.0, 0.984, 0.005]
  - track 7 at frame 7: holes 0, rim-vs-core 0.00, rim-vs-outside 0.03, heterogeneity 0.00; core [1.0, 1.0, 0.0] rim [1.0, 0.996, 0.0]
  - track 11 at frame 8: holes 0, rim-vs-core 0.01, rim-vs-outside 0.02, heterogeneity 0.00; core [1.0, 1.0, 0.0] rim [1.0, 0.993, 0.0]
  - track 25 at frame 8: holes 0, rim-vs-core 0.00, rim-vs-outside 0.01, heterogeneity 0.00; core [1.0, 1.0, 0.0] rim [1.0, 1.0, 0.0]
- radial profiles: no component with area >= 12 px at the sampled frames

## Warnings
- no components at the end: matter died out or fell below threshold
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
