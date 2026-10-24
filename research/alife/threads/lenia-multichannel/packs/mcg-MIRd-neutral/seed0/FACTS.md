# Evidence pack: mcg-MIRd-neutral (seed 0)

- world: `../../../worlds/mcg-MIRd-neutral/world.py`, family `lenia`
- parent: mcg-MIRd; mutation: NEUTRAL CONTROL of mcg-MIRd: identical heredity and mutation, SEL=0 so the trait has no effect
- run: 501 frames x 20 steps x dt 0.1 = time 1000; grid [160, 160]; wall 182s; status ok
- command: `python -m labkit.run threads/lenia-multichannel/worlds/mcg-MIRd-neutral/world.py --out threads/lenia-multichannel/packs/mcg-MIRd-neutral --seeds 0 1 2 --frames 500 --size 160 160 --no-movie`
- segmentation: matter > 0.35 of robust range [0.0, 0.997], min area 6 px

## Measurements
- components: final 12, mean 13.3, max 38; occupancy final 0.06
- tracks: 1608; persistent (alive >= 50% of run): 0; longest 94 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 0.00 (1 = constant size)
- enclosures: components with a hole mean 0.56, final 0; holes at thresholds 0.2/0.35/0.5 final [1, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [33, 15, 9], H1 [2, 0, 0]
- motion: 0 long-lived tracks moved >= 1 body length; max speed 0/time; max body lengths 2.5
- replication: splits 408, persistent splits 0, max generation 0, merges 298, nucleations 501
- channel total drift (end/start - 1): [5.5005, 4.8269, 4.2216, -0.3943, None, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 144 at frame 130: holes 0, rim-vs-core 0.35, rim-vs-outside 1.02, heterogeneity 0.19; core [0.994, 0.813, 0.472, 0.041, 0.384, 0.0] rim [0.794, 0.918, 0.221, 0.115, 0.371, 0.0]
  - track 155 at frame 122: holes 0, rim-vs-core 0.32, rim-vs-outside 0.83, heterogeneity 0.19; core [0.997, 0.613, 0.207, 0.116, 0.947, 0.0] rim [0.751, 0.808, 0.149, 0.169, 0.923, 0.0]
  - track 1232 at frame 378: holes 0, rim-vs-core 0.63, rim-vs-outside 0.98, heterogeneity 0.18; core [1.0, 0.632, 0.568, 0.105, 0.0, 0.305] rim [0.864, 0.997, 0.075, 0.165, 0.0, 0.306]
  - track 73 at frame 92: holes 0, rim-vs-core 0.23, rim-vs-outside 0.89, heterogeneity 0.15; core [0.995, 0.989, 0.25, 0.14, 0.126, 0.0] rim [0.814, 0.867, 0.184, 0.155, 0.117, 0.0]

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, lineage.png, timeseries.png, movie.mp4, metrics.json

Measurements are screens, not verdicts: judge them against the images.
