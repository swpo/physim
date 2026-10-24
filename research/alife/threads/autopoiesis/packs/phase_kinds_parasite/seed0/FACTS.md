# Evidence pack: phase-kinds-parasite (seed 0)

- world: `../../../worlds/phase_kinds_parasite/world.py`, family `autopoiesis`
- parent: threads/autopoiesis/worlds/phase_kinds; mutation: mutant kind K2 is selfish: faster (c2=0.3 vs 0.2) but makes no links (b2=0)
- run: 161 frames x 200 steps x dt 1.0 = time 32000; grid [128, 128]; wall 49s; status ok
- command: `python -m labkit.run threads/autopoiesis/worlds/phase_kinds_parasite/world.py --out threads/autopoiesis/packs/phase_kinds_parasite --seeds 0 1 2 --frames 160 --spf 200`
- segmentation: matter > 0.35 of robust range [0.0, 1.5252], min area 6 px

## Measurements
- components: final 0, mean 18.0, max 45; occupancy final 0.00
- tracks: 158; persistent (alive >= 50% of run): 2; longest 93 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 3.04 (1 = constant size)
- enclosures: components with a hole mean 1.03, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [0, 0, 0], H1 [0, 0, 0]
- motion: 7 long-lived tracks moved >= 1 body length; max speed 0.00395/time; max body lengths 1.8
- replication: splits 76, persistent splits 31, max generation 3, merges 0, nucleations 0
- channel total drift (end/start - 1): [0.006, -1.0, None, -1.0, -1.0]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 50 at frame 73: holes 0, rim-vs-core 0.48, rim-vs-outside 1.06, heterogeneity 0.16; core [0.085, 0.933, 0.0, 0.872, 0.612] rim [0.268, 0.52, 0.0, 0.758, 0.71]
  - track 52 at frame 69: holes 0, rim-vs-core 0.45, rim-vs-outside 1.07, heterogeneity 0.15; core [0.077, 0.914, 0.0, 0.837, 0.598] rim [0.263, 0.538, 0.0, 0.776, 0.739]
  - track 47 at frame 62: holes 0, rim-vs-core 0.29, rim-vs-outside 1.13, heterogeneity 0.15; core [0.103, 0.915, 0.0, 0.88, 0.715] rim [0.199, 0.667, 0.0, 0.795, 0.645]
  - track 68 at frame 70: holes 0, rim-vs-core 0.48, rim-vs-outside 1.03, heterogeneity 0.15; core [0.08, 0.911, 0.0, 0.836, 0.597] rim [0.279, 0.497, 0.0, 0.746, 0.698]

## Warnings
- no components at the end: matter died out or fell below threshold
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, lineage.png, timeseries.png, movie.mp4, metrics.json

Measurements are screens, not verdicts: judge them against the images.
