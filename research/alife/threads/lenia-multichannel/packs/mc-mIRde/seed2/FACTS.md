# Evidence pack: mc-mIRde (seed 2)

- world: `../../../worlds/mc-mIRde/world.py`, family `lenia`
- parent: Chakazul/Lenia found/233s.json#A39RG5<3G9TC1; mutation: reference creature in this thread's multi-channel engine
- run: 301 frames x 10 steps x dt 0.1 = time 300; grid [192, 192]; wall 53s; status ok
- command: `python -m labkit.run threads/lenia-multichannel/worlds/mc-mIRde/world.py --out threads/lenia-multichannel/packs/mc-mIRde --seeds 0 1 2 --frames 300 --no-movie`
- segmentation: matter > 0.35 of robust range [0.0, 3.0], min area 6 px

## Measurements
- components: final 30, mean 19.8, max 45; occupancy final 0.10
- tracks: 1264; persistent (alive >= 50% of run): 0; longest 65 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 0.00 (1 = constant size)
- enclosures: components with a hole mean 1.19, final 2; holes at thresholds 0.2/0.35/0.5 final [3, 2, 1]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [107, 34, 18], H1 [11, 0, 0]
- motion: 3 long-lived tracks moved >= 1 body length; max speed 0.483/time; max body lengths 2.2
- replication: splits 381, persistent splits 1, max generation 1, merges 212, nucleations 275
- channel total drift (end/start - 1): [9.4317, 6.6575, 4.3485]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 781 at frame 265: holes 0, rim-vs-core 0.24, rim-vs-outside 0.97, heterogeneity 0.37; core [0.838, 0.904, 0.423] rim [0.618, 0.882, 0.328]
  - track 876 at frame 270: holes 0, rim-vs-core 0.38, rim-vs-outside 0.69, heterogeneity 0.39; core [0.833, 0.726, 0.386] rim [0.467, 0.827, 0.36]
  - track 550 at frame 212: holes 0, rim-vs-core 0.26, rim-vs-outside 0.70, heterogeneity 0.35; core [0.699, 0.937, 0.4] rim [0.624, 0.699, 0.313]
  - track 593 at frame 217: holes 0, rim-vs-core 0.12, rim-vs-outside 0.90, heterogeneity 0.38; core [0.67, 0.901, 0.268] rim [0.68, 0.784, 0.312]

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, lineage.png, timeseries.png, movie.mp4, metrics.json

Measurements are screens, not verdicts: judge them against the images.
