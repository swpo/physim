# Evidence pack: mc-MIRd (seed 0)

- world: `../../../worlds/mc-MIRd/world.py`, family `lenia`
- parent: Chakazul/Lenia found/233.json#M4HFAN<A39RG5; mutation: reference creature in this thread's multi-channel engine
- run: 201 frames x 10 steps x dt 0.1 = time 200; grid [192, 192]; wall 39s; status ok
- command: `python -m labkit.run threads/lenia-multichannel/worlds/mc-MIRd/world.py --out threads/lenia-multichannel/packs/mc-MIRd --seeds 0 1 2 --frames 200`
- segmentation: matter > 0.35 of robust range [0.0, 1.0], min area 6 px

## Measurements
- components: final 42, mean 18.9, max 42; occupancy final 0.17
- tracks: 300; persistent (alive >= 50% of run): 2; longest 116 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 1.51 (1 = constant size)
- enclosures: components with a hole mean 0.34, final 1; holes at thresholds 0.2/0.35/0.5 final [0, 1, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [88, 52, 40], H1 [1, 1, 0]
- motion: 3 long-lived tracks moved >= 1 body length; max speed 0.71/time; max body lengths 1.5
- replication: splits 103, persistent splits 16, max generation 4, merges 41, nucleations 54
- channel total drift (end/start - 1): [27.2714, 19.7066, 14.4284]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 55 at frame 143: holes 0, rim-vs-core 0.24, rim-vs-outside 0.95, heterogeneity 0.30; core [1.0, 0.89, 0.261] rim [0.802, 0.902, 0.125]
  - track 74 at frame 150: holes 0, rim-vs-core 0.51, rim-vs-outside 0.79, heterogeneity 0.32; core [0.995, 0.966, 0.315] rim [0.767, 0.55, 0.12]
  - track 119 at frame 158: holes 0, rim-vs-core 0.28, rim-vs-outside 0.94, heterogeneity 0.29; core [0.999, 0.973, 0.344] rim [0.798, 0.917, 0.158]
  - track 164 at frame 166: holes 0, rim-vs-core 0.29, rim-vs-outside 0.82, heterogeneity 0.31; core [0.992, 0.953, 0.25] rim [0.751, 0.791, 0.237]

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, lineage.png, timeseries.png, movie.mp4, metrics.json

Measurements are screens, not verdicts: judge them against the images.
