# Evidence pack: mc-MIRd (seed 2)

- world: `../../../worlds/mc-MIRd/world.py`, family `lenia`
- parent: Chakazul/Lenia found/233.json#M4HFAN<A39RG5; mutation: reference creature in this thread's multi-channel engine
- run: 201 frames x 10 steps x dt 0.1 = time 200; grid [192, 192]; wall 34s; status ok
- command: `python -m labkit.run threads/lenia-multichannel/worlds/mc-MIRd/world.py --out threads/lenia-multichannel/packs/mc-MIRd --seeds 0 1 2 --frames 200`
- segmentation: matter > 0.35 of robust range [0.0, 1.0], min area 6 px

## Measurements
- components: final 38, mean 17.1, max 41; occupancy final 0.16
- tracks: 246; persistent (alive >= 50% of run): 2; longest 114 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 1.17 (1 = constant size)
- enclosures: components with a hole mean 0.18, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [85, 53, 38], H1 [0, 0, 0]
- motion: 5 long-lived tracks moved >= 1 body length; max speed 0.836/time; max body lengths 3.1
- replication: splits 81, persistent splits 17, max generation 4, merges 41, nucleations 52
- channel total drift (end/start - 1): [25.843, 18.9994, 14.0849]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 51 at frame 145: holes 0, rim-vs-core 0.25, rim-vs-outside 0.92, heterogeneity 0.34; core [1.0, 0.75, 0.294] rim [0.821, 0.819, 0.136]
  - track 53 at frame 146: holes 0, rim-vs-core 0.40, rim-vs-outside 0.94, heterogeneity 0.34; core [1.0, 0.718, 0.361] rim [0.83, 0.942, 0.081]
  - track 76 at frame 153: holes 0, rim-vs-core 0.20, rim-vs-outside 0.95, heterogeneity 0.34; core [1.0, 0.732, 0.417] rim [0.874, 0.861, 0.326]
  - track 139 at frame 170: holes 0, rim-vs-core 0.49, rim-vs-outside 0.98, heterogeneity 0.34; core [1.0, 0.639, 0.448] rim [0.867, 0.999, 0.145]

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, lineage.png, timeseries.png, movie.mp4, metrics.json

Measurements are screens, not verdicts: judge them against the images.
