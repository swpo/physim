# Evidence pack: reacting-thermals (seed 31)

- world: `../../../../../../../../home/user/physim/research/alife/collective/contrib/20261027T0222-c49-thermals-selection-claim/world.py`, family `reactive-convection`
- parent: None; mutation: -
- run: 1201 frames x 25 steps x dt 0.04 = time 1200; grid [128, 128]; wall 146s; status ok
- command: `python -m labkit.run collective/contrib/20261027T0222-c49-thermals-selection-claim/world.py --out /tmp/claude-0/-home-user-physim/cb6f7f87-7e13-5a25-b6c0-c6ef3066597c/scratchpad/rev/neu --seeds 31 32 --frames 1200 --spf 25 --no-movie`
- segmentation: matter > 0.39 of robust range [0.0, 0.645], min area 6 px

## Measurements
- components: final 0, mean 0.3, max 47; occupancy final 0.00
- tracks: 121; persistent (alive >= 50% of run): 0; longest 20 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 0.00 (1 = constant size)
- enclosures: components with a hole mean 0.01, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [0, 0, 0], H1 [0, 0, 0]
- motion: 0 long-lived tracks moved >= 1 body length; max speed 0/time; max body lengths 2.5
- replication (lineage window K = 20 frames = time 20, default): splits 32, persistent splits 0 (0 more failed only because the siblings re-merged within K), max generation 0, merges 11, merge/split ratio 0.344, nucleations 3
- channel total drift (end/start - 1): [-1.0, 0.0, None, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 30 at frame 10: holes 0, rim-vs-core 0.02, rim-vs-outside 0.42, heterogeneity 0.01; core [1.0, 0.0, 0.0, 0.0] rim [0.996, 0.016, 0.0, 0.0]
  - track 99 at frame 20: holes 0, rim-vs-core 0.00, rim-vs-outside 0.18, heterogeneity 0.00; core [1.0, 0.0, 0.0, 0.0] rim [1.0, 0.0, 0.0, 0.0]
  - track 0 at frame 10: holes 0, rim-vs-core 0.00, rim-vs-outside 0.68, heterogeneity 0.00; core [1.0, 0.0, 0.0, 0.0] rim [1.0, 0.004, 0.0, 0.0]
- radial profiles: no component with area >= 12 px at the sampled frames

## Warnings
- no components at the end: matter died out or fell below threshold
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
