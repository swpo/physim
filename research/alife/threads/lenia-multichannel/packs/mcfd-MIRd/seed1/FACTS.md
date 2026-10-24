# Evidence pack: mcfd-MIRd (seed 1)

- world: `../../../../../../../home/user/physim/research/alife/threads/lenia-multichannel/worlds/mcfd-MIRd/world.py`, family `lenia`
- parent: mcf-MIRd; mutation: add a maintenance cost: all matter decays at rate 0.03 and must be rebuilt from food (no free dormancy)
- run: 701 frames x 20 steps x dt 0.1 = time 1400; grid [128, 128]; wall 149s; status ok
- command: `python -m labkit.run threads/lenia-multichannel/worlds/mcfd-MIRd/world.py --out /tmp/claude-0/-home-user-physim/e4674508-87bc-52b7-a806-6cc562392579/scratchpad/pk11b --seeds 1 2 --frames 700 --no-movie`
- segmentation: matter > 0.35 of robust range [0.0, 0.997], min area 6 px

## Measurements
- components: final 6, mean 9.6, max 25; occupancy final 0.06
- tracks: 1538; persistent (alive >= 50% of run): 0; longest 133 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 0.00 (1 = constant size)
- enclosures: components with a hole mean 0.47, final 0; holes at thresholds 0.2/0.35/0.5 final [1, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [15, 6, 6], H1 [1, 0, 0]
- motion: 2 long-lived tracks moved >= 1 body length; max speed 0.102/time; max body lengths 3.3
- replication: splits 397, persistent splits 0, max generation 0, merges 290, nucleations 465
- channel total drift (end/start - 1): [3.5518, 2.7135, 2.6423, -0.4923]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 16 at frame 100: holes 0, rim-vs-core 0.16, rim-vs-outside 1.02, heterogeneity 0.24; core [1.0, 0.952, 0.229, 0.159] rim [0.879, 0.856, 0.266, 0.188]
  - track 57 at frame 106: holes 0, rim-vs-core 0.58, rim-vs-outside 0.99, heterogeneity 0.26; core [1.0, 0.634, 0.479, 0.197] rim [0.861, 1.0, 0.055, 0.244]
  - track 76 at frame 106: holes 0, rim-vs-core 0.20, rim-vs-outside 0.93, heterogeneity 0.25; core [1.0, 0.861, 0.342, 0.101] rim [0.83, 0.873, 0.257, 0.147]
  - track 601 at frame 300: holes 0, rim-vs-core 0.21, rim-vs-outside 0.93, heterogeneity 0.26; core [1.0, 0.795, 0.26, 0.179] rim [0.819, 0.809, 0.173, 0.241]

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, lineage.png, timeseries.png, movie.mp4, metrics.json

Measurements are screens, not verdicts: judge them against the images.
