# Evidence pack: membrane-evo-up (seed 41)

- world: `../../../../../../../home/user/physim/research/alife/threads/autopoiesis/worlds/membrane_evo_up/world.py`, family `autopoiesis`
- parent: threads/autopoiesis/worlds/membrane_evo (identical-event twin); mutation: K2 link yield b2 = 1.3 b (b = 0.065); same event RNG as the twin membrane_evo
- run: 161 frames x 250 steps x dt 1.0 = time 40000; grid [128, 128]; wall 104s; status ok
- command: `python -m labkit.run threads/autopoiesis/worlds/membrane_evo_up/world.py --out /tmp/claude-0/-home-user-physim/fba552f4-82e1-5fd3-8aee-1d1a9784fecc/scratchpad/rev7/lk --seeds 41 --frames 160 --spf 250 --no-movie`
- segmentation: matter > 0.35 of robust range [0.0, 1.3324], min area 6 px

## Measurements
- components: final 0, mean 0.1, max 13; occupancy final 0.00
- tracks: 13; persistent (alive >= 50% of run): 0; longest 1 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 0.00 (1 = constant size)
- enclosures: components with a hole mean 0.01, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [0, 0, 0], H1 [0, 0, 0]
- motion: 0 long-lived tracks moved >= 1 body length; max speed 0/time; max body lengths 0.0
- replication (lineage window K = 20 frames = time 5000, default): splits 0, persistent splits 0 (0 more failed only because the siblings re-merged within K), max generation 0, merges 0, merge/split ratio n/a, nucleations 0
- channel total drift (end/start - 1): [-1.0, None, -1.0, -1.0]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 0 at frame 0: holes 3, rim-vs-core 0.04, rim-vs-outside 0.81, heterogeneity 0.20; core [0.795, 0.0, 0.81, 1.0] rim [0.805, 0.0, 0.808, 0.963]
  - track 1 at frame 0: holes 0, rim-vs-core 0.11, rim-vs-outside 0.71, heterogeneity 0.20; core [0.807, 0.0, 0.763, 1.0] rim [0.884, 0.0, 0.763, 0.923]
  - track 2 at frame 0: holes 0, rim-vs-core 0.09, rim-vs-outside 0.77, heterogeneity 0.21; core [0.835, 0.0, 0.815, 1.0] rim [0.825, 0.0, 0.799, 0.916]
  - track 3 at frame 0: holes 0, rim-vs-core 0.15, rim-vs-outside 0.34, heterogeneity 0.13; core [0.814, 0.0, 0.794, 1.0] rim [0.905, 0.0, 0.917, 1.0]
- radial profiles: no component with area >= 12 px at the sampled frames

## Warnings
- no components at the end: matter died out or fell below threshold
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
