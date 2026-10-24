# Evidence pack: phase-protocell-notilt (seed 0)

- world: `../../worlds/phase_protocell_notilt/world.py`, family `autopoiesis`
- parent: threads/autopoiesis/worlds/phase_protocell; mutation: ABLATION: links do not tilt the phase (no L -> boundary feedback)
- run: 81 frames x 50 steps x dt 1.0 = time 4000; grid [128, 128]; wall 5s; status ok
- command: `python -m labkit.run threads/autopoiesis/worlds/phase_protocell_notilt/world.py --out threads/autopoiesis/packs/phase_protocell_notilt --frames 80 --no-movie`
- segmentation: matter > 0.35 of robust range [0.0, 0.9973], min area 6 px

## Measurements
- components: final 0, mean 0.2, max 4; occupancy final 0.00
- tracks: 4; persistent (alive >= 50% of run): 0; longest 5 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 0.00 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [0, 0, 0], H1 [0, 0, 0]
- motion: 0 long-lived tracks moved >= 1 body length; max speed 0/time; max body lengths 0.0
- replication: splits 0, persistent splits 0, max generation 0, merges 0, nucleations 0
- channel total drift (end/start - 1): [0.006, -1.0, -1.0, -1.0]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 0 at frame 2: holes 0, rim-vs-core 0.00, rim-vs-outside 0.68, heterogeneity 0.00; core [0.0, 1.0, 1.0, 1.0] rim [0.0, 1.0, 1.0, 1.0]
  - track 1 at frame 2: holes 0, rim-vs-core 0.00, rim-vs-outside 0.68, heterogeneity 0.00; core [0.0, 1.0, 1.0, 1.0] rim [0.0, 1.0, 1.0, 1.0]
  - track 2 at frame 2: holes 0, rim-vs-core 0.00, rim-vs-outside 0.69, heterogeneity 0.00; core [0.0, 1.0, 1.0, 1.0] rim [0.0, 1.0, 1.0, 1.0]
  - track 3 at frame 2: holes 0, rim-vs-core 0.00, rim-vs-outside 0.69, heterogeneity 0.00; core [0.0, 1.0, 1.0, 1.0] rim [0.0, 1.0, 1.0, 1.0]

## Warnings
- no components at the end: matter died out or fell below threshold
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, lineage.png, timeseries.png, movie.mp4, metrics.json

Measurements are screens, not verdicts: judge them against the images.
