# Evidence pack: mcfd-MIRd (seed 2)

- world: `../../../../../../../home/user/physim/research/alife/threads/lenia-multichannel/worlds/mcfd-MIRd/world.py`, family `lenia`
- parent: mcf-MIRd; mutation: add a maintenance cost: all matter decays at rate 0.03 and must be rebuilt from food (no free dormancy)
- run: 701 frames x 20 steps x dt 0.1 = time 1400; grid [128, 128]; wall 113s; status ok
- command: `python -m labkit.run threads/lenia-multichannel/worlds/mcfd-MIRd/world.py --out /tmp/claude-0/-home-user-physim/e4674508-87bc-52b7-a806-6cc562392579/scratchpad/pk11b --seeds 1 2 --frames 700 --no-movie`
- segmentation: matter > 0.35 of robust range [0.0, 0.997], min area 6 px

## Measurements
- components: final 10, mean 10.5, max 25; occupancy final 0.06
- tracks: 1771; persistent (alive >= 50% of run): 0; longest 79 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 0.00 (1 = constant size)
- enclosures: components with a hole mean 0.54, final 1; holes at thresholds 0.2/0.35/0.5 final [1, 1, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [32, 12, 6], H1 [5, 2, 0]
- motion: 0 long-lived tracks moved >= 1 body length; max speed 0/time; max body lengths 2.7
- replication: splits 438, persistent splits 0, max generation 0, merges 339, nucleations 571
- channel total drift (end/start - 1): [3.254, 2.5142, 1.5383, -0.5083]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 1085 at frame 500: holes 0, rim-vs-core 0.31, rim-vs-outside 0.98, heterogeneity 0.25; core [0.995, 0.784, 0.354, 0.052] rim [0.777, 0.949, 0.229, 0.132]
  - track 103 at frame 106: holes 0, rim-vs-core 0.30, rim-vs-outside 1.00, heterogeneity 0.25; core [1.0, 0.767, 0.279, 0.102] rim [0.802, 0.973, 0.207, 0.166]
  - track 575 at frame 271: holes 0, rim-vs-core 0.44, rim-vs-outside 0.63, heterogeneity 0.23; core [0.869, 0.182, 0.063, 0.008] rim [0.685, 0.531, 0.243, 0.043]
  - track 237 at frame 141: holes 0, rim-vs-core 0.21, rim-vs-outside 0.90, heterogeneity 0.24; core [0.935, 0.864, 0.232, 0.015] rim [0.745, 0.796, 0.254, 0.078]

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, lineage.png, timeseries.png, movie.mp4, metrics.json

Measurements are screens, not verdicts: judge them against the images.
