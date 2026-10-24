# Evidence pack: mcg-MIRd-neutral (seed 2)

- world: `../../../worlds/mcg-MIRd-neutral/world.py`, family `lenia`
- parent: mcg-MIRd; mutation: NEUTRAL CONTROL of mcg-MIRd: identical heredity and mutation, SEL=0 so the trait has no effect
- run: 501 frames x 20 steps x dt 0.1 = time 1000; grid [160, 160]; wall 142s; status ok
- command: `python -m labkit.run threads/lenia-multichannel/worlds/mcg-MIRd-neutral/world.py --out threads/lenia-multichannel/packs/mcg-MIRd-neutral --seeds 0 1 2 --frames 500 --size 160 160 --no-movie`
- segmentation: matter > 0.35 of robust range [0.0, 0.997], min area 6 px

## Measurements
- components: final 16, mean 17.4, max 38; occupancy final 0.06
- tracks: 2091; persistent (alive >= 50% of run): 0; longest 127 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 0.00 (1 = constant size)
- enclosures: components with a hole mean 0.90, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 3]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [59, 23, 10], H1 [6, 0, 0]
- motion: 2 long-lived tracks moved >= 1 body length; max speed 0.336/time; max body lengths 2.9
- replication: splits 539, persistent splits 0, max generation 0, merges 383, nucleations 645
- channel total drift (end/start - 1): [5.3314, 4.775, 3.1381, -0.6176, None, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 277 at frame 181: holes 0, rim-vs-core 0.23, rim-vs-outside 0.95, heterogeneity 0.17; core [0.996, 0.852, 0.198, 0.079, 0.0, 0.087] rim [0.805, 0.818, 0.295, 0.145, 0.0, 0.086]
  - track 92 at frame 130: holes 0, rim-vs-core 0.50, rim-vs-outside 0.96, heterogeneity 0.19; core [1.0, 0.699, 0.537, 0.176, 0.0, 0.206] rim [0.823, 0.991, 0.182, 0.239, 0.0, 0.169]
  - track 163 at frame 139: holes 0, rim-vs-core 0.30, rim-vs-outside 0.95, heterogeneity 0.17; core [1.0, 0.815, 0.352, 0.109, 0.077, 0.0] rim [0.813, 0.927, 0.16, 0.174, 0.076, 0.0]
  - track 60 at frame 97: holes 0, rim-vs-core 0.27, rim-vs-outside 0.89, heterogeneity 0.14; core [0.987, 1.0, 0.122, 0.178, 0.0, 0.545] rim [0.78, 0.853, 0.192, 0.238, 0.0, 0.545]

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, lineage.png, timeseries.png, movie.mp4, metrics.json

Measurements are screens, not verdicts: judge them against the images.
