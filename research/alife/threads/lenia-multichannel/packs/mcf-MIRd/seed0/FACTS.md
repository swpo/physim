# Evidence pack: mcf-MIRd (seed 0)

- world: `../../../worlds/mcf-MIRd/world.py`, family `lenia`
- parent: mc-MIRd; mutation: matter can only be built from a consumed, regrowing, diffusing food field F (yield 2, regrowth 0.01): replication limited by food
- run: 401 frames x 10 steps x dt 0.1 = time 400; grid [192, 192]; wall 91s; status ok
- command: `python -m labkit.run threads/lenia-multichannel/worlds/mcf-MIRd/world.py --out threads/lenia-multichannel/packs/mcf-MIRd --seeds 0 1 2 --frames 400`
- segmentation: matter > 0.35 of robust range [0.0, 1.0], min area 6 px

## Measurements
- components: final 16, mean 20.6, max 39; occupancy final 0.05
- tracks: 1073; persistent (alive >= 50% of run): 0; longest 125 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 0.00 (1 = constant size)
- enclosures: components with a hole mean 1.06, final 2; holes at thresholds 0.2/0.35/0.5 final [2, 2, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [63, 26, 11], H1 [6, 1, 0]
- motion: 0 long-lived tracks moved >= 1 body length; max speed 0/time; max body lengths 1.5
- replication: splits 296, persistent splits 6, max generation 3, merges 191, nucleations 286
- channel total drift (end/start - 1): [6.6104, 5.2175, 5.3661, -0.6952]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 303 at frame 239: holes 0, rim-vs-core 0.43, rim-vs-outside 1.01, heterogeneity 0.25; core [1.0, 0.719, 0.447, 0.377] rim [0.871, 0.983, 0.132, 0.369]
  - track 390 at frame 245: holes 0, rim-vs-core 0.43, rim-vs-outside 0.96, heterogeneity 0.27; core [1.0, 0.684, 0.434, 0.246] rim [0.838, 0.977, 0.162, 0.247]
  - track 395 at frame 249: holes 0, rim-vs-core 0.29, rim-vs-outside 0.85, heterogeneity 0.26; core [1.0, 0.851, 0.465, 0.194] rim [0.795, 0.879, 0.255, 0.207]
  - track 547 at frame 286: holes 0, rim-vs-core 0.25, rim-vs-outside 1.00, heterogeneity 0.24; core [0.995, 0.791, 0.42, 0.014] rim [0.84, 0.85, 0.238, 0.053]

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, lineage.png, timeseries.png, movie.mp4, metrics.json

Measurements are screens, not verdicts: judge them against the images.
