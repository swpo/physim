# Evidence pack: crawler (seed 0)

- world: `../../crawler.py`, family `phase-field`
- parent: None; mutation: Ziebert-Aranson crawling cell, body-wise area constraint
- run: 241 frames x 50 steps x dt 0.05 = time 600; grid [256, 256]; wall 128s; status ok
- command: `python -m labkit.run /tmp/claude-0/-home-user-physim/fba552f4-82e1-5fd3-8aee-1d1a9784fecc/scratchpad/cr/crawler.py --out /tmp/claude-0/-home-user-physim/fba552f4-82e1-5fd3-8aee-1d1a9784fecc/scratchpad/cr/K_ok0 --seeds 0 1 --frames 240 --threshold 0.25 --no-movie`
- segmentation: matter > 0.44 of robust range [-0.0, 0.5703], min area 6 px

## Measurements
- components: final 0, mean 0.1, max 1; occupancy final 0.00
- tracks: 1; persistent (alive >= 50% of run): 0; longest 20 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 0.00 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [0, 0, 0], H1 [0, 0, 0]
- motion: 1 long-lived tracks moved >= 1 body length; max speed 3.35/time; max body lengths 4.5
- replication (lineage window K = 20 frames = time 50, default): splits 0, persistent splits 0 (0 more failed only because the siblings re-merged within K), max generation 0, merges 0, merge/split ratio n/a, nucleations 0
- channel total drift (end/start - 1): [-1.0, -1.0, None, -0.0206]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 0 at frame 10: holes 0, rim-vs-core 0.12, rim-vs-outside 0.63, heterogeneity 0.07; core [1.0, 0.983, 1.0, 0.223] rim [1.0, 1.0, 1.0, 0.347]
- radial profiles: no component with area >= 12 px at the sampled frames

## Warnings
- no components at the end: matter died out or fell below threshold
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
