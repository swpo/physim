# Evidence pack: mcg-MIRd-neutral (seed 1)

- world: `../../../worlds/mcg-MIRd-neutral/world.py`, family `lenia`
- parent: mcg-MIRd; mutation: NEUTRAL CONTROL of mcg-MIRd: identical heredity and mutation, SEL=0 so the trait has no effect
- run: 501 frames x 20 steps x dt 0.1 = time 1000; grid [160, 160]; wall 151s; status ok
- command: `python -m labkit.run threads/lenia-multichannel/worlds/mcg-MIRd-neutral/world.py --out threads/lenia-multichannel/packs/mcg-MIRd-neutral --seeds 0 1 2 --frames 500 --size 160 160 --no-movie`
- segmentation: matter > 0.35 of robust range [0.0, 0.997], min area 6 px

## Measurements
- components: final 11, mean 14.7, max 27; occupancy final 0.05
- tracks: 1772; persistent (alive >= 50% of run): 0; longest 104 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 0.00 (1 = constant size)
- enclosures: components with a hole mean 0.74, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [22, 12, 8], H1 [2, 0, 0]
- motion: 1 long-lived tracks moved >= 1 body length; max speed 0.287/time; max body lengths 2.4
- replication: splits 466, persistent splits 0, max generation 0, merges 326, nucleations 539
- channel total drift (end/start - 1): [4.6985, 3.8854, 3.3416, -0.4063, None, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 137 at frame 134: holes 0, rim-vs-core 0.56, rim-vs-outside 0.97, heterogeneity 0.18; core [1.0, 0.636, 0.489, 0.171, 0.289, 0.0] rim [0.821, 1.0, 0.106, 0.223, 0.289, 0.0]
  - track 944 at frame 336: holes 0, rim-vs-core 0.29, rim-vs-outside 0.92, heterogeneity 0.18; core [0.977, 0.709, 0.259, 0.028, 0.078, 0.0] rim [0.783, 0.903, 0.189, 0.094, 0.08, 0.0]
  - track 849 at frame 311: holes 0, rim-vs-core 0.58, rim-vs-outside 0.97, heterogeneity 0.17; core [1.0, 0.571, 0.454, 0.145, 0.477, 0.0] rim [0.889, 0.992, 0.082, 0.182, 0.477, 0.0]
  - track 1579 at frame 454: holes 0, rim-vs-core 0.37, rim-vs-outside 0.61, heterogeneity 0.13; core [0.864, 0.193, 0.03, 0.003, 0.339, 0.0] rim [0.664, 0.45, 0.191, 0.04, 0.339, 0.0]

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, lineage.png, timeseries.png, movie.mp4, metrics.json

Measurements are screens, not verdicts: judge them against the images.
